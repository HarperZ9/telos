"""Validate pass 0097 BuildLang optimization proof workbench receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buildlang-optimization-proof-workbench-receipt-pass-0097.json"
RESULT = ROOT / "schemas" / "pass-0097-buildlang-optimization-proof-workbench-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    out = artifact.get("run_output", {})
    if artifact.get("schema") != "BuildLangOptimizationProofWorkbenchReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "BUILDLANG_OPTIMIZATION_PROOF_WORKBENCH_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("scorecard_pass") != "0096":
        errors.append("source_binding")
    if artifact.get("check_command", {}).get("exit_code") != 0 or artifact.get("verify_command", {}).get("exit_code") != 0 or artifact.get("run_command", {}).get("exit_code") != 0:
        errors.append("commands")
    expected = {"exact value": 162, "exact weight": 29, "exact mask": 2347, "exact feasible": 1275, "greedy value": 146, "greedy weight": 25, "greedy mask": 2331, "bounded value": 157, "bounded weight": 27, "bounded mask": 299, "bounded feasible": 704}
    if any(out.get(key) != value for key, value in expected.items()):
        errors.append("run_output")
    if artifact.get("verify_summary", {}).get("check_count") != 18 or artifact.get("verify_summary", {}).get("failed_checks") != []:
        errors.append("verify_summary")
    if artifact.get("comparison_summary", {}).get("greedy_gap") != 16 or artifact.get("comparison_summary", {}).get("bounded_gap") != 5:
        errors.append("branch_gaps")
    if len(artifact.get("branches", [])) != 3 or len(artifact.get("measurements", [])) != 8:
        errors.append("branch_or_measurement_count")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0097BuildLangOptimizationProofWorkbenchValidatorRun/v1",
        "pass": "0097",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{"artifact": "BuildLangOptimizationProofWorkbenchReceipt", "errors": errors, "path": "schemas/buildlang-optimization-proof-workbench-receipt-pass-0097.json", "exact_value": out.get("exact value"), "greedy_gap": artifact.get("comparison_summary", {}).get("greedy_gap"), "bounded_gap": artifact.get("comparison_summary", {}).get("bounded_gap"), "status": status}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
