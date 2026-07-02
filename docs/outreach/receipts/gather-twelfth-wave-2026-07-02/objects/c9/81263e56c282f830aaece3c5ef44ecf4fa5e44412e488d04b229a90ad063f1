# Pass 0066 Ledger: Tool Growth-Vector Experiment Matrix

Date: 2026-07-01

Status: `MATCH_TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX`

## Purpose

Respond to the growth-vector requirement across the whole substrate rather than
one tool. This pass maps experiments for Gather, Index, Forum, Crucible, Telos,
BuildLang/buildc, build-universe, color calibration, browser evidence, model
foundry, loop ledger, and action receipts.

The point is not a static roadmap. Each vector carries a success metric and a
falsifier so future passes can promote only the rows that become executable
adapters, benchmarks, buyer proof packets, or mathematical proof packets.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_tool_growth_vector_experiment_matrix.py` | Deterministic growth-vector matrix composer. |
| `tools/test_tool_growth_vector_experiment_matrix.py` | Focused RED/GREEN matrix test. |
| `tools/probe_tool_growth_vector_experiment_matrix.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0066_tool_growth_vector_experiment_matrix.py` | Validator for tools, source anchors, vector counts, centrality, and non-promotion controls. |
| `schemas/tool-growth-vector-experiment-matrix-pass-0066.json` | `ToolGrowthVectorExperimentMatrix/v1` artifact. |
| `schemas/pass-0066-tool-growth-vector-experiment-matrix-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0066.json` | Compact Index, Gather, Forum, Crucible, Telos, and shell receipts. |
| `packets/076-tool-growth-vector-experiment-matrix.md` | Human-readable growth-vector packet. |
| `adversarial/pass-0066-tool-growth-vector-experiment-matrix-steelman.md` | Local steelman. |
| `crucible/pass-0066-thesis.json` | Falsifiable claims. |
| `crucible/pass-0066-measurements.json` | Measurements/evidence. |
| `crucible/pass-0066-report.md` | Crucible report. |
| `crucible/pass-0066-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Internal tools | 12 |
| Source anchors | 16 |
| Growth vectors | 36 |
| Cross-tool experiments | 10 |
| Top bundle | `proof_os_core` |
| Top synergy nodes | Telos, Crucible, Forum, Gather, Index |
| Telos centrality | 8 |
| Crucible centrality | 7 |
| Previous pass binding | 0065 |
| Unsupported claims | 0 |
| Promotion state | `EXPERIMENT_MATRIX_NOT_MARKET_PROOF` |

## Top Growth Bundles

| Bundle | Market | Tools |
| --- | --- | --- |
| `proof_os_core` | research and agent proof packets | Gather, Index, Forum, Crucible, Telos |
| `accountable_agent_ops` | regulated agent operations | action receipts, loop ledger, browser evidence, Crucible, Telos |
| `accountable_scientific_compute` | scientific runtime receipts | BuildLang/buildc, build-universe, Crucible, Telos |
| `visual_truth_lab` | color/render measurement proof | color calibration, browser evidence, Crucible, Telos |

## Cross-Tool Experiment Queue

| Experiment | Expected receipt |
| --- | --- |
| `proof_os_core` | claim-to-verdict packet |
| `regulated_agent_spine` | trace-to-receipt packet |
| `scientific_runtime_spine` | compiler-runtime proof receipt |
| `color_truth_spine` | measured color proof kit |
| `ai4science_lab_spine` | research proof packet |
| `routing_repair_spine` | route vocabulary repair receipt |
| `browser_to_claim_spine` | browser evidence claim packet |
| `model_improvement_spine` | model workflow improvement receipt |
| `package_ecosystem_spine` | adapter package map |
| `market_learning_spine` | buyer learning loop packet |

## Tool Findings

- Index status returned `MATCH`.
- Gather read packet 076 with SHA256 `9f17054cbe5da12d9a1daa026a69d9ed399a9689a1292c7f8af0f20880291033` and digest seal `528f2b3bc57d8a48e0aa7b3d6a8131a7a2ea3f7b95489a3a7fa6e1ae714db11d`.
- Forum ledger verified `chain=true`, `deep=true`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `2db3715432cdda7a`.
- Crucible assessment seal: `c06cdf720e52bc35581cc827978606939f17ba90651620260a4d7b6685796944`.
- Crucible registry stats after this pass: 54 theses, 449 claims, 449 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Telos workflow returned `MATCH`.

## Verification

```powershell
python docs\research\dogfood\tools\test_tool_growth_vector_experiment_matrix.py
python docs\research\dogfood\tools\probe_tool_growth_vector_experiment_matrix.py
python docs\research\dogfood\tools\validate_pass_0066_tool_growth_vector_experiment_matrix.py
crucible run docs\research\dogfood\crucible\pass-0066-thesis.json --measurements docs\research\dogfood\crucible\pass-0066-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0066-report.md --out docs\research\dogfood\crucible\pass-0066-run.json --json
```

## Next Pass

Promote one growth vector into an executable experiment. Best candidates:

1. `routing_repair_spine`: repair the cross-domain Forum escalation found in pass 0063.
2. `scientific_runtime_spine`: build another bounded equation/proof packet with a compiler/runtime receipt shape.
3. `color_truth_spine`: turn color calibration into a measured visual truth fixture.
