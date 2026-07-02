"""Validate pass 0036 theorem source-reference integrity receipts."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


EXPECTED_COMMIT = "69d7df765a8f377a5e0628c6d36c088bce7642c9"
PROJECT_SUBDIR = "lean/problem-4b-formalization"
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "theorem-source-ref-integrity-pass-0036.json"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-source-ref-integrity-pass-0036.json"
SOURCE_PACKET = ROOT / "schemas" / "theorem-specific-proof-packets-pass-0035.json"
RESULT_PATH = ROOT / "schemas" / "pass-0036-theorem-source-ref-validator-result.json"


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


def load_json(path: Path) -> object:
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


def run_git(repo: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, encoding="utf-8").strip()


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    source_packet = load_json(SOURCE_PACKET)
    repo = source_root()

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")
    if isinstance(contract, dict):
        require(contract.get("schema") == "TheoremSourceRefIntegritySet/v1", errors, "schema mismatch")
        require(contract.get("status") == "SOURCE_REF_INTEGRITY_MATCH", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("source_ref_binding", {}).get("sha256") == sha256_file(SOURCE_PACKET), errors, "source packet sha mismatch")
        require(contract.get("source_ref_binding", {}).get("seal") == source_packet.get("seal"), errors, "source packet seal mismatch")
        require(contract.get("source_ref_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(contract.get("source_ref_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal reference mismatch")
        require(contract.get("repo_receipt", {}).get("commit") == EXPECTED_COMMIT, errors, "commit mismatch")
        require(contract.get("repo_receipt", {}).get("git_status_clean") is True, errors, "git status not clean")

        measurements = contract.get("verifier_measurements", {})
        require(measurements.get("theorem_count") == 10, errors, "theorem count mismatch")
        require(measurements.get("source_ref_count") == 40, errors, "source ref count mismatch")
        require(measurements.get("unique_file_count") == len(contract.get("unique_files", [])), errors, "unique file count mismatch")
        require(measurements.get("all_refs_match") is True, errors, "not all refs match")
        require(measurements.get("commit_match") is True, errors, "commit_match false")
        require(measurements.get("git_status_clean") is True, errors, "git_status_clean false")
        require(measurements.get("worktree_eol_lf") is True, errors, "worktree_eol_lf false")

        if repo.exists():
            require(run_git(repo, ["rev-parse", "HEAD"]) == EXPECTED_COMMIT, errors, "live repo commit mismatch")
            require(run_git(repo, ["status", "--short"]) == "", errors, "live repo dirty")
            file_map = {row["git_path"]: row for row in contract.get("unique_files", [])}
            for git_path, file_row in file_map.items():
                file_path = repo / git_path
                require(file_path.exists(), errors, f"{git_path} missing")
                if file_path.exists():
                    require(sha256_file(file_path) == file_row.get("worktree_sha256"), errors, f"{git_path} worktree sha mismatch")
                    blob_bytes = subprocess.check_output(["git", "-C", str(repo), "show", f"HEAD:{git_path}"])
                    require(sha256_bytes(blob_bytes) == file_row.get("git_blob_sha256"), errors, f"{git_path} git blob sha mismatch")
                    require(run_git(repo, ["rev-parse", f"HEAD:{git_path}"]) == file_row.get("git_blob_id"), errors, f"{git_path} blob id mismatch")

            for row in contract.get("source_ref_checks", []):
                file_path = repo / row.get("git_path", "")
                if not file_path.exists():
                    errors.append(f"{row.get('ref')} source file missing")
                    continue
                lines = file_path.read_text(encoding="utf-8").splitlines()
                line_no = row.get("line_no")
                require(isinstance(line_no, int) and 1 <= line_no <= len(lines), errors, f"{row.get('ref')} line out of range")
                if isinstance(line_no, int) and 1 <= line_no <= len(lines):
                    line_text = lines[line_no - 1]
                    require(line_text == row.get("line_text"), errors, f"{row.get('ref')} line text mismatch")
                    require(sha256_text(line_text) == row.get("line_text_sha256"), errors, f"{row.get('ref')} line sha mismatch")
                    require(row.get("line_status") == "MATCH", errors, f"{row.get('ref')} line status drift")
                    require(row.get("symbol_present") is True, errors, f"{row.get('ref')} symbol missing")
        else:
            errors.append(f"source repo missing: {repo}")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 8, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "TheoremSourceRefIntegrityFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "artifact": "TheoremSourceRefIntegritySet",
                "errors": errors,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "source_ref_count": contract.get("verifier_measurements", {}).get("source_ref_count") if isinstance(contract, dict) else None,
                "status": "MATCH" if not errors else "DRIFT",
                "unique_file_count": contract.get("verifier_measurements", {}).get("unique_file_count") if isinstance(contract, dict) else None,
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0036",
        "schema": "Pass0036TheoremSourceRefValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
