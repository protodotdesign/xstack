# Statistical comparison of writing

Use this when quantitative verification is requested. Choose methods proportionate to the text and question. Freeze the reference, original, and revised text, and record the extraction rules before inspecting results.

## Prepare comparable prose

Exclude frontmatter, headings, fenced code, figure directives, and URLs from body-prose counts. Keep inline-code words. Analyse footnote text separately or include it consistently in a declared sensitivity check; count footnote markers separately. Preserve paragraph boundaries and sentence-like fragments. Decimal points mustn't split sentences. Distinguish contractions from possessives.

The bundled `scripts/voice_stats.py` accepts already extracted plain prose. It doesn't parse Markdown or detect passive voice. Manually check a few sentence boundaries and all unusual abbreviations. Use the same normalization for every version. Don't drop awkward sections after seeing their results.

## Start with distributions and effect sizes

Compare words, paragraphs, sentences/fragments, mean and median sentence length, standard deviation, coefficient of variation, quantiles, words and sentences per paragraph, and the proportions of short and long sentences. Inspect the sequence of lengths as well as the pooled distribution.

Compare contractions, first-person singular/plural and second-person pronouns, punctuation, and asides per 1,000 words. Review agency and humour manually. A pronoun count doesn't tell whether the narrator owns the action; a comma count doesn't measure cadence by itself.

Compare lexical diversity over equal-length windows, such as MATTR, because raw type-token ratios change with sample length. The helper uses windows of 100 words, or the shorter sample's length if either has fewer than 100.

Inspect word unigrams, bigrams, trigrams, and character 3–5-grams. Word n-grams retain topic, formulas, and names. Sparse higher-order n-grams can show large distances even for one author. Contrast those results with function-word frequencies or n-grams in which content words share a placeholder. State the fixed function-word list and vocabulary treatment.

## Fuller audit

When the user requests aggressive testing and there's enough material:

1. Resample whole paragraphs, sections, or independent documents. Sentences in the same paragraph share context. Keep nearby dependent material together when feasible; state the independence assumption.
2. Use block bootstrap intervals for feature gaps and paragraph-label permutation tests for feature differences, sentence-distribution distances, and n-gram distances. Record the random seed and resample counts. Check whether unequal document structure makes label exchangeability implausible.
3. For classification, keep whole blocks together in repeated stratified cross-validation. Fit vocabulary, scaling, feature selection, and tuning only on the training folds. Use balanced accuracy for unequal sample sizes. Refit the entire procedure under each label permutation. Use character n-grams, function words, and nonlexical style features as separate views.
4. Define test families before examining results. Report raw p-values alongside Holm or another declared multiple-testing correction, effect sizes, confidence intervals, and detected differences. Include the original draft so improvement is observable.
5. Check sensitivity to footnotes, code introductions, unequal lengths, and topic-heavy passages. Retain the primary comparison and explain sensitivity results separately.

Choose a reproducible number of shuffles that gives useful p-value resolution. With B random shuffles, use (1 + number at least as extreme) / (B + 1). Avoid reporting zero p-values. Don't silently skip failed or inconvenient tests.

## Interpret honestly

A high p-value means the test didn't detect a difference with this sample. Equivalence needs declared tolerances and intervals narrow enough to fit inside them. A classifier near chance doesn't establish identical authorship.

Repeatedly revising against the same tests makes the audit exploratory. A fresh held-out reference or document gives stronger evidence if available. Small samples and topic differences limit what any battery can establish. Explain these points in the report, while keeping the rewritten prose free of methodological notes.

Resolve material voice mismatches using the prose evidence. Changing I tested to measured, scattering function words, or copying jokes to push a statistic toward the reference defeats the writing task.
