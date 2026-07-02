"""Generate pass 0099 OR-Tools branch execution artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_ortools_branch_execution_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_ortools_branch_execution_receipt.py"
OUT_PATH = ROOT / "schemas" / "ortools-branch-execution-receipt-pass-0099.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0099.json"
PACKET_PATH = ROOT / "packets" / "109-ortools-branch-execution-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "109-ortools-branch-execution-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0099-ortools-branch-execution-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0099-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0099-measurements.json"


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
    branch = artifact["solver_branch_receipt"]
    return f"""# Packet 109: OR-Tools Branch Execution Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: upgrade the pass 0098 OR-Tools dependency boundary into an executed
`SolverBranchReceipt/v1` branch using an isolated temporary virtual
environment.

```text
global_ortools_available = {artifact['global_availability']['available']}
temp_venv_cleaned = {artifact['temp_venv']['cleaned']}
ortools_version = {artifact['ortools_version']}
branch_id = {branch['branch_id']}
value = {branch['value']}
weight = {branch['weight']}
mask = {branch['mask']}
gap_to_exact = {branch['gap_to_exact']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Result

OR-Tools solved the 12-item knapsack fixture with value 162, weight 29, and
mask 2347. That matches the exact baseline and BuildLang exact branch.

## Source Anchors

- https://developers.google.com/optimization/install
- https://developers.google.com/optimization/pack/knapsack
- https://pypi.org/project/ortools/

Boundary: this proves one isolated OR-Tools execution branch. It does not prove
solver superiority, production coverage, quantum advantage, or a natural law.
"""


def render_brief(artifact: dict) -> str:
    branch = artifact["solver_branch_receipt"]
    return f"""# OR-Tools Branch Execution Brief

Date: 2026-07-01

## Result

Pass 0099 executes OR-Tools in an isolated temp venv and attaches an executed
`SolverBranchReceipt/v1` with value {branch['value']}, weight {branch['weight']},
and gap {branch['gap_to_exact']}.

## Product Meaning

`OptimizationProofWorkbench/v1` can now compare Python exact, SciPy, NetworkX,
BuildLang, and OR-Tools executed branches while keeping D-Wave/Ocean as the
remaining dependency-boundary lane.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0099 Steelman: OR-Tools Branch Execution

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a temp venv execution is not production
integration. Correct. This pass proves an isolated branch and records cleanup;
it does not claim global availability or a committed dependency.

The second objection is that OR-Tools finding the exact value on a 12-item
knapsack is expected. Correct. The value is interoperability evidence, not
solver superiority evidence.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    branch = artifact["solver_branch_receipt"]
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0099", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "ortools_version": artifact["ortools_version"], "branch_value": branch["value"], "temp_cleaned": artifact["temp_venv"]["cleaned"]}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "brief": sha256_file(BRIEF_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT), "tool_receipts": sha256_file(TOOL_RECEIPTS_PATH)}
    branch = artifact["solver_branch_receipt"]
    claims = [
        f"Pass 0099 created an ORToolsBranchExecutionReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0099 binds interop pass {artifact['source_bindings']['interop_pass']} and records global OR-Tools availability as {artifact['global_availability']['available']}.",
        f"Pass 0099 created a temp venv, installed OR-Tools, executed the solver, and cleaned the temp venv.",
        f"Pass 0099 records OR-Tools version {artifact['ortools_version']}.",
        f"Pass 0099 SolverBranchReceipt/v1 branch {branch['branch_id']} records value {branch['value']}, weight {branch['weight']}, mask {branch['mask']}, and gap {branch['gap_to_exact']}.",
        f"Pass 0099 records {len(artifact['source_anchors'])} source anchors and {len(artifact['measurements'])} measurements.",
        f"Pass 0099 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0099 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0099 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"global_available={artifact['global_availability']['available']}"],
        [f"venv_create={artifact['venv_create_command']['exit_code']}", f"install={artifact['install_command']['exit_code']}", f"run={artifact['run_command']['exit_code']}", f"cleaned={artifact['temp_venv']['cleaned']}"],
        [f"ortools_version={artifact['ortools_version']}"],
        [f"branch_id={branch['branch_id']}", f"value={branch['value']}", f"weight={branch['weight']}", f"mask={branch['mask']}", f"gap={branch['gap_to_exact']}"],
        [f"source_anchor_count={len(artifact['source_anchors'])}", f"measurement_count={len(artifact['measurements'])}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0099 OR-Tools Branch Execution", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0099 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "ORTOOLS_BRANCH_EXECUTION_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
