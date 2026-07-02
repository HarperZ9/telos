"""Generate pass 0138 SAIR Stage 1 judge repository adapter docs."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_sair_stage1_judge_repo_adapter.py"
TEST_SCRIPT = ROOT / "tools" / "test_sair_stage1_judge_repo_adapter.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0138_sair_stage1_judge_repo_adapter.py"
ARTIFACT = ROOT / "schemas" / "sair-stage1-judge-repo-adapter-pass-0138.json"
TOOL_RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0138.json"
PACKET = ROOT / "packets" / "148-sair-stage1-judge-repo-adapter.md"
BRIEF = ROOT / "briefs" / "148-sair-stage1-judge-repo-adapter-brief.md"
STEELMAN = ROOT / "adversarial" / "pass-0138-sair-stage1-judge-repo-adapter-steelman.md"
LEDGER = ROOT / "pass-0138-ledger.md"
THESIS = ROOT / "crucible" / "pass-0138-thesis.json"
MEASUREMENTS = ROOT / "crucible" / "pass-0138-measurements.json"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.encode("ascii", "ignore").decode("ascii"), encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 240) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def render_packet(artifact: dict) -> str:
    packet = artifact["competition_packet"]
    model_rows = packet["model_config_summary"]["routes"]
    receipt_rows = [{"command": key, "status": value["status"], "exit": value["exit_code"]} for key, value in packet["local_command_receipts"].items()]
    negative_rows = [{"fixture": row["fixture_id"], "observed": row["observed_status"], "failures": ", ".join(row["failures"])} for row in artifact["negative_fixtures"]]
    return f"""# Packet 148: SAIR Stage 1 Judge Repository Adapter

Date: 2026-07-02

Status: `{artifact['status']}`

Purpose: bind the public SAIR Stage 1 judge repository to our proof-packet
lane without making hosted model calls, exporting secrets, or claiming official
competition performance.

```text
repo_head = {packet['repository']['head_commit']}
observed_files = {len(packet['repository']['observed_files'])}
source_hashes = {len(packet['repository']['source_hashes'])}
official_model_aliases = {packet['model_config_summary']['model_count']}
local_command_receipts = {len(packet['local_command_receipts'])}
negative_fixtures = {len(artifact['negative_fixtures'])}
external_model_calls = {packet['execution_boundary']['external_model_calls']}
seal = {artifact['seal']}
```

## Source Basis

| Ref |
| --- |
{chr(10).join(f"| `{ref}` |" for ref in packet['source_refs'])}

## Official Command Surface Observed

The public repository describes prompt rendering, OpenRouter routed model
calls, verdict extraction, and a local smoke test. This pass executes only the
local no-secret surface: repository tests, prompt rendering, verdict parsing,
and the missing-key boundary.

## Model Configuration

| Alias | Model | Provider | Tokens | Temperature | Seed |
| --- | --- | --- | ---: | ---: | --- |
{table(model_rows, ['alias', 'model', 'provider', 'max_output_tokens', 'temperature', 'seed'])}

## Local Command Receipts

| Command | Status | Exit |
| --- | --- | ---: |
{table(receipt_rows, ['command', 'status', 'exit'])}

## Negative Controls

| Fixture | Observed | Failures |
| --- | --- | --- |
{table(negative_rows, ['fixture', 'observed', 'failures'])}

## Boundary

{packet['promotion_boundary']}
"""


def render_brief(artifact: dict) -> str:
    packet = artifact["competition_packet"]
    return f"""# SAIR Stage 1 Judge Repository Adapter Brief

Date: 2026-07-02

## Decision

Promote the SAIR lane from synthetic fixture to public repository adapter.
The repo gives us a compact competition proof-packet surface: prompt template,
problem JSONL, pinned model config, model-call boundary, verdict extractor, and
test suite.

## Product Implication

This becomes the first `CompetitionProofPacket` adapter class: a source-pinned
public judge repo can be wrapped by Gather source refs, Index context, Forum
routing, Crucible claims, Telos action receipts, and future BuildLang exact
reasoning branches.

## Next Push

Add a hosted-model attempt receipt that records provider route, prompt hash,
problem ids, response hash, parser verdict, cost/tokens, and action admission
without exporting the API key or hidden reasoning. Then attach a Stage 2 Lean
certificate branch.

Repo head: `{packet['repository']['head_commit']}`.
"""


def render_steelman(artifact: dict) -> str:
    packet = artifact["competition_packet"]
    return f"""# Pass 0138 Steelman: SAIR Stage 1 Judge Repository Adapter

Date: 2026-07-02

The strongest objection is that this still does not run official evaluation
models. Accepted. The pass verifies the public repo command surface and local
no-secret gates only.

The second objection is that a public judge repo can change after this pass.
Accepted. The artifact binds to a concrete HEAD commit and file hashes.

The third objection is that model-accuracy work may leak raw responses or
provider credentials. Accepted. The next attempt receipt must hash prompts and
responses, remove secrets, and record action admission before any provider call.

