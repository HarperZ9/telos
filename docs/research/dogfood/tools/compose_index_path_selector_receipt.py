"""Compose pass 0078 Index path-selector receipt fixture."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "IndexPathSelectorReceipt/v1"
PASS_ID = "0078"
STATUS_MATCH = "INDEX_PATH_SELECTOR_RECEIPT_FIXTURE_MATCH"
STATUS_DRIFT = "INDEX_PATH_SELECTOR_RECEIPT_FIXTURE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
BUILDLANG_ROOT = Path("C:/dev/public/pubscan/quantalang")
SELECTORS = ["buildlang", "compiler", "build-universe"]
EXCLUDED_DIRS = {".git", ".ruff_cache", ".pytest_cache", "target", "node_modules", "__pycache__"}
REF_SUFFIXES = {".bld", ".rs", ".toml", ".md", ".lock", ".build", ".json"}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def selector_files(selector_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in selector_root.rglob("*"):
        if path.is_file() and not should_skip(path.relative_to(selector_root)):
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(BUILDLANG_ROOT).as_posix())


def source_ref(path: Path, selector: str) -> dict[str, Any]:
    rel = path.relative_to(BUILDLANG_ROOT).as_posix()
    return {
        "schema": "project-telos.source-ref/v1",
        "kind": "file",
        "selector": selector,
        "repo": "quantalang",
        "repo_path": ".",
        "path": rel,
        "sha256": sha256_file(path),
        "line": None,
        "expand": {
            "tool": "gather.docs",
            "arguments": {
                "path": rel,
                "scope": "index.path-selector.receipt",
            },
        },
    }


def selector_digest(files: list[Path]) -> str:
    rows = [{"path": file.relative_to(BUILDLANG_ROOT).as_posix(), "sha256": sha256_file(file)} for file in files]
    return sha256_obj(rows)


def selector_result(selector: str) -> dict[str, Any]:
    selector_root = BUILDLANG_ROOT / selector
    if not selector_root.exists():
        return {
            "selector": selector,
            "status": "REJECT",
            "reason": "missing_selector",
            "kind": None,
            "file_count": 0,
            "source_ref_count": 0,
            "tree_sha256": None,
        }
    files = selector_files(selector_root)
    refs = [
        source_ref(path, selector)
        for path in files
        if path.suffix.lower() in REF_SUFFIXES
    ][:64]
    return {
        "selector": selector,
        "status": "MATCH",
        "reason": "selected",
        "kind": "directory" if selector_root.is_dir() else "file",
        "file_count": len(files),
        "source_ref_count": len(refs),
        "tree_sha256": selector_digest(files),
        "source_refs": refs,
    }


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "missing_selector_silently_omitted", "expected_status": "REJECT", "reject_reason": "missing selectors require explicit REJECT"},
        {"fixture_id": "target_directory_included", "expected_status": "REJECT", "reject_reason": "generated build outputs excluded from source receipt"},
        {"fixture_id": "raw_payload_included", "expected_status": "REJECT", "reject_reason": "source refs only"},
        {"fixture_id": "repo_root_claimed_path_scoped", "expected_status": "REJECT", "reject_reason": "selected paths required"},
        {"fixture_id": "selector_without_tree_digest", "expected_status": "REJECT", "reject_reason": "tree digest required for selected paths"},
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported claim count must remain zero"},
    ]


def compose() -> dict[str, Any]:
    pass_0076 = read_json(ROOT / "schemas" / "buildlang-index-focus-bridge-pass-0076.json")
    pass_0077 = read_json(ROOT / "schemas" / "path-selector-contract-scorecard-pass-0077.json")
    results = [selector_result(selector) for selector in SELECTORS]
    source_refs = [ref for result in results for ref in result.get("source_refs", [])]
    selected = [row for row in results if row["status"] == "MATCH"]
    rejected = [row for row in results if row["status"] == "REJECT"]
    graph_pack_sha256 = sha256_obj({
        "root": str(BUILDLANG_ROOT),
        "selectors": SELECTORS,
        "selector_digests": {row["selector"]: row["tree_sha256"] for row in selected},
        "rejected": [row["selector"] for row in rejected],
    })
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "root": str(BUILDLANG_ROOT),
        "selectors": SELECTORS,
        "selector_results": results,
        "source_refs": source_refs,
        "source_ref_count": len(source_refs),
        "selected_selector_count": len(selected),
        "rejected_selector_count": len(rejected),
        "graph_pack_sha256": graph_pack_sha256,
        "freshness_root_sha256": pass_0076["root_context"]["freshness_root_sha256"],
        "raw_source_included": False,
        "source_refs_only": True,
        "join_key": sha256_obj({"root": str(BUILDLANG_ROOT), "selectors": SELECTORS, "graph": graph_pack_sha256}),
        "contract_source_pass": "0077",
        "contract_schema": pass_0077["contract"]["schema"],
        "bridge_source_pass": "0076",
        "missing_selector_rejections": [row["selector"] for row in rejected],
        "excluded_dirs": sorted(EXCLUDED_DIRS),
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0078 emits an adapter fixture for path-selector receipts. It does not modify Index itself, include raw source payloads, cover missing build-universe sources, prove market adoption, or promote a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    results = {row["selector"]: row for row in artifact.get("selector_results", [])}
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if results.get("buildlang", {}).get("status") != "MATCH":
        errors.append("buildlang")
    if results.get("compiler", {}).get("status") != "MATCH":
        errors.append("compiler")
    if results.get("build-universe", {}).get("status") != "REJECT":
        errors.append("build_universe")
    if artifact.get("selected_selector_count") != 2 or artifact.get("rejected_selector_count") != 1:
        errors.append("selector_counts")
    if artifact.get("source_ref_count", 0) < 2:
        errors.append("source_refs")
    if artifact.get("raw_source_included") is not False or artifact.get("source_refs_only") is not True:
        errors.append("privacy")
    if "target" not in artifact.get("excluded_dirs", []):
        errors.append("target_exclusion")
    if artifact.get("contract_schema") != "IndexPathSelectorReceipt/v1":
        errors.append("contract")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 6:
        errors.append("negative_fixture_count")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"out": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
