"""Validate pass 0052 agent action packet composer build contract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-action-packet-composer-build-contract-pass-0052.json"
FIXTURE_PATH = ROOT / "fixtures" / "agent-action-packet-composer-build-contract-pass-0052.json"
PREVIOUS_PACKET = ROOT / "schemas" / "agent-action-proof-packet-negative-fixtures-pass-0051.json"
RESULT_PATH = ROOT / "schemas" / "pass-0052-agent-action-packet-composer-build-contract-validator-result.json"


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
    require(contract.get("schema") == "AgentActionPacketComposerBuildContractSet/v1", errors, "schema mismatch")
    require(contract.get("status") == "AGENT_ACTION_PACKET_COMPOSER_BUILD_CONTRACT_MATCH", errors, "status mismatch")
    require(check_seal(contract), errors, "contract seal mismatch")
    require(check_seal(fixture), errors, "fixture seal mismatch")
    require(contract.get("previous_pass_binding", {}).get("sha256") == sha256_file(PREVIOUS_PACKET), errors, "pass0051 sha mismatch")
    require(contract.get("previous_pass_binding", {}).get("seal") == previous.get("seal"), errors, "pass0051 seal mismatch")
    require(contract.get("fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(contract.get("implementation_status") == "CONTRACT_ONLY_NOT_IMPLEMENTED", errors, "implementation overclaimed")
    require(contract.get("one_command_runner", {}).get("status") == "proposed", errors, "runner status mismatch")
    require(m.get("input_schema_count") == 8, errors, "input schema count mismatch")
    require(m.get("output_artifact_count") == 6, errors, "output artifact count mismatch")
    require(m.get("build_gate_count") == 6, errors, "build gate count mismatch")
    require(m.get("milestone_count") == 5, errors, "milestone count mismatch")
    require(contract.get("uniqueness_claim_status") == "HYPOTHESIS_ONLY", errors, "uniqueness overclaimed")
    require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    result = {
        "checks": [{
            "artifact": "AgentActionPacketComposerBuildContractSet",
            "errors": errors,
            "implementation_status": contract.get("implementation_status"),
            "path": str(SCHEMA_PATH.relative_to(ROOT)),
            "status": "MATCH" if not errors else "DRIFT",
        }],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0052",
        "schema": "Pass0052AgentActionPacketComposerBuildContractValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT",
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
