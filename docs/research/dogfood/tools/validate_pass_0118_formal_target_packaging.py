"""Validate pass 0118 formal target packaging receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "formal-target-packaging-receipt-pass-0118.json"
RESULT = ROOT / "schemas" / "pass-0118-formal-target-packaging-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def require(condition: bool, errors: list[str], label: str) -> None:
    if not condition:
        errors.append(label)


def validate_sources(artifact: dict, errors: list[str]) -> None:
    target_ids = set(artifact.get("target_ids", []))
    sources = artifact.get("source_targets", [])
    require(len(sources) == 4, errors, "source_count")
    require({row.get("language") for row in sources} == {"lean4", "rocq", "isabelle", "agda"}, errors, "languages")
    for row in sources:
        path = ROOT / row.get("path", "")
        require(path.exists(), errors, f"{row.get('language')}:missing_file")
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        require(text.isascii(), errors, f"{row.get('language')}:ascii")
        require(sha256_file(path) == row.get("sha256"), errors, f"{row.get('language')}:sha256")
        require(set(row.get("proposition_ids_present", [])) == target_ids, errors, f"{row.get('language')}:target_ids")
        require(all(target_id in text for target_id in target_ids), errors, f"{row.get('language')}:target_text")
        require(row.get("status") == "SOURCE_EMITTED_NOT_EXECUTED", errors, f"{row.get('language')}:status")
        require(row.get("execution_status") == "NOT_EXECUTED", errors, f"{row.get('language')}:execution")


def validate_manifest(artifact: dict, errors: list[str]) -> None:
    manifest = artifact.get("manifest", {})
    path = ROOT / manifest.get("path", "")
    require(path.exists(), errors, "manifest_missing")
    if not path.exists():
        return
    manifest_doc = read_json(path)
    require(sha256_file(path) == manifest.get("sha256"), errors, "manifest_sha256")
    require(manifest_doc.get("schema") == "FormalTargetSourceManifest/v1", errors, "manifest_schema")
    require(manifest_doc.get("source_count") == 4, errors, "manifest_source_count")
    require(manifest_doc.get("target_ids") == artifact.get("target_ids"), errors, "manifest_target_ids")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    errors: list[str] = []

    require(artifact.get("schema") == "FormalTargetPackagingReceipt/v1", errors, "schema")
    require(artifact.get("status") == "FORMAL_TARGET_PACKAGING_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("theorem_prover_adapter_pass") == "0117", errors, "adapter_pass")
    require(set(artifact.get("target_ids", [])) == {"idB_comp_f_eq_f", "f_comp_idA_eq_f", "h_comp_g_comp_f_assoc"}, errors, "target_ids")
    validate_sources(artifact, errors)
    validate_manifest(artifact, errors)
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(artifact.get("negative_fixtures", [{}])[0].get("expected_status") == "REJECT", errors, "negative_fixture")
    require("no Lean/Rocq/Isabelle/Agda parser or prover was executed" in artifact.get("execution_boundary", ""), errors, "boundary")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0118FormalTargetPackagingValidatorRun/v1",
        "pass": "0118",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "FormalTargetPackagingReceipt",
            "errors": errors,
            "path": "schemas/formal-target-packaging-receipt-pass-0118.json",
            "source_count": len(artifact.get("source_targets", [])),
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
