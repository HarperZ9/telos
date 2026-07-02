# Pass 0108 Steelman: Detailed-Balance Markov Receipt

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a three-state chain is not a real probabilistic
program. Correct. It is a kernel-level proof primitive, not a full sampler.

The second objection is that detailed balance is not necessary for stationarity.
Correct. The receipt includes a stationary cyclic fixture that violates detailed
balance so the packet cannot overclaim necessity.

The third objection is that market gaps are inferred. Correct. The listed tools
are source anchors for positioning, not proof that buyers will adopt the wedge.

Non-promotion statement: This pass proves a bounded finite Markov-chain identity and market proof-packet gap. It does not prove sampler correctness for Stan, NumPyro, TFP, PyMC, or any production probabilistic runtime.
