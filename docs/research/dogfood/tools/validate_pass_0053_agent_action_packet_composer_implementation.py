"""Validate pass 0053 agent action packet composer implementation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-action-packet-composer-implementation-pass-0053.json"
BUNDLE_DIR = ROOT / "demo-bundles" / "agent-action-proof-packet-pass-0053"
PREVIOUS_PACKET = ROOT / "schemas" / "agent-action-packet-composer-build-contract-pass-0052.json"
RESULT_PATH = ROOT / "schemas" / "pass-0053-agent-action-packet-composer-implementation-validator-result.json"
EXPECTED_OUTPUTS = ["packet.json", "packet.md", "receipts.json", "negative-fixture-report.json", "index.html", "replay-commands.md"]


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
    previous = load_json(PREVIOUS_PACKET)
    packet = load_json(BUNDLE_DIR / "packet.json")
    negative = load_json(BUNDLE_DIR / "negative-fixture-report.json")
    receipts = load_json(BUNDLE_DIR / "receipts.json")
    m = contract.get("verifier_measurements", {})
    require(contract.get("schema") == "AgentActionPacketComposerImplementationSet/v1", errors, "schema mismatch")
    require(contract.get("status") == "AGENT_ACTION_PACKET_COMPOSER_IMPLEMENTATION_MATCH", errors, "status mismatch")
    require(check_seal(contract), errors, "contract seal mismatch")
    require(contract.get("previous_pass_binding", {}).get("sha256") == sha256_file(PREVIOUS_PACKET), errors, "pass0052 sha mismatch")
    require(contract.get("previous_pass_binding", {}).get("seal") == previous.get("seal"), errors, "pass0052 seal mismatch")
    require(contract.get("implementation_status") == "IMPLEMENTED_LOCAL_DEMO_BUNDLE", errors, "implementation status mismatch")
    require(contract.get("compose_receipt", {}).get("status") == "MATCH", errors, "compose command did not match")
    require(contract.get("test_receipt", {}).get("status") == "MATCH", errors, "composer test did not match")
    require(m.get("output_count") == 6, errors, "output count mismatch")
    require(m.get("output_match_count") == 6, errors, "output match count mismatch")
    require(m.get("negative_fixture_count") == 8, errors, "negative fixture count mismatch")
    require(m.get("negative_match_count") == 8, errors, "negative match count mismatch")
    require(m.get("negative_pass_observed_count") == 0, errors, "negative fixture passed")
    require(packet.get("verification", {}).get("verdict") == "MATCH", errors, "packet verdict mismatch")
    require(negative.get("status") == "MATCH", errors, "negative report mismatch")
    require(receipts.get("status") == "MATCH", errors, "bundle receipts mismatch")
    for rel_path in EXPECTED_OUTPUTS:
        require((BUNDLE_DIR / rel_path).exists(), errors, f"missing bundle output {rel_path}")
    require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    result = {
        "checks": [{
            "artifact": "AgentActionPacketComposerImplementationSet",
            "errors": errors,
            "implementation_status": contract.get("implementation_status"),
            "output_match_count": m.get("output_match_count"),
            "path": str(SCHEMA_PATH.relative_to(ROOT)),
            "status": "MATCH" if not errors else "DRIFT",
        }],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0053",
        "schema": "Pass0053AgentActionPacketComposerImplementationValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT",
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
