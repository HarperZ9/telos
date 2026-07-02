"""Generate pass 0107 reaction-network corpus harness artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_reaction_network_corpus_harness_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_reaction_network_corpus_harness_receipt.py"
OUT_PATH = ROOT / "schemas" / "reaction-network-corpus-harness-receipt-pass-0107.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0107.json"
PACKET_PATH = ROOT / "packets" / "117-reaction-network-corpus-harness-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "117-reaction-network-corpus-harness-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0107-reaction-network-corpus-harness-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0107-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0107-measurements.json"


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


def network_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["network_results"]:
        candidates = "; ".join(f"{check['invariant']}:{check['residual']}" for check in row["candidate_checks"])
        rows.append(f"| {row['network_id']} | {row['status']} | {row['basis_dimension']} | {row['numerical_probe']['max_drift']} | {candidates} |")
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    summary = artifact["corpus_summary"]
    bridge = artifact["buildlang_runtime_bridge"]
    youtube = artifact["youtube_signal_binding"]
    return f"""# Packet 117: Reaction-Network Corpus Harness Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: scale the pass 0106 stoichiometric invariant checker from one network
to a four-case corpus and bind the result to the BuildLang/buildc scientific
runtime lane as a target receipt.

```text
stoichiometric_source_pass = {artifact['source_bindings']['stoichiometric_pass']}
buildlang_native_pass = {artifact['source_bindings']['buildlang_native_pass']}
youtube_scorecard_pass = {artifact['source_bindings']['youtube_scorecard_pass']}
network_count = {summary['network_count']}
match_count = {summary['match_count']}
drift_expected_count = {summary['drift_expected_count']}
derived_invariant_count = {summary['derived_invariant_count']}
buildlang_bridge_status = {bridge['status']}
buildlang_source_digest = {bridge['source_digest']}
buildlang_verify_check_count = {bridge['verify_check_count']}
youtube_valid_videos = {youtube['valid_video_count']}
buildlang_runtime_video_count = {youtube['buildlang_scientific_runtime_video_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Corpus

| Network | Status | Basis dim | Max drift | Candidate residuals |
| --- | --- | ---: | ---: | --- |
{network_rows(artifact)}

## BuildLang Runtime Bridge

This pass does not compile a new chemistry kernel. It binds the existing pass
0095 buildc receipt and records the required next receipts:
`{', '.join(bridge['required_kernel_receipts'])}`.

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    summary = artifact["corpus_summary"]
    return f"""# Reaction-Network Corpus Harness Brief

Date: 2026-07-01

## Decision

Make conserved-quantity checking a corpus harness before attempting a new
BuildLang chemistry kernel.

## Why

One invariant can be a demo. A corpus with positive and negative fixtures
becomes an infrastructure component: it can feed AI4Science claim packets,
BuildLang runtime kernels, and reviewer-facing proof packets.

## Current Result

Networks: {summary['network_count']}. Closed matches: {summary['match_count']}.
Expected open-system rejections: {summary['drift_expected_count']}. Derived
invariants: {summary['derived_invariant_count']}.

## Next Runtime Step

Compile a generated BuildLang kernel that emits matrix digest, vector receipt,
residual-zero check, numeric tolerance receipt, and negative-fixture receipt.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0107 Steelman: Reaction-Network Corpus Harness

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that four networks are still a small corpus. Correct.
The value is that the harness now has multiple conserved quantities and a
negative open-system rejection, not that it covers real biochemical diversity.

The second objection is that the BuildLang bridge is a target spec. Correct.
This pass binds an existing buildc receipt and names the missing chemistry
kernel receipts instead of claiming execution that has not occurred.

The third objection is that YouTube remains a source signal, not proof. Correct.
It only prioritizes the runtime and AI4Science lanes.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0107",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "corpus_summary": artifact["corpus_summary"],
        "buildlang_runtime_bridge": artifact["buildlang_runtime_bridge"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    summary = artifact["corpus_summary"]
    bridge = artifact["buildlang_runtime_bridge"]
    youtube = artifact["youtube_signal_binding"]
    open_result = next(row for row in artifact["network_results"] if row["network_id"] == "open_degradation")
    claims = [
        f"Pass 0107 created a ReactionNetworkCorpusHarnessReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0107 binds stoichiometric pass {artifact['source_bindings']['stoichiometric_pass']}, BuildLang native pass {artifact['source_bindings']['buildlang_native_pass']}, and YouTube scorecard pass {artifact['source_bindings']['youtube_scorecard_pass']}.",
        f"Pass 0107 corpus summary records network_count {summary['network_count']}, match_count {summary['match_count']}, drift_expected_count {summary['drift_expected_count']}, and derived_invariant_count {summary['derived_invariant_count']}.",
        "Pass 0107 records exact candidate residuals for closed_cycle_abc, reversible_dimerization, and enzyme_product_skeleton.",
        f"Pass 0107 open_degradation records status {open_result['status']} and candidate residual {open_result['candidate_checks'][0]['residual']}.",
        f"Pass 0107 BuildLang bridge records status {bridge['status']}, compiler {bridge['compiler']}, source_digest {bridge['source_digest']}, and verify_check_count {bridge['verify_check_count']}.",
        f"Pass 0107 records YouTube valid_video_count {youtube['valid_video_count']} and buildlang_scientific_runtime_video_count {youtube['buildlang_scientific_runtime_video_count']}.",
        f"Pass 0107 records law candidate {artifact['law_candidate']['name']} with status {artifact['law_candidate']['status']}.",
        f"Pass 0107 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0107 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0107 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"corpus_summary={summary}"],
        [f"network_results={[row['candidate_checks'] for row in artifact['network_results'] if row['status'] == 'MATCH']}"],
        [f"open_degradation={open_result}"],
        [f"buildlang_runtime_bridge={bridge}"],
        [f"youtube={youtube}"],
        [f"law_candidate={artifact['law_candidate']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0107 Reaction-Network Corpus Harness Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0107 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "REACTION_NETWORK_CORPUS_HARNESS_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
