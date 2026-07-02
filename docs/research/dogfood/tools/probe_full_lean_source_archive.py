"""Generate pass 0042 full Lean source/build archive receipts."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


PASS = "0042"
ROOT = Path(__file__).resolve().parents[1]
TOOLCHAIN_PACKET = ROOT / "schemas" / "lean-toolchain-import-binding-pass-0041.json"
ARCHIVE_ROOT = ROOT / "archives" / "pass-0042-full-lean-source" / "sha256"
FIXTURE_PATH = ROOT / "fixtures" / "full-lean-source-archive-pass-0042.json"
OUT_PATH = ROOT / "schemas" / "full-lean-source-archive-pass-0042.json"
PACKET_PATH = ROOT / "packets" / "052-full-lean-source-archive.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0042-full-lean-source-archive-steelman.md"


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


def source_root() -> Path:
    configured = os.environ.get("PIPELINE_MATH_SOURCE_ROOT")
    if configured:
        return Path(configured)
    return Path(os.environ.get("TEMP", "")) / "pipeline-math-pass0032-lf"


def git_text(repo: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, encoding="utf-8").strip()


def git_bytes(repo: Path, git_path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), "show", f"HEAD:{git_path}"])


def archive_suffix(git_path: str) -> str:
    suffix = Path(git_path).suffix
    if suffix:
        return suffix
    name = Path(git_path).name
    if name == "lean-toolchain":
        return ".toolchain"
    return ".blob"


def archive_file(repo: Path, git_path: str, roles: list[str], pass0041_sha256: str | None) -> dict:
    body = git_bytes(repo, git_path)
    digest = sha256_bytes(body)
    archive_path = ARCHIVE_ROOT / f"{digest}{archive_suffix(git_path)}"
    write_bytes(archive_path, body)
    text = body.decode("utf-8")
    return {
        "archive_path": str(archive_path.relative_to(ROOT)).replace("\\", "/"),
        "archive_sha256": digest,
        "byte_count": len(body),
        "git_path": git_path,
        "line_count": len(text.splitlines()),
        "pass0041_sha256": pass0041_sha256,
        "roles": sorted(roles),
        "sha_match_pass0041": pass0041_sha256 == digest,
    }


def build_archive_rows(repo: Path, toolchain_packet: dict) -> tuple[list[dict], list[dict], list[dict]]:
    paths: dict[str, set[str]] = {}
    pass0041_shas: dict[str, str] = {}
    for row in toolchain_packet["build_files"]:
        paths.setdefault(row["git_path"], set()).add("build_metadata")
        pass0041_shas[row["git_path"]] = row["sha256"]
    for row in toolchain_packet["lean_modules"]:
        paths.setdefault(row["git_path"], set()).add("lean_module")
        pass0041_shas[row["git_path"]] = row["sha256"]

    unique_rows = [
        archive_file(repo, git_path, sorted(roles), pass0041_shas.get(git_path))
        for git_path, roles in sorted(paths.items())
    ]
    archive_by_path = {row["git_path"]: row for row in unique_rows}
    build_rows = []
    for row in toolchain_packet["build_files"]:
        archive = archive_by_path[row["git_path"]]
        build_rows.append({
            "archive_path": archive["archive_path"],
            "archive_sha256": archive["archive_sha256"],
            "git_path": row["git_path"],
            "pass0041_sha256": row["sha256"],
            "sha_match_pass0041": archive["sha_match_pass0041"],
        })
    module_rows = []
    for row in toolchain_packet["lean_modules"]:
        archive = archive_by_path[row["git_path"]]
        module_rows.append({
            "archive_path": archive["archive_path"],
            "archive_sha256": archive["archive_sha256"],
            "archive_status_pass0042": "FULL_ARCHIVED",
            "git_path": row["git_path"],
            "imports": row["imports"],
            "module": row["module"],
            "pass0041_archive_status": row["archive_status"],
            "pass0041_sha256": row["sha256"],
            "sha_match_pass0041": archive["sha_match_pass0041"],
        })
    return unique_rows, build_rows, module_rows


def render_packet(contract: dict) -> str:
    return f"""# Packet 052: Full Lean Source Archive

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0042 archives every local source/build input identified in pass 0041:
all 16 local Lean modules and all 6 build metadata records. Because
`Prob4b.lean` is both a Lean module and a build/root import file, the archive
contains 21 unique content-addressed files.

## Archive Binding

```text
source = schemas/lean-toolchain-import-binding-pass-0041.json
source_sha256 = {contract['lean_toolchain_import_binding']['sha256']}
source_seal = {contract['lean_toolchain_import_binding']['seal']}
archive_root = archives/pass-0042-full-lean-source/sha256
lean_module_count = {contract['verifier_measurements']['lean_module_count']}
build_file_count = {contract['verifier_measurements']['build_file_count']}
unique_archive_file_count = {contract['verifier_measurements']['unique_archive_file_count']}
module_build_overlap_count = {contract['verifier_measurements']['module_build_overlap_count']}
compiled_replay_status = NOT_RUN
```

## Product Reading

This pass closes the local source archive gap before compiled replay. A later
runner can reconstruct the project inputs from content-addressed files and
compare each byte stream to pass 0041 before attempting Lean/Lake execution.

