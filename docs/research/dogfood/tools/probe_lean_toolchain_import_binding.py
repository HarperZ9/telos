"""Generate pass 0041 Lean toolchain and import-graph binding receipts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path


PASS = "0041"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_REF_PACKET = ROOT / "schemas" / "theorem-source-ref-integrity-pass-0036.json"
ARCHIVE_PACKET = ROOT / "schemas" / "theorem-archived-blob-statement-replay-pass-0040.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-toolchain-import-binding-pass-0041.json"
OUT_PATH = ROOT / "schemas" / "lean-toolchain-import-binding-pass-0041.json"
PACKET_PATH = ROOT / "packets" / "051-lean-toolchain-import-binding.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0041-lean-toolchain-import-binding-steelman.md"

BUILD_FILES = [
    "lean/problem-4b-formalization/lean-toolchain",
    "lean/problem-4b-formalization/lakefile.toml",
    "lean/problem-4b-formalization/lake-manifest.json",
    "lean/problem-4b-formalization/Prob4b.lean",
    "lean/problem-4b-formalization/scripts/frozen.sha256",
    "lean/problem-4b-formalization/scripts/verify.sh",
]
PROJECT_PREFIX = "lean/problem-4b-formalization/"


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


def source_root() -> Path:
    configured = os.environ.get("PIPELINE_MATH_SOURCE_ROOT")
    if configured:
        return Path(configured)
    return Path(os.environ.get("TEMP", "")) / "pipeline-math-pass0032-lf"


def git_text(repo: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, encoding="utf-8").strip()


def git_bytes(repo: Path, git_path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), "show", f"HEAD:{git_path}"])


def git_blob_id(repo: Path, git_path: str) -> str:
    return git_text(repo, ["rev-parse", f"HEAD:{git_path}"])


def module_from_path(git_path: str) -> str:
    rel = git_path.removeprefix(PROJECT_PREFIX).removesuffix(".lean")
    return rel.replace("/", ".")


def path_from_module(module: str) -> str:
    return PROJECT_PREFIX + module.replace(".", "/") + ".lean"


def lean_files(repo: Path) -> list[str]:
    lines = git_text(repo, ["ls-files", PROJECT_PREFIX + "*.lean"]).splitlines()
    return sorted(line for line in lines if line.endswith(".lean"))


def file_receipt(repo: Path, git_path: str, role: str) -> dict:
    body = git_bytes(repo, git_path)
    text = body.decode("utf-8")
    return {
        "byte_count": len(body),
        "git_blob_id": git_blob_id(repo, git_path),
        "git_path": git_path,
        "line_count": len(text.splitlines()),
        "role": role,
        "sha256": sha256_bytes(body),
    }


def parse_imports(text: str) -> list[str]:
    imports: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s*import\s+([A-Za-z0-9_'.]+)\s*$", line)
        if match:
            imports.append(match.group(1))
    return imports


def module_receipts(repo: Path, archive_packet: dict) -> tuple[list[dict], list[dict], list[str]]:
    archived_paths = {row["git_path"] for row in archive_packet["unique_archive_files"]}
    module_rows: list[dict] = []
    edges: list[dict] = []
    for git_path in lean_files(repo):
        body = git_bytes(repo, git_path)
        text = body.decode("utf-8")
        module = module_from_path(git_path)
        imports = parse_imports(text)
        row = {
            "archive_status": "ARCHIVED" if git_path in archived_paths else "NEEDED_FOR_COMPILED_REPLAY",
            "byte_count": len(body),
            "git_blob_id": git_blob_id(repo, git_path),
            "git_path": git_path,
            "import_count": len(imports),
            "imports": imports,
            "line_count": len(text.splitlines()),
            "module": module,
            "sha256": sha256_bytes(body),
        }
        module_rows.append(row)
        for target in imports:
            local_path = path_from_module(target)
            is_local = local_path in set(lean_files(repo))
            edges.append({
                "from": module,
                "from_path": git_path,
                "kind": "local" if is_local else "external",
                "to": target,
                "to_path": local_path if is_local else null_path(target),
            })
    needed_delta = [row["git_path"] for row in module_rows if row["archive_status"] == "NEEDED_FOR_COMPILED_REPLAY"]
    return module_rows, edges, needed_delta


def null_path(module: str) -> None:
    return None


def build_file_receipts(repo: Path) -> tuple[list[dict], dict]:
    rows = [file_receipt(repo, path, "build-metadata") for path in BUILD_FILES]
    toolchain_text = git_bytes(repo, "lean/problem-4b-formalization/lean-toolchain").decode("utf-8").strip()
    manifest = json.loads(git_bytes(repo, "lean/problem-4b-formalization/lake-manifest.json").decode("utf-8"))
    packages = manifest.get("packages", [])
    mathlib = next((pkg for pkg in packages if pkg.get("name") == "mathlib"), {})
    return rows, {
        "lake_manifest_package_count": len(packages),
        "mathlib_input_rev": mathlib.get("inputRev"),
        "mathlib_rev": mathlib.get("rev"),
        "mathlib_url": mathlib.get("url"),
        "toolchain": toolchain_text,
    }


def render_packet(contract: dict) -> str:
    return f"""# Packet 051: Lean Toolchain Import Binding

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0041 binds the archived theorem-source packet to the Lean/Lake metadata
needed for compiled replay: `lean-toolchain`, `lakefile.toml`,
`lake-manifest.json`, root module imports, and the local `Prob4b` import graph.

