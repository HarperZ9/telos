"""Generate pass 0139 SAIR Stage 2 Lean certificate preflight docs."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_sair_stage2_lean_certificate_preflight.py"
TEST_SCRIPT = ROOT / "tools" / "test_sair_stage2_lean_certificate_preflight.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0139_sair_stage2_lean_certificate_preflight.py"
ARTIFACT = ROOT / "schemas" / "sair-stage2-lean-certificate-preflight-pass-0139.json"
TOOL_RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0139.json"
PACKET = ROOT / "packets" / "149-sair-stage2-lean-certificate-preflight.md"
BRIEF = ROOT / "briefs" / "149-sair-stage2-lean-certificate-preflight-brief.md"
STEELMAN = ROOT / "adversarial" / "pass-0139-sair-stage2-lean-certificate-preflight-steelman.md"
LEDGER = ROOT / "pass-0139-ledger.md"
THESIS = ROOT / "crucible" / "pass-0139-thesis.json"
MEASUREMENTS = ROOT / "crucible" / "pass-0139-measurements.json"


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


def run_command(command: list[str], timeout: int = 300) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def render_packet(artifact: dict) -> str:
    packet = artifact["certificate_packet"]
    counts = packet["repository"]["counts"]
    manifests = packet["repository"]["manifest_counts"]
    receipts = [{"tool": key, "status": value["status"], "exit": value["exit_code"]} for key, value in packet["local_command_receipts"].items()]
    negatives = [{"fixture": row["fixture_id"], "observed": row["observed_status"], "failures": ", ".join(row["failures"])} for row in artifact["negative_fixtures"]]
    return f"""# Packet 149: SAIR Stage 2 Lean Certificate Preflight

Date: 2026-07-02

Status: `{artifact['status']}`

Purpose: bind the public SAIR Stage 2 Lean certificate repository into the
proof-packet lane while keeping Lean replay fenced until the Lean toolchain is
available.

```text
repo_head = {packet['repository']['head_commit']}
lean_toolchain = {packet['toolchain']['lean_toolchain']}
tracked_files = {counts['tracked_files']}
lean_files = {counts['lean_files']}
python_files = {counts['python_files']}
harness_cases = {manifests['harness_manifest']}
challenger_cases = {manifests['challenger_manifest']}
marathon_cases = {manifests['marathon_manifest']}
lean_replay_status = {packet['proof_replay']['lean_replay_status']}
external_model_calls = {packet['execution_boundary']['external_model_calls']}
seal = {artifact['seal']}
```

## Source Basis

| Ref |
| --- |
{chr(10).join(f"| `{ref}` |" for ref in packet['source_refs'])}

## Certificate Contract

| Field | Value |
| --- | --- |
| Answer keys | `{', '.join(packet['certificate_contract']['answer_keys'])}` |
| Statuses | `{', '.join(packet['certificate_contract']['statuses'])}` |
| Solver size limit | `{packet['certificate_contract']['size_limits']['solver_py_bytes']}` bytes |
| Lean code limit | `{packet['certificate_contract']['size_limits']['lean_code_bytes']}` bytes |
| False-certificate limit | `{packet['certificate_contract']['size_limits']['false_certificate_bytes']}` bytes |

## Local Command Receipts

| Tool | Status | Exit |
| --- | --- | ---: |
{table(receipts, ['tool', 'status', 'exit'])}

## Negative Controls

| Fixture | Observed | Failures |
| --- | --- | --- |
{table(negatives, ['fixture', 'observed', 'failures'])}

## Boundary

{packet['promotion_boundary']}
"""


def render_brief(artifact: dict) -> str:
    packet = artifact["certificate_packet"]
    return f"""# SAIR Stage 2 Lean Certificate Preflight Brief

Date: 2026-07-02

## Decision

Stage 2 is the first clean bridge from prompt/verdict proof packets to
machine-checkable proof receipts. The right product unit is
`LeanProofReceipt/v1`: source refs, problem id, certificate code hash,
toolchain pin, judge result, rejected-token/declaration policy, and replay
status.

## Result

Pass 0139 binds repo HEAD `{packet['repository']['head_commit']}`, Lean
toolchain `{packet['toolchain']['lean_toolchain']}`, Python compileability,
manifest counts, and six negative fixtures. Replay remains fenced because
Lean/lake/elan are unavailable on this workstation.

## Next Push

Containerize the Lean toolchain or use WSL, run `scripts/run_harness.py`, then
promote only accepted fixture certificates into `LeanProofReceipt/v1`.
"""


def render_steelman(artifact: dict) -> str:
    packet = artifact["certificate_packet"]
    return f"""# Pass 0139 Steelman: SAIR Stage 2 Lean Certificate Preflight

Date: 2026-07-02

The strongest objection is that this is not a proof replay. Accepted. The
artifact explicitly records `UNVERIFIABLE_TOOL_UNAVAILABLE`.

The second objection is that Python compileability does not imply judge
correctness. Accepted. It only proves the Python surface parses locally.

