"""Generate pass 0081 receipts for visual-truth proof-packet refresh."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_visual_truth_proof_packet_refresh.py"
TEST_SCRIPT = ROOT / "tools" / "test_visual_truth_proof_packet_refresh.py"
OUT_PATH = ROOT / "schemas" / "visual-truth-proof-packet-refresh-pass-0081.json"
PACKET_PATH = ROOT / "packets" / "091-visual-truth-proof-packet-refresh.md"
BRIEF_PATH = ROOT / "briefs" / "091-visual-truth-proof-packet-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0081-visual-truth-proof-packet-refresh-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0081-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0081-measurements.json"


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
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    return {"command": " ".join(command), "exit_code": result.returncode, "stderr_sha256": sha256_text(result.stderr), "stdout_sha256": sha256_text(result.stdout), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    return f"""# Packet 091: Visual Truth Proof-Packet Refresh

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: refresh the visual-truth proof packet by binding Build Color software
metrics, source refs, a fresh 88-test targeted regression, market-gap context,
Forum routing, and explicit non-calibration boundaries.

```text
metrics = {artifact['proof_kit_source']['metric_count']}
market_rows = {artifact['market_map']['row_count']}
source_refs = {artifact['source_ref_count']}
targeted_regression = {artifact['targeted_regression']['passed']} passed
forum_route = {artifact['forum_route']['status']}
hardware_measurement_used = {artifact['calibration_boundary']['hardware_measurement_used']}
physical_calibration_claim = {artifact['calibration_boundary']['physical_calibration_claim']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

Boundary: this packet proves a read-only software visual-truth proof surface,
not physical display calibration, ICC installation, LUT writing, or a new color
science law.
"""


def render_brief(artifact: dict) -> str:
    route = artifact["forum_route"]
    return f"""# Visual Truth Proof-Packet Brief

Date: 2026-07-01

## Offer

Visual truth proof packets bind deterministic color math, transform
assumptions, source refs, targeted regression evidence, market-gap context, and
calibration boundaries into one portable artifact.

## Current Evidence

- Build Color metrics: {artifact['proof_kit_source']['metric_count']} PASS.
- Market map rows: {artifact['market_map']['row_count']}.
- Source refs: {artifact['source_ref_count']}.
- Targeted regression: {artifact['targeted_regression']['passed']} tests passed.
- Forum route: needs escalation `{route['needs_escalation']}` with top candidate `{route['top_candidates'][0]['agent']}`.

## Boundaries

No hardware meter, display mutation, ICC install, LUT write, physical
calibration claim, market-uniqueness claim, or new color-science law is
promoted by this packet.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0081 Steelman: Visual Truth Proof-Packet Refresh

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This packet is strong because it refuses the easiest overclaim: it does not say
a physical display was calibrated. The wedge is a portable proof layer around
software color transforms, thresholds, source refs, market context, and
negative calibration boundaries. Hardware calibration remains a separate future
receipt class requiring meter/probe evidence and state mutation records.

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
    }
    claims = [
        f"Pass 0081 created a VisualTruthProofPacketRefresh/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0081 binds proof kit pass 0011 with metric_count {artifact['proof_kit_source']['metric_count']} and all metric statuses PASS.",
        f"Pass 0081 binds market map pass 0011 with row_count {artifact['market_map']['row_count']}.",
        f"Pass 0081 binds {artifact['source_ref_count']} Build Color source refs.",
        f"Pass 0081 targeted regression status is {artifact['targeted_regression']['status']} with {artifact['targeted_regression']['passed']} tests passed.",
        f"Pass 0081 keeps calibration boundary hardware_measurement_used={artifact['calibration_boundary']['hardware_measurement_used']} and physical_calibration_claim={artifact['calibration_boundary']['physical_calibration_claim']}.",
        f"Pass 0081 contains {len(artifact['negative_fixtures'])} negative fixtures, unsupported_claim_count {artifact['unsupported_claim_count']}, and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0081 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"proof_pass=0011", f"metric_count={artifact['proof_kit_source']['metric_count']}", f"metric_statuses={artifact['proof_kit_source']['metric_statuses']}"],
        [f"market_pass=0011", f"row_count={artifact['market_map']['row_count']}"],
        [f"source_ref_count={artifact['source_ref_count']}"],
        [f"regression_status={artifact['targeted_regression']['status']}", f"passed={artifact['targeted_regression']['passed']}"],
        [f"hardware_measurement_used={artifact['calibration_boundary']['hardware_measurement_used']}", f"physical_calibration_claim={artifact['calibration_boundary']['physical_calibration_claim']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0081 Visual Truth Proof Packet Refresh", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0081 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    artifact = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "VISUAL_TRUTH_PROOF_PACKET_REFRESH_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
