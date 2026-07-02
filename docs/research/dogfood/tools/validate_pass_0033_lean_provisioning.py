"""Validate pass 0033 Lean provisioning and build-timeout receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "lean-provisioning-build-timeout-pass-0033.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-provisioning-build-timeout-pass-0033.json"
SOURCE_PATH = ROOT / "schemas" / "lean-replay-remediation-contract-pass-0032.json"
RESULT_PATH = ROOT / "schemas" / "pass-0033-lean-provisioning-validator-result.json"


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
        require(contract.get("schema") == "LeanProvisioningBuildTimeoutContract/v1", errors, "schema mismatch")
        require(contract.get("status") == "LEAN_PROVISIONING_MATCH_WITH_BUILD_TIMEOUT", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("source_remediation_binding", {}).get("sha256") == sha256_file(SOURCE_PATH), errors, "source sha mismatch")
        require(contract.get("source_remediation_binding", {}).get("seal") == source.get("seal"), errors, "source seal mismatch")

        release = contract.get("release_receipt", {})
        require(release.get("release_tag") == "v4.2.3", errors, "release tag mismatch")
        require(release.get("asset_sha256") == "be5e92a2dfdd8176099b2db0b810c27237c9054f1e5db1126f4f2a1134773b25", errors, "zip hash mismatch")
        require(release.get("elan_init_sha256") == "175089915efc623126a1560ed517cd52ec2d4d09f2adc1c10f22f56568fed5ad", errors, "elan-init hash mismatch")
        require(release.get("installer_help", {}).get("no_modify_path_flag") == "--no-modify-path", errors, "no-modify-path flag missing")

        install = contract.get("contained_install_probe", {})
        require(install.get("install_exit_code") == 0, errors, "install exit mismatch")
        require(install.get("elan_home_ref") == "temp:telos-pass0033-elan-home", errors, "ELAN_HOME not temp")
        require(install.get("normal_path_modified") is False, errors, "normal path modified")
        require(install.get("external_write_performed") is False, errors, "external write hidden")
        require("lake.exe" in install.get("bin_files", []), errors, "lake proxy missing")
        require("lean.exe" in install.get("bin_files", []), errors, "lean proxy missing")

        toolchain = contract.get("toolchain_probe", {})
        require("Lean (version 4.31.0" in toolchain.get("lean_version", ""), errors, "Lean version mismatch")
        require("Lake version 5.0.0-src+68218e8" in toolchain.get("lake_version", ""), errors, "Lake version mismatch")
        require(toolchain.get("toolchain_commit") == "68218e876d2a38b1985b8590fff244a83c321783", errors, "toolchain commit mismatch")

        timeout = contract.get("build_timeout_probe", {})
        require(timeout.get("status") == "TIMEOUT_TERMINATED", errors, "timeout status mismatch")
        require(timeout.get("lake_reached") is True, errors, "Lake not reached")
        require(timeout.get("lean_workers_reached") is True, errors, "Lean workers not reached")
        require(timeout.get("theorem_replay_completed") is False, errors, "theorem replay promoted")
        require(timeout.get("semantic_failure_observed") is False, errors, "semantic failure promoted")
        require(timeout.get("process_stop", {}).get("remaining_count_after_stop") == 0, errors, "processes left running")
        require(timeout.get("build_artifacts", {}).get("file_count") == 46930, errors, "build file count mismatch")
        require(timeout.get("build_artifacts", {}).get("byte_sum") == 3208367614, errors, "build byte sum mismatch")

        fixture_ref = contract.get("provisioning_fixture", {})
        require(fixture_ref.get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(fixture_ref.get("seal") == fixture.get("seal"), errors, "fixture seal reference mismatch")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 10, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")

        measurements = contract.get("verifier_measurements", {})
        require(measurements.get("toolchain_install_scope") == "temp_elan_home", errors, "install scope mismatch")
        require(measurements.get("lake_reached") is True, errors, "measurement lake reached mismatch")
        require(measurements.get("theorem_replay_completed") is False, errors, "measurement theorem replay promoted")
        require(measurements.get("processes_remaining_after_stop") == 0, errors, "measurement processes remaining")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "LeanProvisioningBuildTimeoutFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "artifact": "LeanProvisioningBuildTimeoutContract",
                "build_artifact_bytes": contract.get("build_timeout_probe", {}).get("build_artifacts", {}).get("byte_sum") if isinstance(contract, dict) else None,
                "build_artifact_files": contract.get("build_timeout_probe", {}).get("build_artifacts", {}).get("file_count") if isinstance(contract, dict) else None,
                "contained_install_status": contract.get("contained_install_probe", {}).get("status") if isinstance(contract, dict) else None,
                "errors": errors,
                "lake_reached": contract.get("build_timeout_probe", {}).get("lake_reached") if isinstance(contract, dict) else None,
                "lake_version": contract.get("toolchain_probe", {}).get("lake_version") if isinstance(contract, dict) else None,
                "lean_version": contract.get("toolchain_probe", {}).get("lean_version") if isinstance(contract, dict) else None,
                "negative_fixture_count": len(contract.get("negative_fixtures", [])) if isinstance(contract, dict) else 0,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "processes_remaining_after_stop": contract.get("build_timeout_probe", {}).get("process_stop", {}).get("remaining_count_after_stop") if isinstance(contract, dict) else None,
                "status": "MATCH" if not errors else "DRIFT",
                "theorem_replay_completed": contract.get("build_timeout_probe", {}).get("theorem_replay_completed") if isinstance(contract, dict) else None,
                "timeout_status": contract.get("build_timeout_probe", {}).get("status") if isinstance(contract, dict) else None
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0033",
        "schema": "Pass0033LeanProvisioningValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
