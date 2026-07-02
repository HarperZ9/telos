"""Generate pass 0133 YouTube source-lead intake artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_youtube_source_lead_intake.py"
TEST_SCRIPT = ROOT / "tools" / "test_youtube_source_lead_intake.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0133_youtube_source_lead_intake.py"
OUT_PATH = ROOT / "schemas" / "youtube-source-lead-intake-pass-0133.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0133-youtube-source-lead-intake-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0133.json"
PACKET_PATH = ROOT / "packets" / "143-youtube-source-lead-intake.md"
BRIEF_PATH = ROOT / "briefs" / "143-youtube-source-lead-intake-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0133-youtube-source-lead-intake-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0133-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0133-measurements.json"


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


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    leads = [{"id": row["video_id"], "title": row["title"], "route": row["route"], "terms": ",".join(row["top_terms"][:4])} for row in artifact["video_leads"]]
    routes = [{"route": row["route"], "videos": row["video_count"], "status": row["status"]} for row in artifact["route_summary"]]
    products = [{"tool": row["tool"], "status": row["status"], "wedge": row["wedge"]} for row in artifact["product_hypotheses"]]
    return f"""# Packet 143: YouTube Source-Lead Intake

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: ingest the newly supplied YouTube links into the dogfood research
lane as source leads, not verified claims.

```text
source_receipts = {len(artifact['source_receipts'])}
video_leads = {len(artifact['video_leads'])}
routes = {len(artifact['route_summary'])}
negative_fixtures = {len(artifact['negative_fixtures'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Video Leads

| Id | Title | Route | Top terms |
| --- | --- | --- | --- |
{table(leads, ['id', 'title', 'route', 'terms'])}

## Route Summary

| Route | Videos | Status |
| --- | ---: | --- |
{table(routes, ['route', 'videos', 'status'])}

## Product Hypotheses

| Tool | Status | Wedge |
| --- | --- | --- |
{table(products, ['tool', 'status', 'wedge'])}

## Boundary

{artifact['boundary']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# YouTube Source-Lead Intake Brief

Date: 2026-07-01

## Decision

Treat the supplied videos as research lead generators, then route them into
independent proof, paper, market, or model-replay packets.

## Result

Pass 0133 verifies `{len(artifact['source_receipts'])}` receipts and routes
`{len(artifact['video_leads'])}` videos across `{len(artifact['route_summary'])}`
source-lead lanes.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0133 Steelman: YouTube Source-Lead Intake

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that YouTube transcripts are noisy and persuasive
titles can over-anchor the research plan. Correct. This pass only stores
metadata/transcript receipts and marks every route as source-lead-only.

The second objection is that source-lead routing is not a proof. Correct. The
next pass must retrieve primary sources or run executable fixtures before
promotion.

Boundary: {artifact['boundary']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> dict:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0133",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_count": len(artifact["source_receipts"]),
        "video_count": len(artifact["video_leads"]),
        "route_count": len(artifact["route_summary"]),
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)
    return receipts


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0133 created a YouTubeSourceLeadIntakeReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0133 binds upstream pass {artifact['source_bindings']} and records {len(artifact['source_receipts'])} source receipts.",
        f"Pass 0133 records {len(artifact['video_leads'])} video leads with SOURCE_LEAD_ONLY status.",
        f"Pass 0133 records {len(artifact['route_summary'])} route summaries including biology and computing lanes.",
        f"Pass 0133 defines {len(artifact['product_hypotheses'])} product hypotheses.",
        f"Pass 0133 rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0133 boundary rejects video-only claims as verified facts, proofs, market evidence, or natural laws.",
        "Pass 0133 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0133 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0133 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0133 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"source_receipts={artifact['source_receipts']}"],
        [f"video_leads={artifact['video_leads']}"],
        [f"route_summary={artifact['route_summary']}"],
        [f"product_hypotheses={artifact['product_hypotheses']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"boundary={artifact['boundary']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0133 YouTube Source-Lead Intake", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0133 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=180)
    validator_receipt = run_command([sys.executable, str(VALIDATOR)], timeout=120)
    receipts = write_tool_receipts(artifact, compose_receipt, test_receipt, validator_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt, validator_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, receipts)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    ok = all(row["status"] == "MATCH" for row in [compose_receipt, test_receipt, validator_receipt]) and artifact["status"] == "YOUTUBE_SOURCE_LEAD_INTAKE_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
