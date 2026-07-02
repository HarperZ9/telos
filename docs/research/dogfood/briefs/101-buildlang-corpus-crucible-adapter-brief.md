# BuildLang Corpus Crucible Adapter Brief

Date: 2026-07-01

## Result

Pass 0091 converts live `buildc corpus verify` output into
10 Crucible-ready measurements, all matching.

## Product Meaning

BuildLang/buildc now has a direct bridge from compiler corpus receipts to the
same claim-verdict machinery used by Telos dogfood packets. This is the
substrate proof adapter promised by the market research passes.

## Next Adapter

Join one `.bld` source-level `buildc check --receipt` output to the same
Crucible measurement schema.
