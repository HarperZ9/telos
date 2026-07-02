"""Generate pass 0040 content-addressed archive theorem statement replay receipts."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from pathlib import Path


PASS = "0040"
ROOT = Path(__file__).resolve().parents[1]
REMOTE_PACKET = ROOT / "schemas" / "theorem-remote-blob-statement-replay-pass-0039.json"
ARCHIVE_ROOT = ROOT / "archives" / "pass-0040-remote-blobs" / "sha256"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-archived-blob-statement-replay-pass-0040.json"
OUT_PATH = ROOT / "schemas" / "theorem-archived-blob-statement-replay-pass-0040.json"
PACKET_PATH = ROOT / "packets" / "050-theorem-archived-blob-statement-replay.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0040-archived-blob-statement-replay-steelman.md"


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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_bytes(path: Path, body: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def fetch_raw(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "telos-dogfood-pass-0040"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def canonical_signature(signature_text: str) -> str:
    one_line = re.sub(r"\s+", " ", signature_text).strip()
    match = re.match(r"^(theorem|lemma)\s+\S+\s*(.*)$", one_line)
    if match:
        return match.group(2).strip()
    return one_line


def extract_signature(text: str, line_no: int) -> dict:
    lines = text.splitlines()
    parts: list[str] = []
    end_line = line_no
    for idx in range(line_no - 1, len(lines)):
        line = lines[idx].rstrip()
        end_line = idx + 1
        if ":=" in line:
            before = line.split(":=", 1)[0].rstrip()
            if before:
                parts.append(before)
            break
        parts.append(line)
    signature_text = "\n".join(parts).strip()
    return {
        "canonical_signature": canonical_signature(signature_text),
        "signature_sha256": sha256_text(signature_text),
        "signature_span": [line_no, end_line],
        "signature_text": signature_text,
    }


def check_discharge(text: str, line_no: int, theorem: str) -> dict:
    lines = text.splitlines()
    line_text = lines[line_no - 1].strip()
    normalized = re.sub(r"\s+", " ", line_text)
    ok = f"@{theorem} = @{theorem}_proof" in normalized and normalized.endswith(":= rfl")
    return {
        "archive_discharge_status": "MATCH" if ok else "DRIFT",
        "line_text": line_text,
        "line_text_sha256": sha256_text(line_text),
        "normalized_line": normalized,
    }


def archive_remote_files(remote_packet: dict) -> dict[str, dict]:
    archives: dict[str, dict] = {}
    for row in remote_packet["unique_remote_files"]:
        body = fetch_raw(row["remote_url"])
        digest = sha256_bytes(body)
        archive_path = ARCHIVE_ROOT / f"{digest}.lean"
        write_bytes(archive_path, body)
        text = body.decode("utf-8")
        archives[row["git_path"]] = {
            "archive_path": str(archive_path.relative_to(ROOT)).replace("\\", "/"),
            "archive_sha256": digest,
            "byte_count": len(body),
            "capture_status": "MATCH" if digest == row["remote_raw_sha256"] else "DRIFT",
            "commit": row["commit"],
            "git_path": row["git_path"],
            "line_count": len(text.splitlines()),
            "pass0038_blob_sha256": row["pass0038_blob_sha256"],
            "remote_raw_sha256": row["remote_raw_sha256"],
            "remote_url": row["remote_url"],
            "text": text,
        }
    return archives


def build_rows(remote_packet: dict, archives: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for prior in remote_packet["remote_statement_checks"]:
        theorem = prior["theorem"]
        row: dict = {
            "archive_discharge_status": "DRIFT",
            "archive_frozen_proof_status": "DRIFT",
            "archive_frozen_solution_status": "DRIFT",
            "archive_signature_status": "DRIFT",
            "refs": {},
            "theorem": theorem,
        }
        for ref_kind in ("frozen_statement", "solution_decl", "proof_decl"):
            prior_ref = prior["refs"][ref_kind]
            archive = archives[prior_ref["git_path"]]
            sig = extract_signature(archive["text"], prior_ref["line_no"])
            status = "MATCH" if sig["canonical_signature"] == prior_ref["canonical_signature"] else "DRIFT"
            row["refs"][ref_kind] = {
                "archive_path": archive["archive_path"],
                "archive_sha256": archive["archive_sha256"],
                "canonical_signature": sig["canonical_signature"],
                "git_path": prior_ref["git_path"],
                "line_no": prior_ref["line_no"],
                "pass0038_blob_sha256": archive["pass0038_blob_sha256"],
                "prior_canonical_signature": prior_ref["canonical_signature"],
                "ref": prior_ref["ref"],
                "remote_raw_sha256": archive["remote_raw_sha256"],
                "signature_sha256": sig["signature_sha256"],
                "signature_span": sig["signature_span"],
                "signature_status": status,
                "signature_text": sig["signature_text"],
            }
        discharge_prior = prior["refs"]["discharge_gate"]
        discharge_archive = archives[discharge_prior["git_path"]]
        discharge = check_discharge(discharge_archive["text"], discharge_prior["line_no"], theorem)
        row["refs"]["discharge_gate"] = {
            "archive_path": discharge_archive["archive_path"],
            "archive_sha256": discharge_archive["archive_sha256"],
            "git_path": discharge_prior["git_path"],
            "line_no": discharge_prior["line_no"],
            "line_text": discharge["line_text"],
            "line_text_sha256": discharge["line_text_sha256"],
            "normalized_line": discharge["normalized_line"],
            "pass0038_blob_sha256": discharge_archive["pass0038_blob_sha256"],
            "ref": discharge_prior["ref"],
            "remote_raw_sha256": discharge_archive["remote_raw_sha256"],
            "signature_status": discharge["archive_discharge_status"],
        }
        frozen = row["refs"]["frozen_statement"]["canonical_signature"]
        solution = row["refs"]["solution_decl"]["canonical_signature"]
        proof = row["refs"]["proof_decl"]["canonical_signature"]
        row["archive_frozen_solution_status"] = "MATCH" if frozen == solution else "DRIFT"
        row["archive_frozen_proof_status"] = "MATCH" if frozen == proof else "DRIFT"
        row["archive_discharge_status"] = discharge["archive_discharge_status"]
        row["archive_signature_status"] = (
            "MATCH"
            if row["archive_frozen_solution_status"] == "MATCH"
            and row["archive_frozen_proof_status"] == "MATCH"
            and row["archive_discharge_status"] == "MATCH"
            else "DRIFT"
        )
        rows.append(row)
    archive_files = [
        {key: value for key, value in archive.items() if key != "text"}
        for archive in archives.values()
    ]
    return rows, archive_files


def render_packet(contract: dict) -> str:
    table = "\n".join(
        f"| `{row['theorem']}` | `{row['archive_frozen_solution_status']}` | `{row['archive_frozen_proof_status']}` | `{row['archive_discharge_status']}` | `{row['archive_signature_status']}` |"
        for row in contract["archive_statement_checks"]
    )
    return f"""# Packet 050: Theorem Archived Blob Statement Replay

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0040 captures the pass 0039 remote raw bytes into a local
content-addressed archive, then replays the theorem statement-signature checks
from those archived bytes.

