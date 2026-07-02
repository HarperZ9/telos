"""Generate pass 0039 remote raw-blob theorem statement replay receipts."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


PASS = "0039"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_REF_PACKET = ROOT / "schemas" / "theorem-source-ref-integrity-pass-0036.json"
BLOB_PACKET = ROOT / "schemas" / "theorem-blob-statement-replay-pass-0038.json"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-remote-blob-statement-replay-pass-0039.json"
OUT_PATH = ROOT / "schemas" / "theorem-remote-blob-statement-replay-pass-0039.json"
PACKET_PATH = ROOT / "packets" / "049-theorem-remote-blob-statement-replay.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0039-remote-blob-statement-replay-steelman.md"


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


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def repo_slug(github_url: str) -> str:
    stripped = github_url.removesuffix(".git").rstrip("/")
    marker = "github.com/"
    if marker not in stripped:
        raise ValueError(f"unsupported repository URL: {github_url}")
    return stripped.split(marker, 1)[1]


def raw_url(slug: str, commit: str, git_path: str) -> str:
    quoted = urllib.parse.quote(git_path, safe="/")
    return f"https://raw.githubusercontent.com/{slug}/{commit}/{quoted}"


def fetch_raw(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "telos-dogfood-pass-0039"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def canonical_signature(signature_text: str) -> str:
    one_line = re.sub(r"\s+", " ", signature_text).strip()
    match = re.match(r"^(theorem|lemma)\s+\S+\s*(.*)$", one_line)
    if match:
        return match.group(2).strip()
    return one_line


def extract_signature(remote_text: str, line_no: int) -> dict:
    lines = remote_text.splitlines()
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


def check_discharge(remote_text: str, line_no: int, theorem: str) -> dict:
    lines = remote_text.splitlines()
    line_text = lines[line_no - 1].strip()
    normalized = re.sub(r"\s+", " ", line_text)
    ok = f"@{theorem} = @{theorem}_proof" in normalized and normalized.endswith(":= rfl")
    return {
        "line_text": line_text,
        "line_text_sha256": sha256_text(line_text),
        "normalized_line": normalized,
        "remote_discharge_status": "MATCH" if ok else "DRIFT",
    }


def fetch_remote_files(source_ref_packet: dict, blob_packet: dict) -> dict[str, dict]:
    receipt = source_ref_packet["repo_receipt"]
    commit = receipt["commit"]
    slug = repo_slug(receipt["url"])
    prior_files = {row["git_path"]: row for row in blob_packet["unique_blob_files"]}
    remote_files: dict[str, dict] = {}
    for git_path, prior in prior_files.items():
        url = raw_url(slug, commit, git_path)
        body = fetch_raw(url)
        text = body.decode("utf-8")
        remote_files[git_path] = {
            "commit": commit,
            "fetch_status": "MATCH",
            "git_path": git_path,
            "line_count": len(text.splitlines()),
            "pass0036_git_blob_sha256": prior["pass0036_git_blob_sha256"],
            "pass0038_blob_git_blob_id": prior["git_blob_id"],
            "pass0038_blob_sha256": prior["git_blob_sha256"],
            "remote_raw_sha256": sha256_bytes(body),
            "remote_url": url,
            "text": text,
        }
        if remote_files[git_path]["remote_raw_sha256"] != prior["git_blob_sha256"]:
            remote_files[git_path]["fetch_status"] = "DRIFT"
    return remote_files


def build_rows(blob_packet: dict, remote_files: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for prior in blob_packet["blob_statement_checks"]:
        theorem = prior["theorem"]
        row: dict = {
            "refs": {},
            "remote_discharge_status": "DRIFT",
            "remote_frozen_proof_status": "DRIFT",
            "remote_frozen_solution_status": "DRIFT",
            "remote_signature_status": "DRIFT",
            "theorem": theorem,
        }
        for ref_kind in ("frozen_statement", "solution_decl", "proof_decl"):
            prior_ref = prior["refs"][ref_kind]
            remote = remote_files[prior_ref["git_path"]]
            sig = extract_signature(remote["text"], prior_ref["line_no"])
            status = "MATCH" if sig["canonical_signature"] == prior_ref["canonical_signature"] else "DRIFT"
            row["refs"][ref_kind] = {
                "canonical_signature": sig["canonical_signature"],
                "commit": remote["commit"],
                "git_path": prior_ref["git_path"],
                "line_no": prior_ref["line_no"],
                "pass0036_git_blob_sha256": remote["pass0036_git_blob_sha256"],
                "pass0038_blob_git_blob_id": remote["pass0038_blob_git_blob_id"],
                "pass0038_blob_sha256": remote["pass0038_blob_sha256"],
                "prior_canonical_signature": prior_ref["canonical_signature"],
                "ref": prior_ref["ref"],
                "remote_raw_sha256": remote["remote_raw_sha256"],
                "remote_url": remote["remote_url"],
                "signature_sha256": sig["signature_sha256"],
                "signature_span": sig["signature_span"],
                "signature_status": status,
                "signature_text": sig["signature_text"],
            }
        discharge_prior = prior["refs"]["discharge_gate"]
        discharge_remote = remote_files[discharge_prior["git_path"]]
        discharge = check_discharge(discharge_remote["text"], discharge_prior["line_no"], theorem)
        row["refs"]["discharge_gate"] = {
            "commit": discharge_remote["commit"],
            "git_path": discharge_prior["git_path"],
            "line_no": discharge_prior["line_no"],
            "line_text": discharge["line_text"],
            "line_text_sha256": discharge["line_text_sha256"],
            "normalized_line": discharge["normalized_line"],
            "pass0036_git_blob_sha256": discharge_remote["pass0036_git_blob_sha256"],
            "pass0038_blob_git_blob_id": discharge_remote["pass0038_blob_git_blob_id"],
            "pass0038_blob_sha256": discharge_remote["pass0038_blob_sha256"],
            "ref": discharge_prior["ref"],
            "remote_raw_sha256": discharge_remote["remote_raw_sha256"],
            "remote_url": discharge_remote["remote_url"],
            "signature_status": discharge["remote_discharge_status"],
        }
        frozen = row["refs"]["frozen_statement"]["canonical_signature"]
        solution = row["refs"]["solution_decl"]["canonical_signature"]
        proof = row["refs"]["proof_decl"]["canonical_signature"]
        row["remote_frozen_solution_status"] = "MATCH" if frozen == solution else "DRIFT"
        row["remote_frozen_proof_status"] = "MATCH" if frozen == proof else "DRIFT"
        row["remote_discharge_status"] = discharge["remote_discharge_status"]
        row["remote_signature_status"] = (
            "MATCH"
            if row["remote_frozen_solution_status"] == "MATCH"
            and row["remote_frozen_proof_status"] == "MATCH"
            and row["remote_discharge_status"] == "MATCH"
            else "DRIFT"
        )
        rows.append(row)
    file_rows = [
        {key: value for key, value in remote.items() if key != "text"}
        for remote in remote_files.values()
    ]
    return rows, file_rows


def render_packet(contract: dict) -> str:
    table = "\n".join(
        f"| `{row['theorem']}` | `{row['remote_frozen_solution_status']}` | `{row['remote_frozen_proof_status']}` | `{row['remote_discharge_status']}` | `{row['remote_signature_status']}` |"
        for row in contract["remote_statement_checks"]
    )
    return f"""# Packet 049: Theorem Remote Blob Statement Replay

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0039 replays the pass 0038 Git-blob statement checks from public GitHub
raw bytes at the frozen `pipeline-math` commit. This removes dependence on the
local Git object database for the source-signature replay layer.

