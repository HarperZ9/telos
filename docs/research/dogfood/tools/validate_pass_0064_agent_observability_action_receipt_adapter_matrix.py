"""Validate pass 0064 agent observability action-receipt adapter matrix."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "agent-observability-action-receipt-adapter-matrix-pass-0064.json"
RESULT = ROOT / "schemas" / "pass-0064-agent-observability-action-receipt-adapter-matrix-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


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
    source_ids = {row.get("source_id") for row in artifact.get("source_anchors", [])}
    tools = {row.get("tool") for row in artifact.get("adapter_rows", [])}
    required_tools = {"LangSmith", "Langfuse", "Arize Phoenix", "Braintrust", "OpenTelemetry", "MLflow", "W&B Weave", "DVC", "promptfoo", "Helicone"}
    required_fields = {"receipt_id", "source_refs", "workspace_state", "authority_scope", "action_admission", "tool_call", "side_effect_class", "trace_refs", "eval_refs", "verification_verdict", "stop_reason", "compensation_pointer", "privacy_boundary", "receipt_status"}
    if artifact.get("schema") != "AgentObservabilityActionReceiptAdapterMatrix/v1":
        errors.append("schema")
    if artifact.get("status") != "AGENT_OBSERVABILITY_ACTION_RECEIPT_ADAPTER_MATRIX_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if len(source_ids) < 10:
        errors.append("source_anchor_count")
    if not required_tools.issubset(tools):
        errors.append("required_tools")
    if not required_fields.issubset(set(artifact.get("action_receipt_fields", []))):
        errors.append("receipt_fields")
    if artifact.get("unsupported_uniqueness_claim_count") != 0:
        errors.append("unsupported_uniqueness_claim_count")
    if artifact.get("non_replacement_claim") is not True:
        errors.append("non_replacement_claim")
    if len(artifact.get("demo_slices", [])) != 3:
        errors.append("demo_slices")
    for row in artifact.get("adapter_rows", []):
        if row.get("source_id") not in source_ids:
            errors.append(f"source:{row.get('tool')}")
        if row.get("proof_layer_gap_status") != "inferred":
            errors.append(f"proof_gap:{row.get('tool')}")
        if not 1 <= row.get("adapter_priority", 0) <= 5:
            errors.append(f"priority:{row.get('tool')}")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0064AgentObservabilityActionReceiptAdapterMatrixValidatorRun/v1",
        "pass": "0064",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "adapter_count": len(tools),
                "artifact": "AgentObservabilityActionReceiptAdapterMatrix",
                "errors": errors,
                "path": "schemas/agent-observability-action-receipt-adapter-matrix-pass-0064.json",
                "receipt_field_count": len(artifact.get("action_receipt_fields", [])),
                "source_anchor_count": len(source_ids),
                "status": status,
            }
        ],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
