"""Validate pass 0040 content-addressed archive theorem statement replay receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "theorem-archived-blob-statement-replay-pass-0040.json"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-archived-blob-statement-replay-pass-0040.json"
REMOTE_PACKET = ROOT / "schemas" / "theorem-remote-blob-statement-replay-pass-0039.json"
RESULT_PATH = ROOT / "schemas" / "pass-0040-theorem-archived-blob-statement-replay-validator-result.json"


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
    remote_packet = load_json(REMOTE_PACKET)

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")
    if isinstance(contract, dict):
        require(contract.get("schema") == "TheoremArchivedBlobStatementReplaySet/v1", errors, "schema mismatch")
        require(contract.get("status") == "ARCHIVED_BLOB_STATEMENT_REPLAY_MATCH", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("remote_statement_replay_binding", {}).get("sha256") == sha256_file(REMOTE_PACKET), errors, "pass0039 sha mismatch")
        require(contract.get("remote_statement_replay_binding", {}).get("seal") == remote_packet.get("seal"), errors, "pass0039 seal mismatch")
        require(contract.get("theorem_archived_blob_statement_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(contract.get("theorem_archived_blob_statement_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")

        measurements = contract.get("verifier_measurements", {})
        require(measurements.get("theorem_count") == 10, errors, "theorem count mismatch")
        require(measurements.get("archive_check_count") == 10, errors, "archive check count mismatch")
        require(measurements.get("unique_archive_file_count") == len(contract.get("unique_archive_files", [])), errors, "archive file count mismatch")
        require(measurements.get("all_archive_statement_checks_match") is True, errors, "all archive statement checks false")
        require(measurements.get("all_archive_file_sha_match_pass0039") is True, errors, "archive sha pass0039 mismatch")
        require(measurements.get("external_call_required_for_replay") is False, errors, "archive replay should not require external call")
        require(measurements.get("worktree_text_used_for_signatures") is False, errors, "worktree text used as authority")

        for file_row in contract.get("unique_archive_files", []):
            archive_path = ROOT / file_row.get("archive_path", "")
            require(archive_path.exists(), errors, f"{file_row.get('git_path')} archive missing")
            if archive_path.exists():
                digest = sha256_file(archive_path)
                require(digest == file_row.get("archive_sha256"), errors, f"{file_row.get('git_path')} archive sha mismatch")
                require(digest == file_row.get("remote_raw_sha256"), errors, f"{file_row.get('git_path')} remote sha mismatch")
                require(digest == file_row.get("pass0038_blob_sha256"), errors, f"{file_row.get('git_path')} pass0038 sha mismatch")
        prior_rows = {row["theorem"]: row for row in remote_packet["remote_statement_checks"]}
        for row in contract.get("archive_statement_checks", []):
            theorem = row.get("theorem")
            prior = prior_rows.get(theorem, {})
            require(row.get("archive_signature_status") == "MATCH", errors, f"{theorem} archive signature drift")
            require(row.get("archive_frozen_solution_status") == "MATCH", errors, f"{theorem} archive frozen/solution drift")
            require(row.get("archive_frozen_proof_status") == "MATCH", errors, f"{theorem} archive frozen/proof drift")
            require(row.get("archive_discharge_status") == "MATCH", errors, f"{theorem} archive discharge drift")
            for ref_kind in ("frozen_statement", "solution_decl", "proof_decl"):
                ref = row.get("refs", {}).get(ref_kind, {})
                prior_ref = prior.get("refs", {}).get(ref_kind, {})
                require(bool(ref.get("archive_path")), errors, f"{theorem} {ref_kind} archive path missing")
                require(ref.get("canonical_signature") == prior_ref.get("canonical_signature"), errors, f"{theorem} {ref_kind} prior canonical mismatch")
                require(ref.get("archive_sha256") == ref.get("remote_raw_sha256"), errors, f"{theorem} {ref_kind} archive sha drift")
                require(ref.get("signature_status") == "MATCH", errors, f"{theorem} {ref_kind} status drift")
            discharge = row.get("refs", {}).get("discharge_gate", {})
            require(discharge.get("signature_status") == "MATCH", errors, f"{theorem} discharge status drift")
            require(discharge.get("archive_sha256") == discharge.get("remote_raw_sha256"), errors, f"{theorem} discharge archive sha drift")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 8, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "TheoremArchivedBlobStatementReplayFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "archive_check_count": contract.get("verifier_measurements", {}).get("archive_check_count") if isinstance(contract, dict) else None,
                "artifact": "TheoremArchivedBlobStatementReplaySet",
                "errors": errors,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "theorem_count": contract.get("verifier_measurements", {}).get("theorem_count") if isinstance(contract, dict) else None,
                "unique_archive_file_count": contract.get("verifier_measurements", {}).get("unique_archive_file_count") if isinstance(contract, dict) else None,
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0040",
        "schema": "Pass0040TheoremArchivedBlobStatementReplayValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
