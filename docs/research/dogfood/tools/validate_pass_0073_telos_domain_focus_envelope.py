"""Validate pass 0073 Telos domain-focus envelope."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "telos-domain-focus-envelope-pass-0073.json"
RESULT = ROOT / "schemas" / "pass-0073-telos-domain-focus-envelope-validator-result.json"
REQUIRED_LAYERS = {"source_intake", "workspace_context", "routing", "verification", "continuity", "action"}


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
    envelopes = artifact.get("domain_envelopes", [])
    if artifact.get("schema") != "TelosDomainFocusEnvelopeSet/v1":
        errors.append("schema")
    if artifact.get("status") != "TELOS_DOMAIN_FOCUS_ENVELOPE_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("domain_count") != len(envelopes) or artifact.get("domain_count") != 6:
        errors.append("domain_count")
    if artifact.get("root_fallback_envelopes") != 6 or artifact.get("path_scoped_envelopes") != 0:
        errors.append("context_scope_counts")
    for envelope in envelopes:
        if envelope.get("schema") != "TelosDomainFocusEnvelope/v1":
            errors.append(f"envelope_schema:{envelope.get('domain_id')}")
        if set(envelope.get("required_layers", [])) != REQUIRED_LAYERS:
            errors.append(f"layers:{envelope.get('domain_id')}")
        if envelope.get("route_decision") != "project-telos" or envelope.get("route_needs_escalation"):
            errors.append(f"route:{envelope.get('domain_id')}")
        if envelope.get("unsupported_claim_count") != 0:
            errors.append(f"unsupported:{envelope.get('domain_id')}")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 8:
        errors.append("negative_fixture_count")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0073TelosDomainFocusEnvelopeValidatorRun/v1",
        "pass": "0073",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "TelosDomainFocusEnvelopeSet",
            "domain_count": artifact.get("domain_count"),
            "errors": errors,
            "negative_fixture_count": len(artifact.get("negative_fixtures", [])),
            "path": "schemas/telos-domain-focus-envelope-pass-0073.json",
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