## Source Binding

```text
source = schemas/theorem-blob-statement-replay-pass-0038.json
source_sha256 = {contract['blob_statement_replay_binding']['sha256']}
source_seal = {contract['blob_statement_replay_binding']['seal']}
remote_base = {contract['remote_source']['raw_base']}
commit = {contract['remote_source']['commit']}
theorem_count = {contract['verifier_measurements']['theorem_count']}
remote_check_count = {contract['verifier_measurements']['remote_check_count']}
unique_remote_file_count = {contract['verifier_measurements']['unique_remote_file_count']}
```

## Remote Replay Checks

| Theorem | Remote frozen vs solution | Remote frozen vs proof | Remote discharge gate | Overall |
| --- | --- | --- | --- | --- |
{table}

## Product Reading

This pass turns proof-packet source signatures into replayable public archive
receipts. A verifier can fetch raw source bytes by repository, commit, and path,
then compare the resulting digests and theorem signatures to the local packet.

## Non-Promotion Boundary

Pass 0039 checks public raw-source replay by commit. It does not re-run Lean,
prove semantic equivalence by elaboration, prove an axiom-free result, validate
every public `pipeline-math` claim, or promote any natural law.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0039 Steelman: Remote Blob Statement Replay

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0039 claims theorem statement-signature checks can replay from public
GitHub raw bytes by commit rather than a local Git object database.

## Strongest Objections

1. GitHub availability is now part of the verification path.

Correct. This pass improves portability but introduces a network dependency.
A later pass should archive the fetched bytes into a local content-addressed
bundle.

