# Deepening with dependencies

Use the contract and seam distinctions in [SKILL.md](SKILL.md). Classify dependencies to identify feasible substitution points. A dependency category describes testing options; it does not establish that modules should merge.

## Dependency categories

| Category | Dependency evidence and seam placement |
|---|---|
| In-process | Pure computation or in-memory state with no I/O. Test behavior directly. A replacement adapter is unnecessary unless something actually varies. |
| Local-substitutable | A dependency has a local stand-in, such as PGLite for Postgres or an in-memory filesystem. Assess which behavior the stand-in exercises and which integration behavior needs the real dependency. Keep substitution internal when callers do not need to select it. |
| Remote but owned | An owned service communicates over HTTP, gRPC, or a queue. An existing transport contract may provide the substitution point. Run the real service when practical; use an in-memory adapter when a substitute is justified. A new port needs a concrete variation that earns the indirection. |
| True external | A third-party service such as Stripe or Twilio. Use an existing integration seam where possible. Assess available local or sandbox execution before choosing a mock adapter. |

Keep dependency choices out of the caller contract unless callers need to control them. Inject a replaceable dependency at the narrowest useful seam, which may be internal.

## Apply the existing design and testing rules

- Use [model-the-domain](../principle-model-the-domain/SKILL.md) to decide whether shared domain knowledge warrants grouping modules. Use [minimize-reader-load](../principle-minimize-reader-load/SKILL.md) to assess the cost of adapters and layers.
- Use [test-behavior-not-implementation](../principle-test-behavior-not-implementation/SKILL.md) to choose observable assertions. For TypeScript, apply the real-dependency testing rule in [typescript-best-practices](../typescript-best-practices/SKILL.md).
- When replacing an internal API, use [migrate-callers-then-delete-legacy-apis](../principle-migrate-callers-then-delete-legacy-apis/SKILL.md) for caller migration and test cleanup. Identify the behavior each old test protects and confirm replacement coverage before removing it.
- Use [prove-it-works](../principle-prove-it-works/SKILL.md) to verify the real artifact. A test with a substitute adapter establishes behavior against that adapter; verify the production adapter's integration separately.
