# Pass 0067 Ledger: Forum Routing Repair Experiment

Date: 2026-07-01

Status: `MATCH_FORUM_ROUTING_REPAIR_EXPERIMENT`

## Purpose

Promote the pass 0066 `routing_repair_spine` growth vector into a live Forum
route experiment. The pass measures whether prompt shape alone can move a
cross-domain frontier request from escalation into the `project-telos` lane.

This is a prompt-shaping repair receipt. It does not modify Forum source code
and does not prove that every broad cross-domain prompt will route correctly.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_forum_routing_repair_experiment.py` | Deterministic route repair artifact composer. |
| `tools/test_forum_routing_repair_experiment.py` | Focused route repair test. |
| `tools/probe_forum_routing_repair_experiment.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0067_forum_routing_repair_experiment.py` | Validator for route probes, score lift, and non-promotion controls. |
| `schemas/forum-routing-repair-experiment-pass-0067.json` | `ForumRoutingRepairExperiment/v1` artifact. |
| `schemas/pass-0067-forum-routing-repair-experiment-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0067.json` | Compact Index, Gather, Forum, Crucible, Telos, and shell receipts. |
| `packets/077-forum-routing-repair-experiment.md` | Human-readable route repair packet. |
| `adversarial/pass-0067-forum-routing-repair-experiment-steelman.md` | Local steelman. |
| `crucible/pass-0067-thesis.json` | Falsifiable claims. |
| `crucible/pass-0067-measurements.json` | Measurements/evidence. |
| `crucible/pass-0067-report.md` | Crucible report. |
| `crucible/pass-0067-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Route probes | 3 |
| Baseline route | escalation, no decision |
| Baseline `project-telos` score | 0.09090909090909091 |
| Repaired routes | 2 route to `project-telos` without escalation |
| Best repaired `project-telos` score | 0.3181818181818182 |
| Score lift | 0.227272727273 |
| Required prefix | `Project Telos dogfood pass` |
| Required tool chain | Gather, Index, Forum, Crucible, Telos |
| Previous pass binding | 0066 |
| Unsupported claims | 0 |
| Promotion state | `PROMPT_REPAIR_NOT_ROUTER_PATCH` |

## Repair Rule

For cross-domain dogfood research, Forum routes cleanly when the request starts
with explicit Project Telos framing, names the five-tool operator chain, and
uses receipt vocabulary such as `growth-vector`, `proof packet`, `action
receipt`, `loop ledger`, and `scoped adapter lanes`.

The broad prompt still escalates because its vocabulary is evenly spread across
compiler systems, data/ML, deep research, native C++, render pipelines, and
Project Telos.

## Tool Findings

- Index status returned `MATCH`.
- Gather read packet 077 with SHA256 `4f06cee2244a84356a1cfe308a51d066c04f4000976a66cc864a25b3d93272e6` and digest seal `bb20a89f24d3d6892901c99ddaa4cebd261fce103577778df510d2b0f01d7db7`.
- Forum ledger verified `chain=true`, `deep=true`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `170c379af77b0ede`.
- Crucible assessment seal: `b7a8c032f621c7a83175abddd0904fc7381bf871f098c10646d14629c342baac`.
- Crucible registry stats after this pass: 55 theses, 457 claims, 457 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Telos compatibility, operator, and MCP freshness doctors returned `MATCH`.

## Verification

```powershell
python docs\research\dogfood\tools\test_forum_routing_repair_experiment.py
python docs\research\dogfood\tools\probe_forum_routing_repair_experiment.py
python docs\research\dogfood\tools\validate_pass_0067_forum_routing_repair_experiment.py
crucible run docs\research\dogfood\crucible\pass-0067-thesis.json --measurements docs\research\dogfood\crucible\pass-0067-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0067-report.md --out docs\research\dogfood\crucible\pass-0067-run.json --json
```

## Next Pass

Run a multi-tool growth-vector steelman that turns this routing repair into a
broader improvement backlog. Each tool should get at least one executable
experiment, one market-facing wedge, one falsifier, and one adapter or
integration target.
