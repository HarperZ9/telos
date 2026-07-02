"""Compose pass 0119 Hamiltonian/symplectic receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "HamiltonianSymplecticReceipt/v1"
PASS_ID = "0119"
STATUS_MATCH = "HAMILTONIAN_SYMPLECTIC_MATCH"
STATUS_DRIFT = "HAMILTONIAN_SYMPLECTIC_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
FORMAL_PACKAGE = ROOT / "schemas" / "formal-target-packaging-receipt-pass-0118.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def fstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*a)]


def det2(m: list[list[Fraction]]) -> Fraction:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def apply_matrix(m: list[list[Fraction]], x: list[Fraction]) -> list[Fraction]:
    return [sum(row[j] * x[j] for j in range(2)) for row in m]


def qform(s: list[list[Fraction]], x: list[Fraction]) -> Fraction:
    return sum(x[i] * s[i][j] * x[j] for i in range(2) for j in range(2))


def matrix_json(m: list[list[Fraction]]) -> list[list[str]]:
    return [[fstr(v) for v in row] for row in m]


def symplectic_case(h: Fraction, steps: int = 24) -> dict[str, Any]:
    m = [[1 - h * h, h], [-h, 1]]
    s = [[Fraction(1), -h / 2], [-h / 2, Fraction(1)]]
    j = [[Fraction(0), Fraction(1)], [Fraction(-1), Fraction(0)]]
    mt = transpose(m)
    invariant_ok = matmul(mt, matmul(s, m)) == s
    symplectic_form_ok = matmul(mt, matmul(j, m)) == j
    x = [Fraction(1), Fraction(0)]
    modified = [qform(s, x)]
    standard = [(x[0] * x[0] + x[1] * x[1]) / 2]
    for _ in range(steps):
        x = apply_matrix(m, x)
        modified.append(qform(s, x))
        standard.append((x[0] * x[0] + x[1] * x[1]) / 2)
    return {
        "h": fstr(h),
        "steps": steps,
        "matrix": matrix_json(m),
        "invariant_matrix": matrix_json(s),
        "determinant": fstr(det2(m)),
        "phase_space_area_preserved": det2(m) == 1,
        "symplectic_form_preserved": symplectic_form_ok,
        "modified_quadratic_invariant_preserved": invariant_ok and modified[0] == modified[-1],
        "modified_initial": fstr(modified[0]),
        "modified_final": fstr(modified[-1]),
        "standard_energy_initial": fstr(standard[0]),
        "standard_energy_final": fstr(standard[-1]),
        "standard_energy_exactly_preserved": standard[0] == standard[-1],
        "status": "MATCH" if det2(m) == 1 and symplectic_form_ok and modified[0] == modified[-1] else "DRIFT",
    }


def explicit_euler_negative(h: Fraction, steps: int = 24) -> dict[str, Any]:
    m = [[Fraction(1), h], [-h, Fraction(1)]]
    x = [Fraction(1), Fraction(0)]
    e0 = (x[0] * x[0] + x[1] * x[1]) / 2
    for _ in range(steps):
        x = apply_matrix(m, x)
    e1 = (x[0] * x[0] + x[1] * x[1]) / 2
    determinant = det2(m)
    return {
        "fixture_id": "explicit_euler_area_energy_growth",
        "h": fstr(h),
        "steps": steps,
        "matrix": matrix_json(m),
        "determinant": fstr(determinant),
        "expected_reject_reason": "determinant_exceeds_one_and_standard_energy_grows",
        "phase_space_area_preserved": determinant == 1,
        "standard_energy_initial": fstr(e0),
        "standard_energy_final": fstr(e1),
        "standard_energy_growth": e1 > e0,
        "status": "MATCH" if determinant > 1 and e1 > e0 else "DRIFT",
    }


def source_anchors() -> list[dict[str, str]]:
    return [
        {"tool": "SciML SymplecticRK", "url": "https://docs.sciml.ai/DiffEqDocs/latest/api/ordinarydiffeq/dynamicalodeexplicit/SymplecticRK/", "gap_status": "inferred"},
        {"tool": "SciML Dynamical ODE", "url": "https://docs.sciml.ai/DiffEqDocs/stable/types/dynamical_types/", "gap_status": "inferred"},
        {"tool": "ModelingToolkit", "url": "https://docs.sciml.ai/ModelingToolkit/", "gap_status": "inferred"},
        {"tool": "Modelica", "url": "https://modelica.org/", "gap_status": "inferred"},
        {"tool": "OpenModelica", "url": "https://www.openmodelica.org/", "gap_status": "inferred"},
        {"tool": "NVIDIA PhysicsNeMo", "url": "https://docs.nvidia.com/physicsnemo/index.html", "gap_status": "inferred"},
        {"tool": "COMSOL Multiphysics", "url": "https://www.comsol.com/comsol-multiphysics", "gap_status": "inferred"},
        {"tool": "MathWorks Simscape", "url": "https://www.mathworks.com/products/simscape.html", "gap_status": "inferred"},
        {"tool": "Drake", "url": "https://drake.mit.edu/", "gap_status": "inferred"},
        {"tool": "MuJoCo", "url": "https://mujoco.org/", "gap_status": "inferred"},
        {"tool": "FEniCS", "url": "https://fenicsproject.org/", "gap_status": "inferred"},
        {"tool": "PETSc", "url": "https://petsc.org/", "gap_status": "inferred"},
        {"tool": "Ansys Fluent", "url": "https://www.ansys.com/products/fluids/ansys-fluent", "gap_status": "inferred"},
        {"tool": "JAX Autodiff", "url": "https://docs.jax.dev/en/latest/automatic-differentiation.html", "gap_status": "inferred"},
    ]


def market_rows() -> list[dict[str, str]]:
    buyers = {
        "SciML SymplecticRK": "scientific computing and Hamiltonian simulation teams",
        "NVIDIA PhysicsNeMo": "physics-AI and engineering surrogate-model teams",
        "COMSOL Multiphysics": "engineering simulation and multiphysics teams",
        "MathWorks Simscape": "multidomain physical-modeling teams",
        "Drake": "robotics dynamics and verification teams",
        "MuJoCo": "robotics, biomechanics, graphics, and RL simulation teams",
        "PETSc": "HPC PDE and solver teams",
    }
    rows = []
    for anchor in source_anchors():
        rows.append({
            "tool": anchor["tool"],
            "buyer": buyers.get(anchor["tool"], "scientific computing users"),
            "proof_gap_hypothesis": "needs portable invariant receipts that bind source, update rule, exact witness, negative fixture, runtime branch, and verifier verdict",
            "gap_status": anchor["gap_status"],
            "source": anchor["url"],
        })
    return rows


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0119 Hamiltonian symplectic proof receipt for invariant-preserving scientific compute."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def telos_catalog() -> dict[str, Any]:
    code, stdout, stderr, _parsed = run_json(["node", "demo/catalog.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in stdout else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "summary_detected": "Project Telos MCP Catalog" in stdout}


def compose() -> dict[str, Any]:
    formal = read_json(FORMAL_PACKAGE)
    cases = [symplectic_case(Fraction(1, 3)), symplectic_case(Fraction(1, 2)), symplectic_case(Fraction(2, 3))]
    negative = explicit_euler_negative(Fraction(1, 3))
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"formal_target_packaging_pass": formal["pass"], "formal_target_packaging_seal": formal["seal"]},
        "identity": "For the scoped harmonic oscillator kick-drift symplectic Euler map, det(M)=1 and M^T S M=S for S=[[1,-h/2],[-h/2,1]].",
        "law_candidate": {"name": "scoped_symplectic_euler_modified_quadratic_invariant", "status": "LAW_CANDIDATE", "scope": "exact rational harmonic oscillator kick-drift update; not empirical physics and not a general theorem for arbitrary systems"},
        "symplectic_cases": cases,
        "negative_fixtures": [negative],
        "source_surface": {"anchor_count": len(source_anchors()), "anchors": source_anchors(), "market_rows": market_rows()},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0119 records a scoped computational law candidate for a bounded integrator identity. It does not claim new natural law, empirical physics discovery, or correctness beyond the stated update rule.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status(), "telos_catalog": telos_catalog()},
    }
    errors = []
    if any(row["status"] != "MATCH" for row in cases):
        errors.append("symplectic_cases")
    if negative["status"] != "MATCH":
        errors.append("negative_fixture")
    if artifact["source_surface"]["anchor_count"] < 12:
        errors.append("source_surface")
    if any(row.get("status") != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["measurements"] = [{"id": f"symplectic_h_{row['h']}", "status": row["status"]} for row in cases] + [{"id": negative["fixture_id"], "status": negative["status"]}]
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "hamiltonian-symplectic-receipt-pass-0119.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
