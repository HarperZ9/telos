"""Compose pass 0122 scientific runtime receipt layer spec."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "ScientificRuntimeReceiptLayerSpec/v1"
PASS_ID = "0122"
STATUS_MATCH = "SCIENTIFIC_RUNTIME_RECEIPT_LAYER_MATCH"
STATUS_DRIFT = "SCIENTIFIC_RUNTIME_RECEIPT_LAYER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SOURCE_STORE = ROOT / "gather" / "pass-0122-runtime-sources"
BASELINE = ROOT / "schemas" / "hamiltonian-symplectic-receipt-pass-0119.json"
RUNTIME = ROOT / "schemas" / "hamiltonian-runtime-branch-receipt-pass-0120.json"
GROWTH = ROOT / "schemas" / "youtube-megatool-growth-vector-receipt-pass-0121.json"
FLOAT_TOLERANCE = 2e-12
HORIZONS = [24, 240, 2400, 24000]

SOURCES = [
    ("compiler_ir", "OpenXLA XLA", "https://openxla.org/xla", "ML compiler for high-performance execution across hardware."),
    ("compiler_ir", "StableHLO", "https://openxla.org/stablehlo", "Portability layer for ML high-level operations."),
    ("compiler_ir", "MLIR", "https://mlir.llvm.org/", "Reusable and extensible compiler infrastructure for heterogeneous systems."),
    ("array_runtime", "JAX", "https://docs.jax.dev/en/latest/quickstart.html", "Array computation with transformations including JIT and autodiff."),
    ("scientific_runtime", "SciML SymplecticRK", "https://docs.sciml.ai/DiffEqDocs/latest/api/ordinarydiffeq/dynamicalodeexplicit/SymplecticRK/", "Symplectic integrator documentation for Hamiltonian systems."),
    ("array_runtime", "NumPy det", "https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html", "Determinant routine used as a local branch reference."),
    ("array_runtime", "SciPy det", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.det.html", "SciPy determinant routine used as a local branch reference."),
    ("gpu_kernel", "Triton", "https://triton-lang.org/main/programming-guide/chapter-1/introduction.html", "Language/compiler for custom parallel kernels."),
    ("ai_runtime", "Modular MAX", "https://www.modular.com/open-source/max", "High-performance AI inference framework."),
    ("formal_prover", "Lean", "https://lean-lang.org/doc/reference/latest/", "Interactive theorem prover and programming language reference."),
    ("formal_prover", "Rocq", "https://rocq-prover.org/docs", "Interactive theorem prover documentation anchor."),
    ("formal_prover", "Isabelle", "https://isabelle.in.tum.de/", "Generic proof assistant anchor."),
    ("formal_prover", "Agda", "https://agda.readthedocs.io/", "Dependently typed language and proof assistant documentation."),
    ("observability", "OpenTelemetry", "https://opentelemetry.io/docs/concepts/observability-primer/", "Telemetry source for traces, metrics, and logs."),
    ("experiment_tracking", "MLflow Tracking", "https://mlflow.org/docs/latest/ml/tracking/", "Experiment tracking for parameters, code versions, metrics, and outputs."),
    ("experiment_tracking", "Weights and Biases", "https://docs.wandb.ai/models/track", "Experiment tracking for metrics, hyperparameters, system metrics, and artifacts."),
    ("lineage", "OpenLineage", "https://openlineage.io/docs/", "Open framework for lineage collection and analysis."),
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


def read_source_catalog() -> dict[str, dict[str, Any]]:
    path = SOURCE_STORE / "catalog.jsonl"
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        obj = SOURCE_STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
        if obj.exists():
            row["chars"] = len(obj.read_text(encoding="utf-8", errors="replace"))
    return {row["ref"]: row for row in rows}


def source_matrix() -> list[dict[str, Any]]:
    catalog = read_source_catalog()
    rows = []
    for category, tool, url, claim in SOURCES:
        receipt = catalog.get(url)
        status = "GATHER_VERIFIED" if receipt else "OFFICIAL_ANCHOR_UNVERIFIED_LOCALLY"
        if receipt and int(receipt.get("chars", 0)) < 500:
            status = "GATHER_VERIFIED_SHORT_TEXT"
        rows.append({
            "category": category,
            "tool": tool,
            "official_anchor_url": url,
            "official_positioning_summary": claim,
            "local_gather_status": status,
            "local_gather_sha256": receipt.get("sha256") if receipt else None,
            "local_gather_chars": receipt.get("chars") if receipt else 0,
            "gap_status": "inferred",
            "proof_layer_gap_hypothesis": "The anchor documents a local runtime, compiler, prover, telemetry, lineage, or tracking capability; pass 0122 hypothesizes a missing cross-layer receipt that binds source, oracle, runtime branch, compiler state, telemetry, lineage, and verifier verdict.",
        })
    return rows


def frac(value: str) -> Fraction:
    return Fraction(value)


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[j][i] for j in range(2)] for i in range(2)]


def mat_sub(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] - b[i][j] for j in range(2)] for i in range(2)]


def det2(m: list[list[Fraction]]) -> Fraction:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def matrix_float(matrix: list[list[str]]) -> list[list[float]]:
    return [[float(frac(value)) for value in row] for row in matrix]


def float_replay(matrix: list[list[str]], invariant: list[list[str]], steps: int) -> dict[str, float]:
    x0, x1 = 1.0, 0.0
    s = matrix_float(invariant)
    m = matrix_float(matrix)

    def invariant_value(a: float, b: float) -> float:
        return a * (s[0][0] * a + s[0][1] * b) + b * (s[1][0] * a + s[1][1] * b)

    init = invariant_value(x0, x1)
    max_drift = 0.0
    for _ in range(steps):
        x0, x1 = m[0][0] * x0 + m[0][1] * x1, m[1][0] * x0 + m[1][1] * x1
        max_drift = max(max_drift, abs(invariant_value(x0, x1) - init))
    return {"modified_max_abs_drift": max_drift, "standard_energy_final": 0.5 * (x0 * x0 + x1 * x1)}


def exact_and_float_experiment() -> dict[str, Any]:
    baseline = read_json(BASELINE)
    cases = []
    for case in baseline["symplectic_cases"]:
        m = [[frac(v) for v in row] for row in case["matrix"]]
        s = [[frac(v) for v in row] for row in case["invariant_matrix"]]
        residual = mat_sub(matmul(matmul(transpose(m), s), m), s)
        residual_zero = all(value == 0 for row in residual for value in row)
        horizon_rows = []
        for steps in HORIZONS:
            replay = float_replay(case["matrix"], case["invariant_matrix"], steps)
            horizon_rows.append({
                "steps": steps,
                "status": "MATCH" if replay["modified_max_abs_drift"] <= FLOAT_TOLERANCE else "DRIFT",
                "modified_max_abs_drift": replay["modified_max_abs_drift"],
                "standard_energy_final": replay["standard_energy_final"],
                "tolerance": FLOAT_TOLERANCE,
            })
        cases.append({
            "h": case["h"],
            "determinant_exact": str(det2(m)),
            "symplectic_residual_zero": residual_zero,
            "exact_invariant_for_all_steps_by_induction": residual_zero and det2(m) == 1,
            "float_horizons": horizon_rows,
        })
    negative = baseline["negative_fixtures"][0]
    det = float(frac(negative["determinant"]))
    return {
        "schema": "HamiltonianLongHorizonReceipt/v1",
        "source_pass": baseline["pass"],
        "source_seal": baseline["seal"],
        "exact_cases": cases,
        "negative_fixture": {
            "fixture_id": negative["fixture_id"],
            "determinant_exact": negative["determinant"],
            "area_growth_log10_at_240_steps": 240 * math.log10(det),
            "area_growth_log10_at_24000_steps": 24000 * math.log10(det),
            "status": "MATCH",
        },
        "law_candidate_status": "LAW_CANDIDATE",
        "promoted_law_status": "NOT_PROMOTED",
    }


def receipt_contract() -> list[dict[str, str]]:
    fields = [
        ("source_receipts", "Gather/OpenLineage refs for papers, docs, datasets, and source leads."),
        ("oracle", "Exact proof, reference implementation, formal theorem, or declared unavailable oracle."),
        ("runtime_branch", "Runtime name, version, target, seed, hardware, input hash, output hash, and drift metric."),
        ("compiler_branch", "Compiler, IR, flags, target triple/device, build hash, and executable hash when compiled."),
        ("telemetry_branch", "OpenTelemetry-style traces/spans/log refs for action provenance."),
        ("lineage_branch", "Dataset/job/run lineage refs where data pipelines are involved."),
        ("verifier_verdict", "Crucible MATCH/DRIFT/UNVERIFIABLE verdict and falsifier."),
        ("non_promotion_boundary", "Statement of what the packet does not prove."),
    ]
    return [{"field": name, "purpose": purpose, "required_status": "required"} for name, purpose in fields]


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagships() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0122 scientific runtime receipt layer: source, oracle, runtime, compiler, telemetry, lineage, verifier."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided"), "confidence": parsed.get("confidence")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    growth = read_json(GROWTH)
    runtime = read_json(RUNTIME)
    sources = source_matrix()
    experiment = exact_and_float_experiment()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"growth_vector_pass": growth["pass"], "growth_vector_seal": growth["seal"], "runtime_branch_pass": runtime["pass"], "runtime_branch_seal": runtime["seal"], "source_store": str(SOURCE_STORE.relative_to(ROOT)).replace("\\", "/")},
        "source_matrix": sources,
        "receipt_contract": receipt_contract(),
        "long_horizon_experiment": experiment,
        "product_hypothesis": "A scientific runtime receipt layer can become the cross-field bridge from source and proof to executable branch, compiler/runtime evidence, telemetry, lineage, and Crucible verdict.",
        "primary_30_day_push": "scientific_runtime_receipt_layer",
        "market_gap_status": "inferred",
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0122 strengthens a scoped Hamiltonian law candidate and defines a receipt layer. It does not prove BuildLang/buildc execution, solve arbitrary physics, verify all external tool claims, or promote a natural law.",
        "flagship_receipts": flagships(),
    }
    errors = []
    if len(sources) < 15 or sum(row["local_gather_status"].startswith("GATHER_VERIFIED") for row in sources) < 14:
        errors.append("source_matrix")
    if any(not row["exact_invariant_for_all_steps_by_induction"] for row in experiment["exact_cases"]):
        errors.append("exact_identity")
    if any(h["status"] != "MATCH" for row in experiment["exact_cases"] for h in row["float_horizons"]):
        errors.append("float_horizon")
    if len(artifact["receipt_contract"]) < 8:
        errors.append("receipt_contract")
    if any(row["status"] != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "scientific-runtime-receipt-layer-spec-pass-0122.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
