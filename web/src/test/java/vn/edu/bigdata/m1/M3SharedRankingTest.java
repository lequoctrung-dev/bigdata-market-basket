package vn.edu.bigdata.m1;

import org.bson.Document;
import org.junit.jupiter.api.Test;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

/** Same source-faithful cases as Python M3; does not open the M4 application. */
class M3SharedRankingTest {
    @Test void realDevelopmentPredictionsMatchPythonWhenRunIsProvided() throws Exception {
        String directory = System.getProperty("m3.runDirectory");
        assumeTrue(directory != null, "Supply -Dm3.runDirectory=<absolute M3 run folder> for real DEVELOPMENT parity");
        Path run = Path.of(directory);
        List<RuleRanking.Rule> rules = new ArrayList<>();
        for (String line : Files.readAllLines(run.resolve("association_rules.jsonl"), StandardCharsets.UTF_8)) {
            Document row = Document.parse(line);
            rules.add(new RuleRanking.Rule(row.getList("antecedent", String.class), row.getString("consequent"),
                ((Number)row.get("support")).doubleValue(), ((Number)row.get("confidence")).doubleValue(),
                ((Number)row.get("lift")).doubleValue()));
        }
        Document receipt = Document.parse(Files.readString(run.resolve("receipt.json"), StandardCharsets.UTF_8));
        assertEquals("PASS", receipt.getString("status"));
        assertEquals("DEVELOPMENT", receipt.getString("evaluation_stage"));
        assertEquals("NOT_RUN", receipt.getString("final_status"));
        int k = ((Number)receipt.get("protocol", Document.class).get("k")).intValue();
        int checked = 0;
        for (String line : Files.readAllLines(run.resolve("dev-predictions.jsonl"), StandardCharsets.UTF_8)) {
            Document query = Document.parse(line);
            var result = RuleRanking.recommend(rules, query.getList("query", String.class), k);
            assertEquals(query.getList("rules", String.class), result.stream().map(RuleRanking.Rule::consequent).toList(), query.getString("invoice"));
            assertEquals(result.size(), query.getList("rule_keys", String.class).size());
            for (int i = 0; i < result.size(); i++) {
                var pair = Document.parse("{\"pair\":" + query.getList("rule_keys", String.class).get(i) + "}").getList("pair", Object.class);
                assertEquals(result.get(i).antecedent(), pair.get(0));
                assertEquals(result.get(i).consequent(), pair.get(1));
            }
            checked++;
        }
        assertEquals(((Number)receipt.get("counts", Document.class).get("eligible_dev_queries")).intValue(), checked);
    }

    @Test void sharedCasesWithIndependentExpectedAnswers() throws Exception {
        var fixture = Document.parse(Files.readString(Path.of("../pipeline/m3_ranking_cases.json"), StandardCharsets.UTF_8));
        for (var test : fixture.getList("cases", Document.class)) {
            List<RuleRanking.Rule> rules = new ArrayList<>();
            for (var row : test.getList("rules", Document.class)) {
                rules.add(new RuleRanking.Rule(row.getList("antecedent", String.class), row.getString("consequent"),
                    ((Number)row.get("support")).doubleValue(), ((Number)row.get("confidence")).doubleValue(),
                    ((Number)row.get("lift")).doubleValue()));
            }
            for (int order = 0; order < 2; order++) {
                var result = RuleRanking.recommend(rules, test.getList("query", String.class), test.getInteger("k"));
                assertEquals(test.getList("expected", String.class), result.stream().map(RuleRanking.Rule::consequent).toList(), test.getString("name"));
                if (test.containsKey("best_antecedents")) {
                    assertEquals(test.get("best_antecedents"), result.stream().map(RuleRanking.Rule::antecedent).toList(), test.getString("name"));
                }
                Collections.reverse(rules);
            }
        }
    }
}
