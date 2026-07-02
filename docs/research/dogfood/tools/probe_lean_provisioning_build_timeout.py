"""Generate pass 0033 Lean provisioning and build-timeout receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PASS = "0033"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "schemas" / "lean-replay-remediation-contract-pass-0032.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-provisioning-build-timeout-pass-0033.json"
OUT_PATH = ROOT / "schemas" / "lean-provisioning-build-timeout-pass-0033.json"


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


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def main() -> None:
    source = read_json(SOURCE_PATH)
    source_sha = sha256_file(SOURCE_PATH)
    source_seal = source["seal"]

    release_receipt = {
        "api_url": "https://api.github.com/repos/leanprover/elan/releases/latest",
        "asset": "elan-x86_64-pc-windows-msvc.zip",
        "asset_browser_download_url": "https://github.com/leanprover/elan/releases/download/v4.2.3/elan-x86_64-pc-windows-msvc.zip",
        "asset_bytes": 2389007,
        "asset_sha256": "be5e92a2dfdd8176099b2db0b810c27237c9054f1e5db1126f4f2a1134773b25",
        "elan_init_bytes": 5842944,
        "elan_init_sha256": "175089915efc623126a1560ed517cd52ec2d4d09f2adc1c10f22f56568fed5ad",
        "installer_help": {
            "default_toolchain_option": "--default-toolchain <default-toolchain>",
            "no_modify_path_flag": "--no-modify-path",
            "yes_flag": "-y"
        },
        "observed_at_local": "2026-07-01T06:07:00-07:00",
        "published_at": "2026-06-08T07:27:27Z",
        "release_tag": "v4.2.3",
        "release_url": "https://github.com/leanprover/elan/releases/tag/v4.2.3",
        "status": "MATCH"
    }

    contained_install_probe = {
        "bin_files": [
            "elan.exe",
            "lake.exe",
            "lean.exe",
            "leanc.exe",
            "leanchecker.exe",
            "leanmake.exe",
            "leanpkg.exe"
        ],
        "command": "elan-init.exe -y --no-modify-path --default-toolchain leanprover/lean4:v4.31.0",
        "default_toolchain": "leanprover/lean4:v4.31.0",
        "elan_home_ref": "temp:telos-pass0033-elan-home",
        "external_write_performed": False,
        "install_exit_code": 0,
        "normal_path_modified": False,
        "status": "MATCH",
        "temp_write_performed": True
    }

    toolchain_probe = {
        "elan_show": [
            "leanprover/lean4:v4.31.0 (overridden by lean-toolchain)",
            "Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)"
        ],
        "elan_version": "elan 4.2.3 (b6cec7e10 2026-06-08)",
        "lake_version": "Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)",
        "lean_version": "Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)",
        "status": "MATCH",
        "toolchain_commit": "68218e876d2a38b1985b8590fff244a83c321783"
    }

    build_timeout_probe = {
        "active_worker_count_range": {
            "max": 26,
            "min": 22
        },
        "build_artifacts": {
            "byte_sum": 3208367614,
            "file_count": 46930,
            "top_extensions": [
                {"count": 15955, "extension": ".hash"},
                {"count": 9341, "extension": ".lean"},
                {"count": 2702, "extension": ".json"},
                {"count": 2679, "extension": ".trace"},
                {"count": 2659, "extension": ".olean"},
                {"count": 2657, "extension": ".c"},
                {"count": 2657, "extension": ".server"},
                {"count": 2657, "extension": ".ir"},
                {"count": 2657, "extension": ".ilean"},
                {"count": 2657, "extension": ".private"}
            ]
        },
        "command": "scripts/verify.sh --no-log --all",
        "elapsed_timeout_seconds": 604,
        "failure_class": "mathlib_build_long_running_timeout",
        "lake_reached": True,
        "lean_workers_reached": True,
        "monitor_window_seconds": 600,
        "process_stop": {
            "remaining_count_after_stop": 0,
            "stop_scope": "processes whose command lines referenced temp Elan home, temp pipeline-math clone, or temp python3 shim",
            "stopped_count": 27
        },
        "semantic_failure_observed": False,
        "status": "TIMEOUT_TERMINATED",
        "theorem_replay_completed": False
    }

    public_source_receipts = [
        {
            "claim": "The Elan release page provides the Windows MSVC zip asset used in this contained probe.",
            "source": "elan GitHub release",
            "url": "https://github.com/leanprover/elan/releases/tag/v4.2.3",
            "verification_status": "observed"
        },
        {
            "claim": "Elan manages Lean toolchains and supplies Lean and Lake executables for a selected toolchain.",
            "source": "elan README",
            "url": "https://github.com/leanprover/elan",
            "verification_status": "verified"
        },
        {
            "claim": "Lean projects can use a lean-toolchain file to select the toolchain used by Elan.",
            "source": "Lean reference manual",
            "url": "https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/",
            "verification_status": "verified"
        }
    ]

    fixture = with_seal({
        "build_timeout_probe": build_timeout_probe,
        "contained_install_probe": contained_install_probe,
        "pass": PASS,
        "public_source_receipts": public_source_receipts,
        "release_receipt": release_receipt,
        "schema": "LeanProvisioningBuildTimeoutFixture/v1",
        "source_remediation_ref": "schemas/lean-replay-remediation-contract-pass-0032.json",
        "source_remediation_seal": source_seal,
        "source_remediation_sha256": source_sha,
        "toolchain_probe": toolchain_probe
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)

    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0033_lean_provisioning_build_timeout",
            "authority_class": "contained_temp_toolchain_probe",
            "event_id": "evt_dogfood_0033_lean_provisioning_build_timeout",
            "event_type": "lean_provisioning_build_timeout_recorded",
            "external_write_performed": False,
            "normal_path_modified": False,
            "replay_promotion_allowed": False,
            "result_state": "failed",
            "side_effect_class": "temp_write_and_process_execution",
            "stop_reason": "budget_timeout",
            "toolchain_install_scope": "temp_elan_home",
            "verification_verdict": "MATCH"
        },
        "build_timeout_probe": build_timeout_probe,
        "contained_install_probe": contained_install_probe,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "negative_fixture_count": 10,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-temp-install-claimed-system-install"},
            {"expected_validator_status": "REJECT", "id": "negative-no-modify-path-omitted"},
            {"expected_validator_status": "REJECT", "id": "negative-elan-home-not-temp"},
            {"expected_validator_status": "REJECT", "id": "negative-zip-hash-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-lean-version-promoted-without-probe"},
            {"expected_validator_status": "REJECT", "id": "negative-lake-build-promoted-after-timeout"},
            {"expected_validator_status": "REJECT", "id": "negative-timeout-processes-left-running"},
            {"expected_validator_status": "REJECT", "id": "negative-theorem-replay-promoted"},
            {"expected_validator_status": "REJECT", "id": "negative-build-timeout-called-semantic-failure"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "next_actions": [
            "resume or rebuild from the partial temp .lake cache only under a new bounded receipt",
            "try lake exe cache get before building Mathlib locally",
            "separate dependency build from theorem replay and theorem-specific checks",
            "record CPU, wall time, memory, and output digests for every bounded replay attempt"
        ],
        "non_promotion_statement": "Pass 0033 proves contained toolchain provisioning and a long-running Mathlib build timeout only. It does not prove Lake build success, theorem replay, theorem correctness, or any natural law.",
        "pass": PASS,
        "provisioning_fixture": {
            "path": "fixtures/lean-provisioning-build-timeout-pass-0033.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha
        },
        "public_source_receipts": public_source_receipts,
        "release_receipt": release_receipt,
        "schema": "LeanProvisioningBuildTimeoutContract/v1",
        "source_remediation_binding": {
            "path": "schemas/lean-replay-remediation-contract-pass-0032.json",
            "seal": source_seal,
            "sha256": source_sha,
            "source_status": source["status"]
        },
        "status": "LEAN_PROVISIONING_MATCH_WITH_BUILD_TIMEOUT",
        "toolchain_probe": toolchain_probe,
        "verifier_measurements": {
            "build_artifact_bytes": build_timeout_probe["build_artifacts"]["byte_sum"],
            "build_artifact_files": build_timeout_probe["build_artifacts"]["file_count"],
            "contained_install_status": contained_install_probe["status"],
            "external_write_performed": False,
            "lake_reached": True,
            "lake_version_status": "MATCH",
            "lean_version_status": "MATCH",
            "processes_remaining_after_stop": 0,
            "semantic_failure_observed": False,
            "temp_write_performed": True,
            "theorem_replay_completed": False,
            "timeout_status": build_timeout_probe["status"],
            "toolchain_install_scope": "temp_elan_home"
        }
    })
    write_json(OUT_PATH, contract)

    print(json.dumps({
        "build_artifact_files": build_timeout_probe["build_artifacts"]["file_count"],
        "path": str(OUT_PATH),
        "schema": contract["schema"],
        "seal": contract["seal"],
        "status": contract["status"],
        "timeout_status": build_timeout_probe["status"],
        "toolchain": toolchain_probe["lean_version"]
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
