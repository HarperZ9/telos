# Packet 111: Inequality-Safe BQM Receipt

Date: 2026-07-01

Status: `INEQUALITY_SAFE_BQM_RECEIPT_MATCH`

Purpose: test whether the pass 0100 equality-to-capacity BQM penalty is safe
for general `weight <= capacity` knapsack. It is not; this pass records a
counterexample and a slack-variable fix.

```text
problem_values = [10, 9]
problem_weights = [3, 2]
capacity = 4
true_optimum_value = 10
equality_penalty_value = 19
equality_penalty_feasible = False
slack_penalty_value = 10
slack_penalty_feasible = True
law_candidate = knapsack_inequality_bqm_requires_slack_or_inequality_encoding
compose_status = MATCH
test_status = MATCH
```

## Finding

A squared equality penalty on `sum(weights) - capacity` selects the overweight
set with value 19. The true feasible optimum is value 10. Adding binary slack
variables to encode `sum(weights) + slack = capacity` recovers the feasible
optimum.

Boundary: this is a law candidate with one counterexample and one fix, not a
promoted natural law.
