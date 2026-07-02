"""Validate pass 0079 BuildLang path-context envelope join."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buildlang-path-context-envelope-join-pass-0079.json"
RESULT = ROOT / "schemas" / "pass-0079-buildlang-path-context-envelope-join-validator-result.json"


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
    context = artifact.get("path_context_component", {})
    joined = artifact.get("joined_envelope", {})
    if artifact.get("schema") != "BuildLangPathContextEnvelopeJoin/v1":
        errors.append("schema")
    if artifact.get("status") != "BUILDLANG_PATH_CONTEXT_ENVELOPE_JOIN_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if context.get("source_ref_count") != 128:
        errors.append("source_ref_count")
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
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0079BuildLangPathContextEnvelopeJoinValidatorRun/v1",
        "pass": "0079",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "BuildLangPathContextEnvelopeJoin",
            "errors": errors,
            "path": "schemas/buildlang-path-context-envelope-join-pass-0079.json",
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
