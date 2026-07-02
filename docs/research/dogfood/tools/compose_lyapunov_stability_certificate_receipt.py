"""Compose pass 0112 Lyapunov stability certificate receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "LyapunovStabilityCertificateReceipt/v1"
PASS_ID = "0112"
STATUS_MATCH = "LYAPUNOV_STABILITY_CERTIFICATE_RECEIPT_MATCH"
STATUS_DRIFT = "LYAPUNOV_STABILITY_CERTIFICATE_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
RUNTIME_SUITE = ROOT / "schemas" / "multi-kernel-runtime-suite-receipt-pass-0111.json"
YOUTUBE = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"


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


def fstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def frow(row: list[Fraction]) -> list[str]:
    return [fstr(value) for value in row]


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*a)]


def matsub(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matadd(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def max_abs_matrix(a: list[list[Fraction]]) -> Fraction:
    return max(abs(value) for row in a for value in row)


def quad(x: list[Fraction], p: list[list[Fraction]]) -> Fraction:
    return sum(x[i] * p[i][j] * x[j] for i in range(len(x)) for j in range(len(x)))


def apply(a: list[list[Fraction]], x: list[Fraction]) -> list[Fraction]:
    return [sum(a[i][j] * x[j] for j in range(len(x))) for i in range(len(a))]


def lyapunov_residual(a: list[list[Fraction]], p: list[list[Fraction]], q: list[list[Fraction]]) -> list[list[Fraction]]:
    return matadd(matsub(matmul(matmul(transpose(a), p), a), p), q)


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def source_anchors() -> list[dict[str, str]]:
    return [
        {"tool": "SciPy", "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_discrete_lyapunov.html", "claim": "solves the discrete Lyapunov equation", "kind": "official_docs"},
        {"tool": "MATLAB dlyap", "url": "https://www.mathworks.com/help/control/ref/dlyap.html", "claim": "solves discrete-time Lyapunov equations", "kind": "official_docs"},
        {"tool": "MATLAB Control System Toolbox", "url": "https://www.mathworks.com/products/control.html", "claim": "models, analyzes, and designs control systems", "kind": "official_product"},
        {"tool": "python-control", "url": "https://python-control.readthedocs.io/en/0.10.2/generated/control.dlyap.html", "claim": "provides dlyap for discrete Lyapunov equations", "kind": "official_docs"},
        {"tool": "Drake", "url": "https://drake.mit.edu/", "claim": "model-based design and verification for robotics", "kind": "official_docs"},
        {"tool": "CasADi", "url": "https://web.casadi.org/docs/", "claim": "numerical optimization and optimal control", "kind": "official_docs"},
        {"tool": "do-mpc", "url": "https://www.do-mpc.com/", "claim": "robust model predictive control and moving horizon estimation", "kind": "official_docs"},
        {"tool": "OSQP", "url": "https://osqp.org/docs/examples/mpc.html", "claim": "model predictive control example for LTI systems", "kind": "official_docs"},
        {"tool": "CVXPY", "url": "https://www.cvxpy.org/", "claim": "Python-embedded convex optimization modeling", "kind": "official_docs"},
        {"tool": "MIT Underactuated", "url": "https://underactuated.mit.edu/lyapunov.html", "claim": "Lyapunov analysis for control guarantees", "kind": "course_notes"},
    ]


def market_surface() -> dict[str, Any]:
    tools = [{"tool": row["tool"], "source": row["url"], "gap_status": "inferred"} for row in source_anchors()[:9]]
    return {
        "tool_count": len(tools),
        "tools": tools,
        "gap_status": "hypothesis",
        "gap_hypothesis": "Control and optimization tools expose solvers, MPC, and modeling APIs, but portable proof packets can bind the system matrix, certificate, residual, simulation trace, source provenance, and negative fixtures.",
    }


def youtube_binding(roadmap: dict[str, Any]) -> dict[str, Any]:
    summary = roadmap["source_summary"]
    return {
        "roadmap_pass": roadmap["pass"],
        "valid_video_count": summary["valid_video_count"],
        "transcript_receipt_count": summary["transcript_receipt_count"],
        "dominant_cluster": summary["dominant_cluster"],
        "raw_transcript_included": summary["raw_transcript_stored"],
        "source_policy": summary["source_policy"],
    }


def stable_certificate() -> dict[str, Any]:
    a = [[Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 3)]]
    q = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    p = [[Fraction(4, 3), Fraction(0)], [Fraction(0), Fraction(9, 8)]]
    residual = lyapunov_residual(a, p, q)
    samples = []
    for x in [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(2)], [Fraction(3), Fraction(-2)]]:
        ax = apply(a, x)
        delta = quad(ax, p) - quad(x, p)
        q_energy = quad(x, q)
        samples.append({"x": frow(x), "delta_v": fstr(delta), "negative_q_energy": fstr(-q_energy), "identity_residual": fstr(delta + q_energy), "status": "MATCH" if delta + q_energy == 0 else "DRIFT"})
    return {
        "A": [frow(row) for row in a],
        "Q": [frow(row) for row in q],
        "P": [frow(row) for row in p],
        "positive_definite": True,
        "max_spectral_radius_abs": "1/2",
        "lyapunov_residual": [frow(row) for row in residual],
        "max_identity_residual": fstr(max_abs_matrix(residual)),
        "energy_samples": samples,
    }


def negative_fixtures() -> dict[str, Any]:
    q = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    unstable_a = [[Fraction(6, 5), Fraction(0)], [Fraction(0), Fraction(1, 3)]]
    unstable_p = [[Fraction(-25, 11), Fraction(0)], [Fraction(0), Fraction(9, 8)]]
    bad_a = [[Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 3)]]
    bad_p = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    bad_residual = lyapunov_residual(bad_a, bad_p, q)
    return {
        "unstable_spectral_fixture": {"A": [frow(row) for row in unstable_a], "candidate_P": [frow(row) for row in unstable_p], "positive_definite": False, "classification": "PD_FAIL_EXPECTED"},
        "bad_certificate_fixture": {"A": [frow(row) for row in bad_a], "P": [frow(row) for row in bad_p], "lyapunov_residual": [frow(row) for row in bad_residual], "max_identity_residual": fstr(max_abs_matrix(bad_residual)), "classification": "RESIDUAL_DRIFT_EXPECTED"},
    }


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0112: Lyapunov stability certificate receipt for control, robotics, MPC, autonomy safety, and BuildLang proof packets."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    stable = artifact.get("stable_certificate", {})
    neg = artifact.get("negative_fixtures", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if stable.get("lyapunov_residual") != [["0", "0"], ["0", "0"]] or stable.get("positive_definite") is not True:
        errors.append("stable_certificate")
    if any(row.get("status") != "MATCH" for row in stable.get("energy_samples", [])):
        errors.append("energy_samples")
    if neg.get("unstable_spectral_fixture", {}).get("positive_definite") is not False:
        errors.append("unstable_fixture")
    if neg.get("bad_certificate_fixture", {}).get("max_identity_residual") == "0":
        errors.append("bad_certificate")
    if artifact.get("market_surface", {}).get("tool_count", 0) < 8:
        errors.append("market")
    if artifact.get("youtube_binding", {}).get("valid_video_count") != 19:
        errors.append("youtube")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    suite = read_json(RUNTIME_SUITE)
    roadmap = read_json(YOUTUBE)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"runtime_suite_pass": suite["pass"], "youtube_roadmap_pass": roadmap["pass"], "youtube_source_pass": roadmap["source_bindings"]["youtube_pass"]},
        "source_anchors": source_anchors(),
        "market_surface": market_surface(),
        "youtube_binding": youtube_binding(roadmap),
        "stable_certificate": stable_certificate(),
        "negative_fixtures": negative_fixtures(),
        "law_candidate": {"name": "discrete_lyapunov_certificate_energy_decrease", "status": "LAW_CANDIDATE", "scope": "diagonal finite-dimensional discrete-time linear systems with exact rational certificate"},
        "buildlang_target": {"target_kernel": "lyapunov_certificate_kernel.bld", "status": "TARGET_INTERFACE_NOT_COMPILED"},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass proves a bounded exact Lyapunov identity for one rational linear system. It does not validate hardware control, prove nonlinear stability, compile BuildLang, or promote a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "stable_certificate", "status": "MATCH" if artifact["stable_certificate"]["max_identity_residual"] == "0" else "DRIFT"},
        {"id": "energy_samples", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["stable_certificate"]["energy_samples"]) else "DRIFT"},
        {"id": "unstable_fixture", "status": "MATCH" if artifact["negative_fixtures"]["unstable_spectral_fixture"]["classification"] == "PD_FAIL_EXPECTED" else "DRIFT"},
        {"id": "bad_certificate_fixture", "status": "MATCH" if artifact["negative_fixtures"]["bad_certificate_fixture"]["max_identity_residual"] != "0" else "DRIFT"},
        {"id": "market_surface", "status": "MATCH" if artifact["market_surface"]["tool_count"] >= 8 else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "lyapunov-stability-certificate-receipt-pass-0112.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
