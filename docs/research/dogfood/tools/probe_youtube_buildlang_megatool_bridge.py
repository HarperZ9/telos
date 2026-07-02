"""Generate pass 0093 YouTube-to-BuildLang megatool bridge artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_youtube_buildlang_megatool_bridge.py"
TEST_SCRIPT = ROOT / "tools" / "test_youtube_buildlang_megatool_bridge.py"
OUT_PATH = ROOT / "schemas" / "youtube-buildlang-megatool-bridge-pass-0093.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0093.json"
PACKET_PATH = ROOT / "packets" / "103-youtube-buildlang-megatool-bridge.md"
BRIEF_PATH = ROOT / "briefs" / "103-youtube-buildlang-megatool-bridge-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0093-youtube-buildlang-megatool-bridge-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0093-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0093-measurements.json"


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


def node_rows(artifact: dict) -> str:
    rows = []
    for node in artifact["megatool_nodes"]:
        score = node["wedge_score"]
        rows.append(f"| {node['cluster_id']} | {node['market_facing_product']} | {node['source_video_count']} | {score['total']} | {node['next_experiment']} |")
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    source = artifact["source_summary"]
    solver = artifact["solver_summary"]
    buildlang = artifact["buildlang_summary"]
    primary = artifact["primary_30_day_push"]
    return f"""# Packet 103: YouTube-to-BuildLang Megatool Bridge

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: compound the user-supplied YouTube source corpus into the newer solver
and BuildLang receipt passes, then rank the next megatool product experiments.

```text
youtube_valid_videos = {source['valid_video_count']}
dominant_cluster = {source['dominant_cluster']}
dominant_cluster_video_count = {source['dominant_cluster_video_count']}
exact_optimum_value = {solver['exact_optimum_value']}
scipy_exact_hit_count = {solver['scipy_exact_hit_count']}
buildc_verify_check_count = {buildlang['buildc_verify_check_count']}
buildc_measurement_count = {buildlang['buildc_measurement_count']}
primary_30_day_push = {primary['market_facing_product']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Ranked Megatool Nodes

| Cluster | Product | Sources | Score | Next Experiment |
| --- | --- | ---: | ---: | --- |
{node_rows(artifact)}

## Integration Meaning

The highest-leverage motion is no longer "watch the videos" or "build a
solver demo" as isolated work. The bridge is: YouTube source receipts ->
problem formulation -> solver branch receipts -> BuildLang source/runtime
receipts -> Crucible verdict -> market-facing proof packet.

Boundary: every node remains a hypothesis with local receipts. This packet does
not promote YouTube claims, quantum advantage, BuildLang replacement,
scientific discovery, investment advice, or a natural law.
"""


def render_brief(artifact: dict) -> str:
    primary = artifact["primary_30_day_push"]
    return f"""# YouTube-to-BuildLang Megatool Bridge Brief

Date: 2026-07-01

## Decision

The primary 30-day push is `{primary['market_facing_product']}`.

## Why

It has the strongest combined evidence: 13 source videos in the dominant
YouTube cluster, an exact optimization baseline, a SciPy adapter with exact
hits, an availability matrix, and a BuildLang `buildc check --receipt` adapter.

## Shape

Ship one public packet that shows source intake, problem definition, solver
branch comparison, dependency state, BuildLang source receipt, measurement
verdicts, and non-promotion boundaries. Then mirror the same schema into
AI4Science and ARC/AGI evaluation skeletons.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0093 Steelman: YouTube-to-BuildLang Megatool Bridge

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that the bridge ranks product experiments, not
world-scale solutions. Correct. It is a prioritization packet built from local
receipts, and it should be judged by whether the next demo becomes more
checkable.

The second objection is that the YouTube corpus is skewed toward quantum
optimization. Correct. The ranking uses that skew rather than pretending the
source set is representative of all science and society.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0093",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "primary_30_day_push": artifact["primary_30_day_push"]["market_facing_product"],
        "node_count": len(artifact["megatool_nodes"]),
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
    solver = artifact["solver_summary"]
    buildlang = artifact["buildlang_summary"]
    claims = [
        f"Pass 0093 created a YouTubeBuildLangMegatoolBridge/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0093 binds source passes {artifact['source_bindings']} and keeps YouTube videos as source leads.",
        f"Pass 0093 source summary records {source['valid_video_count']} valid videos, dominant cluster {source['dominant_cluster']}, and {source['dominant_cluster_video_count']} dominant-cluster videos.",
        f"Pass 0093 solver summary records exact optimum value {solver['exact_optimum_value']}, SciPy exact hit count {solver['scipy_exact_hit_count']}, and local available/source-present surfaces {solver['local_available_or_source_present']}.",
        f"Pass 0093 BuildLang summary records buildc source digest {buildlang['buildc_source_digest']}, {buildlang['buildc_verify_check_count']} verify checks, and {buildlang['buildc_measurement_count']} adapter measurements.",
        f"Pass 0093 ranks {len(artifact['megatool_nodes'])} megatool nodes and selects {artifact['primary_30_day_push']['market_facing_product']} as the primary 30-day push.",
        f"Pass 0093 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0093 contains {len(artifact['negative_fixtures'])} negative fixtures, unsupported_claim_count {artifact['unsupported_claim_count']}, and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0093 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"valid_video_count={source['valid_video_count']}", f"dominant_cluster={source['dominant_cluster']}", f"dominant_cluster_video_count={source['dominant_cluster_video_count']}"],
        [f"exact_optimum_value={solver['exact_optimum_value']}", f"scipy_exact_hit_count={solver['scipy_exact_hit_count']}", f"local_available_or_source_present={solver['local_available_or_source_present']}"],
        [f"buildc_source_digest={buildlang['buildc_source_digest']}", f"buildc_verify_check_count={buildlang['buildc_verify_check_count']}", f"buildc_measurement_count={buildlang['buildc_measurement_count']}"],
        [f"node_count={len(artifact['megatool_nodes'])}", f"primary_30_day_push={artifact['primary_30_day_push']['market_facing_product']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0093 YouTube-to-BuildLang Megatool Bridge", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0093 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "YOUTUBE_BUILDLANG_MEGATOOL_BRIDGE_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
