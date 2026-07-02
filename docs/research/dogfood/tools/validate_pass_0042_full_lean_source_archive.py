"""Validate pass 0042 full Lean source/build archive receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "full-lean-source-archive-pass-0042.json"
FIXTURE_PATH = ROOT / "fixtures" / "full-lean-source-archive-pass-0042.json"
TOOLCHAIN_PACKET = ROOT / "schemas" / "lean-toolchain-import-binding-pass-0041.json"
RESULT_PATH = ROOT / "schemas" / "pass-0042-full-lean-source-archive-validator-result.json"


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


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    packet = load_json(TOOLCHAIN_PACKET)

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")
    if isinstance(contract, dict):
        require(contract.get("schema") == "FullLeanSourceArchiveSet/v1", errors, "schema mismatch")
        require(contract.get("status") == "FULL_LEAN_SOURCE_ARCHIVE_MATCH", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("lean_toolchain_import_binding", {}).get("sha256") == sha256_file(TOOLCHAIN_PACKET), errors, "pass0041 sha mismatch")
        require(contract.get("lean_toolchain_import_binding", {}).get("seal") == packet.get("seal"), errors, "pass0041 seal mismatch")
        require(contract.get("theorem_full_lean_source_archive_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(contract.get("theorem_full_lean_source_archive_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")

        measurements = contract.get("verifier_measurements", {})
        require(measurements.get("lean_module_count") == 16, errors, "lean module count mismatch")
        require(measurements.get("build_file_count") == 6, errors, "build file count mismatch")
        require(measurements.get("role_record_count") == 22, errors, "role record count mismatch")
        require(measurements.get("unique_archive_file_count") == 21, errors, "unique archive file count mismatch")
        require(measurements.get("module_build_overlap_count") == 1, errors, "module/build overlap count mismatch")
        require(measurements.get("needed_for_compiled_replay_count") == 6, errors, "needed replay count mismatch")
        require(measurements.get("needed_for_compiled_replay_archived_count") == 6, errors, "needed replay archive count mismatch")
        require(measurements.get("all_archived_sha_match_pass0041") is True, errors, "archive sha pass0041 mismatch")
        require(measurements.get("compiled_replay_status") == "NOT_RUN", errors, "compiled replay overclaimed")
        require(measurements.get("external_call_required_for_replay") is False, errors, "replay should not require external call")
        require(contract.get("module_build_overlap") == ["lean/problem-4b-formalization/Prob4b.lean"], errors, "overlap file mismatch")
        require(contract.get("repo_receipt", {}).get("commit_match_pass0041") is True, errors, "commit mismatch")

        for row in contract.get("full_archive_files", []):
            archive_path = ROOT / row.get("archive_path", "")
            require(archive_path.exists(), errors, f"{row.get('git_path')} archive missing")
            if archive_path.exists():
                digest = sha256_file(archive_path)
                require(digest == row.get("archive_sha256"), errors, f"{row.get('git_path')} archive sha mismatch")
                require(digest == row.get("pass0041_sha256"), errors, f"{row.get('git_path')} pass0041 sha mismatch")
            require(row.get("sha_match_pass0041") is True, errors, f"{row.get('git_path')} sha match false")
            require(bool(row.get("roles")), errors, f"{row.get('git_path')} roles missing")

        module_paths = {row.get("git_path") for row in contract.get("lean_modules", [])}
        build_paths = {row.get("git_path") for row in contract.get("build_files", [])}
        require(len(module_paths) == 16, errors, "module path set mismatch")
        require(len(build_paths) == 6, errors, "build path set mismatch")
        require(set(contract.get("needed_for_compiled_replay_archived", [])) == set(packet.get("needed_for_compiled_replay", [])), errors, "needed replay delta not closed")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 8, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "FullLeanSourceArchiveFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "artifact": "FullLeanSourceArchiveSet",
                "errors": errors,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "role_record_count": contract.get("verifier_measurements", {}).get("role_record_count") if isinstance(contract, dict) else None,
                "status": "MATCH" if not errors else "DRIFT",
                "unique_archive_file_count": contract.get("verifier_measurements", {}).get("unique_archive_file_count") if isinstance(contract, dict) else None,
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0042",
        "schema": "Pass0042FullLeanSourceArchiveValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
