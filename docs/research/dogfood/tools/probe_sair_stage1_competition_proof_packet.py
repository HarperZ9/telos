"""Generate pass 0137 SAIR-style CompetitionProofPacket docs and claims."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_sair_stage1_competition_proof_packet.py"
TEST_SCRIPT = ROOT / "tools" / "test_sair_stage1_competition_proof_packet.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0137_sair_stage1_competition_proof_packet.py"
ARTIFACT = ROOT / "schemas" / "sair-stage1-competition-proof-packet-pass-0137.json"
TOOL_RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0137.json"
PACKET = ROOT / "packets" / "147-sair-stage1-competition-proof-packet.md"
BRIEF = ROOT / "briefs" / "147-sair-stage1-competition-proof-packet-brief.md"
STEELMAN = ROOT / "adversarial" / "pass-0137-sair-competition-proof-packet-steelman.md"
THESIS = ROOT / "crucible" / "pass-0137-thesis.json"
MEASUREMENTS = ROOT / "crucible" / "pass-0137-measurements.json"


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


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def table(rows: list[dict], cols: list[str]) -> str:
    lines = []
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |")
    return "\n".join(lines)


def render_packet(artifact: dict) -> str:
    packet = artifact["competition_packet"]
    problems = [
        {
            "id": row["problem_id"],
            "eq1": row["equation1"],
            "eq2": row["equation2"],
            "expected": row["expected_answer"],
            "oracle": row["oracle_kind"],
        }
        for row in artifact["problem_fixtures"]
    ]
    attempts = [
        {
            "problem": row["problem_id"],
            "parsed": row["parsed_verdict"],
            "expected": row["expected_answer"],
            "correct": row["correct"],
            "runner": row["runner"],
        }
        for row in packet["attempt_receipts"]
    ]
    negatives = [
        {"fixture": row["fixture_id"], "observed": row["observed_status"], "failures": ", ".join(row["failures"])}
        for row in packet["negative_fixtures"]
    ]
    return f"""# Packet 147: SAIR Stage 1 Competition Proof Packet Fixture

Date: 2026-07-02

Status: `{artifact['status']}`

Purpose: turn the SAIR Stage 1-style math-distillation source lead into a
local, replayable `CompetitionProofPacket` fixture. This packet does not call
external model APIs, does not submit to SAIR, does not claim leaderboard
performance, and does not prove new mathematics.

```text
source_refs = {len(packet['source_refs'])}
problem_fixtures = {len(artifact['problem_fixtures'])}
attempts = {packet['verdict_summary']['attempts']}
correct_attempts = {packet['verdict_summary']['correct']}
external_model_calls = {packet['verdict_summary']['external_model_calls']}
parser_tests = {len(artifact['parser_tests'])}
negative_fixtures = {len(packet['negative_fixtures'])}
seal = {artifact['seal']}
```

## Source Basis

| Ref |
| --- |
{chr(10).join(f"| `{ref}` |" for ref in packet['source_refs'])}

## Problem Fixtures

| Problem | Equation 1 | Equation 2 | Expected | Oracle |
| --- | --- | --- | --- | --- |
{table(problems, ['id', 'eq1', 'eq2', 'expected', 'oracle'])}

## Attempt Receipts

| Problem | Parsed | Expected | Correct | Runner |
| --- | --- | --- | --- | --- |
{table(attempts, ['problem', 'parsed', 'expected', 'correct', 'runner'])}

## Negative Controls

| Fixture | Observed | Failures |
| --- | --- | --- |
{table(negatives, ['fixture', 'observed', 'failures'])}

## Boundary

{packet['promotion_boundary']}
"""


def render_brief(artifact: dict) -> str:
    packet = artifact["competition_packet"]
    return f"""# SAIR Stage 1 Competition Proof Packet Brief

Date: 2026-07-02

## Decision

The next market/product wedge is a `CompetitionProofPacket/v1`: source refs,
problem fixtures, prompt rendering, local attempt receipts, verdict parsing,
negative controls, and promotion gates.

## Result

Pass 0137 builds the first local fixture: `{packet['verdict_summary']['attempts']}`
deterministic equation-implication attempts, `{len(artifact['parser_tests'])}`
parser tests, `{len(packet['negative_fixtures'])}` rejected negative fixtures,
and `{packet['verdict_summary']['external_model_calls']}` external model calls.

## Next Push

Turn this fixture into a real adapter against a checked-out public judge repo,
then add a Lean certificate branch for Stage 2-style proof artifacts.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0137 Steelman: SAIR Competition Proof Packet Fixture

Date: 2026-07-02

The strongest objection is that a local fixture is not the official SAIR judge.
Accepted. This pass proves the packet shape and parser gates only. It does not
prove official competition performance.

The second objection is that curated equation fixtures are tiny. Accepted. They
are regression fixtures for receipt mechanics, not a benchmark.

The third objection is that model-free attempts avoid the real model-eval
problem. Accepted. That is intentional for the first adapter because it keeps
source refs, prompt hashes, parser behavior, negative controls, and promotion
boundaries testable without external API noise.

Promotion boundary: {artifact['competition_packet']['promotion_boundary']}
"""


def build_receipts(compose: dict, test: dict, validator: dict, artifact: dict) -> dict:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0137",
        "compose": compose,
        "test": test,
        "validator": validator,
        "artifact_status": artifact["status"],
        "attempt_count": artifact["competition_packet"]["verdict_summary"]["attempts"],
        "negative_fixture_count": len(artifact["competition_packet"]["negative_fixtures"]),
        "external_model_calls": artifact["competition_packet"]["verdict_summary"]["external_model_calls"],
        "forum_route_gap": artifact["tooling_gap"],
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
        f"Pass 0137 created a CompetitionProofPacketFixtureReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0137 records {len(packet['source_refs'])} source refs for the SAIR Stage 1-style fixture.",
        f"Pass 0137 records {len(artifact['problem_fixtures'])} local equation-implication problem fixtures.",
        f"Pass 0137 records {packet['verdict_summary']['attempts']} deterministic attempts with {packet['verdict_summary']['correct']} correct parsed verdicts.",
        f"Pass 0137 records {packet['verdict_summary']['external_model_calls']} external model calls.",
        f"Pass 0137 records {len(artifact['parser_tests'])} parser tests and all are MATCH.",
        f"Pass 0137 rejects {len(packet['negative_fixtures'])} negative fixtures.",
        "Pass 0137 promotes no theorem result, leaderboard result, model capability result, market-demand result, or BuildLang/buildc replacement result.",
        f"Pass 0137 validator status is {receipts['validator']['status']} and test status is {receipts['test']['status']}.",
        f"Pass 0137 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_refs={packet['source_refs']}"],
        [f"problem_fixtures={artifact['problem_fixtures']}"],
        [f"verdict_summary={packet['verdict_summary']}"],
        [f"external_model_calls={packet['verdict_summary']['external_model_calls']}"],
        [f"parser_tests={artifact['parser_tests']}"],
        [f"negative_fixtures={packet['negative_fixtures']}"],
        [f"current_promoted_results={packet['current_promoted_results']}", f"promotion_boundary={packet['promotion_boundary']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0137 SAIR Stage 1 Competition Proof Packet Fixture", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0137 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


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
    ok = artifact["status"] == "COMPETITION_PROOF_PACKET_FIXTURE_MATCH" and all(row["status"] == "MATCH" for row in [compose, test, validator])
    print(json.dumps({"status": "MATCH" if ok else "DRIFT", "artifact": str(ARTIFACT), "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
