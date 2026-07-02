# Quantum Experiment Receipts

Date: 2026-07-01

Status: `PROBE_MATCH`.

This pass converts the pass 0012 no-cloning proof packet into a narrower engineering receipt: `QuantumExperimentReceipt/v1`. The receipt exists to prevent a common scientific-computing failure mode: treating an exact simulator result, a noisy simulator result, a hardware mock, and a cloud-hardware run as if they are interchangeable evidence.

The immediate target is not a new theorem, a quantum hardware result, or a quantum-advantage claim. The target is a reliable boundary object for future quantum work inside Telos, BuildLang/buildc, build-universe, and external SDK adapters.

## Why This Matters

Quantum research systems already have strong fragments:

- SDKs can define and run circuits.
- Simulators can produce exact statevectors, samples, and noise-injected outputs.
- Cloud providers can run jobs and return task metadata.
- Resource estimators can project qubits, gate counts, and fault-tolerance assumptions.
- Formal proof tools can verify algebraic or theorem-level claims.

The missing product object is the joined receipt: the circuit, backend branch, execution assumptions, resource estimate, result, verifier status, and non-promotion policy in one portable packet.

That joined receipt is the wedge. It is what lets Telos say:

- this is only a simulator result;
- this is a noisy simulator result with specified assumptions;
- this is only a resource estimate;
- this is a real cloud-hardware result;
- this supports a bounded probe, not a theorem;
- this supports a theorem only because a separate proof receipt exists.

## Fixture

The fixture uses the pass 0012 no-cloning CNOT witness:

```text
source: |+>|0>
operations: H(q0), CNOT(q0,q1)
desired clone: |+>|+>
```

The exact simulator branch returns:

```text
statevector = (|00> + |11>) / sqrt(2)
histogram = {00: 0.5, 11: 0.5}
fidelity_to_desired_clone = 0.5
status = FAILS_CLONING_AS_EXPECTED
```

The noisy simulator branch adds a phase-flip component on the target qubit with probability `0.1`. It returns the same computational-basis histogram:

```text
histogram_l1_drift_from_exact = 0.0
```

But the phase-sensitive fidelity drops:

```text
exact fidelity = 0.5
noisy fidelity = 0.45
```

That is the point of the pass. A histogram-only proof packet would miss the distinction. A quantum receipt must preserve the branch, state-sensitive or phase-sensitive metric, noise model, and hardware-promotion status.

## Non-Promotion Policy

The pass 0013 schema forbids these promotions:

| From | To | Status |
| --- | --- | --- |
| Exact simulator | Hardware result | Forbidden |
| Noisy simulator | Hardware result | Forbidden |
| Resource estimate | Executed backend result | Forbidden |
| Hardware mock | Cloud hardware | Forbidden |
| Experiment receipt | Theorem proof | Forbidden unless linked to a proof packet |
| Histogram match | State/fidelity match | Forbidden without phase-sensitive evidence |

## Market Implication

The same receipt layer can become a megatool bridge:

| Internal Layer | Quantum Product Function |
| --- | --- |
| Gather | Collect SDK docs, cloud task docs, calibration docs, resource estimator docs, and papers. |
| Index | Map experiment receipts, circuit files, source papers, code, and prior proof packets. |
| Forum | Run adversarial objections: branch confusion, fake hardware claims, insufficient baseline, missing calibration, and invalid theorem promotion. |
| Crucible | Check falsifiable thesis claims against measurements and receipts. |
| Telos | Bind source, action, execution, verifier, and non-promotion records. |
| BuildLang/buildc | Compile numerical kernels, circuit preprocessors, postprocessing metrics, and receipt-generating runtime hooks. |
| build-universe | Package reproducible domain stacks for quantum, physics, biology, finance, rendering, and security. |
| Model foundry | Generate hypotheses and code, but attach every action to receipts rather than treating text as proof. |

This is not a monolithic app. It is a family of proof-centered products with a common evidence object.

## External Source Anchors

| Source | Relevance |
| --- | --- |
| Qiskit Aer noise models | Establishes that noise models and simulator assumptions are first-class SDK concerns. |
| IBM Quantum noise-model guide | Supports backend-derived and explicit noise-model receipt fields. |
| Cirq noisy simulation | Supports noisy simulator branch semantics and channel-level modeling. |
| Azure Quantum Resource Estimator | Supports resource-estimate receipt fields and assumption capture. |
| Amazon Braket task monitoring | Supports cloud task status and result receipt boundaries. |
| IonQ simulation with noise models | Supports cloud-style simulator noise-model evidence boundaries. |

## Acceptance Result

The validator for this pass must prove:

1. The schema defines required receipt fields.
2. The schema includes exact simulator, noisy simulator, hardware mock, and cloud hardware branch values.
3. Branch promotion is explicitly forbidden.
4. The receipt set includes exact and noisy simulator branches.
5. The noisy simulator branch has zero histogram drift but lower fidelity than the exact simulator branch.
6. Neither branch permits a hardware claim.
7. The fixture is sealed.

## Natural-Law Promotion

Current promoted natural laws: none.

