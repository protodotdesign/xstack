#!/usr/bin/env python3
"""Remind the agent of active skill rules without forcing repeated reads."""
import json
import os

SKILLS = os.path.join(os.environ.get("CLAUDE_PLUGIN_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "skills")

REMINDER = f"""
When functioning as a planning, design, or code writing agent, use:
  - For coding: trace the problem, reuse existing code, and make the smallest correct change.

When responding directly to a user, ensure the following skills are loaded and you use them:
  - i-have-adhd: lead with the action or result, keep paragraphs short, number multi-step instructions, and name one next action when work remains.
  - asd-ste100 for responses: use plain words, active voice, and one instruction per sentence. "

Respect the user's explicit requests to disable or change these skills, but load them by default if they were not previously loaded in this conversation. Before reading a skill file, check the current conversation history. Reuse full skill instructions already present in that history. Read the full SKILL.md only for an active, applicable skill whose instructions are absent from the current history, including after compaction removes them. A skill name, file path, or this brief reminder alone does not count as full instructions. "

Skill files:
- i-have-adhd ({SKILLS}/i-have-adhd/SKILL.md)
- asd-ste100 ({SKILLS}/asd-ste100/SKILL.md)
"""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": REMINDER
    },
}))
