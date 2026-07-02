# crucible report: Dogfood Pass 0013 Quantum Experiment Receipt Branch Separation

## Summary

- thesis_id: `f913da2728a49106`
- thesis_seal: `f913da2728a4910617a6b67c061741351194dcbf79e42b4c157bfdd3b7787124`
- assessment_seal: `3fc5059ece29da40f18768f7ee5893830c17d137dbedf4f184650a0505dd331f`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0013 created a QuantumExperimentReceiptSchema/v1 artifact with required receipt fields, four branch values, and branch_promotion_forbidden set to true. | MATCH | fenced | 1 | schema-review | deviation 0 within tolerance 0.5 |
| Pass 0013 created a QuantumExperimentReceiptSet/v1 fixture with exact and noisy simulator receipts, status RECEIPT_SET_MATCH, branch separation status BRANCH_SEPARATION_MATCH, and seal e5bcaf8a0cbe73fd51d6745539a8fca2ea1faff3ff9f375fe94a646761ce3ea9. | MATCH | fenced | 1 | receipt-set-review | deviation 0 within tolerance 0.5 |
| The pass 0013 exact simulator branch records hardware_claim_allowed=false, fidelity_to_desired_clone=0.5, and computational-basis histogram {00:0.5, 01:0.0, 10:0.0, 11:0.5}. | MATCH | fenced | 1 | exact-branch-review | deviation 0 within tolerance 0.5 |
| The pass 0013 noisy simulator branch records hardware_claim_allowed=false, status NOISY_BRANCH_NOT_THEOREM_PROOF, histogram_l1_drift_from_exact=0.0, and fidelity_to_desired_clone=0.45. | MATCH | fenced | 1 | noisy-branch-review | deviation 0 within tolerance 0.5 |
| Pass 0013 records the negative evidence lesson that identical computational-basis histograms can hide phase-sensitive fidelity drift, so histogram equality alone is insufficient evidence. | MATCH | fenced | 1 | negative-fixture-review | deviation 0 within tolerance 0.5 |
| The pass 0013 validator reports MATCH with two matched checks and zero drift. | MATCH | fenced | 1 | validator-run-review | deviation 0 within tolerance 0.5 |
| Pass 0013 attempted Forum submit paths, preserved the executor JSON parsing error as UNVERIFIABLE, and did not treat the local steelman as a witnessed Forum adversarial result. | MATCH | fenced | 1 | forum-tool-review | deviation 0 within tolerance 0.5 |
| Pass 0013 promotes zero new quantum hardware results, quantum advantage claims, theorem proofs, natural laws, or scientific discoveries. | MATCH | fenced | 1 | non-promotion-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0013 created a QuantumExperimentReceiptSchema/v1 artifact with required receipt fields, four branch values, and branch_promotion_forbidden set to true. | schema-review | schemas/quantum-experiment-receipt-schema-pass-0013.json schema=QuantumExperimentReceiptSchema/v1; required_receipt_fields include receipt_id, schema, branch, hardware_claim_allowed, theorem_claim_ref, circuit, backend, resource_estimate, result, verdict; branch_values include EXACT_SIMULATOR, NOISY_SIMULATOR, HARDWARE_MOCK, CLOUD_HARDWARE; branch_promotion_forbidden=true; source_anchors include Qiskit Aer, IBM Quantum, Cirq, Azure Quantum Resource Estimator, Amazon Braket, and IonQ |
| Pass 0013 created a QuantumExperimentReceiptSet/v1 fixture with exact and noisy simulator receipts, status RECEIPT_SET_MATCH, branch separation status BRANCH_SEPARATION_MATCH, and seal e5bcaf8a0cbe73fd51d6745539a8fca2ea1faff3ff9f375fe94a646761ce3ea9. | receipt-set-review | schemas/quantum-experiment-receipts-pass-0013.json schema=QuantumExperimentReceiptSet/v1; status=RECEIPT_SET_MATCH; receipt branches include EXACT_SIMULATOR and NOISY_SIMULATOR; branch_separation.status=BRANCH_SEPARATION_MATCH; seal=e5bcaf8a0cbe73fd51d6745539a8fca2ea1faff3ff9f375fe94a646761ce3ea9 |
| The pass 0013 exact simulator branch records hardware_claim_allowed=false, fidelity_to_desired_clone=0.5, and computational-basis histogram {00:0.5, 01:0.0, 10:0.0, 11:0.5}. | exact-branch-review | receipt_id=quantum-exp-pass-0013-exact-simulator; branch=EXACT_SIMULATOR; hardware_claim_allowed=false; result.status=FAILS_CLONING_AS_EXPECTED; fidelity_to_desired_clone=0.5; measurement_histogram 00=0.5, 01=0.0, 10=0.0, 11=0.5 |
| The pass 0013 noisy simulator branch records hardware_claim_allowed=false, status NOISY_BRANCH_NOT_THEOREM_PROOF, histogram_l1_drift_from_exact=0.0, and fidelity_to_desired_clone=0.45. | noisy-branch-review | receipt_id=quantum-exp-pass-0013-noisy-simulator; branch=NOISY_SIMULATOR; hardware_claim_allowed=false; result.status=NOISY_BRANCH_NOT_THEOREM_PROOF; histogram_l1_drift_from_exact=0.0; fidelity_to_desired_clone=0.45 |
| Pass 0013 records the negative evidence lesson that identical computational-basis histograms can hide phase-sensitive fidelity drift, so histogram equality alone is insufficient evidence. | negative-fixture-review | schemas/quantum-experiment-receipts-pass-0013.json branch_separation.histogram_warning records identical histogram insufficiency; packets/023-quantum-experiment-receipts.md states histogram_l1_drift_from_exact=0.0; packets/023-quantum-experiment-receipts.md states exact fidelity=0.5 and noisy fidelity=0.45; packets/023-quantum-experiment-receipts.md forbids histogram match to state/fidelity match promotion |
| The pass 0013 validator reports MATCH with two matched checks and zero drift. | validator-run-review | schemas/pass-0013-quantum-experiment-validator-result.json status=MATCH; match=2; drift=0; checks include QuantumExperimentReceiptSchema status MATCH; checks include QuantumExperimentReceiptSet status MATCH |
| Pass 0013 attempted Forum submit paths, preserved the executor JSON parsing error as UNVERIFIABLE, and did not treat the local steelman as a witnessed Forum adversarial result. | forum-tool-review | adversarial/pass-0013-branch-separation-steelman.md status=UNVERIFIABLE for Forum submit; Forum status entries=3 checkpoint=a146467e8ef2c07fac3932cf8ce3900a532b8829795d6bf377f012f476b62668; Forum verify chain=true deep=true; Forum submit error recorded: configured executor did not return valid JSON; file states this pass does not claim a witnessed Forum adversarial answer |
| Pass 0013 promotes zero new quantum hardware results, quantum advantage claims, theorem proofs, natural laws, or scientific discoveries. | non-promotion-review | packets/023-quantum-experiment-receipts.md states target is not a new theorem, quantum hardware result, or quantum-advantage claim; schemas/quantum-experiment-receipt-schema-pass-0013.json non_promotion_policy forbids hardware result without CLOUD_HARDWARE and hardware_claim_allowed=true; schemas/quantum-experiment-receipt-schema-pass-0013.json non_promotion_policy forbids theorem promotion from experiment receipt alone; Current promoted natural laws: none |
