"""Validate pass 0034 Lean replay verification receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "lean-replay-verification-pass-0034.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-replay-verification-pass-0034.json"
SOURCE_PATH = ROOT / "schemas" / "lean-provisioning-build-timeout-pass-0033.json"
RESULT_PATH = ROOT / "schemas" / "pass-0034-lean-replay-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
    source = load_json(SOURCE_PATH)

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")

    if isinstance(contract, dict):
        require(contract.get("schema") == "LeanReplayVerificationPacket/v1", errors, "schema mismatch")
        require(contract.get("status") == "LEAN_REPLAY_VERIFIED_WITH_AXIOM_BOUNDARY", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("source_provisioning_binding", {}).get("sha256") == sha256_file(SOURCE_PATH), errors, "source sha mismatch")
        require(contract.get("source_provisioning_binding", {}).get("seal") == source.get("seal"), errors, "source seal mismatch")

        cache = contract.get("cache_hydration", {})
        require(cache.get("exit_code") == 0, errors, "cache get exit mismatch")
        require(cache.get("downloaded_files") == 8542, errors, "cache download count mismatch")
        require(cache.get("decompressed_files") == 8542, errors, "cache decompressed count mismatch")
        require(cache.get("cache_file_count") == 8542, errors, "cache file count mismatch")
        require(cache.get("cache_byte_sum") == 432264798, errors, "cache byte sum mismatch")

        run = contract.get("verifier_run", {})
        require(run.get("exit_code") == 0, errors, "verifier exit mismatch")
        require(run.get("result") == "PASS", errors, "verifier result mismatch")
        require(run.get("result_issue_count") == 0, errors, "issue count mismatch")
        require(run.get("frozen_sha_pins_status") == "PASS", errors, "frozen pin status mismatch")
        require(run.get("banned_keywords_status") == "PASS", errors, "banned keyword status mismatch")
        require(run.get("lake_build_status") == "PASS", errors, "lake build status mismatch")
        require(run.get("build_jobs") == 8574, errors, "build jobs mismatch")
        require(run.get("theorem_axiom_status") == "PASS", errors, "theorem axiom status mismatch")
        require(len(run.get("theorem_axiom_checks", [])) == 10, errors, "axiom check count mismatch")
        for row in run.get("theorem_axiom_checks", []):
            require(row.get("status") == "PASS", errors, f"axiom check {row.get('name')} not PASS")
            require(row.get("axioms") == ["propext", "Classical.choice", "Quot.sound"], errors, f"axiom set mismatch for {row.get('name')}")
        require(run.get("statement_gates") == [
            {"module": "Prob4b.Discharge", "status": "PASS"},
            {"module": "Prob4b.Solution", "status": "PASS"}
        ], errors, "statement gates mismatch")

        artifacts = contract.get("build_artifacts", {})
        require(artifacts.get("lake_file_count") == 123892, errors, "lake file count mismatch")
        require(artifacts.get("lake_byte_sum") == 8009101293, errors, "lake byte sum mismatch")
        require(artifacts.get("prob4b_build_file_count") == 75, errors, "Prob4b build file count mismatch")
        require(artifacts.get("prob4b_build_byte_sum") == 10048128, errors, "Prob4b build byte sum mismatch")
        require(artifacts.get("remaining_temp_processes") == 0, errors, "temp processes left")

        fixture_ref = contract.get("replay_fixture", {})
        require(fixture_ref.get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(fixture_ref.get("seal") == fixture.get("seal"), errors, "fixture seal reference mismatch")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 10, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")

        measurements = contract.get("verifier_measurements", {})
        require(measurements.get("cache_get_status") == "MATCH", errors, "cache measurement mismatch")
        require(measurements.get("lake_build_status") == "PASS", errors, "lake build measurement mismatch")
        require(measurements.get("axiom_check_count") == 10, errors, "axiom measurement mismatch")
        require(measurements.get("statement_gate_count") == 2, errors, "statement gate measurement mismatch")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "LeanReplayVerificationFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "artifact": "LeanReplayVerificationPacket",
                "axiom_check_count": len(contract.get("verifier_run", {}).get("theorem_axiom_checks", [])) if isinstance(contract, dict) else 0,
                "cache_file_count": contract.get("cache_hydration", {}).get("cache_file_count") if isinstance(contract, dict) else None,
                "errors": errors,
                "lake_build_status": contract.get("verifier_run", {}).get("lake_build_status") if isinstance(contract, dict) else None,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "prob4b_build_file_count": contract.get("build_artifacts", {}).get("prob4b_build_file_count") if isinstance(contract, dict) else None,
                "remaining_temp_processes": contract.get("build_artifacts", {}).get("remaining_temp_processes") if isinstance(contract, dict) else None,
                "status": "MATCH" if not errors else "DRIFT",
                "theorem_axiom_status": contract.get("verifier_run", {}).get("theorem_axiom_status") if isinstance(contract, dict) else None,
                "verifier_exit_code": contract.get("verifier_run", {}).get("exit_code") if isinstance(contract, dict) else None,
                "verifier_result": contract.get("verifier_run", {}).get("result") if isinstance(contract, dict) else None
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0034",
        "schema": "Pass0034LeanReplayValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
