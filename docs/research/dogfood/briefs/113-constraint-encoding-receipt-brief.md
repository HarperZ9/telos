# Constraint-Encoding Receipt Brief

Date: 2026-07-01

## Decision

Add `ConstraintEncodingReceipt/v1` to solver branch packets before using
optimization demos as market-facing proof.

## Why

The Ocean/dimod branch matched the exact fixture, but pass 0101 showed that the
same equality-to-capacity BQM pattern is not a general `<= capacity` encoding.
The adapter keeps this distinction inspectable.

## Next Implementation Target

Promote the adapter fields into BuildLang/buildc and solver branch receipts:
constraint type, encoding method, feasibility check, counterexample reference,
and promotion block status.
