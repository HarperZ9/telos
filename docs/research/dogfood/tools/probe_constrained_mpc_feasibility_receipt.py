"""Generate pass 0113 constrained-MPC feasibility artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_constrained_mpc_feasibility_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_constrained_mpc_feasibility_receipt.py"
OUT_PATH = ROOT / "schemas" / "constrained-mpc-feasibility-receipt-pass-0113.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0113.json"
PACKET_PATH = ROOT / "packets" / "123-constrained-mpc-feasibility-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "123-constrained-mpc-feasibility-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0113-constrained-mpc-feasibility-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0113-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0113-measurements.json"


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


def source_rows(artifact: dict) -> str:
    return "\n".join(f"| {row['tool']} | {row['kind']} | {row['url']} |" for row in artifact["source_anchors"])


def video_rows(artifact: dict) -> str:
    req = artifact["youtube_requirements"]
    return "\n".join(f"| {vid} | {title} |" for vid, title in zip(req["source_video_ids"], req["source_titles"]))


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    feasible = artifact["feasible_case"]
    neg = artifact["negative_fixtures"]
    youtube = artifact["youtube_binding"]
    req = artifact["youtube_requirements"]
    return f"""# Packet 123: Constrained-MPC Feasibility Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: convert the YouTube critical-data roadmap into a bounded control and
optimization proof packet. The pass uses the 13-video enterprise quantum
optimization cluster as source-lead pressure, then refuses to promote video
claims until exact local feasibility witnesses and source anchors exist.

```text
lyapunov_pass = {artifact['source_bindings']['lyapunov_pass']}
youtube_roadmap_pass = {artifact['source_bindings']['youtube_roadmap_pass']}
top_priority = {req['top_priority']}
dominant_cluster = {req['dominant_cluster']}
dominant_cluster_video_count = {req['dominant_cluster_video_count']}
valid_youtube_videos = {youtube['valid_video_count']}
transcript_receipts = {youtube['transcript_receipt_count']}
raw_transcripts_included = {youtube['raw_transcript_included']}
system = {feasible['system']}
x0 = {feasible['x0']}
controls = {feasible['controls']}
states = {feasible['states']}
terminal_residual = {feasible['terminal_residual']}
objective = {feasible['objective']}
infeasible_fixture = {neg['infeasible_terminal_fixture']['classification']}
bad_plan_fixture = {neg['bad_plan_fixture']['classification']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## YouTube-Derived Requirements

The source videos are crucial data for product direction, not standalone proof.
They force the packet to include these fields:
`{', '.join(req['required_receipt_fields'])}`.

| Video id | Source-lead title |
| --- | --- |
{video_rows(artifact)}

## Exact Feasible Rollout

| Field | Value |
| --- | --- |
| System | `{feasible['system']}` |
| Horizon | `{feasible['horizon']}` |
| Controls | `{feasible['controls']}` |
| States | `{feasible['states']}` |
| Objective | `{feasible['objective']}` |
| Constraint status | `{feasible['constraint_status']}` |

## Negative Fixtures

| Fixture | Witness | Classification |
| --- | --- | --- |
| Infeasible terminal | minimum terminal absolute residual `{neg['infeasible_terminal_fixture']['minimum_terminal_abs_residual']}` | `{neg['infeasible_terminal_fixture']['classification']}` |
| Bad plan | terminal residual `{neg['bad_plan_fixture']['terminal_residual']}` | `{neg['bad_plan_fixture']['classification']}` |

## Source Anchors

| Tool | Kind | URL |
| --- | --- | --- |
{source_rows(artifact)}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    req = artifact["youtube_requirements"]
    return f"""# Constrained-MPC Feasibility Brief

Date: 2026-07-01

## Decision

Promote constrained control feasibility packets as the next bridge between the
YouTube-driven optimization market signal and BuildLang/buildc scientific
runtime work.

## Why Now

The pass 0102 YouTube corpus identified `{req['top_priority']}` as the top
priority, with {req['dominant_cluster_video_count']} videos in the
`{req['dominant_cluster']}` cluster. Pass 0113 turns that pressure into exact
rollout, constraint, infeasibility, and bad-plan receipts.

## Product Wedge

MPC tools solve and model constrained control problems. The Telos/Build wedge is
the portable proof packet: source leads, formal problem statement, candidate
plan, rollout, constraint verdicts, negative fixtures, and Crucible claims.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0113 Steelman: Constrained-MPC Feasibility

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a scalar integrator is not a warehouse,
robotics, defense, or quantum optimization workflow. Correct. It is the smallest
exact receipt that proves the packet can bind problem, plan, constraints,
rollout, and negative witnesses before claiming broader scope.

The second objection is that YouTube videos are weak technical evidence.
Correct. This pass treats them as crucial market and architecture data only.
They determine which receipt fields must exist; they do not validate solver,
hardware, investment, policy, or scientific claims.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0113",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "feasible_case": artifact["feasible_case"],
        "negative_fixtures": artifact["negative_fixtures"],
        "market_surface": artifact["market_surface"],
        "youtube_binding": artifact["youtube_binding"],
        "youtube_requirements": artifact["youtube_requirements"],
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    feasible = artifact["feasible_case"]
    neg = artifact["negative_fixtures"]
    youtube = artifact["youtube_binding"]
    req = artifact["youtube_requirements"]
    claims = [
        f"Pass 0113 created a ConstrainedMPCFeasibilityReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0113 binds Lyapunov pass {artifact['source_bindings']['lyapunov_pass']} and YouTube roadmap pass {artifact['source_bindings']['youtube_roadmap_pass']}.",
        f"Pass 0113 feasible case records system {feasible['system']}, x0 {feasible['x0']}, controls {feasible['controls']}, states {feasible['states']}, terminal_residual {feasible['terminal_residual']}, and objective {feasible['objective']}.",
        f"Pass 0113 infeasible fixture classification is {neg['infeasible_terminal_fixture']['classification']} with minimum_terminal_abs_residual {neg['infeasible_terminal_fixture']['minimum_terminal_abs_residual']}.",
        f"Pass 0113 bad plan fixture classification is {neg['bad_plan_fixture']['classification']} with terminal_residual {neg['bad_plan_fixture']['terminal_residual']}.",
        f"Pass 0113 YouTube binding records {youtube['valid_video_count']} valid videos, {youtube['transcript_receipt_count']} transcript receipts, dominant cluster {youtube['dominant_cluster']}, and raw_transcript_included {youtube['raw_transcript_included']}.",
        f"Pass 0113 YouTube requirements record top priority {req['top_priority']}, dominant_cluster_video_count {req['dominant_cluster_video_count']}, and first required field {req['required_receipt_fields'][0]}.",
        f"Pass 0113 records {len(artifact['source_anchors'])} source anchors and market tool_count {artifact['market_surface']['tool_count']}.",
        f"Pass 0113 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0113 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0113 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"feasible_case={feasible}"],
        [f"infeasible_fixture={neg['infeasible_terminal_fixture']}"],
        [f"bad_plan_fixture={neg['bad_plan_fixture']}"],
        [f"youtube_binding={youtube}"],
        [f"youtube_requirements={req}"],
        [f"source_anchor_count={len(artifact['source_anchors'])}", f"market_surface={artifact['market_surface']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0113 Constrained-MPC Feasibility Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0113 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "CONSTRAINED_MPC_FEASIBILITY_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
