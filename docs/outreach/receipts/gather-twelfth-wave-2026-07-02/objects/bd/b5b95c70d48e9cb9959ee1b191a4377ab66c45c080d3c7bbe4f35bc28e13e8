# Pass 0101 Ledger: Inequality-Safe BQM Receipt

Date: 2026-07-01

Status: `INEQUALITY_SAFE_BQM_RECEIPT_MATCH`

## Purpose

Convert the Ocean/dimod BQM branch from pass 0100 into a falsification pass.
The pass shows that a squared equality-to-capacity penalty is not a general
encoding of a `<= capacity` knapsack constraint, then records a slack-variable
BQM that recovers the true feasible optimum on the same bounded fixture.

This is a law candidate, not a promoted natural law.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_inequality_safe_bqm_receipt.py` | Creates a temp venv, installs `dimod`, runs equality and slack BQMs, records Forum/Index/Telos receipts, and cleans temp state. |
| `tools/test_inequality_safe_bqm_receipt.py` | Focused counterexample, slack-fix, and promotion-boundary test. |
| `tools/probe_inequality_safe_bqm_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0101_inequality_safe_bqm.py` | Independent validator for artifact seal, fixture values, solver outputs, and boundaries. |
| `schemas/inequality-safe-bqm-receipt-pass-0101.json` | `InequalitySafeBQMReceipt/v1` artifact. |
| `schemas/tool-receipts-pass-0101.json` | Compact compose, test, Forum, Index, Telos, and law-candidate receipts. |
| `packets/111-inequality-safe-bqm-receipt.md` | Human-readable inequality-safe BQM packet. |
| `briefs/111-inequality-safe-bqm-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0101-inequality-safe-bqm-steelman.md` | Local steelman of BQM-encoding and scope limits. |
| `crucible/pass-0101-thesis.json` | Falsifiable claims. |
| `crucible/pass-0101-measurements.json` | Measurements/evidence. |
| `crucible/pass-0101-report.md` | Crucible report. |
| `crucible/pass-0101-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Source binding | pass 0100 Ocean/dimod local BQM branch |
| Global dimod available | false |
| Temporary venv path | `C:\Users\Zain\AppData\Local\Temp\telos-inequality-bqm-pass0101` |
| Temporary venv created | true |
| Temporary venv cleaned | true |
| dimod version | `0.12.22` |
| Problem values | `[10, 9]` |
| Problem weights | `[3, 2]` |
| Capacity | 4 |
| Penalty | 100 |
| True feasible optimum | value 10, weight 3, items `[0]` |
| Equality-to-capacity BQM result | value 19, weight 5, feasible false |
| Slack-variable BQM result | value 10, weight 3, feasible true |
| Law candidate | `knapsack_inequality_bqm_requires_slack_or_inequality_encoding` |
| Unsupported claim count | 0 |
| Promoted natural laws | 0 |
| Artifact file SHA256 | `c48b4fd7e6ef88dddfbb0f8a895bcdc97b91443c31de9641072784fba324f5c2` |
| Artifact seal | `cd3fc1e66878fb9529f8e0c61890830819fcc3456dce0a96a24dcbfdf7eb4b1a` |

## Product Finding

The optimization proof workbench needs explicit inequality-safe encodings before
it presents BQM or annealing branches as solver-equivalent. A receipt layer that
records constraint encoding, counterexamples, slack variables, feasibility, and
true-optimum cross-checks is a product advantage over raw solver invocation.

This finding should flow into BuildLang/buildc and solver branch receipts as an
adapter requirement: each optimization branch should declare whether a constraint
is equality, inequality, slack-encoded, penalty-encoded, or externally enforced.

## Tool Findings

- Forum route receipt: `MATCH`.
- Index context envelope: `MATCH`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `1f5f3a08120f9eea2f2ea7f157f5ea41b104963b6dacf002c380c70804c346a3`,
  digest seal `aca07540a759f77ac03a3bd8958a1314f983400fc170e6267dfd6e95ef9344dd`.
- Gather brief receipt: SHA256
  `b631d91056eaf3e4de5fc9f270e1d55be69a2977dab4e01f0b6715ddd4ece4d8`,
  digest seal `77460dd09d00043228c894dfcddabb4ac98fada6a4e5f15cef9f45ac8b1e3740`.
- Crucible result: 9 claims, 9 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `9cca4f833c111044`.
- Crucible assessment seal:
  `8109ff2795a2081ca4da6951010007f4b0d9a2c2d5ff04bbddfa2579663c0cda`.
- Observed registry stats after this pass: 89 theses, 740 claims, 740 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not prove QPU execution, hybrid-provider execution, quantum
advantage, production-scale optimization, or a promoted law. It proves one
bounded counterexample and one bounded slack-variable repair under local CPU
exact BQM solving.

## Verification

```powershell
python -m py_compile docs\research\dogfood\tools\compose_inequality_safe_bqm_receipt.py docs\research\dogfood\tools\test_inequality_safe_bqm_receipt.py docs\research\dogfood\tools\validate_pass_0101_inequality_safe_bqm.py docs\research\dogfood\tools\probe_inequality_safe_bqm_receipt.py
python docs\research\dogfood\tools\probe_inequality_safe_bqm_receipt.py
python docs\research\dogfood\tools\test_inequality_safe_bqm_receipt.py
python docs\research\dogfood\tools\validate_pass_0101_inequality_safe_bqm.py
crucible run docs\research\dogfood\crucible\pass-0101-thesis.json --measurements docs\research\dogfood\crucible\pass-0101-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0101-report.md --out docs\research\dogfood\crucible\pass-0101-run.json --json
gather docs docs\research\dogfood\packets\111-inequality-safe-bqm-receipt.md --json
gather docs docs\research\dogfood\briefs\111-inequality-safe-bqm-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Use the operator-supplied YouTube videos as crucial source data for a broader
growth-vector pass. The next packet should ingest the links as source leads,
capture metadata/transcript availability where possible, and separate video
claims from verified external sources before using them to steer architecture.