## Toolchain Binding

```text
repo_commit = {contract['repo_receipt']['commit']}
toolchain = {contract['toolchain_summary']['toolchain']}
mathlib_input_rev = {contract['toolchain_summary']['mathlib_input_rev']}
mathlib_rev = {contract['toolchain_summary']['mathlib_rev']}
lake_manifest_package_count = {contract['toolchain_summary']['lake_manifest_package_count']}
build_file_count = {contract['verifier_measurements']['build_file_count']}
lean_module_count = {contract['verifier_measurements']['lean_module_count']}
local_import_edge_count = {contract['verifier_measurements']['local_import_edge_count']}
external_import_edge_count = {contract['verifier_measurements']['external_import_edge_count']}
compiled_replay_status = NOT_RUN
```

## Archive Delta

```text
archived_source_file_count = {contract['verifier_measurements']['archived_source_file_count']}
needed_for_compiled_replay_count = {contract['verifier_measurements']['needed_for_compiled_replay_count']}
archive_replay_binding = {contract['archive_statement_replay_binding']['path']}
```

## Product Reading

This pass turns source-signature proof packets into a compile-replay planning
packet. It identifies the exact Lean version, mathlib revision, Lake manifest,
root module, import edges, archived theorem files, and additional local files
that must be included before a full Lean replay can be attempted.

## Non-Promotion Boundary

Pass 0041 discovers and binds toolchain/import metadata. It does not run Lean,
prove semantic equivalence by elaboration, prove an axiom-free result, validate
every public `pipeline-math` claim, or promote any natural law.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0041 Steelman: Lean Toolchain Import Binding

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0041 claims the archived theorem packet can be bound to the Lean toolchain
and local import graph required for compiled replay planning.

## Strongest Objections

1. Toolchain discovery is not compilation.

Correct. The pass records Lean/Lake metadata and import dependencies. It does
not invoke `lake build` or the Lean kernel.

2. The existing archive does not cover every local module needed for replay.

Correct. That is the point of the pass: it records the dependency delta so the
next archive can include every local module, not only theorem-signature files.

3. Lake dependencies are pinned by manifest but not fetched or checked here.

Correct. Pass 0041 binds manifest metadata. A later pass should verify package
availability and downloaded dependency hashes.

4. Import parsing is textual.

Correct. The import graph is source-level planning evidence, not elaboration.

## Verdict

