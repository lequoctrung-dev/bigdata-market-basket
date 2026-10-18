package vn.edu.bigdata.m1;

import com.mongodb.MongoTimeoutException;
import org.bson.Document;
import org.junit.jupiter.api.Test;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.server.context.WebServerApplicationContext;
import org.springframework.context.annotation.*;

import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.*;

/** Isolated synthetic probe: real MVC/Thymeleaf/HTTP, no Mongo writes or fixture publication. */
class AnalysisWebTest {
    static final AtomicReference<Object> result=new AtomicReference<>();
    @Configuration(proxyBeanMethods=false)
    static class ProbeConfiguration {
        @Bean @Primary AnalysisResults probeResults() {
            return new AnalysisResults(null) {
                @Override Snapshot snapshot() {
                    Object current=result.get();
                    if(current instanceof RuntimeException e) throw e;
                    return (Snapshot) current;
                }
            };
        }
    }
    record Fixture(Document pointer,Document run,Document pre,Document dataset,List<Document> catalog,List<Document> sets,List<Document> rules,List<Document> summaries) {
        AnalysisResults.Snapshot snapshot() { return AnalysisResults.assemble(pointer,run,pre,dataset,catalog,sets,rules,summaries); }
    }
    static Document d(Object... values) { Document d=new Document();for(int i=0;i<values.length;i+=2) d.put((String)values[i],values[i+1]);return d; }
    static Fixture fixture() {
        Document stages=d("baskets",2L,"items",2L,"summaries",5L,"raw",3L,"duplicates",0L,"retained",3L,
            "positive_valid",3L,"invalid_or_nonpositive",0L,"excluded",0L,"merchandise",3L,"single_item_baskets",1L,
            "multi_item_baskets",1L,"merchandise_missing_customer",0L);
        Document config=d("k",5L);
        Document metric=d("queries",0L,"hits",0L,"with_recommendations",0L,"status","NOT_APPLICABLE","recall_at_k",null,"recommendation_rate",null);
        Document m=d("status","PASS","run_id","fixture","evaluation_stage","DEVELOPMENT","final_status","NOT_RUN",
            "schema_version",AnalysisResults.SCHEMA,"config",config,"dataset_id","synthetic","basket_set_id","basket",
            "protocol",d("k",5L,"ranking_version",AnalysisResults.RANKING,"version","m3-temporal-hide-one-v1"),
            "stage_counts",stages,"counts",d("train_items",2L,"train_baskets",2L,"itemsets",0L,"rules",0L,"eligible_dev_queries",0L),
            "output_validation",d("items",d("expected",2L,"actual",2L,"checksum","a".repeat(64)),"frequent_itemsets",d("expected",0L,"actual",0L,"checksum","b".repeat(64)),"association_rules",d("expected",0L,"actual",0L,"checksum","c".repeat(64))),
            "development",d("all",d("rules",metric,"baseline",metric)),"split",d("train",d("baskets",2L)),"new_items",d());
        Document run=d("_id","fixture","status","READY","mode","FULL_SOURCE","stage","MODEL_DEVELOPMENT","evaluation_stage","DEVELOPMENT",
            "schema_version",AnalysisResults.SCHEMA,"basket_set_id","basket","dataset_id","synthetic","ranking_version",AnalysisResults.RANKING,
            "policy_hash","policy","policy_version","fixture-policy","manifest",m,"config",config);
        Document pre=d("status","VALIDATED","basket_set_status","READY","stage","PREPROCESSING","schema_version",AnalysisResults.SCHEMA,
            "basket_set_id","basket","dataset_id","synthetic","manifest",d("policy_hash","policy","status","PASS","counts",stages,"merchandise_value_gbp","1.005"));
        List<Document> summaries=new ArrayList<>();
        for(Document s:List.of(d("summary_type","month","bucket_key","2010-01","payload",d("invoices",2L,"line_value_gbp","1.005")),
            d("summary_type","basket_size","bucket_key","1","payload",d("baskets",1L)),
            d("summary_type","basket_size","bucket_key","2","payload",d("baskets",1L)),
            d("summary_type","item","bucket_key","A","payload",d("baskets",2L,"quantity",2L)),
            d("summary_type","item","bucket_key","B","payload",d("baskets",1L,"quantity",1L)))) {
            summaries.add(s.append("basket_set_id","basket").append("policy_hash","policy").append("scope","merchandise").append("denominator_baskets",2L));
        }
        Document qualityStages=new Document();
        for(String field:List.of("raw","duplicates","retained","invalid_or_nonpositive","positive_valid","excluded","merchandise","merchandise_missing_customer")) qualityStages.put(field,stages.get(field));
        summaries.add(d("basket_set_id","basket","policy_hash","policy","scope","raw","summary_type","quality","bucket_key","all",
            "payload",d("stage_counts",qualityStages,"overlapping_retained_quality",d("missing_customer",0L),"excluded_positive_rows",d())));
        stages.put("summaries",6L);
        return new Fixture(d("run_id","fixture","basket_set_id","basket","schema_version",AnalysisResults.SCHEMA,"version",1L),run,pre,d("status","READY"),
            List.of(d("_id","A","run_id","fixture","stock_code","A","display_name","<script>alert('x')</script>","train_basket_count",2L),
                d("_id","B","run_id","fixture","stock_code","B","display_name","Tên B & <img src=x onerror=alert(1)>","train_basket_count",1L)),List.of(),List.of(),summaries);
    }
    @Test void manifestConfirmedZeroRulesAndMoneyAreValid() {
        var snapshot=fixture().snapshot(); assertTrue(snapshot.rules().isEmpty());assertEquals("1.01",snapshot.gbp());assertEquals(2,snapshot.items().size());
    }
    @Test void missingMismatchedAndUnsupportedDataFailClosed() {
        Fixture f=fixture();f.pointer.put("schema_version","future");assertThrows(AnalysisResults.Unavailable.class,f::snapshot);
        f=fixture();f.run.put("status","WRITING");assertThrows(AnalysisResults.Unavailable.class,f::snapshot);
        f=fixture();AnalysisResults.doc(AnalysisResults.doc(f.run,"manifest"),"counts").put("rules",1L);assertThrows(AnalysisResults.Unavailable.class,f::snapshot);
        f=fixture();f.summaries.remove(0);assertThrows(AnalysisResults.Unavailable.class,f::snapshot);
        f=fixture();f.catalog.get(0).put("train_basket_count",2);assertThrows(AnalysisResults.Unavailable.class,f::snapshot);
        f=fixture();f.pre.put("basket_set_status","WRITING");assertThrows(AnalysisResults.Unavailable.class,f::snapshot);
        f=fixture();AnalysisResults.doc(f.run,"manifest").remove("development");assertThrows(AnalysisResults.Unavailable.class,f::snapshot);
    }
    @Test void realHttpRendersEscapedTextAndHandlesInputStaleAndUnavailable() throws Exception {
        result.set(fixture().snapshot());
        try(var context=new SpringApplicationBuilder(SampleApplication.class,ProbeConfiguration.class).run("--server.port=0","--app.mode=DEVELOPMENT")) {
            int port=((WebServerApplicationContext)context).getWebServer().getPort();
            HttpClient client=HttpClient.newHttpClient();
            Function request=new Function(client,port);
            var response=request.get("/basket");assertEquals(200,response.statusCode());
            assertTrue(response.body().contains("&lt;script&gt;"));assertTrue(response.body().contains("&lt;img"));assertFalse(response.body().contains("<script>alert"));
            assertTrue(response.headers().firstValue("content-security-policy").orElse("").contains("script-src 'self'"));
            response=request.post("runId=fixture&version=1&items=A");assertEquals(200,response.statusCode());assertTrue(response.body().contains("Không có luật gợi ý"));
            response=request.post("runId=fixture&version=1&items=A&items=A");assertEquals(200,response.statusCode());
            // A valid large catalog basket must not hit SpEL's string concatenation limit.
            Fixture longNames=fixture();longNames.catalog.get(0).put("display_name","X".repeat(60000));longNames.catalog.get(1).put("display_name","Y".repeat(60000));
            result.set(longNames.snapshot());response=request.post("runId=fixture&version=1&items=A&items=B");
            assertEquals(200,response.statusCode());assertTrue(response.body().contains("X".repeat(60000)));assertTrue(response.body().contains("Y".repeat(60000)));
            result.set(fixture().snapshot());
            response=request.post("runId=fixture&version=1&items=A&items=UNKNOWN");assertEquals(400,response.statusCode());assertTrue(response.body().contains("checked=\"checked\""));
            assertEquals(400,request.post("runId=fixture&version=1").statusCode());
            assertEquals(400,request.post("runId=fixture&version=oops&items=A").statusCode());
            assertEquals(400,request.post("runId=fixture&version=1&items%5B%24ne%5D=A").statusCode());
            response=request.post("runId=fixture&version=0&items=A");assertEquals(409,response.statusCode());assertTrue(response.body().contains("phiên cũ"));
            assertEquals(400,request.get("/patterns?min=NaN").statusCode());
            assertEquals(400,request.get("/?page=-1").statusCode());
            assertEquals(400,request.get("/?sort=%7B%24where:1%7D").statusCode());
            assertEquals(400,request.get("/?page=2").statusCode());
            response=request.get("/patterns");assertEquals(200,response.statusCode());assertTrue(response.body().contains("NOT_APPLICABLE"));assertTrue(response.body().contains("NOT_RUN"));
            result.set(new AnalysisResults.Unavailable("Chưa có lượt dữ liệu được công bố."));
            assertEquals(503,request.get("/").statusCode());
            result.set(new MongoTimeoutException("private_uri_must_not_leak"));response=request.get("/basket");assertEquals(503,response.statusCode());assertFalse(response.body().contains("private_uri"));
        }
    }
    record Function(HttpClient client,int port) {
        HttpResponse<String> get(String path) throws Exception { return client.send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:"+port+path)).GET().build(),HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)); }
        HttpResponse<String> post(String body) throws Exception { return client.send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:"+port+"/recommend")).header("Content-Type","application/x-www-form-urlencoded").POST(HttpRequest.BodyPublishers.ofString(body)).build(),HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)); }
    }
}
