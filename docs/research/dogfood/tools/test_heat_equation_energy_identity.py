"""Behavior test for pass 0062 heat-equation energy identity."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_heat_equation_energy_identity.py"


def test_heat_equation_energy_identity_is_bounded_and_not_promoted() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-pass-0062-") as tmp:
        out_path = Path(tmp) / "heat-identity.json"
        result = subprocess.run(
            [sys.executable, str(COMPOSER), "--out", str(out_path)],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        packet = json.loads(out_path.read_text(encoding="utf-8"))

    probe = packet["numeric_probe"]
    energies = [row["energy_l2"] for row in probe["time_samples"]]

    assert packet["schema"] == "HeatEquationEnergyIdentity/v1"
    assert packet["pass"] == "0062"
    assert packet["status"] == "HEAT_EQUATION_ENERGY_IDENTITY_MATCH"
    assert packet["promotion_state"] == "IDENTITY_NOT_PROMOTED_LAW"
    assert packet["law_candidate_status"] == "BOUNDED_MATHEMATICAL_IDENTITY"
    assert packet["current_promoted_natural_laws"] == []
    assert packet["unsupported_claim_count"] == 0
    assert packet["domain_scope"]["equation"] == "u_t = kappa * u_xx"
    assert packet["domain_scope"]["boundary_condition"] == "periodic"
    assert packet["domain_scope"]["spatial_domain"] == "[0, 2*pi]"
    assert len(packet["source_anchors"]) >= 3
    assert packet["analytic_identity"]["identity"] == "d/dt ||u||_L2^2 = -2*kappa*||u_x||_L2^2"
    assert len(packet["analytic_identity"]["derivation_steps"]) >= 5
    assert probe["max_symbolic_residual"] <= 1e-12
    assert probe["max_finite_difference_residual"] <= 1e-5
    assert all(next_energy <= energy for energy, next_energy in zip(energies, energies[1:]))
    assert probe["energy_monotone_nonincreasing"] is True
    assert probe["mode_count"] == 3
    assert packet["falsifiers"]
    assert "nonperiodic_boundary_flux" in packet["known_limits"]


if __name__ == "__main__":
    test_heat_equation_energy_identity_is_bounded_and_not_promoted()
    print("PASS heat equation energy identity verified")
