"""Validate pass 0047 AI4Science proof-market source receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "ai4science-proof-market-sources-pass-0047.json"
FIXTURE_PATH = ROOT / "fixtures" / "ai4science-proof-market-sources-pass-0047.json"
PREVIOUS_PACKET = ROOT / "schemas" / "elan-controlled-install-plan-pass-0046.json"
RESULT_PATH = ROOT / "schemas" / "pass-0047-ai4science-proof-market-sources-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


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
    require(contract.get("schema") == "AI4ScienceProofMarketSourcesSet/v1", errors, "schema mismatch")
    require(contract.get("status") == "AI4SCIENCE_PROOF_MARKET_SOURCES_MATCH", errors, "status mismatch")
    require(check_seal(contract), errors, "contract seal mismatch")
    require(check_seal(fixture), errors, "fixture seal mismatch")
    require(contract.get("controlled_install_plan_binding", {}).get("sha256") == sha256_file(PREVIOUS_PACKET), errors, "pass0046 sha mismatch")
    require(contract.get("controlled_install_plan_binding", {}).get("seal") == previous.get("seal"), errors, "pass0046 seal mismatch")
    require(contract.get("fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(m.get("source_count") == 10, errors, "source count mismatch")
    require(m.get("source_match_count") == 10, errors, "source match count mismatch")
    require(m.get("wedge_count") == 5, errors, "wedge count mismatch")
    require(contract.get("uniqueness_claim_status") == "HYPOTHESIS_ONLY", errors, "uniqueness overclaimed")
    for row in contract.get("source_receipts", []):
        require(row.get("status") == "MATCH", errors, f"source {row.get('id')} drift")
        require(all(row.get("contains", {}).values()), errors, f"source {row.get('id')} missing phrase")
    require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    result = {
        "checks": [{
            "artifact": "AI4ScienceProofMarketSourcesSet",
            "errors": errors,
            "path": str(SCHEMA_PATH.relative_to(ROOT)),
            "source_match_count": m.get("source_match_count"),
            "status": "MATCH" if not errors else "DRIFT",
        }],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0047",
        "schema": "Pass0047AI4ScienceProofMarketSourcesValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
