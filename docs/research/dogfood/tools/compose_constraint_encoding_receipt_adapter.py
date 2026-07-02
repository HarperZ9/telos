"""Compose pass 0103 constraint-encoding receipt adapter."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "ConstraintEncodingReceiptAdapter/v1"
PASS_ID = "0103"
STATUS_MATCH = "CONSTRAINT_ENCODING_RECEIPT_ADAPTER_MATCH"
STATUS_DRIFT = "CONSTRAINT_ENCODING_RECEIPT_ADAPTER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
INTEROP = ROOT / "schemas" / "solver-branch-receipt-interop-schema-pass-0098.json"
ORTOOLS = ROOT / "schemas" / "ortools-branch-execution-receipt-pass-0099.json"
OCEAN = ROOT / "schemas" / "ocean-dimod-bqm-branch-receipt-pass-0100.json"
INEQUALITY = ROOT / "schemas" / "inequality-safe-bqm-receipt-pass-0101.json"
ROADMAP = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def merged_branches(interop: dict[str, Any], ortools: dict[str, Any], ocean: dict[str, Any]) -> list[dict[str, Any]]:
    branches = []
    for row in interop["branch_receipts"]:
        if row["branch_id"] in {"ortools_knapsack", "dwave_ocean_sampler"}:
            row = dict(row)
            row["adapter_status"] = "SUPERSEDED_BY_EXECUTED_BRANCH"
        branches.append(row)
    branches.append(ortools["solver_branch_receipt"])
    branches.append(ocean["solver_branch_receipt"])
    return branches


def encoding_method(branch_id: str, method: str) -> dict[str, Any]:
    lower = f"{branch_id} {method}".lower()
    if "ocean_dimod_exact_bqm" in lower:
        return {
            "encoding_method": "bqm_equality_penalty_to_capacity",
            "encoding_safety": "UNSAFE_WITHOUT_SLACK_OR_INEQUALITY_RECEIPT",
            "requires_counterexample_fixture": True,
        }
    if "dwave_ocean_sampler" in lower:
        return {"encoding_method": "provider_boundary_unknown", "encoding_safety": "UNVERIFIABLE_UNTIL_EXECUTED", "requires_counterexample_fixture": True}
    if "ortools" in lower:
        return {"encoding_method": "solver_native_knapsack_capacity", "encoding_safety": "MATCH", "requires_counterexample_fixture": False}
    if "networkx" in lower or "dag" in lower:
        return {"encoding_method": "capacity_state_graph", "encoding_safety": "MATCH", "requires_counterexample_fixture": False}
    if "enumeration" in lower or "greedy" in lower or "bounded" in lower or "scipy" in lower:
        return {"encoding_method": "explicit_feasibility_filter", "encoding_safety": "MATCH", "requires_counterexample_fixture": False}
    return {"encoding_method": "unknown", "encoding_safety": "UNVERIFIABLE", "requires_counterexample_fixture": True}


def branch_encoding_receipt(branch: dict[str, Any], capacity: int, inequality: dict[str, Any]) -> dict[str, Any]:
    value = branch.get("value")
    weight = branch.get("weight")
    method = encoding_method(branch["branch_id"], branch.get("method", ""))
    executable = str(branch.get("execution_status", "")).startswith("EXECUTED")
    feasible = isinstance(weight, int) and weight <= capacity
    boundary = branch.get("adapter_status") == "SUPERSEDED_BY_EXECUTED_BRANCH" or branch.get("execution_status", "").startswith("NOT_EXECUTED")
    status = "MATCH"
    if boundary:
        status = "BOUNDARY_ONLY"
    if method["encoding_safety"] != "MATCH" and executable:
        status = "MATCH_WITH_PROMOTION_BLOCK"
    return {
        "schema": "ConstraintEncodingReceipt/v1",
        "branch_id": branch["branch_id"],
        "origin_pass": branch.get("origin_pass"),
        "runtime": branch.get("runtime"),
        "execution_status": branch.get("execution_status"),
        "constraint_type": "knapsack_weight_le_capacity",
        "capacity": capacity,
        "value": value,
        "weight": weight,
        "feasible_under_capacity": feasible if executable else None,
        "feasibility_check": "weight <= capacity" if executable else "not_executed",
        "encoding_method": method["encoding_method"],
        "encoding_safety": method["encoding_safety"],
        "requires_counterexample_fixture": method["requires_counterexample_fixture"],
        "counterexample_ref": "schemas/inequality-safe-bqm-receipt-pass-0101.json",
        "law_candidate": inequality["law_candidate"]["name"],
        "promotion_blocked": method["encoding_safety"] != "MATCH",
        "adapter_status": status,
    }


def receipts(branches: list[dict[str, Any]], inequality: dict[str, Any]) -> list[dict[str, Any]]:
    return [branch_encoding_receipt(branch, 29, inequality) for branch in branches]


def coverage(rows: list[dict[str, Any]]) -> dict[str, Any]:
    executable = [row for row in rows if str(row["execution_status"]).startswith("EXECUTED")]
    unsafe = [row for row in rows if row["promotion_blocked"] and str(row["execution_status"]).startswith("EXECUTED")]
    boundary = [row for row in rows if row["adapter_status"] == "BOUNDARY_ONLY"]
    return {
        "receipt_count": len(rows),
        "executed_receipt_count": len(executable),
        "boundary_only_count": len(boundary),
        "promotion_blocked_executed_count": len(unsafe),
        "safe_executed_count": len(executable) - len(unsafe),
        "all_executed_have_feasibility_check": all(row["feasible_under_capacity"] is not None for row in executable),
        "unsafe_executed_branch_ids": [row["branch_id"] for row in unsafe],
    }


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "bqm_without_slack_promoted", "expected_status": "REJECT", "reject_reason": "pass_0101_counterexample_blocks_general_promotion"},
        {"fixture_id": "branch_without_feasibility_check", "expected_status": "REJECT", "reject_reason": "executed_optimization_branch_must_record_feasibility"},
        {"fixture_id": "provider_branch_without_runtime_receipt", "expected_status": "REJECT", "reject_reason": "hardware_or_provider_claim_needs_execution_receipt"},
    ]


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0103: route a constraint-encoding receipt adapter for optimization solver branches, BQM slack safety, OR-Tools, Ocean, and BuildLang."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    cov = artifact.get("coverage", {})
    rows = artifact.get("constraint_encoding_receipts", [])
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if cov.get("receipt_count") != 10 or cov.get("executed_receipt_count") != 8:
        errors.append("coverage_counts")
    if cov.get("promotion_blocked_executed_count") != 1:
        errors.append("promotion_block_count")
    if cov.get("unsafe_executed_branch_ids") != ["ocean_dimod_exact_bqm"]:
        errors.append("unsafe_branch")
    if not cov.get("all_executed_have_feasibility_check"):
        errors.append("feasibility_checks")
    if not any(row["branch_id"] == "ocean_dimod_exact_bqm" and row["encoding_method"] == "bqm_equality_penalty_to_capacity" for row in rows):
        errors.append("ocean_encoding")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    interop = read_json(INTEROP)
    ortools = read_json(ORTOOLS)
    ocean = read_json(OCEAN)
    inequality = read_json(INEQUALITY)
    roadmap = read_json(ROADMAP)
    rows = receipts(merged_branches(interop, ortools, ocean), inequality)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"interop_pass": interop["pass"], "ortools_pass": ortools["pass"], "ocean_pass": ocean["pass"], "inequality_pass": inequality["pass"], "roadmap_pass": roadmap["pass"]},
        "adapter_rule": {
            "requirement_id": "constraint_encoding_receipt",
            "required_fields": ["constraint_type", "encoding_method", "feasibility_check", "counterexample_ref", "promotion_blocked"],
            "source_law_candidate": inequality["law_candidate"],
        },
        "constraint_encoding_receipts": rows,
        "coverage": coverage(rows),
        "negative_fixtures": negative_fixtures(),
        "current_promoted_natural_laws": [],
        "unsupported_claim_count": 0,
        "non_promotion_statement": "This adapter records solver-encoding safety and promotion blocks. It does not prove quantum advantage, production optimization, provider hardware execution, or a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "receipt_count", "status": "MATCH" if artifact["coverage"]["receipt_count"] == 10 else "DRIFT"},
        {"id": "executed_count", "status": "MATCH" if artifact["coverage"]["executed_receipt_count"] == 8 else "DRIFT"},
        {"id": "unsafe_block", "status": "MATCH" if artifact["coverage"]["unsafe_executed_branch_ids"] == ["ocean_dimod_exact_bqm"] else "DRIFT"},
        {"id": "feasibility_checks", "status": "MATCH" if artifact["coverage"]["all_executed_have_feasibility_check"] else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] and artifact["unsupported_claim_count"] == 0 else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "constraint-encoding-receipt-adapter-pass-0103.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
