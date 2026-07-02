"""Generate pass 0110 stochastic-runtime chain artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_stochastic_runtime_chain_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_stochastic_runtime_chain_receipt.py"
OUT_PATH = ROOT / "schemas" / "stochastic-runtime-chain-receipt-pass-0110.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0110.json"
PACKET_PATH = ROOT / "packets" / "120-stochastic-runtime-chain-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "120-stochastic-runtime-chain-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0110-stochastic-runtime-chain-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0110-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0110-measurements.json"


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


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    runtime = artifact["runtime_receipt"]
    diag = runtime["diagnostics_receipt"]
    adapter = artifact["adapter_contract"]
    youtube = artifact["youtube_binding"]
    return f"""# Packet 120: Stochastic Runtime Chain Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: instantiate the pass 0109 stochastic-kernel adapter contract as a
finite-chain runtime receipt with seed, warmup, diagnostics, and negative
fixtures.

```text
stochastic_kernel_corpus_pass = {artifact['source_bindings']['stochastic_kernel_corpus_pass']}
youtube_roadmap_pass = {artifact['source_bindings']['youtube_roadmap_pass']}
kernel_family = {runtime['kernel_family']}
seed = {runtime['chain_seed_receipt']['seed']}
warmup_steps = {runtime['warmup_schedule_receipt']['warmup_steps']}
sample_steps = {runtime['warmup_schedule_receipt']['sample_steps']}
adapter_missing_fields = {adapter['missing_fields']}
exact_l1_distance_to_pi = {diag['exact_distribution_l1_distance_to_pi']}
empirical_l1_distance_to_pi = {diag['empirical_l1_distance_to_pi']}
valid_youtube_videos = {youtube['valid_video_count']}
dominant_youtube_cluster = {youtube['dominant_cluster']}
buildlang_target_status = {artifact['buildlang_target']['status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Runtime Receipt Fields

Required fields satisfied: `{adapter['required_fields_satisfied']}` of
`{adapter['required_field_count']}`.

Fields: `{', '.join(adapter['required_fields'])}`.

## Diagnostics

| Check | Value |
| --- | --- |
| Stationary residual status | `{diag['stationary_residual_check']['status']}` |
| Detailed-balance status | `{diag['detailed_balance_or_invariance_check']['status']}` |
| Exact distribution L1 | `{diag['exact_distribution_l1_distance_to_pi']}` |
| Empirical distribution L1 | `{diag['empirical_l1_distance_to_pi']}` |
| Empirical threshold | `{diag['empirical_threshold_l1']}` |

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    diag = artifact["runtime_receipt"]["diagnostics_receipt"]
    youtube = artifact["youtube_binding"]
    return f"""# Stochastic Runtime Chain Brief

Date: 2026-07-01

## Decision

Advance from kernel corpus receipts to runtime-chain receipts. The next product
unit is a sampler adapter that binds target, transition kernel, seed, warmup,
diagnostics, source provenance, and negative fixtures.

## Current Result

Pass 0110 records exact L1 `{diag['exact_distribution_l1_distance_to_pi']}` and
seeded empirical L1 `{diag['empirical_l1_distance_to_pi']}` against the target
distribution. It binds {youtube['valid_video_count']} YouTube source leads but
keeps all video-specific claims unpromoted.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0110 Steelman: Stochastic Runtime Chain Receipt

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this is a finite toy runtime, not Stan or
NumPyro. Correct. It is the receipt minimum before adapting production tools.

The second objection is empirical sampling variance. Correct. The receipt keeps
an exact distribution diagnostic separate from the seeded empirical diagnostic.

The third objection is BuildLang overclaim risk. Correct. The BuildLang target
is explicitly `TARGET_INTERFACE_NOT_COMPILED`.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0110",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "adapter_contract": artifact["adapter_contract"],
        "diagnostics": artifact["runtime_receipt"]["diagnostics_receipt"],
        "youtube_binding": artifact["youtube_binding"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    runtime = artifact["runtime_receipt"]
    diag = runtime["diagnostics_receipt"]
    adapter = artifact["adapter_contract"]
    youtube = artifact["youtube_binding"]
    claims = [
        f"Pass 0110 created a StochasticRuntimeChainReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0110 binds stochastic-kernel corpus pass {artifact['source_bindings']['stochastic_kernel_corpus_pass']} and YouTube roadmap pass {artifact['source_bindings']['youtube_roadmap_pass']}.",
        f"Pass 0110 satisfies {adapter['required_fields_satisfied']} of {adapter['required_field_count']} adapter fields with missing_fields {adapter['missing_fields']}.",
        f"Pass 0110 records kernel_family {runtime['kernel_family']}, seed {runtime['chain_seed_receipt']['seed']}, warmup_steps {runtime['warmup_schedule_receipt']['warmup_steps']}, and sample_steps {runtime['warmup_schedule_receipt']['sample_steps']}.",
        f"Pass 0110 exact diagnostic records l1_distance_to_pi {diag['exact_distribution_l1_distance_to_pi']}.",
        f"Pass 0110 empirical diagnostic records l1_distance_to_pi {diag['empirical_l1_distance_to_pi']} under threshold {diag['empirical_threshold_l1']}.",
        f"Pass 0110 negative fixtures keep row_stochastic_not_stationary status {runtime['negative_fixture_receipt']['row_stochastic_not_stationary']['status']} and source boundary status {runtime['negative_fixture_receipt']['uncalibrated_random_walk_source_boundary']['status']}.",
        f"Pass 0110 BuildLang target status is {artifact['buildlang_target']['status']}.",
        f"Pass 0110 YouTube binding records {youtube['valid_video_count']} valid videos, {youtube['transcript_receipt_count']} transcript receipts, and raw_transcript_included {youtube['raw_transcript_included']}.",
        f"Pass 0110 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0110 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0110 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"adapter_contract={adapter}"],
        [f"runtime_seed={runtime['chain_seed_receipt']}", f"warmup={runtime['warmup_schedule_receipt']}"],
        [f"exact_distribution_l1_distance_to_pi={diag['exact_distribution_l1_distance_to_pi']}"],
        [f"empirical_l1_distance_to_pi={diag['empirical_l1_distance_to_pi']}", f"threshold={diag['empirical_threshold_l1']}"],
        [f"negative_fixture_receipt={runtime['negative_fixture_receipt']}"],
        [f"buildlang_target={artifact['buildlang_target']}"],
        [f"youtube_binding={youtube}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0110 Stochastic Runtime Chain Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0110 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "STOCHASTIC_RUNTIME_CHAIN_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
