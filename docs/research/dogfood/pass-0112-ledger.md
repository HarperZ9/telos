# Pass 0112 Ledger: Lyapunov Stability Certificate Receipt

Date: 2026-07-01

## Objective

Move laterally into control theory and create a bounded exact Lyapunov
stability certificate receipt. The pass proves one rational discrete-time
linear-system identity, records negative fixtures, binds official control and
optimization source anchors, and preserves the YouTube corpus as source-lead
architecture data rather than scientific proof.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_lyapunov_stability_certificate_receipt.py` | Exact Lyapunov certificate composer plus Forum, Index, and Telos receipts. |
| `tools/test_lyapunov_stability_certificate_receipt.py` | Focused TDD test for pass 0112. |
| `tools/probe_lyapunov_stability_certificate_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0112_lyapunov_stability_certificate.py` | Independent validator for exact residuals, fixtures, source anchors, and boundaries. |
| `schemas/lyapunov-stability-certificate-receipt-pass-0112.json` | `LyapunovStabilityCertificateReceipt/v1` artifact. |
| `schemas/pass-0112-lyapunov-stability-certificate-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0112.json` | Compact certificate, market, YouTube, Forum, Index, Telos, compose, and test receipts. |
| `packets/122-lyapunov-stability-certificate-receipt.md` | Human-readable Lyapunov certificate packet. |
| `briefs/122-lyapunov-stability-certificate-brief.md` | Buyer-facing control certificate brief. |
| `adversarial/pass-0112-lyapunov-stability-certificate-steelman.md` | Local pass 0112 steelman. |
| `crucible/pass-0112-thesis.json` | Falsifiable claims. |
| `crucible/pass-0112-measurements.json` | Measurements/evidence. |
| `crucible/pass-0112-report.md` | Crucible report. |
| `crucible/pass-0112-run.json` | Crucible run record. |

## Result

| Measurement | Value |
| --- | --- |
| Artifact status | `LYAPUNOV_STABILITY_CERTIFICATE_RECEIPT_MATCH` |
| Artifact sha256 | `0066b268d07d31afc077667d226bee0723c1e2ff6cc8c50dce8e1b4a6afb35db` |
| Artifact seal | `fcb8647a852df0d3fa14ed16115e9cc15cb812427012773b4cca5a967bb31ac4` |
| Runtime suite pass | `0111` |
| YouTube roadmap pass | `0102` |
| Stable system A | `[[1/2, 0], [0, 1/3]]` |
| Certificate P | `[[4/3, 0], [0, 9/8]]` |
| Q | `[[1, 0], [0, 1]]` |
| Spectral radius bound | `1/2` |
| Lyapunov residual | `[[0, 0], [0, 0]]` |
| Energy sample count | `3` |
| Unstable fixture | `PD_FAIL_EXPECTED` |
| Bad certificate fixture | `RESIDUAL_DRIFT_EXPECTED` |
| Source anchors | `10` |
| Market tools | `9` |
| Valid YouTube videos | `19` |
| Raw transcripts included | `false` |
| Unsupported claims | 0 |
| Current promoted natural laws | 0 |

## Exact Identity

For the stable fixture:

```text
A = [[1/2, 0], [0, 1/3]]
Q = [[1, 0], [0, 1]]
P = [[4/3, 0], [0, 9/8]]
A^T P A - P + Q = 0
V(Ax) - V(x) = -x^T Q x
```

Energy samples:

| x | Delta V | -xTQx | Status |
| --- | --- | --- | --- |
| `[1, 0]` | `-1` | `-1` | `MATCH` |
| `[0, 2]` | `-4` | `-4` | `MATCH` |
| `[3, -2]` | `-13` | `-13` | `MATCH` |

## Source Anchors

| Tool | URL |
| --- | --- |
| SciPy | `https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_discrete_lyapunov.html` |
| MATLAB dlyap | `https://www.mathworks.com/help/control/ref/dlyap.html` |
| MATLAB Control System Toolbox | `https://www.mathworks.com/products/control.html` |
| python-control | `https://python-control.readthedocs.io/en/0.10.2/generated/control.dlyap.html` |
| Drake | `https://drake.mit.edu/` |
| CasADi | `https://web.casadi.org/docs/` |
| do-mpc | `https://www.do-mpc.com/` |
| OSQP MPC | `https://osqp.org/docs/examples/mpc.html` |
| CVXPY | `https://www.cvxpy.org/` |
| MIT Underactuated Lyapunov | `https://underactuated.mit.edu/lyapunov.html` |

## Gather

| Document | sha256 | seal |
| --- | --- | --- |
| `packets/122-lyapunov-stability-certificate-receipt.md` | `98502565de3a9af4a87060e5daaa89da9a899b80b4cf41d825648a88ee25cb34` | `4e28f1af00f76d397e753c4dadcb4a59096448e1097315db4c032fd056629348` |
| `briefs/122-lyapunov-stability-certificate-brief.md` | `436ec3b7c0076723af4c330b97077f3129740c4a6df5a4b583c6f06aa582e057` | `f57689867459d503c1da54d177a5f5ba4bb9ab4710c09125a0cdb3b203c69d45` |

## Crucible

| Measurement | Value |
| --- | --- |
| Thesis id | `35de33b8086c12f0` |
| Claims | 11 |
| MATCH | 11 |
| DRIFT | 0 |
| UNVERIFIABLE | 0 |
| Verdict seal | `d2499c5ae0fe9131e78f24b699c611841951fe5783c724373ef704b831f5a74f` |
| Measurement seal | `1c277b4b1ee2982243a2fc8006b522920ab552a15ce6545888b9faa59047508c` |
| Assessment seal | `ba240749a78fc0517109a228cf4451f62cd21337750dc78097a50c3aea86b09f` |

Registry after pass 0112:

- theses: `101`;
- claims: `864`;
- verdicts: `864 MATCH`, `0 DRIFT`, `0 UNVERIFIABLE`.

## Verification Commands

```powershell
python -m py_compile docs\research\dogfood\tools\compose_lyapunov_stability_certificate_receipt.py docs\research\dogfood\tools\test_lyapunov_stability_certificate_receipt.py docs\research\dogfood\tools\validate_pass_0112_lyapunov_stability_certificate.py docs\research\dogfood\tools\probe_lyapunov_stability_certificate_receipt.py
python docs\research\dogfood\tools\probe_lyapunov_stability_certificate_receipt.py
python docs\research\dogfood\tools\test_lyapunov_stability_certificate_receipt.py
python docs\research\dogfood\tools\validate_pass_0112_lyapunov_stability_certificate.py
gather docs docs\research\dogfood\packets\122-lyapunov-stability-certificate-receipt.md --json
gather docs docs\research\dogfood\briefs\122-lyapunov-stability-certificate-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0112-thesis.json --measurements docs\research\dogfood\crucible\pass-0112-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0112-report.md --out docs\research\dogfood\crucible\pass-0112-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

The next useful control pass is a constrained-MPC feasibility receipt: bind a
linear system, constraint set, finite horizon, candidate control sequence,
state rollout, violation checks, negative infeasible fixture, and proof packet
source anchors.
