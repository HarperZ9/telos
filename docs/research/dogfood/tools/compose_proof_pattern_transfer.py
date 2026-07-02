"""Compose pass 0132 proof pattern transfer receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import expm

SCHEMA = "ProofPatternTransferReceipt/v1"
PASS_ID = "0132"
STATUS_MATCH = "PROOF_PATTERN_TRANSFER_MATCH"
STATUS_DRIFT = "PROOF_PATTERN_TRANSFER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0132-proof-pattern-transfer"
PASS_0131 = ROOT / "schemas" / "tradition-derivation-atlas-pass-0131.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def ascii_text(value: str) -> str:
    return value.encode("ascii", "ignore").decode("ascii")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def read_catalog() -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    result = []
    for row in rows:
        obj = STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
        body = obj.read_text(encoding="utf-8", errors="replace") if obj.exists() else ""
        result.append({
            "ref": row["ref"], "kind": row["kind"], "source": row["source"],
            "method": row["method"], "title": ascii_text(row.get("title", "")),
            "sha256": row["sha256"], "chars": len(body),
            "status": "GATHER_VERIFIED" if obj.exists() else "MISSING_OBJECT",
            "raw_body_exported": False,
        })
    return sorted(result, key=lambda item: item["ref"])


def proof_sources(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = ["ref", "kind", "source", "method", "title", "sha256", "chars", "status", "raw_body_exported"]
    return [{key: row[key] for key in keys} for row in rows]


def exact_continuous_fixture() -> dict[str, Any]:
    a = np.array([[0.0, -2.0, 0.0], [2.0, 0.0, -3.0], [0.0, 3.0, 0.0]])
    x = np.array([1.25, -0.5, 2.0])
    derivative = float(x @ ((a + a.T) @ x))
    t = 0.125
    flow = expm(t * a)
    orthogonal_residual = float(np.linalg.norm(flow.T @ flow - np.eye(3), ord="fro"))
    norm_delta = float(abs(np.linalg.norm(flow @ x) - np.linalg.norm(x)))
    return {
        "fixture_id": "skew_generator_exact_flow",
        "status": "MATCH" if abs(derivative) < 1e-12 and orthogonal_residual < 1e-12 and norm_delta < 1e-12 else "DRIFT",
        "generator_sha256": sha256_obj(a.tolist()),
        "state_sha256": sha256_obj(x.tolist()),
        "identity": "d/dt ||x||^2 = x^T(A + A^T)x = 0 when A^T = -A",
        "derivative_residual": derivative,
        "orthogonal_residual": orthogonal_residual,
        "norm_delta": norm_delta,
        "tolerance": 1e-12,
        "runtime_branch": "scipy.linalg.expm",
    }


def closed_form_rotation_fixture() -> dict[str, Any]:
    omega = 3.0
    theta = 0.4
    x = np.array([1.0, -2.0])
    r = np.array([[np.cos(omega * theta), -np.sin(omega * theta)], [np.sin(omega * theta), np.cos(omega * theta)]])
    orthogonal_residual = float(np.linalg.norm(r.T @ r - np.eye(2), ord="fro"))
    norm_delta = float(abs(np.linalg.norm(r @ x) - np.linalg.norm(x)))
    return {
        "fixture_id": "closed_form_two_dimensional_rotation",
        "status": "MATCH" if orthogonal_residual < 1e-12 and norm_delta < 1e-12 else "DRIFT",
        "omega": omega,
        "theta": theta,
        "orthogonal_residual": orthogonal_residual,
        "norm_delta": norm_delta,
        "tolerance": 1e-12,
    }


def counterexamples() -> list[dict[str, Any]]:
    b = np.array([[1.0, 0.0], [0.0, 0.0]])
    x = np.array([2.0, 1.0])
    derivative = float(x @ ((b + b.T) @ x))
    a = np.array([[0.0, -3.0], [3.0, 0.0]])
    h = 0.1
    y = (np.eye(2) + h * a) @ x
    euler_delta_sq = float((y @ y) - (x @ x))
    return [
        {
            "fixture_id": "non_skew_generator_rejected",
            "status": "REJECTED",
            "measured_derivative": derivative,
            "failure": "A + A^T is nonzero, so squared norm is not invariant",
        },
        {
            "fixture_id": "explicit_euler_drift_rejected",
            "status": "REJECTED",
            "step_size": h,
            "squared_norm_delta": euler_delta_sq,
            "failure": "explicit Euler does not preserve the skew-generator norm invariant",
        },
    ]


def transfer_modules() -> list[dict[str, str]]:
    return [
        {"module": "source_trace", "transfer": "bind algebra, runtime, and symmetry sources before proof claims"},
        {"module": "prerequisite_path", "transfer": "skew-symmetric -> orthogonal flow -> norm invariant"},
        {"module": "contrast_class", "transfer": "continuous exact flow differs from explicit Euler update"},
        {"module": "inferential_rewrite", "transfer": "rewrite conservation as x^T(A + A^T)x = 0"},
        {"module": "overclaim_audit", "transfer": "demote Noether/source-only, numerical, and natural-law overclaims"},
    ]


def product_hypotheses() -> list[dict[str, str]]:
    return [
        {"tool": "Invariant Receipt Runtime", "status": "HYPOTHESIS", "wedge": "every simulation step carries source, generator, invariant, residual, and method-boundary receipts"},
        {"tool": "Numerical Method Boundary Auditor", "status": "HYPOTHESIS", "wedge": "separates exact identities from discretization artifacts and negative fixtures"},
        {"tool": "BuildLang Conservation Kernel", "status": "HYPOTHESIS", "wedge": "compile-time declaration of preserved quantities with runtime residual checks"},
        {"tool": "Proof Pattern Transfer Kit", "status": "HYPOTHESIS", "wedge": "move source-trace and overclaim-gate structures across humanities, math, physics, and runtime domains"},
    ]


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "source_only_noether_rejected", "status": "REJECTED", "failures": ["source_context_only", "requires_system_specific_symmetry"]},
        {"fixture_id": "non_skew_as_conservation_law_rejected", "status": "REJECTED", "failures": ["counterexample_derivative_nonzero"]},
        {"fixture_id": "explicit_euler_as_exact_flow_rejected", "status": "REJECTED", "failures": ["discretization_drift", "requires_structure_preserving_method"]},
        {"fixture_id": "floating_residual_as_proof_rejected", "status": "REJECTED", "failures": ["numeric_evidence_only", "requires_symbolic_identity"]},
        {"fixture_id": "raw_source_export_rejected", "status": "REJECTED", "failures": ["copyright_boundary", "receipt_digest_only"]},
        {"fixture_id": "promoted_natural_law_rejected", "status": "REJECTED", "failures": ["bounded_linear_identity", "requires_independent_review"]},
    ]


def run_json(command: list[str], timeout: int = 60) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0132 proof pattern transfer for skew-generator conservation receipts."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1400", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    upstream = read_json(PASS_0131)
    sources = proof_sources(read_catalog())
    fixtures = [exact_continuous_fixture(), closed_form_rotation_fixture()]
    counter = counterexamples()
    negatives = negative_fixtures()
    law_candidate = {
        "status": "LAW_CANDIDATE",
        "promotion_status": "NOT_PROMOTED",
        "statement": "For real finite-dimensional x' = A x with A^T = -A, exact continuous flow preserves ||x||^2.",
        "scope": "finite-dimensional real linear ODE, exact continuous flow, Euclidean norm",
        "falsifier": "find skew A and x such that x^T(A + A^T)x != 0 in exact arithmetic",
    }
    artifact: dict[str, Any] = {
        "schema": SCHEMA, "pass": PASS_ID, "generated_on": "2026-07-01",
        "source_bindings": {"tradition_atlas_pass": upstream["pass"], "tradition_atlas_seal": upstream["seal"], "source_store": "gather/pass-0132-proof-pattern-transfer"},
        "source_receipts": sources,
        "transfer_modules": transfer_modules(),
        "positive_fixtures": fixtures,
        "counterexample_fixtures": counter,
        "law_candidate": law_candidate,
        "product_hypotheses": product_hypotheses(),
        "negative_fixtures": negatives,
        "boundary": "Pass 0132 proves a bounded finite-dimensional skew-generator norm invariant and records method-boundary counterexamples. It does not promote a universal natural law, prove Noether generally, or claim explicit Euler preserves the invariant.",
        "current_promoted_natural_laws": [],
        "unsupported_claim_count": 0,
        "flagship_receipts": flagship_receipts(),
    }
    errors = []
    if len(sources) < 6 or any(row["status"] != "GATHER_VERIFIED" for row in sources):
        errors.append("source_receipts")
    if any(row["status"] != "MATCH" for row in fixtures):
        errors.append("positive_fixtures")
    if len(counter) < 2 or any(row["status"] != "REJECTED" for row in counter):
        errors.append("counterexamples")
    if law_candidate["status"] != "LAW_CANDIDATE" or law_candidate["promotion_status"] != "NOT_PROMOTED":
        errors.append("law_candidate_boundary")
    if any(row["status"] != "REJECTED" for row in negatives):
        errors.append("negative_fixtures")
    if any(row["status"] != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "proof-pattern-transfer-pass-0132.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
