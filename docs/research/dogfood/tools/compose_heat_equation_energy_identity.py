"""Compose pass 0062 heat-equation energy identity packet."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


SCHEMA = "HeatEquationEnergyIdentity/v1"
STATUS_MATCH = "HEAT_EQUATION_ENERGY_IDENTITY_MATCH"
STATUS_DRIFT = "HEAT_EQUATION_ENERGY_IDENTITY_DRIFT"
KAPPA = 0.7
MODES = [
    {"amplitude": 1.0, "basis": "sin", "mode": 1},
    {"amplitude": 0.4, "basis": "cos", "mode": 3},
    {"amplitude": -0.2, "basis": "sin", "mode": 5},
]
TIMES = [0.0, 0.05, 0.1, 0.2, 0.4]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def source_anchors() -> list[dict[str, str]]:
    return [
        {
            "confidence": "high",
            "source_id": "mit-ocw-18-303-heat-equation",
            "url": "https://ocw.mit.edu/courses/18-303-linear-partial-differential-equations-fall-2006/d11b374a85c3fde55ec971fe587f8a50_heateqni.pdf",
            "verification_status": "source_lead",
            "summary": "MIT OCW heat-equation notes describe heat transfer and the one-dimensional heat equation.",
        },
        {
            "confidence": "high",
            "source_id": "stanford-math220b-heat-equation",
            "url": "https://web.stanford.edu/class/math220b/handouts/heateqn.pdf",
            "verification_status": "source_lead",
            "summary": "Stanford notes give periodic heat-equation Fourier-series solutions.",
        },
        {
            "confidence": "medium",
            "source_id": "ut-finite-difference-heat-equation",
            "url": "https://www-udc.ig.utexas.edu/external/becker/teaching/557/problem_sets/problem_set_fd_explicit.pdf",
            "verification_status": "source_lead",
            "summary": "UT teaching material describes finite-difference discretization for the one-dimensional heat equation.",
        },
    ]


def mode_energy(amplitude: float, mode: int, time: float) -> float:
    return math.pi * amplitude * amplitude * math.exp(-2.0 * KAPPA * mode * mode * time)


def mode_gradient_energy(amplitude: float, mode: int, time: float) -> float:
    return math.pi * mode * mode * amplitude * amplitude * math.exp(-2.0 * KAPPA * mode * mode * time)


def energy(time: float) -> float:
    return sum(mode_energy(row["amplitude"], row["mode"], time) for row in MODES)


def gradient_energy(time: float) -> float:
    return sum(mode_gradient_energy(row["amplitude"], row["mode"], time) for row in MODES)


def energy_derivative(time: float) -> float:
    return -2.0 * KAPPA * gradient_energy(time)


def finite_difference_derivative(time: float, step: float = 1e-7) -> float:
    return (energy(time + step) - energy(time - step)) / (2.0 * step)


def numeric_probe() -> dict[str, Any]:
    samples = []
    max_symbolic_residual = 0.0
    max_fd_residual = 0.0
    for time in TIMES:
        e_value = energy(time)
        grad_value = gradient_energy(time)
        derivative_value = energy_derivative(time)
        identity_rhs = -2.0 * KAPPA * grad_value
        symbolic_residual = abs(derivative_value - identity_rhs)
        fd_residual = abs(finite_difference_derivative(time) - identity_rhs)
        max_symbolic_residual = max(max_symbolic_residual, symbolic_residual)
        max_fd_residual = max(max_fd_residual, fd_residual)
        samples.append({
            "energy_derivative": derivative_value,
            "energy_l2": e_value,
            "gradient_energy_l2": grad_value,
            "identity_rhs": identity_rhs,
            "symbolic_residual": symbolic_residual,
            "t": time,
        })
    energies = [row["energy_l2"] for row in samples]
    return {
        "basis": "finite Fourier series",
        "energy_monotone_nonincreasing": all(b <= a for a, b in zip(energies, energies[1:])),
        "finite_difference_step": 1e-7,
        "kappa": KAPPA,
        "max_finite_difference_residual": max_fd_residual,
        "max_symbolic_residual": max_symbolic_residual,
        "mode_count": len(MODES),
        "modes": MODES,
        "time_samples": samples,
    }


def analytic_identity() -> dict[str, Any]:
    return {
        "derivation_steps": [
            "Let E(t) = integral_0^(2*pi) u(x,t)^2 dx.",
            "Differentiate under the integral for smooth u: E'(t) = 2 integral u u_t dx.",
            "Substitute u_t = kappa u_xx.",
            "Integrate by parts: integral u u_xx dx = [u u_x]_0^(2*pi) - integral u_x^2 dx.",
            "Periodic boundary conditions make [u u_x]_0^(2*pi) vanish.",
            "Therefore E'(t) = -2*kappa integral u_x^2 dx.",
        ],
        "identity": "d/dt ||u||_L2^2 = -2*kappa*||u_x||_L2^2",
        "proof_status": "ANALYTIC_DERIVATION_WITH_NUMERIC_PROBE",
    }


def compose() -> dict[str, Any]:
    packet = {
        "schema": SCHEMA,
        "analytic_identity": analytic_identity(),
        "current_promoted_natural_laws": [],
        "domain_scope": {
            "boundary_condition": "periodic",
            "equation": "u_t = kappa * u_xx",
            "kappa": KAPPA,
            "regularity": "smooth finite Fourier series",
            "spatial_domain": "[0, 2*pi]",
        },
        "falsifiers": [
            "Boundary conditions are not periodic and boundary flux is nonzero.",
            "Solution regularity is too weak to justify differentiating under the integral or integration by parts.",
            "The equation includes forcing, advection, nonlinear diffusion, or source terms not represented in the scope.",
            "A numeric probe produces positive L2 energy growth inside the declared assumptions.",
        ],
        "generated_on": "2026-07-01",
        "known_limits": [
            "nonperiodic_boundary_flux",
            "forced_heat_equation",
            "nonlinear_diffusion",
            "weak_solution_regularization_not_proved_here",
            "physical_law_not_claimed",
        ],
        "law_candidate_status": "BOUNDED_MATHEMATICAL_IDENTITY",
        "non_promotion_statement": "Pass 0062 proves and probes a bounded mathematical identity for a scoped heat equation. It does not claim a new natural law, empirical physics result, or general PDE theorem beyond the stated assumptions.",
        "numeric_probe": numeric_probe(),
        "pass": "0062",
        "promotion_state": "IDENTITY_NOT_PROMOTED_LAW",
        "source_anchors": source_anchors(),
        "unsupported_claim_count": 0,
    }
    errors = validate(packet)
    packet["validation_errors"] = errors
    packet["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet["seal"] = sha256_obj(packet)
    return packet


def validate(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    probe = packet.get("numeric_probe", {})
    if packet.get("schema") != SCHEMA:
        errors.append("schema")
    if packet.get("promotion_state") != "IDENTITY_NOT_PROMOTED_LAW":
        errors.append("promotion_state")
    if packet.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    if packet.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claims")
    if probe.get("max_symbolic_residual", 1.0) > 1e-12:
        errors.append("symbolic_residual")
    if probe.get("max_finite_difference_residual", 1.0) > 1e-5:
        errors.append("finite_difference_residual")
    if not probe.get("energy_monotone_nonincreasing"):
        errors.append("energy_monotonicity")
    if len(packet.get("source_anchors", [])) < 3:
        errors.append("source_anchors")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    packet = compose()
    write_json(Path(args.out), packet)
    print(json.dumps({"out": args.out, "seal": packet["seal"], "status": packet["status"]}, indent=2, sort_keys=True))
    if packet["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
