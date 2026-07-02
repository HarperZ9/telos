# Formal Target Packaging Brief

Date: 2026-07-01

## Decision

Make formal-prover source files first-class packet material. Pass 0118 emits
and hashes Lean, Rocq, Isabelle, and Agda targets derived from the pass 0117
finite category witness. This is still not a prover execution claim.

## Product Meaning

This moves the formal proof lane from loose target strings to portable source
files that a future prover runner can parse, execute, and return receipts for.
It is the adapter seam between research proof packets and actual formal proof
toolchains.

Manifest: `formal-targets/pass-0118/manifest.json`
