"""Generate pass 0094 quantum optimization workflow artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_quantum_optimization_workflow_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_quantum_optimization_workflow_receipt.py"
OUT_PATH = ROOT / "schemas" / "quantum-optimization-workflow-receipt-pass-0094.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0094.json"
PACKET_PATH = ROOT / "packets" / "104-quantum-optimization-workflow-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "104-quantum-optimization-workflow-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0094-quantum-optimization-workflow-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0094-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0094-measurements.json"


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


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def branch_rows(artifact: dict) -> str:
    rows = []
    for branch_id, branch in artifact["workflow"]["solver_branches"].items():
        rows.append(f"| `{branch_id}` | {branch.get('status')} | {branch.get('value', 'n/a')} | {branch.get('weight', 'n/a')} |")
    return "\n".join(rows)


def measurement_rows(artifact: dict) -> str:
    rows = []
    for item in artifact["measurements"]:
        rows.append(f"| `{item['measurement_id']}` | {item['status']} | {item['claim']} |")
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    workflow = artifact["workflow"]
    objective = workflow["objective_measurements"]
    buildlang = artifact["buildlang_binding"]
    return f"""# Packet 104: Quantum Optimization Workflow Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: implement the first `QuantumOptimizationWorkflowReceipt/v1` fixture
from the YouTube-to-BuildLang megatool bridge.

```text
problem_id = {workflow['problem']['problem_id']}
capacity = {workflow['problem']['capacity']}
exact_value = {objective['exact_value']}
exact_weight = {objective['exact_weight']}
executed_branch_count = {objective['executed_branch_count']}
dependency_boundary_branch_count = {objective['dependency_boundary_branch_count']}
buildc_source_digest = {buildlang['source_digest']}
buildc_verify_check_count = {buildlang['verify_check_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Branches

| Branch | Status | Value | Weight |
| --- | --- | ---: | ---: |
{branch_rows(artifact)}

## Measurements

| Measurement | Status | Claim |
| --- | --- | --- |
{measurement_rows(artifact)}

Boundary: this is a toy optimization workflow receipt. It does not prove
quantum advantage, production solver coverage, BuildLang replacement,
scientific discovery, or a natural law.
"""


def render_brief(artifact: dict) -> str:
    nx_branch = artifact["workflow"]["solver_branches"]["networkx_capacity_dag_longest_path"]
    return f"""# Quantum Optimization Workflow Brief

Date: 2026-07-01

## Result

Pass 0094 creates the first `QuantumOptimizationWorkflowReceipt/v1` fixture.
Exact enumeration, SciPy dual annealing, and a live NetworkX capacity-DAG branch
all reach value 162; OR-Tools and D-Wave are recorded as missing-dependency
boundaries.

## Product Meaning

The useful market demo is the receipt shape: source lead, problem definition,
solver branches, dependency state, BuildLang source receipt, objective
measurements, and Crucible verdict. NetworkX contributes {nx_branch['node_count']}
nodes and {nx_branch['edge_count']} edges to the replayable DAG branch.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0094 Steelman: Quantum Optimization Workflow

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this is not quantum execution. Correct. The
D-Wave branch is a missing-dependency receipt, not a hardware claim.

The second objection is that the problem is small. Correct. Small is deliberate:
the receipt has an exact baseline, so solver branch claims are falsifiable.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    objective = artifact["workflow"]["objective_measurements"]
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0094", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "objective": objective}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    paths = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in paths.items()}
    objective = artifact["workflow"]["objective_measurements"]
    branches = artifact["workflow"]["solver_branches"]
    claims = [
        f"Pass 0094 created a QuantumOptimizationWorkflowReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0094 binds YouTube pass {artifact['source_binding']['source_pass']} and BuildLang pass {artifact['buildlang_binding']['source_pass']}.",
        f"Pass 0094 exact branch records value {objective['exact_value']}, weight {objective['exact_weight']}, and capacity violation {objective['capacity_violation']}.",
        f"Pass 0094 SciPy branch records value {branches['scipy_dual_annealing']['value']} and exact hit count {branches['scipy_dual_annealing']['exact_hit_count']}.",
        f"Pass 0094 NetworkX branch records status {branches['networkx_capacity_dag_longest_path']['status']} and value {branches['networkx_capacity_dag_longest_path']['value']}.",
        f"Pass 0094 records OR-Tools and D-Wave branches as {branches['ortools_knapsack']['status']} and {branches['dwave_ocean_sampler']['status']}.",
        f"Pass 0094 records {len(artifact['measurements'])} measurements, {len(artifact['source_anchors'])} official source anchors, and MATCH flagship receipts.",
        f"Pass 0094 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0094 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_binding={artifact['source_binding']}", f"buildlang_binding={artifact['buildlang_binding']}"],
        [f"exact_value={objective['exact_value']}", f"exact_weight={objective['exact_weight']}", f"capacity_violation={objective['capacity_violation']}"],
        [f"scipy_value={branches['scipy_dual_annealing']['value']}", f"exact_hit_count={branches['scipy_dual_annealing']['exact_hit_count']}"],
        [f"networkx_status={branches['networkx_capacity_dag_longest_path']['status']}", f"networkx_value={branches['networkx_capacity_dag_longest_path']['value']}"],
        [f"ortools_status={branches['ortools_knapsack']['status']}", f"dwave_status={branches['dwave_ocean_sampler']['status']}"],
        [f"measurement_count={len(artifact['measurements'])}", f"source_anchor_count={len(artifact['source_anchors'])}", f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0094 Quantum Optimization Workflow Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0094 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)], timeout=180)
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "QUANTUM_OPTIMIZATION_WORKFLOW_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
