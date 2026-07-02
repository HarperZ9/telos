"""Focused tests for pass 0067 Forum routing repair experiment."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_forum_routing_repair_experiment.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_forum_routing_repair_experiment", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_forum_routing_repair_experiment_shape() -> None:
    module = load_composer()
    packet = module.compose()

    assert packet["schema"] == "ForumRoutingRepairExperiment/v1"
    assert packet["pass"] == "0067"
    assert packet["status"] == "FORUM_ROUTING_REPAIR_EXPERIMENT_MATCH"
    assert packet["previous_pass_binding"]["pass"] == "0066"

    probes = packet["route_probes"]
    assert len(probes) == 3
    assert probes[0]["needs_escalation"] is True
    assert probes[0]["decided"] is None
    assert probes[1]["decided"] == "project-telos"
    assert probes[2]["decided"] == "project-telos"
    assert probes[1]["needs_escalation"] is False
    assert probes[2]["needs_escalation"] is False

    metrics = packet["repair_metrics"]
    assert metrics["baseline_project_telos_score"] < metrics["best_repaired_project_telos_score"]
    assert metrics["repaired_no_escalation_count"] == 2
    assert metrics["routing_repair_status"] == "MATCH"

    assert packet["repair_rule"]["required_prefix"]
    assert "Gather" in packet["repair_rule"]["required_tool_chain"]
    assert "Crucible" in packet["repair_rule"]["required_tool_chain"]
    assert packet["negative_fixture"]["status"] == "FAIL_EXPECTED"
    assert packet["unsupported_claim_count"] == 0


if __name__ == "__main__":
    test_forum_routing_repair_experiment_shape()
