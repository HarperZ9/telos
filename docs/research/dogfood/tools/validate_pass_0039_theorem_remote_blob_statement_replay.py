"""Validate pass 0039 remote raw-blob theorem statement replay receipts."""

from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "theorem-remote-blob-statement-replay-pass-0039.json"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-remote-blob-statement-replay-pass-0039.json"
SOURCE_REF_PACKET = ROOT / "schemas" / "theorem-source-ref-integrity-pass-0036.json"
BLOB_PACKET = ROOT / "schemas" / "theorem-blob-statement-replay-pass-0038.json"
RESULT_PATH = ROOT / "schemas" / "pass-0039-theorem-remote-blob-statement-replay-validator-result.json"


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


def fetch_raw(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "telos-dogfood-pass-0039-validator"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    source_ref_packet = load_json(SOURCE_REF_PACKET)
    blob_packet = load_json(BLOB_PACKET)

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")
    if isinstance(contract, dict):
        require(contract.get("schema") == "TheoremRemoteBlobStatementReplaySet/v1", errors, "schema mismatch")
        require(contract.get("status") == "REMOTE_BLOB_STATEMENT_REPLAY_MATCH", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("source_ref_integrity_binding", {}).get("sha256") == sha256_file(SOURCE_REF_PACKET), errors, "source ref sha mismatch")
        require(contract.get("source_ref_integrity_binding", {}).get("seal") == source_ref_packet.get("seal"), errors, "source ref seal mismatch")
        require(contract.get("blob_statement_replay_binding", {}).get("sha256") == sha256_file(BLOB_PACKET), errors, "pass0038 sha mismatch")
        require(contract.get("blob_statement_replay_binding", {}).get("seal") == blob_packet.get("seal"), errors, "pass0038 seal mismatch")
        require(contract.get("theorem_remote_blob_statement_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(contract.get("theorem_remote_blob_statement_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")

        measurements = contract.get("verifier_measurements", {})
        rows = contract.get("remote_statement_checks", [])
        require(measurements.get("theorem_count") == 10, errors, "theorem count mismatch")
        require(measurements.get("remote_check_count") == 10, errors, "remote check count mismatch")
        require(measurements.get("unique_remote_file_count") == len(contract.get("unique_remote_files", [])), errors, "remote file count mismatch")
        require(measurements.get("all_remote_statement_checks_match") is True, errors, "all remote statement checks false")
        require(measurements.get("all_remote_file_sha_match_pass0038") is True, errors, "remote sha pass0038 mismatch")
        require(measurements.get("external_call_performed") is True, errors, "external call flag missing")
        require(measurements.get("worktree_text_used_for_signatures") is False, errors, "worktree text used as authority")

        for file_row in contract.get("unique_remote_files", []):
            url = file_row.get("remote_url")
            require(bool(url), errors, f"{file_row.get('git_path')} remote URL missing")
            if url:
                try:
                    body = fetch_raw(url)
                    remote_sha = sha256_bytes(body)
                except Exception as exc:  # pragma: no cover - records network failure as data.
                    errors.append(f"{file_row.get('git_path')} remote fetch failed: {exc}")
                    continue
                require(remote_sha == file_row.get("remote_raw_sha256"), errors, f"{file_row.get('git_path')} remote sha mismatch")
                require(remote_sha == file_row.get("pass0038_blob_sha256"), errors, f"{file_row.get('git_path')} pass0038 sha mismatch")
                require(remote_sha == file_row.get("pass0036_git_blob_sha256"), errors, f"{file_row.get('git_path')} pass0036 sha mismatch")

        prior_rows = {row["theorem"]: row for row in blob_packet["blob_statement_checks"]}
        for row in rows:
            theorem = row.get("theorem")
            prior = prior_rows.get(theorem, {})
            require(row.get("remote_signature_status") == "MATCH", errors, f"{theorem} remote signature drift")
            require(row.get("remote_frozen_solution_status") == "MATCH", errors, f"{theorem} remote frozen/solution drift")
            require(row.get("remote_frozen_proof_status") == "MATCH", errors, f"{theorem} remote frozen/proof drift")
            require(row.get("remote_discharge_status") == "MATCH", errors, f"{theorem} remote discharge drift")
            for ref_kind in ("frozen_statement", "solution_decl", "proof_decl"):
                ref = row.get("refs", {}).get(ref_kind, {})
                prior_ref = prior.get("refs", {}).get(ref_kind, {})
                require(bool(ref.get("remote_url")), errors, f"{theorem} {ref_kind} remote URL missing")
                require(ref.get("canonical_signature") == prior_ref.get("canonical_signature"), errors, f"{theorem} {ref_kind} prior canonical mismatch")
                require(ref.get("remote_raw_sha256") == ref.get("pass0038_blob_sha256"), errors, f"{theorem} {ref_kind} remote sha drift")
                require(ref.get("signature_status") == "MATCH", errors, f"{theorem} {ref_kind} status drift")
            discharge = row.get("refs", {}).get("discharge_gate", {})
            require(discharge.get("signature_status") == "MATCH", errors, f"{theorem} discharge status drift")
            require(discharge.get("remote_raw_sha256") == discharge.get("pass0038_blob_sha256"), errors, f"{theorem} discharge remote sha drift")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 8, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "TheoremRemoteBlobStatementReplayFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "artifact": "TheoremRemoteBlobStatementReplaySet",
                "errors": errors,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "remote_check_count": contract.get("verifier_measurements", {}).get("remote_check_count") if isinstance(contract, dict) else None,
                "status": "MATCH" if not errors else "DRIFT",
                "theorem_count": contract.get("verifier_measurements", {}).get("theorem_count") if isinstance(contract, dict) else None,
                "unique_remote_file_count": contract.get("verifier_measurements", {}).get("unique_remote_file_count") if isinstance(contract, dict) else None,
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0039",
        "schema": "Pass0039TheoremRemoteBlobStatementReplayValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
