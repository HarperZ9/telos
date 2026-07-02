# Dogfood Pass 0043 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `dfb13dcdd32a219f`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `dfb13dcdd32a219fa471c2aa10fd145a13651af1e5ed6fcea30a8c3e890a1114`;
- verdict seal: `7a7f292147b0c97c67a8fab64d05d6335f320e2bcf115c43987f00749c87fed6`;
- measurement seal: `4d52f30dba34800628c4b46bc27daecd42915860df3df6ede11dc002d83f8c50`;
- assessment seal: `a55bb92be117989e0e04d8e1b2202ea4f42a90f4f58a44d1e432e5b2ef175ef2`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: Lake dependency cache binding for compiled replay preparation.
The pass checks that all nine packages in `lake-manifest.json` have present
local `.lake/packages` checkouts, clean worktrees, origin URLs matching the
manifest after `.git` suffix normalization, and HEAD commits matching the
manifest revisions.

This pass checks dependency cache identity only. It does not run Lean, compile
dependencies, prove semantic equivalence by elaboration, prove an axiom-free
result, validate every public `pipeline-math` claim, or promote a natural law.

## Primary Receipt

Receipt:

```text
path = schemas/lake-dependency-cache-binding-pass-0043.json
schema = LakeDependencyCacheBindingSet/v1
status = LAKE_DEPENDENCY_CACHE_BINDING_MATCH
sha256 = 393f71b91fb69d800aff7f81751517eb62af2ee0d098670ae97d4f16a869de22
seal = 8e88cd761c7ae0996c6d20bfeb78fb5cf9bf6083a3de1f09601a62463a5d665b
```

Fixture:

```text
path = fixtures/lake-dependency-cache-binding-pass-0043.json
sha256 = f5873cca174833d9f8e8e655586774d2a46487ee07a8b1710660e80eef5e3c5b
seal = 4eb29447aeb8870d281f61e422bd4d4c0629dc3f812ec77368b5e11712e3f94d
```

Source binding:

```text
path = schemas/full-lean-source-archive-pass-0042.json
sha256 = 83eefbfeab7e258aae80c8bb405bd93cc9dd7117804a3e84d3c74e1534142343
seal = 0c5b4d29bf7ea2e72398278fd57c0cf23e5e297ce2d5d99cec84aab60e528d7c
status = FULL_LEAN_SOURCE_ARCHIVE_MATCH
```

## Dependency Cache Summary

```text
lake_manifest = lean/problem-4b-formalization/lake-manifest.json
package_count = 9
present_package_count = 9
head_match_count = 9
clean_package_count = 9
all_package_heads_match_manifest = true
all_package_urls_match_manifest = true
compiled_replay_status = NOT_RUN
```

Bound package revisions:

| Package | Manifest rev |
| --- | --- |
| `mathlib` | `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` |
| `plausible` | `63045536fe95024e6c18fc7b48e03f506701c5bc` |
| `LeanSearchClient` | `c5d5b8fe6e5158def25cd28eb94e4141ad97c843` |
| `importGraph` | `5c7542ed018c78194f1e2b903eaf6a792b74c03d` |
| `proofwidgets` | `24b0d9dc081c5423f8eec7e866c441e5184f29d9` |
| `aesop` | `e3cb2f741431ce31bf73549fb52316a57368b06f` |
| `Qq` | `f46324995fca5f0483b742e4eb4daec7f4ee50d2` |
| `batteries` | `fa08db58b30eb033edcdab331bba000827f9f785` |
| `Cli` | `92564e5770e4d09f2d86dfbf8ada1e9c715b384c` |

## Tool Substrate Receipt

Gather docs receipt for packet 053:

```text
sha256 = 96228fb6991631c4f84466bef2111e67143efe86434170f8931ca0cea6413473
seal = f7855433a2e8e74998b405d20c434a72b5f3fc37e2173e1fd0d15e7d35e371de
chars = 1201
```

Index dogfood substrate map:

```text
root_sha256_prefix = f2f0af39219698a9
top_level_count = 52
```

Index MCP context envelope:

```text
schema = project-telos.context-envelope/v1
verification_verdict = MATCH
graph_pack_sha256 = 185c0236c1370daa81b49d11c7cab1f29c2a279be3d83302150f0d63396ad6dd
```

Tool receipt status:

```text
schemas/tool-receipts-pass-0043.json
status = MATCH_WITH_FORUM_SUBMIT_GAP_AND_NON_SEMANTIC_BOUNDARY
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
| `tools/probe_lake_dependency_cache_binding.py` | Lake dependency cache binding generator. |
| `tools/validate_pass_0043_lake_dependency_cache_binding.py` | Validator for pass 0043 package presence, clean status, URL matching, HEAD matching, pass 0042 binding, and non-promotion controls. |
| `fixtures/lake-dependency-cache-binding-pass-0043.json` | Lake dependency cache binding fixture. |
| `packets/053-lake-dependency-cache-binding.md` | Human-readable Lake dependency cache binding packet. |
| `adversarial/pass-0043-lake-dependency-cache-binding-steelman.md` | Local pass 0043 steelman. |
| `schemas/lake-dependency-cache-binding-pass-0043.json` | `LakeDependencyCacheBindingSet/v1` artifact. |
| `schemas/pass-0043-lake-dependency-cache-binding-validator-result.json` | Validator receipt for pass 0043. |
| `schemas/tool-receipts-pass-0043.json` | Compact Index, Gather, Shell, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0043-thesis.json` | Falsifiable claims for the forty-third pass. |
| `crucible/pass-0043-measurements.json` | Measurements/evidence for the forty-third pass. |
| `crucible/pass-0043-report.md` | Crucible report for the forty-third pass. |
| `crucible/pass-0043-run.json` | Crucible run record for the forty-third pass. |

## Primary Next Push

Create a Lean/Lake executable availability and command preflight packet before
attempting a bounded compiled replay.

## Natural-Law Promotion

Current promoted natural laws: none.
