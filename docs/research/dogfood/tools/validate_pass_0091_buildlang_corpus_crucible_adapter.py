"""Validate pass 0091 BuildLang corpus-to-Crucible adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buildlang-corpus-crucible-adapter-pass-0091.json"
RESULT = ROOT / "schemas" / "pass-0091-buildlang-corpus-crucible-adapter-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


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
    corpus = artifact.get("buildc_corpus_run", {})
    adapter = artifact.get("crucible_adapter", {})
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != "BuildLangCorpusCrucibleAdapterReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "BUILDLANG_CORPUS_CRUCIBLE_ADAPTER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("prior_binding", {}).get("source_pass") != "0090":
        errors.append("prior_binding")
    if artifact.get("proof_surface_binding", {}).get("source_pass") != "0080":
        errors.append("proof_surface_binding")
    if artifact.get("repo_state", {}).get("exists") is not True:
        errors.append("repo_state")
    if corpus.get("status") != "MATCH" or corpus.get("match") != 10 or corpus.get("drift") != 0:
        errors.append("corpus")
    if adapter.get("measurement_count") != 10 or adapter.get("match") != 10 or adapter.get("drift") != 0:
        errors.append("adapter_count")
    if any(item.get("status") != "MATCH" or item.get("deviation") != 0.0 for item in adapter.get("measurements", [])):
        errors.append("adapter_measurements")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if any(boundary.get(key) for key in ["julia_replacement_claim", "scientific_discovery_claim", "new_natural_law_claim"]):
        errors.append("promotion_boundary")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0091BuildLangCorpusCrucibleAdapterValidatorRun/v1",
        "pass": "0091",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "BuildLangCorpusCrucibleAdapter",
            "errors": errors,
            "path": "schemas/buildlang-corpus-crucible-adapter-pass-0091.json",
            "corpus_status": corpus.get("status"),
            "measurement_count": adapter.get("measurement_count"),
            "adapter_match": adapter.get("match"),
            "adapter_drift": adapter.get("drift"),
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
