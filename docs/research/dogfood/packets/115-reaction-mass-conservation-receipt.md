# Packet 115: Reaction Mass-Conservation Receipt

Date: 2026-07-01

Status: `REACTION_MASS_CONSERVATION_RECEIPT_MATCH`

Purpose: prove and numerically probe the invariant for a closed first-order
reaction `A -> B` with mass-action rate `kA`.

```text
reaction = A -> B
derivation = d(A+B)/dt=dA/dt+dB/dt=-kA+kA
symbolic_derivative_total = 0
grid_points = 97
max_exact_invariant_drift = 0.0
max_euler_invariant_drift = 4.440892098500626e-16
negative_fixture_breaks_invariant = True
law_candidate = closed_first_order_reaction_total_mass_invariant
compose_status = MATCH
test_status = MATCH
```

## Samples

| t | A exact | B exact | Euler total |
| ---: | ---: | ---: | ---: |
| 0.000 | 2.500000000 | 0.750000000 | 3.250000000 |
| 3.000 | 0.823897403 | 2.426102597 | 3.250000000 |
| 6.000 | 0.271522772 | 2.978477228 | 3.250000000 |
| 9.000 | 0.089482763 | 3.160517237 | 3.250000000 |
| 12.000 | 0.029489846 | 3.220510154 | 3.250000000 |

## Boundary

This is a bounded invariant for a closed toy reaction model. It is not a new
natural law, biological discovery, enzyme mechanism, or experimental result.
