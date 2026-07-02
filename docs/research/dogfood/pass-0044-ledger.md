# Dogfood Pass 0044 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `2a61d018b04208e7`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `2a61d018b04208e7380b792f260a0a90c875c042bd3028a7fb0fc6e45493eb8e`;
- verdict seal: `973a0ca42746a6916accbb055210438a2812f06c506431035e7ea95df0bcfa2c`;
- measurement seal: `d38d9082cefa02691c03d2a3f4ceccbd14cb250cd040722f27e862ed3123c55c`;
- assessment seal: `07766394f2a3f056e117bffe51ce4ede154715f348903c1cf273399846b827be`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: Lean/Lake executable preflight before compiled replay. The pass
records that this shell cannot currently discover `lake`, `lean`, or `elan` on
PATH or in the checked common Elan locations. It also records the expected
toolchain and a Lake manifest/lakefile project-name mismatch.

This pass is an admission gate, not a compile pass. It does not run Lean, run
`lake build`, compile dependencies, prove semantic equivalence by elaboration,
validate every public `pipeline-math` claim, or promote a natural law.

## Primary Receipt

Receipt:

```text
path = schemas/lean-lake-executable-preflight-pass-0044.json
schema = LeanLakeExecutablePreflightSet/v1
status = LEAN_LAKE_EXECUTABLE_PREFLIGHT_BLOCKED
sha256 = d98513f50b384ed38e4d52d6379916bc6b43dacc318571e0299ecd1d3dcc055f
seal = 7139ea2e8ed154dcb5069fd5d5433fec85103b88d9bf309450dfd1193a6de607
```

Fixture:

```text
path = fixtures/lean-lake-executable-preflight-pass-0044.json
sha256 = 51f60da2e6581cf87b26111818060e37c59af0dec859f43df8b67bbe9e1b8898
seal = 7eb73ddc3f379c7c51a31fe570be2430171a8ad3242ad0e7bc582998f7959746
```

Source binding:

```text
path = schemas/lake-dependency-cache-binding-pass-0043.json
sha256 = 393f71b91fb69d800aff7f81751517eb62af2ee0d098670ae97d4f16a869de22
seal = 8e88cd761c7ae0996c6d20bfeb78fb5cf9bf6083a3de1f09601a62463a5d665b
status = LAKE_DEPENDENCY_CACHE_BINDING_MATCH
```

## Preflight Summary

```text
expected_toolchain = leanprover/lean4:v4.31.0
lake_on_path = false
lean_on_path = false
elan_on_path = false
common_elan_candidates_present = 0
compiled_replay_admissible = false
compiled_replay_status = NOT_RUN
lakefile_name = Prob4b
manifest_name = Prob27b
project_name_match = false
```

## Tool Substrate Receipt

Gather docs receipt for packet 054:

```text
sha256 = 91e38389327c8daee3c939e605a43213f8001707d3ade0a9ca2bfaa3107db570
seal = 2d9640f6cea256b90b4117652b12415ad9c86a58b67193fe1a9cb5720d9fd37f
chars = 1395
```

Index dogfood substrate map:

```text
root_sha256_prefix = f2f0af39219698a9
top_level_count = 53
```

Tool receipt status:

```text
schemas/tool-receipts-pass-0044.json
status = MATCH_WITH_FORUM_SUBMIT_GAP_AND_EXECUTABLE_PREFLIGHT_BLOCKED
```

Forum route:

```text
decided = null
confidence = 0.045454545454545456
needs_escalation = true
top_candidates = project-telos, backend, ci-cd
```

Forum submit attempt:

```text
status = UNVERIFIABLE
error = submit needs a model executor
```

Telos operator doctor:

```text
aggregate_verdict = MATCH
check_count = 14
passed_count = 14
tool_count = 65
telos_tool_count = 37
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_lean_lake_executable_preflight.py` | Lean/Lake executable preflight generator. |
| `tools/validate_pass_0044_lean_lake_executable_preflight.py` | Validator for pass 0044 executable absence, toolchain binding, project-name signal, pass 0043 binding, and non-promotion controls. |
| `fixtures/lean-lake-executable-preflight-pass-0044.json` | Lean/Lake executable preflight fixture. |
| `packets/054-lean-lake-executable-preflight.md` | Human-readable Lean/Lake executable preflight packet. |
| `adversarial/pass-0044-lean-lake-executable-preflight-steelman.md` | Local pass 0044 steelman. |
| `schemas/lean-lake-executable-preflight-pass-0044.json` | `LeanLakeExecutablePreflightSet/v1` artifact. |
| `schemas/pass-0044-lean-lake-executable-preflight-validator-result.json` | Validator receipt for pass 0044. |
| `schemas/tool-receipts-pass-0044.json` | Compact Index, Gather, Shell, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0044-thesis.json` | Falsifiable claims for the forty-fourth pass. |
| `crucible/pass-0044-measurements.json` | Measurements/evidence for the forty-fourth pass. |
| `crucible/pass-0044-report.md` | Crucible report for the forty-fourth pass. |
| `crucible/pass-0044-run.json` | Crucible run record for the forty-fourth pass. |

## Primary Next Push

Either locate/install the Lean executable layer for `leanprover/lean4:v4.31.0`
or pivot to a non-Lean proof packet that advances market/architecture strategy
while the replay blocker remains explicit.

## Natural-Law Promotion

Current promoted natural laws: none.
