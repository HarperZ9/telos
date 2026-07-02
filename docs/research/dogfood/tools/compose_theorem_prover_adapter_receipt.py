"""Compose pass 0117 theorem-prover adapter receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "TheoremProverAdapterReceipt/v1"
PASS_ID = "0117"
STATUS_MATCH = "THEOREM_PROVER_ADAPTER_MATCH"
STATUS_DRIFT = "THEOREM_PROVER_ADAPTER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BRIDGE = ROOT / "schemas" / "formal-physics-source-lead-bridge-pass-0116.json"


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


def availability() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for exe in ["lean", "lake", "coqc", "isabelle", "agda"]:
        path = shutil.which(exe)
        result[exe] = {"executable": exe, "status": "AVAILABLE" if path else "MISSING", "path": path}
    return result


def compose_map(first: dict[str, str], second: dict[str, str]) -> dict[str, str]:
    return {key: second[value] for key, value in first.items()}


def finite_model() -> dict[str, Any]:
    ida = {"a0": "a0", "a1": "a1"}
    idb = {"b0": "b0", "b1": "b1"}
    f = {"a0": "b0", "a1": "b1"}
    g = {"b0": "c1", "b1": "c0"}
    h = {"c0": "d0", "c1": "d1"}
    return {"idA": ida, "idB": idb, "f": f, "g": g, "h": h}


def theorem_targets(model: dict[str, Any]) -> list[dict[str, Any]]:
    f, g, h = model["f"], model["g"], model["h"]
    id_a, id_b = model["idA"], model["idB"]
    associativity_left = compose_map(compose_map(f, g), h)
    associativity_right = compose_map(f, compose_map(g, h))
    rows = [
        ("left_identity", "idB_comp_f_eq_f", compose_map(f, id_b), f),
        ("right_identity", "f_comp_idA_eq_f", compose_map(id_a, f), f),
        ("associativity", "h_comp_g_comp_f_assoc", associativity_left, associativity_right),
    ]
    targets = []
    for target_id, proposition, observed, expected in rows:
        targets.append({
            "target_id": target_id,
            "proposition": proposition,
            "claim_status": "FINITE_MODEL_VERIFIED" if observed == expected else "DRIFT",
            "observed": observed,
            "expected": expected,
            "lean_style_target": f"theorem {proposition} : finite_model_check := by native_decide",
            "proof_object_status": "NOT_EXECUTED_PROVER_UNAVAILABLE",
        })
    return targets


def countermodel() -> dict[str, Any]:
    model = finite_model()
    bad_idb = {"b0": "b1", "b1": "b0"}
    observed = compose_map(model["f"], bad_idb)
    return {
        "status": "MATCH" if observed != model["f"] else "DRIFT",
        "classification": "BAD_IDENTITY_DRIFT",
        "bad_identity": bad_idb,
        "observed": observed,
        "expected": model["f"],
    }


def prover_branches(avail: dict[str, dict[str, Any]], targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    branches = [{
        "branch_id": "python_finite_model_replay",
        "status": "MATCH" if all(row["claim_status"] == "FINITE_MODEL_VERIFIED" for row in targets) else "DRIFT",
        "target_count": len(targets),
        "verifier": "python_finite_function_equality",
    }]
    for exe, branch_id in [("lean", "lean4_target"), ("coqc", "rocq_target"), ("isabelle", "isabelle_target"), ("agda", "agda_target")]:
        branches.append({
            "branch_id": branch_id,
            "executable": exe,
            "status": "AVAILABLE_NOT_EXECUTED" if avail[exe]["status"] == "AVAILABLE" else "UNAVAILABLE_FENCED",
            "target_count": len(targets),
        })
    return branches


def source_anchors() -> list[dict[str, str]]:
    return [
        {"tool": "Lean", "url": "https://lean-lang.org/doc/reference/latest/", "kind": "official_docs"},
        {"tool": "Lean TPIL", "url": "https://lean-lang.org/theorem_proving_in_lean4/", "kind": "official_docs"},
        {"tool": "Lean mathlib", "url": "https://leanprover-community.github.io/mathlib4_docs/", "kind": "official_docs"},
        {"tool": "Lean Lake", "url": "https://leanprover-community.github.io/install/project.html", "kind": "official_docs"},
        {"tool": "Rocq", "url": "https://rocq-prover.org/", "kind": "official_docs"},
        {"tool": "Isabelle", "url": "https://isabelle.in.tum.de/", "kind": "official_docs"},
        {"tool": "Agda", "url": "https://agda.readthedocs.io/en/latest/getting-started/what-is-agda.html", "kind": "official_docs"},
    ]


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0117: theorem-prover adapter receipt with Lean-style targets and unavailable prover fences."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def compose() -> dict[str, Any]:
    bridge = read_json(BRIDGE)
    model = finite_model()
    targets = theorem_targets(model)
    avail = availability()
    branches = prover_branches(avail, targets)
    anchors = source_anchors()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"formal_physics_bridge_pass": bridge["pass"], "category_case_id": "category_set_identity_associativity"},
        "availability": avail,
        "finite_model": model,
        "theorem_targets": targets,
        "countermodel": countermodel(),
        "prover_branches": branches,
        "source_surface": {"anchor_count": len(anchors), "anchors": anchors, "gap_status": "hypothesis"},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass verifies finite-model theorem targets only. It does not claim Lean, Rocq, Isabelle, or Agda execution when those tools are unavailable.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    errors = []
    if any(row["claim_status"] != "FINITE_MODEL_VERIFIED" for row in targets):
        errors.append("targets")
    if artifact["countermodel"]["status"] != "MATCH":
        errors.append("countermodel")
    if branch(branches, "python_finite_model_replay")["status"] != "MATCH":
        errors.append("python_replay")
    if artifact["source_surface"]["anchor_count"] < 6:
        errors.append("source_surface")
    if any(row.get("status") != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["measurements"] = [{"id": row["branch_id"], "status": row["status"]} for row in branches]
    artifact["measurements"].append({"id": "countermodel", "status": artifact["countermodel"]["status"]})
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def branch(branches: list[dict[str, Any]], branch_id: str) -> dict[str, Any]:
    return next(row for row in branches if row["branch_id"] == branch_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "theorem-prover-adapter-receipt-pass-0117.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