The third objection is that certificate acceptance cannot be inferred from
README claims. Accepted. Acceptance requires Lean execution and judge output.

Boundary: {packet['promotion_boundary']}
"""


def build_receipts(compose: dict, test: dict, validator: dict, artifact: dict) -> dict:
    packet = artifact["certificate_packet"]
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0139",
        "compose": compose,
        "test": test,
        "validator": validator,
        "artifact_status": artifact["status"],
        "repo_head": packet["repository"]["head_commit"],
        "lean_toolchain": packet["toolchain"]["lean_toolchain"],
        "lean_replay_status": packet["proof_replay"]["lean_replay_status"],
        "external_model_calls": packet["execution_boundary"]["external_model_calls"],
        "tooling_gap": artifact["tooling_gap"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    return receipts


def thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": ARTIFACT, "composer": COMPOSER, "probe": Path(__file__).resolve(), "packet": PACKET, "brief": BRIEF, "steelman": STEELMAN, "test": TEST_SCRIPT, "validator": VALIDATOR, "tool_receipts": TOOL_RECEIPTS}
    shas = {name: sha256_file(path) for name, path in files.items()}
    packet = artifact["certificate_packet"]
    claims = [
        f"Pass 0139 created a SAIRStage2LeanCertificatePreflightReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0139 binds the public Stage 2 repo HEAD {packet['repository']['head_commit']} and ls-remote HEAD {packet['repository']['ls_remote_head']}.",
        f"Pass 0139 records {len(packet['repository']['observed_files'])} observed files and {len(packet['repository']['source_hashes'])} source hashes.",
        f"Pass 0139 records Lean toolchain {packet['toolchain']['lean_toolchain']} and repository counts {packet['repository']['counts']}.",
        f"Pass 0139 records manifest counts {packet['repository']['manifest_counts']}.",
        f"Pass 0139 Python compileall status is {packet['local_command_receipts']['python_compileall']['status']} and Lean replay status is {packet['proof_replay']['lean_replay_status']}.",
        f"Pass 0139 records {packet['execution_boundary']['external_model_calls']} external model calls.",
        f"Pass 0139 rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0139 promotes no accepted certificate, official evaluation, theorem result, market-fit result, or natural law.",
        f"Pass 0139 validator status is {receipts['validator']['status']} and test status is {receipts['test']['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"repository={packet['repository']}"],
        [f"observed_files={packet['repository']['observed_files']}", f"source_hashes={packet['repository']['source_hashes']}"],
        [f"toolchain={packet['toolchain']}", f"counts={packet['repository']['counts']}"],
        [f"manifest_counts={packet['repository']['manifest_counts']}"],
        [f"local_command_receipts={packet['local_command_receipts']}", f"proof_replay={packet['proof_replay']}"],
        [f"execution_boundary={packet['execution_boundary']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"current_promoted_results={packet['current_promoted_results']}", f"promotion_boundary={packet['promotion_boundary']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
    ]
    thesis = {"title": "Dogfood Pass 0139 SAIR Stage 2 Lean Certificate Preflight", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0139 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def render_ledger(artifact: dict) -> str:
    paths = [ARTIFACT, PACKET, BRIEF, STEELMAN, TOOL_RECEIPTS, COMPOSER, TEST_SCRIPT, VALIDATOR, Path(__file__).resolve(), THESIS, MEASUREMENTS]
    rows = [{"artifact": str(path.relative_to(ROOT)).replace("\\", "/"), "sha": sha256_file(path).upper()} for path in paths]
    return f"""# Pass 0139 Ledger - SAIR Stage 2 Lean Certificate Preflight

Date: 2026-07-02

## Objective

Move the SAIR lane from Stage 1 public judge packets into Stage 2 Lean
certificate preflight. This pass records the command surface and toolchain gap
without claiming proof replay.

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
| Repo HEAD | `{artifact['certificate_packet']['repository']['head_commit']}` |
| Lean toolchain | `{artifact['certificate_packet']['toolchain']['lean_toolchain']}` |
| Lean replay status | `{artifact['certificate_packet']['proof_replay']['lean_replay_status']}` |
| External model calls | `{artifact['certificate_packet']['execution_boundary']['external_model_calls']}` |
| Promoted results | `{len(artifact['certificate_packet']['current_promoted_results'])}` |

## Tooling Gap

{artifact['tooling_gap']}
"""


def main() -> None:
    compose = run_command([sys.executable, str(COMPOSER)])
    artifact = read_json(ARTIFACT)
    test = run_command([sys.executable, str(TEST_SCRIPT)])
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
    ok = artifact["status"] == "SAIR_STAGE2_LEAN_CERTIFICATE_PREFLIGHT_MATCH_WITH_TOOLCHAIN_GAP" and all(row["status"] == "MATCH" for row in [compose, test, validator])
    print(json.dumps({"status": "MATCH" if ok else "DRIFT", "artifact": str(ARTIFACT), "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