## Non-Promotion Boundary

Pass 0042 archives source and build inputs. It does not run Lean, prove semantic
equivalence by elaboration, prove an axiom-free result, validate every public
`pipeline-math` claim, or promote any natural law.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0042 Steelman: Full Lean Source Archive

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0042 claims the local source/build input set needed before compiled replay
is captured into a content-addressed archive.

## Strongest Objections

1. A source archive is not a successful Lean build.

Correct. The pass is a precondition for compiled replay. It does not run
`lake build` or invoke the Lean kernel.

2. Dependency packages are not archived here.

Correct. The pass archives local project sources and build metadata. Mathlib
and Lake dependencies still need their own dependency-cache proof packet.

3. Archive paths prove byte identity, not theorem truth.

Correct. This is provenance and replay-preparation evidence, not mathematical
semantics.

4. One file has two roles.

Correct. `Prob4b.lean` is both a root import module and part of the build/replay
metadata surface. The archive records 22 role records over 21 unique files.

## Verdict

Useful source-completeness hardening before compiled replay. Still bounded to
source/build archive integrity, not semantic proof verification.
"""


def main() -> None:
    repo = source_root()
    packet = read_json(TOOLCHAIN_PACKET)
    packet_sha = sha256_file(TOOLCHAIN_PACKET)
    head = git_text(repo, ["rev-parse", "HEAD"])
    unique_rows, build_rows, module_rows = build_archive_rows(repo, packet)
    module_paths = {row["git_path"] for row in module_rows}
    build_paths = {row["git_path"] for row in build_rows}
    overlap = sorted(module_paths & build_paths)
    needed_paths = set(packet["needed_for_compiled_replay"])
    archived_needed = sorted(needed_paths & {row["git_path"] for row in unique_rows})
    all_match = all(row["sha_match_pass0041"] for row in unique_rows)
    fixture = with_seal({
        "build_files": build_rows,
        "full_archive_files": unique_rows,
        "generated_on": "2026-07-01",
        "lean_modules": module_rows,
        "pass": PASS,
        "schema": "FullLeanSourceArchiveFixture/v1",
        "toolchain_import_binding_sha256": packet_sha,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0042_full_lean_source_archive",
            "authority_class": "read_only_full_source_archive",
            "event_id": "evt_dogfood_0042_full_lean_source_archive",
            "event_type": "full_lean_source_archive_verified",
            "external_call_performed": False,
            "external_write_performed": False,
            "normal_path_modified": False,
            "result_state": "completed",
            "side_effect_class": "local_git_object_read_and_repo_artifact_write",
            "stop_reason": "completed",
            "verification_verdict": "MATCH" if all_match else "DRIFT",
        },
        "archive_source": {
            "archive_root": "archives/pass-0042-full-lean-source/sha256",
            "content_address": "sha256",
        },
        "build_files": build_rows,
        "compiled_replay_status": "NOT_RUN",
        "current_promoted_natural_laws": [],
        "full_archive_files": unique_rows,
        "generated_on": "2026-07-01",
        "lean_modules": module_rows,
        "lean_toolchain_import_binding": {
            "path": "schemas/lean-toolchain-import-binding-pass-0041.json",
            "seal": packet["seal"],
            "sha256": packet_sha,
            "source_status": packet["status"],
        },
        "module_build_overlap": overlap,
        "needed_for_compiled_replay_archived": archived_needed,
        "negative_fixture_count": 8,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-source-file-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-source-file-sha-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-build-file-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-module-count-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-pass0041-binding-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-compiled-replay-overclaimed"},
            {"expected_validator_status": "REJECT", "id": "negative-public-claim-overpromoted"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "non_promotion_statement": "Pass 0042 archives source and build inputs. It does not run Lean, prove semantic equivalence by elaboration, prove an axiom-free result, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "repo_receipt": {
            "commit": head,
            "commit_match_pass0041": head == packet["repo_receipt"]["commit"],
            "project_subdir": packet["repo_receipt"]["project_subdir"],
            "url": packet["repo_receipt"]["url"],
        },
        "schema": "FullLeanSourceArchiveSet/v1",
        "status": "FULL_LEAN_SOURCE_ARCHIVE_MATCH" if all_match else "FULL_LEAN_SOURCE_ARCHIVE_DRIFT",
        "theorem_full_lean_source_archive_fixture": {
            "path": "fixtures/full-lean-source-archive-pass-0042.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "verifier_measurements": {
            "all_archived_sha_match_pass0041": all_match,
            "build_file_count": len(build_rows),
            "commit_match_pass0041": head == packet["repo_receipt"]["commit"],
            "compiled_replay_status": "NOT_RUN",
            "external_call_required_for_replay": False,
            "lean_module_count": len(module_rows),
            "module_build_overlap_count": len(overlap),
            "needed_for_compiled_replay_archived_count": len(archived_needed),
            "needed_for_compiled_replay_count": len(packet["needed_for_compiled_replay"]),
            "role_record_count": len(build_rows) + len(module_rows),
            "unique_archive_file_count": len(unique_rows),
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
        "role_record_count": len(build_rows) + len(module_rows),
        "unique_archive_file_count": len(unique_rows),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
