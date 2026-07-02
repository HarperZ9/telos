"""Compose pass 0107 reaction-network corpus harness receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "ReactionNetworkCorpusHarnessReceipt/v1"
PASS_ID = "0107"
STATUS_MATCH = "REACTION_NETWORK_CORPUS_HARNESS_RECEIPT_MATCH"
STATUS_DRIFT = "REACTION_NETWORK_CORPUS_HARNESS_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PASS0106 = ROOT / "tools" / "compose_stoichiometric_invariant_checker_receipt.py"
STOICH = ROOT / "schemas" / "stoichiometric-invariant-checker-receipt-pass-0106.json"
BUILDLANG = ROOT / "schemas" / "buildlang-native-optimization-kernel-receipt-pass-0095.json"
SCORECARD = ROOT / "schemas" / "youtube-field-growth-vector-scorecard-pass-0096.json"
ROADMAP = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"


def load_stoich_module():
    spec = importlib.util.spec_from_file_location("compose_stoichiometric_invariant_checker_receipt", PASS0106)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ST = load_stoich_module()


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


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def network_specs() -> list[dict[str, Any]]:
    return [
        {"id": "closed_cycle_abc", "species": ["A", "B", "C"], "reactions": ["A_to_B", "B_to_C", "C_to_A"], "matrix": [[-1, 0, 1], [1, -1, 0], [0, 1, -1]], "candidates": [[1, 1, 1]], "initial": [2.0, 0.5, 1.25], "expected": "MATCH"},
        {"id": "reversible_dimerization", "species": ["A", "B"], "reactions": ["2A_to_B", "B_to_2A"], "matrix": [[-2, 2], [1, -1]], "candidates": [[1, 2]], "initial": [3.0, 0.2], "expected": "MATCH"},
        {"id": "enzyme_product_skeleton", "species": ["E", "S", "ES", "P"], "reactions": ["E_plus_S_to_ES", "ES_to_E_plus_S", "ES_to_E_plus_P"], "matrix": [[-1, 1, 1], [-1, 1, 0], [1, -1, -1], [0, 0, 1]], "candidates": [[1, 0, 1, 0], [0, 1, 1, 1]], "initial": [1.0, 2.0, 0.1, 0.0], "expected": "MATCH"},
        {"id": "open_degradation", "species": ["A"], "reactions": ["A_to_sink"], "matrix": [[-1]], "candidates": [[1]], "initial": [2.0], "expected": "DRIFT_EXPECTED"},
    ]


def rate_vector(network_id: str, state: list[float]) -> list[float]:
    if network_id == "closed_cycle_abc":
        return [0.23 * state[0], 0.31 * state[1], 0.17 * state[2]]
    if network_id == "reversible_dimerization":
        return [0.015 * state[0] * state[0], 0.04 * state[1]]
    if network_id == "enzyme_product_skeleton":
        return [0.02 * state[0] * state[1], 0.03 * state[2], 0.04 * state[2]]
    return [0.1 * state[0]]


def numerical_probe(spec: dict[str, Any]) -> dict[str, Any]:
    state = [float(value) for value in spec["initial"]]
    starts = [sum(vec[i] * state[i] for i in range(len(state))) for vec in spec["candidates"]]
    dt, steps = 0.025, 200
    max_drifts = [0.0 for _ in starts]
    for _ in range(steps + 1):
        for idx, vec in enumerate(spec["candidates"]):
            current = sum(vec[i] * state[i] for i in range(len(state)))
            max_drifts[idx] = max(max_drifts[idx], abs(current - starts[idx]))
        rates = rate_vector(spec["id"], state)
        matrix = spec["matrix"]
        deltas = [sum(matrix[row][col] * rates[col] for col in range(len(rates))) * dt for row in range(len(state))]
        state = [state[idx] + deltas[idx] for idx in range(len(state))]
    return {"grid_points": steps + 1, "initial_invariants": starts, "max_invariant_drifts": max_drifts, "max_drift": max(max_drifts), "final_state": state}


def candidate_check(spec: dict[str, Any], vector: list[int]) -> dict[str, Any]:
    res = ST.residual(vector, spec["matrix"])
    return {"vector": vector, "invariant": ST.invariant_label(spec["species"], vector), "residual": res, "residual_zero": all(value == 0 for value in res)}


def evaluate_network(spec: dict[str, Any]) -> dict[str, Any]:
    basis = ST.nullspace(ST.transpose(spec["matrix"]))
    derived = [candidate_check(spec, vector) for vector in basis]
    checks = [candidate_check(spec, vector) for vector in spec["candidates"]]
    probe = numerical_probe(spec)
    if spec["expected"] == "MATCH":
        status = "MATCH" if all(row["residual_zero"] for row in checks) and probe["max_drift"] <= 1e-10 else "DRIFT"
    else:
        status = "DRIFT_EXPECTED" if any(not row["residual_zero"] for row in checks) and probe["max_drift"] > 0.01 else "DRIFT"
    return {
        "network_id": spec["id"],
        "species": spec["species"],
        "reactions": spec["reactions"],
        "stoichiometric_matrix": spec["matrix"],
        "matrix_sha256": sha256_obj(spec["matrix"]),
        "basis_dimension": len(basis),
        "derived_conservation_vectors": derived,
        "candidate_checks": checks,
        "numerical_probe": probe,
        "status": status,
    }


def buildlang_bridge() -> dict[str, Any]:
    native = read_json(BUILDLANG)
    scorecard = read_json(SCORECARD)
    check = native["check_receipt"]
    binding = scorecard["buildlang_binding"]
    return {
        "status": "TARGET_SPECIFIED_WITH_EXISTING_BUILDC_RECEIPT",
        "native_pass": binding["native_pass"],
        "native_status": binding["native_status"],
        "compiler": check["compiler"],
        "compiler_version": check["compiler_version"],
        "source_digest": check["source_digest"]["hex"],
        "verify_check_count": binding["verify_check_count"],
        "target_kernel": "reaction_network_invariant_kernel.bld",
        "required_kernel_receipts": ["stoichiometric_matrix_digest", "conservation_vector_receipt", "residual_zero_check", "numeric_tolerance_receipt", "negative_fixture_receipt"],
        "boundary": "This pass does not compile a new BuildLang chemistry kernel; it binds the existing buildc receipt and specifies the next runtime receipt target.",
    }


def youtube_binding() -> dict[str, Any]:
    scorecard = read_json(SCORECARD)
    roadmap = read_json(ROADMAP)
    by_node = {row["node_id"]: row for row in roadmap["roadmap_nodes"]}
    return {
        "youtube_scorecard_pass": scorecard["pass"],
        "roadmap_pass": roadmap["pass"],
        "valid_video_count": roadmap["source_summary"]["valid_video_count"],
        "buildlang_scientific_runtime_video_count": by_node["buildlang_scientific_runtime"]["source_video_count"],
        "ai4science_video_count": by_node["ai4science_claim_to_experiment"]["source_video_count"],
        "architecture_pull": "move from single invariant packet to corpus and runtime receipt targets",
    }


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0107: reaction-network corpus harness, AI4Science conserved quantities, BuildLang scientific-runtime target receipts, YouTube critical-data roadmap."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def summarize(results: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "network_count": len(results),
        "match_count": sum(1 for row in results if row["status"] == "MATCH"),
        "drift_expected_count": sum(1 for row in results if row["status"] == "DRIFT_EXPECTED"),
        "derived_invariant_count": sum(len(row["derived_conservation_vectors"]) for row in results),
        "candidate_check_count": sum(len(row["candidate_checks"]) for row in results),
    }


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    summary = artifact.get("corpus_summary", {})
    bridge = artifact.get("buildlang_runtime_bridge", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if summary.get("network_count") != 4 or summary.get("match_count") != 3 or summary.get("drift_expected_count") != 1:
        errors.append("summary")
    if summary.get("derived_invariant_count", 0) < 4:
        errors.append("derived_invariants")
    if bridge.get("status") != "TARGET_SPECIFIED_WITH_EXISTING_BUILDC_RECEIPT" or bridge.get("verify_check_count") != 18:
        errors.append("buildlang_bridge")
    if artifact.get("youtube_signal_binding", {}).get("valid_video_count") != 19:
        errors.append("youtube_binding")
    if any(row.get("status") not in {"MATCH", "DRIFT_EXPECTED"} for row in artifact.get("network_results", [])):
        errors.append("network_status")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    stoich = read_json(STOICH)
    results = [evaluate_network(spec) for spec in network_specs()]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"stoichiometric_pass": stoich["pass"], "buildlang_native_pass": "0095", "youtube_scorecard_pass": "0096", "youtube_roadmap_pass": "0102"},
        "youtube_signal_binding": youtube_binding(),
        "source_anchors": ST.source_anchors(),
        "network_results": results,
        "corpus_summary": summarize(results),
        "buildlang_runtime_bridge": buildlang_bridge(),
        "law_candidate": {"name": "reaction_network_corpus_left_nullspace_conservation_harness", "status": "LAW_CANDIDATE", "scope": "bounded corpus of closed reaction networks with exact residual checks and open-network rejection fixtures"},
        "promotion_requirements": ["larger curated network corpus", "BuildLang chemistry kernel execution", "independent reproduction", "domain reviewer signoff"],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass proves only a bounded corpus harness and target BuildLang runtime bridge. It does not prove a new natural law, biological discovery, wet-lab result, or compiled chemistry kernel.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "corpus_summary", "status": "MATCH" if artifact["corpus_summary"]["network_count"] == 4 else "DRIFT"},
        {"id": "closed_networks", "status": "MATCH" if artifact["corpus_summary"]["match_count"] == 3 else "DRIFT"},
        {"id": "open_rejection", "status": "MATCH" if artifact["corpus_summary"]["drift_expected_count"] == 1 else "DRIFT"},
        {"id": "buildlang_bridge", "status": "MATCH" if artifact["buildlang_runtime_bridge"]["verify_check_count"] == 18 else "DRIFT"},
        {"id": "youtube_signal_binding", "status": "MATCH" if artifact["youtube_signal_binding"]["valid_video_count"] == 19 else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "reaction-network-corpus-harness-receipt-pass-0107.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
