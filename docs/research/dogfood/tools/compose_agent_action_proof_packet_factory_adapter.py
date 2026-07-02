"""Compose pass 0124 agent action proof-packet factory adapter."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "AgentActionProofPacketFactoryAdapter/v1"
PASS_ID = "0124"
STATUS_MATCH = "AGENT_ACTION_PROOF_PACKET_FACTORY_ADAPTER_MATCH"
STATUS_DRIFT = "AGENT_ACTION_PROOF_PACKET_FACTORY_ADAPTER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SOURCE_STORE = ROOT / "gather" / "pass-0124-agent-action-adapter-sources"
MATRIX = ROOT / "schemas" / "agent-observability-action-receipt-adapter-matrix-pass-0064.json"
OTEL_FIXTURE = ROOT / "schemas" / "otel-trace-to-action-receipt-fixture-pass-0065.json"
FACTORY = ROOT / "schemas" / "field-to-proof-packet-factory-pass-0123.json"

SOURCE_LABELS = {
    "https://opentelemetry.io/docs/concepts/signals/traces/": ("opentelemetry_traces", "OpenTelemetry traces"),
    "https://opentelemetry.io/docs/concepts/context-propagation/": ("opentelemetry_context", "OpenTelemetry context propagation"),
    "https://www.w3.org/TR/trace-context/": ("trace_context", "W3C Trace Context"),
    "https://docs.langchain.com/langsmith/observability": ("langsmith", "LangSmith observability"),
    "https://langfuse.com/docs/observability/overview": ("langfuse", "Langfuse observability"),
    "https://arize.com/docs/phoenix/tracing/llm-traces": ("phoenix", "Phoenix tracing"),
    "https://www.braintrust.dev/docs/guides/tracing": ("braintrust", "Braintrust tracing"),
}

NATIVE_TRACES = [
    ("opentelemetry", {"trace_id": "4f7e65b0c6c34c2aa1d6f64e08b03a65", "span_ids": ["0f1a", "0f1b", "0f1c"], "metric_ref": "metric:latency_ms"}),
    ("langsmith", {"trace_ref": "ls-trace-0124", "run_url": "local://langsmith/run/0124", "evaluation_ref": "eval:authority-boundary"}),
    ("langfuse", {"trace_id": "lf-trace-0124", "prompt_version": "prompt:v3", "score_ref": "score:unsupported-claim-count"}),
    ("phoenix", {"trace_id": "px-trace-0124", "span_id": "px-span-root", "annotation_ref": "annotation:human-review"}),
    ("braintrust", {"experiment_id": "bt-exp-0124", "trace_ref": "bt-trace-0124", "eval_ref": "bt-eval-admission"}),
]


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


def read_catalog() -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in (SOURCE_STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        obj = SOURCE_STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
        row["chars"] = len(obj.read_text(encoding="utf-8", errors="replace")) if obj.exists() else 0
    return rows


def source_matrix() -> list[dict[str, Any]]:
    output = []
    for row in read_catalog():
        source_id, label = SOURCE_LABELS.get(row["ref"], ("unclassified", row["title"]))
        output.append({
            "source_id": source_id,
            "label": label,
            "url": row["ref"],
            "title": row["title"].encode("ascii", "ignore").decode("ascii"),
            "sha256": row["sha256"],
            "chars": row["chars"],
            "gather_status": "GATHER_VERIFIED" if row["chars"] >= 500 else "GATHER_VERIFIED_SHORT_TEXT",
            "gap_status": "inferred",
        })
    return sorted(output, key=lambda item: item["source_id"])


def adapter_contract() -> list[str]:
    return read_json(MATRIX)["action_receipt_fields"]


def trace_inputs() -> list[dict[str, Any]]:
    return [{"native_system": system, "native_refs": refs, "native_ref_digest": sha256_obj(refs), "source_status": "TRACE_INPUT_FIXTURE"} for system, refs in NATIVE_TRACES]


def action_receipt(trace: dict[str, Any], required: list[str]) -> dict[str, Any]:
    system = trace["native_system"]
    receipt = {
        "receipt_id": f"agent-action-proof-pass-0124-{system}",
        "schema": "project-telos.action-receipt/v1",
        "source_refs": [{"kind": "official_source", "ref": f"source:{system}"}, {"kind": "prior_pass", "ref": "pass-0123"}],
        "workspace_state": {"repo": "telos", "path": "docs/research/dogfood", "dirty_allowed": True},
        "authority_scope": {"scope": "local_dogfood_research", "allowed_side_effects": ["local_write", "local_read"]},
        "action_admission": {"decision": "admit", "admission_id": f"admit-{system}-0124", "required": True},
        "tool_call": {"name": "agent_action_proof_packet_factory_adapter", "mode": "synthetic_trace_import", "native_system": system},
        "side_effect_class": "local_write",
        "materials_digest": trace["native_ref_digest"],
        "trace_refs": {"native_system": system, "native_refs": trace["native_refs"]},
        "eval_refs": [{"kind": "validator", "ref": "pass-0124-validator"}],
        "model_refs": [{"kind": "model_boundary", "ref": "hidden_reasoning_not_exported"}],
        "runtime_refs": [{"kind": "python", "ref": "local interpreter"}],
        "verification_verdict": "MATCH",
        "stop_reason": "completed_with_match_verdict",
        "compensation_pointer": {"required": False, "reason": "local dogfood fixture"},
        "privacy_boundary": "no raw private payloads, secrets, tokens, PII, or hidden reasoning exported",
        "receipt_status": "MATCH",
    }
    missing = [field for field in required if field not in receipt]
    receipt["adapter_status"] = "MATCH" if not missing else "DRIFT"
    receipt["adapter_missing_fields"] = missing
    digestable = dict(receipt)
    receipt["receipt_digest"] = sha256_obj(digestable)
    return receipt


def classify_broken(receipt: dict[str, Any], required: list[str]) -> list[str]:
    failures = [f"missing_{field}" for field in required if field not in receipt]
    admission = receipt.get("action_admission", {})
    if receipt.get("side_effect_class") in {"local_write", "external_write"} and admission.get("decision") != "admit":
        failures.append("write_without_admission")
    if receipt.get("side_effect_class") == "external_write" and receipt.get("authority_scope", {}).get("external_write_allowed") is not True:
        failures.append("external_write_not_authorized")
    if receipt.get("verification_verdict") not in {"MATCH", "DRIFT", "UNVERIFIABLE"}:
        failures.append("invalid_or_missing_verification_verdict")
    if receipt.get("reasoning_trace_exposed") is True:
        failures.append("hidden_reasoning_exported")
    return sorted(set(failures))


def negative_fixtures(required: list[str]) -> list[dict[str, Any]]:
    base = action_receipt(trace_inputs()[0], required)
    cases = []
    for fixture_id, remove in [("missing_authority_scope", "authority_scope"), ("missing_action_admission", "action_admission"), ("missing_verifier", "verification_verdict")]:
        bad = dict(base)
        bad.pop(remove, None)
        cases.append({"fixture_id": fixture_id, "failures": classify_broken(bad, required), "status": "REJECTED"})
    bad = dict(base)
    bad["side_effect_class"] = "external_write"
    bad["reasoning_trace_exposed"] = True
    cases.append({"fixture_id": "external_write_and_hidden_reasoning", "failures": classify_broken(bad, required), "status": "REJECTED"})
    return cases


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagships() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0124 executable agent action proof-packet adapter for observability traces, authority, admission, and verifier receipts."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided"), "confidence": parsed.get("confidence")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    required = adapter_contract()
    traces = trace_inputs()
    receipts = [action_receipt(trace, required) for trace in traces]
    negatives = negative_fixtures(required)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"adapter_matrix_pass": read_json(MATRIX)["pass"], "otel_fixture_pass": read_json(OTEL_FIXTURE)["pass"], "factory_pass": read_json(FACTORY)["pass"], "source_store": str(SOURCE_STORE.relative_to(ROOT)).replace("\\", "/")},
        "source_matrix": source_matrix(),
        "adapter_contract_fields": required,
        "trace_inputs": traces,
        "action_receipts": receipts,
        "negative_fixtures": negatives,
        "adapter_claim_status": "HYPOTHESIS_WITH_EXECUTABLE_FIXTURES",
        "market_gap_status": "inferred",
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0124 is a local synthetic adapter fixture across observability trace shapes. It does not claim production ingestion, replacement of incumbents, market fit, external-write authority, scientific discovery, or a promoted natural law.",
        "flagship_receipts": flagships(),
    }
    errors = []
    if len(artifact["source_matrix"]) < 7 or sum(row["chars"] >= 500 for row in artifact["source_matrix"]) < 7:
        errors.append("source_matrix")
    if len(receipts) != 5 or any(row["adapter_status"] != "MATCH" for row in receipts):
        errors.append("action_receipts")
    if len(negatives) != 4 or any(row["status"] != "REJECTED" or not row["failures"] for row in negatives):
        errors.append("negative_fixtures")
    if any(row["status"] != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "agent-action-proof-packet-factory-adapter-pass-0124.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
