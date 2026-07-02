"""Compose pass 0079 BuildLang path-context envelope join."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "BuildLangPathContextEnvelopeJoin/v1"
PASS_ID = "0079"
STATUS_MATCH = "BUILDLANG_PATH_CONTEXT_ENVELOPE_JOIN_MATCH"
STATUS_DRIFT = "BUILDLANG_PATH_CONTEXT_ENVELOPE_JOIN_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
DOMAIN_ID = "buildlang_buildc"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def path_context_component(receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "workspace_context",
        "component_id": "index.path-selector.receipt.0078",
        "label": "BuildLang selected-path IndexPathSelectorReceipt adapter fixture",
        "digest": receipt["seal"],
        "graph_pack_sha256": receipt["graph_pack_sha256"],
        "verification_status": "MATCH" if receipt["status"] == "INDEX_PATH_SELECTOR_RECEIPT_FIXTURE_MATCH" else "DRIFT",
        "raw_payload_included": receipt["raw_source_included"],
        "source_refs_only": receipt["source_refs_only"],
        "source_ref_count": receipt["source_ref_count"],
        "selected_selector_count": receipt["selected_selector_count"],
        "rejected_selector_count": receipt["rejected_selector_count"],
        "missing_selector_rejections": receipt["missing_selector_rejections"],
        "adapter_fixture": True,
        "native_index_path_selector": False,
    }


def join_envelope(previous: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    joined = dict(previous["joined_envelope"])
    joined["envelope_id"] = "telos.domain-focus.buildlang_buildc.0079"
    joined["component_digests"] = dict(joined["component_digests"])
    joined["component_digests"]["workspace_context"] = context["digest"]
    joined["workspace_context_component_id"] = context["component_id"]
    joined["workspace_context_graph_pack_sha256"] = context["graph_pack_sha256"]
    joined["workspace_context_source_ref_count"] = context["source_ref_count"]
    joined["workspace_context_selected_selector_count"] = context["selected_selector_count"]
    joined["workspace_context_rejected_selector_count"] = context["rejected_selector_count"]
    joined["missing_selector_rejections"] = context["missing_selector_rejections"]
    joined["index_strategy"] = "adapter_path_selector_receipt_plus_source_refs"
    joined["root_context_fallback"] = False
    joined["path_scoped_context"] = True
    joined["adapter_fixture"] = True
    joined["native_index_path_selector"] = False
    joined["raw_private_payload_required"] = False
    joined["verification_status"] = "MATCH"
    joined.pop("seal", None)
    joined["seal"] = sha256_obj(joined)
    return joined


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "claims_native_index_path_selector", "expected_status": "REJECT", "reject_reason": "adapter_fixture_not_native_index"},
        {"fixture_id": "claims_build_universe_covered", "expected_status": "REJECT", "reject_reason": "missing_selector_rejected"},
        {"fixture_id": "path_context_without_source_refs", "expected_status": "REJECT", "reject_reason": "source_refs_required"},
        {"fixture_id": "raw_payload_required", "expected_status": "REJECT", "reject_reason": "source_refs_only_boundary"},
        {"fixture_id": "target_output_promoted", "expected_status": "REJECT", "reject_reason": "generated_outputs_excluded"},
        {"fixture_id": "root_context_fallback_claim", "expected_status": "REJECT", "reject_reason": "path_context_replaces_root_fallback"},
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
    ]


def compose() -> dict[str, Any]:
    pass_0075 = read_json(ROOT / "schemas" / "buildlang-domain-envelope-join-pass-0075.json")
    pass_0078 = read_json(ROOT / "schemas" / "index-path-selector-receipt-pass-0078.json")
    context = path_context_component(pass_0078)
    joined = join_envelope(pass_0075, context)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "domain_id": DOMAIN_ID,
        "previous_envelope_pass": "0075",
        "path_context_receipt_pass": "0078",
        "previous_workspace_context_digest": pass_0075["joined_envelope"]["component_digests"]["workspace_context"],
        "path_context_component": context,
        "joined_envelope": joined,
        "root_context_fallback_replaced": True,
        "path_scoped_context": True,
        "adapter_fixture": True,
        "native_index_path_selector": False,
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0079 joins an adapter path-selector receipt into the BuildLang domain envelope. It does not modify Index natively, cover missing build-universe sources, include raw payloads, prove market adoption, or promote a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    context = artifact.get("path_context_component", {})
    joined = artifact.get("joined_envelope", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("domain_id") != DOMAIN_ID or joined.get("domain_id") != DOMAIN_ID:
        errors.append("domain")
    if context.get("verification_status") != "MATCH":
        errors.append("context_status")
    if context.get("source_ref_count") != 128:
        errors.append("source_ref_count")
    if context.get("raw_payload_included") is not False or context.get("source_refs_only") is not True:
        errors.append("privacy")
    if "build-universe" not in context.get("missing_selector_rejections", []):
        errors.append("missing_selector")
    if joined.get("component_digests", {}).get("workspace_context") != context.get("digest"):
        errors.append("workspace_digest_join")
    if joined.get("root_context_fallback") is not False or joined.get("path_scoped_context") is not True:
        errors.append("context_scope")
    if joined.get("adapter_fixture") is not True or joined.get("native_index_path_selector") is not False:
        errors.append("adapter_boundary")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 7:
        errors.append("negative_fixture_count")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"out": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
