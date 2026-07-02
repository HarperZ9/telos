"""Validate pass 0041 Lean toolchain and import-graph binding receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "lean-toolchain-import-binding-pass-0041.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-toolchain-import-binding-pass-0041.json"
ARCHIVE_PACKET = ROOT / "schemas" / "theorem-archived-blob-statement-replay-pass-0040.json"
RESULT_PATH = ROOT / "schemas" / "pass-0041-lean-toolchain-import-binding-validator-result.json"


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
    archive_packet = load_json(ARCHIVE_PACKET)

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")
    if isinstance(contract, dict):
        require(contract.get("schema") == "LeanToolchainImportBindingSet/v1", errors, "schema mismatch")
        require(contract.get("status") == "LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("archive_statement_replay_binding", {}).get("sha256") == sha256_file(ARCHIVE_PACKET), errors, "pass0040 sha mismatch")
        require(contract.get("archive_statement_replay_binding", {}).get("seal") == archive_packet.get("seal"), errors, "pass0040 seal mismatch")
        require(contract.get("theorem_lean_toolchain_import_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(contract.get("theorem_lean_toolchain_import_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")

        measurements = contract.get("verifier_measurements", {})
        require(measurements.get("build_file_count") == 6, errors, "build file count mismatch")
        require(measurements.get("lean_module_count") == 16, errors, "lean module count mismatch")
        require(measurements.get("archived_source_file_count") == 10, errors, "archive source file count mismatch")
        require(measurements.get("needed_for_compiled_replay_count") == 6, errors, "compiled replay delta mismatch")
        require(measurements.get("commit_match_pass0036") is True, errors, "commit mismatch")
        require(measurements.get("toolchain_bound") is True, errors, "toolchain not bound")
        require(measurements.get("compiled_replay_status") == "NOT_RUN", errors, "compiled replay overclaimed")
        require(measurements.get("worktree_text_used_for_signatures") is False, errors, "worktree text used as theorem signature authority")
        require(contract.get("toolchain_summary", {}).get("toolchain") == "leanprover/lean4:v4.31.0", errors, "toolchain version mismatch")
        require(contract.get("toolchain_summary", {}).get("mathlib_input_rev") == "v4.31.0", errors, "mathlib input rev mismatch")
        require(bool(contract.get("toolchain_summary", {}).get("mathlib_rev")), errors, "mathlib rev missing")
        require(len(contract.get("build_files", [])) == 6, errors, "build files missing")
        require(len(contract.get("lean_modules", [])) == 16, errors, "lean modules missing")
        require(len(contract.get("needed_for_compiled_replay", [])) == 6, errors, "needed delta list mismatch")
        require(any(edge.get("kind") == "external" and edge.get("to") == "Mathlib" for edge in contract.get("import_edges", [])), errors, "Mathlib external import missing")
        require(any(edge.get("from") == "Prob4b" and edge.get("to") == "Prob4b.Solution" for edge in contract.get("import_edges", [])), errors, "root Solution import missing")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 8, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "LeanToolchainImportBindingFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "artifact": "LeanToolchainImportBindingSet",
                "build_file_count": contract.get("verifier_measurements", {}).get("build_file_count") if isinstance(contract, dict) else None,
                "errors": errors,
                "lean_module_count": contract.get("verifier_measurements", {}).get("lean_module_count") if isinstance(contract, dict) else None,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0041",
        "schema": "Pass0041LeanToolchainImportBindingValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
