# xstack

Agent workflows, principle skills, and subagents for Claude Code.

## Install

Install it as a Claude Code plugin. That gets you every skill, the `xstack-agent` and `comment-sicko` subagents, and the reminder hook:

```
/plugin marketplace add protodotdesign/xstack
/plugin install xstack@xstack
```

To try a local checkout without installing, run `claude --plugin-dir /path/to/xstack`.

Plugin skills are namespaced, so `/xstack-mode` is also reachable as `/xstack:xstack-mode`. Run `/setup-pstack` once to pick models per role.

## Skills

Start with `/xstack-mode`. It matches the task to a playbook and runs the other skills as its steps need them. `/xstack-help` maps a question to the right skill. The [guide](docs/guide/README.md) walks through each workflow.

These skills don't call other skills, so each one works alone:

`unslop`, `how`, `tdd`, `typescript-best-practices`, `arena`, `swarm`, `interrogate`, `reflect`, `show-me-your-work`, `figure-it-out`, `automate-me`, `correct`, `benchmark-checklist`

Some skills call other skills:

| Skill | Uses |
|---|---|
| `teach` | `how`, `why` |
| `why` | `how` |
| `technical-writing` | `unslop` |
| `architect` | `arena`, `how` |
| `blast-radius` | `arena`, `how`, `why`, `unslop` |
| `create-verification-skill` | `maintain-verification-skill` |
| `xstack-mode` | all `principle-*` skills and most of the other skills |
| `xstack-help` | the skills you want help with |

## License

MIT. See [LICENSE](LICENSE).
