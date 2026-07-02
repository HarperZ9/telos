"""Validate pass 0075 BuildLang domain-envelope join."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buildlang-domain-envelope-join-pass-0075.json"
RESULT = ROOT / "schemas" / "pass-0075-buildlang-domain-envelope-join-validator-result.json"


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
    joined = artifact.get("joined_envelope", {})
    source = artifact.get("buildlang_source_component", {})
    if artifact.get("schema") != "BuildLangDomainEnvelopeJoin/v1":
        errors.append("schema")
    if artifact.get("status") != "BUILDLANG_DOMAIN_ENVELOPE_JOIN_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("domain_id") != "buildlang_buildc" or joined.get("domain_id") != "buildlang_buildc":
        errors.append("domain_id")
    if joined.get("component_digests", {}).get("source_intake") != source.get("digest"):
        errors.append("source_digest_join")
    if source.get("corpus_verify_status") != "MATCH":
        errors.append("corpus_verify")
    if source.get("production_backend_claim") != "C backend only":
        errors.append("backend_scope")
    if joined.get("root_context_fallback") is not True or joined.get("path_scoped_context") is not False:
        errors.append("context_scope")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 8:
        errors.append("negative_fixture_count")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0075BuildLangDomainEnvelopeJoinValidatorRun/v1",
        "pass": "0075",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "BuildLangDomainEnvelopeJoin",
            "domain_id": artifact.get("domain_id"),
            "errors": errors,
            "path": "schemas/buildlang-domain-envelope-join-pass-0075.json",
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
