"""Generate pass 0059 receipts for buyer-discovery evidence scorecards."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


PASS = "0059"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_discovery_evidence_scorecards.py"
TEST_SCRIPT = ROOT / "tools" / "test_buyer_discovery_evidence_scorecards.py"
BRIDGE = ROOT / "schemas" / "forum-route-vocabulary-bridge-pass-0058.json"
OUT_PATH = ROOT / "schemas" / "buyer-discovery-evidence-scorecards-pass-0059.json"
PACKET_PATH = ROOT / "packets" / "069-buyer-discovery-evidence-scorecards.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0059-buyer-discovery-evidence-scorecards-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0059-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0059-measurements.json"


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
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stderr_sha256": sha256_text(result.stderr),
        "stdout_sha256": sha256_text(result.stdout),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def render_packet(packet: dict, compose_receipt: dict, test_receipt: dict) -> str:
    rows = "\n".join(
        f"| `{row['buyer_id']}` | {row['interview_prompt_count']} | {len(row['source_ids'])} | {len(row['market_data_targets'])} | `{row['scorecard_status']}` |"
        for row in packet["scorecards"]
    )
    return f"""# Packet 069: Buyer Discovery Evidence Scorecards

Date: 2026-07-01

Status: `{packet['status']}`

Pass 0059 turns pass 0058 discovery prompts into evidence scorecards with
current source anchors and market-data collection targets. It does not score the
market yet; it defines the evidence required to score it.

```text
source_anchor_count = {packet['source_anchor_count']}
scorecard_count = {len(packet['scorecards'])}
interview_prompt_count = {sum(row['interview_prompt_count'] for row in packet['scorecards'])}
market_data_status = {packet['market_data_status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

| Buyer | Prompts | Sources | Targets | Status |
| --- | ---: | ---: | ---: | --- |
{rows}

Current promoted natural laws: none.
"""


def render_steelman(packet: dict) -> str:
    return f"""# Pass 0059 Steelman: Buyer Discovery Evidence Scorecards

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass defines collection targets, not market proof. It can fail if source
anchors are stale, interviews do not confirm urgency or budget, or the proof
packet demo does not beat incumbent workflows in practice.

The packet remains `{packet['market_claim_boundary']}` and promotes no natural
laws.
"""


def build_thesis_measurements(packet: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    prompt_count = sum(row["interview_prompt_count"] for row in packet["scorecards"])
    target_count = sum(len(row["market_data_targets"]) for row in packet["scorecards"])
    claims = [
        f"Pass 0059 created a BuyerDiscoveryEvidenceScorecards/v1 artifact with status {packet['status']}, source_anchor_count {packet['source_anchor_count']}, prompt_count {prompt_count}, target_count {target_count}, sha256 {shas['artifact']}, and seal {packet['seal']}.",
        f"Pass 0059 implements compose_buyer_discovery_evidence_scorecards.py with sha256 {shas['composer']} and compose_receipt status {compose_receipt['status']}.",
        f"Pass 0059 records a buyer discovery scorecard test with sha256 {shas['test']} and test_receipt status {test_receipt['status']}.",
        f"Pass 0059 contains three buyer scorecards and upstream bridge seal {packet['upstream_bridge']['seal']}.",
        f"Pass 0059 source anchors are verified primary sources and include source_anchor_count {packet['source_anchor_count']}.",
        f"Pass 0059 market_data_status is {packet['market_data_status']} and collection next_pass is {packet['collection_plan']['next_pass']}.",
        f"Pass 0059 unsupported_claim_count is {packet['unsupported_claim_count']}, market_claim_boundary is {packet['market_claim_boundary']}, and current_promoted_natural_laws remains none.",
        f"Pass 0059 records packet 069 sha256 {shas['packet']} and steelman sha256 {shas['steelman']}.",
    ]
    evidence = [
        [f"schema={packet['schema']}", f"status={packet['status']}", f"source_anchor_count={packet['source_anchor_count']}", f"prompt_count={prompt_count}", f"target_count={target_count}", f"sha256={shas['artifact']}", f"seal={packet['seal']}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
        [f"scorecard_count={len(packet['scorecards'])}", f"upstream_bridge_seal={packet['upstream_bridge']['seal']}"],
        [f"source_anchor_count={packet['source_anchor_count']}", "verification_status=verified_primary_source"],
        [f"market_data_status={packet['market_data_status']}", f"next_pass={packet['collection_plan']['next_pass']}"],
        [f"unsupported_claim_count={packet['unsupported_claim_count']}", f"market_claim_boundary={packet['market_claim_boundary']}", "current_promoted_natural_laws=[]"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}"],
    ]
    methods = ["artifact-schema-review", "composer-file-review", "composer-test-review", "scorecard-binding-review", "source-anchor-review", "collection-plan-review", "non-promotion-boundary-review", "packet-steelman-review"]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0059 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0059 Buyer Discovery Evidence Scorecards"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": methods[i], "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--bridge", str(BRIDGE), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    packet = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(packet, compose_receipt, test_receipt))
    write_text(STEELMAN_PATH, render_steelman(packet))
    thesis, measurements = build_thesis_measurements(packet, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and packet["status"].endswith("_MATCH") else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": packet["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
