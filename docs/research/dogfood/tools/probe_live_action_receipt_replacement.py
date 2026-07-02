"""Generate pass 0070 receipts for live action-receipt replacement."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_live_action_receipt_replacement.py"
TEST_SCRIPT = ROOT / "tools" / "test_live_action_receipt_replacement.py"
OUT_PATH = ROOT / "schemas" / "live-action-receipt-replacement-pass-0070.json"
PACKET_PATH = ROOT / "packets" / "080-live-action-receipt-replacement.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0070-live-action-receipt-replacement-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0070-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0070-measurements.json"


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
    action = [row for row in artifact["component_receipts"] if row["kind"] == "action"][0]
    negatives = "\n".join(f"- `{row['fixture_id']}` -> `{row['reject_reason']}`" for row in artifact["negative_fixtures"])
    checks = "\n".join(f"- `{key}`: {value}" for key, value in artifact["action_surface_checks"]["checks"].items())
    return f"""# Packet 080: Live Action-Receipt Replacement

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: replace the pass 0069 synthetic action component with a live local
Telos action-receipt surface from `node demo/action-receipt.mjs`.

```text
live_surface_status = {artifact['live_surface']['status']}
required_field_count = {artifact['live_surface']['required_field_count']}
negative_test_count = {artifact['live_surface']['negative_test_count']}
action_component = {action['component_id']}
component_count = {len(artifact['component_receipts'])}
negative_fixture_count = {len(artifact['negative_fixtures'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Action Surface Checks

{checks}

## Negative Fixtures

{negatives}

Current promoted natural laws: none.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0070 Steelman: Live Action-Receipt Replacement

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass improves pass 0069 by replacing one synthetic component with a live
local Telos action-receipt fixture. It still does not prove append-only storage
in a production ledger, external write safety, or buyer adoption. The next
promotion should persist the receipt through the receptor/storage adapter or
replace another synthetic component with a live Gather/Index/Forum/Crucible
receipt while preserving all negative fixtures.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    action = [row for row in artifact["component_receipts"] if row["kind"] == "action"][0]
    claims = [
        f"Pass 0070 created a LiveActionReceiptReplacement/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0070 loaded live action surface command {artifact['live_surface']['command']} with status {artifact['live_surface']['status']} and schema {artifact['live_surface']['schema']}.",
        f"Pass 0070 action surface checks have match {artifact['action_surface_checks']['match']} and drift {artifact['action_surface_checks']['drift']}.",
        f"Pass 0070 replaced the action component with {action['component_id']} and digest {action['digest']}.",
        f"Pass 0070 product packet has component_count {artifact['product_packet']['component_count']} and unsupported_claim_count {artifact['product_packet']['unsupported_claim_count']}.",
        f"Pass 0070 contains {len(artifact['negative_fixtures'])} negative fixtures and {len(artifact['ablation_results'])} ablation results.",
        f"Pass 0070 composer sha256 is {shas['composer']} and compose_receipt status is {compose_receipt['status']}.",
        f"Pass 0070 packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"command={artifact['live_surface']['command']}", f"status={artifact['live_surface']['status']}", f"schema={artifact['live_surface']['schema']}"],
        [f"match={artifact['action_surface_checks']['match']}", f"drift={artifact['action_surface_checks']['drift']}"],
        [f"action_component={action['component_id']}", f"action_digest={action['digest']}"],
        [f"component_count={artifact['product_packet']['component_count']}", f"unsupported_claim_count={artifact['product_packet']['unsupported_claim_count']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"ablation_count={len(artifact['ablation_results'])}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0070 Live Action Receipt Replacement", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0070 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    artifact = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "LIVE_ACTION_RECEIPT_REPLACEMENT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
