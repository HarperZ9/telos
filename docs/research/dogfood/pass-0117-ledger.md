# Pass 0117 Ledger: Theorem-Prover Adapter Receipt

Date: 2026-07-01

## Objective

Turn pass 0116's finite category witness into a theorem-prover adapter receipt.
The pass declares Lean-style theorem targets, records local prover availability,
keeps missing prover branches fenced, and uses the Python finite model as the
only positive verification witness.

This pass does not claim Lean, Rocq, Isabelle, or Agda execution.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_theorem_prover_adapter_receipt.py` | Theorem-prover adapter composer with finite model replay and unavailable prover fences. |
| `tools/test_theorem_prover_adapter_receipt.py` | Focused TDD test for pass 0117. |
| `tools/probe_theorem_prover_adapter_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0117_theorem_prover_adapter.py` | Independent validator for targets, availability, branches, countermodel, and boundaries. |
| `schemas/theorem-prover-adapter-receipt-pass-0117.json` | `TheoremProverAdapterReceipt/v1` artifact. |
| `schemas/pass-0117-theorem-prover-adapter-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0117.json` | Compact target, availability, branch, Forum, Index, Telos, compose, and test receipts. |
| `packets/127-theorem-prover-adapter-receipt.md` | Human-readable theorem-prover adapter packet. |
| `briefs/127-theorem-prover-adapter-brief.md` | Buyer-facing theorem-prover adapter brief. |
| `adversarial/pass-0117-theorem-prover-adapter-steelman.md` | Local pass 0117 steelman. |
| `crucible/pass-0117-thesis.json` | Falsifiable claims. |
| `crucible/pass-0117-measurements.json` | Measurements/evidence. |
| `crucible/pass-0117-report.md` | Crucible report. |
| `crucible/pass-0117-run.json` | Crucible run record. |

## Result

| Measurement | Value |
| --- | --- |
| Artifact status | `THEOREM_PROVER_ADAPTER_MATCH` |
| Artifact sha256 | `edce139ee88d7b173f57df9845e137042418112dd04fc01aab91dc310b380df2` |
| Artifact seal | `0acf2e699a4a24b1cc0a9426f3525d56d44edd3a7f418e269d1ab8a2cff1fa3e` |
| Formal/physics bridge pass | `0116` |
| Theorem targets | `3` |
| Prover branches | `5` |
| Source anchors | `7` |
| Unsupported claims | `0` |
| Current promoted natural laws | `0` |

## Local Prover Availability

| Executable | Status |
| --- | --- |
| `lean` | `MISSING` |
| `lake` | `MISSING` |
| `coqc` | `MISSING` |
| `isabelle` | `MISSING` |
| `agda` | `MISSING` |

## Theorem Targets

| Target | Proposition | Claim status | Proof object |
| --- | --- | --- | --- |
| `left_identity` | `idB_comp_f_eq_f` | `FINITE_MODEL_VERIFIED` | `NOT_EXECUTED_PROVER_UNAVAILABLE` |
| `right_identity` | `f_comp_idA_eq_f` | `FINITE_MODEL_VERIFIED` | `NOT_EXECUTED_PROVER_UNAVAILABLE` |
| `associativity` | `h_comp_g_comp_f_assoc` | `FINITE_MODEL_VERIFIED` | `NOT_EXECUTED_PROVER_UNAVAILABLE` |

## Prover Branches

| Branch | Status | Meaning |
| --- | --- | --- |
| `python_finite_model_replay` | `MATCH` | Exact finite function equality replay. |
| `lean4_target` | `UNAVAILABLE_FENCED` | `lean` executable missing. |
| `rocq_target` | `UNAVAILABLE_FENCED` | `coqc` executable missing. |
| `isabelle_target` | `UNAVAILABLE_FENCED` | `isabelle` executable missing. |
| `agda_target` | `UNAVAILABLE_FENCED` | `agda` executable missing. |

## Countermodel

The bad identity fixture maps `b0 -> b1` and `b1 -> b0`. Composing `f` with this
bad identity produces `a0 -> b1` and `a1 -> b0`, which differs from `f`.

Classification: `BAD_IDENTITY_DRIFT`.

## Source Anchors

| Tool | Source |
| --- | --- |
| Lean | `https://lean-lang.org/doc/reference/latest/` |
| Lean TPIL | `https://lean-lang.org/theorem_proving_in_lean4/` |
| Lean mathlib | `https://leanprover-community.github.io/mathlib4_docs/` |
| Lean Lake | `https://leanprover-community.github.io/install/project.html` |
| Rocq | `https://rocq-prover.org/` |
| Isabelle | `https://isabelle.in.tum.de/` |
| Agda | `https://agda.readthedocs.io/en/latest/getting-started/what-is-agda.html` |

