package vn.edu.bigdata.m1;

import com.mongodb.client.model.Filters;
import org.bson.Document;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;

/** Chỉ đọc đúng run của pointer; không fit Spark hoặc ghi MongoDB. */
@Service
public class SampleResults {
    static final String SCHEMA = "m0-contract-v1";
    public record Snapshot(String runId, long version, List<Document> items, List<RuleRanking.Rule> rules,
                    Document run, Document summary, int k) { }
    private final MongoTemplate mongo;

    SampleResults(MongoTemplate mongo) { this.mongo = mongo; }

    Snapshot snapshot() {
        Document pointer = mongo.getCollection("publication").find(Filters.eq("_id", "active")).first();
        if (pointer == null) throw new IllegalStateException("Chưa có lượt mẫu hoàn chỉnh. Chạy batch M1 trước.");
        if (!SCHEMA.equals(pointer.getString("schema_version"))) throw new IllegalStateException("Schema chưa được hỗ trợ.");
        String runId = pointer.getString("run_id"), basketSetId = pointer.getString("basket_set_id");
        Document run = mongo.getCollection("runs").find(Filters.eq("_id", runId)).first();
        if (run == null || !"READY".equals(run.getString("status")) || !"SAMPLE".equals(run.getString("mode"))
                || !SCHEMA.equals(run.getString("schema_version")) || !basketSetId.equals(run.getString("basket_set_id"))) {
            throw new IllegalStateException("Lượt mẫu chưa hoàn chỉnh hoặc manifest không khớp.");
        }
        List<Document> items = mongo.getCollection("items").find(Filters.eq("run_id", runId)).into(new ArrayList<>());
        items.sort((a, b) -> RuleRanking.codePointOrder(a.getString("stock_code"), b.getString("stock_code")));
        List<Document> rows = mongo.getCollection("association_rules").find(Filters.eq("run_id", runId)).into(new ArrayList<>());
        Document counts = run.get("manifest", Document.class).get("counts", Document.class);
        if (items.size() != 3 || rows.size() != ((Number) counts.get("rules")).intValue()) {
            throw new IllegalStateException("Danh mục/luật thiếu so với manifest.");
        }
        List<RuleRanking.Rule> rules = rows.stream().map(row -> new RuleRanking.Rule(
                row.getList("antecedent", String.class), row.getString("consequent"),
                number(row, "support"), number(row, "confidence"), number(row, "lift"))).toList();
        Document summary = mongo.getCollection("summaries").find(Filters.and(
                Filters.eq("basket_set_id", basketSetId), Filters.eq("summary_type", "m1"),
                Filters.eq("scope", "merchandise"), Filters.eq("bucket_key", "all"))).first();
        if (summary == null) throw new IllegalStateException("Thiếu thống kê mẫu.");
        int k = ((Number) run.get("config", Document.class).get("k")).intValue();
        return new Snapshot(runId, ((Number) pointer.get("version")).longValue(), items, rules, run, summary, k);
    }

    private static double number(Document row, String field) { return ((Number) row.get(field)).doubleValue(); }

    Map<String, Object> proof(Snapshot data) {
        Document rt = data.summary().get("roundtrip", Document.class);
        BigDecimal price = new BigDecimal(rt.getString("price_text"));
        BigDecimal amount = new BigDecimal(data.summary().getString("line_value_gbp"));
        LocalDateTime time = LocalDateTime.parse(rt.getString("invoice_time_local"));
        Map<String, Boolean> checks = new LinkedHashMap<>();
        checks.put("invoice_string_leading_zeros", "0001".equals(rt.getString("invoice")));
        checks.put("explicit_null_preserved", rt.containsKey("customer_id") && rt.get("customer_id") == null);
        checks.put("array_preserved", List.of("SKU_A", "SKU_B").equals(rt.getList("items", String.class)));
        checks.put("empty_array_preserved", rt.containsKey("empty_items") && rt.getList("empty_items", String.class).isEmpty());
        checks.put("count_int64_preserved", data.summary().get("basket_count") instanceof Long);
        checks.put("price_bigdecimal_exact", price.compareTo(new BigDecimal("1.23456789")) == 0);
        checks.put("sum_bigdecimal_exact", amount.compareTo(new BigDecimal("16.04938257")) == 0);
        checks.put("local_datetime_preserved", LocalDateTime.of(2020, 1, 2, 3, 4, 5).equals(time));
        List<Document> cases = data.run().get("manifest", Document.class).getList("ranking_cases", Document.class);
        checks.put("python_java_ranking", cases.stream().allMatch(test ->
                RuleRanking.recommend(data.rules(), test.getList("query", String.class), data.k()).stream()
                        .map(RuleRanking.Rule::consequent).toList().equals(test.getList("expected", String.class))));
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("mode", "SAMPLE"); result.put("schema_version", SCHEMA);
        result.put("run_id", data.runId()); result.put("publication_version", data.version());
        result.put("checks", checks); result.put("all_passed", checks.values().stream().allMatch(Boolean::booleanValue));
        result.put("spring_boot", org.springframework.boot.SpringBootVersion.getVersion());
        result.put("java", System.getProperty("java.version"));
        result.put("spring_data_mongodb", MongoTemplate.class.getPackage().getImplementationVersion());
        result.put("mongodb_driver", com.mongodb.client.MongoClient.class.getPackage().getImplementationVersion());
        result.put("price_text", price.toPlainString()); result.put("line_value_gbp", amount.toPlainString());
        result.put("invoice_time_local", time.toString());
        return result;
    }
}
