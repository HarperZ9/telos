# Packet 051: Lean Toolchain Import Binding

Date: 2026-07-01

Status: `LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH`

Pass 0041 binds the archived theorem-source packet to the Lean/Lake metadata
needed for compiled replay: `lean-toolchain`, `lakefile.toml`,
`lake-manifest.json`, root module imports, and the local `Prob4b` import graph.

## Toolchain Binding

```text
repo_commit = 69d7df765a8f377a5e0628c6d36c088bce7642c9
toolchain = leanprover/lean4:v4.31.0
mathlib_input_rev = v4.31.0
mathlib_rev = fabf563a7c95a166b8d7b6efca11c8b4dc9d911f
lake_manifest_package_count = 9
build_file_count = 6
lean_module_count = 16
local_import_edge_count = 41
external_import_edge_count = 1
compiled_replay_status = NOT_RUN
```

## Archive Delta

```text
archived_source_file_count = 10
needed_for_compiled_replay_count = 6
archive_replay_binding = schemas/theorem-archived-blob-statement-replay-pass-0040.json
```

## Product Reading

This pass turns source-signature proof packets into a compile-replay planning
packet. It identifies the exact Lean version, mathlib revision, Lake manifest,
root module, import edges, archived theorem files, and additional local files
that must be included before a full Lean replay can be attempted.

## Non-Promotion Boundary

Pass 0041 discovers and binds toolchain/import metadata. It does not run Lean,
prove semantic equivalence by elaboration, prove an axiom-free result, validate
every public `pipeline-math` claim, or promote any natural law.

Current promoted natural laws: none.
