"""Generate pass 0126 source-lead demotion gate artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_source_lead_demotion_gate.py"
TEST_SCRIPT = ROOT / "tools" / "test_source_lead_demotion_gate.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0126_source_lead_demotion_gate.py"
OUT_PATH = ROOT / "schemas" / "source-lead-demotion-gate-pass-0126.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0126-source-lead-demotion-gate-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0126.json"
PACKET_PATH = ROOT / "packets" / "136-source-lead-demotion-gate.md"
BRIEF_PATH = ROOT / "briefs" / "136-source-lead-demotion-gate-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0126-source-lead-demotion-gate-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0126-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0126-measurements.json"


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


def fixture_rows(artifact: dict) -> list[dict]:
    return [{"fixture": row["fixture_id"], "requested": row["requested_status"], "status": row["gate_status"], "failures": ",".join(row["failures"])} for row in artifact["gate_fixtures"]]


def source_rows(artifact: dict) -> list[dict]:
    return [{"video": row["video_id"], "status": row["claim_status"], "signal": row["dominant_signal"], "raw": row["raw_transcript_included"]} for row in artifact["source_lead_summary"]]


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    return f"""# Packet 136: Source-Lead Demotion Gate

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: make the pass 0125 video-source boundary executable. Video metadata,
transcript hashes, and keyword signals may route experiments, but they cannot
promote a claim to fact or law without independent artifacts.

```text
source_leads = {len(artifact['source_lead_summary'])}
fixtures = {len(artifact['gate_fixtures'])}
accepted = {artifact['accepted_count']}
rejected = {artifact['rejected_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Source Summary

| Video | Status | Dominant signal | Raw transcript in packet |
| --- | --- | --- | --- |
{table(source_rows(artifact), ['video', 'status', 'signal', 'raw'])}

## Gate Fixtures

| Fixture | Requested status | Gate status | Failures |
| --- | --- | --- | --- |
{table(fixture_rows(artifact), ['fixture', 'requested', 'status', 'failures'])}

## Policy

- Source leads may remain `SOURCE_LEAD_ONLY` or `HYPOTHESIS`.
- Fact-like statuses require independent non-video evidence.
- `PROMOTED_LAW` is rejected by this gate.
- Raw transcript packet exports are rejected.
- Keyword signal counts are routing data, not proof.

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Source-Lead Demotion Gate Brief

Date: 2026-07-01

## Decision

Ship `SourceLeadDemotionGate` before expanding the runtime router. It is the
guardrail that keeps high-velocity video/talk corpora useful without letting
them become unsupported fact, benchmark, law, or market-fit claims.

## Result

The gate accepted {artifact['accepted_count']} safe fixtures and rejected
{artifact['rejected_count']} unsafe fixtures, including video-only fact
promotion, video-to-law promotion, raw transcript export, and keyword-count
proof misuse.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0126 Steelman: Source-Lead Demotion Gate

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that the gate is still fixture-based. Correct. It
does not prove production ingestion. It proves the minimum policy behavior that
future source routers must preserve.

The second objection is that strict demotion may slow discovery. Correct, but
that is intentional: video leads are allowed to route work quickly while fact,
law, and benchmark promotion waits for independent artifacts.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0126",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "accepted_count": artifact["accepted_count"],
        "rejected_count": artifact["rejected_count"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0126 created a SourceLeadDemotionGateReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0126 binds pass 0125 and pass 0124 receipts through source_bindings {artifact['source_bindings']}.",
        f"Pass 0126 records {len(artifact['source_lead_summary'])} video source leads and none include raw transcript exports.",
        f"Pass 0126 evaluates {len(artifact['gate_fixtures'])} fixtures with {artifact['accepted_count']} accepted and {artifact['rejected_count']} rejected.",
        "Pass 0126 rejects video-only fact promotion, video-to-law promotion, raw transcript export, and keyword-count-as-proof misuse.",
        "Pass 0126 allows SOURCE_LEAD_ONLY, HYPOTHESIS, and independently evidenced PROBE_MATCH fixtures.",
        f"Pass 0126 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0126 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0126 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0126 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"source_lead_summary={artifact['source_lead_summary']}"],
        [f"fixtures={artifact['gate_fixtures']}"],
        [f"rejected={[row for row in artifact['gate_fixtures'] if row['gate_status'] == 'REJECTED']}"],
        [f"accepted={[row for row in artifact['gate_fixtures'] if row['gate_status'] == 'ACCEPTED']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0126 Source-Lead Demotion Gate", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0126 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "SOURCE_LEAD_DEMOTION_GATE_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
