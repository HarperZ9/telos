# Dogfood Pass 0042 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `c97a7cc65ccdafec`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `c97a7cc65ccdafec761d01a8055680ce7fa4f44ae6d5d524f5077ead61c2ebc2`;
- verdict seal: `21c7c43a6350d0827e10ce75be05427aea5aee0ec8d05eccd8f2f56bb37747a3`;
- measurement seal: `b67b83225c5cbaefd6d4e7f5d24fab443293b48605fa09451faafe0d68b1662a`;
- assessment seal: `2da430cbbf545e82930b893c9bbc5be224ed27fedc91b71c5e4f2581e8c37011`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: full Lean source/build archive for compiled replay preparation.
The pass archives all 16 local Lean modules and all 6 build metadata records
identified in pass 0041. `Prob4b.lean` has both roles, so the pass contains 22
role records over 21 unique content-addressed files.

This pass archives source/build inputs only. It does not run Lean, prove
semantic equivalence by elaboration, prove an axiom-free theorem, validate every
public `pipeline-math` claim, or promote a natural law.

## Primary Receipt

Receipt:

```text
path = schemas/full-lean-source-archive-pass-0042.json
schema = FullLeanSourceArchiveSet/v1
status = FULL_LEAN_SOURCE_ARCHIVE_MATCH
sha256 = 83eefbfeab7e258aae80c8bb405bd93cc9dd7117804a3e84d3c74e1534142343
seal = 0c5b4d29bf7ea2e72398278fd57c0cf23e5e297ce2d5d99cec84aab60e528d7c
```

Fixture:

```text
path = fixtures/full-lean-source-archive-pass-0042.json
sha256 = 2a397cee6f014ee2a6c1113637d880de264324c6591d7898533d8047e8b1e83c
seal = db500e73b024ef1b1af29c4b32efeafb19faf4de3ad3e85234c75c93e1ceb9e8
```

Source binding:

```text
path = schemas/lean-toolchain-import-binding-pass-0041.json
sha256 = ae72dadc5da817622374a9b5654f7389242f3e4f7b218e4c89387d364ef2b0e7
seal = e932959ff41df5260e5af88942184e45c2e9620b878db02b4ccbb609387c78b6
status = LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH
```

## Archive Summary

```text
archive_root = archives/pass-0042-full-lean-source/sha256
lean_module_count = 16
build_file_count = 6
role_record_count = 22
unique_archive_file_count = 21
module_build_overlap_count = 1
needed_for_compiled_replay_count = 6
needed_for_compiled_replay_archived_count = 6
all_archived_sha_match_pass0041 = true
compiled_replay_status = NOT_RUN
external_call_required_for_replay = false
```

Overlapping module/build file:

```text
lean/problem-4b-formalization/Prob4b.lean
```

## Tool Substrate Receipt

Gather docs receipt for packet 052:

```text
sha256 = 85c149c0167b4d94efd3e86f8d338f2906f2fefe633ceaed41ff613b76665cfa
seal = fb44712f252e5762848fd2ccade0ff71cfb9ebfe2ea1901a98d71a36b1f51b0b
chars = 1344
```

Index dogfood substrate map:

```text
root_sha256_prefix = f2f0af39219698a9
top_level_count = 51
```

Tool receipt status:

```text
schemas/tool-receipts-pass-0042.json
status = MATCH_WITH_FORUM_SUBMIT_GAP_AND_NON_SEMANTIC_BOUNDARY
```

Forum route:

```text
decided = null
confidence = 0.07500000000000001
needs_escalation = true
top_candidates = ci-cd, model-foundry, project-telos
```

Forum submit attempt:

```text
status = UNVERIFIABLE
error = submit needs a model executor
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_full_lean_source_archive.py` | Full Lean source/build archive generator. |
| `tools/validate_pass_0042_full_lean_source_archive.py` | Validator for pass 0042 archive completeness, SHA matching, role counts, compile delta closure, and non-promotion controls. |
| `archives/pass-0042-full-lean-source/sha256/*` | Twenty-one SHA-256-addressed local source/build files. |
| `fixtures/full-lean-source-archive-pass-0042.json` | Full Lean source archive fixture. |
| `packets/052-full-lean-source-archive.md` | Human-readable full Lean source archive packet. |
| `adversarial/pass-0042-full-lean-source-archive-steelman.md` | Local pass 0042 steelman. |
| `schemas/full-lean-source-archive-pass-0042.json` | `FullLeanSourceArchiveSet/v1` artifact. |
| `schemas/pass-0042-full-lean-source-archive-validator-result.json` | Validator receipt for pass 0042. |
| `schemas/tool-receipts-pass-0042.json` | Compact Index, Gather, Shell, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0042-thesis.json` | Falsifiable claims for the forty-second pass. |
| `crucible/pass-0042-measurements.json` | Measurements/evidence for the forty-second pass. |
| `crucible/pass-0042-report.md` | Crucible report for the forty-second pass. |
| `crucible/pass-0042-run.json` | Crucible run record for the forty-second pass. |

## Primary Next Push

Create a dependency-cache proof packet for the Lake manifest packages, starting
with mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, before attempting a
compiled Lean replay.

## Natural-Law Promotion

Current promoted natural laws: none.
