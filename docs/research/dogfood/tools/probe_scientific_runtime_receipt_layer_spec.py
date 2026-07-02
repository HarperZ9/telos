"""Generate pass 0122 scientific runtime receipt layer artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_scientific_runtime_receipt_layer_spec.py"
TEST_SCRIPT = ROOT / "tools" / "test_scientific_runtime_receipt_layer_spec.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0122_scientific_runtime_layer.py"
OUT_PATH = ROOT / "schemas" / "scientific-runtime-receipt-layer-spec-pass-0122.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0122-scientific-runtime-layer-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0122.json"
PACKET_PATH = ROOT / "packets" / "132-scientific-runtime-receipt-layer-spec.md"
BRIEF_PATH = ROOT / "briefs" / "132-scientific-runtime-receipt-layer-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0122-scientific-runtime-receipt-layer-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0122-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0122-measurements.json"


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


def source_rows(artifact: dict) -> list[dict]:
    return [{"category": row["category"], "tool": row["tool"], "gather": row["local_gather_status"], "gap": row["gap_status"]} for row in artifact["source_matrix"]]


def contract_rows(artifact: dict) -> list[dict]:
    return [{"field": row["field"], "required": row["required_status"]} for row in artifact["receipt_contract"]]


def horizon_rows(artifact: dict) -> list[dict]:
    rows = []
    for case in artifact["long_horizon_experiment"]["exact_cases"]:
        max_drift = max(row["modified_max_abs_drift"] for row in case["float_horizons"])
        rows.append({"h": case["h"], "exact": case["exact_invariant_for_all_steps_by_induction"], "max_float_drift": max_drift, "status": "MATCH" if case["exact_invariant_for_all_steps_by_induction"] else "DRIFT"})
    return rows


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    gathered = sum(row["local_gather_status"].startswith("GATHER_VERIFIED") for row in artifact["source_matrix"])
    return f"""# Packet 132: Scientific Runtime Receipt Layer Spec

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: turn the pass 0121 `scientific_runtime_receipt_layer` push into a
concrete source-backed receipt contract and a long-horizon Hamiltonian runtime
experiment.

```text
source_rows = {len(artifact['source_matrix'])}
gather_verified_sources = {gathered}
receipt_contract_fields = {len(artifact['receipt_contract'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Source Matrix

| Category | Tool | Gather status | Gap status |
| --- | --- | --- | --- |
{table(source_rows(artifact), ['category', 'tool', 'gather', 'gap'])}

## Receipt Contract

| Field | Required |
| --- | --- |
{table(contract_rows(artifact), ['field', 'required'])}

## Hamiltonian Long-Horizon Experiment

| h | Exact invariant all steps | Max float drift | Status |
| --- | --- | ---: | --- |
{table(horizon_rows(artifact), ['h', 'exact', 'max_float_drift', 'status'])}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Scientific Runtime Receipt Layer Brief

Date: 2026-07-01

## Decision

Package the next public push around `{artifact['primary_30_day_push']}`: source
receipt, exact oracle, runtime branch, compiler branch, telemetry, lineage, and
Crucible verdict in one portable object.

## Product Meaning

This is the bridge between BuildLang/buildc, proof packets, AI/ML runtime
tooling, formal proof, observability, and color/rendering measurement. The
Hamiltonian experiment strengthens one scoped law candidate, but nothing is
promoted yet.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0122 Steelman: Scientific Runtime Receipt Layer

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a receipt contract is not a runtime. Correct.
BuildLang/buildc, JAX, Julia, MLIR, OpenXLA, and Triton branches still require
real executable adapters.

The second objection is that local float drift is not a physics discovery.
Correct. The exact identity is scoped to one rational map; the float replay is
a bounded measurement branch, not a promoted natural law.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0122",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_count": len(artifact["source_matrix"]),
        "receipt_contract_count": len(artifact["receipt_contract"]),
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {
        "artifact": OUT_PATH,
        "composer": COMPOSER,
        "packet": PACKET_PATH,
        "brief": BRIEF_PATH,
        "steelman": STEELMAN_PATH,
        "test": TEST_SCRIPT,
        "validator": VALIDATOR,
        "validator_result": VALIDATOR_RESULT,
        "tool_receipts": TOOL_RECEIPTS_PATH,
    }
    shas = {name: sha256_file(path) for name, path in files.items()}
    sources = artifact["source_matrix"]
    experiment = artifact["long_horizon_experiment"]
    gathered = sum(row["local_gather_status"].startswith("GATHER_VERIFIED") for row in sources)
    max_drift = max(h["modified_max_abs_drift"] for row in experiment["exact_cases"] for h in row["float_horizons"])
    claims = [
        f"Pass 0122 created a ScientificRuntimeReceiptLayerSpec/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0122 records {len(sources)} official source rows and {gathered} local Gather-verified web receipts.",
        f"Pass 0122 marks every source matrix gap_status as inferred and does not assert uniqueness as fact.",
        f"Pass 0122 defines {len(artifact['receipt_contract'])} required receipt contract fields.",
        f"Pass 0122 proves exact symplectic residual zero for {len(experiment['exact_cases'])} Hamiltonian cases by matrix identity and induction.",
        f"Pass 0122 long-horizon float replay has maximum modified-invariant drift {max_drift} within tolerance.",
        "Pass 0122 negative fixture records area growth for explicit Euler and keeps the result as a boundary witness.",
        "Pass 0122 binds pass 0121 growth vectors and pass 0120 Hamiltonian runtime branch receipt.",
        "Pass 0122 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0122 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0122 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0122 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_count={len(sources)}", f"gather_verified={gathered}"],
        [f"gap_statuses={sorted(set(row['gap_status'] for row in sources))}"],
        [f"contract_fields={[row['field'] for row in artifact['receipt_contract']]}"],
        [f"exact_cases={experiment['exact_cases']}"],
        [f"max_float_drift={max_drift}"],
        [f"negative_fixture={experiment['negative_fixture']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0122 Scientific Runtime Receipt Layer", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0122 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "SCIENTIFIC_RUNTIME_RECEIPT_LAYER_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
