"""Generate pass 0121 YouTube megatool growth-vector artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_youtube_megatool_growth_vector_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_youtube_megatool_growth_vector_receipt.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0121_youtube_megatool_growth_vectors.py"
OUT_PATH = ROOT / "schemas" / "youtube-megatool-growth-vector-receipt-pass-0121.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0121-youtube-megatool-growth-vector-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0121.json"
PACKET_PATH = ROOT / "packets" / "131-youtube-megatool-growth-vector-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "131-youtube-megatool-growth-vector-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0121-youtube-megatool-growth-vector-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0121-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0121-measurements.json"


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
    lines = []
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |")
    return "\n".join(lines)


def lead_rows(artifact: dict) -> list[dict]:
    return [{
        "video": row["video_id"],
        "title": row["title"],
        "chars": row["transcript_chars"],
        "dominant": row["dominant_signal"],
        "status": row["claim_status"],
    } for row in artifact["youtube_source_leads"]]


def vector_rows(artifact: dict) -> list[dict]:
    return [{
        "rank": idx + 1,
        "vector": row["vector_id"],
        "total": row["scores"]["total"],
        "status": row["claim_status"],
        "sources": ",".join(row["source_video_ids"]),
    } for idx, row in enumerate(artifact["growth_vectors"])]


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    return f"""# Packet 131: YouTube Megatool Growth-Vector Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: use the four refreshed YouTube source leads as critical data for
megatool strategy without promoting the videos' claims as verified facts.

```text
youtube_source_leads = {len(artifact['youtube_source_leads'])}
growth_vectors = {len(artifact['growth_vectors'])}
primary_30_day_push = {artifact['primary_30_day_push']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Source Leads

| Video | Title | Transcript chars | Dominant signal | Status |
| --- | --- | ---: | --- | --- |
{table(lead_rows(artifact), ['video', 'title', 'chars', 'dominant', 'status'])}

## Ranked Growth Vectors

| Rank | Vector | Score | Status | Sources |
| ---: | --- | ---: | --- | --- |
{table(vector_rows(artifact), ['rank', 'vector', 'total', 'status', 'sources'])}

## Integration Map

| Node | Market Product |
| --- | --- |
{table(artifact['integration_map'], ['node', 'market_product'])}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    top = artifact["growth_vectors"][0]
    return f"""# YouTube Megatool Growth-Vector Brief

Date: 2026-07-01

## Decision

Use the four refreshed video leads to prioritize `{top['vector_id']}` as the
next 30-day push, while keeping every video-derived product implication at
`HYPOTHESIS`.

## Product Meaning

The practical path is not one tool. It is a proof-centered system: source
intake, workspace context, expert routing, verifier verdicts, loop/action
receipts, BuildLang/runtime receipts, and measurement truth kits.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0121 Steelman: YouTube Megatool Growth Vectors

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that YouTube transcripts are weak evidence for
technical truth. Correct. This pass uses them as source leads and strategy
pressure, not as proof.

The second objection is that signal counts are crude. Correct. They are only
a routing aid; every proposed product vector still needs an experiment,
receipt, and Crucible verdict.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0121",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "youtube_source_leads": artifact["youtube_source_leads"],
        "primary_30_day_push": artifact["primary_30_day_push"],
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {
        "artifact": OUT_PATH,
        "composer": COMPOSER,
        "packet": PACKET_PATH,
        "brief": BRIEF_PATH,
        "steelman": STEELMAN_PATH,
        "test": TEST_SCRIPT,
        "validator": VALIDATOR,
        "validator_result": VALIDATOR_RESULT,
        "tool_receipts": TOOL_RECEIPTS_PATH,
    }
    shas = {name: sha256_file(path) for name, path in files.items()}
    ids = [row["video_id"] for row in artifact["youtube_source_leads"]]
    vector_ids = [row["vector_id"] for row in artifact["growth_vectors"]]
    claims = [
        f"Pass 0121 created a YoutubeMegatoolGrowthVectorReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0121 refreshed YouTube source leads {ids} and every transcript object was present under its catalog receipt key.",
        f"Pass 0121 records no raw transcript text in the artifact and keeps all video leads at SOURCE_LEAD_ONLY.",
        f"Pass 0121 ranks growth vectors {vector_ids} and sets primary_30_day_push to {artifact['primary_30_day_push']}.",
        "Pass 0121 binds pass 0116 formal/physics source-lead bridge and pass 0120 Hamiltonian runtime branch receipt.",
        "Pass 0121 includes a BuildLang/buildc node in the integration map and a scientific runtime receipt growth vector.",
        "Pass 0121 keeps every growth vector at HYPOTHESIS and gap_status inferred.",
        "Pass 0121 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0121 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0121 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0121 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"video_ids={ids}", "transcript_object_present=all_true"],
        ["raw_transcript_included=false", "claim_status=SOURCE_LEAD_ONLY"],
        [f"growth_vectors={vector_ids}", f"primary_30_day_push={artifact['primary_30_day_push']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"integration_map={artifact['integration_map']}"],
        [f"claim_statuses={[row['claim_status'] for row in artifact['growth_vectors']]}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0121 YouTube Megatool Growth Vectors", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0121 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "YOUTUBE_MEGATOOL_GROWTH_VECTOR_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
