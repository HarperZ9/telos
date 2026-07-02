"""Generate pass 0043 Lake dependency cache binding receipts."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


PASS = "0043"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_ARCHIVE_PACKET = ROOT / "schemas" / "full-lean-source-archive-pass-0042.json"
FIXTURE_PATH = ROOT / "fixtures" / "lake-dependency-cache-binding-pass-0043.json"
OUT_PATH = ROOT / "schemas" / "lake-dependency-cache-binding-pass-0043.json"
PACKET_PATH = ROOT / "packets" / "053-lake-dependency-cache-binding.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0043-lake-dependency-cache-binding-steelman.md"
PROJECT_SUBDIR = "lean/problem-4b-formalization"


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


def git_status(repo: Path) -> str:
    return git_text(repo, ["status", "--short"])


def git_ls_count(repo: Path) -> int:
    output = git_text(repo, ["ls-files"])
    if not output:
        return 0
    return len(output.splitlines())


def load_manifest(project_root: Path) -> dict:
    return json.loads((project_root / "lake-manifest.json").read_text(encoding="utf-8"))


def package_rows(project_root: Path, manifest: dict) -> list[dict]:
    rows: list[dict] = []
    packages_root = project_root / ".lake" / "packages"
    for package in manifest["packages"]:
        name = package["name"]
        cache_path = packages_root / name
        present = cache_path.exists()
        head = git_text(cache_path, ["rev-parse", "HEAD"]) if present else None
        status_short = git_status(cache_path) if present else "CACHE_MISSING"
        origin = git_text(cache_path, ["config", "--get", "remote.origin.url"]) if present else None
        row = {
            "cache_path": str(cache_path),
            "cache_present": present,
            "clean": status_short == "",
            "config_file": package.get("configFile"),
            "head": head,
            "head_matches_manifest": head == package.get("rev"),
            "input_rev": package.get("inputRev"),
            "local_file_count": git_ls_count(cache_path) if present else 0,
            "manifest_rev": package.get("rev"),
            "manifest_url": package.get("url"),
            "name": name,
            "origin_url": origin,
            "origin_url_matches_manifest": (origin or "").removesuffix(".git") == package.get("url", "").removesuffix(".git"),
            "status_short": status_short,
        }
        rows.append(row)
    return rows


def render_packet(contract: dict) -> str:
    return f"""# Packet 053: Lake Dependency Cache Binding

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0043 binds the local `.lake/packages` dependency cache to
`lake-manifest.json`. It checks every manifest package is present, clean, and
at the pinned revision.

## Dependency Cache Binding

```text
source = schemas/full-lean-source-archive-pass-0042.json
source_sha256 = {contract['full_source_archive_binding']['sha256']}
source_seal = {contract['full_source_archive_binding']['seal']}
package_count = {contract['verifier_measurements']['package_count']}
present_package_count = {contract['verifier_measurements']['present_package_count']}
head_match_count = {contract['verifier_measurements']['head_match_count']}
clean_package_count = {contract['verifier_measurements']['clean_package_count']}
compiled_replay_status = NOT_RUN
```

## Product Reading

This pass closes the local dependency identity gap before compiled replay. A
runner can now check the project source archive and the Lake dependency cache
against pinned manifest revisions before attempting `lake build`.

## Non-Promotion Boundary

Pass 0043 checks dependency cache identity only. It does not run Lean, compile
dependencies, prove semantic equivalence by elaboration, prove an axiom-free
result, validate every public `pipeline-math` claim, or promote any natural law.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0043 Steelman: Lake Dependency Cache Binding

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0043 claims the local Lake dependency cache is bound to the manifest
revisions needed before compiled replay.

## Strongest Objections

1. Matching package HEADs is not compilation.

Correct. This pass checks cache identity. It does not run `lake build`, compile
mathlib, or invoke Lean.

2. Git cleanliness is not a cryptographic supply-chain attestation.

