"""Generate pass 0031 Lean replay environment contract receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PASS = "0031"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_PREFLIGHT_PATH = ROOT / "schemas" / "theorem-replay-preflight-pass-0030.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-replay-environment-contract-pass-0031.json"
OUT_PATH = ROOT / "schemas" / "lean-replay-environment-contract-pass-0031.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


source_preflight = read_json(SOURCE_PREFLIGHT_PATH)

fixture = {
    "schema": "LeanReplayEnvironmentContractFixture/v1",
    "pass": PASS,
    "source_preflight_ref": "schemas/theorem-replay-preflight-pass-0030.json",
    "source_preflight_sha256": sha256_file(SOURCE_PREFLIGHT_PATH),
    "source_preflight_seal": source_preflight["seal"],
    "runner_probe": {
        "git_bash_path_ref": "program-files-git-bash",
        "git_bash_absolute_path_observed": True,
        "bash_version": "GNU bash, version 5.2.37(1)-release (x86_64-pc-msys)",
        "bash_on_path": False,
        "absolute_bash_invocation_status": "MATCH",
    },
    "verify_script_attempt": {
        "command": "program-files-git-bash scripts/verify.sh --no-log --all",
        "exit_code": 1,
        "status": "DRIFT",
        "first_failed_check": "Frozen SHA pins",
        "failure_class": "crlf_pin_file_path_drift",
        "failure_summary": "scripts/frozen.sha256 is read with CRLF path text, so sha256sum sees Prob4b/Defs.lean with a trailing carriage return.",
        "raw_log_included": False,
        "lean_or_lake_reached": False,
    },
    "toolchain_availability": {
        "docker": "UNAVAILABLE",
        "wsl": "UNAVAILABLE_NOT_INSTALLED",
        "podman": "UNAVAILABLE",
        "winget": "UNAVAILABLE",
        "elan": "UNAVAILABLE",
        "lake": "UNAVAILABLE",
        "lean": "UNAVAILABLE",
        "git": "MATCH",
        "python": "MATCH",
        "git_bash_absolute": "MATCH",
    },
    "environment_strategy": {
        "selected_strategy": "non_mutating_plan",
        "toolchain_install_performed": False,
        "external_write_performed": False,
        "recommended_next_strategy": "Clone with LF-preserving settings or normalize verifier inputs, then provision elan and Lean v4.31.0 in an isolated temp or container environment.",
        "blocked_until": [
            "line_ending_normalization_decided",
            "elan_or_container_available",
            "lake_and_lean_available",
        ],
    },
    "replay_policy": {
        "theorem_replay_status": "UNVERIFIABLE_ENVIRONMENT_NOT_READY",
        "lake_build_status": "UNVERIFIABLE_ENVIRONMENT_NOT_READY",
        "axiom_check_status": "UNVERIFIABLE_ENVIRONMENT_NOT_READY",
        "statement_gate_status": "UNVERIFIABLE_ENVIRONMENT_NOT_READY",
        "replay_promotion_allowed": False,
    },
}
fixture["seal"] = sha256_obj({key: value for key, value in fixture.items() if key != "seal"})
write_json(FIXTURE_PATH, fixture)

fixture_sha = sha256_file(FIXTURE_PATH)
source_preflight_sha = sha256_file(SOURCE_PREFLIGHT_PATH)

negative_fixtures = [
    {
        "fixture_id": "negative-bash-path-assumed-from-path",
        "failure_mode": "The packet treats bash as available on PATH instead of absolute Git Bash only.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-crlf-failure-ignored",
        "failure_mode": "The packet ignores the frozen.sha256 CRLF path failure.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-lean-replay-promoted-after-script-failure",
        "failure_mode": "The packet promotes theorem replay after verify.sh exits before Lean/Lake.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-container-available-without-docker-or-wsl",
        "failure_mode": "The packet chooses a container replay despite Docker and WSL being unavailable.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-toolchain-install-claimed",
        "failure_mode": "The packet claims a toolchain install occurred.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-source-preflight-link-missing",
        "failure_mode": "The environment contract is not linked to pass 0030.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-axiom-check-promoted",
        "failure_mode": "The packet claims axiom checks ran.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-lake-build-promoted",
        "failure_mode": "The packet claims Lake build success.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-external-write-hidden",
        "failure_mode": "The packet hides an external write or environment mutation.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-natural-law-promoted",
        "failure_mode": "The packet promotes an environment contract into a solved theorem or natural law.",
        "expected_validator_status": "REJECT",
    },
]

record = {
    "schema": "LeanReplayEnvironmentContract/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "LEAN_REPLAY_ENVIRONMENT_CONTRACT_MATCH_WITH_REPLAY_GAP",
    "source_preflight_binding": {
        "path": "schemas/theorem-replay-preflight-pass-0030.json",
        "sha256": source_preflight_sha,
        "seal": source_preflight["seal"],
        "schema": source_preflight["schema"],
    },
    "environment_fixture": {
        "path": "fixtures/lean-replay-environment-contract-pass-0031.json",
        "sha256": fixture_sha,
        "seal": fixture["seal"],
        "schema": fixture["schema"],
    },
    "runner_probe": fixture["runner_probe"],
    "verify_script_attempt": fixture["verify_script_attempt"],
    "toolchain_availability": fixture["toolchain_availability"],
    "environment_strategy": fixture["environment_strategy"],
    "replay_policy": fixture["replay_policy"],
    "action_receipt_proposal": {
        "schema": "ActionReceiptLeanReplayEnvironmentContract/v1",
        "action_id": "act_dogfood_0031_lean_environment_contract",
        "event_id": "evt_dogfood_0031_lean_environment_contract",
        "event_type": "lean_replay_environment_contract_created",
        "authority_class": "read_only_environment_probe",
        "input_refs": [
            "artifact:schemas/theorem-replay-preflight-pass-0030.json",
            "artifact:fixtures/lean-replay-environment-contract-pass-0031.json",
        ],
        "input_digests": [
            f"sha256:{source_preflight_sha}",
            f"sha256:{fixture_sha}",
        ],
        "output_ref": "artifact:schemas/lean-replay-environment-contract-pass-0031.json",
        "external_write_performed": False,
        "toolchain_install_performed": False,
        "replay_promotion_allowed": False,
        "verification": {
            "verdict": "MATCH",
            "ref": "validator:pass-0031-lean-replay-environment-contract",
        },
    },
    "verifier_measurements": {
        "schema": "LeanReplayEnvironmentContractMeasurements/v1",
        "absolute_bash_invocation_status": "MATCH",
        "bash_on_path": False,
        "verify_script_exit_code": 1,
        "verify_script_first_failed_check": "Frozen SHA pins",
        "crlf_pin_file_path_drift_detected": True,
        "lean_or_lake_reached": False,
        "missing_runtime_count": 6,
        "toolchain_install_performed": False,
        "external_write_performed": False,
        "theorem_replay_status": "UNVERIFIABLE_ENVIRONMENT_NOT_READY",
        "replay_success_promoted": False,
        "measurement_status": "MATCH",
    },
    "negative_fixtures": negative_fixtures,
    "negative_fixture_count": len(negative_fixtures),
    "next_actions": [
        "Choose LF-preserving checkout or blob-byte hash policy.",
        "Provision elan and Lean v4.31.0 in a reversible temp path or container.",
        "Rerun scripts/verify.sh --no-log --all with logs captured as receipts.",
        "Promote only after Lake build, axiom checks, and statement gates complete.",
    ],
    "non_promotion_statement": "Pass 0031 verifies environment readiness and a verifier-script failure mode only. It does not install Lean, does not run Lake, does not prove any theorem, and does not promote any natural law.",
    "current_promoted_natural_laws": [],
}
record["seal"] = sha256_obj({key: value for key, value in record.items() if key != "seal"})
write_json(OUT_PATH, record)

print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "schema": record["schema"],
            "status": record["status"],
            "absolute_bash_invocation_status": record["runner_probe"]["absolute_bash_invocation_status"],
            "verify_script_exit_code": record["verify_script_attempt"]["exit_code"],
            "failure_class": record["verify_script_attempt"]["failure_class"],
            "theorem_replay_status": record["replay_policy"]["theorem_replay_status"],
            "negative_fixture_count": record["negative_fixture_count"],
            "seal": record["seal"],
        },
        indent=2,
        sort_keys=True,
    )
)
