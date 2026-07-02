# Pass 0087 Ledger: Quantum Simulator Branch Adapter

Date: 2026-07-01

Status: `MATCH_QUANTUM_SIMULATOR_BRANCH_ADAPTER`

## Purpose

Add a seeded simulator branch to the pass 0086 exact quantum-optimization
workflow receipt. This pass records a hand-rolled simulated-annealing adapter
contract, seed records, run digest, objective distribution, exact-baseline
comparison, source anchors, negative fixtures, and explicit non-promotion
boundaries.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_quantum_simulator_branch_adapter.py` | Seeded simulated-annealing branch composer. |
| `tools/test_quantum_simulator_branch_adapter.py` | Focused adapter, replay-gate, and boundary test. |
| `tools/probe_quantum_simulator_branch_adapter.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0087_quantum_simulator_branch_adapter.py` | Independent validator for seal, run digest, exact comparison, source anchors, and boundaries. |
| `schemas/quantum-simulator-branch-adapter-pass-0087.json` | `QuantumSimulatorBranchAdapterReceipt/v1` artifact. |
| `schemas/pass-0087-quantum-simulator-branch-adapter-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0087.json` | Compact simulator, Forum, Index, Telos, compose, and test receipts. |
| `packets/097-quantum-simulator-branch-adapter.md` | Human-readable simulator branch packet. |
| `briefs/097-quantum-simulator-branch-adapter-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0087-quantum-simulator-branch-adapter-steelman.md` | Local steelman of the simulator-branch limits. |
| `crucible/pass-0087-thesis.json` | Falsifiable claims. |
| `crucible/pass-0087-measurements.json` | Measurements/evidence. |
| `crucible/pass-0087-report.md` | Crucible report. |
| `crucible/pass-0087-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Exact baseline pass | 0086 |
| Run count | 32 |
| Seed range | 8700..8731 |
| Beta schedule | `[0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4]` |
| Sweeps per beta | 12 |
| Optimum hit count | 30 |
| Best-run constraint violation rate | 0.0 |
| Exact best bits | `[0,0,1,1,1,1]` |
| Simulator best bits | `[0,0,1,1,1,1]` |
| Exact best energy | -36 |
| Simulator best energy | -36 |
| Replay gate | MATCH |
| Run digest | `4df12bbe1c5b3ee42d05f5ccce708bd5880f4d1d4c1c5a90f3f9528656d912b7` |
| Quantum hardware claim | false |
| Quantum advantage claim | false |
| Promoted natural laws | 0 |

## Source Anchors

| Source | URL | Status |
| --- | --- | --- |
| D-Wave samplers simulated annealing | `https://docs.dwavequantum.com/en/latest/ocean/api_ref_samplers/index.html` | `SOURCE_LEAD` |
| D-Wave dimod BQM/QUBO models | `https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/models.html` | `SOURCE_LEAD` |

## Product Finding

The useful product layer is the adapter contract, not the toy annealer itself.
The branch records solver parameters, seed records, run outputs, distribution
summary, source anchors, and a replay gate against exact enumeration. That is
the invariant a future Ocean, D-Wave, or other optimization adapter must
preserve before any hardware, speed, quality, or market claim is allowed.

The result also creates a measurable next step: increase problem size while
keeping exact enumeration possible, then compare exact, simulated annealing,
and greedy baselines through the same receipt fields.

## Tool Findings

- Forum route receipt: `MATCH`, `needs_escalation=true`, top candidates
  `model-foundry`, `project-telos`.
- Index context envelope: `MATCH`, schema
  `project-telos.context-envelope/v1`, graph pack SHA256
  `8ee383e19ae9a6141bee70de733fb6aa09201ff9d284ce6778ce58b06e6b68b2`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `b65a7a19c5329e645f0535890c3bdc5dad29ba29fdf1a9610cff7accb48dbd7b`,
  digest seal `0522f9c2cebb12c54f2080169fe339fe94b17765908db4e5328c2a8337621a99`.
- Gather brief receipt: SHA256
  `4914242aebded2d49da76f8161afa6a75c2d8cdc3d130bccadce06a1c48525ce`,
  digest seal `d8758e18f2ed8c52d98bfade841f3bf1c0da9ade2d34609f45a8288bdd1ae4bd`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `fdf9df53059dfe5a`.
- Crucible assessment seal:
  `279ae9e66c116c8bc481076cce03740612afbf08b11918289388d6edfb419369`.
- Crucible registry stats after this pass: 75 theses, 614 claims, 614 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not claim production-grade D-Wave/Ocean integration, quantum
hardware execution, quantum advantage, benchmark superiority, new physics, or a
natural law. It verifies a simulator branch contract against a toy exact
baseline.

## Verification

```powershell
python -m py_compile docs\research\dogfood\tools\compose_quantum_simulator_branch_adapter.py docs\research\dogfood\tools\test_quantum_simulator_branch_adapter.py docs\research\dogfood\tools\validate_pass_0087_quantum_simulator_branch_adapter.py docs\research\dogfood\tools\probe_quantum_simulator_branch_adapter.py
python docs\research\dogfood\tools\probe_quantum_simulator_branch_adapter.py
python docs\research\dogfood\tools\test_quantum_simulator_branch_adapter.py
python docs\research\dogfood\tools\validate_pass_0087_quantum_simulator_branch_adapter.py
crucible run docs\research\dogfood\crucible\pass-0087-thesis.json --measurements docs\research\dogfood\crucible\pass-0087-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0087-report.md --out docs\research\dogfood\crucible\pass-0087-run.json --json
gather docs docs\research\dogfood\packets\097-quantum-simulator-branch-adapter.md --json
gather docs docs\research\dogfood\briefs\097-quantum-simulator-branch-adapter-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Create a larger exact-enumerable optimization benchmark, then compare exact,
simulated annealing, greedy, and random-search baselines through a shared
`OptimizationBranchComparisonReceipt/v1`.
