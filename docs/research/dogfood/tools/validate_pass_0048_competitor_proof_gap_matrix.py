"""Validate pass 0048 competitor proof-gap matrix receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "competitor-proof-gap-matrix-pass-0048.json"
FIXTURE_PATH = ROOT / "fixtures" / "competitor-proof-gap-matrix-pass-0048.json"
PREVIOUS_PACKET = ROOT / "schemas" / "ai4science-proof-market-sources-pass-0047.json"
RESULT_PATH = ROOT / "schemas" / "pass-0048-competitor-proof-gap-matrix-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def check_seal(value: dict) -> bool:
    copy = dict(value)
    seal = copy.pop("seal", None)
    return seal == sha256_obj(copy)


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    previous = load_json(PREVIOUS_PACKET)
    m = contract.get("verifier_measurements", {})
    rows = contract.get("market_rows", [])
    receipts = contract.get("source_receipts", [])
    track_counts = contract.get("track_counts", {})
    require(contract.get("schema") == "CompetitorProofGapMatrixSet/v1", errors, "schema mismatch")
    require(contract.get("status") == "COMPETITOR_PROOF_GAP_MATRIX_MATCH", errors, "status mismatch")
    require(check_seal(contract), errors, "contract seal mismatch")
    require(check_seal(fixture), errors, "fixture seal mismatch")
    require(contract.get("previous_pass_binding", {}).get("sha256") == sha256_file(PREVIOUS_PACKET), errors, "pass0047 sha mismatch")
    require(contract.get("previous_pass_binding", {}).get("seal") == previous.get("seal"), errors, "pass0047 seal mismatch")
    require(contract.get("fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(m.get("market_row_count") == 45, errors, "market row count mismatch")
    require(m.get("source_count") == 45, errors, "source count mismatch")
    require(m.get("source_match_count") == 45, errors, "source match count mismatch")
    require(track_counts.get("research_ai4science") == 15, errors, "research track count mismatch")
    require(track_counts.get("ai_infra_agent_ops") == 15, errors, "ai infra track count mismatch")
    require(track_counts.get("visual_compiler_compute") == 15, errors, "visual/compiler track count mismatch")
    require(contract.get("uniqueness_claim_status") == "HYPOTHESIS_ONLY", errors, "uniqueness overclaimed")
    require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    require(len(contract.get("wedge_scores", [])) == 3, errors, "wedge score count mismatch")
    require(len(contract.get("megatool_nodes", [])) >= 8, errors, "megatool node count mismatch")
    for row in rows:
        require(row.get("gap_status") in {"verified", "inferred", "unverified"}, errors, f"invalid gap status for {row.get('company_tool')}")
        require(row.get("sources"), errors, f"missing source for {row.get('company_tool')}")
    for receipt in receipts:
        require(receipt.get("status") == "MATCH", errors, f"source {receipt.get('id')} drift")
        require(all(receipt.get("contains", {}).values()), errors, f"source {receipt.get('id')} missing phrase")
    result = {
        "checks": [{
            "artifact": "CompetitorProofGapMatrixSet",
            "errors": errors,
            "market_row_count": m.get("market_row_count"),
            "path": str(SCHEMA_PATH.relative_to(ROOT)),
            "source_match_count": m.get("source_match_count"),
            "status": "MATCH" if not errors else "DRIFT",
        }],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0048",
        "schema": "Pass0048CompetitorProofGapMatrixValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT",
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
