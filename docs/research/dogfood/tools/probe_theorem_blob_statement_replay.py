"""Generate pass 0038 Git-blob theorem statement replay receipts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path


PASS = "0038"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_REF_PACKET = ROOT / "schemas" / "theorem-source-ref-integrity-pass-0036.json"
STATEMENT_PACKET = ROOT / "schemas" / "theorem-statement-equivalence-pass-0037.json"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-blob-statement-replay-pass-0038.json"
OUT_PATH = ROOT / "schemas" / "theorem-blob-statement-replay-pass-0038.json"
PACKET_PATH = ROOT / "packets" / "048-theorem-blob-statement-replay.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0038-blob-statement-replay-steelman.md"


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


def read_json(path: Path) -> object:
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


def source_root() -> Path:
    configured = os.environ.get("PIPELINE_MATH_SOURCE_ROOT")
    if configured:
        return Path(configured)
    return Path(os.environ.get("TEMP", "")) / "pipeline-math-pass0032-lf"


def run_git(repo: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, encoding="utf-8").strip()


def git_blob_bytes(repo: Path, git_path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), "show", f"HEAD:{git_path}"])


def canonical_signature(signature_text: str) -> str:
    one_line = re.sub(r"\s+", " ", signature_text).strip()
    match = re.match(r"^(theorem|lemma)\s+\S+\s*(.*)$", one_line)
    if match:
        return match.group(2).strip()
    return one_line


def extract_signature_from_blob(blob_text: str, line_no: int) -> dict:
    lines = blob_text.splitlines()
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


def check_discharge_from_blob(blob_text: str, line_no: int, theorem: str) -> dict:
    lines = blob_text.splitlines()
    line_text = lines[line_no - 1].strip()
    normalized = re.sub(r"\s+", " ", line_text)
    ok = f"@{theorem} = @{theorem}_proof" in normalized and normalized.endswith(":= rfl")
    return {
        "discharge_gate_status": "MATCH" if ok else "DRIFT",
        "line_text": line_text,
        "line_text_sha256": sha256_text(line_text),
        "normalized_line": normalized,
    }


def statement_map(statement_packet: dict) -> dict[str, dict]:
    return {row["theorem"]: row for row in statement_packet["statement_checks"]}


def source_ref_map(source_ref_packet: dict) -> dict[tuple[str, str], dict]:
    return {
        (row["theorem"], row["ref_kind"]): row
        for row in source_ref_packet["source_ref_checks"]
    }


def blob_cache(repo: Path, source_ref_packet: dict) -> dict[str, dict]:
    cache: dict[str, dict] = {}
    for file_row in source_ref_packet["unique_files"]:
        git_path = file_row["git_path"]
        blob_bytes = git_blob_bytes(repo, git_path)
        blob_text = blob_bytes.decode("utf-8")
        cache[git_path] = {
            "git_blob_id": run_git(repo, ["rev-parse", f"HEAD:{git_path}"]),
            "git_blob_sha256": sha256_bytes(blob_bytes),
            "git_path": git_path,
            "line_count": len(blob_text.splitlines()),
            "pass0036_git_blob_id": file_row["git_blob_id"],
            "pass0036_git_blob_sha256": file_row["git_blob_sha256"],
            "pass0036_worktree_sha256": file_row["worktree_sha256"],
            "text": blob_text,
        }
    return cache


def build_rows(repo: Path, source_ref_packet: dict, statement_packet: dict) -> tuple[list[dict], list[dict]]:
    sources = source_ref_map(source_ref_packet)
    statements = statement_map(statement_packet)
    blobs = blob_cache(repo, source_ref_packet)
    rows: list[dict] = []
    for theorem, prior in statements.items():
        theorem_row: dict = {
            "blob_discharge_status": "DRIFT",
            "blob_frozen_proof_status": "DRIFT",
            "blob_frozen_solution_status": "DRIFT",
            "blob_signature_status": "DRIFT",
            "refs": {},
            "theorem": theorem,
        }
        for ref_kind in ("frozen_statement", "solution_decl", "proof_decl"):
            source_row = sources[(theorem, ref_kind)]
            blob = blobs[source_row["git_path"]]
            sig = extract_signature_from_blob(blob["text"], source_row["line_no"])
            prior_key = {
                "frozen_statement": "frozen_signature",
                "solution_decl": "solution_signature",
                "proof_decl": "proof_signature",
            }[ref_kind]
            prior_sig = prior[prior_key]
            status = "MATCH" if sig["canonical_signature"] == prior_sig["canonical_signature"] else "DRIFT"
            theorem_row["refs"][ref_kind] = {
                "blob_git_blob_id": blob["git_blob_id"],
                "blob_git_blob_sha256": blob["git_blob_sha256"],
                "blob_line_count": blob["line_count"],
                "canonical_signature": sig["canonical_signature"],
                "git_path": source_row["git_path"],
                "line_no": source_row["line_no"],
                "pass0036_git_blob_id": blob["pass0036_git_blob_id"],
                "pass0036_git_blob_sha256": blob["pass0036_git_blob_sha256"],
                "prior_canonical_signature": prior_sig["canonical_signature"],
                "ref": source_row["ref"],
                "signature_sha256": sig["signature_sha256"],
                "signature_span": sig["signature_span"],
                "signature_status": status,
                "signature_text": sig["signature_text"],
            }
        discharge_row = sources[(theorem, "discharge_gate")]
        discharge_blob = blobs[discharge_row["git_path"]]
        discharge = check_discharge_from_blob(discharge_blob["text"], discharge_row["line_no"], theorem)
        theorem_row["refs"]["discharge_gate"] = {
            "blob_git_blob_id": discharge_blob["git_blob_id"],
            "blob_git_blob_sha256": discharge_blob["git_blob_sha256"],
            "git_path": discharge_row["git_path"],
            "line_no": discharge_row["line_no"],
            "line_text": discharge["line_text"],
            "line_text_sha256": discharge["line_text_sha256"],
            "normalized_line": discharge["normalized_line"],
            "pass0036_git_blob_id": discharge_blob["pass0036_git_blob_id"],
            "pass0036_git_blob_sha256": discharge_blob["pass0036_git_blob_sha256"],
            "ref": discharge_row["ref"],
            "signature_status": discharge["discharge_gate_status"],
        }
        frozen = theorem_row["refs"]["frozen_statement"]["canonical_signature"]
        solution = theorem_row["refs"]["solution_decl"]["canonical_signature"]
        proof = theorem_row["refs"]["proof_decl"]["canonical_signature"]
        theorem_row["blob_frozen_solution_status"] = "MATCH" if frozen == solution else "DRIFT"
        theorem_row["blob_frozen_proof_status"] = "MATCH" if frozen == proof else "DRIFT"
        theorem_row["blob_discharge_status"] = discharge["discharge_gate_status"]
        theorem_row["blob_signature_status"] = (
            "MATCH"
            if theorem_row["blob_frozen_solution_status"] == "MATCH"
            and theorem_row["blob_frozen_proof_status"] == "MATCH"
            and theorem_row["blob_discharge_status"] == "MATCH"
            else "DRIFT"
        )
        rows.append(theorem_row)
    blob_rows = [
        {key: value for key, value in blob.items() if key != "text"}
        for blob in blobs.values()
    ]
    return rows, blob_rows


def render_packet(contract: dict) -> str:
    table = "\n".join(
        f"| `{row['theorem']}` | `{row['blob_frozen_solution_status']}` | `{row['blob_frozen_proof_status']}` | `{row['blob_discharge_status']}` | `{row['blob_signature_status']}` |"
        for row in contract["blob_statement_checks"]
    )
    return f"""# Packet 048: Theorem Blob Statement Replay

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0038 replays the pass 0037 statement-signature checks from Git object
bytes using `git show HEAD:<path>`, instead of reading source text from the
worktree.

