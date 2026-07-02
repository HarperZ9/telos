# Periodic Incompressible Advection Skew-Symmetry

Packet: `navier-stokes-periodic-skew-symmetry-v0`

## Statement

Let `u(x,y)` be a smooth divergence-free velocity field on the periodic domain
`Omega = [0, 2pi]^2`. The nonlinear advection term has zero direct
contribution to kinetic energy:

```text
integral_Omega u dot ((u dot grad)u) dx dy = 0.
```

Equivalently, in the formal energy balance, advection redistributes kinetic
energy but does not create it. Viscosity is the dissipative term.

## Derivation

Use the product identity:

```text
u dot ((u dot grad)u) = (1/2) u dot grad(|u|^2).
```

Integrate over the periodic domain:

```text
integral_Omega (1/2) u dot grad(|u|^2)
  = (1/2) integral_Omega div(u |u|^2) - (1/2) integral_Omega (div u) |u|^2.
```

The divergence term integrates to zero on a periodic domain. The second term is
zero because `div u = 0`. Therefore:

```text
integral_Omega u dot ((u dot grad)u) dx dy = 0.
```

## Executable Witness

The reference kernel constructs a deterministic finite Fourier-mode
streamfunction:

```text
psi(x,y) = sum_j a_j sin(kx_j x + ky_j y + phase_j)
```

and derives velocity by:

```text
u = (partial_y psi, -partial_x psi).
```

This makes the field analytically divergence-free. The kernel evaluates
analytic derivatives on a uniform periodic grid and checks:

- maximum pointwise divergence
- kinetic energy
- gradient-energy dissipation proxy
- nonlinear energy-transfer integral

## What This Proves

The written derivation proves the smooth-periodic skew-symmetry identity under
the stated assumptions, subject to ordinary mathematical review or formal
replay.

The executable receipt proves only that this particular finite-mode witness
matches the identity within declared numeric tolerance.

## What This Does Not Prove

- It does not prove Navier-Stokes existence and smoothness.
- It does not prove global regularity.
- It does not prove that arbitrary finite-difference schemes preserve the
  identity.
- It does not validate a physical fluid simulation.
- It does not establish a new law of physics.

