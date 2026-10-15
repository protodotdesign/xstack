# Explore alternative interfaces

When alternative interfaces need exploration, use [architect](../architect/SKILL.md). It owns grounding, candidate generation through [arena](../arena/SKILL.md), comparison, synthesis, and implementation checkpoints.

Include this evidence in the architectural task:

- The full caller contract from [SKILL.md](SKILL.md), including invariants, ordering, errors, configuration, and performance obligations.
- Concrete caller examples and the behavior the module should hide.
- Dependencies classified with [DEEPENING.md](DEEPENING.md), including available real runtimes and justified substitutes.
- Proposed internal and caller-visible seams, and who needs to control each dependency.
- Existing project terminology and any domain glossary the project actually provides.

Run architect's design exploration once for the decision. Pass this evidence into its existing runner briefs. Follow its candidate-selection and synthesis rules.

Use architect's existing rationale to record the chosen caller contract, seam placement, and dependency strategy.
