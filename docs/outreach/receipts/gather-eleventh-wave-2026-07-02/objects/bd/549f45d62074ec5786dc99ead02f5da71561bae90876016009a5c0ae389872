# crucible report: Dogfood Pass 0009 Heat Equation Energy Proof Kit

## Summary

- thesis_id: `8b33cb27a05d4b34`
- thesis_seal: `8b33cb27a05d4b34b69d84d916a0aad608b7f8e8580eb004b148d20198b31226`
- assessment_seal: `d5e95a020347443c1e8daebf0cf037f29d86f385e92365ba7b6d893e5a955727`
- counts: MATCH 6 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0009 created a ProofPacket/v1 heat-equation energy packet with three claims: continuous L2 energy identity, stable finite-difference witness, and unstable negative fixture. | MATCH | fenced | 1 | json-structure-review | deviation 0 within tolerance 0.5 |
| The heat-equation probe reports PROBE_MATCH, with cfl=0.45 recording zero stable energy increases over 400 steps and cfl=0.55 detecting unstable energy growth. | MATCH | fenced | 1 | numerical-probe-review | deviation 0 within tolerance 0.5 |
| The pass 0009 scientific-compute market map includes at least ten rows and covers language-ecosystem, pde-framework, hpc-solver, physics-ai, and commercial-simulation categories. | MATCH | fenced | 1 | market-map-validator-review | deviation 0 within tolerance 0.5 |
| Every pass 0009 market-map row includes an HTTPS source URL and a BuildLang/buildc wedge hypothesis. | MATCH | fenced | 1 | market-row-field-review | deviation 0 within tolerance 0.5 |
| The pass 0009 validators report MATCH: the ProofPacket validator reports one match and zero drift; the scientific-compute validator reports two matches and zero drift. | MATCH | fenced | 1 | validator-run-review | deviation 0 within tolerance 0.5 |
| Pass 0009 promotes zero natural-law discoveries; the heat-equation energy identity is explicitly treated as a classical identity and proof-packet systems test. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0009 created a ProofPacket/v1 heat-equation energy packet with three claims: continuous L2 energy identity, stable finite-difference witness, and unstable negative fixture. | json-structure-review | schemas/heat-equation-proof-packet-pass-0009.json schema=ProofPacket/v1; packet_id=proof-packet-pass-0009-heat-equation-energy; claim_count=3; claim ids include claim-continuous-heat-energy-identity; claim ids include claim-bounded-stable-cfl-witness; claim ids include claim-negative-unstable-cfl-fixture |
| The heat-equation probe reports PROBE_MATCH, with cfl=0.45 recording zero stable energy increases over 400 steps and cfl=0.55 detecting unstable energy growth. | numerical-probe-review | schemas/heat-equation-energy-probe-pass-0009.json status=PROBE_MATCH; stable_probe cfl=0.45; stable_probe steps=400; stable_probe increase_count=0; stable_probe status=ENERGY_MONOTONE; unstable_probe cfl=0.55; unstable_probe status=ENERGY_INCREASE_DETECTED; unstable_probe first_increase step=201; probe seal=b3021c14b0e5dc8adeddadf0d22e2780dbf259c349caf5cbc2ba255b591fd7d5 |
| The pass 0009 scientific-compute market map includes at least ten rows and covers language-ecosystem, pde-framework, hpc-solver, physics-ai, and commercial-simulation categories. | market-map-validator-review | schemas/scientific-compute-market-map-pass-0009.json rows=10; category language-ecosystem present; category pde-framework present; category hpc-solver present; category physics-ai present; category commercial-simulation present; schemas/pass-0009-scientific-compute-validator-result.json categories list contains all required categories |
| Every pass 0009 market-map row includes an HTTPS source URL and a BuildLang/buildc wedge hypothesis. | market-row-field-review | validator required_fields includes source_url; validator required_fields includes buildlang_wedge_hypothesis; validator rejects non-HTTPS source URLs; rows include Julia, SciML, FEniCS, Firedrake, PETSc, OpenFOAM, NVIDIA PhysicsNeMo, COMSOL Multiphysics, Ansys Fluent, and SimScale |
| The pass 0009 validators report MATCH: the ProofPacket validator reports one match and zero drift; the scientific-compute validator reports two matches and zero drift. | validator-run-review | schemas/proof-packet-validator-pass-0009.json status=MATCH; schemas/proof-packet-validator-pass-0009.json match=1; schemas/proof-packet-validator-pass-0009.json drift=0; schemas/pass-0009-scientific-compute-validator-result.json status=MATCH; schemas/pass-0009-scientific-compute-validator-result.json match=2; schemas/pass-0009-scientific-compute-validator-result.json drift=0 |
| Pass 0009 promotes zero natural-law discoveries; the heat-equation energy identity is explicitly treated as a classical identity and proof-packet systems test. | artifact-review | schemas/heat-equation-proof-packet-pass-0009.json failure_labels include NOT_A_NEW_PHYSICAL_LAW; packets/019-heat-equation-energy-proof.md says this is not promoted as a new law; schemas/heat-equation-proof-packet-pass-0009.json claim-continuous-heat-energy-identity promotion_state=IDENTITY; pass 0009 artifacts use proof-packet systems-test language rather than promoted discovery language |
