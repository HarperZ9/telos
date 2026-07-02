# Pass 0108 Ledger: Detailed-Balance Markov Receipt

Date: 2026-07-01

Status: `DETAILED_BALANCE_MARKOV_RECEIPT_MATCH`

## Purpose

Move the dogfood loop from reaction-network invariants into stochastic dynamics:
finite Markov kernels, detailed balance, MCMC, probabilistic programming,
physics-style reversible dynamics, and AI uncertainty tooling.

This pass proves and probes one bounded identity: detailed balance is sufficient
for stationarity in a finite Markov kernel. It also records two adversarial
fixtures so the packet does not overclaim.

The result is a scoped `LAW_CANDIDATE`, not a promoted natural law.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_detailed_balance_markov_receipt.py` | Builds exact rational kernels, theorem residuals, negative fixtures, market surface, and Forum/Index/Telos receipts. |
| `tools/test_detailed_balance_markov_receipt.py` | Focused TDD test for exact residuals, convergence probe, boundary fixtures, and market fields. |
| `tools/probe_detailed_balance_markov_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0108_detailed_balance_markov.py` | Independent validator for seal, theorem fields, fixtures, market surface, and boundaries. |
| `schemas/detailed-balance-markov-receipt-pass-0108.json` | `DetailedBalanceMarkovReceipt/v1` artifact. |
| `schemas/pass-0108-detailed-balance-markov-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0108.json` | Compact Markov, market, Forum, Index, Telos, compose, and test receipts. |
| `packets/118-detailed-balance-markov-receipt.md` | Human-readable detailed-balance packet. |
| `briefs/118-detailed-balance-markov-brief.md` | Buyer-facing stochastic proof brief. |
| `adversarial/pass-0108-detailed-balance-markov-steelman.md` | Local pass 0108 steelman. |
| `crucible/pass-0108-thesis.json` | Falsifiable claims. |
| `crucible/pass-0108-measurements.json` | Measurements/evidence. |
| `crucible/pass-0108-report.md` | Crucible report. |
| `crucible/pass-0108-run.json` | Crucible run record. |

## Theorem Measurements

| Check | Result |
| --- | --- |
| Source reaction corpus pass | 0107 |
| Identity | detailed balance implies stationarity |
| Symbolic step | `sum_i pi_i P_ij = sum_i pi_j P_ji = pi_j` |
| Stationary distribution | `[1/2, 1/3, 1/6]` |
| Transition matrix row sums | `[1, 1, 1]` |
| Max detailed-balance residual | `0` |
| Stationary residual | `[0, 0, 0]` |
| Simulation steps | 200 |
| L1 distance to `pi` | `9.159339953157541e-16` |
| Artifact file SHA256 | `2459140679a2d6d05718cdfa77fe7995cee6c4fc0d1ace65a5938dd6f6c588df` |
| Artifact seal | `a1a1694780c096fce96074a5e48ca94fdde9f31bb085ffd6c56b8ac83260f8fd` |

## Negative And Boundary Fixtures

| Fixture | Purpose | Result |
| --- | --- | --- |
| `row_stochastic_not_stationary` | Reject the idea that row sums alone prove target stationarity. | Row sums `[1,1,1]`; stationary residual `[-2/15, 11/60, -1/20]`; status `DRIFT_EXPECTED`. |
| `stationary_not_reversible` | Prevent overclaiming that detailed balance is necessary. | Uniform `pi` is stationary with residual `[0,0,0]`, but detailed-balance residual is `1/3`; status `BOUNDARY_EXPECTED`. |

## Market Surface

| Tool | Category | Gap Status |
| --- | --- | --- |
| Stan | Bayesian modeling and MCMC | inferred |
| NumPyro | JAX-backed probabilistic programming and MCMC | inferred |
| TensorFlow Probability | probabilistic reasoning and MCMC in TensorFlow | inferred |
| PyMC | Bayesian modeling and MCMC ecosystem | inferred |
| BlackJAX | JAX sampling algorithms | inferred |
| Turing.jl | Julia probabilistic programming | inferred |
| ArviZ | Bayesian diagnostics and visualization | inferred |
| UQpy | uncertainty quantification with MCMC sampling | inferred |

Gap hypothesis: probabilistic runtimes expose samplers and diagnostics, but a
portable proof packet can bind transition kernels, detailed-balance residuals,
stationary residuals, convergence probes, and negative fixtures.

## Source Anchors

| Source | URL | Evidence Role |
| --- | --- | --- |
| Stan Reference Manual: MCMC Sampling | `https://mc-stan.org/docs/reference-manual/mcmc.html` | Official MCMC tooling source anchor. |
| NumPyro Markov Chain Monte Carlo | `https://num.pyro.ai/en/latest/mcmc.html` | Official MCMC tooling source anchor. |
| TensorFlow Probability API | `https://www.tensorflow.org/probability/api_docs/python/tfp` | Official probabilistic tooling source anchor. |
| TensorFlow Probability UncalibratedRandomWalk | `https://www.tensorflow.org/probability/api_docs/python/tfp/mcmc/UncalibratedRandomWalk` | Official negative-boundary source anchor for uncalibrated kernels. |
| Detailed Balance and Markov Chain Monte Carlo | `https://personal.math.ubc.ca/~holmescerfon/teaching/asa22/handout-Lecture3_2022.pdf` | Detailed-balance source anchor. |
| Markov Chains and Markov Chain Monte Carlo | `https://www.stats.ox.ac.uk/~teh/teaching/dtc2014/Markov4.pdf` | Stationarity and detailed-balance source anchor. |
| tfp.mcmc whitepaper | `https://arxiv.org/pdf/2002.01184` | MCMC runtime whitepaper source anchor. |

