"""Validate pass 0044 Lean/Lake executable preflight receipts."""

from __future__ import annotations

import hashlib
import json
import shutil
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "lean-lake-executable-preflight-pass-0044.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-lake-executable-preflight-pass-0044.json"
PREVIOUS_PACKET = ROOT / "schemas" / "lake-dependency-cache-binding-pass-0043.json"
RESULT_PATH = ROOT / "schemas" / "pass-0044-lean-lake-executable-preflight-validator-result.json"
PROJECT_SUBDIR = "lean/problem-4b-formalization"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def check_seal(value: dict) -> bool:
    copy = dict(value)
    seal = copy.pop("seal", None)
    return seal == sha256_obj(copy)


def source_root() -> Path:
    import os
    configured = os.environ.get("PIPELINE_MATH_SOURCE_ROOT")
    if configured:
        return Path(configured)
    return Path(os.environ.get("TEMP", "")) / "pipeline-math-pass0032-lf"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def load_lakefile(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    previous = load_json(PREVIOUS_PACKET)
    project_root = source_root() / PROJECT_SUBDIR
    lean_toolchain = (project_root / "lean-toolchain").read_text(encoding="utf-8").strip()
    lake_manifest = load_json(project_root / "lake-manifest.json")
    lakefile = load_lakefile(project_root / "lakefile.toml")

    require(contract.get("schema") == "LeanLakeExecutablePreflightSet/v1", errors, "schema mismatch")
    require(contract.get("status") == "LEAN_LAKE_EXECUTABLE_PREFLIGHT_BLOCKED", errors, "status mismatch")
    require(check_seal(contract), errors, "contract seal mismatch")
    require(fixture.get("schema") == "LeanLakeExecutablePreflightFixture/v1", errors, "fixture schema mismatch")
    require(check_seal(fixture), errors, "fixture seal mismatch")
    require(contract.get("dependency_cache_binding", {}).get("sha256") == sha256_file(PREVIOUS_PACKET), errors, "pass0043 sha mismatch")
    require(contract.get("dependency_cache_binding", {}).get("seal") == previous.get("seal"), errors, "pass0043 seal mismatch")
    require(contract.get("executable_preflight_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(contract.get("executable_preflight_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")

    measurements = contract.get("verifier_measurements", {})
    require(measurements.get("expected_toolchain") == lean_toolchain, errors, "toolchain mismatch")
    require(measurements.get("lake_manifest_package_count") == len(lake_manifest.get("packages", [])), errors, "manifest package count mismatch")
    require(measurements.get("lakefile_name") == lakefile.get("name"), errors, "lakefile name mismatch")
    require(measurements.get("manifest_name") == lake_manifest.get("name"), errors, "manifest name mismatch")
    require(measurements.get("project_name_match") == (lakefile.get("name") == lake_manifest.get("name")), errors, "project name match mismatch")
    require(measurements.get("compiled_replay_status") == "NOT_RUN", errors, "compiled replay overclaimed")
    require(measurements.get("compiled_replay_admissible") is False, errors, "compiled replay marked admissible")
    require(measurements.get("lake_on_path") is (shutil.which("lake") is not None), errors, "lake PATH result drift")
    require(measurements.get("lean_on_path") is (shutil.which("lean") is not None), errors, "lean PATH result drift")
    require(measurements.get("elan_on_path") is (shutil.which("elan") is not None), errors, "elan PATH result drift")
    require(measurements.get("lake_on_path") is False, errors, "lake unexpectedly on PATH")
    require(measurements.get("lean_on_path") is False, errors, "lean unexpectedly on PATH")
    require(measurements.get("elan_on_path") is False, errors, "elan unexpectedly on PATH")
    require(measurements.get("common_elan_candidates_present") == 0, errors, "common Elan candidate drift")
    require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    require(len(contract.get("negative_fixtures", [])) == 6, errors, "negative fixture count mismatch")
    for row in contract.get("negative_fixtures", []):
        require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")

    result = {
        "checks": [
            {
                "artifact": "LeanLakeExecutablePreflightSet",
                "compiled_replay_admissible": measurements.get("compiled_replay_admissible"),
                "errors": errors,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0044",
        "schema": "Pass0044LeanLakeExecutablePreflightValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
