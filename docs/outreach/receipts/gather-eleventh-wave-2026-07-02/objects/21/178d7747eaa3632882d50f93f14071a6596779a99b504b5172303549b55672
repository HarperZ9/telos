# Packet 019: Heat Equation Energy Proof Kit

Date: 2026-07-01

Status: `IDENTITY` plus bounded `PROBE_MATCH`.

This packet is a scientific-compute proof-packet prototype for BuildLang/buildc. It proves a standard continuous identity for the heat equation, then attaches a bounded finite-difference witness with one stable run and one intentionally unstable negative fixture.

No new physical law is claimed. The identity is classical and is used here as a receipt-design target.

## Continuous Identity

Let `u_t = alpha u_xx` on `x in [0, 1]` with zero Dirichlet boundary conditions `u(0,t)=u(1,t)=0` and `alpha > 0`.

Define the squared `L2` energy:

```text
E(t) = int_0^1 u(x,t)^2 dx
```

Differentiate under the integral:

```text
dE/dt = 2 int_0^1 u u_t dx
      = 2 alpha int_0^1 u u_xx dx
```

Integrate by parts:

```text
int_0^1 u u_xx dx = [u u_x]_0^1 - int_0^1 u_x^2 dx
```

The boundary term vanishes because `u=0` at both endpoints. Therefore:

```text
dE/dt = -2 alpha int_0^1 u_x^2 dx <= 0
```

This proves energy monotonicity for sufficiently smooth solutions with the stated boundary conditions.

## Numerical Witness

The probe script `tools/probe_heat_equation_energy.py` runs an explicit finite-difference heat solver on 129 grid points for 400 steps.

Stable run:

- `cfl=0.45`;
- initial energy `0.53125`;
- final energy `0.4069449317114255`;
- energy increase count `0`;
- status `ENERGY_MONOTONE`.

Negative fixture:

- `cfl=0.55`;
- first detected energy increase at step `201`;
- increase count `199`;
- final energy `1.5979193736301155e+28`;
- status `ENERGY_INCREASE_DETECTED`.

Probe seal:

```text
b3021c14b0e5dc8adeddadf0d22e2780dbf259c349caf5cbc2ba255b591fd7d5
```

## BuildLang/buildc Receipt Requirement

For scientific-compute credibility, BuildLang/buildc should not only execute PDE kernels. It should emit a proof kit:

- continuous identity or model invariant;
- discretization assumptions;
- stability condition;
- compiler/runtime receipt;
- input and output hashes;
- thresholded measurements;
- negative fixture;
- external verdict.

The heat equation is the smallest useful example because the continuous identity is short, the discrete CFL boundary is visible, and the negative fixture fails in a way buyers understand.

## Non-Promotion Statement

This packet promotes no new natural law, theorem breakthrough, engineering safety result, medical result, finance result, or production CFD result.
