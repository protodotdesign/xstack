#!/usr/bin/env python3
"""Compare extracted plain prose using descriptive style statistics (stdlib only)."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import statistics

WORD = re.compile(r"(?:\d+(?:\.\d+)+|[^\W_]+)(?:['-][^\W_]+)*", re.UNICODE)
CONTRACTION = re.compile(r"(?:n't|'m|'re|'ve|'ll|'d)$|^(?:he|she|it|that|there|here|what|who|where|when|how|let)'s$")
SINGULAR = {'i', 'me', 'my', 'mine', 'myself'}
PLURAL = {'we', 'us', 'our', 'ours', 'ourselves'}
SECOND = {'you', 'your', 'yours', 'yourself', 'yourselves'}
ABBREVIATIONS = re.compile(r'\b(?:Mr|Mrs|Ms|Dr|Prof|vs|etc)\.|\b(?:e\.g\.|i\.e\.)', re.IGNORECASE)


def words(text):
    return WORD.findall(text.lower().replace('’', "'"))


def sentences(paragraph):
    protected = re.sub(r'(?<=\d)\.(?=\d)', '\uE000', paragraph)
    protected = ABBREVIATIONS.sub(lambda m: m[0].replace('.', '\uE000'), protected)
    parts = re.split(r'[.!?]+[\'"”’)]*(?=\s|$)', protected)
    return [words(p.replace('\uE000', '.')) for p in parts if words(p.replace('\uE000', '.'))]


def mattr(tokens, window):
    counts = Counter(tokens[:window])
    total = len(counts)
    for i in range(window, len(tokens)):
        previous = tokens[i-window]
        counts[previous] -= 1
        if not counts[previous]:
            del counts[previous]
        counts[tokens[i]] += 1
        total += len(counts)
    return total / ((len(tokens)-window+1)*window)


def quantile(values, fraction):
    ordered = sorted(values)
    index = (len(ordered)-1)*fraction
    low = int(index)
    high = min(low+1, len(ordered)-1)
    return ordered[low]+(ordered[high]-ordered[low])*(index-low)


def load(path):
    text = path.read_text(encoding='utf-8')
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if words(p)]
    if not paragraphs:
        raise ValueError(f'No prose words in {path}')
    return {'path': str(path.resolve()), 'paragraphs': paragraphs,
            'tokens': [w for p in paragraphs for w in words(p)]}


def describe(sample, window):
    paragraphs, tokens = sample['paragraphs'], sample['tokens']
    lengths = [len(s) for p in paragraphs for s in sentences(p)]
    mean = statistics.mean(lengths)
    sd = statistics.pstdev(lengths)
    joined = '\n\n'.join(paragraphs)
    rate = lambda count: count*1000/len(tokens)
    pronouns = [t.split("'")[0] if CONTRACTION.search(t) else t for t in tokens]
    ngrams = {}
    for size in (1, 2, 3):
        counts = Counter()
        for p in paragraphs:
            ts = words(p)
            counts.update(tuple(ts[i:i+size]) for i in range(len(ts)-size+1))
        ngrams[size] = counts
    overview = {
        'source': sample['path'], 'words': len(tokens), 'paragraphs': len(paragraphs),
        'sentences_and_fragments': len(lengths), 'sentence_mean': mean,
        'sentence_median': statistics.median(lengths), 'sentence_sd_population': sd,
        'sentence_cv': sd/mean,
        'sentence_quantiles': {str(q): quantile(lengths, q) for q in (.1, .25, .75, .9)},
        'sentences_le_10_pct': 100*sum(n <= 10 for n in lengths)/len(lengths),
        'sentences_ge_35_pct': 100*sum(n >= 35 for n in lengths)/len(lengths),
        'sentence_lengths_in_order': lengths,
        'words_per_paragraph': len(tokens)/len(paragraphs),
        'sentences_per_paragraph': len(lengths)/len(paragraphs),
        'mean_word_characters': statistics.mean(map(len, tokens)),
        'mattr_window': window, 'mattr': mattr(tokens, window),
        'per_1000_words': {
            'contractions': rate(sum(bool(CONTRACTION.search(t)) for t in tokens)),
            'first_person_singular': rate(sum(t in SINGULAR for t in pronouns)),
            'first_person_plural': rate(sum(t in PLURAL for t in pronouns)),
            'second_person': rate(sum(t in SECOND for t in pronouns)),
            **{name: rate(joined.count(mark)) for name, mark in
               [('commas', ','), ('semicolons', ';'), ('colons', ':'), ('opening_parentheses', '(')]}
        },
        'top_word_ngrams': {
            str(n): [{'text': ' '.join(k), 'count': v} for k, v in
                     sorted(c.items(), key=lambda item: (-item[1], item[0]))[:15]]
            for n, c in ngrams.items()
        }
    }
    return overview, ngrams


def js_bits(left, right):
    nl, nr = sum(left.values()), sum(right.values())
    if not nl or not nr:
        return None
    result = 0.0
    for term in left.keys() | right.keys():
        p, q = left.get(term, 0)/nl, right.get(term, 0)/nr
        middle = (p+q)/2
        if p:
            result += .5*p*math.log2(p/middle)
        if q:
            result += .5*q*math.log2(q/middle)
    return result


def compare(reference, rewrite, before=None):
    samples = {'reference': load(reference)}
    if before:
        samples['before'] = load(before)
    samples['rewrite'] = load(rewrite)
    window = min(100, *(len(s['tokens']) for s in samples.values()))
    described = {name: describe(sample, window) for name, sample in samples.items()}
    return {
        'method': 'Descriptive only. Plain prose inputs; heuristic sentence splitting; population SD. Word n-grams stay within paragraphs. JS bits range 0 to 1 and retain topic; null means insufficient n-grams. No significance or authorship claim.',
        'samples': {name: pair[0] for name, pair in described.items()},
        'word_ngram_js_bits_from_reference': {
            name: {str(n): js_bits(described['reference'][1][n], pair[1][n]) for n in (1, 2, 3)}
            for name, pair in described.items() if name != 'reference'
        }
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference', type=Path)
    parser.add_argument('rewrite', type=Path)
    parser.add_argument('--before', type=Path)
    args = parser.parse_args()
    try:
        report = compare(args.reference, args.rewrite, args.before)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == '__main__':
    main()
