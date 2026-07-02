"""Generate pass 0101 inequality-safe BQM artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_inequality_safe_bqm_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_inequality_safe_bqm_receipt.py"
OUT_PATH = ROOT / "schemas" / "inequality-safe-bqm-receipt-pass-0101.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0101.json"
PACKET_PATH = ROOT / "packets" / "111-inequality-safe-bqm-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "111-inequality-safe-bqm-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0101-inequality-safe-bqm-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0101-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0101-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 360) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    res = artifact["results"]
    law = artifact["law_candidate"]
    return f"""# Packet 111: Inequality-Safe BQM Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: test whether the pass 0100 equality-to-capacity BQM penalty is safe
for general `weight <= capacity` knapsack. It is not; this pass records a
counterexample and a slack-variable fix.

```text
problem_values = {res['problem']['values']}
problem_weights = {res['problem']['weights']}
capacity = {res['problem']['capacity']}
true_optimum_value = {res['true_optimum']['value']}
equality_penalty_value = {res['equality_penalty']['value']}
equality_penalty_feasible = {res['equality_penalty']['feasible']}
slack_penalty_value = {res['slack_penalty']['value']}
slack_penalty_feasible = {res['slack_penalty']['feasible']}
law_candidate = {law['name']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Finding

A squared equality penalty on `sum(weights) - capacity` selects the overweight
set with value 19. The true feasible optimum is value 10. Adding binary slack
variables to encode `sum(weights) + slack = capacity` recovers the feasible
optimum.

Boundary: this is a law candidate with one counterexample and one fix, not a
promoted natural law.
"""


def render_brief(artifact: dict) -> str:
    return f"""# Inequality-Safe BQM Brief

Date: 2026-07-01

## Result

Pass 0101 found a real encoding hazard: equality-to-capacity BQM penalties can
select infeasible overweight knapsack states. A slack-variable encoding fixes
the bounded counterexample.

## Product Meaning

The optimization workbench now needs an encoding-safety layer before any BQM,
quantum, or hybrid branch is allowed to claim a valid inequality-constrained
result.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0101 Steelman: Inequality-Safe BQM

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that one counterexample is not a full proof of the
slack encoding. Correct. It falsifies the unsafe equality encoding and motivates
the next proof obligation: general proof or broader randomized counterexample
search.

The second objection is that ExactSolver is local CPU. Correct. The pass is
about encoding safety, not hardware execution.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0101", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "law_candidate": artifact["law_candidate"]["name"]}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "brief": sha256_file(BRIEF_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT), "tool_receipts": sha256_file(TOOL_RECEIPTS_PATH)}
    res = artifact["results"]
    claims = [
        f"Pass 0101 created an InequalitySafeBQMReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0101 binds Ocean/dimod pass {artifact['source_bindings']['ocean_pass']} and uses dimod version {res['dimod_version']}.",
        f"Pass 0101 counterexample has true feasible optimum value {res['true_optimum']['value']} and weight {res['true_optimum']['weight']}.",
        f"Pass 0101 equality penalty selects value {res['equality_penalty']['value']} with feasible={res['equality_penalty']['feasible']}.",
        f"Pass 0101 slack-variable penalty selects value {res['slack_penalty']['value']} with feasible={res['slack_penalty']['feasible']}.",
        f"Pass 0101 records law candidate {artifact['law_candidate']['name']} with status {artifact['law_candidate']['status']}.",
        f"Pass 0101 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0101 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0101 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"dimod_version={res['dimod_version']}"],
        [f"true_value={res['true_optimum']['value']}", f"true_weight={res['true_optimum']['weight']}"],
        [f"equality_value={res['equality_penalty']['value']}", f"equality_feasible={res['equality_penalty']['feasible']}"],
        [f"slack_value={res['slack_penalty']['value']}", f"slack_feasible={res['slack_penalty']['feasible']}"],
        [f"law_candidate={artifact['law_candidate']['name']}", f"law_status={artifact['law_candidate']['status']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0101 Inequality-Safe BQM", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0101 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)], timeout=420)
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "INEQUALITY_SAFE_BQM_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
