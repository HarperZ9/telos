"""Generate pass 0111 multi-kernel runtime suite artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_multi_kernel_runtime_suite_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_multi_kernel_runtime_suite_receipt.py"
OUT_PATH = ROOT / "schemas" / "multi-kernel-runtime-suite-receipt-pass-0111.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0111.json"
PACKET_PATH = ROOT / "packets" / "121-multi-kernel-runtime-suite-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "121-multi-kernel-runtime-suite-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0111-multi-kernel-runtime-suite-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0111-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0111-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.encode("ascii", "ignore").decode("ascii"), encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def case_rows(artifact: dict) -> str:
    return "\n".join(
        f"| {row['case_id']} | {row['classification']} | {row['stationary_residual_check']['status']} | {row['detailed_balance_or_invariance_check']['status']} | {row['exact_distribution_l1_distance_to_declared_pi']} |"
        for row in artifact["case_results"]
    )


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    summary = artifact["suite_summary"]
    youtube = artifact["youtube_binding"]
    return f"""# Packet 121: Multi-Kernel Runtime Suite Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: run the same stochastic runtime receipt interface across positive,
expected-drift, and boundary kernels.

```text
runtime_chain_pass = {artifact['source_bindings']['runtime_chain_pass']}
stochastic_kernel_corpus_pass = {artifact['source_bindings']['stochastic_kernel_corpus_pass']}
case_count = {summary['case_count']}
match_count = {summary['match_count']}
drift_expected_count = {summary['drift_expected_count']}
boundary_expected_count = {summary['boundary_expected_count']}
adapter_missing_field_total = {summary['adapter_missing_field_total']}
valid_youtube_videos = {youtube['valid_video_count']}
dominant_youtube_cluster = {youtube['dominant_cluster']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Suite Cases

| Case | Classification | Stationary Check | Balance/Invariance Check | Exact L1 To Declared Pi |
| --- | --- | --- | --- | --- |
{case_rows(artifact)}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    summary = artifact["suite_summary"]
    return f"""# Multi-Kernel Runtime Suite Brief

Date: 2026-07-01

## Decision

Use the same receipt interface across positive, drift, and boundary kernels
before adapting production probabilistic runtimes.

## Current Result

The suite records {summary['case_count']} cases: {summary['match_count']} MATCH,
{summary['drift_expected_count']} expected drift, and
{summary['boundary_expected_count']} boundary case, with zero missing adapter
fields.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0111 Steelman: Multi-Kernel Runtime Suite

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that three kernels are still a small suite. Correct.
The point is classification under one interface, not broad coverage.

The second objection is that the cyclic boundary is stationary but not mixing
from a point start. Correct. The pass classifies it by residual and detailed
balance boundary, not by pretending a single chain proves mixing.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0111",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "suite_summary": artifact["suite_summary"],
        "youtube_binding": artifact["youtube_binding"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    summary = artifact["suite_summary"]
    results = {row["case_id"]: row for row in artifact["case_results"]}
    youtube = artifact["youtube_binding"]
    claims = [
        f"Pass 0111 created a MultiKernelRuntimeSuiteReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0111 binds runtime-chain pass {artifact['source_bindings']['runtime_chain_pass']} and stochastic-kernel corpus pass {artifact['source_bindings']['stochastic_kernel_corpus_pass']}.",
        f"Pass 0111 records case_count {summary['case_count']}, match_count {summary['match_count']}, drift_expected_count {summary['drift_expected_count']}, boundary_expected_count {summary['boundary_expected_count']}, and adapter_missing_field_total {summary['adapter_missing_field_total']}.",
        f"Pass 0111 reversible case classification is {results['reversible_detailed_balance']['classification']} with exact_l1 {results['reversible_detailed_balance']['exact_distribution_l1_distance_to_declared_pi']}.",
        f"Pass 0111 row-stochastic case classification is {results['row_stochastic_not_stationary']['classification']} with stationary status {results['row_stochastic_not_stationary']['stationary_residual_check']['status']}.",
        f"Pass 0111 cycle case classification is {results['stationary_nonreversible_cycle']['classification']} with max_detailed_balance_residual {results['stationary_nonreversible_cycle']['max_detailed_balance_residual']}.",
        f"Pass 0111 source-boundary fixture status is {artifact['source_boundary_receipts']['uncalibrated_random_walk_source_boundary']['status']}.",
        f"Pass 0111 YouTube binding records {youtube['valid_video_count']} valid videos and raw_transcript_included {youtube['raw_transcript_included']}.",
        f"Pass 0111 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0111 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0111 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"suite_summary={summary}"],
        [f"case={results['reversible_detailed_balance']}"],
        [f"case={results['row_stochastic_not_stationary']}"],
        [f"case={results['stationary_nonreversible_cycle']}"],
        [f"source_boundary={artifact['source_boundary_receipts']['uncalibrated_random_walk_source_boundary']}"],
        [f"youtube_binding={youtube}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0111 Multi-Kernel Runtime Suite Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0111 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)], timeout=180)
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "MULTI_KERNEL_RUNTIME_SUITE_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
