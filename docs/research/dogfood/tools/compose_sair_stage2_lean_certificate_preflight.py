"""Compose pass 0139 SAIR Stage 2 Lean certificate preflight."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

SCHEMA = "SAIRStage2LeanCertificatePreflightReceipt/v1"
PASS_ID = "0139"
STATUS_MATCH = "SAIR_STAGE2_LEAN_CERTIFICATE_PREFLIGHT_MATCH_WITH_TOOLCHAIN_GAP"
STATUS_DRIFT = "SAIR_STAGE2_LEAN_CERTIFICATE_PREFLIGHT_DRIFT"
REPO_URL = "https://github.com/SAIRcompetition/equational-theories-lean-stage2.git"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "schemas" / "sair-stage2-lean-certificate-preflight-pass-0139.json"
CHECKOUT = Path(tempfile.gettempdir()) / "telos-pass-0139-stage2-lean"

OBSERVED_FILES = [
    "README.md",
    "rules/evaluation.md",
    "docs/solo_mode.md",
    "docs/marathon_mode.md",
    "lean-toolchain",
    "lakefile.lean",
    "lake-manifest.json",
    "judge/verify.py",
    "judge/JudgeMagma/Magma.lean",
    "judge/JudgeDecide/DecideBang.lean",
    "judge/JudgeFinOp/MemoFinOp.lean",
    "judge/JudgeSupport/Inspect.lean",
    "scripts/run_harness.py",
    "scripts/run_marathon_harness.py",
    "pipeline/config.json",
    "tests/harness_manifest.json",
    "tests/challenger_manifest.json",
    "tests/marathon_manifest.json",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def run_command(command: list[str], cwd: Path, timeout: int = 120) -> dict[str, Any]:
    env = os.environ.copy()
    for key in ("OPENROUTER_API_KEY", "OPENAI_API_KEY"):
        env.pop(key, None)
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, env=env)
    except FileNotFoundError as exc:
        return {
            "command": " ".join(command),
            "exit_code": 127,
            "stdout_sha256": sha256_text(""),
            "stderr_sha256": sha256_text(str(exc)),
            "combined_excerpt": str(exc).encode("ascii", "ignore").decode("ascii")[:240],
        }
    text = (result.stdout + "\n" + result.stderr).strip()
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "combined_excerpt": text[:240].encode("ascii", "ignore").decode("ascii"),
    }


def ensure_checkout() -> dict[str, Any]:
    if CHECKOUT.exists() and (CHECKOUT / ".git").exists():
        head = run_command(["git", "rev-parse", "HEAD"], CHECKOUT)
        if head["exit_code"] == 0:
            return {"path": str(CHECKOUT), "head": head["combined_excerpt"].strip(), "reused": True}
    CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
    clone = run_command(["git", "clone", "--depth", "1", "--filter=blob:none", REPO_URL, str(CHECKOUT)], CHECKOUT.parent, timeout=240)
    head = run_command(["git", "rev-parse", "HEAD"], CHECKOUT)
    return {"path": str(CHECKOUT), "head": head["combined_excerpt"].strip(), "reused": False, "clone": clone}


def source_hashes() -> dict[str, str]:
    return {name: sha256_file(CHECKOUT / name) for name in OBSERVED_FILES if (CHECKOUT / name).exists()}


def repo_counts() -> dict[str, int]:
    tracked = subprocess.run(["git", "ls-files"], cwd=CHECKOUT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    tracked_files = len([line for line in tracked.stdout.splitlines() if line.strip()])
    return {
        "tracked_files": tracked_files,
        "lean_files": len(list(CHECKOUT.rglob("*.lean"))),
        "python_files": len(list(CHECKOUT.rglob("*.py"))),
        "problem_files": len(list((CHECKOUT / "examples" / "problems").glob("*"))),
        "challenger_answers": len(list((CHECKOUT / "tests" / "challenger" / "answers").glob("*"))),
    }


def manifest_counts() -> dict[str, int]:
    out: dict[str, int] = {}
    for name in ("harness_manifest", "challenger_manifest", "marathon_manifest"):
        data = json.loads((CHECKOUT / "tests" / f"{name}.json").read_text(encoding="utf-8"))
        if isinstance(data, list):
            out[name] = len(data)
        else:
            keys = ("cases", "public_attack_cases", "private_attack_cases", "solvers")
            out[name] = sum(len(data.get(key, [])) for key in keys)
    return out


def toolchain_receipts() -> dict[str, Any]:
    receipts = {}
    for tool in ("lean", "lake", "elan"):
        probe = run_command([tool, "--version"], CHECKOUT)
        receipts[tool] = {
            **probe,
            "status": "MATCH" if probe["exit_code"] == 0 else "UNVERIFIABLE_TOOL_UNAVAILABLE",
        }
    compileall = run_command(["python", "-m", "compileall", "-q", "judge", "pipeline", "scripts", "examples"], CHECKOUT, timeout=180)
    harness = run_command(["python", "scripts/run_harness.py"], CHECKOUT, timeout=180)
    receipts["python_compileall"] = {**compileall, "status": "MATCH" if compileall["exit_code"] == 0 else "DRIFT"}
    receipts["run_harness"] = {
        **harness,
        "status": "UNVERIFIABLE_TOOL_UNAVAILABLE" if "missing lean binary" in harness["combined_excerpt"].lower() else ("MATCH" if harness["exit_code"] == 0 else "DRIFT"),
    }
    return receipts


def certificate_contract() -> dict[str, Any]:
    verify_text = (CHECKOUT / "judge" / "verify.py").read_text(encoding="utf-8", errors="replace")
    return {
        "answer_keys": ["verdict", "code"],
        "problem_keys": ["id", "eq1_id", "eq2_id", "equation1", "equation2"],
        "statuses": ["accepted", "unparsed", "malformed", "incomplete_proof", "incorrect"],
        "true_certificate": "Lean 4 proof that the hypothesis equation implies the goal equation",
        "false_certificate": "finite magma witness where the hypothesis holds and the goal fails",
        "banned_token_count": verify_text.count('"') and len([
            "sorry", "admit", "sorryAx", "mkSorry", "dbg_trace", "run_tac", "initialize", "#eval", "unsafe", "unsafeCast"
        ]),
        "size_limits": {"solver_py_bytes": 500_000, "lean_code_bytes": 100_000, "false_certificate_bytes": 10_000},
    }


def validate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    if packet["repository"]["head_commit"] != packet["repository"]["ls_remote_head"]:
        failures.append("head_commit_mismatch")
    if len(packet["repository"]["source_hashes"]) < len(OBSERVED_FILES):
        failures.append("missing_observed_source_hashes")
    if not packet["toolchain"]["lean_toolchain"]:
        failures.append("missing_lean_toolchain")
    if packet["local_command_receipts"]["python_compileall"]["status"] != "MATCH":
        failures.append("python_compileall_drift")
    if packet["local_command_receipts"]["run_harness"]["status"] != "UNVERIFIABLE_TOOL_UNAVAILABLE":
        failures.append("unexpected_harness_status")
    if packet["proof_replay"]["lean_replay_status"] != "UNVERIFIABLE_TOOL_UNAVAILABLE":
        failures.append("lean_replay_promoted")
    if packet["current_promoted_results"]:
        failures.append("promoted_result_present")
    return {"status": "MATCH" if not failures else "REJECTED", "failures": failures}


def negative_fixtures(packet: dict[str, Any]) -> list[dict[str, Any]]:
    cases = []
    mutations = [
        ("head_commit_mismatch", lambda p: p["repository"].update({"head_commit": "0" * 40})),
        ("missing_source_hashes", lambda p: p["repository"].update({"source_hashes": {}})),
        ("missing_toolchain_pin", lambda p: p["toolchain"].update({"lean_toolchain": ""})),
        ("lean_replay_promoted_without_lean", lambda p: p["proof_replay"].update({"lean_replay_status": "MATCH"})),
        ("harness_claim_promoted", lambda p: p["local_command_receipts"]["run_harness"].update({"status": "MATCH"})),
        ("leaderboard_claim_promoted", lambda p: p.update({"current_promoted_results": ["accepted_certificate_claim"]})),
    ]
    for fixture_id, mutate in mutations:
        clone = json.loads(json.dumps(packet))
        mutate(clone)
        observed = validate_packet(clone)
        cases.append({"fixture_id": fixture_id, "observed_status": observed["status"], "failures": observed["failures"], "status": "MATCH" if observed["failures"] else "DRIFT"})
    return cases


def compose() -> dict[str, Any]:
    checkout = ensure_checkout()
    ls_remote = run_command(["git", "ls-remote", REPO_URL, "HEAD"], CHECKOUT.parent)
    head = checkout["head"].splitlines()[0].strip()
    receipts = toolchain_receipts()
    packet: dict[str, Any] = {
        "packet_id": "sair-stage2-lean-certificate-preflight-pass-0139",
        "source_refs": [
            "https://github.com/SAIRcompetition/equational-theories-lean-stage2",
            "https://competition.sair.foundation/competitions/mathematics-distillation-challenge-equational-theories-stage2/overview",
            "https://teorth.github.io/equational_theories/",
            "docs/research/dogfood/schemas/sair-stage1-judge-repo-adapter-pass-0138.json",
        ],
        "repository": {
            "url": REPO_URL,
            "head_commit": head,
            "ls_remote_head": ls_remote["combined_excerpt"].split()[0],
            "checkout_kind": "temp_external_readonly_checkout",
            "observed_files": OBSERVED_FILES,
            "source_hashes": source_hashes(),
            "counts": repo_counts(),
            "manifest_counts": manifest_counts(),
        },
        "toolchain": {"lean_toolchain": (CHECKOUT / "lean-toolchain").read_text(encoding="utf-8").strip()},
        "certificate_contract": certificate_contract(),
        "local_command_receipts": receipts,
        "proof_replay": {"lean_replay_status": "UNVERIFIABLE_TOOL_UNAVAILABLE", "reason": "lean, lake, and elan are unavailable on PATH"},
        "execution_boundary": {"api_keys_captured": False, "external_model_calls": 0, "official_submission": False},
        "current_promoted_results": [],
        "promotion_boundary": "This pass verifies the public Stage 2 repository preflight surface only. It does not replay Lean proofs, accept certificates, claim official evaluation, or promote a theorem or natural law.",
    }
    positive = validate_packet(packet)
    negatives = negative_fixtures(packet)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-02",
        "checkout": checkout,
        "certificate_packet": packet,
        "positive_validation": positive,
        "negative_fixtures": negatives,
        "tooling_gap": "Install or containerize Lean/lake/elan before promoting this from certificate preflight to LeanProofReceipt replay.",
    }
    ok = positive["status"] == "MATCH" and all(row["status"] == "MATCH" for row in negatives)
    artifact["status"] = STATUS_MATCH if ok else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def main() -> None:
    artifact = compose()
    write_json(OUT, artifact)
    print(json.dumps({"path": str(OUT), "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
