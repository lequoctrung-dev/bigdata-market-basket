package vn.edu.bigdata.m1;

import org.bson.Document;
import org.junit.jupiter.api.Test;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

/** Every final query: Java order AND best antecedent, plus train-only baseline. */
class M5FinalRankingTest {
    @Test void realFinalPredictionsMatchBothMethods() throws Exception {
        String directory=System.getProperty("m5.runDirectory");
        assumeTrue(directory!=null,"Supply -Dm5.runDirectory=<FINAL run folder>");
        Path path=Path.of(directory);
        Document receipt=Document.parse(Files.readString(path.resolve("receipt.json"),StandardCharsets.UTF_8));
        assertEquals("PASS",receipt.getString("status"));assertEquals("FINAL",receipt.getString("evaluation_stage"));
        List<RuleRanking.Rule> rules=new ArrayList<>();
        for(String line:Files.readAllLines(path.resolve("association_rules.jsonl"),StandardCharsets.UTF_8)) {
            Document r=Document.parse(line);
            rules.add(new RuleRanking.Rule(r.getList("antecedent",String.class),r.getString("consequent"),
                ((Number)r.get("support")).doubleValue(),((Number)r.get("confidence")).doubleValue(),((Number)r.get("lift")).doubleValue()));
        }
        List<Document> catalog=new ArrayList<>();
        for(String line:Files.readAllLines(path.resolve("items.jsonl"),StandardCharsets.UTF_8)) catalog.add(Document.parse(line));
        catalog.sort(Comparator.<Document>comparingLong(r->((Number)r.get("train_basket_count")).longValue()).reversed()
            .thenComparing(r->r.getString("stock_code"),RuleRanking::codePointOrder));
        int k=((Number)receipt.get("config",Document.class).get("k")).intValue(), n=0;
        long hits=0,nonempty=0,baselineHits=0,baselineNonempty=0;
        for(String line:Files.readAllLines(path.resolve("test-predictions.jsonl"),StandardCharsets.UTF_8)) {
            Document q=Document.parse(line);List<String> query=q.getList("query",String.class);
            var answer=RuleRanking.recommend(rules,query,k);
            assertEquals(q.getList("rules",String.class),answer.stream().map(RuleRanking.Rule::consequent).toList(),q.getString("invoice"));
            var best=q.getList("best_rules",Document.class);assertEquals(answer.size(),best.size());
            for(int i=0;i<answer.size();i++) {
                assertEquals(answer.get(i).antecedent(),best.get(i).getList("antecedent",String.class));
                assertEquals(answer.get(i).consequent(),best.get(i).getString("consequent"));
            }
            var baseline=catalog.stream().map(r->r.getString("stock_code")).filter(c->!query.contains(c)).limit(k).toList();
            assertEquals(q.getList("baseline",String.class),baseline);
            if(answer.stream().anyMatch(r->r.consequent().equals(q.getString("target")))) hits++;
            if(!answer.isEmpty()) nonempty++;
            if(baseline.contains(q.getString("target"))) baselineHits++;
            if(!baseline.isEmpty()) baselineNonempty++;
            n++;
        }
        assertEquals(((Number)receipt.get("counts",Document.class).get("eligible_test_queries")).intValue(),n);
        var all=receipt.get("final",Document.class).get("all",Document.class);
        assertEquals(((Number)all.get("rules",Document.class).get("hits")).longValue(),hits);
        assertEquals(((Number)all.get("rules",Document.class).get("with_recommendations")).longValue(),nonempty);
        assertEquals(((Number)all.get("baseline",Document.class).get("hits")).longValue(),baselineHits);
        assertEquals(((Number)all.get("baseline",Document.class).get("with_recommendations")).longValue(),baselineNonempty);
    }
}
