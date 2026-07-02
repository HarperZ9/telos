"""Focused tests for pass 0073 Telos domain-focus envelope."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_telos_domain_focus_envelope.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_telos_domain_focus_envelope", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_telos_domain_focus_envelope_shape() -> None:
    module = load_composer()
    artifact = module.compose()

    assert artifact["schema"] == "TelosDomainFocusEnvelopeSet/v1"
    assert artifact["pass"] == "0073"
    assert artifact["status"] == "TELOS_DOMAIN_FOCUS_ENVELOPE_MATCH"
    assert artifact["domain_count"] == 6
    assert artifact["root_fallback_envelopes"] == 6
    assert artifact["path_scoped_envelopes"] == 0
    assert artifact["unsupported_claim_count"] == 0
    assert len(artifact["domain_envelopes"]) == 6
    assert len(artifact["negative_fixtures"]) >= 8
    for envelope in artifact["domain_envelopes"]:
        assert envelope["schema"] == "TelosDomainFocusEnvelope/v1"
        assert envelope["route_decision"] == "project-telos"
        assert envelope["route_needs_escalation"] is False
        assert set(envelope["required_layers"]) == set(module.REQUIRED_LAYERS)
        assert envelope["root_context_fallback"] is True
        assert envelope["path_scoped_context"] is False


if __name__ == "__main__":
    test_telos_domain_focus_envelope_shape()
