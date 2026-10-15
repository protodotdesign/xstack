---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, find this conversation's transcript in the active workspace's session directory. Do not glob across every project's directory. That crosses workspace boundaries and reads private chats from unrelated projects.

Transcripts live at `~/.claude/projects/<slug>/<session-id>.jsonl`, where `<slug>` is the workspace path with every character that isn't a letter or digit turned into "-".

```bash
ls -t ~/.claude/projects/<slug>/*.jsonl | head -10
```

Take the newest candidates first and confirm one by finding the conversation's opening user prompt in its first user message. If none matches, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

One message, three `Agent` calls, `subagent_type: "general-purpose"`. Reviewers need MCP access to look up the tickets, chat threads, and observability traces the transcript references, so don't use a read-only agent type such as `Explore`.

Each reviewer and the synthesizer name a role line in the pstack settings file (`~/.agents/pstack-models.md`) and a default. Split that line's value, or the default if the file or the line is missing, into `model` and `effort` (format in **setup-pstack**). Leave both unset when the value is `auto` or `inherit-parent`. If the `Agent` tool rejects a model, use the default and say so.

| Lens | Role line | Default `model` | Prompt template |
|---|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `opus-xhigh` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `sonnet-xhigh` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `opus-xhigh` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the `Agent` result.

## 3. Synthesize

One `Agent` call, `subagent_type: "general-purpose"`, `model` and `effort` from the `reflect judgment, divergent, synthesizer` line (default `opus-xhigh`). It spot-verifies citations through MCP, so it needs the full tool set. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File each Backlog item to your team's devex or backlog tracker without waiting. Only the Accepted list waits for approval.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to Anthropic's `skill-creator` skill and run its draft / test / iterate loop. If it isn't installed, follow the Agent Skills format at agentskills.io.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop.
- `new skill via skill-creator: <kebab-name>`: hand creation to `skill-creator`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
