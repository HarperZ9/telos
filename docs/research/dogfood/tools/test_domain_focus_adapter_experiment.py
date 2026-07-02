"""Focused tests for pass 0072 domain-focus adapter experiment."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_domain_focus_adapter_experiment.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_domain_focus_adapter_experiment", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_domain_focus_adapter_experiment_shape() -> None:
    module = load_composer()
    artifact = module.compose()

    assert artifact["schema"] == "DomainFocusAdapterExperiment/v1"
    assert artifact["pass"] == "0072"
    assert artifact["status"] == "DOMAIN_FOCUS_ADAPTER_EXPERIMENT_MATCH"
    assert artifact["domain_count"] == len(module.DOMAINS)
    assert artifact["route_summary"]["adapted_project_telos"] == len(module.DOMAINS)
    assert artifact["route_summary"]["adapted_escalations"] == 0
    assert artifact["index_summary"]["valid_focuses"] == ["telos"]
    assert artifact["index_summary"]["rejected_focus_count"] >= 5
    assert len(artifact["adapter_rows"]) == len(module.DOMAINS)
    assert len(artifact["tool_improvement_queue"]) == 5
    assert artifact["unsupported_claim_count"] == 0
    assert len(artifact["negative_fixtures"]) >= 6
    assert all(item["expected_status"] == "REJECT" for item in artifact["negative_fixtures"])


if __name__ == "__main__":
    test_domain_focus_adapter_experiment_shape()