## Source Binding

```text
source = schemas/theorem-statement-equivalence-pass-0037.json
source_sha256 = {contract['statement_equivalence_binding']['sha256']}
source_seal = {contract['statement_equivalence_binding']['seal']}
theorem_count = {contract['verifier_measurements']['theorem_count']}
blob_check_count = {contract['verifier_measurements']['blob_check_count']}
unique_blob_file_count = {contract['verifier_measurements']['unique_blob_file_count']}
```

## Blob Replay Checks

| Theorem | Blob frozen vs solution | Blob frozen vs proof | Blob discharge gate | Overall |
| --- | --- | --- | --- | --- |
{table}

## Product Reading

This pass removes a major product weakness: proof-packet source signatures can
be replayed from immutable Git object bytes rather than a mutable checkout. The
next production step is to archive or fetch these blob bytes by commit without
requiring the temp clone to remain on disk.

## Non-Promotion Boundary

Pass 0038 checks source-signature replay from Git blob bytes. It does not re-run
Lean, prove semantic equivalence by elaboration, prove an axiom-free result,
validate every public `pipeline-math` claim, or promote any natural law.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0038 Steelman: Blob Statement Replay

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0038 claims statement-signature checks can replay from Git object bytes
rather than worktree files.

## Strongest Objections

1. It still requires a local Git object database.

