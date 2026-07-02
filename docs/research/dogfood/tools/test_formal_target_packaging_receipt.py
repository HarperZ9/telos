"""Focused tests for pass 0118 formal target packaging receipt."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_formal_target_packaging_receipt.py"
ARTIFACT = ROOT / "schemas" / "formal-target-packaging-receipt-pass-0118.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_formal_target_packaging_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_formal_target_packaging_shape() -> None:
    artifact = read_artifact()
    sources = artifact["source_targets"]
    target_ids = set(artifact["target_ids"])

    assert artifact["schema"] == "FormalTargetPackagingReceipt/v1"
    assert artifact["status"] == "FORMAL_TARGET_PACKAGING_MATCH"
    assert artifact["source_bindings"]["theorem_prover_adapter_pass"] == "0117"
    assert artifact["manifest"]["source_count"] == 4
    assert len(sources) == 4
    assert {row["language"] for row in sources} == {"lean4", "rocq", "isabelle", "agda"}
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []
    assert all(row["status"] == "SOURCE_EMITTED_NOT_EXECUTED" for row in sources)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in sources)
    assert all(row["ascii"] is True for row in sources)

    for row in sources:
        path = ROOT / row["path"]
        text = path.read_text(encoding="utf-8")
        assert path.exists()
        assert sha256_file(path) == row["sha256"]
        assert set(row["proposition_ids_present"]) == target_ids
        assert all(target_id in text for target_id in target_ids)
        assert "not executed here" in text

    manifest_path = ROOT / artifact["manifest"]["path"]
    assert manifest_path.exists()
    assert sha256_file(manifest_path) == artifact["manifest"]["sha256"]
    assert artifact["negative_fixtures"][0]["expected_status"] == "REJECT"
    assert all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values())


if __name__ == "__main__":
    test_formal_target_packaging_shape()
