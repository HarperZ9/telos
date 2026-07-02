# Packet 052: Full Lean Source Archive

Date: 2026-07-01

Status: `FULL_LEAN_SOURCE_ARCHIVE_MATCH`

Pass 0042 archives every local source/build input identified in pass 0041:
all 16 local Lean modules and all 6 build metadata records. Because
`Prob4b.lean` is both a Lean module and a build/root import file, the archive
contains 21 unique content-addressed files.

## Archive Binding

```text
source = schemas/lean-toolchain-import-binding-pass-0041.json
source_sha256 = ae72dadc5da817622374a9b5654f7389242f3e4f7b218e4c89387d364ef2b0e7
source_seal = e932959ff41df5260e5af88942184e45c2e9620b878db02b4ccbb609387c78b6
archive_root = archives/pass-0042-full-lean-source/sha256
lean_module_count = 16
build_file_count = 6
unique_archive_file_count = 21
module_build_overlap_count = 1
compiled_replay_status = NOT_RUN
```

## Product Reading

This pass closes the local source archive gap before compiled replay. A later
runner can reconstruct the project inputs from content-addressed files and
compare each byte stream to pass 0041 before attempting Lean/Lake execution.

## Non-Promotion Boundary

Pass 0042 archives source and build inputs. It does not run Lean, prove semantic
equivalence by elaboration, prove an axiom-free result, validate every public
`pipeline-math` claim, or promote any natural law.

Current promoted natural laws: none.
