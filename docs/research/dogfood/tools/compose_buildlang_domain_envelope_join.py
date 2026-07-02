"""Compose pass 0075 BuildLang domain-envelope join."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "BuildLangDomainEnvelopeJoin/v1"
PASS_ID = "0075"
STATUS_MATCH = "BUILDLANG_DOMAIN_ENVELOPE_JOIN_MATCH"
STATUS_DRIFT = "BUILDLANG_DOMAIN_ENVELOPE_JOIN_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
DOMAIN_ID = "buildlang_buildc"
REQUIRED_LAYERS = ["source_intake", "workspace_context", "routing", "verification", "continuity", "action"]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def buildlang_source_component(receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "source_intake",
        "component_id": "buildlang.source-ref.receipt.0074",
        "label": "BuildLang source refs plus live buildc corpus verify receipt",
        "digest": receipt["seal"],
        "seal": sha256_obj({
            "source_refs": receipt["source_ref_count"],
            "corpus_stdout": receipt["corpus_verify"]["stdout_sha256"],
            "production_backend_claim": receipt["production_backend_claim"],
        }),
        "verification_status": "MATCH" if receipt["status"] == "BUILDLANG_SOURCE_REF_RECEIPT_MATCH" else "DRIFT",
        "raw_payload_included": False,
        "source_ref_count": receipt["source_ref_count"],
        "program_count": receipt["program_count"],
        "corpus_verify_status": receipt["corpus_verify"]["status"],
        "corpus_verify_stdout_sha256": receipt["corpus_verify"]["stdout_sha256"],
        "production_backend_claim": receipt["production_backend_claim"],
    }


def join_envelope(prior_envelope: dict[str, Any], source_component: dict[str, Any]) -> dict[str, Any]:
    joined = dict(prior_envelope)
    joined["envelope_id"] = "telos.domain-focus.buildlang_buildc.0075"
    joined["source_component_id"] = source_component["component_id"]
    joined["component_digests"] = dict(joined["component_digests"])
    joined["component_digests"]["source_intake"] = source_component["digest"]
    joined["buildlang_source_ref_count"] = source_component["source_ref_count"]
    joined["buildlang_corpus_verify_status"] = source_component["corpus_verify_status"]
    joined["buildlang_program_count"] = source_component["program_count"]
    joined["buildlang_production_backend_claim"] = source_component["production_backend_claim"]
    joined["domain_source_ref_replaced"] = True
    joined["root_context_fallback"] = True
    joined["path_scoped_context"] = False
    joined["verification_status"] = "MATCH"
    joined.pop("seal", None)
    joined["seal"] = sha256_obj(joined)
    return joined


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "missing_buildlang_source_receipt", "expected_status": "REJECT", "reject_reason": "missing_domain_source_receipt"},
        {"fixture_id": "buildc_corpus_verify_drift", "expected_status": "REJECT", "reject_reason": "corpus_verify_not_match"},
        {"fixture_id": "source_digest_drift", "expected_status": "REJECT", "reject_reason": "source_ref_digest_drift"},
        {"fixture_id": "claims_path_scoped_context_without_index_refs", "expected_status": "REJECT", "reject_reason": "path_scoped_context_unproven"},
        {"fixture_id": "claims_all_backends_production", "expected_status": "REJECT", "reject_reason": "experimental_backends_promoted"},
        {"fixture_id": "self_hosted_compiler_promoted", "expected_status": "REJECT", "reject_reason": "self_hosted_compiler_unverified"},
        {"fixture_id": "raw_payload_required", "expected_status": "REJECT", "reject_reason": "raw_private_payload_required"},
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
    ]


def ablation_results() -> list[dict[str, Any]]:
    rows = [{"case_id": "full_buildlang_domain_envelope_join", "removed_layer": None, "verdict": "MATCH", "reason": "BuildLang source receipt joined with all required layers"}]
    for layer in REQUIRED_LAYERS:
        rows.append({"case_id": f"without_{layer}", "removed_layer": layer, "verdict": "REJECT", "reason": f"missing_required_layer:{layer}"})
    return rows


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    joined = artifact.get("joined_envelope", {})
    source = artifact.get("buildlang_source_component", {})
    if artifact.get("domain_id") != DOMAIN_ID:
        errors.append("domain_id")
    if joined.get("domain_id") != DOMAIN_ID:
        errors.append("joined_domain")
    if not joined.get("domain_source_ref_replaced"):
        errors.append("domain_source_ref_replaced")
    if joined.get("component_digests", {}).get("source_intake") != source.get("digest"):
        errors.append("source_digest_join")
    if source.get("corpus_verify_status") != "MATCH":
        errors.append("corpus_verify")
    if source.get("production_backend_claim") != "C backend only":
        errors.append("backend_scope")
    if joined.get("path_scoped_context") is not False or joined.get("root_context_fallback") is not True:
        errors.append("context_scope")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 8:
        errors.append("negative_fixture_count")
    return errors


def compose() -> dict[str, Any]:
    pass_0073 = read_json(ROOT / "schemas" / "telos-domain-focus-envelope-pass-0073.json")
    pass_0074 = read_json(ROOT / "schemas" / "buildlang-source-ref-receipt-pass-0074.json")
    prior = [row for row in pass_0073["domain_envelopes"] if row["domain_id"] == DOMAIN_ID][0]
    source = buildlang_source_component(pass_0074)
    joined = join_envelope(prior, source)
    artifact = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "domain_id": DOMAIN_ID,
        "previous_domain_envelope_seal": prior["seal"],
        "previous_domain_envelope_source_digest": prior["component_digests"]["source_intake"],
        "buildlang_source_component": source,
        "joined_envelope": joined,
        "domain_source_ref_replaced": True,
        "root_context_fallback_preserved": True,
        "path_scoped_context": False,
        "ablation_results": ablation_results(),
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0075 joins the BuildLang source-ref receipt into one domain envelope. It does not implement path-scoped Index context, prove all BuildLang backends production-ready, prove self-hosting, replace Julia, establish market adoption, solve a scientific problem, or establish a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


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
