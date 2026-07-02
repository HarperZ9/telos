"""Validate pass 0055 multi-trace causality graph artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "multitrace-causality-graph-adapter-pass-0055.json"
GRAPH = ROOT / "schemas" / "multitrace-causality-graph-pass-0055.json"
SOURCE_BINDING = ROOT / "schemas" / "source-evidence-binding-pass-0028.json"
TRACE_JOIN = ROOT / "schemas" / "otel-trace-receipt-join-pass-0054.json"
TOOL_RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0054.json"
RESULT_PATH = ROOT / "schemas" / "pass-0055-multitrace-causality-graph-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    graph = read_json(GRAPH)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    summary = graph.get("graph_summary", {})
    bindings = artifact.get("upstream_bindings", {})
    if artifact.get("schema") != "MultiTraceCausalityGraphAdapterSet/v1":
        errors.append("schema")
    if artifact.get("status") != "MULTITRACE_CAUSALITY_GRAPH_ADAPTER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("graph_output", {}).get("sha256") != sha256_file(GRAPH):
        errors.append("graph_sha")
    if graph.get("status") != "MULTITRACE_CAUSALITY_GRAPH_MATCH":
        errors.append("graph_status")
    if summary.get("node_count") != 4 or summary.get("edge_count") != 3:
        errors.append("graph_shape")
    if summary.get("independent_receipt_count") != 4:
        errors.append("independent_receipt_count")
    if summary.get("trace_identity_substitution_count") != 0:
        errors.append("trace_identity_substitution_count")
    if graph.get("negative_match_count") != 5 or graph.get("negative_pass_observed_count") != 0:
        errors.append("negative_fixture_replay")
    if bindings.get("source_binding", {}).get("sha256") != sha256_file(SOURCE_BINDING):
        errors.append("source_binding_sha")
    if bindings.get("trace_join", {}).get("sha256") != sha256_file(TRACE_JOIN):
        errors.append("trace_join_sha")
    if bindings.get("tool_receipts", {}).get("sha256") != sha256_file(TOOL_RECEIPTS):
        errors.append("tool_receipts_sha")
    if artifact.get("current_promoted_natural_laws") != [] or graph.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0055MultiTraceCausalityGraphValidatorRun/v1",
        "pass": "0055",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "MultiTraceCausalityGraphAdapterSet",
                "edge_count": summary.get("edge_count"),
                "errors": errors,
                "node_count": summary.get("node_count"),
                "path": "schemas/multitrace-causality-graph-adapter-pass-0055.json",
                "status": status,
                "trace_identity_substitution_count": summary.get("trace_identity_substitution_count"),
            }
        ],
    }


def main() -> None:
    result = validate()
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
