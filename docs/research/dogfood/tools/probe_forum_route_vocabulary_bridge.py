"""Generate pass 0058 receipts for the Forum route-vocabulary bridge."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


PASS = "0058"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_forum_route_vocabulary_bridge.py"
TEST_SCRIPT = ROOT / "tools" / "test_forum_route_vocabulary_bridge.py"
BRIEF = ROOT / "schemas" / "buyer-objection-brief-pass-0057.json"
RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0057.json"
OUT_PATH = ROOT / "schemas" / "forum-route-vocabulary-bridge-pass-0058.json"
PACKET_PATH = ROOT / "packets" / "068-forum-route-vocabulary-bridge.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0058-forum-route-vocabulary-bridge-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0058-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0058-measurements.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


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
    lane_rows = "\n".join(
        f"| `{row['lane_id']}` | {row['purpose']} | {', '.join(row['bridge_terms'][:4])} |"
        for row in packet["lane_taxonomy"]
    )
    gap_rows = "\n".join(
        f"| `{row['gap_id']}` | `{row['verification_status']}` | {row['gap']} |"
        for row in packet["integration_gaps"]
    )
    script = packet["buyer_discovery_script"]
    return f"""# Packet 068: Forum Route Vocabulary Bridge

Date: 2026-07-01

Status: `{packet['status']}`

Pass 0058 turns the pass 0057 buyer-objection brief into route vocabulary,
rewrite fixtures, and buyer-discovery prompts. It is an operator bridge, not a
Forum router patch.

```text
rewrite_fixture_count = {len(packet['rewrite_fixtures'])}
buyer_discovery_prompt_count = {script['prompt_count']}
source_objection_count = {script['source_objection_count']}
observed_forum_gap = {packet['observed_forum_gap']['status']}
ready_for_operator_use = {packet['route_readiness']['ready_for_operator_use']}
ready_for_forum_patch = {packet['route_readiness']['ready_for_forum_patch']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Lane Taxonomy

| Lane | Purpose | Bridge terms |
| --- | --- | --- |
{lane_rows}

## Integration Gaps

| Gap | Status | Description |
| --- | --- | --- |
{gap_rows}

Current promoted natural laws: none.
"""


def render_steelman(packet: dict) -> str:
    return f"""# Pass 0058 Steelman: Forum Route Vocabulary Bridge

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass does not patch Forum. It only creates deterministic prompts and a
split-lane bridge that an operator can use today. The bridge can still fail if
Forum's actual router remains single-lane, if market-research terms drift, or if
Forum submit remains unavailable.

The output is bounded as `{packet['market_claim_boundary']}` and promotes no
natural laws.
"""


def build_thesis_measurements(packet: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    claims = [
        f"Pass 0058 created a ForumRouteVocabularyBridge/v1 artifact with status {packet['status']}, rewrite_fixture_count {len(packet['rewrite_fixtures'])}, buyer_discovery_prompt_count {packet['buyer_discovery_script']['prompt_count']}, sha256 {shas['artifact']}, and seal {packet['seal']}.",
        f"Pass 0058 implements compose_forum_route_vocabulary_bridge.py with sha256 {shas['composer']} and compose_receipt status {compose_receipt['status']}.",
        f"Pass 0058 records a route bridge test script with sha256 {shas['test']} and test_receipt status {test_receipt['status']}.",
        f"Pass 0058 lane taxonomy contains project-telos, deep-research, and technical-writing with ready_for_operator_use {packet['route_readiness']['ready_for_operator_use']} and ready_for_forum_patch {packet['route_readiness']['ready_for_forum_patch']}.",
        f"Pass 0058 observed Forum gap status is {packet['observed_forum_gap']['status']} and upstream brief seal is {packet['upstream_brief']['seal']}.",
        f"Pass 0058 buyer discovery script has source_objection_count {packet['buyer_discovery_script']['source_objection_count']} and prompt_count {packet['buyer_discovery_script']['prompt_count']}.",
        f"Pass 0058 unsupported_claim_count is {packet['unsupported_claim_count']}, market_claim_boundary is {packet['market_claim_boundary']}, and current_promoted_natural_laws remains none.",
        f"Pass 0058 records packet 068 sha256 {shas['packet']} and steelman sha256 {shas['steelman']}.",
    ]
    evidence = [
        [f"schema={packet['schema']}", f"status={packet['status']}", f"rewrite_fixture_count={len(packet['rewrite_fixtures'])}", f"prompt_count={packet['buyer_discovery_script']['prompt_count']}", f"sha256={shas['artifact']}", f"seal={packet['seal']}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
        ["lane_ids=project-telos,deep-research,technical-writing", f"ready_for_operator_use={packet['route_readiness']['ready_for_operator_use']}", f"ready_for_forum_patch={packet['route_readiness']['ready_for_forum_patch']}"],
        [f"observed_forum_gap={packet['observed_forum_gap']['status']}", f"upstream_brief_seal={packet['upstream_brief']['seal']}"],
        [f"source_objection_count={packet['buyer_discovery_script']['source_objection_count']}", f"prompt_count={packet['buyer_discovery_script']['prompt_count']}"],
        [f"unsupported_claim_count={packet['unsupported_claim_count']}", f"market_claim_boundary={packet['market_claim_boundary']}", "current_promoted_natural_laws=[]"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}"],
    ]
    methods = ["artifact-schema-review", "composer-file-review", "composer-test-review", "lane-taxonomy-review", "forum-gap-binding-review", "discovery-script-review", "non-promotion-boundary-review", "packet-steelman-review"]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0058 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0058 Forum Route Vocabulary Bridge"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": methods[i], "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--brief", str(BRIEF), "--receipts", str(RECEIPTS), "--out", str(OUT_PATH)])
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
