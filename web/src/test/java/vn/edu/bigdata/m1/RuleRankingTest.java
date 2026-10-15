package vn.edu.bigdata.m1;

import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class RuleRankingTest {
    private RuleRanking.Rule rule(List<String> a, String c, double confidence) {
        return new RuleRanking.Rule(a, c, .4, confidence, 1.2);
    }
    @Test void fullAntecedentRequiredAndExistingItemExcluded() {
        var rules = List.of(rule(List.of("A", "B"), "C", .9), rule(List.of("A"), "B", .7));
        assertEquals(List.of("B"), RuleRanking.recommend(rules, List.of("A"), 3).stream().map(RuleRanking.Rule::consequent).toList());
        assertTrue(RuleRanking.recommend(rules, List.of("A", "B", "C"), 3).isEmpty());
    }
    @Test void candidateDeduplicatedBeforeTopKAndStableTie() {
        var rules = List.of(rule(List.of("B"), "C", .8), rule(List.of("A"), "C", .9), rule(List.of("A"), "D", .9));
        var answer = RuleRanking.recommend(rules, List.of("A", "B", "A"), 2);
        assertEquals(List.of("C", "D"), answer.stream().map(RuleRanking.Rule::consequent).toList());
        assertEquals(List.of("A"), answer.get(0).antecedent());
    }
    @Test void unicodeTieUsesCodePointsRatherThanUtf16CodeUnits() {
        assertTrue(RuleRanking.codePointOrder("\uE000", "\uD800\uDC00") < 0);
    }
    @Test void noRuleHasNoFallbackAndInvalidMetricsRejected() {
        assertTrue(RuleRanking.recommend(List.of(), List.of("A"), 3).isEmpty());
        assertThrows(IllegalStateException.class, () -> rule(List.of("A"), "B", Double.NaN));
    }
}
