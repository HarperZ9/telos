# Periodic Taylor-Green Energy Identity

Packet: `navier-stokes-periodic-energy-identity-v0`

Status: bounded subclaim, not a grand theorem.

## Statement

Let

```text
u1(x,y,t) = A(t) sin(x) cos(y)
u2(x,y,t) = -A(t) cos(x) sin(y)
A(t) = exp(-2 nu t)
```

on the periodic square `[0, 2*pi]^2`, with `nu > 0`.

For this smooth divergence-free field:

```text
E(t) = 0.5 * integral(|u|^2)
D(t) = nu * integral(|grad u|^2)
dE/dt + D(t) = 0
```

## Analytic Check

Using periodic trigonometric averages:

```text
integral(u1^2) = pi^2 A(t)^2
integral(u2^2) = pi^2 A(t)^2
integral(|u|^2) = 2 pi^2 A(t)^2
E(t) = pi^2 A(t)^2
dE/dt = -4 nu pi^2 A(t)^2
integral(|grad u|^2) = 4 pi^2 A(t)^2
D(t) = 4 nu pi^2 A(t)^2
```

Therefore:

```text
dE/dt + D(t) = 0
```

## What This Proves

If the statement, assumptions, and executable receipt match, this packet can support a bounded identity claim for this smooth periodic velocity field.

## What This Does Not Prove

- It does not prove existence and smoothness for arbitrary Navier-Stokes solutions.
- It does not prove global regularity.
- It does not prove uniqueness.
- It does not prove turbulence closure.
- It does not validate a physical simulator.
- It does not establish a new law of physics.

## Promotion Rule

The subclaim may become `CRUCIBLE_MATCH` if the executable receipt shows residuals within tolerance and Crucible rechecks the bounded claim. The parent Millennium problem remains `UNVERIFIABLE`.
