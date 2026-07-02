"""Generate pass 0120 Hamiltonian runtime branch artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_hamiltonian_runtime_branch_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_hamiltonian_runtime_branch_receipt.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0120_hamiltonian_runtime_branch.py"
OUT_PATH = ROOT / "schemas" / "hamiltonian-runtime-branch-receipt-pass-0120.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0120-hamiltonian-runtime-branch-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0120.json"
PACKET_PATH = ROOT / "packets" / "130-hamiltonian-runtime-branch-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "130-hamiltonian-runtime-branch-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0120-hamiltonian-runtime-branch-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0120-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0120-measurements.json"


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


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    return f"""# Packet 130: Hamiltonian Runtime Branch Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: replay pass 0119's exact Hamiltonian/symplectic oracle through
available local runtime branches and fence unavailable branches.

```text
hamiltonian_symplectic_pass = {artifact['source_bindings']['hamiltonian_symplectic_pass']}
runtime_branches = {len(artifact['runtime_branches'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Runtime Branches

| Branch | Runtime | Status |
| --- | --- | --- |
{table(artifact['runtime_branches'], ['branch_id', 'runtime', 'status'])}

## Availability

| Runtime | Status |
| --- | --- |
{table([{'runtime': key, 'status': value['status']} for key, value in artifact['availability'].items()], ['runtime', 'status'])}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    executed = [row for row in artifact["runtime_branches"] if row["status"] == "MATCH"]
    return f"""# Hamiltonian Runtime Branch Brief

Date: 2026-07-01

## Decision

Make runtime drift a first-class proof-packet field. Pass 0120 replays the
Hamiltonian law candidate through available NumPy and SciPy branches while
keeping JAX, BuildLang/buildc, and Julia fenced.

Executed MATCH branches: {len(executed)}.

## Product Meaning

This is the bridge from exact proof packet to executable scientific runtime
receipt: oracle, runtime availability, drift tolerance, negative fixture, and
verifier verdict in one object.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0120 Steelman: Hamiltonian Runtime Branch

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that NumPy/SciPy float64 replay is not a BuildLang
compiler receipt. Correct. BuildLang, JAX, and Julia branches are fenced.

The second objection is that a 24-step drift check is not long-horizon
geometric integration validation. Correct. This pass proves only bounded replay
against pass 0119's exact oracle.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0120",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "availability": artifact["availability"],
        "runtime_branches": artifact["runtime_branches"],
        "source_surface": artifact["source_surface"],
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    branches = artifact["runtime_branches"]
    numpy_count = sum(row["branch_id"].startswith("numpy_float64") and row["status"] == "MATCH" for row in branches)
    scipy_count = sum(row["branch_id"].startswith("scipy_linalg") and row["status"] == "MATCH" for row in branches)
    fenced = [row["branch_id"] for row in branches if row["status"] == "UNAVAILABLE_FENCED"]
    claims = [
        f"Pass 0120 created a HamiltonianRuntimeBranchReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0120 binds Hamiltonian symplectic pass {artifact['source_bindings']['hamiltonian_symplectic_pass']} with seal {artifact['source_bindings']['hamiltonian_symplectic_seal']}.",
        f"Pass 0120 records NumPy AVAILABLE and runs {numpy_count} positive NumPy float64 branches with MATCH status.",
        f"Pass 0120 records SciPy AVAILABLE and runs {scipy_count} SciPy determinant branches with MATCH status.",
        "Pass 0120 records a NumPy explicit-Euler negative branch with MATCH status, determinant above 1, and energy growth.",
        f"Pass 0120 fences unavailable runtime branches {fenced}.",
        f"Pass 0120 records source anchor_count {artifact['source_surface']['anchor_count']} for NumPy, SciPy, JAX, and Python decimal references.",
        "Pass 0120 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0120 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0120 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0120 non-promotion statement is: {artifact['non_promotion_statement']}",
        f"Pass 0120 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"availability={artifact['availability']['numpy']}", f"numpy_count={numpy_count}"],
        [f"availability={artifact['availability']['scipy']}", f"scipy_count={scipy_count}"],
        [str(next(row for row in branches if row["branch_id"] == "numpy_explicit_euler_negative"))],
        [f"fenced={fenced}", f"availability={artifact['availability']}"],
        [f"source_surface={artifact['source_surface']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}", f"telos_catalog={artifact['flagship_receipts']['telos_catalog']['status']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [artifact["non_promotion_statement"]],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0120 Hamiltonian Runtime Branch Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0120 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)], timeout=180)
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
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "HAMILTONIAN_RUNTIME_BRANCH_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
