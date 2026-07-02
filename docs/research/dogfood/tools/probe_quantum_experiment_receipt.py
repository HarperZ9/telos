#!/usr/bin/env python3
"""Generate quantum experiment receipt fixtures for dogfood pass 0013."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any


Vector = list[complex]


def tensor(a: Vector, b: Vector) -> Vector:
    return [x * y for x in a for y in b]


def inner(a: Vector, b: Vector) -> complex:
    return sum(x.conjugate() * y for x, y in zip(a, b))


def fidelity(a: Vector, b: Vector) -> float:
    return abs(inner(a, b)) ** 2


def cnot(two_qubit: Vector) -> Vector:
    return [two_qubit[0], two_qubit[1], two_qubit[3], two_qubit[2]]


def z_on_target(two_qubit: Vector) -> Vector:
    # Basis order |00>, |01>, |10>, |11>; target=1 basis states get phase -1.
    return [two_qubit[0], -two_qubit[1], two_qubit[2], -two_qubit[3]]


def histogram(state: Vector) -> dict[str, float]:
    labels = ["00", "01", "10", "11"]
    return {label: round(abs(amplitude) ** 2, 15) for label, amplitude in zip(labels, state)}


def realify(value: Any) -> Any:
    if isinstance(value, complex):
        return [round(value.real, 15), round(value.imag, 15)]
    if isinstance(value, float):
        return round(value, 15)
    if isinstance(value, list):
        return [realify(item) for item in value]
    if isinstance(value, dict):
        return {key: realify(item) for key, item in value.items()}
    return value


def seal(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    zero: Vector = [1.0 + 0.0j, 0.0 + 0.0j]
    plus: Vector = [1.0 / math.sqrt(2.0) + 0.0j, 1.0 / math.sqrt(2.0) + 0.0j]
    blank = zero

    exact_state = cnot(tensor(plus, blank))
    phase_flipped_state = z_on_target(exact_state)
    desired_clone = tensor(plus, plus)

    phase_error_probability = 0.1
    exact_fidelity = fidelity(exact_state, desired_clone)
    phase_flipped_fidelity = fidelity(phase_flipped_state, desired_clone)
    noisy_mixture_fidelity = (
        (1.0 - phase_error_probability) * exact_fidelity
        + phase_error_probability * phase_flipped_fidelity
    )

    exact_histogram = histogram(exact_state)
    noisy_histogram = {
        key: round(
            (1.0 - phase_error_probability) * exact_histogram[key]
            + phase_error_probability * histogram(phase_flipped_state)[key],
            15,
        )
        for key in exact_histogram
    }
    histogram_l1_drift = sum(abs(noisy_histogram[key] - exact_histogram[key]) for key in exact_histogram)

    receipt = {
        "schema": "QuantumExperimentReceiptSet/v1",
        "pass": "0013",
        "generated_on": "2026-07-01",
        "experiment_id": "no-cloning-plus-state-cnot-fixture",
        "receipts": [
            {
                "receipt_id": "quantum-exp-pass-0013-exact-simulator",
                "schema": "QuantumExperimentReceipt/v1",
                "branch": "EXACT_SIMULATOR",
                "hardware_claim_allowed": False,
                "theorem_claim_ref": "claim-no-cloning-inner-product-identity",
                "circuit": {
                    "source_state": "|+>|0>",
                    "operations": ["H(q0)", "CNOT(q0,q1)"],
                    "qubits": 2,
                    "gate_count": 2,
                    "two_qubit_gate_count": 1,
                    "depth": 2,
                },
                "backend": {
                    "sdk": "local-python-fixture",
                    "simulator": "statevector",
                    "noise_model": "none",
                    "shots": "analytic",
                    "seed": "deterministic-no-random-seed",
                },
                "resource_estimate": {
                    "logical_qubits": 2,
                    "physical_qubits": "not_applicable",
                    "qec_scheme": "none",
                    "gate_count": 2,
                    "depth": 2,
                    "runtime_estimate": "local analytic fixture",
                },
                "result": {
                    "statevector": realify(exact_state),
                    "measurement_histogram": exact_histogram,
                    "fidelity_to_desired_clone": exact_fidelity,
                    "status": "FAILS_CLONING_AS_EXPECTED",
                },
                "verdict": "MATCH",
            },
            {
                "receipt_id": "quantum-exp-pass-0013-noisy-simulator",
                "schema": "QuantumExperimentReceipt/v1",
                "branch": "NOISY_SIMULATOR",
                "hardware_claim_allowed": False,
                "theorem_claim_ref": "claim-no-cloning-inner-product-identity",
                "circuit": {
                    "source_state": "|+>|0>",
                    "operations": ["H(q0)", "CNOT(q0,q1)", "phase_error_on_target_with_probability_0.1"],
                    "qubits": 2,
                    "gate_count": 2,
                    "two_qubit_gate_count": 1,
                    "depth": 2,
                },
                "backend": {
                    "sdk": "local-python-fixture",
                    "simulator": "density-mixture-analytic",
                    "noise_model": "target_phase_flip_probability_0.1",
                    "shots": "analytic",
                    "seed": "deterministic-no-random-seed",
                },
                "resource_estimate": {
                    "logical_qubits": 2,
                    "physical_qubits": "not_applicable",
                    "qec_scheme": "none",
                    "gate_count": 2,
                    "depth": 2,
                    "runtime_estimate": "local analytic fixture",
                },
                "result": {
                    "mixture_components": [
                        {
                            "weight": 0.9,
                            "state": realify(exact_state),
                            "fidelity_to_desired_clone": exact_fidelity,
                        },
                        {
                            "weight": 0.1,
                            "state": realify(phase_flipped_state),
                            "fidelity_to_desired_clone": phase_flipped_fidelity,
                        },
                    ],
                    "measurement_histogram": noisy_histogram,
                    "fidelity_to_desired_clone": noisy_mixture_fidelity,
                    "histogram_l1_drift_from_exact": histogram_l1_drift,
                    "status": "NOISY_BRANCH_NOT_THEOREM_PROOF",
                },
                "verdict": "MATCH_WITH_BRANCH_WARNING",
            },
        ],
        "branch_separation": {
            "rule": "Simulator evidence, noisy-simulator evidence, hardware-mock evidence, and cloud-hardware evidence must not be promoted across branch boundaries.",
            "histogram_warning": "The noisy phase-flip branch has the same computational-basis histogram as the exact branch, so histogram equality alone is insufficient evidence.",
            "status": "BRANCH_SEPARATION_MATCH",
        },
    }
    receipt = realify(receipt)
    receipt["seal"] = seal(receipt)
    receipt["status"] = "RECEIPT_SET_MATCH"
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