## Source Binding

```text
source = schemas/theorem-remote-blob-statement-replay-pass-0039.json
source_sha256 = {contract['remote_statement_replay_binding']['sha256']}
source_seal = {contract['remote_statement_replay_binding']['seal']}
archive_root = archives/pass-0040-remote-blobs/sha256
theorem_count = {contract['verifier_measurements']['theorem_count']}
archive_check_count = {contract['verifier_measurements']['archive_check_count']}
unique_archive_file_count = {contract['verifier_measurements']['unique_archive_file_count']}
```

## Archive Replay Checks

| Theorem | Archive frozen vs solution | Archive frozen vs proof | Archive discharge gate | Overall |
| --- | --- | --- | --- | --- |
{table}

## Product Reading

This pass converts remote proof-packet dependencies into local
content-addressed evidence. After capture, a verifier can replay the statement
checks from archive paths and SHA-256 digests without relying on GitHub, a temp
checkout, or a local Git object database.

## Non-Promotion Boundary

Pass 0040 checks archived raw-source replay by digest. It does not re-run Lean,
prove semantic equivalence by elaboration, prove an axiom-free result, validate
every public `pipeline-math` claim, or promote any natural law.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0040 Steelman: Archived Blob Statement Replay

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0040 claims theorem statement-signature checks can replay from a local
content-addressed archive after remote capture.

## Strongest Objections

1. Capture still depends on GitHub availability.

Correct. The archive removes remote dependence after capture, but the capture
step still needs source availability or a mirror.

