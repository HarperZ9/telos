# Packet 118: Detailed-Balance Markov Receipt

Date: 2026-07-01

Status: `DETAILED_BALANCE_MARKOV_RECEIPT_MATCH`

Purpose: prove a bounded finite-state Markov identity for stochastic physics,
MCMC, AI uncertainty, and probabilistic runtime proof packets.

```text
source_reaction_corpus_pass = 0107
pi = ['1/2', '1/3', '1/6']
max_detailed_balance_residual = 0
stationary_residual = ['0', '0', '0']
simulation_steps = 200
simulation_l1_distance_to_pi = 9.159339953157541e-16
row_stochastic_negative_residual = ['-2/15', '11/60', '-1/20']
stationary_not_reversible_residual = 1/3
market_tool_count = 8
compose_status = MATCH
test_status = MATCH
```

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

## Product Meaning

The proof-packet wedge is not "another sampler." It is a portable receipt for
kernel-level balance equations, stationary residuals, convergence probes,
diagnostic boundaries, and negative fixtures.

## Boundary

This pass proves a bounded finite Markov-chain identity and market proof-packet gap. It does not prove sampler correctness for Stan, NumPyro, TFP, PyMC, or any production probabilistic runtime.
