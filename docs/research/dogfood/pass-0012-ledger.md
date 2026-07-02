# Dogfood Pass 0012 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `123dcf1159cd431d`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `123dcf1159cd431d5981bc66a02bc6f317bfc6774813c262de9de8f5e1093407`;
- verdict seal: `935490c7c8b81e0c6c242e5962597807ac7a0c2d17cbeda1636c02e9f9427ff8`;
- measurement seal: `c325206e5ee5cf138606cddb25cc80b0ae33b4110dc1e0f52a85e247bfc98514`;
- assessment seal: `70fff2aa721b83ed088980398822071e62e1c5aebf0aa7afbd6d3fbadf4912f9`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: quantum proof packets. This pass uses the no-cloning theorem as a compact proof-packet systems test, then maps the adjacent quantum SDK, cloud, hardware, compiler, quantum AI, neutral-atom, and annealing market.

No new theorem, quantum hardware result, quantum advantage claim, cryptographic break, natural law, biological result, material result, medical result, finance result, or safety result is promoted in this pass.

## Theorem Finding

The algebraic identity is:

```text
If U(|psi>|b>) = |psi>|psi> and U(|phi>|b>) = |phi>|phi>,
then <psi|phi> = <psi|phi>^2.
```

For nonorthogonal distinct states such as `|0>` and `|+>`, the overlap is `1/sqrt(2)`, while the squared overlap is `1/2`. That mismatch blocks a universal unitary cloner.

## Probe Finding

The bounded probe uses a CNOT basis fixture:

| Input | Desired | Fidelity | Status |
| --- | --- | ---: | --- |
| `|0>|0>` | `|0>|0>` | `1.0` | `PASS` |
| `|1>|0>` | `|1>|1>` | `1.0` | `PASS` |
| `|+>|0>` | `|+>|+>` | `0.5` | `FAILS_SUPERPOSITION` |

The probe seal is `c8c9baf1cebd832cc4f49caca611fc3c578ab8511c2b01b51ba9d6bc1a2b270a`.

## Source Anchors

| Source | Evidence Used |
| --- | --- |
| IBM Qiskit | SDK for quantum workflows, circuits, operators, primitives, and orchestration. |
| Microsoft Azure Quantum | Cloud quantum platform combining HPC, AI, and quantum technologies. |
| Amazon Braket | Managed quantum service with simulators and multiple hardware modalities. |
| Google Cirq | Python library for circuits, optimization, simulators, and NISQ workflows. |
| Google Quantum AI | Research and hardware program focused on error-corrected quantum computation. |
| Quantinuum | Trapped-ion hardware and full-stack quantum software positioning. |
| IonQ | Cloud access to trapped-ion quantum computers across SDK/cloud examples. |
| Rigetti | Superconducting QPU and quantum cloud services positioning. |
| PennyLane / Xanadu | Quantum computing, quantum machine learning, and quantum chemistry software platform. |
| D-Wave Ocean | Python tools for quantum annealing and hybrid solver workflows. |
| Classiq | Quantum algorithm design, synthesis, optimization, and hardware-aware circuit platform. |
| QuEra | Neutral-atom quantum computer provider positioning. |
| Pasqal | Neutral-atom processors, HPC/cloud integration, optimization, simulation, and AI-adjacent workloads. |

## Forum Steelman Receipt

Forum status and chain verification were reachable, but both `forum.submit` attempts returned an executor JSON parsing error. This pass records Forum steelman status as `UNVERIFIABLE` and includes a local steelman in `adversarial/pass-0012-forum-steelman.md`.

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_no_cloning_theorem.py` | Deterministic no-cloning theorem simulator witness. |
| `tools/validate_pass_0012_quantum.py` | Validator for pass 0012 probe, market map, and proof packet. |
| `packets/022-quantum-no-cloning-proof-packet.md` | Human-readable no-cloning proof and market thesis. |
| `adversarial/pass-0012-forum-steelman.md` | Forum failure receipt plus local adversarial steelman. |
| `schemas/no-cloning-probe-pass-0012.json` | Bounded simulator receipt with basis pass and superposition failure. |
| `schemas/quantum-computing-market-map-pass-0012.json` | 13-row quantum market map. |
| `schemas/no-cloning-proof-packet-pass-0012.json` | `ProofPacket/v1` for the no-cloning theorem proof kit. |
| `schemas/pass-0012-quantum-validator-result.json` | Validator receipt for pass 0012. |
| `schemas/proof-packet-validator-pass-0012.json` | Generic proof-packet validator receipt for pass 0012. |
| `crucible/pass-0012-thesis.json` | Falsifiable claims for the twelfth pass. |
| `crucible/pass-0012-measurements.json` | Measurements/evidence for the twelfth pass. |
| `crucible/pass-0012-report.md` | Crucible assessment report. |
| `crucible/pass-0012-run.json` | Crucible run record. |

## Primary Next Push

`QuantumExperimentReceipt/v1`.

Add a receipt schema that separates:

- theorem proof status;
- circuit source;
- SDK and transpiler version;
- backend branch: exact simulator, noisy simulator, hardware mock, cloud hardware;
- seed, noise model, calibration, and queue metadata;
- resource estimates;
- result histogram;
- verifier verdicts.

## Natural-Law Promotion

Current promoted natural laws: none.

## Next-Pass Queue

1. Implement `QuantumExperimentReceipt/v1` from the no-cloning circuit fixture.
2. Add a noisy simulator negative fixture that cannot be confused with an exact simulator proof.
3. Add a resource-estimation receipt with qubit count, gate count, depth, and backend assumptions.
4. Add a Qiskit- or Cirq-compatible circuit adapter fixture.
5. Repair Forum executor JSON output so adversarial steelman can become a real Forum receipt again.
