"""Focused tests for pass 0095 BuildLang native optimization kernel."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_buildlang_native_optimization_kernel_receipt.py"
ARTIFACT = ROOT / "schemas" / "buildlang-native-optimization-kernel-receipt-pass-0095.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_buildlang_native_optimization_kernel_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_buildlang_native_optimization_kernel_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    receipt = artifact["check_receipt"]
    output = artifact["run_output"]

    assert artifact["schema"] == "BuildLangNativeOptimizationKernelReceipt/v1"
    assert artifact["pass"] == "0095"
    assert artifact["status"] == "BUILDLANG_NATIVE_OPTIMIZATION_KERNEL_RECEIPT_MATCH"
    assert artifact["prior_workflow_binding"]["source_pass"] == "0094"
    assert output == {"best value": 162, "best weight": 29, "best mask": 2347, "feasible count": 1275}
    assert artifact["check_command"]["exit_code"] == 0
    assert artifact["verify_command"]["exit_code"] == 0
    assert artifact["run_command"]["exit_code"] == 0
    assert receipt["schema"] == "buildlang-check-receipt/v1"
    assert receipt["status"] == "passed"
    assert receipt["policy"]["profile"] == "console-only"
    assert artifact["verify_summary"]["all_required_passed"] is True
    assert len(artifact["measurements"]) == 10
    assert all(row["status"] == "MATCH" for row in artifact["measurements"])
    assert all(tool["status"] == "MATCH" for tool in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_buildlang_native_optimization_kernel_shape()
