---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes a settings file that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write pstack's model settings, one model per role, to `~/.agents/pstack-models.md`. pstack skills read this file when they pick a model. "The settings file" below means this file.

## Model values

A role value is `<model>-<effort>`, such as `opus-xhigh` or `sonnet-high`. When you spawn a subagent with the `Agent` tool, pass the part before the last hyphen as `model` and the last token as `effort`. A value with no effort token (`opus`) sets only `model`. The alias `inherit-parent` (also written `auto`) means: omit both `model` and `effort`, so the role runs on the parent chat model.

## Steps

### 1. Detect available models

The dependable source is the `model` enum of the `Agent` tool in this session (for example `sonnet`, `opus`, `haiku`, `fable`). The effort ladder is `max` > `xhigh` > `high` > `medium` > `low`. Never write a model you have not confirmed is in that enum. The aliases `inherit-parent` and `auto` are always valid.

### 2. Load current state

The default role-to-model mapping is the shape shown in step 5 below. If the settings file already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults. A line whose role is not in step 5, such as `how critics`, is from a retired role. Drop it. A value in the old slug format (`claude-opus-5-5-xhigh`, `grok-4.7-xhigh-fast`) maps to `opus-<effort>` for `claude-opus-*` and to `sonnet-<effort>` for anything else. Say which lines you converted.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Use `AskUserQuestion`. Offer these four options with these exact labels, and name the current budget when the file records one. With no file, say that `large` matches the skill defaults.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table from the skill defaults, and on a re-run keep any role you changed by model, list, or alias. `unlimited`, `large`, `medium`, and `small` set the effort token of every value, panel entries included, to `max`, `xhigh`, `high`, or `medium`. `inherit-parent` and `auto` do not change. So `unlimited` turns `opus-xhigh` into `opus-max`, and `small` turns the defaults into `opus-medium` and `sonnet-medium`.

**(c) Show the roles and confirm.** Show every role with its value, marking any model not in the detected set as needing a choice. Also list each line step 2 dropped. Ask with `AskUserQuestion` whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` as the options. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every model written must be in the detected set, and every effort token on the ladder. `inherit-parent` and `auto` always pass. If a chosen value is not available, stop and ask again.

### 5. Write the file

Write the settings file with a `# budget` line with the chosen label and its target effort, and one line per role, using the same labels xstack-mode uses. Overwrite the whole file so re-runs stay idempotent. Shape:

```
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# Value: <model>-<effort>, passed to the Agent tool as `model` and `effort`. `inherit-parent` runs the role on the parent chat model. Alias entries in a panel list still count toward its fan-out.
# budget: large (xhigh)
feature, refactoring: sonnet-xhigh
bug-fix: sonnet-xhigh
perf-issue: sonnet-xhigh
hillclimb: sonnet-xhigh
judgment and prose: opus-xhigh
hardest tasks: opus-xhigh
how explorer: sonnet-xhigh
how explainer: opus-xhigh
why investigators: sonnet-xhigh
why synthesizer: opus-xhigh
reflect tooling: sonnet-xhigh
reflect judgment, divergent, synthesizer: opus-xhigh
arena runners: opus-xhigh, sonnet-xhigh
arena cross-judge pool: opus-xhigh, sonnet-xhigh
swarm workers: sonnet-xhigh
architect runners: opus-xhigh, sonnet-xhigh
interrogate reviewers: opus-xhigh, sonnet-xhigh
```

### 6. Confirm

Tell the user which file was written. pstack skills read `~/.agents/pstack-models.md` when they pick a model. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill`. On no, move on without pushing.