Correct. This pass removes dependence on mutable worktree files, not on local
Git availability. A later pass should fetch or archive blob bytes by commit.

2. Git object bytes are still source text, not Lean elaboration.

Correct. The pass checks source signatures and discharge gate shape. It does not
replace compiled Lean replay.

3. The replay inherits pass 0037 normalization.

Correct. The packet binds pass 0038 canonical signatures back to pass 0037 so
normalization drift is visible.

4. It does not inspect proof bodies.

Correct. Proof body and kernel-term inspection are separate future layers.

## Verdict

Useful hardening for proof-packet portability. Still bounded to source-signature
replay, not semantic proof verification.
"""


def main() -> None:
    repo = source_root()
    if not repo.exists():
        raise SystemExit(f"missing source checkout: {repo}")
    source_ref_packet = read_json(SOURCE_REF_PACKET)
    statement_packet = read_json(STATEMENT_PACKET)
    source_ref_sha = sha256_file(SOURCE_REF_PACKET)
    statement_sha = sha256_file(STATEMENT_PACKET)
    checks, blob_files = build_rows(repo, source_ref_packet, statement_packet)
    all_match = all(row["blob_signature_status"] == "MATCH" for row in checks)
    all_blob_sha_match = all(row["git_blob_sha256"] == row["pass0036_git_blob_sha256"] for row in blob_files)
    fixture = with_seal({
        "blob_statement_checks": checks,
        "generated_on": "2026-07-01",
        "pass": PASS,
        "schema": "TheoremBlobStatementReplayFixture/v1",
        "source_ref_integrity_sha256": source_ref_sha,
        "statement_equivalence_sha256": statement_sha,
        "unique_blob_files": blob_files,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0038_blob_statement_replay",
            "authority_class": "read_only_git_blob_signature_replay",
            "event_id": "evt_dogfood_0038_blob_statement_replay",
            "event_type": "theorem_blob_statement_replay_verified",
            "external_call_performed": False,
            "external_write_performed": False,
            "normal_path_modified": False,
            "result_state": "completed",
            "side_effect_class": "local_git_object_read_and_repo_artifact_write",
            "stop_reason": "completed",
            "verification_verdict": "MATCH" if all_match and all_blob_sha_match else "DRIFT",
        },
        "blob_statement_checks": checks,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "negative_fixture_count": 8,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-blob-sha-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-blob-signature-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-worktree-text-used-as-authority"},
            {"expected_validator_status": "REJECT", "id": "negative-discharge-gate-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-prior-statement-binding-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-source-ref-binding-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-public-claim-overpromoted"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "non_promotion_statement": "Pass 0038 checks source-signature replay from Git blob bytes. It does not re-run Lean, prove semantic equivalence by elaboration, prove an axiom-free result, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "schema": "TheoremBlobStatementReplaySet/v1",
        "source_ref_integrity_binding": {
            "path": "schemas/theorem-source-ref-integrity-pass-0036.json",
            "seal": source_ref_packet["seal"],
            "sha256": source_ref_sha,
            "source_status": source_ref_packet["status"],
        },
        "statement_equivalence_binding": {
            "path": "schemas/theorem-statement-equivalence-pass-0037.json",
            "seal": statement_packet["seal"],
            "sha256": statement_sha,
            "source_status": statement_packet["status"],
        },
        "status": "BLOB_STATEMENT_REPLAY_MATCH" if all_match and all_blob_sha_match else "BLOB_STATEMENT_REPLAY_DRIFT",
        "theorem_blob_statement_fixture": {
            "path": "fixtures/theorem-blob-statement-replay-pass-0038.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "unique_blob_files": blob_files,
        "verifier_measurements": {
            "all_blob_discharge_gates_match": all(row["blob_discharge_status"] == "MATCH" for row in checks),
            "all_blob_file_sha_match_pass0036": all_blob_sha_match,
            "all_blob_frozen_proof_match": all(row["blob_frozen_proof_status"] == "MATCH" for row in checks),
            "all_blob_frozen_solution_match": all(row["blob_frozen_solution_status"] == "MATCH" for row in checks),
            "all_blob_statement_checks_match": all_match,
            "blob_check_count": len(checks),
            "theorem_count": len(checks),
            "unique_blob_file_count": len(blob_files),
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
        "unique_blob_file_count": len(blob_files),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
