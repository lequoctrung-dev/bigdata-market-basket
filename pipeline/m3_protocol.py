"""Giao thức DEVELOPMENT thuần Python; không đọc hoặc đánh giá test cuối."""
from collections import Counter, defaultdict
import hashlib
import math

from m2_source import canonical, check, digest

PROTOCOL = {
    'version': 'm3-temporal-hide-one-v1',
    'train_start': '2009-12-01T00:00:00',
    'dev_start': '2011-07-01T00:00:00',
    'test_start': '2011-10-01T00:00:00',
    'test_end': '2011-12-10T00:00:00',
    'boundary': '[start,end)', 'source_timezone': 'UNKNOWN',
    'k': 5, 'seed': 20261015,
    'mask_version': 'sha256-json-version-seed-invoice-mod-canonical-size-v1',
    'ranking_version': 'confidence-lift-support-codepoint-v1',
    'catalog_version': 'train-merchandise-modal-trim-description-codepoint-v1',
    'metrics_version': 'one-target-hit-and-nonempty-over-all-eligible-v1',
    'final_status': 'NOT_RUN',
}
TRIALS = [dict(min_support=s, min_confidence=.3, num_partitions=8) for s in (.03, .02, .01)]


def split_name(local, protocol=PROTOCOL):
    # All source timestamps are canonical ISO local strings, checked by prepare.
    check(protocol['train_start'] <= local < protocol['test_end'], 'TIME_OUTSIDE_SPLIT')
    return 'train' if local < protocol['dev_start'] else 'dev' if local < protocol['test_start'] else 'test'


def mask(invoice, items, protocol=PROTOCOL):
    items = sorted(set(items))
    check(len(items) >= 2, 'MASK_REQUIRES_TWO_ITEMS')
    key = [protocol['mask_version'], protocol['seed'], invoice]
    index = int(digest(key), 16) % len(items)
    return items[:index] + items[index+1:], items[index]


def rule_order(rule):
    return (-rule['confidence'], -rule['lift'], -rule['support'],
            rule['consequent'], tuple(rule['antecedent']))


def validate_rule(rule):
    a, c = rule['antecedent'], rule['consequent']
    check(a and a == sorted(set(a)) and c not in a and isinstance(c, str), 'RULE_ARRAY_CONTRACT')
    for name in ('support', 'confidence', 'lift'):
        v = rule[name]
        check(math.isfinite(v) and v > 0 and (name == 'lift' or v <= 1), 'RULE_METRIC_CONTRACT')


class RuleIndex:
    """Index one required item per rule; still check ALL antecedents before ranking."""
    def __init__(self, rules):
        self.by_anchor = defaultdict(list)
        for rule in rules:
            validate_rule(rule)
            self.by_anchor[rule['antecedent'][0]].append((frozenset(rule['antecedent']), rule))

    def recommend(self, query, k):
        check(type(k) is int and k > 0, 'INVALID_K')
        query, best = set(query), {}
        for anchor in query:
            for antecedent, rule in self.by_anchor.get(anchor, ()):
                c = rule['consequent']
                if c not in query and antecedent <= query:
                    if c not in best or rule_order(rule) < rule_order(best[c]):
                        best[c] = rule
        return sorted(best.values(), key=rule_order)[:k]


def baseline_order(catalog):
    return [r['stock_code'] for r in sorted(catalog, key=lambda r: (-r['train_basket_count'], r['stock_code']))]


def baseline(query, ordered, k):
    check(type(k) is int and k > 0, 'INVALID_K')
    query = set(query)
    result = []
    for code in ordered:
        if code not in query:
            result.append(code)
            if len(result) == k:
                break
    return result


def metrics(rows, method):
    n = len(rows)
    hits = sum(r['target'] in r[method] for r in rows)
    nonempty = sum(bool(r[method]) for r in rows)
    return {'status': 'MEASURED' if n else 'NOT_APPLICABLE', 'queries': n,
            'hits': hits, 'with_recommendations': nonempty,
            'recall_at_k': hits/n if n else None,
            'recommendation_rate': nonempty/n if n else None}


def evaluate(queries, rules, catalog, k):
    index, ordered = RuleIndex(rules), baseline_order(catalog)
    known, rows = set(ordered), []
    for q in queries:
        rules_out = index.recommend(q['query'], k)
        rows.append(dict(q, rules=[r['consequent'] for r in rules_out],
                         rule_keys=[r['rule_key'] for r in rules_out],
                         baseline=baseline(q['query'], ordered, k),
                         new_target=q['target'] not in known,
                         new_context=sorted(set(q['query'])-known)))
    groups = {
        'all': rows,
        'new_target': [r for r in rows if r['new_target']],
        'known_target': [r for r in rows if not r['new_target']],
        'new_context': [r for r in rows if r['new_context']],
        'no_rule': [r for r in rows if not r['rules']],
        **{f'basket_size_{lo}_{hi}': [r for r in rows if lo <= len(r['query'])+1 <= hi]
           for lo, hi in [(2, 5), (6, 20), (21, 100), (101, 1000000)]},
    }
    return rows, {group: {method: metrics(values, method) for method in ('rules', 'baseline')}
                  for group, values in groups.items()}


def logical_checksum(rows):
    # Caller supplies canonical logical sort, excluding run UUID/system times.
    value = hashlib.sha256()
    for row in rows:
        value.update((canonical(row)+'\n').encode('utf-8'))
    return value.hexdigest()


def catalog_from_counts(frequencies, names):
    return [{'stock_code': code, 'train_basket_count': n,
             'display_name': min(names[code], key=lambda s: (-names[code][s], s)) if names[code] else code}
            for code, n in sorted(frequencies.items())]


def selection_key(receipt):
    m = receipt['development']['all']['rules']
    check(m['status'] == 'MEASURED', 'NO_DEVELOPMENT_FOR_SELECTION')
    return (-m['recall_at_k'], -m['recommendation_rate'], receipt['counts']['rules'],
            -receipt['config']['min_support'], receipt['run_id'])
