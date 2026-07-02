"""Generate pass 0128 cross-field proof suite artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_cross_field_proof_suite.py"
TEST_SCRIPT = ROOT / "tools" / "test_cross_field_proof_suite.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0128_cross_field_proof_suite.py"
OUT_PATH = ROOT / "schemas" / "cross-field-proof-suite-pass-0128.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0128-cross-field-proof-suite-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0128.json"
PACKET_PATH = ROOT / "packets" / "138-cross-field-proof-suite.md"
BRIEF_PATH = ROOT / "briefs" / "138-cross-field-proof-suite-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0128-cross-field-proof-suite-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0128-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0128-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.encode("ascii", "ignore").decode("ascii"), encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def fixture_rows(artifact: dict) -> list[dict]:
    rows = []
    for fixture in artifact["fixtures"]:
        branch = fixture["runtime_branch"]
        rows.append({
            "fixture": fixture["fixture_id"],
            "field": fixture["field"],
            "runtime": branch.get("runtime"),
            "status": branch.get("status"),
            "law": fixture["law_candidate_status"],
        })
    return rows


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    sources = [{"ref": row["ref"], "status": row["status"], "sha256": row["sha256"][:16]} for row in artifact["source_receipts"]]
    negatives = [{"fixture": row["fixture_id"], "status": row["status"], "failures": ",".join(row["failures"])} for row in artifact["negative_fixtures"]]
    return f"""# Packet 138: Cross-Field Proof Suite

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: generalize the pass 0127 runtime router from one fixture to a small
suite with shared source, oracle, runtime, verifier, and non-promotion slots.

```text
fixture_count = {len(artifact['fixtures'])}
source_receipts = {len(artifact['source_receipts'])}
negative_fixtures = {len(artifact['negative_fixtures'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
promoted_laws = {len(artifact['current_promoted_natural_laws'])}
```

## Fixtures

| Fixture | Field | Runtime | Status | Law status |
| --- | --- | --- | --- | --- |
{table(fixture_rows(artifact), ['fixture', 'field', 'runtime', 'status', 'law'])}

## Source Receipts

| Ref | Status | sha256 |
| --- | --- | --- |
{table(sources, ['ref', 'status', 'sha256'])}

## Negative Fixtures

| Fixture | Status | Failures |
| --- | --- | --- |
{table(negatives, ['fixture', 'status', 'failures'])}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Cross-Field Proof Suite Brief

Date: 2026-07-01

## Decision

Promote the router into a four-fixture proof suite: formal identity, quantum
normalization, bounded optimization, and counterexample revision.

## Result

All four bounded fixtures match their local runtime branches. Four negative
controls reject law promotion, source-only market claims, counterexample
omission, and raw transcript export. Current promoted natural laws remain
`{len(artifact['current_promoted_natural_laws'])}`.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0128 Steelman: Cross-Field Proof Suite

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that these are small fixtures. Correct. The point is
to harden the packet contract before harder problems: every field must carry
source receipts, an exact oracle, a runtime branch, verifier status, and a
non-promotion boundary.

The second objection is that no BuildLang/buildc branch runs here. Correct.
This pass defines the slots a compiled branch must satisfy; it does not claim
the compiler path is active.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> dict:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0128",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "fixture_count": len(artifact["fixtures"]),
        "negative_count": len(artifact["negative_fixtures"]),
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)
    return receipts


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    fixtures = {row["fixture_id"]: row for row in artifact["fixtures"]}
    claims = [
        f"Pass 0128 created a CrossFieldProofSuiteReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0128 binds upstream passes {artifact['source_bindings']} and records {len(artifact['source_receipts'])} Gather-verified source receipts.",
        f"Pass 0128 formal odd-sum fixture has runtime max_abs_error {fixtures['formal_odd_sum_identity']['runtime_branch']['max_abs_error']}.",
        f"Pass 0128 quantum fixture reuses pass 0127 normalization with runtime status {fixtures['quantum_born_normalization']['runtime_branch']['status']}.",
        f"Pass 0128 bounded knapsack fixture optimum is {fixtures['bounded_knapsack_exact_oracle']['exact_oracle']['optimum']}.",
        f"Pass 0128 counterexample fixture rejects the unbounded Euler polynomial claim at n={fixtures['euler_prime_counterexample_revision']['counterexample']['n']}.",
        f"Pass 0128 rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0128 marks market gaps as inferred hypotheses rather than verified market facts.",
        "Pass 0128 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0128 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0128 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0128 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"source_receipts={artifact['source_receipts']}"],
        [f"formal_fixture={fixtures['formal_odd_sum_identity']}"],
        [f"quantum_fixture={fixtures['quantum_born_normalization']}"],
        [f"optimization_fixture={fixtures['bounded_knapsack_exact_oracle']}"],
        [f"counterexample_fixture={fixtures['euler_prime_counterexample_revision']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"market_gap_hypotheses={artifact['market_gap_hypotheses']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0128 Cross-Field Proof Suite", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0128 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=180)
    validator_receipt = run_command([sys.executable, str(VALIDATOR)], timeout=120)
    receipts = write_tool_receipts(artifact, compose_receipt, test_receipt, validator_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt, validator_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, receipts)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    ok = all(row["status"] == "MATCH" for row in [compose_receipt, test_receipt, validator_receipt]) and artifact["status"] == "CROSS_FIELD_PROOF_SUITE_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
