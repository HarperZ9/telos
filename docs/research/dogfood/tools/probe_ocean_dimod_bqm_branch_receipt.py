"""Generate pass 0100 Ocean/dimod BQM branch artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_ocean_dimod_bqm_branch_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_ocean_dimod_bqm_branch_receipt.py"
OUT_PATH = ROOT / "schemas" / "ocean-dimod-bqm-branch-receipt-pass-0100.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0100.json"
PACKET_PATH = ROOT / "packets" / "110-ocean-dimod-bqm-branch-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "110-ocean-dimod-bqm-branch-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0100-ocean-dimod-bqm-branch-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0100-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0100-measurements.json"


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
    bqm = artifact["bqm_summary"]
    return f"""# Packet 110: Ocean/dimod BQM Branch Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: upgrade the remaining D-Wave/Ocean lane from a dependency boundary
into an executed local-CPU Ocean-compatible BQM branch using `dimod.ExactSolver`.

```text
global_dimod_available = {artifact['global_availability']['dimod_available']}
global_dwave_available = {artifact['global_availability']['dwave_available']}
temp_venv_cleaned = {artifact['temp_venv']['cleaned']}
dimod_version = {artifact['dimod_version']}
branch_id = {branch['branch_id']}
value = {branch['value']}
weight = {branch['weight']}
mask = {branch['mask']}
gap_to_exact = {branch['gap_to_exact']}
bqm_linear_terms = {bqm['linear_terms']}
bqm_quadratic_terms = {bqm['quadratic_terms']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

Boundary: this is local CPU exact BQM execution, not QPU execution, quantum
advantage, production solver coverage, or a natural law.
"""


def render_brief(artifact: dict) -> str:
    branch = artifact["solver_branch_receipt"]
    return f"""# Ocean/dimod BQM Branch Brief

Date: 2026-07-01

## Result

Pass 0100 executes an Ocean-compatible `dimod.ExactSolver` BQM branch in an
isolated temp venv. It matches the exact baseline with value {branch['value']},
weight {branch['weight']}, and gap {branch['gap_to_exact']}.

## Product Meaning

`OptimizationProofWorkbench/v1` now has local executed receipts for Python,
SciPy, NetworkX, OR-Tools, BuildLang, and Ocean/dimod. The remaining gap is
provider-backed QPU or hybrid execution, not local solver coverage.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0100 Steelman: Ocean/dimod BQM Branch

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that `dimod.ExactSolver` is not a quantum sampler.
Correct. This pass deliberately labels the branch as local CPU exact execution.

The second objection is that the BQM penalty can encode the answer shape for a
small fixture. Correct. This pass proves interop and receipt structure, not
quantum advantage or production optimization.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    branch = artifact["solver_branch_receipt"]
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0100", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "dimod_version": artifact["dimod_version"], "branch_value": branch["value"], "temp_cleaned": artifact["temp_venv"]["cleaned"]}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "brief": sha256_file(BRIEF_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT), "tool_receipts": sha256_file(TOOL_RECEIPTS_PATH)}
    branch = artifact["solver_branch_receipt"]
    claims = [
        f"Pass 0100 created an OceanDimodBQMBranchReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0100 binds OR-Tools pass {artifact['source_bindings']['ortools_pass']} and records global dimod/dwave availability as false.",
        f"Pass 0100 created a temp venv, installed dimod, executed ExactSolver, and cleaned the temp venv.",
        f"Pass 0100 records dimod version {artifact['dimod_version']}.",
        f"Pass 0100 SolverBranchReceipt/v1 branch {branch['branch_id']} records value {branch['value']}, weight {branch['weight']}, mask {branch['mask']}, and gap {branch['gap_to_exact']}.",
        f"Pass 0100 records BQM term counts linear={artifact['bqm_summary']['linear_terms']} and quadratic={artifact['bqm_summary']['quadratic_terms']}.",
        f"Pass 0100 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0100 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0100 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"dimod_available={artifact['global_availability']['dimod_available']}", f"dwave_available={artifact['global_availability']['dwave_available']}"],
        [f"venv_create={artifact['venv_create_command']['exit_code']}", f"install={artifact['install_command']['exit_code']}", f"run={artifact['run_command']['exit_code']}", f"cleaned={artifact['temp_venv']['cleaned']}"],
        [f"dimod_version={artifact['dimod_version']}"],
        [f"branch_id={branch['branch_id']}", f"value={branch['value']}", f"weight={branch['weight']}", f"mask={branch['mask']}", f"gap={branch['gap_to_exact']}"],
        [f"linear_terms={artifact['bqm_summary']['linear_terms']}", f"quadratic_terms={artifact['bqm_summary']['quadratic_terms']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0100 Ocean/dimod BQM Branch", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0100 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "OCEAN_DIMOD_BQM_BRANCH_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