Correct. It is local replay hygiene. A stronger pass should archive dependency
trees or attach signed mirror attestations.

3. Package URLs can differ in harmless formatting.

Correct. The validator normalizes only `.git` suffixes. More URL canonical forms
can be added if needed.

4. The dependency cache is workstation-local.

Correct. This pass proves local availability, not remote reproducibility.

## Verdict

Useful dependency identity evidence before compiled replay. Still bounded to
manifest/cache matching, not semantic proof verification.
"""


def main() -> None:
    repo = source_root()
    project_root = repo / PROJECT_SUBDIR
    source_archive = read_json(SOURCE_ARCHIVE_PACKET)
    source_archive_sha = sha256_file(SOURCE_ARCHIVE_PACKET)
    manifest = load_manifest(project_root)
    rows = package_rows(project_root, manifest)
    all_present = all(row["cache_present"] for row in rows)
    all_heads = all(row["head_matches_manifest"] for row in rows)
    all_clean = all(row["clean"] for row in rows)
    all_urls = all(row["origin_url_matches_manifest"] for row in rows)
    fixture = with_seal({
        "dependency_packages": rows,
        "full_source_archive_sha256": source_archive_sha,
        "generated_on": "2026-07-01",
        "lake_manifest_version": manifest.get("version"),
        "pass": PASS,
        "schema": "LakeDependencyCacheBindingFixture/v1",
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    status = "LAKE_DEPENDENCY_CACHE_BINDING_MATCH" if all_present and all_heads and all_clean and all_urls else "LAKE_DEPENDENCY_CACHE_BINDING_DRIFT"
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0043_lake_dependency_cache_binding",
            "authority_class": "read_only_lake_dependency_cache_binding",
            "event_id": "evt_dogfood_0043_lake_dependency_cache_binding",
            "event_type": "lake_dependency_cache_binding_verified",
            "external_call_performed": False,
            "external_write_performed": False,
            "normal_path_modified": False,
            "result_state": "completed",
            "side_effect_class": "local_dependency_git_read_and_repo_artifact_write",
            "stop_reason": "completed",
            "verification_verdict": "MATCH" if status.endswith("MATCH") else "DRIFT",
        },
        "compiled_replay_status": "NOT_RUN",
        "current_promoted_natural_laws": [],
        "dependency_packages": rows,
        "full_source_archive_binding": {
            "path": "schemas/full-lean-source-archive-pass-0042.json",
            "seal": source_archive["seal"],
            "sha256": source_archive_sha,
            "source_status": source_archive["status"],
        },
        "generated_on": "2026-07-01",
        "lake_manifest": {
            "path": f"{PROJECT_SUBDIR}/lake-manifest.json",
            "package_count": len(manifest["packages"]),
            "version": manifest.get("version"),
        },
        "negative_fixture_count": 8,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-package-cache-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-package-head-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-package-dirty"},
            {"expected_validator_status": "REJECT", "id": "negative-package-url-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-pass0042-binding-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-compiled-replay-overclaimed"},
            {"expected_validator_status": "REJECT", "id": "negative-public-claim-overpromoted"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "non_promotion_statement": "Pass 0043 checks dependency cache identity only. It does not run Lean, compile dependencies, prove semantic equivalence by elaboration, prove an axiom-free result, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "schema": "LakeDependencyCacheBindingSet/v1",
        "status": status,
        "theorem_lake_dependency_cache_fixture": {
            "path": "fixtures/lake-dependency-cache-binding-pass-0043.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "verifier_measurements": {
            "all_package_heads_match_manifest": all_heads,
            "all_package_urls_match_manifest": all_urls,
            "clean_package_count": sum(1 for row in rows if row["clean"]),
            "compiled_replay_status": "NOT_RUN",
            "head_match_count": sum(1 for row in rows if row["head_matches_manifest"]),
            "package_count": len(rows),
            "present_package_count": sum(1 for row in rows if row["cache_present"]),
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
        "package_count": len(rows),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
