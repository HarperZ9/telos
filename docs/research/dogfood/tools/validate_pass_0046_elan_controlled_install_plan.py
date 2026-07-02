"""Validate pass 0046 controlled Elan install-plan receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "elan-controlled-install-plan-pass-0046.json"
FIXTURE_PATH = ROOT / "fixtures" / "elan-controlled-install-plan-pass-0046.json"
PREVIOUS_PACKET = ROOT / "schemas" / "lean-toolchain-acquisition-sources-pass-0045.json"
RESULT_PATH = ROOT / "schemas" / "pass-0046-elan-controlled-install-plan-validator-result.json"


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
    require(contract.get("schema") == "ElanControlledInstallPlanSet/v1", errors, "schema mismatch")
    require(contract.get("status") == "ELAN_CONTROLLED_INSTALL_PLAN_MATCH", errors, "status mismatch")
    require(check_seal(contract), errors, "contract seal mismatch")
    require(fixture.get("schema") == "ElanControlledInstallPlanFixture/v1", errors, "fixture schema mismatch")
    require(check_seal(fixture), errors, "fixture seal mismatch")
    require(contract.get("acquisition_source_binding", {}).get("sha256") == sha256_file(PREVIOUS_PACKET), errors, "pass0045 sha mismatch")
    require(contract.get("acquisition_source_binding", {}).get("seal") == previous.get("seal"), errors, "pass0045 seal mismatch")
    require(contract.get("elan_controlled_install_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(contract.get("elan_controlled_install_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")
    for key in ["default_toolchain_supported", "no_modify_path_supported", "no_prompt_supported", "start_process_present"]:
        require(m.get(key) is True, errors, f"{key} missing")
    require(m.get("installer_script_executed") is False, errors, "installer executed")
    require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    result = {
        "checks": [{
            "artifact": "ElanControlledInstallPlanSet",
            "errors": errors,
            "path": str(SCHEMA_PATH.relative_to(ROOT)),
            "status": "MATCH" if not errors else "DRIFT",
        }],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0046",
        "schema": "Pass0046ElanControlledInstallPlanValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
