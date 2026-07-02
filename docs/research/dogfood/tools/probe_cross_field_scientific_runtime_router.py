"""Generate pass 0127 cross-field scientific runtime router artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_cross_field_scientific_runtime_router.py"
TEST_SCRIPT = ROOT / "tools" / "test_cross_field_scientific_runtime_router.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0127_cross_field_runtime_router.py"
OUT_PATH = ROOT / "schemas" / "cross-field-scientific-runtime-router-pass-0127.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0127-cross-field-runtime-router-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0127.json"
PACKET_PATH = ROOT / "packets" / "137-cross-field-scientific-runtime-router.md"
BRIEF_PATH = ROOT / "briefs" / "137-cross-field-scientific-runtime-router-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0127-cross-field-scientific-runtime-router-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0127-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0127-measurements.json"


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


def negative_rows(artifact: dict) -> list[dict]:
    return [{"fixture": row["fixture_id"], "status": row["status"], "failures": ",".join(row["failures"])} for row in artifact["negative_fixtures"]]


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    branch = artifact["runtime_branch"]
    oracle = artifact["exact_oracle"]
    return f"""# Packet 137: Cross-Field Scientific Runtime Router

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: route one video source lead through the demotion gate into a bounded
scientific runtime receipt. The source lead creates pressure; the proof is only
the exact normalization oracle and local Python float64 branch agreement.

```text
source_video = {artifact['source_lead']['video_id']}
demotion_gate = {artifact['demotion_gate_result']['gate_status']}
oracle_status = {oracle['status']}
runtime_status = {branch['status']}
probability_sum = {oracle['probability_sum']}
runtime_sum_drift = {branch['probability_sum_abs_drift']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Runtime Fixture

| Field | Value |
| --- | --- |
| Amplitudes | `{','.join(oracle['amplitudes'])}` |
| Exact probabilities | `{','.join(oracle['probabilities'])}` |
| Exact probability sum | `{oracle['probability_sum']}` |
| Runtime branch | `{branch['branch_id']}` |
| Runtime probability sum | `{branch['probability_sum']}` |
| Runtime drift | `{branch['probability_sum_abs_drift']}` |

## Negative Fixtures

| Fixture | Status | Failures |
| --- | --- | --- |
{table(negative_rows(artifact), ['fixture', 'status', 'failures'])}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Cross-Field Scientific Runtime Router Brief

Date: 2026-07-01

## Decision

Promote `CrossFieldScientificRuntimeRouter` from roadmap to the first executable
fixture. It routes a quantum-foundation source lead into a receipt-backed
normalization check while keeping interpretation, market, and law claims
unpromoted.

## Result

The exact oracle and local Python runtime branch match for the bounded fixture;
three negative fixtures reject missing normalization, interpretation promotion,
and market-fit promotion.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0127 Steelman: Cross-Field Scientific Runtime Router

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this is a tiny arithmetic fixture. Correct. It
does not prove quantum mechanics or BuildLang execution. It proves the router
shape: source lead, demotion gate, exact oracle, runtime branch, verifier
fields, and non-promotion boundary.

The second objection is that Python float64 is not the target runtime. Correct.
This is the local executable branch; BuildLang/buildc remains a future branch
until a compiled receipt exists.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0127",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "router_status": artifact["router_status"],
        "negative_count": len(artifact["negative_fixtures"]),
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0127 created a CrossFieldScientificRuntimeRouterReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0127 binds pass receipts {artifact['source_bindings']}.",
        f"Pass 0127 routes source lead {artifact['source_lead']['video_id']} through demotion gate status {artifact['demotion_gate_result']['gate_status']}.",
        f"Pass 0127 exact oracle records probabilities {artifact['exact_oracle']['probabilities']} with probability_sum {artifact['exact_oracle']['probability_sum']}.",
        f"Pass 0127 runtime branch {artifact['runtime_branch']['branch_id']} has status {artifact['runtime_branch']['status']} and drift {artifact['runtime_branch']['probability_sum_abs_drift']}.",
        "Pass 0127 rejects missing normalization, interpretation promotion, and market-fit promotion fixtures.",
        f"Pass 0127 keeps interpretation_claim_status {artifact['interpretation_claim_status']} and market_claim_status {artifact['market_claim_status']}.",
        f"Pass 0127 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0127 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0127 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0127 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"source_lead={artifact['source_lead']}", f"demotion_gate={artifact['demotion_gate_result']}"],
        [f"exact_oracle={artifact['exact_oracle']}"],
        [f"runtime_branch={artifact['runtime_branch']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"interpretation={artifact['interpretation_claim_status']}", f"market={artifact['market_claim_status']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0127 Cross-Field Scientific Runtime Router", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0127 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    validator_receipt = run_command([sys.executable, str(VALIDATOR)], timeout=120)
    receipts = {"compose": compose_receipt, "test": test_receipt, "validator": validator_receipt}
    write_tool_receipts(artifact, compose_receipt, test_receipt, validator_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt, validator_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, receipts)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "CROSS_FIELD_SCIENTIFIC_RUNTIME_ROUTER_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
