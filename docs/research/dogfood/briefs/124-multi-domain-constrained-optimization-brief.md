# Multi-Domain Constrained Optimization Brief

Date: 2026-07-01

## Decision

Move from single-demo proof packets into a reusable constrained optimization
suite. The current suite has 4 toy cases across
4 domains and 4 negative
fixtures.

## Wedge

Existing solvers and simulators are strong locally. The Telos/Build wedge is a
cross-domain proof packet that carries source leads, exact constraints,
candidate plan, objective, negative witness, solver branch, and Crucible verdict
in one portable object.
