"""Validate pass 0080 BuildLang proof-packet demo surface."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buildlang-proof-packet-demo-surface-pass-0080.json"
RESULT = ROOT / "schemas" / "pass-0080-buildlang-proof-packet-demo-surface-validator-result.json"


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
    workspace = artifact.get("workspace_context", {})
    if artifact.get("schema") != "BuildLangProofPacketDemoSurface/v1":
        errors.append("schema")
    if artifact.get("status") != "BUILDLANG_PROOF_PACKET_DEMO_SURFACE_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_intake", {}).get("source_ref_count") != 13:
        errors.append("source_intake")
    if workspace.get("path_scoped_context") is not True or workspace.get("root_context_fallback") is not False:
        errors.append("workspace_context")
    if artifact.get("live_buildc_corpus", {}).get("status") != "MATCH":
        errors.append("live_buildc")
    if artifact.get("forum_route", {}).get("status") != "MATCH":
        errors.append("forum_route")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0080BuildLangProofPacketDemoSurfaceValidatorRun/v1",
        "pass": "0080",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "BuildLangProofPacketDemoSurface",
            "errors": errors,
            "path": "schemas/buildlang-proof-packet-demo-surface-pass-0080.json",
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
