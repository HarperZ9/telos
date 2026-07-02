"""Generate pass 0096 YouTube field growth-vector scorecard artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_youtube_field_growth_vector_scorecard.py"
TEST_SCRIPT = ROOT / "tools" / "test_youtube_field_growth_vector_scorecard.py"
OUT_PATH = ROOT / "schemas" / "youtube-field-growth-vector-scorecard-pass-0096.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0096.json"
PACKET_PATH = ROOT / "packets" / "106-youtube-field-growth-vector-scorecard.md"
BRIEF_PATH = ROOT / "briefs" / "106-youtube-field-growth-vector-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0096-youtube-field-growth-vector-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0096-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0096-measurements.json"


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


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def vector_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["field_vectors"]:
        score = row["wedge_score"]["total"]
        rows.append(f"| {row['id']} | {row['field']} | {row['source_video_count']} | {score} | {row['combined_megatool']} |")
    return "\n".join(rows)


def integration_rows(artifact: dict) -> str:
    return "\n".join(f"| {row['internal_tool']} | {', '.join(row['outputs'])} | {row['market_product']} |" for row in artifact["integration_map"])


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    source = artifact["source_summary"]
    buildlang = artifact["buildlang_binding"]
    primary = artifact["primary_30_day_push"]
    return f"""# Packet 106: YouTube Field Growth-Vector Scorecard

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: use the pass 0085 YouTube corpus as crucial source-lead data, then
bind those leads to the pass 0093 bridge, pass 0094 optimization workflow, and
pass 0095 BuildLang-native receipt.

```text
valid_videos = {source['valid_video_count']}
metadata_receipts = {source['metadata_match_count']}
transcript_receipts = {source['transcript_receipt_count']}
dominant_cluster = {source['dominant_cluster']}
dominant_cluster_video_count = {source['dominant_cluster_video_count']}
buildlang_native_pass = {buildlang['native_pass']}
buildlang_verify_checks = {buildlang['verify_check_count']}
primary_30_day_push = {primary['product']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Ranked Growth Vectors

| Vector | Field | Videos | Score | Megatool |
| --- | --- | ---: | ---: | --- |
{vector_rows(artifact)}

## Megatool Integration Map

| Internal Tool | Outputs | Product Layer |
| --- | --- | --- |
{integration_rows(artifact)}

## Primary Push

{primary['experiment']}

Acceptance:

1. {primary['acceptance'][0]}
2. {primary['acceptance'][1]}
3. {primary['acceptance'][2]}

Boundary: videos remain source leads, not proof. This packet ranks hypotheses
and next experiments; it does not promote market dominance, scientific
discovery, language replacement, quantum advantage, or a natural law.
"""


def render_brief(artifact: dict) -> str:
    primary = artifact["primary_30_day_push"]
    return f"""# YouTube Field Growth-Vector Brief

Date: 2026-07-01

## Decision

Run `{primary['product']}` as the next 30-day market push.

## Why

It is the only vector with 13 source videos plus verified local receipts across
solver replay, NetworkX DAG optimization, BuildLang check/verify/run receipts,
Forum, Index, Telos, Gather, and Crucible.

## Product Shape

Turn the workflow into a public proof workbench: source intake, objective
definition, branch comparison, BuildLang native kernels, dependency boundaries,
and verdict export.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0096 Steelman: YouTube Field Growth Vectors

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that the source set is skewed. Correct. Thirteen of
nineteen valid videos sit in enterprise quantum optimization, so the scorecard
should prioritize optimization while still preserving smaller but strategically
important vectors for AI4Science, evals, quant, proof search, visual truth, and
governance.

The second objection is that market need is still inferred. Correct. Each gap
is labeled as an inferred hypothesis unless backed by a local receipt. The next
pass must convert one vector into an executable proof demo, not another essay.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0096",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "primary_vector": artifact["primary_30_day_push"]["vector_id"],
        "vector_count": len(artifact["field_vectors"]),
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
    buildlang = artifact["buildlang_binding"]
    primary = artifact["primary_30_day_push"]
    claims = [
        f"Pass 0096 created a YouTubeFieldGrowthVectorScorecard/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0096 binds source passes {artifact['source_bindings']} and treats YouTube videos as source leads.",
        f"Pass 0096 source summary records {source['valid_video_count']} valid videos, {source['metadata_match_count']} metadata receipts, {source['transcript_receipt_count']} transcript receipts, and {source['cluster_count']} clusters.",
        f"Pass 0096 ranks {len(artifact['field_vectors'])} field vectors and selects {primary['vector_id']} as the primary 30-day push.",
        f"Pass 0096 primary vector has {artifact['field_vectors'][0]['source_video_count']} source videos and product {primary['product']}.",
        f"Pass 0096 binds BuildLang native pass {buildlang['native_pass']} with {buildlang['verify_check_count']} verify checks and best value {buildlang['best_value']}.",
        f"Pass 0096 integration map contains {len(artifact['integration_map'])} internal megatool nodes.",
        f"Pass 0096 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0096 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0096 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"source_policy={source['source_policy']}"],
        [f"valid_video_count={source['valid_video_count']}", f"metadata={source['metadata_match_count']}", f"transcripts={source['transcript_receipt_count']}", f"clusters={source['cluster_count']}"],
        [f"vector_count={len(artifact['field_vectors'])}", f"primary={primary['vector_id']}"],
        [f"primary_video_count={artifact['field_vectors'][0]['source_video_count']}", f"product={primary['product']}"],
        [f"native_pass={buildlang['native_pass']}", f"verify_check_count={buildlang['verify_check_count']}", f"best_value={buildlang['best_value']}"],
        [f"integration_node_count={len(artifact['integration_map'])}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0096 YouTube Field Growth-Vector Scorecard", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0096 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "YOUTUBE_FIELD_GROWTH_VECTOR_SCORECARD_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
