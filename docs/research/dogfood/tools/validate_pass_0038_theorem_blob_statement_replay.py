"""Validate pass 0038 Git-blob theorem statement replay receipts."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "theorem-blob-statement-replay-pass-0038.json"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-blob-statement-replay-pass-0038.json"
SOURCE_REF_PACKET = ROOT / "schemas" / "theorem-source-ref-integrity-pass-0036.json"
STATEMENT_PACKET = ROOT / "schemas" / "theorem-statement-equivalence-pass-0037.json"
RESULT_PATH = ROOT / "schemas" / "pass-0038-theorem-blob-statement-replay-validator-result.json"


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


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    source_ref_packet = load_json(SOURCE_REF_PACKET)
    statement_packet = load_json(STATEMENT_PACKET)
    repo = source_root()

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")
    if isinstance(contract, dict):
        require(contract.get("schema") == "TheoremBlobStatementReplaySet/v1", errors, "schema mismatch")
        require(contract.get("status") == "BLOB_STATEMENT_REPLAY_MATCH", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("source_ref_integrity_binding", {}).get("sha256") == sha256_file(SOURCE_REF_PACKET), errors, "source ref sha mismatch")
        require(contract.get("source_ref_integrity_binding", {}).get("seal") == source_ref_packet.get("seal"), errors, "source ref seal mismatch")
        require(contract.get("statement_equivalence_binding", {}).get("sha256") == sha256_file(STATEMENT_PACKET), errors, "statement sha mismatch")
        require(contract.get("statement_equivalence_binding", {}).get("seal") == statement_packet.get("seal"), errors, "statement seal mismatch")
        require(contract.get("theorem_blob_statement_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(contract.get("theorem_blob_statement_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")

        rows = contract.get("blob_statement_checks", [])
        measurements = contract.get("verifier_measurements", {})
        require(repo.exists(), errors, f"source repo missing: {repo}")
        require(measurements.get("theorem_count") == 10, errors, "theorem count mismatch")
        require(measurements.get("blob_check_count") == 10, errors, "blob check count mismatch")
        require(measurements.get("unique_blob_file_count") == len(contract.get("unique_blob_files", [])), errors, "blob file count mismatch")
        require(measurements.get("all_blob_statement_checks_match") is True, errors, "all blob statement checks false")
        require(measurements.get("all_blob_file_sha_match_pass0036") is True, errors, "blob sha pass0036 mismatch")
        require(measurements.get("worktree_text_used_for_signatures") is False, errors, "worktree text used as authority")

        prior_rows = {row["theorem"]: row for row in statement_packet["statement_checks"]}
        for file_row in contract.get("unique_blob_files", []):
            git_path = file_row.get("git_path")
            if repo.exists() and git_path:
                blob = subprocess.check_output(["git", "-C", str(repo), "show", f"HEAD:{git_path}"])
                require(sha256_bytes(blob) == file_row.get("git_blob_sha256"), errors, f"{git_path} blob sha mismatch")
                require(file_row.get("git_blob_sha256") == file_row.get("pass0036_git_blob_sha256"), errors, f"{git_path} pass0036 blob sha mismatch")
                require(file_row.get("git_blob_id") == file_row.get("pass0036_git_blob_id"), errors, f"{git_path} pass0036 blob id mismatch")
        for row in rows:
            theorem = row.get("theorem")
            prior = prior_rows.get(theorem, {})
            require(row.get("blob_signature_status") == "MATCH", errors, f"{theorem} blob signature drift")
            require(row.get("blob_frozen_solution_status") == "MATCH", errors, f"{theorem} blob frozen/solution drift")
            require(row.get("blob_frozen_proof_status") == "MATCH", errors, f"{theorem} blob frozen/proof drift")
            require(row.get("blob_discharge_status") == "MATCH", errors, f"{theorem} blob discharge drift")
            for ref_kind, prior_key in (
                ("frozen_statement", "frozen_signature"),
                ("solution_decl", "solution_signature"),
                ("proof_decl", "proof_signature"),
            ):
                ref = row.get("refs", {}).get(ref_kind, {})
                prior_sig = prior.get(prior_key, {})
                require(bool(ref.get("signature_text")), errors, f"{theorem} {ref_kind} signature text missing")
                require(ref.get("canonical_signature") == prior_sig.get("canonical_signature"), errors, f"{theorem} {ref_kind} prior canonical mismatch")
                require(ref.get("signature_status") == "MATCH", errors, f"{theorem} {ref_kind} status drift")
                require(ref.get("blob_git_blob_sha256") == ref.get("pass0036_git_blob_sha256"), errors, f"{theorem} {ref_kind} blob sha drift")
            discharge = row.get("refs", {}).get("discharge_gate", {})
            require(discharge.get("signature_status") == "MATCH", errors, f"{theorem} discharge status drift")
            require(discharge.get("blob_git_blob_sha256") == discharge.get("pass0036_git_blob_sha256"), errors, f"{theorem} discharge blob sha drift")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 8, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "TheoremBlobStatementReplayFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "artifact": "TheoremBlobStatementReplaySet",
                "blob_check_count": contract.get("verifier_measurements", {}).get("blob_check_count") if isinstance(contract, dict) else None,
                "errors": errors,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "theorem_count": contract.get("verifier_measurements", {}).get("theorem_count") if isinstance(contract, dict) else None,
                "unique_blob_file_count": contract.get("verifier_measurements", {}).get("unique_blob_file_count") if isinstance(contract, dict) else None,
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0038",
        "schema": "Pass0038TheoremBlobStatementReplayValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
