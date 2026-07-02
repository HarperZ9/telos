# Packet 122: Lyapunov Stability Certificate Receipt

Date: 2026-07-01

Status: `LYAPUNOV_STABILITY_CERTIFICATE_RECEIPT_MATCH`

Purpose: prove a bounded exact discrete-time Lyapunov certificate for a rational
linear system and package it as a control/autonomy proof packet.

```text
runtime_suite_pass = 0111
youtube_roadmap_pass = 0102
A = [['1/2', '0'], ['0', '1/3']]
P = [['4/3', '0'], ['0', '9/8']]
Q = [['1', '0'], ['0', '1']]
max_spectral_radius_abs = 1/2
max_identity_residual = 0
unstable_fixture = PD_FAIL_EXPECTED
bad_certificate_fixture = RESIDUAL_DRIFT_EXPECTED
source_anchor_count = 10
valid_youtube_videos = 19
compose_status = MATCH
test_status = MATCH
```

## Energy Samples

| x | Delta V | -xTQx | Status |
| --- | --- | --- | --- |
| ['1', '0'] | -1 | -1 | MATCH |
| ['0', '2'] | -4 | -4 | MATCH |
| ['3', '-2'] | -13 | -13 | MATCH |

## Source Anchors

| Tool | Kind | URL |
| --- | --- | --- |
| SciPy | official_docs | https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_discrete_lyapunov.html |
| MATLAB dlyap | official_docs | https://www.mathworks.com/help/control/ref/dlyap.html |
| MATLAB Control System Toolbox | official_product | https://www.mathworks.com/products/control.html |
| python-control | official_docs | https://python-control.readthedocs.io/en/0.10.2/generated/control.dlyap.html |
| Drake | official_docs | https://drake.mit.edu/ |
| CasADi | official_docs | https://web.casadi.org/docs/ |
| do-mpc | official_docs | https://www.do-mpc.com/ |
| OSQP | official_docs | https://osqp.org/docs/examples/mpc.html |
| CVXPY | official_docs | https://www.cvxpy.org/ |
| MIT Underactuated | course_notes | https://underactuated.mit.edu/lyapunov.html |

## Boundary

This pass proves a bounded exact Lyapunov identity for one rational linear system. It does not validate hardware control, prove nonlinear stability, compile BuildLang, or promote a natural law.
