"""Validate pass 0032 Lean replay remediation contract receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "lean-replay-remediation-contract-pass-0032.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-replay-remediation-contract-pass-0032.json"
SOURCE_ENV_PATH = ROOT / "schemas" / "lean-replay-environment-contract-pass-0031.json"
RESULT_PATH = ROOT / "schemas" / "pass-0032-lean-replay-remediation-validator-result.json"


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
    source = load_json(SOURCE_ENV_PATH)
    errors: list[str] = []

    require(data.get("schema") == "LeanReplayRemediationContract/v1", errors, "wrong schema")
    require(data.get("pass") == "0032", errors, "wrong pass")
    require(data.get("status") == "LEAN_REPLAY_REMEDIATION_MATCH_WITH_LAKE_GAP", errors, "wrong status")
    require(data.get("seal") == sha256_obj({key: value for key, value in data.items() if key != "seal"}), errors, "seal mismatch")

    binding = data.get("source_environment_binding", {})
    require(binding.get("path") == "schemas/lean-replay-environment-contract-pass-0031.json", errors, "wrong source environment path")
    require(binding.get("sha256") == sha256_file(SOURCE_ENV_PATH), errors, "source environment sha mismatch")
    require(binding.get("seal") == source.get("seal"), errors, "source environment seal mismatch")
    require(binding.get("schema") == "LeanReplayEnvironmentContract/v1", errors, "source environment schema mismatch")

    fixture_ref = data.get("remediation_fixture", {})
    require(fixture_ref.get("path") == "fixtures/lean-replay-remediation-contract-pass-0032.json", errors, "wrong fixture path")
    require(fixture_ref.get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(fixture_ref.get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")
    require(fixture.get("seal") == sha256_obj({key: value for key, value in fixture.items() if key != "seal"}), errors, "fixture self seal mismatch")

    sources = data.get("public_source_receipts", [])
    require(len(sources) == 3, errors, "wrong official source count")
    require(all(item.get("verification_status") == "verified" for item in sources), errors, "unverified official source")
    source_names = {item.get("source") for item in sources}
    require({"elan README", "Lean reference manual", "Git config manual"} == source_names, errors, "official source set mismatch")

    lf = data.get("lf_clone_probe", {})
    require(lf.get("repo_commit") == "69d7df765a8f377a5e0628c6d36c088bce7642c9", errors, "repo commit mismatch")
    require(lf.get("checkout_policy") == "core.autocrlf=false", errors, "checkout policy mismatch")
    require(lf.get("status") == "MATCH", errors, "lf clone status mismatch")
    eol = lf.get("eol_probe", {})
    require(len(eol) == 3, errors, "eol probe count mismatch")
    require(all(value == "i/lf w/lf" for value in eol.values()), errors, "eol probe not all LF")

    shim = data.get("python3_shim_probe", {})
    require(shim.get("shim_kind") == "reversible_temp_path_wrapper", errors, "shim kind mismatch")
    require(shim.get("shim_contents_hash") == sha256_text("#!/usr/bin/env bash\nexec python \"$@\"\n"), errors, "shim hash mismatch")
    require(shim.get("python_version") == "Python 3.12.10", errors, "python version mismatch")
    require(shim.get("temp_write_performed") is True, errors, "temp write not recorded")
    require(shim.get("external_write_performed") is False, errors, "external write recorded")
    require(shim.get("status") == "MATCH", errors, "shim status mismatch")

    attempts = data.get("verify_attempts", [])
    require(len(attempts) == 2, errors, "attempt count mismatch")
    first = attempts[0] if attempts else {}
    second = attempts[1] if len(attempts) > 1 else {}
    require(first.get("attempt_id") == "lf_no_python3_shim", errors, "first attempt id mismatch")
    require(first.get("exit_code") == 1, errors, "first attempt exit mismatch")
    require(first.get("passed_checks") == ["Frozen SHA pins"], errors, "first passed checks mismatch")
    require(first.get("failed_check") == "Banned keywords", errors, "first failed check mismatch")
    require(first.get("failure_class") == "python3_missing_in_git_bash", errors, "first failure class mismatch")
    require(first.get("lake_or_lean_reached") is False, errors, "first attempt reached lake/lean")
    require(second.get("attempt_id") == "lf_with_python3_shim", errors, "second attempt id mismatch")
    require(second.get("exit_code") == 1, errors, "second attempt exit mismatch")
    require(second.get("passed_checks") == ["Frozen SHA pins", "Banned keywords"], errors, "second passed checks mismatch")
    require(second.get("failed_check") == "lake build", errors, "second failed check mismatch")
    require(second.get("failure_class") == "lake_missing", errors, "second failure class mismatch")
    require(second.get("lake_or_lean_reached") is False, errors, "second attempt reached lake/lean")

    decision = data.get("remediation_decision", {})
    require(decision.get("line_ending_gate_status") == "RESOLVED_IN_TEMP_LF_CLONE", errors, "line-ending gate mismatch")
    require(decision.get("python3_gate_status") == "RESOLVED_BY_REVERSIBLE_TEMP_SHIM", errors, "python3 gate mismatch")
    require(decision.get("next_blocker") == "lake_missing", errors, "next blocker mismatch")
    require(decision.get("toolchain_install_performed") is False, errors, "toolchain install performed")
    require(decision.get("replay_success_promoted") is False, errors, "replay promoted")
    require(decision.get("selected_next_strategy") == "provision_elan_or_lake_lean_in_reversible_environment", errors, "next strategy mismatch")

    proposal = data.get("action_receipt_proposal", {})
    require(proposal.get("schema") == "ActionReceiptLeanReplayRemediation/v1", errors, "proposal schema mismatch")
    require(proposal.get("event_type") == "lean_replay_remediation_contract_created", errors, "proposal event mismatch")
    require(proposal.get("temp_write_performed") is True, errors, "proposal temp write mismatch")
    require(proposal.get("external_write_performed") is False, errors, "proposal external write")
    require(proposal.get("toolchain_install_performed") is False, errors, "proposal install")
    require(proposal.get("replay_promotion_allowed") is False, errors, "proposal replay allowed")
    require(proposal.get("verification", {}).get("verdict") == "MATCH", errors, "proposal verification mismatch")

    measurements = data.get("verifier_measurements", {})
    require(measurements.get("lf_clone_eol_match_count") == 3, errors, "measurement eol count mismatch")
    require(measurements.get("attempt_count") == 2, errors, "measurement attempt count mismatch")
    require(measurements.get("first_attempt_passed_check_count") == 1, errors, "first pass count mismatch")
    require(measurements.get("second_attempt_passed_check_count") == 2, errors, "second pass count mismatch")
    require(measurements.get("python3_shim_status") == "MATCH", errors, "measurement shim mismatch")
    require(measurements.get("next_blocker") == "lake_missing", errors, "measurement blocker mismatch")
    require(measurements.get("lake_build_status") == "UNVERIFIABLE_TOOL_UNAVAILABLE", errors, "lake build promoted")
    require(measurements.get("lean_replay_status") == "UNVERIFIABLE_TOOL_UNAVAILABLE", errors, "lean replay promoted")
    require(measurements.get("official_source_count") == 3, errors, "official source count mismatch")
    require(measurements.get("toolchain_install_performed") is False, errors, "measurement install performed")
    require(measurements.get("external_write_performed") is False, errors, "measurement external write")
    require(measurements.get("replay_success_promoted") is False, errors, "measurement replay promoted")
    require(measurements.get("measurement_status") == "MATCH", errors, "measurement status mismatch")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 10, errors, "expected at least ten negatives")
    require(all(item.get("expected_validator_status") == "REJECT" for item in negatives), errors, "negative not rejected")
    required_negative_ids = {
        "negative-lf-clone-not-required",
        "negative-python3-shim-treated-as-system-install",
        "negative-banned-keywords-promoted-without-shim",
        "negative-lake-build-promoted-without-lake",
        "negative-lean-replay-promoted",
        "negative-source-environment-link-missing",
        "negative-official-source-basis-missing",
        "negative-external-write-hidden",
        "negative-next-blocker-misidentified",
        "negative-natural-law-promoted",
    }
    require(required_negative_ids == {item.get("fixture_id") for item in negatives}, errors, "negative id set mismatch")
    require(data.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    require("does not install elan" in data.get("non_promotion_statement", ""), errors, "missing non-promotion statement")

    result = {
        "schema": "Pass0032LeanReplayRemediationValidatorRun/v1",
        "pass": "0032",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "LeanReplayRemediationContract",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "lf_clone_eol_match_count": len(eol),
                "attempt_count": len(attempts),
                "first_attempt_failed_check": first.get("failed_check"),
                "second_attempt_failed_check": second.get("failed_check"),
                "python3_shim_status": shim.get("status"),
                "line_ending_gate_status": decision.get("line_ending_gate_status"),
                "python3_gate_status": decision.get("python3_gate_status"),
                "next_blocker": decision.get("next_blocker"),
                "lake_build_status": measurements.get("lake_build_status"),
                "lean_replay_status": measurements.get("lean_replay_status"),
                "official_source_count": len(sources),
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
