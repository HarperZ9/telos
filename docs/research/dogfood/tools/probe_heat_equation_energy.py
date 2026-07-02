"""Probe the 1D heat-equation energy identity with explicit finite differences."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any


def simulate(*, grid_points: int, alpha: float, cfl: float, steps: int) -> dict[str, Any]:
    dx = 1.0 / (grid_points - 1)
    dt = cfl * dx * dx / alpha
    x = [i * dx for i in range(grid_points)]
    u = [math.sin(math.pi * xi) + 0.25 * math.sin(3.0 * math.pi * xi) for xi in x]
    u[0] = 0.0
    u[-1] = 0.0

    energies = []
    for _ in range(steps + 1):
        energy = dx * sum(value * value for value in u)
        energies.append(energy)
        next_u = u[:]
        for i in range(1, grid_points - 1):
            next_u[i] = u[i] + cfl * (u[i - 1] - 2.0 * u[i] + u[i + 1])
        u = next_u

    increases = [
        {
            "step": i,
            "before": energies[i],
            "after": energies[i + 1],
            "increase": energies[i + 1] - energies[i],
        }
        for i in range(len(energies) - 1)
        if energies[i + 1] > energies[i] + 1e-12
    ]

    return {
        "grid_points": grid_points,
        "alpha": alpha,
        "dx": dx,
        "dt": dt,
        "cfl": cfl,
        "steps": steps,
        "initial_energy": energies[0],
        "final_energy": energies[-1],
        "max_single_step_increase": max(
            [0.0] + [energies[i + 1] - energies[i] for i in range(len(energies) - 1)]
        ),
        "increase_count": len(increases),
        "first_increase": increases[0] if increases else None,
        "status": "ENERGY_MONOTONE" if not increases else "ENERGY_INCREASE_DETECTED",
    }


def main() -> int:
    result = {
        "schema": "HeatEquationEnergyProbe/v1",
        "identity": "For u_t = alpha u_xx with zero Dirichlet boundary conditions, d/dt int u^2 dx = -2 alpha int |u_x|^2 dx <= 0.",
        "stable_probe": simulate(grid_points=129, alpha=1.0, cfl=0.45, steps=400),
        "unstable_probe": simulate(grid_points=129, alpha=1.0, cfl=0.55, steps=400),
        "interpretation": {
            "stable_expected": "The explicit scheme should preserve discrete energy monotonicity for this smooth test under a conservative CFL.",
            "unstable_expected": "The intentionally high CFL run is a negative fixture and should detect energy growth.",
            "limits": "This is a bounded numerical witness and not a substitute for the continuous integration-by-parts proof.",
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["seal"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    result["status"] = (
        "PROBE_MATCH"
        if result["stable_probe"]["status"] == "ENERGY_MONOTONE"
        and result["unstable_probe"]["status"] == "ENERGY_INCREASE_DETECTED"
        else "DRIFT"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PROBE_MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
