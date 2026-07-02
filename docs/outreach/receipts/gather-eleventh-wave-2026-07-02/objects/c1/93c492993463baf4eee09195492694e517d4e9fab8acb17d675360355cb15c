# crucible report: Dogfood Pass 0012 Quantum No-Cloning Proof Packet

## Summary

- thesis_id: `123dcf1159cd431d`
- thesis_seal: `123dcf1159cd431d5981bc66a02bc6f317bfc6774813c262de9de8f5e1093407`
- assessment_seal: `70fff2aa721b83ed088980398822071e62e1c5aebf0aa7afbd6d3fbadf4912f9`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0012 created a NoCloningProbe/v1 artifact reporting PROBE_MATCH: CNOT clones \|0> and \|1> basis fixtures with fidelity 1.0 and fails the \|+> superposition clone fixture with fidelity 0.5. | MATCH | fenced | 1 | probe-review | deviation 0 within tolerance 0.5 |
| Pass 0012 records the inner-product no-cloning impossibility for \|0> and \|+>, including overlap 0.707106781186547, overlap_squared 0.5, and positive defect 0.207106781186548. | MATCH | fenced | 1 | inner-product-review | deviation 0 within tolerance 0.5 |
| Pass 0012 created a 13-row quantum market map covering quantum-sdk, cloud-platform, hardware-platform, quantum-ai, quantum-compiler, neutral-atom, and annealing categories. | MATCH | fenced | 1 | market-map-review | deviation 0 within tolerance 0.5 |
| Every pass 0012 market-map row includes an HTTPS source URL, proof receipt gap, Telos wedge hypothesis, gap status, and confidence label. | MATCH | fenced | 1 | market-row-field-review | deviation 0 within tolerance 0.5 |
| Pass 0012 created a ProofPacket/v1 no-cloning packet with at least four claims and no PROMOTED_LAW state. | MATCH | fenced | 1 | proof-packet-review | deviation 0 within tolerance 0.5 |
| The pass 0012 validators report MATCH: the quantum validator reports three matches and zero drift, and the proof-packet validator reports one match and zero drift. | MATCH | fenced | 1 | validator-run-review | deviation 0 within tolerance 0.5 |
| Pass 0012 attempted Forum steelman twice but preserved the executor JSON error as UNVERIFIABLE rather than treating it as a successful Forum adversarial result. | MATCH | fenced | 1 | forum-receipt-review | deviation 0 within tolerance 0.5 |
| Pass 0012 promotes zero new theorems, quantum hardware results, quantum advantage claims, cryptographic breaks, natural laws, or scientific discoveries. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0012 created a NoCloningProbe/v1 artifact reporting PROBE_MATCH: CNOT clones \|0> and \|1> basis fixtures with fidelity 1.0 and fails the \|+> superposition clone fixture with fidelity 0.5. | probe-review | schemas/no-cloning-probe-pass-0012.json schema=NoCloningProbe/v1; status=PROBE_MATCH; basis check \|0>\|0> fidelity=1.0 status=PASS; basis check \|1>\|0> fidelity=1.0 status=PASS; superposition_negative_fixture status=FAILS_SUPERPOSITION; superposition fidelity_to_desired_clone=0.5; probe seal=c8c9baf1cebd832cc4f49caca611fc3c578ab8511c2b01b51ba9d6bc1a2b270a |
| Pass 0012 records the inner-product no-cloning impossibility for \|0> and \|+>, including overlap 0.707106781186547, overlap_squared 0.5, and positive defect 0.207106781186548. | inner-product-review | inner_product_impossibility states include \|0> and \|+>; overlap=0.707106781186547; overlap_squared=0.5; defect=0.207106781186548; status=IMPOSSIBLE_FOR_NONORTHOGONAL_DISTINCT_STATES |
| Pass 0012 created a 13-row quantum market map covering quantum-sdk, cloud-platform, hardware-platform, quantum-ai, quantum-compiler, neutral-atom, and annealing categories. | market-map-review | schemas/quantum-computing-market-map-pass-0012.json rows=13; category quantum-sdk present; category cloud-platform present; category hardware-platform present; category quantum-ai present; category quantum-compiler present; category neutral-atom present; category annealing present |
| Every pass 0012 market-map row includes an HTTPS source URL, proof receipt gap, Telos wedge hypothesis, gap status, and confidence label. | market-row-field-review | validator required_fields includes source_url; validator required_fields includes proof_receipt_gap; validator required_fields includes telos_wedge_hypothesis; validator required_fields includes gap_status; validator required_fields includes confidence; validator rejects non-HTTPS source URLs; validator restricts gap_status to verified, inferred, or unverified |
| Pass 0012 created a ProofPacket/v1 no-cloning packet with at least four claims and no PROMOTED_LAW state. | proof-packet-review | schemas/no-cloning-proof-packet-pass-0012.json schema=ProofPacket/v1; packet_id=proof-packet-pass-0012-no-cloning; claim_count=4; failure_labels include NOT_A_NEW_THEOREM; failure_labels include NO_QUANTUM_HARDWARE_RUN; validator rejects PROMOTED_LAW in pass 0012 packet |
| The pass 0012 validators report MATCH: the quantum validator reports three matches and zero drift, and the proof-packet validator reports one match and zero drift. | validator-run-review | schemas/pass-0012-quantum-validator-result.json status=MATCH; schemas/pass-0012-quantum-validator-result.json match=3; schemas/pass-0012-quantum-validator-result.json drift=0; schemas/proof-packet-validator-pass-0012.json status=MATCH; schemas/proof-packet-validator-pass-0012.json match=1; schemas/proof-packet-validator-pass-0012.json drift=0 |
| Pass 0012 attempted Forum steelman twice but preserved the executor JSON error as UNVERIFIABLE rather than treating it as a successful Forum adversarial result. | forum-receipt-review | adversarial/pass-0012-forum-steelman.md status=UNVERIFIABLE; adversarial/pass-0012-forum-steelman.md records configured executor did not return valid JSON; schemas/no-cloning-proof-packet-pass-0012.json ForumSteelman status=UNVERIFIABLE; local steelman is labeled local rather than Forum-verified |
| Pass 0012 promotes zero new theorems, quantum hardware results, quantum advantage claims, cryptographic breaks, natural laws, or scientific discoveries. | artifact-review | packets/022-quantum-no-cloning-proof-packet.md Non-Promotion Statement promotes no new theorem or hardware result; schemas/no-cloning-proof-packet-pass-0012.json failure label NOT_A_NEW_THEOREM; schemas/no-cloning-proof-packet-pass-0012.json failure label NO_QUANTUM_HARDWARE_RUN; no pass 0012 claim uses PROMOTED_LAW |
