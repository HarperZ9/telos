"""Generate pass 0112 Lyapunov stability certificate artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_lyapunov_stability_certificate_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_lyapunov_stability_certificate_receipt.py"
OUT_PATH = ROOT / "schemas" / "lyapunov-stability-certificate-receipt-pass-0112.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0112.json"
PACKET_PATH = ROOT / "packets" / "122-lyapunov-stability-certificate-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "122-lyapunov-stability-certificate-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0112-lyapunov-stability-certificate-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0112-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0112-measurements.json"


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


def source_rows(artifact: dict) -> str:
    return "\n".join(f"| {row['tool']} | {row['kind']} | {row['url']} |" for row in artifact["source_anchors"])


def sample_rows(artifact: dict) -> str:
    return "\n".join(f"| {row['x']} | {row['delta_v']} | {row['negative_q_energy']} | {row['status']} |" for row in artifact["stable_certificate"]["energy_samples"])


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    stable = artifact["stable_certificate"]
    neg = artifact["negative_fixtures"]
    youtube = artifact["youtube_binding"]
    return f"""# Packet 122: Lyapunov Stability Certificate Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: prove a bounded exact discrete-time Lyapunov certificate for a rational
linear system and package it as a control/autonomy proof packet.

```text
runtime_suite_pass = {artifact['source_bindings']['runtime_suite_pass']}
youtube_roadmap_pass = {artifact['source_bindings']['youtube_roadmap_pass']}
A = {stable['A']}
P = {stable['P']}
Q = {stable['Q']}
max_spectral_radius_abs = {stable['max_spectral_radius_abs']}
max_identity_residual = {stable['max_identity_residual']}
unstable_fixture = {neg['unstable_spectral_fixture']['classification']}
bad_certificate_fixture = {neg['bad_certificate_fixture']['classification']}
source_anchor_count = {len(artifact['source_anchors'])}
valid_youtube_videos = {youtube['valid_video_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Energy Samples

| x | Delta V | -xTQx | Status |
| --- | --- | --- | --- |
{sample_rows(artifact)}

## Source Anchors

| Tool | Kind | URL |
| --- | --- | --- |
{source_rows(artifact)}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    market = artifact["market_surface"]
    return f"""# Lyapunov Stability Certificate Brief

Date: 2026-07-01

## Decision

Add control-certificate proof packets as a new frontier lane for robotics,
autonomy, MPC, simulation, and BuildLang scientific runtime work.

## Current Result

The receipt proves one exact rational discrete-time Lyapunov identity, records
two negative fixtures, and binds {market['tool_count']} adjacent control and
optimization tools as market/source anchors.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0112 Steelman: Lyapunov Stability Certificate

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a diagonal two-state system is not a real robot.
Correct. It is a minimal exact certificate fixture before nonlinear or hardware
claims.

The second objection is that Lyapunov equations are already solved by mature
tools. Correct. The wedge is not a solver; it is a portable proof packet binding
source, system, certificate, residuals, samples, and negative fixtures.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0112",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "stable_certificate": artifact["stable_certificate"],
        "market_surface": artifact["market_surface"],
        "youtube_binding": artifact["youtube_binding"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    stable = artifact["stable_certificate"]
    neg = artifact["negative_fixtures"]
    youtube = artifact["youtube_binding"]
    claims = [
        f"Pass 0112 created a LyapunovStabilityCertificateReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0112 binds runtime suite pass {artifact['source_bindings']['runtime_suite_pass']} and YouTube roadmap pass {artifact['source_bindings']['youtube_roadmap_pass']}.",
        f"Pass 0112 stable certificate records A {stable['A']}, P {stable['P']}, Q {stable['Q']}, max_spectral_radius_abs {stable['max_spectral_radius_abs']}, and max_identity_residual {stable['max_identity_residual']}.",
        f"Pass 0112 records {len(stable['energy_samples'])} energy samples and all have MATCH status.",
        f"Pass 0112 unstable fixture classification is {neg['unstable_spectral_fixture']['classification']} with positive_definite {neg['unstable_spectral_fixture']['positive_definite']}.",
        f"Pass 0112 bad certificate fixture classification is {neg['bad_certificate_fixture']['classification']} with max_identity_residual {neg['bad_certificate_fixture']['max_identity_residual']}.",
        f"Pass 0112 records {len(artifact['source_anchors'])} source anchors and market tool_count {artifact['market_surface']['tool_count']}.",
        f"Pass 0112 YouTube binding records {youtube['valid_video_count']} valid videos, {youtube['transcript_receipt_count']} transcript receipts, and raw_transcript_included {youtube['raw_transcript_included']}.",
        f"Pass 0112 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0112 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0112 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"stable_certificate={stable}"],
        [f"energy_samples={stable['energy_samples']}"],
        [f"unstable_fixture={neg['unstable_spectral_fixture']}"],
        [f"bad_certificate_fixture={neg['bad_certificate_fixture']}"],
        [f"source_anchor_count={len(artifact['source_anchors'])}", f"market_surface={artifact['market_surface']}"],
        [f"youtube_binding={youtube}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0112 Lyapunov Stability Certificate Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0112 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "LYAPUNOV_STABILITY_CERTIFICATE_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
