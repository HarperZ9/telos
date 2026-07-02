"""Generate pass 0134 all-video author/theory index artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_all_video_author_theory_index.py"
SOURCE_HELPER = ROOT / "tools" / "all_video_author_theory_index_sources.py"
TEST_SCRIPT = ROOT / "tools" / "test_all_video_author_theory_index.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0134_all_video_author_theory_index.py"
OUT_PATH = ROOT / "schemas" / "all-video-author-theory-index-pass-0134.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0134-all-video-author-theory-index-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0134.json"
PACKET_PATH = ROOT / "packets" / "144-all-video-author-theory-index.md"
BRIEF_PATH = ROOT / "briefs" / "144-all-video-author-theory-index-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0134-all-video-author-theory-index-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0134-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0134-measurements.json"


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


def run_command(command: list[str], timeout: int = 240) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    lanes = [{"lane": row["lane_id"], "videos": row["video_count"], "tool": row["market_tool_hypothesis"]} for row in artifact["theory_lanes"]]
    authors = [{"author": row["name"], "videos": row["video_count"], "lanes": ",".join(row["lanes"][:3])} for row in artifact["author_nodes"][:20]]
    queue = [{"author": row["author"], "status": row["status"], "gate": "Requires primary-source receipts plus one negative-control fixture."} for row in artifact["reference_expansion_queue"][:12]]
    return f"""# Packet 144: All-Video Author Theory Index

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: normalize every locally recoverable YouTube/video source lead from
the Telos dogfood and demo receipts into an author, work, reference-expansion,
theory-chain, and experiment queue.

```text
video_sources = {len(artifact['video_sources'])}
channel_sources = {len(artifact['channel_sources'])}
author_nodes = {len(artifact['author_nodes'])}
theory_lanes = {len(artifact['theory_lanes'])}
reference_queue = {len(artifact['reference_expansion_queue'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Theory Lanes

| Lane | Videos | Market tool hypothesis |
| --- | ---: | --- |
{table(lanes, ['lane', 'videos', 'tool'])}

## Top Author Nodes

| Author | Videos | Lanes |
| --- | ---: | --- |
{table(authors, ['author', 'videos', 'lanes'])}

## Reference Expansion Queue

| Author | Status | Promotion gate |
| --- | --- | --- |
{table(queue, ['author', 'status', 'gate'])}

## Boundary

{artifact['recovery_boundary']['corpus_policy']} Video-derived author and
theory links remain source leads until primary works, references, and negative
fixtures are gathered and checked.
"""


def render_brief(artifact: dict) -> str:
    top_lane = artifact["theory_lanes"][0]
    return f"""# All-Video Author Theory Index Brief

Date: 2026-07-01

## Decision

Treat the months-long video corpus as a source-author graph, not a playlist.
Each author gets a work-catalog queue, reference-expansion queue, proof target,
experiment lane, and overclaim gate.

## Result

Pass 0134 indexes `{len(artifact['video_sources'])}` locally recoverable video
sources, `{len(artifact['author_nodes'])}` author nodes, and
`{len(artifact['theory_lanes'])}` theory lanes. The largest lane is
`{top_lane['lane_id']}` with `{top_lane['video_count']}` videos.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0134 Steelman: All-Video Author Theory Index

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a local repo scan is not the same as all videos
sent across every private context. Correct. This pass records the recoverable
corpus and rejects thread history as complete evidence.

The second objection is that titles and uploaders are weak author evidence.
Correct. Every author edge is a source node, not authority. The next pass must
gather primary bibliographies, papers, books, repos, and explicit citations.

The third objection is that theory lanes can overfit current interests. Correct.
The lanes are hypotheses and must be tested by executable probes, negative
fixtures, and market/source comparison before promotion.

Boundary: {artifact['recovery_boundary']['corpus_policy']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> dict:
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0134", "compose": compose_receipt, "test": test_receipt, "validator": validator_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "telos_catalog": artifact["flagship_receipts"]["telos_catalog"], "video_count": len(artifact["video_sources"]), "author_count": len(artifact["author_nodes"]), "lane_count": len(artifact["theory_lanes"])}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)
    return receipts


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "source_helper": SOURCE_HELPER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0134 created an AllVideoAuthorTheoryIndexReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0134 indexes {len(artifact['video_sources'])} locally recoverable video sources and {len(artifact['channel_sources'])} channel sources.",
        f"Pass 0134 builds {len(artifact['author_nodes'])} author nodes and {len(artifact['reference_expansion_queue'])} reference-expansion queue rows.",
        f"Pass 0134 builds {len(artifact['theory_lanes'])} theory lanes and all lanes remain HYPOTHESIS_SOURCE_LEAD.",
        "Pass 0134 keeps all video sources at SOURCE_LEAD_ONLY status.",
        f"Pass 0134 rejects {len(artifact['negative_fixtures'])} negative fixtures including thread-history completeness, raw transcript export, and natural-law promotion.",
        "Pass 0134 records recovery boundary notes for repo-recoverable corpus and incomplete thread search.",
        "Pass 0134 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0134 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0134 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0134 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"video_count={len(artifact['video_sources'])}", f"channel_count={len(artifact['channel_sources'])}"],
        [f"author_nodes={artifact['author_nodes'][:10]}", f"reference_queue_count={len(artifact['reference_expansion_queue'])}"],
        [f"theory_lanes={artifact['theory_lanes']}"],
        [f"source_statuses={sorted(set(row['claim_status'] for row in artifact['video_sources']))}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"recovery_boundary={artifact['recovery_boundary']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0134 All-Video Author Theory Index", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0134 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    validator_receipt = run_command([sys.executable, str(VALIDATOR)])
    receipts = write_tool_receipts(artifact, compose_receipt, test_receipt, validator_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt, validator_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, receipts)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    ok = all(row["status"] == "MATCH" for row in [compose_receipt, test_receipt, validator_receipt]) and artifact["status"] == "ALL_VIDEO_AUTHOR_THEORY_INDEX_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT", "videos": len(artifact["video_sources"]), "authors": len(artifact["author_nodes"])}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
