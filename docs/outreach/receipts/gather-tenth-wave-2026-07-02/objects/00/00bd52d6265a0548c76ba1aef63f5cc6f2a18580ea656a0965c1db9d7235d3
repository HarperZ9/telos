# Packet 003: Physics and PDE Law Candidates

Status: `IDENTITY` plus `PROBE_MATCH`

## Question

Can Telos use computational tooling to discover, test, and package law candidates without overclaiming new physics?

## Source Anchors

- Physics-informed machine learning survey: https://link.springer.com/article/10.1007/s44379-025-00016-0
- Nature physics-informed ML collection: https://www.nature.com/collections/jaihfcabgi
- Aurora Earth-system model paper: https://www.nature.com/articles/s41586-025-09005-y

## Identity Seed: Heat Equation Energy Decay

For the heat equation

```text
u_t = kappa * Delta u
```

on a periodic domain, the energy

```text
E(t) = 1/2 * integral u(x,t)^2 dx
```

satisfies

```text
dE/dt = -kappa * integral |grad u|^2 dx <= 0
```

under the usual smoothness and boundary assumptions.

This is not new. It is a known mathematical identity suitable for a Telos proof-packet fixture.

## Numeric Probe

Pass 0001 finite-difference probe:

```json
{
  "n": 128,
  "steps": 200,
  "energy_initial": 0.265625,
  "energy_final": 0.20892202084351844,
  "energy_drop": 0.056702979156481564,
  "increases": 0
}
```

Verdict: `PROBE_MATCH` for the bounded numerical claim "this discretization did not increase energy over 200 steps."

## Adversarial Steelman

Objection: a stable finite-difference probe does not prove the continuous identity, and a continuous identity does not validate arbitrary learned PDE models.

Response: correct. Telos must separate:

- symbolic identity;
- discretization choice;
- numerical stability condition;
- observed run;
- physical interpretation;
- learned model generalization.

## Next Proof Attempt

Add wave-equation energy conservation and Burgers-equation shock/entropy packets. Each needs symbolic derivation, numerical probe, and failure fixture.