## Gather

| Document | sha256 | seal |
| --- | --- | --- |
| `packets/127-theorem-prover-adapter-receipt.md` | `e2bcec920e2cfdf07a996f5a9a47002e96ad1121106417c28c4d854a3890b779` | `14e94f1732e5ee8a5e90636989c4f51a69604eb4f68f3faeb8a166bde81363c2` |
| `briefs/127-theorem-prover-adapter-brief.md` | `2a6243be5a04f9a708ac34e978abc89fe5bb637432b998c2c309f7d7ab3e1de2` | `fcb8f95335d0d018db78514dcdd6d279662d13210f46d58b04464bf2bcbc7087` |

## Crucible

| Measurement | Value |
| --- | --- |
| Thesis id | `1e8b9858c613e118` |
| Claims | `11` |
| MATCH | `11` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `9bd279cad24f495360899339f886ec9c89364af7914ab0727e058928de84c788` |
| Measurement seal | `2c315446d04224bbd6d9203bfa446e88ca97402f22b1645af1ec2e24d628a36c` |
| Assessment seal | `8ab92b1d41ddf9e0cae6b80a1ec12b0c0166adbb47f52c36cdf0ac63fb4005f8` |

Registry after pass 0117:

- theses: `108`;
- claims: `946`;
- verdicts: `946 MATCH`, `0 DRIFT`, `0 UNVERIFIABLE`.

## File Hashes

| File | sha256 |
| --- | --- |
| `schemas/pass-0117-theorem-prover-adapter-validator-result.json` | `54b864b82b3fafcdd6323edfb5ed51bfa17771af6e5e57c4cdbc3675c19edeb4` |
| `schemas/tool-receipts-pass-0117.json` | `6e71792a2774ee2c1f0bcb4981c2cf8586aefb9d221a45ff06a190fd3081ea2e` |
| `adversarial/pass-0117-theorem-prover-adapter-steelman.md` | `92f27e1d3ccd0809c86b886b47f9872814424fb714f095906b78888df9a37ac8` |
| `crucible/pass-0117-thesis.json` | `8d119cced7d0dce2894e8b0fe46bb4560d37fd92c32546a64a55847d96781ed0` |
| `crucible/pass-0117-measurements.json` | `5c3a968f85a02eebfad78b8edbb3c3c09f93501d59f5955d262dcc95d93f8e7d` |
| `crucible/pass-0117-report.md` | `aef9526790e86de91ff27f92fd6be437015feff1b5d3d49c447fff296b9c8b2f` |
| `crucible/pass-0117-run.json` | `3627273955c17323cb7eb0999558c3bd3e5e914ef056c8c17621141d38291464` |
| `tools/compose_theorem_prover_adapter_receipt.py` | `4262cb3ca01936f0ff9d6fcd67ca13161de3dbab28442a2321c78c2b8def922d` |
| `tools/test_theorem_prover_adapter_receipt.py` | `a66cff793a4ef9de7a0a2f605806cf91174766c58a273bbed6017888d34ae919` |
| `tools/validate_pass_0117_theorem_prover_adapter.py` | `eebbce8849be08aad38829ac0b023b385c541043365e2d17493ecbe73ab20cfd` |
| `tools/probe_theorem_prover_adapter_receipt.py` | `2ad72f98440fc87411b4cba006d6cc6724567c13f51898db7e18518542f7323a` |

## Verification Commands

```powershell
python docs\research\dogfood\tools\probe_theorem_prover_adapter_receipt.py
python docs\research\dogfood\tools\test_theorem_prover_adapter_receipt.py
python docs\research\dogfood\tools\validate_pass_0117_theorem_prover_adapter.py
python -m py_compile docs\research\dogfood\tools\compose_theorem_prover_adapter_receipt.py docs\research\dogfood\tools\test_theorem_prover_adapter_receipt.py docs\research\dogfood\tools\validate_pass_0117_theorem_prover_adapter.py docs\research\dogfood\tools\probe_theorem_prover_adapter_receipt.py
gather docs docs\research\dogfood\packets\127-theorem-prover-adapter-receipt.md --json
gather docs docs\research\dogfood\briefs\127-theorem-prover-adapter-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0117-thesis.json --measurements docs\research\dogfood\crucible\pass-0117-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0117-report.md --out docs\research\dogfood\crucible\pass-0117-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

The next useful pass is a local formalization packaging pass: emit concrete
Lean/Rocq/Isabelle/Agda target files as artifacts, hash them, and keep execution
fenced until a prover toolchain is available. The receipt should separate source
generation, parser/prover execution, and finite-model replay.
