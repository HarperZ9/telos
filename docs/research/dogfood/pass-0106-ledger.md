# Pass 0106 Ledger: Stoichiometric Invariant Checker Receipt

Date: 2026-07-01

Status: `STOICHIOMETRIC_INVARIANT_CHECKER_RECEIPT_MATCH`

## Purpose

Generalize the pass 0105 reaction invariant from one hand-written `A -> B`
equation into a stoichiometric-matrix checker. This pass derives a conserved
quantity from `l^T S = 0`, probes a closed three-species reaction cycle, and
rejects a leaky open-system fixture.

The result is a scoped `LAW_CANDIDATE`, not a promoted natural law.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_stoichiometric_invariant_checker_receipt.py` | Builds source anchors, exact left-nullspace derivation, numerical probe, negative fixture, YouTube binding, and Forum/Index/Telos receipts. |
| `tools/test_stoichiometric_invariant_checker_receipt.py` | Focused TDD test for source bindings, conservation vector, numerical drift, and negative fixture. |
| `tools/probe_stoichiometric_invariant_checker_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0106_stoichiometric_invariant_checker.py` | Independent validator for seal, source bindings, invariant residual, probes, and boundaries. |
| `schemas/stoichiometric-invariant-checker-receipt-pass-0106.json` | `StoichiometricInvariantCheckerReceipt/v1` artifact. |
| `schemas/pass-0106-stoichiometric-invariant-checker-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0106.json` | Compact stoichiometric checker, Forum, Index, Telos, compose, and test receipts. |
| `packets/116-stoichiometric-invariant-checker-receipt.md` | Human-readable stoichiometric invariant packet. |
| `briefs/116-stoichiometric-invariant-checker-brief.md` | Buyer-facing stoichiometric invariant brief. |
| `adversarial/pass-0106-stoichiometric-invariant-checker-steelman.md` | Local pass 0106 steelman. |
| `crucible/pass-0106-thesis.json` | Falsifiable claims. |
| `crucible/pass-0106-measurements.json` | Measurements/evidence. |
| `crucible/pass-0106-report.md` | Crucible report. |
| `crucible/pass-0106-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Reaction source pass | 0105 |
| AI4Science source pass | 0104 |
| YouTube source pass | 0085 |
| YouTube roadmap pass | 0102 |
| Valid YouTube videos | 19 |
| Transcript receipts | 19 |
| Closed network | `A_to_B`, `B_to_C`, `C_to_A` |
| Stoichiometric matrix rows | `A[-1,0,1]`, `B[1,-1,0]`, `C[0,1,-1]` |
| Derived vector | `[1, 1, 1]` |
| Invariant | `A+B+C` |
| Residual | `[0, 0, 0]` |
| Grid points | 201 |
| Closed-cycle max total drift | `3.9968028886505635e-15` |
| Negative fixture | `cycle_with_C_sink` |
| Negative candidate residual | `[0, 0, 0, -1]` |
| Negative fixture drift | `0.455672581497486` |
| Law candidate | `stoichiometric_left_nullspace_conservation_invariant` |
| Law status | `LAW_CANDIDATE` |
| Unsupported claim count | 0 |
| Promoted natural laws | 0 |
| Artifact file SHA256 | `cb526f4bc62693a0eef2b6c804a3c76fe8b67f7a5286086b01fe0574e4b3f83b` |
| Artifact seal | `93ee54b44bc5b863fb386e08067ce1ee69747bf8395ac07aacaea8fbfd9ad5f8` |

## Source Anchors

| Source | URL | Evidence Role |
| --- | --- | --- |
| The Convex Basis of the Left Null Space of the Stoichiometric Matrix | `https://pmc.ncbi.nlm.nih.gov/articles/PMC1303061/` | Left-nullspace conservation source anchor. |
| What makes a reaction network chemical? | `https://pmc.ncbi.nlm.nih.gov/articles/PMC9484159/` | Stoichiometric conservation-structure source anchor. |
| Catalyst.jl CRN Theory | `https://docs.sciml.ai/Catalyst/stable/network_analysis/crn_theory/` | Official reaction-network conservation-law source anchor. |
| Catalyst.jl Network Analysis API | `https://docs.sciml.ai/Catalyst/stable/api/network_analysis_api/` | Official conservation-law API source anchor. |
| EQTK Core Concepts | `https://eqtk.github.io/user_guide/core_concepts.html` | Conservation matrix/nullspace source anchor. |

## Product Finding

The YouTube corpus should be treated as architecture pressure, not claim proof.
Pass 0106 converts that pressure into an executable AI4Science primitive:
source-backed invariant derivation, numerical probe, explicit negative fixture,
and promotion boundary. This is a better compound step than another strategy
matrix because it gives BuildLang/buildc and AI4Science packets a concrete
receipt target.

The next architectural step is a reaction-network corpus harness that can run
the checker across multiple stoichiometric matrices, attach BuildLang runtime
receipts, and reject unsupported discovery claims before any lab or market
language is allowed.

## Tool Findings

- TDD red observed before the composer existed: `FileNotFoundError`.
- Forum route receipt: `MATCH`.
- Index context envelope: `MATCH`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `e057301b473aa8ac5adcb5e19540e57fb83025796bd5b33f99944b9ecf7b04e8`,
  digest seal `d1e8721775e625712071c9b818919e9fbb3862c95b99f80cc25ce452ba46067d`.
- Gather brief receipt: SHA256
  `d3e013dcc2e0b0ea3e46a5bdcfd1849d67c37cf7310723384f55d6c437b7584d`,
  digest seal `3e50efa736549d099a04898daddba538bc11b77e859d11e66cfe638871a37620`.
- Crucible result: 10 claims, 10 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `168ec59cc8f13dfb`.
- Crucible assessment seal:
  `52406f08f04bafa5bf94976de79e7b3e52f1183945f2c2e9943b7b2dddec7ff3`.
- Crucible registry stats after this pass: 95 theses, 796 claims, 796 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not prove a new natural law, biological discovery, wet-lab
result, or production scientific runtime. It proves and probes a bounded
conservation invariant for a toy closed reaction network, then rejects a leaky
negative fixture.

## Verification

```powershell
python docs\research\dogfood\tools\test_stoichiometric_invariant_checker_receipt.py
python -m py_compile docs\research\dogfood\tools\compose_stoichiometric_invariant_checker_receipt.py docs\research\dogfood\tools\test_stoichiometric_invariant_checker_receipt.py docs\research\dogfood\tools\validate_pass_0106_stoichiometric_invariant_checker.py docs\research\dogfood\tools\probe_stoichiometric_invariant_checker_receipt.py
python docs\research\dogfood\tools\probe_stoichiometric_invariant_checker_receipt.py
python docs\research\dogfood\tools\validate_pass_0106_stoichiometric_invariant_checker.py
crucible run docs\research\dogfood\crucible\pass-0106-thesis.json --measurements docs\research\dogfood\crucible\pass-0106-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0106-report.md --out docs\research\dogfood\crucible\pass-0106-run.json --json
gather docs docs\research\dogfood\packets\116-stoichiometric-invariant-checker-receipt.md --json
gather docs docs\research\dogfood\briefs\116-stoichiometric-invariant-checker-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Turn the stoichiometric checker into a reaction-network corpus harness with
multiple closed and open networks, then attach a BuildLang/buildc runtime receipt
for at least one generated invariant kernel.
