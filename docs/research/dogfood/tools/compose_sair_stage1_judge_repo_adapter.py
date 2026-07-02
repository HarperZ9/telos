"""Compose pass 0138 SAIR Stage 1 public judge repository adapter."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

SCHEMA = "SAIRStage1JudgeRepoAdapterReceipt/v1"
PASS_ID = "0138"
STATUS_MATCH = "SAIR_STAGE1_JUDGE_REPO_ADAPTER_MATCH"
STATUS_DRIFT = "SAIR_STAGE1_JUDGE_REPO_ADAPTER_DRIFT"
REPO_URL = "https://github.com/SAIRcompetition/equational-theories-stage1-judge.git"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "schemas" / "sair-stage1-judge-repo-adapter-pass-0138.json"
CHECKOUT = Path(tempfile.gettempdir()) / "telos-pass-0138-stage1-judge-fe00cf9e"

OBSERVED_FILES = [
    "README.md",
    "pyproject.toml",
    "evaluation_models.json",
    "examples/run_smoke.py",
    "examples/example_complete_prompt.txt",
    "examples/problems_hard3_20.jsonl",
    "judge.py",
    "llm.py",
    "models.py",
    "prompt.py",
    "tests/test_judge.py",
    "tests/test_llm.py",
    "tests/test_models.py",
    "tests/test_prompt.py",
    "tests/test_run_smoke.py",
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


def run_command(command: list[str], cwd: Path, timeout: int = 120, scrub_key: bool = False) -> dict[str, Any]:
    env = os.environ.copy()
    if scrub_key:
        env.pop("OPENROUTER_API_KEY", None)
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=env,
    )
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
    clone = run_command(["git", "clone", "--depth", "1", "--filter=blob:none", REPO_URL, str(CHECKOUT)], CHECKOUT.parent, timeout=180)
    head = run_command(["git", "rev-parse", "HEAD"], CHECKOUT)
    return {"path": str(CHECKOUT), "head": head["combined_excerpt"].strip(), "reused": False, "clone": clone}


def source_hashes() -> dict[str, str]:
    return {name: sha256_file(CHECKOUT / name) for name in OBSERVED_FILES if (CHECKOUT / name).exists()}


def model_summary() -> dict[str, Any]:
    data = json.loads((CHECKOUT / "evaluation_models.json").read_text(encoding="utf-8"))
    models = data["models"]
    return {
        "allow_fallbacks": data["defaults"]["allow_fallbacks"],
        "max_output_tokens_cap": data["defaults"]["max_output_tokens_cap"],
        "model_aliases": sorted(models),
        "model_count": len(models),
        "routes": [
            {
                "alias": alias,
                "model": entry["model"],
                "provider": entry["provider"],
                "temperature": entry["temperature"],
                "max_output_tokens": entry["max_output_tokens"],
                "seed": entry.get("seed"),
            }
            for alias, entry in sorted(models.items())
        ],
    }


def command_receipts() -> dict[str, Any]:
    pytest = run_command(["python", "-m", "pytest", "tests"], CHECKOUT, timeout=180)
    prompt = run_command(
        [
            "python",
            "prompt.py",
            "Does {{equation1}} imply {{equation2}}? Reply VERDICT: TRUE or FALSE.",
            "x=x",
            "x=x",
        ],
        CHECKOUT,
    )
    judge = run_command(["python", "judge.py", "VERDICT: TRUE", "--expected", "true", "--json"], CHECKOUT)
    missing_key = run_command(
        ["python", "examples/run_smoke.py", "--limit", "1", "--models", "gpt-oss-120b", "--hide-response"],
        CHECKOUT,
        scrub_key=True,
    )
    return {
        "pytest": {**pytest, "status": "MATCH" if pytest["exit_code"] == 0 else "DRIFT"},
        "prompt_cli": {**prompt, "status": "MATCH" if prompt["exit_code"] == 0 and "Does x=x imply x=x?" in prompt["combined_excerpt"] else "DRIFT"},
        "judge_cli": {**judge, "status": "MATCH" if judge["exit_code"] == 0 and '"correct": true' in judge["combined_excerpt"] else "DRIFT"},
        "missing_key_boundary": {
            **missing_key,
            "status": "MATCH" if missing_key["exit_code"] != 0 and "Missing API key" in missing_key["combined_excerpt"] else "DRIFT",
            "external_model_call_performed": False,
        },
    }


def validate_adapter(packet: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    if packet["repository"]["head_commit"] != packet["repository"]["ls_remote_head"]:
        failures.append("head_commit_mismatch")
    if len(packet["repository"]["source_hashes"]) < len(OBSERVED_FILES):
        failures.append("missing_observed_source_hashes")
    if packet["model_config_summary"]["model_count"] != 3:
        failures.append("unexpected_model_count")
    if packet["model_config_summary"]["allow_fallbacks"] is not False:
        failures.append("fallbacks_not_disabled")
    if packet["model_config_summary"]["max_output_tokens_cap"] != 8192:
        failures.append("unexpected_token_cap")
    if any(row["status"] != "MATCH" for row in packet["local_command_receipts"].values()):
        failures.append("local_command_receipt_drift")
    if packet["execution_boundary"]["external_model_calls"] != 0:
        failures.append("external_model_call_present")
    if packet["current_promoted_results"]:
        failures.append("promoted_result_present")
    return {"status": "MATCH" if not failures else "REJECTED", "failures": failures}


def negative_fixtures(packet: dict[str, Any]) -> list[dict[str, Any]]:
    cases = []
    mutations = [
        ("head_commit_mismatch", lambda p: p["repository"].update({"head_commit": "0" * 40})),
        ("missing_source_hashes", lambda p: p["repository"].update({"source_hashes": {}})),
        ("fallbacks_enabled", lambda p: p["model_config_summary"].update({"allow_fallbacks": True})),
        ("hidden_external_model_call", lambda p: p["execution_boundary"].update({"external_model_calls": 1})),
        ("missing_key_boundary_ignored", lambda p: p["local_command_receipts"]["missing_key_boundary"].update({"status": "DRIFT"})),
        ("leaderboard_claim_promoted", lambda p: p.update({"current_promoted_results": ["leaderboard_claim"]})),
    ]
    for fixture_id, mutate in mutations:
        clone = json.loads(json.dumps(packet))
        mutate(clone)
        observed = validate_adapter(clone)
        cases.append({
            "fixture_id": fixture_id,
            "observed_status": observed["status"],
            "failures": observed["failures"],
            "status": "MATCH" if observed["status"] == "REJECTED" and observed["failures"] else "DRIFT",
        })
    return cases


def compose() -> dict[str, Any]:
    checkout = ensure_checkout()
    ls_remote = run_command(["git", "ls-remote", REPO_URL, "HEAD"], CHECKOUT.parent, timeout=60)
    head = checkout["head"].splitlines()[0].strip()
    packet: dict[str, Any] = {
        "packet_id": "sair-stage1-judge-repo-adapter-pass-0138",
        "source_refs": [
            "https://github.com/SAIRcompetition/equational-theories-stage1-judge",
            "https://competition.sair.foundation/competitions/mathematics-distillation-challenge-equational-theories-stage1/overview",
            "https://sair.foundation/",
            "docs/research/dogfood/schemas/sair-stage1-competition-proof-packet-pass-0137.json",
        ],
        "repository": {
            "url": REPO_URL,
            "head_commit": head,
            "ls_remote_head": ls_remote["combined_excerpt"].split()[0],
            "checkout_kind": "temp_external_readonly_checkout",
            "observed_files": OBSERVED_FILES,
            "source_hashes": source_hashes(),
        },
        "model_config_summary": model_summary(),
        "adapter_contract": {
            "inputs": ["complete_prompt_template", "problem_jsonl", "evaluation_models_json", "model_aliases", "OPENROUTER_API_KEY"],
            "local_no_secret_steps": ["prompt_rendering", "verdict_extraction", "model_config_loading", "pytest_suite"],
            "external_call_step": "OpenRouter call in examples/run_smoke.py; blocked without explicit action receipt and redacted provider receipt",
            "outputs": ["per_problem_json_line", "summary_total_calls_parseable_correct"],
        },
        "local_command_receipts": command_receipts(),
        "execution_boundary": {
            "openrouter_api_key_captured": False,
            "external_model_calls": 0,
            "official_leaderboard_submission": False,
            "raw_model_response_exported": False,
        },
        "current_promoted_results": [],
        "promotion_boundary": "This pass verifies the public judge repository command surface and local no-secret gates. It does not claim official SAIR evaluation, model accuracy, leaderboard standing, theorem proof, market fit, or a promoted natural law.",
    }
    positive = validate_adapter(packet)
    negatives = negative_fixtures(packet)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-02",
        "checkout": checkout,
        "competition_packet": packet,
        "positive_validation": positive,
        "negative_fixtures": negatives,
        "tooling_gap": "Forum needs a route for formal_math_competition_repo_adapter so source-lead, fixture, public judge repo, hosted-model receipt, and Lean certificate stages are distinguishable.",
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