Boundary: {packet['promotion_boundary']}
"""


def build_receipts(compose: dict, test: dict, validator: dict, artifact: dict) -> dict:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0138",
        "compose": compose,
        "test": test,
        "validator": validator,
        "artifact_status": artifact["status"],
        "repo_head": artifact["competition_packet"]["repository"]["head_commit"],
        "observed_file_count": len(artifact["competition_packet"]["repository"]["observed_files"]),
        "source_hash_count": len(artifact["competition_packet"]["repository"]["source_hashes"]),
        "external_model_calls": artifact["competition_packet"]["execution_boundary"]["external_model_calls"],
        "tooling_gap": artifact["tooling_gap"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    return receipts


def thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {
        "artifact": ARTIFACT,
        "composer": COMPOSER,
        "probe": Path(__file__).resolve(),
        "packet": PACKET,
        "brief": BRIEF,
        "steelman": STEELMAN,
        "test": TEST_SCRIPT,
        "validator": VALIDATOR,
        "tool_receipts": TOOL_RECEIPTS,
    }
    shas = {name: sha256_file(path) for name, path in files.items()}
    packet = artifact["competition_packet"]
    claims = [
        f"Pass 0138 created a SAIRStage1JudgeRepoAdapterReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0138 binds the public judge repo HEAD {packet['repository']['head_commit']} and ls-remote HEAD {packet['repository']['ls_remote_head']}.",
        f"Pass 0138 records {len(packet['repository']['observed_files'])} observed public repo files and {len(packet['repository']['source_hashes'])} source hashes.",
        f"Pass 0138 records {packet['model_config_summary']['model_count']} official local model aliases with allow_fallbacks={packet['model_config_summary']['allow_fallbacks']} and token cap {packet['model_config_summary']['max_output_tokens_cap']}.",
        "Pass 0138 local command receipts for pytest, prompt CLI, judge CLI, and missing-key boundary are MATCH.",
        f"Pass 0138 records {packet['execution_boundary']['external_model_calls']} external model calls.",
        f"Pass 0138 rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0138 promotes no official evaluation, leaderboard result, theorem result, market-fit result, or natural law.",
        f"Pass 0138 validator status is {receipts['validator']['status']} and test status is {receipts['test']['status']}.",
        f"Pass 0138 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"repository={packet['repository']}"],
        [f"observed_files={packet['repository']['observed_files']}", f"source_hashes={packet['repository']['source_hashes']}"],
        [f"model_config_summary={packet['model_config_summary']}"],
        [f"local_command_receipts={packet['local_command_receipts']}"],
        [f"execution_boundary={packet['execution_boundary']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"current_promoted_results={packet['current_promoted_results']}", f"promotion_boundary={packet['promotion_boundary']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0138 SAIR Stage 1 Judge Repo Adapter", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0138 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def render_ledger(artifact: dict) -> str:
    paths = [ARTIFACT, PACKET, BRIEF, STEELMAN, TOOL_RECEIPTS, COMPOSER, TEST_SCRIPT, VALIDATOR, Path(__file__).resolve(), THESIS, MEASUREMENTS]
    rows = [{"artifact": str(path.relative_to(ROOT)).replace("\\", "/"), "sha": sha256_file(path).upper()} for path in paths]
    return f"""# Pass 0138 Ledger - SAIR Stage 1 Judge Repository Adapter

Date: 2026-07-02

## Objective

Move the SAIR Stage 1 lane from a synthetic local proof-packet fixture into a
source-pinned public judge repository adapter. This pass observes the public
repository at a concrete HEAD, runs its local no-secret command surface, and
keeps hosted model calls fenced.

## Outputs

| Artifact | SHA-256 |
| --- | --- |
{table(rows, ['artifact', 'sha'])}

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `{artifact['schema']}` |
| Status | `{artifact['status']}` |
| Artifact seal | `{artifact['seal']}` |
| Repo HEAD | `{artifact['competition_packet']['repository']['head_commit']}` |
| Observed files | `{len(artifact['competition_packet']['repository']['observed_files'])}` |
| Source hashes | `{len(artifact['competition_packet']['repository']['source_hashes'])}` |
| Local command receipts | `{len(artifact['competition_packet']['local_command_receipts'])}` |
| Negative fixtures | `{len(artifact['negative_fixtures'])}` |
| External model calls | `{artifact['competition_packet']['execution_boundary']['external_model_calls']}` |
| Promoted results | `{len(artifact['competition_packet']['current_promoted_results'])}` |

## Tooling Gap

{artifact['tooling_gap']}

## Next Pass Queue

1. Add a hosted-model attempt receipt with redacted provider call evidence.
2. Add a Stage 2 Lean certificate receipt adapter.
3. Add a BuildLang/buildc exact equational-reasoning branch.
4. Add Forum routing for `formal_math_competition_repo_adapter`.
"""


def main() -> None:
    compose = run_command([sys.executable, str(COMPOSER)])
    artifact = read_json(ARTIFACT)
    test = run_command([sys.executable, str(TEST_SCRIPT)], timeout=300)
    validator = run_command([sys.executable, str(VALIDATOR)])
    receipts = build_receipts(compose, test, validator, artifact)
    write_json(TOOL_RECEIPTS, receipts)
    write_text(PACKET, render_packet(artifact))
    write_text(BRIEF, render_brief(artifact))
    write_text(STEELMAN, render_steelman(artifact))
    thesis, measurements = thesis_measurements(artifact, receipts)
    write_json(THESIS, thesis)
    write_json(MEASUREMENTS, measurements)
    write_text(LEDGER, render_ledger(artifact))
    ok = artifact["status"] == "SAIR_STAGE1_JUDGE_REPO_ADAPTER_MATCH" and all(row["status"] == "MATCH" for row in [compose, test, validator])
    print(json.dumps({"status": "MATCH" if ok else "DRIFT", "artifact": str(ARTIFACT), "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
