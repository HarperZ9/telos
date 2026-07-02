# BuildLang Check Receipt Adapter Brief

Date: 2026-07-01

## Result

Pass 0092 parses a real `buildc check --receipt` JSON object and verifies it
with `buildc receipt verify --json`. It emits 10
Crucible-ready measurements with 10 MATCH and 0
DRIFT.

## Product Meaning

This is the first structured BuildLang compiler-receipt bridge: source digest,
input graph digest, declared effects, observed capabilities, policy profile, and
verification checks are now portable into Telos proof packets.

## Next Adapter

Run the same adapter over a source that uses filesystem or environment effects,
then compare policy pass/fail behavior.
