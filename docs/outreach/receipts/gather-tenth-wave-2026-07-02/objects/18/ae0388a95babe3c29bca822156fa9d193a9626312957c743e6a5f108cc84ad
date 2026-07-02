# Pass 0013 Branch-Separation Steelman

Date: 2026-07-01

Status: `UNVERIFIABLE` for Forum submit; `MATCH` for local adversarial analysis.

## Forum Tool Receipt

Forum status and chain verification remain reachable:

```json
{
  "status": {
    "entries": 3,
    "checkpoint": "a146467e8ef2c07fac3932cf8ce3900a532b8829795d6bf377f012f476b62668"
  },
  "verify": {
    "chain": true,
    "deep": true
  }
}
```

Both Forum submit paths failed with executor JSON parsing errors:

```json
{
  "error": "the configured executor did not return valid JSON; point the daemon at a real model executor (could not parse JSON from output: Extra data: line 2 column 1 (char 98))"
}
```

Therefore this pass does not claim a witnessed Forum adversarial answer. It records the failure as a tool-surface gap and uses the local steelman below as an unsealed adversarial checklist.

## Steelman Objections

### Objection 1: Histogram Equality Can Hide Phase Errors

The pass 0013 fixture intentionally creates this failure mode. The exact branch and noisy phase-flip branch both report:

```text
histogram = {00: 0.5, 11: 0.5}
histogram_l1_drift_from_exact = 0.0
```

But the phase-sensitive clone fidelity changes:

```text
exact fidelity = 0.5
noisy fidelity = 0.45
```

If the product only captures histograms, the receipt can falsely imply equivalence. The hardening requirement is that claims must declare which result metrics are probative: histogram, statevector, density matrix, process fidelity, observable expectation, or task-specific scalar.

### Objection 2: Simulator Branches Can Be Laundered Into Hardware Claims

Quantum demos often sound more impressive than their backend. A receipt that records a circuit and result but omits backend branch allows marketing or downstream agents to imply a hardware run.

Hardening requirement:

- every receipt must include `branch`;
- every receipt must include `hardware_claim_allowed`;
- hardware claims require `branch = CLOUD_HARDWARE` and `hardware_claim_allowed = true`;
- simulator and noisy-simulator results must be rejected when cited as hardware evidence.

### Objection 3: Resource Estimates Are Planning Artifacts, Not Results

Resource estimators can be decision-grade, but they do not execute the target computation. A future Telos packet can include resource estimates, but must keep them separate from execution receipts.

Hardening requirement:

- resource estimate fields must record assumptions;
- resource estimates cannot satisfy execution-result fields;
- quantum-advantage claims require a separate benchmark receipt binding quantum backend, classical baseline, calibration, cost, and verifier verdict.

### Objection 4: Exact Simulation Is Not a Theorem

An exact simulator can witness a bounded case. It does not prove an unbounded theorem unless joined to formal reasoning.

Hardening requirement:

- experiment receipts must reference theorem claims but not promote them;
- theorem promotion requires a proof packet, formal verifier receipt, or independent proof review.

### Objection 5: Cloud-Hardware Receipts Need Operational Metadata

A cloud-hardware receipt needs more than a backend name. It should bind task id, provider, device, queue timestamp, calibration snapshot or calibration reference, shot count, result payload hash, SDK version, transpilation or compilation path, and cost/runtime metadata where available.

Hardening requirement:

- `CLOUD_HARDWARE` is invalid unless operational metadata fields are present;
- absent calibration or task metadata should produce `UNVERIFIABLE`, not `MATCH`.

## Required Next Hardening

1. Add negative fixtures that attempt to promote exact simulator evidence into `CLOUD_HARDWARE` and ensure validators reject them.
2. Add a mock cloud-hardware receipt shape with task metadata, but keep it clearly labeled `HARDWARE_MOCK`.
3. Add a Qiskit or Cirq circuit adapter output so the receipt can ingest external circuit formats.
4. Repair Forum executor JSON output so the adversarial review can be witnessed by Forum instead of recorded locally.
5. Add metric-specific claim binding: each claim must name which metrics are sufficient and which are only auxiliary.

## Verdict

The current `QuantumExperimentReceipt/v1` shape addresses the most dangerous branch-confusion risk, but it is not complete for real cloud-hardware claims. It should be treated as a simulator/noisy-simulator boundary pass, not a production cloud-quantum receipt.

