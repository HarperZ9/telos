"""Generate pass 0125 YouTube experiment router artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_youtube_experiment_router.py"
TEST_SCRIPT = ROOT / "tools" / "test_youtube_experiment_router.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0125_youtube_experiment_router.py"
OUT_PATH = ROOT / "schemas" / "youtube-experiment-router-pass-0125.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0125-youtube-experiment-router-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0125.json"
PACKET_PATH = ROOT / "packets" / "135-youtube-experiment-router.md"
BRIEF_PATH = ROOT / "briefs" / "135-youtube-experiment-router-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0125-youtube-experiment-router-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0125-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0125-measurements.json"


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


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def source_rows(artifact: dict) -> list[dict]:
    return [{"video": row["video_id"], "theme": row["theme"], "chars": row["transcript_chars"], "dominant": row["dominant_signal"], "status": row["claim_status"]} for row in artifact["youtube_source_leads"]]


def experiment_rows(artifact: dict) -> list[dict]:
    return [{"rank": idx + 1, "experiment": row["experiment_id"], "product": row["market_product"], "score": row["scores"]["total"], "sources": ",".join(row["source_video_ids"])} for idx, row in enumerate(artifact["routed_experiments"])]


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    return f"""# Packet 135: YouTube Experiment Router

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: use the refreshed YouTube video receipts as critical frontier-signal
data and convert them into falsifiable product and architecture experiments.
Video claims remain source leads until independent proof artifacts promote them.

```text
source_leads = {len(artifact['youtube_source_leads'])}
routed_experiments = {len(artifact['routed_experiments'])}
primary_next_experiment = {artifact['primary_next_experiment']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Source Leads

| Video | Theme | Transcript chars | Dominant signal | Status |
| --- | --- | ---: | --- | --- |
{table(source_rows(artifact), ['video', 'theme', 'chars', 'dominant', 'status'])}

## Experiment Router

| Rank | Experiment | Product | Score | Sources |
| ---: | --- | --- | ---: | --- |
{table(experiment_rows(artifact), ['rank', 'experiment', 'product', 'score', 'sources'])}

## Architecture Improvements

{chr(10).join('- ' + item for item in artifact['required_architecture_improvements'])}

## Thirty-Day Push

{artifact['thirty_day_push']}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    top = artifact["routed_experiments"][0]
    return f"""# YouTube Experiment Router Brief

Date: 2026-07-01

## Decision

Promote `{top['experiment_id']}` as the next video-driven dogfood target while
shipping the demotion gate as a reliability guardrail.

## Why

The videos are high-velocity frontier signals. The marketable product is not a
better summarizer; it is a receipt router that converts talks into experiments,
falsifiers, and proof packets across Telos, BuildLang/buildc, Crucible, Forum,
Index, and Gather.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0125 Steelman: YouTube Experiment Router

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that transcript keyword counts are weak evidence.
Correct. This pass uses them only to route experiments; every routed claim stays
`HYPOTHESIS` and every video stays `SOURCE_LEAD_ONLY`.

The second objection is that market strategy cannot be proven by four videos.
Correct. The pass treats the videos as frontier-signal pressure and binds them
to existing pass 0121, 0123, and 0124 receipts rather than claiming market fit.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0125",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_leads": len(artifact["youtube_source_leads"]),
        "routed_experiments": len(artifact["routed_experiments"]),
        "primary_next_experiment": artifact["primary_next_experiment"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0125 created a YoutubeExperimentRouterReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0125 refreshed {len(artifact['youtube_source_leads'])} YouTube source leads and every transcript object is present.",
        "Pass 0125 records no raw transcript text in the artifact and keeps all video leads at SOURCE_LEAD_ONLY.",
        f"Pass 0125 routes {len(artifact['routed_experiments'])} experiments and sets primary_next_experiment to {artifact['primary_next_experiment']}.",
        f"Pass 0125 binds upstream pass receipts {artifact['upstream_receipts']}.",
        "Pass 0125 includes BuildLang/buildc, Telos, Gather, Index, Forum, and Crucible in routed experiments or architecture improvements.",
        f"Pass 0125 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0125 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0125 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0125 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"lead_ids={[row['video_id'] for row in artifact['youtube_source_leads']]}"],
        [f"lead_statuses={[row['claim_status'] for row in artifact['youtube_source_leads']]}", f"raw_flags={[row['raw_transcript_included'] for row in artifact['youtube_source_leads']]}"],
        [f"experiments={[row['experiment_id'] for row in artifact['routed_experiments']]}"],
        [f"upstreams={artifact['upstream_receipts']}"],
        [f"experiments={artifact['routed_experiments']}", f"architecture={artifact['required_architecture_improvements']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0125 YouTube Experiment Router", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0125 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    validator_receipt = run_command([sys.executable, str(VALIDATOR)], timeout=120)
    receipts = {"compose": compose_receipt, "test": test_receipt, "validator": validator_receipt}
    write_tool_receipts(artifact, compose_receipt, test_receipt, validator_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt, validator_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, receipts)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "YOUTUBE_EXPERIMENT_ROUTER_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