2. Raw file bytes are still source text, not Lean elaboration.

Correct. The pass verifies source-signature replay and discharge-gate text. It
does not inspect compiled kernel terms or proof bodies.

3. The pass trusts GitHub's raw endpoint for serving the commit path.

Correct. The commit, path, digest, and previous local blob digest make drift
visible, but a stronger archival layer should include independent mirrors.

4. The replay inherits pass 0038 signature extraction.

Correct. Pass 0039 binds to pass 0038 and tests byte-source portability, not a
new theorem semantics layer.

## Verdict

Useful portability hardening for public proof packets. Still bounded to
source-signature replay, not semantic proof verification.
"""


def main() -> None:
    source_ref_packet = read_json(SOURCE_REF_PACKET)
    blob_packet = read_json(BLOB_PACKET)
    blob_packet_sha = sha256_file(BLOB_PACKET)
    source_ref_sha = sha256_file(SOURCE_REF_PACKET)
    remote_files = fetch_remote_files(source_ref_packet, blob_packet)
    checks, file_rows = build_rows(blob_packet, remote_files)
    all_match = all(row["remote_signature_status"] == "MATCH" for row in checks)
    all_remote_sha_match = all(row["remote_raw_sha256"] == row["pass0038_blob_sha256"] for row in file_rows)
    receipt = source_ref_packet["repo_receipt"]
    slug = repo_slug(receipt["url"])
    fixture = with_seal({
        "generated_on": "2026-07-01",
        "pass": PASS,
        "remote_statement_checks": checks,
        "schema": "TheoremRemoteBlobStatementReplayFixture/v1",
        "source_ref_integrity_sha256": source_ref_sha,
        "theorem_blob_statement_replay_sha256": blob_packet_sha,
        "unique_remote_files": file_rows,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0039_remote_blob_statement_replay",
            "authority_class": "read_only_public_raw_blob_signature_replay",
            "event_id": "evt_dogfood_0039_remote_blob_statement_replay",
            "event_type": "theorem_remote_blob_statement_replay_verified",
            "external_call_performed": True,
            "external_write_performed": False,
            "normal_path_modified": False,
            "result_state": "completed",
            "side_effect_class": "external_read_and_repo_artifact_write",
            "stop_reason": "completed",
            "verification_verdict": "MATCH" if all_match and all_remote_sha_match else "DRIFT",
        },
        "blob_statement_replay_binding": {
            "path": "schemas/theorem-blob-statement-replay-pass-0038.json",
            "seal": blob_packet["seal"],
            "sha256": blob_packet_sha,
            "source_status": blob_packet["status"],
        },
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "negative_fixture_count": 8,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-remote-fetch-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-remote-sha-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-remote-signature-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-discharge-gate-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-pass0038-binding-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-raw-url-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-public-claim-overpromoted"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "non_promotion_statement": "Pass 0039 checks public raw-source replay by commit. It does not re-run Lean, prove semantic equivalence by elaboration, prove an axiom-free result, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "remote_source": {
            "commit": receipt["commit"],
            "raw_base": f"https://raw.githubusercontent.com/{slug}/{receipt['commit']}/",
            "repository": receipt["url"],
        },
        "remote_statement_checks": checks,
        "schema": "TheoremRemoteBlobStatementReplaySet/v1",
        "source_ref_integrity_binding": {
            "path": "schemas/theorem-source-ref-integrity-pass-0036.json",
            "seal": source_ref_packet["seal"],
            "sha256": source_ref_sha,
            "source_status": source_ref_packet["status"],
        },
        "status": "REMOTE_BLOB_STATEMENT_REPLAY_MATCH" if all_match and all_remote_sha_match else "REMOTE_BLOB_STATEMENT_REPLAY_DRIFT",
        "theorem_remote_blob_statement_fixture": {
            "path": "fixtures/theorem-remote-blob-statement-replay-pass-0039.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "unique_remote_files": file_rows,
        "verifier_measurements": {
            "all_remote_discharge_gates_match": all(row["remote_discharge_status"] == "MATCH" for row in checks),
            "all_remote_file_sha_match_pass0038": all_remote_sha_match,
            "all_remote_frozen_proof_match": all(row["remote_frozen_proof_status"] == "MATCH" for row in checks),
            "all_remote_frozen_solution_match": all(row["remote_frozen_solution_status"] == "MATCH" for row in checks),
            "all_remote_statement_checks_match": all_match,
            "external_call_performed": True,
            "remote_check_count": len(checks),
            "theorem_count": len(checks),
            "unique_remote_file_count": len(file_rows),
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
        "unique_remote_file_count": len(file_rows),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
