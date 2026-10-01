# WindowsAgentArena harness (skeleton)

This folder measures Telos against other computer-use actuators on
[WindowsAgentArena](https://github.com/microsoft/WindowsAgentArena) (MIT): 154
tasks across 12 Windows app domains. The plan it implements is section 7 of the
0.7.0 design: four arms under one model, one system prompt, one step budget and
one VM snapshot.

| Arm | Actuator | Runner here |
|---|---|---|
| A | WAA Navi agent, its UIA backend | not built |
| B | Telos 0.7.0, refs first, benchmark grant | dry run |
| C | Windows-MCP, same model | not built |
| D | Playwright MCP, Chrome and Edge subset | not built |

## Run the dry run

```
node bench/waa/harness.mjs                       # synthetic task list, 154 ids
node bench/waa/harness.mjs --tasks <WAA checkout>/src/win-arena-container/client/evaluation_examples_windows/test_all.json
node bench/waa/harness.mjs --out waa-dry-run.json
```

The dry run reads the task list, plans the episodes (154 tasks x 3 seeds x 3
Windows arms, plus 30 browser tasks x 3 seeds for arm D), builds the benchmark
grant each domain needs, and sends probe calls through the real tier gate and
the signed receipt chain with fake drivers in a throwaway state root. Every
call is a dry run and the executor throws if anything reaches it. The report
shows, per domain, which probes would hold for confirmation, which the gate
refuses (an off-scope origin, a terminal window, exec and eval outside the
grant), what the scripted approver decides, and whether the receipt chain
verifies. Exit 0 means zero executed actions and every chain verified.

`--live` is refused. A live run executes inside a WAA guest VM under a
benchmark grant the operator issues there. The guest relay is not built, and
the harness never acts on the host.

## What is fixed before a scored run

- The decision the run informs, its owner, the baseline and the trigger
  (design 7.1), written to the project records before the first scored episode.
- The benchmark grant tops out at T3. Settings tasks that need a T4 config verb
  count as out of grant; the grant is not widened mid-run.
- The scripted approver's policy (approve in-scope holds, reject the rest) is
  published with the results.
- Metrics: success rate per arm and domain with a Wilson 95% interval
  (`stats.mjs`), exact McNemar on paired tasks, holds per task, out-of-scope
  actions executed (target 0), receipt chains that verify (target all).

## What the dry run does not show

It does not show that any task can be solved, that the window patterns in
`domains.mjs` match the WAA guest image (each is marked `verified: false`), or
any success rate. The WAA step budget and temperature defaults have not been
read; they stay unset until they are.