## Product Finding

The proof-packet product should not try to out-sample Stan, NumPyro, TFP, PyMC,
or Turing. The wedge is a proof layer around samplers: transition-kernel intake,
kernel residual checks, stationary residual checks, convergence probes,
diagnostic receipts, and explicit boundaries for uncalibrated kernels.

This field is a good next market/research lane because it connects physics,
statistics, AI uncertainty, quant modeling, and probabilistic programming with a
small proof object that can be checked exactly before scaling to harder kernels.

## Tool Findings

- TDD red observed before the composer existed: `FileNotFoundError`.
- Forum route receipt: `MATCH`.
- Index context envelope: `MATCH`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `d9c3a847c6abdb5f14c38b90e391475be432ee8b372357dedf41f8d732f3341c`,
  digest seal `e966667260c016dac562f6ef155f1de49c29b19cb2d1c33a9d780a302893aa4b`.
- Gather brief receipt: SHA256
  `db9c8e3ad1f06a7d660181deda7dab8385a6be03b069dd1d787905ecc23e3ddc`,
  digest seal `e16b4e9907b817f39d5b8aa736ff10e2443a9eb71fba534025b1d234932e761e`.
- Crucible result: 11 claims, 11 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `87f8c91475ce06ad`.
- Crucible assessment seal:
  `5e6226eda2d6b01b8c6064f059dfdd47c05964045a2bdc8f6554ae5e5e51f9fa`.
- Crucible registry stats after this pass: 97 theses, 818 claims, 818 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not prove sampler correctness for Stan, NumPyro, TFP, PyMC,
BlackJAX, Turing, ArviZ, UQpy, or any production runtime. It proves one bounded
finite Markov-chain identity and records a market gap hypothesis.

## Verification

```powershell
python docs\research\dogfood\tools\test_detailed_balance_markov_receipt.py
python -m py_compile docs\research\dogfood\tools\compose_detailed_balance_markov_receipt.py docs\research\dogfood\tools\test_detailed_balance_markov_receipt.py docs\research\dogfood\tools\validate_pass_0108_detailed_balance_markov.py docs\research\dogfood\tools\probe_detailed_balance_markov_receipt.py
python docs\research\dogfood\tools\probe_detailed_balance_markov_receipt.py
python docs\research\dogfood\tools\validate_pass_0108_detailed_balance_markov.py
crucible run docs\research\dogfood\crucible\pass-0108-thesis.json --measurements docs\research\dogfood\crucible\pass-0108-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0108-report.md --out docs\research\dogfood\crucible\pass-0108-run.json --json
gather docs docs\research\dogfood\packets\118-detailed-balance-markov-receipt.md --json
gather docs docs\research\dogfood\briefs\118-detailed-balance-markov-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Build a stochastic-kernel corpus harness that includes reversible, stationary
non-reversible, non-stationary, and uncalibrated-kernel fixtures, then specify
the adapter fields needed for Stan/NumPyro/TFP-style sampler receipts.
