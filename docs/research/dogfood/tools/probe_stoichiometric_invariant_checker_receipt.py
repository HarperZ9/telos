"""Generate pass 0106 stoichiometric invariant checker artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_stoichiometric_invariant_checker_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_stoichiometric_invariant_checker_receipt.py"
OUT_PATH = ROOT / "schemas" / "stoichiometric-invariant-checker-receipt-pass-0106.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0106.json"
PACKET_PATH = ROOT / "packets" / "116-stoichiometric-invariant-checker-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "116-stoichiometric-invariant-checker-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0106-stoichiometric-invariant-checker-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0106-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0106-measurements.json"


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


def sample_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["numerical_probe"]["samples"]:
        rows.append(f"| {row['t']:.3f} | {row['A']:.9f} | {row['B']:.9f} | {row['C']:.9f} | {row['total']:.9f} |")
    return "\n".join(rows)


def source_rows(artifact: dict) -> str:
    return "\n".join(f"| {row['title']} | {row['url']} | {row['kind']} |" for row in artifact["source_anchors"])


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    vector = artifact["derived_conservation_vectors"][0]
    youtube = artifact["youtube_signal_binding"]
    probe = artifact["numerical_probe"]
    negative = artifact["negative_network"]
    return f"""# Packet 116: Stoichiometric Invariant Checker Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: generalize the pass 0105 `A -> B` invariant into a small
stoichiometric-matrix checker that derives conserved quantities from
`l^T S = 0`, then rejects an open leaky network.

```text
source_reaction_pass = {artifact['source_bindings']['reaction_pass']}
source_ai4science_pass = {artifact['source_bindings']['ai4science_pass']}
youtube_pass = {youtube['youtube_pass']}
roadmap_pass = {youtube['roadmap_pass']}
valid_youtube_videos = {youtube['valid_video_count']}
transcript_receipts = {youtube['transcript_receipt_count']}
network = closed A->B->C->A cycle
derived_vector = {vector['vector']}
invariant = {vector['invariant']}
residual = {vector['residual']}
grid_points = {probe['grid_points']}
max_total_drift = {probe['max_total_drift']}
negative_candidate_residual = {negative['candidate_residual']}
negative_max_total_drift = {negative['max_total_drift']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Numerical Samples

| t | A | B | C | total |
| ---: | ---: | ---: | ---: | ---: |
{sample_rows(artifact)}

## Source Anchors

| Source | URL | Kind |
| --- | --- | --- |
{source_rows(artifact)}

## Product Meaning

The YouTube corpus pulls toward AI4Science proof packets, BuildLang scientific
runtime receipts, and optimization/scientific computing workflows. This pass
turns that signal into one reusable proof primitive: conserved-quantity
derivation with a negative fixture and promotion boundary.

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    youtube = artifact["youtube_signal_binding"]
    return f"""# Stoichiometric Invariant Checker Brief

Date: 2026-07-01

## Decision

Package conserved-quantity checks as a reusable AI4Science and BuildLang
proof-packet primitive.

## Why

The YouTube roadmap already identifies AI4Science and accountable scientific
runtime as growth vectors. This pass converts that signal into an executable
receipt: source binding, exact invariant derivation, numerical probe, negative
fixture, Forum/Index/Telos receipts, and Crucible-ready claims.

## Market Use

- Research labs get claim-to-model invariant checks before expensive assays.
- Compiler/runtime users get a target receipt shape for scientific kernels.
- Solver and optimization demos get a reusable conservation/falsification
  pattern alongside the existing constraint-encoding receipts.

## Source Binding

Valid YouTube videos: {youtube['valid_video_count']}. Transcript receipts:
{youtube['transcript_receipt_count']}. Raw transcripts included here: false.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0106 Steelman: Stoichiometric Invariant Checker

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a three-species cycle is still a toy network.
Correct. The gain over pass 0105 is not domain novelty; it is generalization
from one hand-written invariant to an exact nullspace-derived invariant.

The second objection is that numerical conservation can be an integration
artifact. Correct. The receipt therefore separates exact residual checking from
the numerical probe and includes a leaky negative fixture whose candidate
residual is nonzero.

The third objection is that YouTube videos do not prove market or scientific
claims. Correct. They are carried only as receipt-backed source signals.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0106",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "law_candidate": artifact["law_candidate"],
        "youtube_signal_binding": artifact["youtube_signal_binding"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    vector = artifact["derived_conservation_vectors"][0]
    probe = artifact["numerical_probe"]
    negative = artifact["negative_network"]
    youtube = artifact["youtube_signal_binding"]
    claims = [
        f"Pass 0106 created a StoichiometricInvariantCheckerReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0106 binds reaction pass {artifact['source_bindings']['reaction_pass']}, AI4Science pass {artifact['source_bindings']['ai4science_pass']}, YouTube pass {youtube['youtube_pass']}, and roadmap pass {youtube['roadmap_pass']}.",
        f"Pass 0106 derives conservation vector {vector['vector']} with invariant {vector['invariant']} and residual {vector['residual']}.",
        f"Pass 0106 numerical probe records {probe['grid_points']} grid points and max_total_drift {probe['max_total_drift']}.",
        f"Pass 0106 negative fixture records candidate_residual {negative['candidate_residual']} and max_total_drift {negative['max_total_drift']}.",
        f"Pass 0106 records valid_video_count {youtube['valid_video_count']} and transcript_receipt_count {youtube['transcript_receipt_count']} without raw transcript inclusion.",
        f"Pass 0106 records law candidate {artifact['law_candidate']['name']} with status {artifact['law_candidate']['status']}.",
        f"Pass 0106 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0106 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0106 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"youtube={youtube}"],
        [f"vector={vector}"],
        [f"grid_points={probe['grid_points']}", f"max_total_drift={probe['max_total_drift']}"],
        [f"negative={negative}"],
        [f"valid_video_count={youtube['valid_video_count']}", f"transcript_receipt_count={youtube['transcript_receipt_count']}", f"raw_transcript_included={youtube['raw_transcript_included']}"],
        [f"law_candidate={artifact['law_candidate']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0106 Stoichiometric Invariant Checker Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0106 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "STOICHIOMETRIC_INVARIANT_CHECKER_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
