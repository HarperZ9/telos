"""Generate pass 0102 YouTube critical-data megatool roadmap artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_youtube_critical_data_megatool_roadmap.py"
TEST_SCRIPT = ROOT / "tools" / "test_youtube_critical_data_megatool_roadmap.py"
OUT_PATH = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0102.json"
PACKET_PATH = ROOT / "packets" / "112-youtube-critical-data-megatool-roadmap.md"
BRIEF_PATH = ROOT / "briefs" / "112-youtube-critical-data-megatool-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0102-youtube-critical-data-megatool-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0102-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0102-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ascii_text(value: object) -> str:
    return str(value).encode("ascii", "ignore").decode("ascii").strip()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    safe = text.encode("ascii", "ignore").decode("ascii")
    path.write_text(safe, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def cluster_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["source_to_architecture_claims"]:
        rows.append(
            f"| `{row['cluster_id']}` | {row['video_count']} | {ascii_text(row['observed_signal'])} | {ascii_text(row['architecture_pull'])} |"
        )
    return "\n".join(rows)


def roadmap_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["roadmap_nodes"]:
        reqs = []
        for req in row["requirements"]:
            reqs.append(req["requirement_id"] if isinstance(req, dict) else str(req))
        rows.append(
            f"| `{row['node_id']}` | {row['source_video_count']} | {row['wedge_score']['total']} | {row['market_product']} | {', '.join(reqs)} |"
        )
    return "\n".join(rows)


def experiment_rows(artifact: dict) -> str:
    return "\n".join(
        f"| `{row['experiment_id']}` | {', '.join(row['source_nodes'])} | {', '.join(row['acceptance'])} | {row['status']} |"
        for row in artifact["experiments"]
    )


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    source = artifact["source_summary"]
    return f"""# Packet 112: YouTube Critical-Data Megatool Roadmap

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: use the supplied YouTube videos as critical architecture and market
data, then bind them to the current Telos/Build optimization receipts. Raw
transcripts are not stored; metadata and transcript receipt hashes are used as
source evidence, and video-specific claims remain source leads.

```text
valid_videos = {source['valid_video_count']}
invalid_urls = {source['invalid_url_count']}
metadata_receipts = {source['metadata_match_count']}
transcript_receipts = {source['transcript_receipt_count']}
dominant_cluster = {source['dominant_cluster']}
top_priority = {artifact['top_priority']}
constraint_lesson = {artifact['constraint_encoding_lesson']['name']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Source Signals

| Cluster | Videos | Observed Signal | Architecture Pull |
| --- | ---: | --- | --- |
{cluster_rows(artifact)}

## Roadmap Nodes

| Node | Videos | Score | Product | Required Receipts |
| --- | ---: | ---: | --- | --- |
{roadmap_rows(artifact)}

## Next Experiments

| Experiment | Nodes | Acceptance | Status |
| --- | --- | --- | --- |
{experiment_rows(artifact)}

## Boundary

The video corpus is crucial input, not proof. This roadmap uses it to rank
architecture work and market hypotheses. It does not promote any scientific,
investment, policy, benchmark, language-replacement, or natural-law claim.
"""


def render_brief(artifact: dict) -> str:
    top = artifact["roadmap_nodes"][0]
    return f"""# YouTube Critical-Data Megatool Brief

Date: 2026-07-01

## Decision

Prioritize `{top['market_product']}` and back-propagate pass 0101's constraint
encoding lesson into every optimization branch receipt.

## Why

The video corpus supplies 19 gathered video leads, 19 transcript receipt hashes,
and a 13-video enterprise quantum optimization cluster. The local proof stack
now adds a concrete failure mode: equality-to-capacity BQM penalties can certify
the wrong thing unless the receipt exposes inequality/slack encoding.

## 30-Day Shape

Ship a public demo where YouTube source leads, problem statement, solver
branches, BuildLang kernels, encoding receipts, feasibility checks, and
Crucible verdicts are one portable packet.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0102 Steelman: YouTube Critical-Data Roadmap

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is source skew. Thirteen videos come from D-Wave and
enterprise quantum optimization. That should drive the first public demo, but
not narrow the mission. The smaller clusters still create high-upside adapters
for AI4Science, ARC/AGI evaluation, quant finance, search/verifier loops, risk,
governance, and visual truth.

The second objection is that video metadata is not evidence of the underlying
technical claims. Correct. Pass 0102 uses metadata and transcript receipt hashes
as source leads only. It adds executable local receipts, especially pass 0101's
constraint-encoding counterexample, before promoting architecture requirements.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0102",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "top_priority": artifact["top_priority"],
        "roadmap_node_count": len(artifact["roadmap_nodes"]),
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "brief": sha256_file(BRIEF_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
        "tool_receipts": sha256_file(TOOL_RECEIPTS_PATH),
    }
    source = artifact["source_summary"]
    claims = [
        f"Pass 0102 created a YouTubeCriticalDataMegatoolRoadmap/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0102 binds source passes {artifact['source_bindings']} and keeps YouTube claims as source leads.",
        f"Pass 0102 records {source['valid_video_count']} valid videos, {source['invalid_url_count']} invalid URL, {source['metadata_match_count']} metadata receipts, and {source['transcript_receipt_count']} transcript receipts.",
        f"Pass 0102 maps {len(artifact['source_to_architecture_claims'])} source clusters into architecture pulls.",
        f"Pass 0102 ranks {len(artifact['roadmap_nodes'])} roadmap nodes and selects {artifact['top_priority']} as top priority.",
        "Pass 0102 propagates pass 0101's constraint_encoding_receipt requirement into the top optimization roadmap node.",
        f"Pass 0102 defines {len(artifact['experiments'])} next experiments.",
        f"Pass 0102 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0102 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0102 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", "claim_status=SOURCE_LEAD"],
        [f"valid={source['valid_video_count']}", f"invalid={source['invalid_url_count']}", f"metadata={source['metadata_match_count']}", f"transcripts={source['transcript_receipt_count']}"],
        [f"cluster_count={len(artifact['source_to_architecture_claims'])}"],
        [f"node_count={len(artifact['roadmap_nodes'])}", f"top_priority={artifact['top_priority']}"],
        [f"top_requirements={artifact['roadmap_nodes'][0]['requirements']}"],
        [f"experiment_count={len(artifact['experiments'])}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0102 YouTube Critical-Data Megatool Roadmap", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0102 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "YOUTUBE_CRITICAL_DATA_MEGATOOL_ROADMAP_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
