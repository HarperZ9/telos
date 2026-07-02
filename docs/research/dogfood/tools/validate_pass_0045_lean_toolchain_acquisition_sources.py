"""Validate pass 0045 Lean/Elan toolchain acquisition source receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "lean-toolchain-acquisition-sources-pass-0045.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-toolchain-acquisition-sources-pass-0045.json"
PREVIOUS_PACKET = ROOT / "schemas" / "lean-lake-executable-preflight-pass-0044.json"
RESULT_PATH = ROOT / "schemas" / "pass-0045-lean-toolchain-acquisition-sources-validator-result.json"


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
    measurements = contract.get("verifier_measurements", {})

    require(contract.get("schema") == "LeanToolchainAcquisitionSourcesSet/v1", errors, "schema mismatch")
    require(contract.get("status") == "LEAN_TOOLCHAIN_ACQUISITION_SOURCES_MATCH", errors, "status mismatch")
    require(check_seal(contract), errors, "contract seal mismatch")
    require(fixture.get("schema") == "LeanToolchainAcquisitionSourcesFixture/v1", errors, "fixture schema mismatch")
    require(check_seal(fixture), errors, "fixture seal mismatch")
    require(contract.get("executable_preflight_binding", {}).get("sha256") == sha256_file(PREVIOUS_PACKET), errors, "pass0044 sha mismatch")
    require(contract.get("executable_preflight_binding", {}).get("seal") == previous.get("seal"), errors, "pass0044 seal mismatch")
    require(contract.get("toolchain_acquisition_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(contract.get("toolchain_acquisition_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")
    require(contract.get("expected_project_toolchain") == previous["verifier_measurements"]["expected_toolchain"], errors, "expected toolchain mismatch")
    require(measurements.get("source_count") == 4, errors, "source count mismatch")
    require(measurements.get("source_match_count") == 4, errors, "source match count mismatch")
    require(measurements.get("windows_installer_script_fetched") is True, errors, "installer script not fetched")
    require(measurements.get("windows_installer_script_executed") is False, errors, "installer script executed")
    for row in contract.get("source_receipts", []):
        require(row.get("status") == "MATCH", errors, f"source {row.get('id')} drift")
        require(row.get("status_code") == 200, errors, f"source {row.get('id')} status code")
        require(all(row.get("contains", {}).values()), errors, f"source {row.get('id')} missing expected phrase")
    require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    result = {
        "checks": [{
            "artifact": "LeanToolchainAcquisitionSourcesSet",
            "errors": errors,
            "path": str(SCHEMA_PATH.relative_to(ROOT)),
            "source_match_count": measurements.get("source_match_count"),
            "status": "MATCH" if not errors else "DRIFT",
        }],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0045",
        "schema": "Pass0045LeanToolchainAcquisitionSourcesValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
