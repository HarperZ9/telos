"""Validate pass 0043 Lake dependency cache binding receipts."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "lake-dependency-cache-binding-pass-0043.json"
FIXTURE_PATH = ROOT / "fixtures" / "lake-dependency-cache-binding-pass-0043.json"
SOURCE_ARCHIVE_PACKET = ROOT / "schemas" / "full-lean-source-archive-pass-0042.json"
RESULT_PATH = ROOT / "schemas" / "pass-0043-lake-dependency-cache-binding-validator-result.json"


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
    configured = os.environ.get("PIPELINE_MATH_SOURCE_ROOT")
    if configured:
        return Path(configured)
    return Path(os.environ.get("TEMP", "")) / "pipeline-math-pass0032-lf"


def git_text(repo: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, encoding="utf-8").strip()


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    source_archive = load_json(SOURCE_ARCHIVE_PACKET)
    root = source_root()

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")
    if isinstance(contract, dict):
        require(contract.get("schema") == "LakeDependencyCacheBindingSet/v1", errors, "schema mismatch")
        require(contract.get("status") == "LAKE_DEPENDENCY_CACHE_BINDING_MATCH", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("full_source_archive_binding", {}).get("sha256") == sha256_file(SOURCE_ARCHIVE_PACKET), errors, "pass0042 sha mismatch")
        require(contract.get("full_source_archive_binding", {}).get("seal") == source_archive.get("seal"), errors, "pass0042 seal mismatch")
        require(contract.get("theorem_lake_dependency_cache_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(contract.get("theorem_lake_dependency_cache_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")
        measurements = contract.get("verifier_measurements", {})
        require(measurements.get("package_count") == 9, errors, "package count mismatch")
        require(measurements.get("present_package_count") == 9, errors, "present package count mismatch")
        require(measurements.get("head_match_count") == 9, errors, "head match count mismatch")
        require(measurements.get("clean_package_count") == 9, errors, "clean package count mismatch")
        require(measurements.get("all_package_heads_match_manifest") is True, errors, "package head mismatch")
        require(measurements.get("all_package_urls_match_manifest") is True, errors, "package url mismatch")
        require(measurements.get("compiled_replay_status") == "NOT_RUN", errors, "compiled replay overclaimed")
        for row in contract.get("dependency_packages", []):
            cache_path = Path(row["cache_path"])
            require(cache_path.exists(), errors, f"{row.get('name')} cache missing")
            if cache_path.exists():
                head = git_text(cache_path, ["rev-parse", "HEAD"])
                status_short = git_text(cache_path, ["status", "--short"])
                require(head == row.get("manifest_rev"), errors, f"{row.get('name')} head drift")
                require(status_short == "", errors, f"{row.get('name')} dirty")
            require(row.get("head_matches_manifest") is True, errors, f"{row.get('name')} recorded head mismatch")
            require(row.get("origin_url_matches_manifest") is True, errors, f"{row.get('name')} recorded url mismatch")
            require(row.get("clean") is True, errors, f"{row.get('name')} recorded dirty")
        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 8, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "LakeDependencyCacheBindingFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "artifact": "LakeDependencyCacheBindingSet",
                "errors": errors,
                "package_count": contract.get("verifier_measurements", {}).get("package_count") if isinstance(contract, dict) else None,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0043",
        "schema": "Pass0043LakeDependencyCacheBindingValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
