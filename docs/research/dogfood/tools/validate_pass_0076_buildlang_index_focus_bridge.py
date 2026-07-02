"""Validate pass 0076 BuildLang Index focus bridge."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buildlang-index-focus-bridge-pass-0076.json"
RESULT = ROOT / "schemas" / "pass-0076-buildlang-index-focus-bridge-validator-result.json"


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
    presence = artifact.get("index_map", {}).get("requested_path_presence", {})
    if artifact.get("schema") != "BuildLangIndexFocusBridge/v1":
        errors.append("schema")
    if artifact.get("status") != "BUILDLANG_INDEX_FOCUS_BRIDGE_REQUIRED":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("root_context", {}).get("status") != "MATCH":
        errors.append("root_context")
    if artifact.get("root_context", {}).get("source_refs_only") is not True:
        errors.append("source_refs_only")
    if artifact.get("path_scoped_context") is not False or artifact.get("bridge_required") is not True:
        errors.append("bridge_scope")
    if any(row.get("verdict") != "EXPECTED_REJECT" for row in artifact.get("focus_probes", [])):
        errors.append("focus_probe_verdicts")
    if presence.get("buildlang", {}).get("present") is not True:
        errors.append("buildlang_presence")
    if presence.get("compiler", {}).get("present") is not True:
        errors.append("compiler_presence")
    if presence.get("build-universe", {}).get("present") is not False:
        errors.append("build_universe_absence")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 8:
        errors.append("negative_fixture_count")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0076BuildLangIndexFocusBridgeValidatorRun/v1",
        "pass": "0076",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "BuildLangIndexFocusBridge",
            "errors": errors,
            "path": "schemas/buildlang-index-focus-bridge-pass-0076.json",
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
