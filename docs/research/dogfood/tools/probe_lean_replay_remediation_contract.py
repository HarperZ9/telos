"""Generate pass 0032 Lean replay remediation contract receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PASS = "0032"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_ENV_PATH = ROOT / "schemas" / "lean-replay-environment-contract-pass-0031.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-replay-remediation-contract-pass-0032.json"
OUT_PATH = ROOT / "schemas" / "lean-replay-remediation-contract-pass-0032.json"


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


source_env = read_json(SOURCE_ENV_PATH)

fixture = {
    "schema": "LeanReplayRemediationContractFixture/v1",
    "pass": PASS,
    "source_environment_ref": "schemas/lean-replay-environment-contract-pass-0031.json",
    "source_environment_sha256": sha256_file(SOURCE_ENV_PATH),
    "source_environment_seal": source_env["seal"],
    "public_source_receipts": [
        {
            "source": "elan README",
            "url": "https://github.com/leanprover/elan",
            "verification_status": "verified",
            "claim": "Elan manages Lean installations and places lean and lake binaries on PATH, selecting the version from lean-toolchain when needed.",
            "locator": "web:turn0view0:L285-L287",
        },
        {
            "source": "Lean reference manual",
            "url": "https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/",
            "verification_status": "verified",
            "claim": "Elan installs and runs Lean toolchains; projects can use lean-toolchain files to select a Lean version.",
            "locator": "web:turn1view0:L84-L88 and web:turn1view1:L149-L162",
        },
        {
            "source": "Git config manual",
            "url": "https://git-scm.com/docs/git-config",
            "verification_status": "verified",
            "claim": "core.autocrlf=true converts working-directory text files to CRLF; core.eol is ignored when core.autocrlf is true or input.",
            "locator": "web:turn1view2:L1644-L1658",
        },
    ],
    "lf_clone_probe": {
        "command": "git -c core.autocrlf=false clone --depth 1 https://github.com/Pengbinghui/pipeline-math.git temp:pipeline-math-pass0032-lf",
        "repo_commit": "69d7df765a8f377a5e0628c6d36c088bce7642c9",
        "checkout_policy": "core.autocrlf=false",
        "eol_probe": {
            "Prob4b/Defs.lean": "i/lf w/lf",
            "Prob4b/Theorems.lean": "i/lf w/lf",
            "scripts/frozen.sha256": "i/lf w/lf",
        },
        "status": "MATCH",
    },
    "python3_shim_probe": {
        "shim_ref": "temp:telos-pass0032-shim/python3",
        "shim_kind": "reversible_temp_path_wrapper",
        "shim_contents_hash": sha256_text("#!/usr/bin/env bash\nexec python \"$@\"\n"),
        "python3_resolution": "temp:telos-pass0032-shim/python3",
        "python_version": "Python 3.12.10",
        "temp_write_performed": True,
        "external_write_performed": False,
        "status": "MATCH",
    },
    "verify_attempts": [
        {
            "attempt_id": "lf_no_python3_shim",
            "command": "absolute Git Bash scripts/verify.sh --no-log --all",
            "exit_code": 1,
            "passed_checks": ["Frozen SHA pins"],
            "failed_check": "Banned keywords",
            "failure_class": "python3_missing_in_git_bash",
            "lake_or_lean_reached": False,
            "status": "DRIFT",
        },
        {
            "attempt_id": "lf_with_python3_shim",
            "command": "absolute Git Bash with temp python3 shim scripts/verify.sh --no-log --all",
            "exit_code": 1,
            "passed_checks": ["Frozen SHA pins", "Banned keywords"],
            "failed_check": "lake build",
            "failure_class": "lake_missing",
            "lake_or_lean_reached": False,
            "status": "DRIFT",
        },
    ],
    "remediation_decision": {
        "line_ending_gate_status": "RESOLVED_IN_TEMP_LF_CLONE",
        "python3_gate_status": "RESOLVED_BY_REVERSIBLE_TEMP_SHIM",
        "next_blocker": "lake_missing",
        "toolchain_install_performed": False,
        "replay_success_promoted": False,
        "selected_next_strategy": "provision_elan_or_lake_lean_in_reversible_environment",
        "official_source_basis": ["elan README", "Lean reference manual", "Git config manual"],
    },
    "non_claims": [
        "This remediation contract does not install elan.",
        "This remediation contract does not run lake successfully.",
        "This remediation contract does not run Lean theorem checking.",
        "This remediation contract does not prove Problem 4(b).",
    ],
}
fixture["seal"] = sha256_obj({key: value for key, value in fixture.items() if key != "seal"})
write_json(FIXTURE_PATH, fixture)

fixture_sha = sha256_file(FIXTURE_PATH)
source_env_sha = sha256_file(SOURCE_ENV_PATH)

negative_fixtures = [
    {
        "fixture_id": "negative-lf-clone-not-required",
        "failure_mode": "The packet ignores that LF checkout is required to pass frozen SHA pin checks on this workstation.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-python3-shim-treated-as-system-install",
        "failure_mode": "The packet treats the temp python3 shim as a system Python install.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-banned-keywords-promoted-without-shim",
        "failure_mode": "The packet claims banned-keyword check passed without resolving python3 in Git Bash.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-lake-build-promoted-without-lake",
        "failure_mode": "The packet claims lake build success even though lake is missing.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-lean-replay-promoted",
        "failure_mode": "The packet promotes theorem replay despite Lean never being reached.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-source-environment-link-missing",
        "failure_mode": "The remediation packet is not linked to pass 0031.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-official-source-basis-missing",
        "failure_mode": "The packet lacks official Lean/Git source basis for the remediation plan.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-external-write-hidden",
        "failure_mode": "The packet hides an external write or toolchain install.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-next-blocker-misidentified",
        "failure_mode": "The packet identifies a blocker other than lake_missing after the temp shim run.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-natural-law-promoted",
        "failure_mode": "The packet promotes remediation progress into a solved theorem or natural law.",
        "expected_validator_status": "REJECT",
    },
]

record = {
    "schema": "LeanReplayRemediationContract/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "LEAN_REPLAY_REMEDIATION_MATCH_WITH_LAKE_GAP",
    "source_environment_binding": {
        "path": "schemas/lean-replay-environment-contract-pass-0031.json",
        "sha256": source_env_sha,
        "seal": source_env["seal"],
        "schema": source_env["schema"],
    },
    "remediation_fixture": {
        "path": "fixtures/lean-replay-remediation-contract-pass-0032.json",
        "sha256": fixture_sha,
        "seal": fixture["seal"],
        "schema": fixture["schema"],
    },
    "public_source_receipts": fixture["public_source_receipts"],
    "lf_clone_probe": fixture["lf_clone_probe"],
    "python3_shim_probe": fixture["python3_shim_probe"],
    "verify_attempts": fixture["verify_attempts"],
    "remediation_decision": fixture["remediation_decision"],
    "action_receipt_proposal": {
        "schema": "ActionReceiptLeanReplayRemediation/v1",
        "action_id": "act_dogfood_0032_lean_replay_remediation",
        "event_id": "evt_dogfood_0032_lean_replay_remediation",
        "event_type": "lean_replay_remediation_contract_created",
        "authority_class": "temp_clone_and_reversible_shim_probe",
        "input_refs": [
            "artifact:schemas/lean-replay-environment-contract-pass-0031.json",
            "artifact:fixtures/lean-replay-remediation-contract-pass-0032.json",
        ],
        "input_digests": [f"sha256:{source_env_sha}", f"sha256:{fixture_sha}"],
        "output_ref": "artifact:schemas/lean-replay-remediation-contract-pass-0032.json",
        "temp_write_performed": True,
        "external_write_performed": False,
        "toolchain_install_performed": False,
        "replay_promotion_allowed": False,
        "verification": {
            "verdict": "MATCH",
            "ref": "validator:pass-0032-lean-replay-remediation",
        },
    },
    "verifier_measurements": {
        "schema": "LeanReplayRemediationMeasurements/v1",
        "lf_clone_eol_match_count": 3,
        "attempt_count": 2,
        "first_attempt_passed_check_count": 1,
        "second_attempt_passed_check_count": 2,
        "python3_shim_status": "MATCH",
        "line_ending_gate_status": "RESOLVED_IN_TEMP_LF_CLONE",
        "python3_gate_status": "RESOLVED_BY_REVERSIBLE_TEMP_SHIM",
        "next_blocker": "lake_missing",
        "lake_build_status": "UNVERIFIABLE_TOOL_UNAVAILABLE",
        "lean_replay_status": "UNVERIFIABLE_TOOL_UNAVAILABLE",
        "official_source_count": 3,
        "toolchain_install_performed": False,
        "external_write_performed": False,
        "replay_success_promoted": False,
        "measurement_status": "MATCH",
    },
    "negative_fixtures": negative_fixtures,
    "negative_fixture_count": len(negative_fixtures),
    "next_actions": [
        "Provision elan or a lake/lean toolchain in a reversible temp environment.",
        "Keep LF checkout policy or blob-byte frozen-pin validation.",
        "Keep the python3 shim or patch verifier invocation in a temp copy only.",
        "Rerun verify.sh and promote only if lake build, axiom checks, and statement gates complete.",
    ],
    "non_promotion_statement": "Pass 0032 resolves line-ending and python3 Git Bash gates in temporary probes only. It does not install elan, does not run lake successfully, does not reach Lean theorem replay, and does not promote any natural law.",
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
            "line_ending_gate_status": record["remediation_decision"]["line_ending_gate_status"],
            "python3_gate_status": record["remediation_decision"]["python3_gate_status"],
            "next_blocker": record["remediation_decision"]["next_blocker"],
            "attempt_count": record["verifier_measurements"]["attempt_count"],
            "negative_fixture_count": record["negative_fixture_count"],
            "seal": record["seal"],
        },
        indent=2,
        sort_keys=True,
    )
)
