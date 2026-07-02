"""Validate pass 0089 external solver adapter receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "external-solver-adapter-receipt-pass-0089.json"
RESULT = ROOT / "schemas" / "pass-0089-external-solver-adapter-receipt-validator-result.json"


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
    deps = artifact.get("dependency_receipts", {})
    adapter = artifact.get("external_adapter", {})
    comparison = adapter.get("comparison_to_exact", {})
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != "ExternalSolverAdapterReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "EXTERNAL_SOLVER_ADAPTER_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("prior_binding", {}).get("source_pass") != "0088":
        errors.append("prior_binding")
    if artifact.get("upstream_research_binding", {}).get("dominant_cluster") != "enterprise_quantum_optimization":
        errors.append("upstream_research_binding")
    if not deps.get("scipy", {}).get("available") or not deps.get("numpy", {}).get("available"):
        errors.append("solver_dependencies")
    if deps.get("ortools", {}).get("available") is not False:
        errors.append("ortools_dependency_receipt")
    if adapter.get("adapter_status") != "MATCH" or adapter.get("run_count") != 16:
        errors.append("adapter_runs")
    if not adapter.get("runs_sha256") or not adapter.get("warnings_sha256"):
        errors.append("adapter_digests")
    if comparison.get("hit_exact_bits") is not True or comparison.get("exact_value_gap") != 0:
        errors.append("exact_comparison")
    if comparison.get("exact_hit_count", 0) <= 0:
        errors.append("exact_hit_count")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if any(boundary.get(key) for key in ["solver_superiority_claim", "quantum_hardware_claim", "quantum_advantage_claim", "new_natural_law_claim"]):
        errors.append("promotion_boundary")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0089ExternalSolverAdapterReceiptValidatorRun/v1",
        "pass": "0089",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "ExternalSolverAdapterReceipt",
            "errors": errors,
            "path": "schemas/external-solver-adapter-receipt-pass-0089.json",
            "adapter": adapter.get("adapter"),
            "run_count": adapter.get("run_count"),
            "exact_value_gap": comparison.get("exact_value_gap"),
            "exact_hit_count": comparison.get("exact_hit_count"),
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
