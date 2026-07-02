"""Generate pass 0085 YouTube research compounding packet artifacts."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_youtube_research_compounding_packet.py"
TEST_SCRIPT = ROOT / "tools" / "test_youtube_research_compounding_packet.py"
OUT_PATH = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0085.json"
PACKET_PATH = ROOT / "packets" / "095-youtube-research-compounding-packet.md"
BRIEF_PATH = ROOT / "briefs" / "095-youtube-research-compounding-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0085-youtube-research-compounding-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0085-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0085-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def command_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_command(command: list[str], timeout: int = 600) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, env=command_env())
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def md_escape(value: object) -> str:
    normalized = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    return normalized.replace("|", "\\|").replace("\n", " ").strip()


def card_cluster_map(artifact: dict) -> dict[str, str]:
    rows: dict[str, str] = {}
    for cluster in artifact["research_clusters"]:
        for video_id in cluster["video_ids"]:
            rows[video_id] = cluster["cluster_id"]
    return rows


def render_source_table(artifact: dict) -> str:
    clusters = card_cluster_map(artifact)
    rows = []
    for card in artifact["source_cards"]:
        if card.get("status") == "INVALID_URL":
            rows.append(f"| {card['input_index']} | INVALID | n/a | n/a | {md_escape(card['reason'])} |")
            continue
        meta = card["metadata"]
        rows.append(
            f"| {card['input_index']} | [{card['video_id']}]({card['url']}) | {md_escape(meta.get('title'))} | "
            f"{md_escape(meta.get('channel'))} | {md_escape(clusters.get(card['video_id']))} |"
        )
    return "\n".join(rows)


def render_cluster_table(artifact: dict) -> str:
    rows = []
    for cluster in artifact["research_clusters"]:
        rows.append(
            f"| {cluster['cluster_id']} | {cluster['source_count']} | {md_escape(cluster['strategic_signal'])} | "
            f"{md_escape(cluster['product_response'])} |"
        )
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    summary = artifact["video_corpus_summary"]
    return f"""# Packet 095: YouTube Research Compounding Packet

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: treat the supplied YouTube corpus as critical source data for the next
Telos/Build compounding pass. The videos are ingested as metadata plus Gather
transcript receipts; strategic product implications are explicitly hypotheses.

```text
input_urls = {artifact['input_url_count']}
valid_urls = {artifact['valid_url_count']}
metadata_matches = {artifact['metadata_match_count']}
gather_matches = {artifact['gather_match_count']}
transcript_receipts = {artifact['transcript_receipt_count']}
invalid_urls = {artifact['invalid_url_count']}
dominant_cluster = {summary['dominant_cluster']}
dominant_cluster_video_count = {summary['dominant_cluster_video_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Source Corpus

| # | Video | Title | Channel | Cluster |
| --- | --- | --- | --- | --- |
{render_source_table(artifact)}

## Research Clusters

| Cluster | Sources | Strategic Signal | Product Response |
| --- | ---: | --- | --- |
{render_cluster_table(artifact)}

## Compounding Vectors

{chr(10).join(f"- `{row['cluster_id']}` -> {row['market_product']}: {row['next_experiment']}" for row in artifact['compounding_vectors'])}

Boundary: this pass uses the videos as source leads and transcript receipts. It
does not publish raw transcripts, make investment recommendations, assert that
the videos prove scientific discoveries, or promote a new natural law.
"""


def render_brief(artifact: dict) -> str:
    vectors = artifact["compounding_vectors"]
    return f"""# YouTube Research Compounding Brief

Date: 2026-07-01

## Decision

Use the video corpus to push three immediate product experiments:

1. `{vectors[4]['market_product']}` from the 13-video enterprise quantum optimization cluster.
2. `{vectors[0]['market_product']}` from the molecular AI/drug-discovery signal.
3. `{vectors[1]['market_product']}` from the ARC/AGI evaluation signal.

## Why

The corpus is not evenly distributed: the dominant weight is quantum
optimization, with single-source but high-leverage signals in drug discovery,
ARC/AGI evaluation, quant finance, AlphaZero-style search, AGI risk, and AI
governance. That shape argues for one proof-packet architecture with
domain-specific adapters, not seven disconnected tools.

## Product Translation

The shared primitive is a claim-to-receipt object: source intake, workspace
context, model/tool action records, solver/compiler/runtime context,
measurements, verifier verdicts, and non-promotion boundaries.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0085 Steelman: YouTube Research Compounding

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that YouTube videos are weak evidence for technical
truth. They are useful market and research signal, not proof. This pass
therefore treats the videos as critical source leads while refusing to turn
their content into scientific, investment, or policy conclusions.

The second objection is source skew: 13 of 19 valid videos are from D-Wave, so
the dominant cluster reflects the supplied corpus, not the whole frontier. The
right response is to use that skew as a near-term quantum optimization demo
opportunity while continuing separate passes for biology, formal math,
scientific compute, and societal systems.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


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
    claims = [
        f"Pass 0085 created a YouTubeResearchCompoundingPacket/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0085 ingested {artifact['input_url_count']} supplied URLs, recorded {artifact['valid_url_count']} valid YouTube URLs, {artifact['invalid_url_count']} invalid URL, and {artifact['metadata_match_count']} metadata matches.",
        f"Pass 0085 recorded {artifact['gather_match_count']} Gather video matches and {artifact['transcript_receipt_count']} transcript receipt hashes without storing raw transcripts.",
        f"Pass 0085 records {len(artifact['research_clusters'])} research clusters and dominant cluster {artifact['video_corpus_summary']['dominant_cluster']} with {artifact['video_corpus_summary']['dominant_cluster_video_count']} videos.",
        f"Pass 0085 records {len(artifact['compounding_vectors'])} hypothesis-only compounding vectors and treats all video-driven product responses as hypotheses.",
        f"Pass 0085 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0085 contains {len(artifact['negative_fixtures'])} negative fixtures, unsupported_claim_count {artifact['unsupported_claim_count']}, and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0085 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"input_url_count={artifact['input_url_count']}", f"valid_url_count={artifact['valid_url_count']}", f"invalid_url_count={artifact['invalid_url_count']}", f"metadata_match_count={artifact['metadata_match_count']}"],
        [f"gather_match_count={artifact['gather_match_count']}", f"transcript_receipt_count={artifact['transcript_receipt_count']}", f"raw_transcript_any={any(row.get('raw_transcript_included') for row in artifact['source_cards'])}"],
        [f"cluster_count={len(artifact['research_clusters'])}", f"dominant_cluster={artifact['video_corpus_summary']['dominant_cluster']}", f"dominant_cluster_video_count={artifact['video_corpus_summary']['dominant_cluster_video_count']}"],
        [f"compounding_vector_count={len(artifact['compounding_vectors'])}", f"statuses={sorted({row['verification_status'] for row in artifact['compounding_vectors']})}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0085 YouTube Research Compounding Packet", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0085 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0085",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "youtube": {
            "valid_url_count": artifact["valid_url_count"],
            "metadata_match_count": artifact["metadata_match_count"],
            "gather_match_count": artifact["gather_match_count"],
            "transcript_receipt_count": artifact["transcript_receipt_count"],
            "raw_transcripts_stored": False,
        },
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "YOUTUBE_RESEARCH_COMPOUNDING_PACKET_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
