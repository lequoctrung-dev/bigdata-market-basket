package vn.edu.bigdata.m1;

import java.util.*;

/** Comparator chung với batch: không làm tròn hoặc tie theo locale. */
public final class RuleRanking {
    public record Rule(List<String> antecedent, String consequent, double support, double confidence, double lift) {
        public Rule {
            antecedent = List.copyOf(antecedent);
            if (antecedent.isEmpty() || new HashSet<>(antecedent).size() != antecedent.size()
                    || antecedent.contains(consequent) || !Double.isFinite(support) || support <= 0 || support > 1
                    || !Double.isFinite(confidence) || confidence <= 0 || confidence > 1
                    || !Double.isFinite(lift) || lift <= 0) {
                throw new IllegalStateException("Luật không hợp lệ");
            }
        }
    }

    static int codePointOrder(String a, String b) {
        int[] left = a.codePoints().toArray(), right = b.codePoints().toArray();
        for (int i = 0; i < Math.min(left.length, right.length); i++) {
            int result = Integer.compare(left[i], right[i]);
            if (result != 0) return result;
        }
        return Integer.compare(left.length, right.length);
    }

    private static int antecedentOrder(List<String> a, List<String> b) {
        for (int i = 0; i < Math.min(a.size(), b.size()); i++) {
            int result = codePointOrder(a.get(i), b.get(i));
            if (result != 0) return result;
        }
        return Integer.compare(a.size(), b.size());
    }

    static final Comparator<Rule> ORDER = Comparator.comparingDouble(Rule::confidence).reversed()
            .thenComparing(Comparator.comparingDouble(Rule::lift).reversed())
            .thenComparing(Comparator.comparingDouble(Rule::support).reversed())
            .thenComparing(Rule::consequent, RuleRanking::codePointOrder)
            .thenComparing(Rule::antecedent, RuleRanking::antecedentOrder);

    static List<Rule> recommend(List<Rule> rules, Collection<String> query, int k) {
        if (k < 1) throw new IllegalArgumentException("K không hợp lệ");
        Set<String> basket = new HashSet<>(query);
        Map<String, Rule> best = new HashMap<>();
        for (Rule rule : rules) {
            if (basket.containsAll(rule.antecedent()) && !basket.contains(rule.consequent())) {
                best.merge(rule.consequent(), rule, (a, b) -> ORDER.compare(a, b) <= 0 ? a : b);
            }
        }
        return best.values().stream().sorted(ORDER).limit(k).toList();
    }
}
