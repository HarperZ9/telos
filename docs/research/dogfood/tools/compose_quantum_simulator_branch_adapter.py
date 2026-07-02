"""Compose pass 0087 simulator branch adapter contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "QuantumSimulatorBranchAdapterReceipt/v1"
PASS_ID = "0087"
STATUS_MATCH = "QUANTUM_SIMULATOR_BRANCH_ADAPTER_MATCH"
STATUS_DRIFT = "QUANTUM_SIMULATOR_BRANCH_ADAPTER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BASELINE = ROOT / "schemas" / "quantum-optimization-workflow-receipt-pass-0086.json"
SEEDS = list(range(8700, 8732))
BETAS = [0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4]
SWEEPS_PER_BETA = 12
SOURCE_ANCHORS = [
    {
        "source_id": "dwave-samplers-simulated-annealing",
        "url": "https://docs.dwavequantum.com/en/latest/ocean/api_ref_samplers/index.html",
        "claim": "D-Wave documents simulated annealing as useful for heuristic optimization or approximate Boltzmann sampling.",
        "verification_status": "SOURCE_LEAD",
    },
    {
        "source_id": "dwave-dimod-bqm-models",
        "url": "https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/models.html",
        "claim": "D-Wave dimod documentation describes binary quadratic model support and QUBO conversion surfaces.",
        "verification_status": "SOURCE_LEAD",
    },
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def item_vectors(baseline: dict[str, Any]) -> tuple[list[str], list[int], list[int], int, int]:
    items = baseline["optimization_problem"]["items"]
    return ([row["id"] for row in items], [row["value"] for row in items], [row["resource"] for row in items], baseline["optimization_problem"]["capacity"], baseline["optimization_problem"]["penalty"])


def energy(bits: list[int], values: list[int], resources: list[int], capacity: int, penalty: int) -> tuple[int, int, int, int]:
    value = sum(bit * val for bit, val in zip(bits, values))
    resource = sum(bit * res for bit, res in zip(bits, resources))
    violation = max(0, resource - capacity)
    return -value + penalty * violation * violation, value, resource, violation


def anneal(seed: int, values: list[int], resources: list[int], capacity: int, penalty: int) -> dict[str, Any]:
    rng = random.Random(seed)
    bits = [rng.randrange(2) for _ in values]
    best_bits = list(bits)
    best_energy, best_value, best_resource, best_violation = energy(bits, values, resources, capacity, penalty)
    accepted = 0
    proposals = 0
    for beta in BETAS:
        for _ in range(SWEEPS_PER_BETA):
            for index in rng.sample(range(len(bits)), len(bits)):
                current_energy = energy(bits, values, resources, capacity, penalty)[0]
                trial = list(bits)
                trial[index] = 1 - trial[index]
                trial_energy, value, resource, violation = energy(trial, values, resources, capacity, penalty)
                delta = trial_energy - current_energy
                proposals += 1
                if delta <= 0 or rng.random() < math.exp(-beta * delta):
                    bits = trial
                    accepted += 1
                    if (trial_energy, -value, resource) < (best_energy, -best_value, best_resource):
                        best_bits, best_energy, best_value, best_resource, best_violation = list(trial), trial_energy, value, resource, violation
    final_energy, final_value, final_resource, final_violation = energy(bits, values, resources, capacity, penalty)
    return {
        "seed": seed,
        "best_bits": best_bits,
        "best_energy": best_energy,
        "best_value": best_value,
        "best_resource": best_resource,
        "best_capacity_violation": best_violation,
        "final_bits": bits,
        "final_energy": final_energy,
        "final_value": final_value,
        "final_resource": final_resource,
        "final_capacity_violation": final_violation,
        "accepted_moves": accepted,
        "proposal_count": proposals,
    }


def simulator_receipt(baseline: dict[str, Any]) -> dict[str, Any]:
    names, values, resources, capacity, penalty = item_vectors(baseline)
    runs = [anneal(seed, values, resources, capacity, penalty) for seed in SEEDS]
    exact = baseline["measurement"]["best_feasible"]
    exact_bits = exact["bits"]
    exact_energy = exact["qubo_energy"]
    best = min(runs, key=lambda row: (row["best_energy"], -row["best_value"], row["best_resource"]))
    optimum_hits = sum(1 for row in runs if row["best_bits"] == exact_bits)
    feasible_best = sum(1 for row in runs if row["best_capacity_violation"] == 0)
    return {
        "adapter_id": "simulated_annealing_branch_seeded_v1",
        "external_analogs": ["D-Wave Ocean simulated annealing sampler", "neal SimulatedAnnealingSampler", "dimod BQM sampler API"],
        "source_anchors": SOURCE_ANCHORS,
        "run_count": len(runs),
        "seed_range": [SEEDS[0], SEEDS[-1]],
        "beta_schedule": BETAS,
        "sweeps_per_beta": SWEEPS_PER_BETA,
        "variable_order": names,
        "runs_sha256": sha256_obj(runs),
        "runs": runs,
        "best_run": best,
        "exact_baseline_bits": exact_bits,
        "exact_baseline_energy": exact_energy,
        "optimum_hit_count": optimum_hits,
        "best_feasible_count": feasible_best,
        "constraint_violation_rate": round(1 - feasible_best / len(runs), 6),
        "objective_values": sorted(row["best_value"] for row in runs),
        "replay_gate": "MATCH" if best["best_bits"] == exact_bits and optimum_hits > 0 else "DRIFT",
    }


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0087: seeded simulated annealing branch adapter contract compared against exact quantum optimization baseline receipt."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "missing_seed_record", "expected_status": "REJECT", "reject_reason": "stochastic_adapter_requires_seed_records"},
        {"fixture_id": "missing_exact_baseline", "expected_status": "REJECT", "reject_reason": "simulator_branch_requires_exact_baseline_comparison"},
        {"fixture_id": "single_run_promotion", "expected_status": "REJECT", "reject_reason": "stochastic_branch_requires_distribution_summary"},
        {"fixture_id": "quantum_hardware_claim", "expected_status": "REJECT", "reject_reason": "simulated_branch_is_not_hardware_execution"},
        {"fixture_id": "quantum_advantage_claim", "expected_status": "REJECT", "reject_reason": "simulated_branch_does_not_establish_quantum_advantage"},
        {"fixture_id": "unsealed_run_list", "expected_status": "REJECT", "reject_reason": "run_list_digest_required_for_replay"},
    ]


def compose() -> dict[str, Any]:
    baseline = read_json(BASELINE)
    simulator = simulator_receipt(baseline)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "baseline_binding": {"source_pass": "0086", "source_schema": baseline["schema"], "source_seal": baseline["seal"], "candidate_digest": baseline["measurement"]["all_candidates_sha256"]},
        "simulator_branch": simulator,
        "comparison_to_exact": {
            "status": simulator["replay_gate"],
            "exact_best_bits": simulator["exact_baseline_bits"],
            "simulator_best_bits": simulator["best_run"]["best_bits"],
            "exact_best_energy": simulator["exact_baseline_energy"],
            "simulator_best_energy": simulator["best_run"]["best_energy"],
            "optimum_hit_count": simulator["optimum_hit_count"],
            "run_count": simulator["run_count"],
        },
        "promotion_boundary": {"simulator_only": True, "quantum_hardware_claim": False, "quantum_advantage_claim": False, "new_physics_claim": False, "new_natural_law_claim": False},
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0087 verifies a seeded simulated-annealing branch against an exact toy baseline; it does not claim hardware execution, quantum advantage, new physics, or a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sim = artifact.get("simulator_branch", {})
    comparison = artifact.get("comparison_to_exact", {})
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("baseline_binding", {}).get("source_pass") != "0086":
        errors.append("baseline_binding")
    if sim.get("run_count") != 32 or sim.get("optimum_hit_count", 0) <= 0:
        errors.append("run_distribution")
    if comparison.get("status") != "MATCH" or comparison.get("exact_best_bits") != comparison.get("simulator_best_bits"):
        errors.append("baseline_comparison")
    if sim.get("runs_sha256") != sha256_obj(sim.get("runs", [])):
        errors.append("run_digest")
    if any(boundary.get(key) for key in ["quantum_hardware_claim", "quantum_advantage_claim", "new_physics_claim", "new_natural_law_claim"]):
        errors.append("promotion_boundary")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if len(artifact.get("negative_fixtures", [])) < 6:
        errors.append("negative_fixtures")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"out": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
