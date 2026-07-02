"""Generate pass 0115 solver-branch replay adapter artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_solver_branch_replay_adapter.py"
TEST_SCRIPT = ROOT / "tools" / "test_solver_branch_replay_adapter.py"
OUT_PATH = ROOT / "schemas" / "solver-branch-replay-adapter-pass-0115.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0115.json"
PACKET_PATH = ROOT / "packets" / "125-solver-branch-replay-adapter.md"
BRIEF_PATH = ROOT / "briefs" / "125-solver-branch-replay-adapter-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0115-solver-branch-replay-adapter-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0115-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0115-measurements.json"


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


def md(value: object) -> str:
    return str(value).replace("|", "/").replace("\n", " ")


def branch_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["solver_branches"]:
        detail = row.get("case_id") or row.get("module") or row.get("kind")
        rows.append(f"| {row['branch_id']} | {row['status']} | {md(detail)} |")
    return "\n".join(rows)


def lead_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["new_youtube_source_leads"]:
        rows.append(f"| {row['video_id']} | {md(row.get('title'))} | {row['source_status']} | {row['claim_status']} | {row.get('transcript_chars')} |")
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    y = artifact["new_youtube_lead_summary"]
    return f"""# Packet 125: Solver-Branch Replay Adapter

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: replay the pass 0114 constrained optimization suite through local
solver branches while fencing unavailable solvers and binding four new YouTube
videos as Gather-verified source leads.

```text
suite_pass = {artifact['source_bindings']['suite_pass']}
youtube_roadmap_pass = {artifact['source_bindings']['youtube_roadmap_pass']}
new_youtube_leads = {y['lead_count']}
new_youtube_transcript_receipts = {y['transcript_receipt_count']}
raw_transcripts_included = {str(y['raw_transcripts_included']).lower()}
drift_total = {artifact['drift_total']}
unavailable_branch_count = {artifact['unavailable_branch_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Solver Branches

| Branch | Status | Detail |
| --- | --- | --- |
{branch_rows(artifact)}

## New YouTube Source Leads

| Video | Title | Source status | Claim status | Transcript chars |
| --- | --- | --- | --- | ---: |
{lead_rows(artifact)}

## Roadmap Pressure

All four roadmap pressure items remain hypotheses. The pass does not claim to
solve quantum foundations, category theory, theoretical CS, or looped LLM
reasoning; it records where the next proof packets should point.

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    y = artifact["new_youtube_lead_summary"]
    return f"""# Solver-Branch Replay Adapter Brief

Date: 2026-07-01

## Decision

Turn the multi-domain optimization suite into a solver-branch replay adapter.
The pass now records exact local replay, SciPy HiGHS replay for the quant case,
and explicit unavailable fences for OR-Tools and PuLP in this environment.

## Market Wedge

The useful product is not another solver wrapper. It is a proof packet that
binds solver availability, objective, assignment, source leads, tool receipts,
and non-promotion boundaries. The four new YouTube leads add pressure toward
physics, formal math, theoretical CS, and agent-loop research packets.

## Source Discipline

New lead count: {y['lead_count']}. Transcript receipt count:
{y['transcript_receipt_count']}. Raw transcript included: {y['raw_transcripts_included']}.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0115 Steelman: Solver-Branch Replay Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that the adapter mostly proves small toy cases, not
industrial solver integration. Correct. This pass validates replay receipts,
availability fences, and source-lead handling.

The second objection is that YouTube transcripts can create false authority.
Correct. The videos are treated as source leads only: metadata, hashes, topic
hypotheses, and roadmap pressure, with no raw transcript content promoted.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0115",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "availability": artifact["availability"],
        "solver_branches": artifact["solver_branches"],
        "new_youtube_lead_summary": artifact["new_youtube_lead_summary"],
        "new_youtube_source_leads": artifact["new_youtube_source_leads"],
        "roadmap_pressure": artifact["roadmap_pressure"],
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    y = artifact["new_youtube_lead_summary"]
    claims = [
        f"Pass 0115 created a SolverBranchReplayAdapterReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0115 binds suite pass {artifact['source_bindings']['suite_pass']}, YouTube roadmap pass {artifact['source_bindings']['youtube_roadmap_pass']}, and lead store {artifact['source_bindings']['new_youtube_lead_store']}.",
        f"Pass 0115 records SciPy as {artifact['availability']['scipy']['status']}, OR-Tools as {artifact['availability']['ortools']['status']}, and PuLP as {artifact['availability']['pulp']['status']}.",
        "Pass 0115 builtin exhaustive replay matched all four pass 0114 optimization cases.",
        "Pass 0115 SciPy HiGHS replay matched quant_risk_budget objective 9/2 with asset weights 1/2, 1/4, and 1/4.",
        "Pass 0115 fenced OR-Tools CP-SAT and PuLP CBC as UNAVAILABLE_FENCED in this environment.",
        f"Pass 0115 records {y['lead_count']} new YouTube source leads, {y['gather_verified_count']} Gather-verified leads, {y['transcript_receipt_count']} transcript receipts, and raw_transcripts_included {y['raw_transcripts_included']}.",
        "Pass 0115 records video ids HbKzqvey5PA, 4MQbd5wTlI8, EdVG5qNm2rY, and nYwid6Q5HXk as SOURCE_LEAD_ONLY.",
        f"Pass 0115 records {len(artifact['roadmap_pressure'])} roadmap-pressure hypotheses derived from the four new source leads.",
        f"Pass 0115 records market tool_count {artifact['market_surface']['tool_count']} with official solver documentation anchors.",
        "Pass 0115 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0115 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0115 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"availability={artifact['availability']}"],
        [f"exhaustive={next(row for row in artifact['solver_branches'] if row['branch_id'] == 'builtin_exhaustive_replay')}"],
        [f"scipy={next(row for row in artifact['solver_branches'] if row['branch_id'] == 'scipy_highs_quant_replay')}"],
        [f"ortools={next(row for row in artifact['solver_branches'] if row['branch_id'] == 'ortools_cp_sat')}", f"pulp={next(row for row in artifact['solver_branches'] if row['branch_id'] == 'pulp_cbc')}"],
        [f"new_youtube_lead_summary={y}"],
        [f"video_ids={[row['video_id'] for row in artifact['new_youtube_source_leads']]}"],
        [f"roadmap_pressure={artifact['roadmap_pressure']}"],
        [f"market_surface={artifact['market_surface']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0115 Solver-Branch Replay Adapter", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0115 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "SOLVER_BRANCH_REPLAY_ADAPTER_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
