---
name: match-writing
description: "Match a draft to supplied reference writing, preserving the author's voice, cadence, sentence-length variation, humour, perspective, and factual meaning. Use when asked to match my writing, write like this, make sections sound like the same author, or rewrite in an established voice. Also supports before-and-after stylistic statistics when requested."
disable-model-invocation: true
---

# Match Writing

## Establish the reference and editing boundary

Read the full reference and target before editing. Identify which passages the user wrote or approved, the intended audience, the genre, and the exact editable range. Treat the supplied reference as the voice authority. Apply explicit user constraints even when a sample breaks them.

Keep a frozen reference and original draft for comparison. Preserve the reference passage, facts, numbers, technical relationships, uncertainty, attribution, code, links, and embedded assets. Keep unrelated edits intact. Before writing a file, check for changes made since the snapshot and incorporate them.

If the user supplies no reference, look for writing they have identified as theirs in this conversation or workspace. For this user's technical narrative voice, read [calibration.md](references/calibration.md). If evidence is insufficient, ask for a reference and continue any independent work.

## Build a voice fingerprint

Record a compact fingerprint with representative excerpts. Identify:

- **Agency and perspective:** who performs actions; how the author uses I, we, you, impersonal descriptions, and admissions of uncertainty.
- **Cadence:** sentence lengths and their spread, fragments, clause chains, paragraph lengths, and where short reactions interrupt long explanations.
- **Diction:** concrete verbs, technical vocabulary, contractions, transitions, punctuation, asides, and repeated constructions.
- **Humour:** its source, target, placement, frequency, and relationship to the facts. Observe how the author undercuts their own confidence.
- **Explanation:** how the author introduces terms, uses examples, moves from observation to interpretation, and revises a mistaken idea.

Distinguish repeatable habits from choices caused by one topic or passage. Describe what the sample actually does. Avoid replacing its habits with generic advice to shorten every sentence or make every paragraph punchy.

## Rewrite for the reader

Rewrite complete paragraphs while preserving the argument and factual relationships. Match the distribution and sequence of sentence lengths, rather than forcing every sentence toward a mean.

Keep the actor visible where the reference does. Check passive clauses, nominalizations, and participial labels that conceal agency. “Across the shapes I tested” retains the narrator in a way that “Across the measured shapes” doesn't, even though the latter phrase isn't itself a complete passive clause. Use first person only for actions the author actually performed.

Let humour arise from specific facts, decisions, or disappointments already supported by the draft. Match its placement and restraint. Avoid borrowing a reference's punchlines, inventing events, inserting a joke into every paragraph, or copying accidental typos.

Read the result aloud or simulate that reading sentence by sentence. Check whether transitions, asides, technical explanations, and reactions sound like one person. Remove added throat-clearing, symmetrical slogans, generic summaries, and explanatory scaffolding absent from the reference.

## Compare and iterate

Always do a qualitative comparison. Use descriptive statistics for a substantial rewrite when useful; run the fuller audit when the user requests quantitative evidence or statistical indistinguishability. Read [statistical-audit.md](references/statistical-audit.md) for methods and interpretation.

For a quick reproducible comparison, prepare plain prose files with the same extraction rules and run:

```sh
python3 <skill-directory>/scripts/voice_stats.py reference.txt rewrite.txt --before original.txt
```

The bundled script reports cadence, paragraph structure, contractions, pronouns, punctuation, lexical diversity, and word n-gram distances. It provides descriptive measurements; use the audit reference for inference. The script's heuristic sentence splitting needs a manual check for unusual abbreviations or punctuation.

Revise meaningful mismatches, then rerun the same extraction and measurements. Preserve narrator agency and natural phrasing while doing so. Avoid tuning articles, pronouns, filler, punctuation, or jokes merely to improve a score. Stop when the remaining differences reflect topic, necessary structure, or insufficient evidence rather than a useful prose improvement.

Report the edited result and the checks actually run. When statistics are requested, show reference, original, and rewrite together, including remaining differences. Keep methodological explanations in the conversation or a separate report. Don't add them to the rewritten deliverable unless requested. Never promise indistinguishability under every possible statistical test.
