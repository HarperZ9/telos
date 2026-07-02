"""Validate pass 0095 BuildLang native optimization kernel receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buildlang-native-optimization-kernel-receipt-pass-0095.json"
RESULT = ROOT / "schemas" / "pass-0095-buildlang-native-optimization-kernel-receipt-validator-result.json"


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
    output = artifact.get("run_output", {})
    receipt = artifact.get("check_receipt", {})
    if artifact.get("schema") != "BuildLangNativeOptimizationKernelReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "BUILDLANG_NATIVE_OPTIMIZATION_KERNEL_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("prior_workflow_binding", {}).get("source_pass") != "0094":
        errors.append("prior_binding")
    if output.get("best value") != 162 or output.get("best weight") != 29 or output.get("feasible count") != 1275:
        errors.append("run_output")
    if artifact.get("check_command", {}).get("exit_code") != 0 or artifact.get("verify_command", {}).get("exit_code") != 0 or artifact.get("run_command", {}).get("exit_code") != 0:
        errors.append("commands")
    if receipt.get("status") != "passed" or receipt.get("policy", {}).get("profile") != "console-only":
        errors.append("check_receipt")
    if artifact.get("verify_summary", {}).get("all_required_passed") is not True:
        errors.append("verify_summary")
    if len(artifact.get("measurements", [])) != 10 or any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0095BuildLangNativeOptimizationKernelValidatorRun/v1",
        "pass": "0095",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "BuildLangNativeOptimizationKernelReceipt",
            "errors": errors,
            "path": "schemas/buildlang-native-optimization-kernel-receipt-pass-0095.json",
            "best_value": output.get("best value"),
            "feasible_count": output.get("feasible count"),
            "receipt_status": receipt.get("status"),
            "status": status,
        }],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
