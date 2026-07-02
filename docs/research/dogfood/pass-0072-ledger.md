# Pass 0072 Ledger: Domain-Focus Adapter Experiment

Date: 2026-07-01

Status: `MATCH_DOMAIN_FOCUS_ADAPTER_EXPERIMENT`

## Purpose

Test a multi-tool growth vector: can Project Telos route domain-specific work
for BuildLang/buildc, color calibration, AI4Science, agent ops, market recon,
and quantum/physics through a common adapter layer across Gather, Index, Forum,
Crucible, and Telos?

This pass does not implement the adapter in the flagship tools. It measures the
current live surfaces, records the failure modes, and defines the product shape
for the next implementation pass.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_domain_focus_adapter_experiment.py` | Live Forum/Index domain-focus experiment composer. |
| `tools/test_domain_focus_adapter_experiment.py` | Focused route/focus adapter test. |
| `tools/probe_domain_focus_adapter_experiment.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0072_domain_focus_adapter_experiment.py` | Validator for route counts, Index focus boundaries, negative fixtures, and seal. |
| `schemas/domain-focus-adapter-experiment-pass-0072.json` | `DomainFocusAdapterExperiment/v1` artifact. |
| `schemas/pass-0072-domain-focus-adapter-experiment-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0072.json` | Compact Index, Forum, Gather, Crucible, Telos, and shell receipts. |
| `packets/082-domain-focus-adapter-experiment.md` | Human-readable domain-focus adapter packet. |
| `adversarial/pass-0072-domain-focus-adapter-experiment-steelman.md` | Local steelman. |
| `crucible/pass-0072-thesis.json` | Falsifiable claims. |
| `crucible/pass-0072-measurements.json` | Measurements/evidence. |
| `crucible/pass-0072-report.md` | Crucible report. |
| `crucible/pass-0072-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Domain rows | 6 |
| Raw Forum route escalations | 6 |
| Adapted Forum route decisions | 6 `project-telos` |
| Adapted Forum route escalations | 0 |
| Average Project Telos score lift | 0.393939 |
| Valid Index focuses | `telos` |
| Rejected Index focuses | 7 |
| Tool improvement rows | 5 |
| Negative fixtures | 6 |
| Unsupported claims | 0 |

## Domain Rows

- `buildlang_buildc`: BuildLang/buildc scientific compute.
- `color_calibration`: color calibration and rendering measurement.
- `ai4science`: AI4Science research proof packets.
- `agent_ops`: agent operations and action receipts.
- `market_recon`: market recon and buyer evidence.
- `quantum_physics`: quantum and physics proof packets.

Each raw prompt escalated. Each adapted prompt using the five-flagship
operator-spine vocabulary routed to `project-telos` without escalation.

## Tool Improvement Queue

- Index: add path/domain focus resolution over repo-root context envelopes.
- Forum: teach domain-focus vocabulary directly so manual bridge wording is not required.
- Gather: emit domain packet catalogs keyed by field, buyer, source family, and proof-demo stage.
- Crucible: standardize route/focus negative fixtures as reusable promotion gates.
- Telos: define `TelosDomainFocusEnvelope/v1` as a product join layer across source, context, route, verification, continuity, and action receipts.

## Steelman

The pass demonstrates a route vocabulary bridge and an adapter contract. It
does not implement true Index path focus, semantic repo slicing, market proof,
or scientific discovery. The strongest finding is practical: our system needs a
first-class domain-focus layer before it can scale from generic root context to
field-specific proof packets.

## Tool Findings

- Index status returned `MATCH`; only `--focus telos` matched, while `docs/research/dogfood`, `buildc`, `buildlang`, `color`, `forum`, `gather`, and `crucible` were rejected as unknown focus repos.
- Forum doctor returned `MATCH`; raw domain prompts escalated, adapted operator-spine prompts routed.
- Gather read packet 082 with SHA256 `5cf28727160169d5147ad23b278dded219dbda640070caaba97e05d99785b518` and digest seal `cd254ea7a31e1b79d4d2d7613e433cfc425027892dcfd8c1d57297644f046f2a`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `eb9fe6ecfc658f38`.
- Crucible assessment seal: `c1551300a0baab4dec1d13a26610dccd48856ed5b4a9be47b8e676917477e447`.
- Crucible registry stats after this pass: 60 theses, 497 claims, 497 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Telos product gap: domain focus is not yet a first-class envelope joining source, context, route, verification, continuity, and action receipts.

## Verification

```powershell
python docs\research\dogfood\tools\test_domain_focus_adapter_experiment.py
python docs\research\dogfood\tools\probe_domain_focus_adapter_experiment.py
python docs\research\dogfood\tools\validate_pass_0072_domain_focus_adapter_experiment.py
crucible run docs\research\dogfood\crucible\pass-0072-thesis.json --measurements docs\research\dogfood\crucible\pass-0072-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0072-report.md --out docs\research\dogfood\crucible\pass-0072-run.json --json
```

## Next Pass

Implement a local `TelosDomainFocusEnvelope/v1` fixture that joins one domain
row to source-intake, root context, route bridge, Crucible verdict, continuity,
and action receipts. The next hardening step after that is replacing the
root-context fallback with real path-scoped Index source refs.