2. The archive stores source text, not compiled proof evidence.

Correct. This is a source-provenance layer. It is not Lean kernel replay.

3. File names by SHA-256 are not a complete supply-chain proof.

Correct. They make byte identity portable. A stronger layer should add mirror
attestations, signatures, and toolchain receipts.

4. The pass inherits pass 0039 signature extraction.

Correct. Pass 0040 tests archive portability, not new theorem semantics.

## Verdict

Useful for portable proof packets and offline review. Still bounded to
source-signature replay, not semantic proof verification.
"""


def main() -> None:
    remote_packet = read_json(REMOTE_PACKET)
    remote_packet_sha = sha256_file(REMOTE_PACKET)
    archives = archive_remote_files(remote_packet)
    checks, archive_files = build_rows(remote_packet, archives)
    all_match = all(row["archive_signature_status"] == "MATCH" for row in checks)
    all_archive_sha_match = all(row["archive_sha256"] == row["remote_raw_sha256"] == row["pass0038_blob_sha256"] for row in archive_files)
    fixture = with_seal({
        "archive_statement_checks": checks,
        "generated_on": "2026-07-01",
        "pass": PASS,
        "schema": "TheoremArchivedBlobStatementReplayFixture/v1",
        "theorem_remote_blob_statement_replay_sha256": remote_packet_sha,
        "unique_archive_files": archive_files,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0040_archived_blob_statement_replay",
            "authority_class": "read_only_archived_blob_signature_replay",
            "event_id": "evt_dogfood_0040_archived_blob_statement_replay",
            "event_type": "theorem_archived_blob_statement_replay_verified",
            "external_call_performed_for_capture": True,
            "external_call_required_for_replay": False,
            "external_write_performed": False,
            "normal_path_modified": False,
            "result_state": "completed",
            "side_effect_class": "external_read_then_local_archive_write",
            "stop_reason": "completed",
            "verification_verdict": "MATCH" if all_match and all_archive_sha_match else "DRIFT",
        },
        "archive_source": {
            "archive_root": "archives/pass-0040-remote-blobs/sha256",
            "content_address": "sha256",
            "file_extension": ".lean",
        },
        "archive_statement_checks": checks,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "negative_fixture_count": 8,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-archive-file-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-archive-sha-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-archive-signature-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-discharge-gate-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-pass0039-binding-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-external-replay-required"},
            {"expected_validator_status": "REJECT", "id": "negative-public-claim-overpromoted"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "non_promotion_statement": "Pass 0040 checks archived raw-source replay by digest. It does not re-run Lean, prove semantic equivalence by elaboration, prove an axiom-free result, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "remote_statement_replay_binding": {
            "path": "schemas/theorem-remote-blob-statement-replay-pass-0039.json",
            "seal": remote_packet["seal"],
            "sha256": remote_packet_sha,
            "source_status": remote_packet["status"],
        },
        "schema": "TheoremArchivedBlobStatementReplaySet/v1",
        "status": "ARCHIVED_BLOB_STATEMENT_REPLAY_MATCH" if all_match and all_archive_sha_match else "ARCHIVED_BLOB_STATEMENT_REPLAY_DRIFT",
        "theorem_archived_blob_statement_fixture": {
            "path": "fixtures/theorem-archived-blob-statement-replay-pass-0040.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "unique_archive_files": archive_files,
        "verifier_measurements": {
            "all_archive_discharge_gates_match": all(row["archive_discharge_status"] == "MATCH" for row in checks),
            "all_archive_file_sha_match_pass0039": all_archive_sha_match,
            "all_archive_frozen_proof_match": all(row["archive_frozen_proof_status"] == "MATCH" for row in checks),
            "all_archive_frozen_solution_match": all(row["archive_frozen_solution_status"] == "MATCH" for row in checks),
            "all_archive_statement_checks_match": all_match,
            "archive_check_count": len(checks),
            "external_call_performed_for_capture": True,
            "external_call_required_for_replay": False,
            "theorem_count": len(checks),
            "unique_archive_file_count": len(archive_files),
            "worktree_text_used_for_signatures": False,
        },
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "path": str(OUT_PATH),
        "schema": contract["schema"],
        "seal": contract["seal"],
        "status": contract["status"],
        "theorem_count": len(checks),
        "unique_archive_file_count": len(archive_files),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
