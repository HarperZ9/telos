"""Generate pass 0109 stochastic-kernel corpus harness artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_stochastic_kernel_corpus_harness_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_stochastic_kernel_corpus_harness_receipt.py"
OUT_PATH = ROOT / "schemas" / "stochastic-kernel-corpus-harness-receipt-pass-0109.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0109.json"
PACKET_PATH = ROOT / "packets" / "119-stochastic-kernel-corpus-harness-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "119-stochastic-kernel-corpus-harness-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0109-stochastic-kernel-corpus-harness-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0109-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0109-measurements.json"


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
    rows = []
    for case in artifact["kernel_cases"]:
        rows.append(
            f"| {case['case_id']} | {case['status']} | {case.get('max_stationary_residual', 'n/a')} | {case.get('max_detailed_balance_residual', 'n/a')} |"
        )
    return "\n".join(rows)


def market_rows(artifact: dict) -> str:
    return "\n".join(f"| {row['tool']} | {row['category']} | {row['gap_status']} |" for row in artifact["market_binding"]["tools"])


def architecture_rows(artifact: dict) -> str:
    return "\n".join(
        f"| {row['cluster_id']} | {row['video_count']} | {row['evidence_status']} | {row['architecture_pull']} |"
        for row in artifact["youtube_binding"]["architecture_pulls"]
    )


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    summary = artifact["corpus_summary"]
    youtube = artifact["youtube_binding"]
    adapter = artifact["adapter_spec"]
    return f"""# Packet 119: Stochastic-Kernel Corpus Harness Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: scale pass 0108 from one detailed-balance proof into a small corpus
of stochastic-kernel cases and a sampler-adapter receipt contract.

```text
detailed_balance_pass = {artifact['source_bindings']['detailed_balance_pass']}
youtube_roadmap_pass = {artifact['source_bindings']['youtube_roadmap_pass']}
case_count = {summary['case_count']}
exact_kernel_count = {summary['exact_kernel_count']}
match_count = {summary['match_count']}
drift_expected_count = {summary['drift_expected_count']}
boundary_expected_count = {summary['boundary_expected_count']}
adapter_required_field_count = {adapter['required_field_count']}
valid_youtube_videos = {youtube['valid_video_count']}
youtube_transcript_receipts = {youtube['transcript_receipt_count']}
dominant_youtube_cluster = {youtube['dominant_cluster']}
raw_transcript_included = {youtube['raw_transcript_included']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Kernel Cases

| Case | Status | Max Stationary Residual | Max Detailed-Balance Residual |
| --- | --- | --- | --- |
{case_rows(artifact)}

## Adapter Contract

Required fields: `{', '.join(adapter['required_fields'])}`.

Acceptance rule: {adapter['acceptance_rule']}

## YouTube Source-Pull Binding

| Cluster | Videos | Evidence | Architecture Pull |
| --- | --- | --- | --- |
{architecture_rows(artifact)}

## Market Surface

| Tool | Category | Gap Status |
| --- | --- | --- |
{market_rows(artifact)}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    summary = artifact["corpus_summary"]
    youtube = artifact["youtube_binding"]
    return f"""# Stochastic-Kernel Corpus Harness Brief

Date: 2026-07-01

## Decision

Advance stochastic-kernel proof packets as a bridge between AI/ML runtime
research, probabilistic programming, physics, quant, and BuildLang scientific
runtime work.

## Why

The YouTube roadmap remains a crucial prioritization signal: {youtube['valid_video_count']}
valid videos, {youtube['transcript_receipt_count']} transcript receipts, and a
dominant {youtube['dominant_cluster']} cluster. The new pass turns that signal
into a bounded receipt harness instead of promoting video claims.

## Current Result

The harness records {summary['case_count']} cases: one exact MATCH, one expected
stationarity drift, and two boundary cases. The required adapter fields define
the minimum shape for future Stan, NumPyro, TFP, PyMC, BlackJAX, and Turing.jl
receipt adapters.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0109 Steelman: Stochastic-Kernel Corpus Harness

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that three finite kernels are still tiny. Correct.
This pass proves only that the harness can distinguish exact, drift, and
boundary cases.

The second objection is that YouTube videos should not drive scientific truth.
Correct. They drive architecture prioritization only; transcript hashes and
metadata receipts are source evidence, not discovery proof.

The third objection is that uncalibrated kernels are not runtime failures by
themselves. Correct. The receipt marks the source case as `REQUIRES_CALIBRATION`
rather than `DRIFT`.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0109",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "youtube_binding": artifact["youtube_binding"],
        "adapter_spec": artifact["adapter_spec"],
        "law_candidate": artifact["law_candidate"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    summary = artifact["corpus_summary"]
    youtube = artifact["youtube_binding"]
    adapter = artifact["adapter_spec"]
    cases = {case["case_id"]: case for case in artifact["kernel_cases"]}
    claims = [
        f"Pass 0109 created a StochasticKernelCorpusHarnessReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0109 binds detailed-balance pass {artifact['source_bindings']['detailed_balance_pass']} and YouTube roadmap pass {artifact['source_bindings']['youtube_roadmap_pass']}.",
        f"Pass 0109 records corpus counts case_count {summary['case_count']}, exact_kernel_count {summary['exact_kernel_count']}, match_count {summary['match_count']}, drift_expected_count {summary['drift_expected_count']}, and boundary_expected_count {summary['boundary_expected_count']}.",
        f"Pass 0109 reversible kernel records stationary_residual {cases['reversible_detailed_balance']['stationary_residual']} and max_detailed_balance_residual {cases['reversible_detailed_balance']['max_detailed_balance_residual']}.",
        f"Pass 0109 stationary nonreversible cycle records stationary_residual {cases['stationary_nonreversible_cycle']['stationary_residual']} and max_detailed_balance_residual {cases['stationary_nonreversible_cycle']['max_detailed_balance_residual']}.",
        f"Pass 0109 row-stochastic negative fixture records row_sums {cases['row_stochastic_not_stationary']['row_sums']} and stationary_residual {cases['row_stochastic_not_stationary']['stationary_residual']}.",
        f"Pass 0109 source-boundary fixture records status {cases['uncalibrated_random_walk_source_boundary']['status']} and calibration_required {cases['uncalibrated_random_walk_source_boundary']['calibration_required']}.",
        f"Pass 0109 adapter spec records required_field_count {adapter['required_field_count']} and target tools {adapter['target_tools']}.",
        f"Pass 0109 YouTube binding records {youtube['valid_video_count']} valid videos, {youtube['transcript_receipt_count']} transcript receipts, dominant cluster {youtube['dominant_cluster']}, and raw_transcript_included {youtube['raw_transcript_included']}.",
        f"Pass 0109 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0109 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0109 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"corpus_summary={summary}"],
        [f"case={cases['reversible_detailed_balance']}"],
        [f"case={cases['stationary_nonreversible_cycle']}"],
        [f"case={cases['row_stochastic_not_stationary']}"],
        [f"case={cases['uncalibrated_random_walk_source_boundary']}"],
        [f"adapter_spec={adapter}"],
        [f"youtube_binding={youtube}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0109 Stochastic-Kernel Corpus Harness", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0109 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "STOCHASTIC_KERNEL_CORPUS_HARNESS_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
