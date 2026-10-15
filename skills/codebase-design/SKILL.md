---
name: codebase-design
description: Clarify a module's full caller contract, locate substitution seams, and assess dependencies before deepening modules. Use for interface or seam-placement questions; route design exploration, refactoring, and testing through the existing skills.
disable-model-invocation: true
---

# Codebase design

Use this skill to identify what callers must know and where dependencies can be replaced. The existing skills own design exploration, code organization, and verification.

## Caller contracts and substitution

- **Module:** code with a caller-facing interface and an implementation. It can be a function, class, package, or capability spanning deployment tiers.
- **Interface:** everything a caller must know to use the module correctly. Include types, invariants, ordering constraints, error modes, required configuration, and performance characteristics. A short type signature can still hide a demanding caller contract.
- **Seam:** a place where behavior can be replaced without editing the code that uses it. Locate the substitution point separately from deciding what behavior the module owns.
- **Adapter:** a concrete implementation that satisfies the contract at a seam. This describes its role, regardless of how much code it contains.

Use these distinctions when they help explain a design. Preserve the project's names and conventional terms such as API, service, and component. A system boundary describes ownership or validation; a seam describes substitution. One location can serve both purposes.

## Internal versus caller-visible seams

A module can hide substantial behavior while using smaller parts internally. Apply the depth criteria in [architect's design red flags](../architect/references/design-red-flags.md). Implementation line count does not establish depth.

An internal seam belongs to the implementation and may support the module's own tests. A caller-visible seam makes dependency selection part of the caller contract. Keep dependency construction and substitution internal when callers do not need to control them.

An additional adapter needs a concrete use, such as a production integration and a justified test substitute. Counting adapters alone does not justify a seam. Use [minimize-reader-load](../principle-minimize-reader-load/SKILL.md) to decide whether the indirection earns its place.

Use the deletion test as a diagnostic: imagine removing the module. Complexity that reappears across callers shows what the module was hiding. Complexity that disappears suggests an unnecessary layer. Check actual responsibilities before deciding to remove it.

## Use the existing skills

Read the linked skill when its task applies. Pass it the caller contract, proposed substitution points, and dependency evidence gathered here.

| Task | Existing instructions and how to use them |
|---|---|
| Decide what belongs together | Use [model-the-domain](../principle-model-the-domain/SKILL.md) to identify shared knowledge and ownership. Use [minimize-reader-load](../principle-minimize-reader-load/SKILL.md) to evaluate layers and hidden state. |
| Explore alternative interfaces | Follow [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md), which routes through [architect](../architect/SKILL.md). |
| Assess dependencies before deepening | Read [DEEPENING.md](DEEPENING.md) for dependency categories and seam placement. |
| Place validation and separate computation from effects | Use [boundary-discipline](../principle-boundary-discipline/SKILL.md). Include validation and error obligations in the caller contract. |
| Reshape an existing interface | Use [laziness-protocol](../principle-laziness-protocol/SKILL.md) to scope the change. Use [migrate-callers-then-delete-legacy-apis](../principle-migrate-callers-then-delete-legacy-apis/SKILL.md) when its compatibility conditions hold. |
| Select or replace tests | Use [test-behavior-not-implementation](../principle-test-behavior-not-implementation/SKILL.md). For TypeScript, use [typescript-best-practices](../typescript-best-practices/SKILL.md), including its real-dependency testing rule. Use [tdd](../tdd/SKILL.md) when its bug-fix trigger applies. |
| Verify the result | Use [prove-it-works](../principle-prove-it-works/SKILL.md). Exercise the real integration as well as behavior tested with substitute adapters. |