Useful compile-replay planning evidence. Still bounded to toolchain/import
binding, not semantic proof verification.
"""


def main() -> None:
    repo = source_root()
    source_ref_packet = read_json(SOURCE_REF_PACKET)
    archive_packet = read_json(ARCHIVE_PACKET)
    archive_packet_sha = sha256_file(ARCHIVE_PACKET)
    head = git_text(repo, ["rev-parse", "HEAD"])
    build_rows, toolchain_summary = build_file_receipts(repo)
    module_rows, import_edges, needed_delta = module_receipts(repo, archive_packet)
    local_edges = [edge for edge in import_edges if edge["kind"] == "local"]
    external_edges = [edge for edge in import_edges if edge["kind"] == "external"]
    archived_source_paths = {row["git_path"] for row in archive_packet["unique_archive_files"]}
    status = "LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH" if head == source_ref_packet["repo_receipt"]["commit"] else "LEAN_TOOLCHAIN_IMPORT_BINDING_DRIFT"
    fixture = with_seal({
        "build_files": build_rows,
        "generated_on": "2026-07-01",
        "import_edges": import_edges,
        "lean_modules": module_rows,
        "pass": PASS,
        "schema": "LeanToolchainImportBindingFixture/v1",
        "theorem_archived_blob_statement_replay_sha256": archive_packet_sha,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0041_lean_toolchain_import_binding",
            "authority_class": "read_only_lean_toolchain_import_discovery",
            "event_id": "evt_dogfood_0041_lean_toolchain_import_binding",
            "event_type": "lean_toolchain_import_binding_verified",
            "external_call_performed": False,
            "external_write_performed": False,
            "normal_path_modified": False,
            "result_state": "completed",
            "side_effect_class": "local_git_object_read_and_repo_artifact_write",
            "stop_reason": "completed",
            "verification_verdict": "MATCH" if status.endswith("MATCH") else "DRIFT",
        },
        "archive_statement_replay_binding": {
            "path": "schemas/theorem-archived-blob-statement-replay-pass-0040.json",
            "seal": archive_packet["seal"],
            "sha256": archive_packet_sha,
            "source_status": archive_packet["status"],
        },
        "build_files": build_rows,
        "compiled_replay_status": "NOT_RUN",
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "import_edges": import_edges,
        "lean_modules": module_rows,
        "needed_for_compiled_replay": needed_delta,
        "negative_fixture_count": 8,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-toolchain-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-manifest-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-commit-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-import-edge-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-archive-binding-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-compiled-replay-overclaimed"},
            {"expected_validator_status": "REJECT", "id": "negative-public-claim-overpromoted"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "non_promotion_statement": "Pass 0041 discovers and binds Lean toolchain/import metadata. It does not run Lean, prove semantic equivalence by elaboration, prove an axiom-free result, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "repo_receipt": {
            "commit": head,
            "commit_match_pass0036": head == source_ref_packet["repo_receipt"]["commit"],
            "project_subdir": source_ref_packet["repo_receipt"]["project_subdir"],
            "url": source_ref_packet["repo_receipt"]["url"],
        },
        "schema": "LeanToolchainImportBindingSet/v1",
        "status": status,
        "theorem_lean_toolchain_import_fixture": {
            "path": "fixtures/lean-toolchain-import-binding-pass-0041.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "toolchain_summary": toolchain_summary,
        "verifier_measurements": {
            "archived_source_file_count": len(archived_source_paths),
            "build_file_count": len(build_rows),
            "commit_match_pass0036": head == source_ref_packet["repo_receipt"]["commit"],
            "compiled_replay_status": "NOT_RUN",
            "external_import_edge_count": len(external_edges),
            "lean_module_count": len(module_rows),
            "local_import_edge_count": len(local_edges),
            "needed_for_compiled_replay_count": len(needed_delta),
            "toolchain_bound": toolchain_summary["toolchain"] == "leanprover/lean4:v4.31.0",
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
        "lean_module_count": len(module_rows),
        "needed_for_compiled_replay_count": len(needed_delta),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
