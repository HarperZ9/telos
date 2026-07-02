"""Validate pass 0031 Lean replay environment contract receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "lean-replay-environment-contract-pass-0031.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-replay-environment-contract-pass-0031.json"
SOURCE_PREFLIGHT_PATH = ROOT / "schemas" / "theorem-replay-preflight-pass-0030.json"
RESULT_PATH = ROOT / "schemas" / "pass-0031-lean-environment-contract-validator-result.json"


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


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    source = load_json(SOURCE_PREFLIGHT_PATH)
    errors: list[str] = []

    require(data.get("schema") == "LeanReplayEnvironmentContract/v1", errors, "wrong schema")
    require(data.get("pass") == "0031", errors, "wrong pass")
    require(data.get("status") == "LEAN_REPLAY_ENVIRONMENT_CONTRACT_MATCH_WITH_REPLAY_GAP", errors, "wrong status")
    require(data.get("seal") == sha256_obj({key: value for key, value in data.items() if key != "seal"}), errors, "seal mismatch")

    binding = data.get("source_preflight_binding", {})
    require(binding.get("path") == "schemas/theorem-replay-preflight-pass-0030.json", errors, "wrong source preflight path")
    require(binding.get("sha256") == sha256_file(SOURCE_PREFLIGHT_PATH), errors, "source preflight sha mismatch")
    require(binding.get("seal") == source.get("seal"), errors, "source preflight seal mismatch")
    require(binding.get("schema") == "TheoremReplayPreflightPacket/v1", errors, "source preflight schema mismatch")

    fixture_ref = data.get("environment_fixture", {})
    require(fixture_ref.get("path") == "fixtures/lean-replay-environment-contract-pass-0031.json", errors, "wrong fixture path")
    require(fixture_ref.get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(fixture_ref.get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")
    require(fixture.get("seal") == sha256_obj({key: value for key, value in fixture.items() if key != "seal"}), errors, "fixture self seal mismatch")

    runner = data.get("runner_probe", {})
    require(runner.get("git_bash_absolute_path_observed") is True, errors, "git bash absolute path not observed")
    require(runner.get("absolute_bash_invocation_status") == "MATCH", errors, "absolute bash did not match")
    require(runner.get("bash_on_path") is False, errors, "bash path status mismatch")
    require("5.2.37" in runner.get("bash_version", ""), errors, "bash version mismatch")

    attempt = data.get("verify_script_attempt", {})
    require(attempt.get("exit_code") == 1, errors, "verify script exit mismatch")
    require(attempt.get("status") == "DRIFT", errors, "verify script status mismatch")
    require(attempt.get("first_failed_check") == "Frozen SHA pins", errors, "first failed check mismatch")
    require(attempt.get("failure_class") == "crlf_pin_file_path_drift", errors, "failure class mismatch")
    require(attempt.get("lean_or_lake_reached") is False, errors, "lean/lake should not be reached")
    require(attempt.get("raw_log_included") is False, errors, "raw log included")

    availability = data.get("toolchain_availability", {})
    for name in ["docker", "podman", "winget", "elan", "lake", "lean"]:
        require(availability.get(name) == "UNAVAILABLE", errors, f"{name} availability mismatch")
    require(availability.get("wsl") == "UNAVAILABLE_NOT_INSTALLED", errors, "wsl availability mismatch")
    require(availability.get("git") == "MATCH", errors, "git availability mismatch")
    require(availability.get("python") == "MATCH", errors, "python availability mismatch")
    require(availability.get("git_bash_absolute") == "MATCH", errors, "git bash availability mismatch")

    strategy = data.get("environment_strategy", {})
    require(strategy.get("selected_strategy") == "non_mutating_plan", errors, "strategy mismatch")
    require(strategy.get("toolchain_install_performed") is False, errors, "toolchain install performed")
    require(strategy.get("external_write_performed") is False, errors, "external write performed")
    require("line_ending_normalization_decided" in strategy.get("blocked_until", []), errors, "line-ending blocker missing")
    require("elan_or_container_available" in strategy.get("blocked_until", []), errors, "elan/container blocker missing")
    require("lake_and_lean_available" in strategy.get("blocked_until", []), errors, "lake/lean blocker missing")

    replay = data.get("replay_policy", {})
    for field in ["theorem_replay_status", "lake_build_status", "axiom_check_status", "statement_gate_status"]:
        require(replay.get(field) == "UNVERIFIABLE_ENVIRONMENT_NOT_READY", errors, f"{field} promoted")
    require(replay.get("replay_promotion_allowed") is False, errors, "replay promotion allowed")

    proposal = data.get("action_receipt_proposal", {})
    require(proposal.get("schema") == "ActionReceiptLeanReplayEnvironmentContract/v1", errors, "proposal schema mismatch")
    require(proposal.get("event_type") == "lean_replay_environment_contract_created", errors, "proposal event mismatch")
    require(proposal.get("external_write_performed") is False, errors, "proposal external write")
    require(proposal.get("toolchain_install_performed") is False, errors, "proposal install")
    require(proposal.get("replay_promotion_allowed") is False, errors, "proposal promotion allowed")
    require(proposal.get("verification", {}).get("verdict") == "MATCH", errors, "proposal verification mismatch")

    measurements = data.get("verifier_measurements", {})
    require(measurements.get("absolute_bash_invocation_status") == "MATCH", errors, "measurement bash mismatch")
    require(measurements.get("bash_on_path") is False, errors, "measurement bash path mismatch")
    require(measurements.get("verify_script_exit_code") == 1, errors, "measurement exit mismatch")
    require(measurements.get("verify_script_first_failed_check") == "Frozen SHA pins", errors, "measurement first failure mismatch")
    require(measurements.get("crlf_pin_file_path_drift_detected") is True, errors, "measurement CRLF drift mismatch")
    require(measurements.get("lean_or_lake_reached") is False, errors, "measurement lean/lake reached")
    require(measurements.get("missing_runtime_count") == 6, errors, "missing runtime count mismatch")
    require(measurements.get("toolchain_install_performed") is False, errors, "measurement install performed")
    require(measurements.get("external_write_performed") is False, errors, "measurement external write")
    require(measurements.get("theorem_replay_status") == "UNVERIFIABLE_ENVIRONMENT_NOT_READY", errors, "measurement theorem status mismatch")
    require(measurements.get("replay_success_promoted") is False, errors, "replay success promoted")
    require(measurements.get("measurement_status") == "MATCH", errors, "measurement status mismatch")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 10, errors, "expected at least ten negatives")
    require(all(item.get("expected_validator_status") == "REJECT" for item in negatives), errors, "negative not rejected")
    required_negative_ids = {
        "negative-bash-path-assumed-from-path",
        "negative-crlf-failure-ignored",
        "negative-lean-replay-promoted-after-script-failure",
        "negative-container-available-without-docker-or-wsl",
        "negative-toolchain-install-claimed",
        "negative-source-preflight-link-missing",
        "negative-axiom-check-promoted",
        "negative-lake-build-promoted",
        "negative-external-write-hidden",
        "negative-natural-law-promoted",
    }
    require(required_negative_ids == {item.get("fixture_id") for item in negatives}, errors, "negative id set mismatch")
    require(data.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    require("does not install Lean" in data.get("non_promotion_statement", ""), errors, "missing install non-promotion")

    result = {
        "schema": "Pass0031LeanEnvironmentContractValidatorRun/v1",
        "pass": "0031",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "LeanReplayEnvironmentContract",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "absolute_bash_invocation_status": runner.get("absolute_bash_invocation_status"),
                "bash_on_path": runner.get("bash_on_path"),
                "verify_script_exit_code": attempt.get("exit_code"),
                "failure_class": attempt.get("failure_class"),
                "lean_or_lake_reached": attempt.get("lean_or_lake_reached"),
                "theorem_replay_status": replay.get("theorem_replay_status"),
                "missing_runtime_count": measurements.get("missing_runtime_count"),
                "negative_fixture_count": len(negatives),
                "errors": errors,
            }
        ],
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
