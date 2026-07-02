# Packet 009: Quantum Computing Proof Packets

Status: `HYPOTHESIS` plus `PROBE_MATCH`

## Market Context

Quantum computing is moving from abstract roadmap marketing into concrete fault-tolerance milestones, but the market still has a verification problem: users need to understand what was simulated, what ran on hardware, what was error-mitigated, what was fault-tolerant, what was only a vendor roadmap, and what classical baseline was used.

Source anchor: IBM states a 2029 Starling target for a fault-tolerant system with 200 logical qubits and 100 million gates, and describes architectural criteria such as fault tolerance, addressability, universality, adaptivity, modularity, and efficiency.

Source URL: https://www.ibm.com/quantum/blog/large-scale-ftqc

## Telos Wedge

Hypothesis: quantum tooling needs a `QuantumClaimPacket` that binds:

- algorithm source and circuit representation;
- simulator, backend, hardware, or roadmap provenance;
- qubit count, logical/physical distinction, error model, and decoder assumptions;
- classical baseline;
- measurement distribution and seed provenance;
- domain validator verdict;
- claim label: `simulated`, `hardware-run`, `error-mitigated`, `fault-tolerant`, `roadmap`, or `unverified`.

This is not a replacement for Qiskit, Cirq, PennyLane, or quantum hardware APIs. It is a proof envelope around them.

## Local Probe

The pass ran a two-qubit Bell-state simulator:

- probabilities: `[0.4999999999999999, 0.0, 0.0, 0.4999999999999999]`;
- probability sum: `0.9999999999999998`;
- sum error: `2.220446049250313e-16`;
- non-Bell mass: `0.0`;
- `|00>` and `|11>` probabilities matched exactly within floating-point tolerance.

Classification: `PROBE_MATCH`. This proves only that the packet can carry a simple exact state-vector check.

## Internal Integration

| Internal tool | Role |
| --- | --- |
| Gather | Intake quantum papers, vendor roadmaps, benchmarks, and SDK docs. |
| Index | Bind circuit source, notebooks, generated artifacts, and local repo context. |
| Forum | Route between Telos, deep research, GPU compute, compiler systems, and quantum specialist validators. |
| Crucible | Judge bounded falsifiable claims like normalization, expected distribution, or benchmark reproduction. |
| Telos | Emit action receipts for simulator runs, hardware API calls, and approval boundaries. |
| BuildLang/buildc | Future target for typed circuit DSL experiments, kernel receipts, and deterministic numerical routines. |

## Gaps

| Gap | Label | Note |
| --- | --- | --- |
| No callable quantum SDK was verified in this pass. | `verified` | Only a small local Python state-vector probe was run. |
| No hardware quantum result was produced. | `verified` | The packet must not imply hardware execution. |
| Fault-tolerant claims require specialist review. | `verified` | Forum routed quantum into Telos, but domain validation remains separate. |
| BuildLang quantum DSL is only a future hypothesis in this packet. | `unverified` | No `.bld` quantum circuit module was inspected. |

## Demo Candidate

Create `quantum-receipt-demo`:

1. Load a small circuit from OpenQASM or a plain JSON circuit.
2. Run a deterministic simulator.
3. Emit `QuantumClaimPacket`.
4. Crucible checks normalization, expected distribution, and source digest.
5. Packet labels the result `simulated`, not hardware.

## Market Read

Buyers: research labs, quantum software teams, enterprise teams evaluating quantum vendors, auditors comparing roadmap claims against executable artifacts.

Near-term wedge: not "better quantum computing"; instead, quantum claim hygiene. This is useful before fault-tolerant hardware is broadly available.
