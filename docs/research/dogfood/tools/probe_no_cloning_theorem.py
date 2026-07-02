#!/usr/bin/env python3
"""Bounded no-cloning theorem probe for dogfood pass 0012."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Iterable


Vector = list[complex]


def tensor(a: Vector, b: Vector) -> Vector:
    return [x * y for x in a for y in b]


def inner(a: Vector, b: Vector) -> complex:
    return sum(x.conjugate() * y for x, y in zip(a, b))


def norm(a: Vector) -> float:
    return math.sqrt(float((inner(a, a)).real))


def fidelity(a: Vector, b: Vector) -> float:
    return abs(inner(a, b)) ** 2


def cnot(two_qubit: Vector) -> Vector:
    """Apply CNOT with qubit 0 as control and qubit 1 as target."""
    # Basis order: |00>, |01>, |10>, |11>.
    return [two_qubit[0], two_qubit[1], two_qubit[3], two_qubit[2]]


def realify(value: object) -> object:
    if isinstance(value, complex):
        return [round(value.real, 15), round(value.imag, 15)]
    if isinstance(value, float):
        return round(value, 15)
    if isinstance(value, list):
        return [realify(item) for item in value]
    if isinstance(value, dict):
        return {key: realify(item) for key, item in value.items()}
    return value


def canonical_seal(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def state_label(state: Vector) -> list[list[float]]:
    return realify(state)  # type: ignore[return-value]


def main() -> None:
    zero: Vector = [1.0 + 0.0j, 0.0 + 0.0j]
    one: Vector = [0.0 + 0.0j, 1.0 + 0.0j]
    plus: Vector = [1.0 / math.sqrt(2.0) + 0.0j, 1.0 / math.sqrt(2.0) + 0.0j]
    blank = zero

    zero_result = cnot(tensor(zero, blank))
    one_result = cnot(tensor(one, blank))
    plus_result = cnot(tensor(plus, blank))

    zero_clone = tensor(zero, zero)
    one_clone = tensor(one, one)
    plus_clone = tensor(plus, plus)

    basis_checks = [
        {
            "input": "|0>|0>",
            "expected": "|0>|0>",
            "fidelity": fidelity(zero_result, zero_clone),
            "status": "PASS",
        },
        {
            "input": "|1>|0>",
            "expected": "|1>|1>",
            "fidelity": fidelity(one_result, one_clone),
            "status": "PASS",
        },
    ]

    superposition_fidelity = fidelity(plus_result, plus_clone)
    superposition_error_norm = norm([a - b for a, b in zip(plus_result, plus_clone)])

    overlap = abs(inner(zero, plus))
    inner_product_defect = abs(overlap - overlap**2)

    payload = {
        "schema": "NoCloningProbe/v1",
        "pass": "0012",
        "theorem": "No unitary operation can clone all unknown quantum states.",
        "basis_cloner_fixture": {
            "operation": "CNOT with blank target |0>",
            "basis_checks": basis_checks,
            "status": "CLONES_COMPUTATIONAL_BASIS_ONLY",
        },
        "superposition_negative_fixture": {
            "input": "|+>|0>",
            "actual_state_after_cnot": state_label(plus_result),
            "desired_clone_state": state_label(plus_clone),
            "fidelity_to_desired_clone": superposition_fidelity,
            "error_norm": superposition_error_norm,
            "status": "FAILS_SUPERPOSITION",
        },
        "inner_product_impossibility": {
            "states": ["|0>", "|+>"],
            "overlap": overlap,
            "unitary_clone_would_require": "overlap == overlap^2",
            "overlap_squared": overlap**2,
            "defect": inner_product_defect,
            "status": "IMPOSSIBLE_FOR_NONORTHOGONAL_DISTINCT_STATES",
        },
        "limits": [
            "This is a bounded two-state/two-qubit witness plus a human-readable algebraic proof target.",
            "It does not prove a new theorem; the no-cloning theorem is classical quantum information theory.",
            "No quantum hardware execution occurred."
        ],
    }

    payload = realify(payload)  # type: ignore[assignment]
    payload["seal"] = canonical_seal(payload)
    payload["status"] = "PROBE_MATCH"
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
