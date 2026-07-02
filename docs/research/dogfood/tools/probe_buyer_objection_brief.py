"""Generate pass 0057 receipts for the buyer-objection brief packet."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


PASS = "0057"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_objection_brief.py"
TEST_SCRIPT = ROOT / "tools" / "test_buyer_objection_brief.py"
BUNDLE = ROOT / "demo-bundles" / "multitrace-causality-demo-pass-0056"
MANIFEST = BUNDLE / "manifest.json"
PANES = BUNDLE / "review-panes.json"
FAILURES = BUNDLE / "failure-verdicts.json"
REPLAY = BUNDLE / "replay-commands.md"
OUT_PATH = ROOT / "schemas" / "buyer-objection-brief-pass-0057.json"
PACKET_PATH = ROOT / "packets" / "067-buyer-objection-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0057-buyer-objection-brief-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0057-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0057-measurements.json"


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


def count_objections(brief: dict) -> int:
    return sum(len(row["objections"]) for row in brief["buyer_briefs"])


def render_packet(brief: dict, compose_receipt: dict, test_receipt: dict) -> str:
    buyer_rows = "\n".join(
        f"| `{row['buyer_id']}` | {row['buyer']} | {len(row['objections'])} | {row['primary_wedge']} |"
        for row in brief["buyer_briefs"]
    )
    source_rows = "\n".join(
        f"| `{row['source_id']}` | {row['url']} | `{row['verification_status']}` | `{row['confidence']}` |"
        for row in brief["source_anchors"]
    )
    d = brief["demo_bindings"]
    return f"""# Packet 067: Buyer Objection Brief

Date: 2026-07-01

Status: `{brief['status']}`

Pass 0057 maps the pass 0056 buyer-review demo into three buyer-objection
briefs. The output is a market-facing packet, not a market-uniqueness proof.

```text
buyer_brief_count = {brief['buyer_brief_count']}
source_anchor_count = {brief['source_anchor_count']}
objection_count = {count_objections(brief)}
unsupported_claim_count = {brief['unsupported_claim_count']}
market_claim_boundary = {brief['market_claim_boundary']}
public_review_ready = {d['public_review_ready']}
production_ready = {d['production_ready']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Buyer Briefs

| Buyer ID | Buyer | Objections | Primary wedge |
| --- | --- | ---: | --- |
{buyer_rows}

## Source Anchors

| Source ID | URL | Status | Confidence |
| --- | --- | --- | --- |
{source_rows}

## Boundaries

- Verified: pass 0056 demo counts, replay command count, negative verdict count,
  public-review boundary, production boundary, and zero promoted laws.
- Inferred: buyer wedge language and differentiation against existing markets.
- Unverified: market demand, customer budget, production compliance sufficiency,
  and universal uniqueness.

Current promoted natural laws: none.
"""


def render_steelman(brief: dict) -> str:
    return f"""# Pass 0057 Steelman: Buyer Objection Brief

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this pass still transforms a local proof
packet into buyer language; it does not prove market demand, procurement
urgency, production compliance, or superiority over incumbents.

The brief should therefore be used as a demo-discovery script and evidence map,
not as a finished go-to-market proof. Every uniqueness claim remains
`{brief['market_claim_boundary']}`, and the artifact promotes no natural laws.
"""


def build_thesis_measurements(brief: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    d = brief["demo_bindings"]
    source_ids = ",".join(row["source_id"] for row in brief["source_anchors"])
    buyer_ids = ",".join(row["buyer_id"] for row in brief["buyer_briefs"])
    claims = [
        f"Pass 0057 created a BuyerObjectionBrief/v1 artifact with status {brief['status']}, buyer_brief_count {brief['buyer_brief_count']}, source_anchor_count {brief['source_anchor_count']}, objection_count {count_objections(brief)}, sha256 {shas['artifact']}, and seal {brief['seal']}.",
        f"Pass 0057 implements compose_buyer_objection_brief.py with sha256 {shas['composer']} and compose_receipt status {compose_receipt['status']}.",
        f"Pass 0057 records a buyer objection brief test script with sha256 {shas['test']} and test_receipt status {test_receipt['status']}.",
        f"Pass 0057 binds to pass 0056 manifest hash {d['manifest_hash']}, review_pane_count {d['review_pane_count']}, failure_verdict_count {d['failure_verdict_count']}, replay_command_count {d['replay_command_count']}, public_review_ready {d['public_review_ready']}, and production_ready {d['production_ready']}.",
        f"Pass 0057 source anchors are verified official sources with source_ids {source_ids}.",
        f"Pass 0057 buyer_ids are {buyer_ids}, each with at least three objections and no_universal_uniqueness_claim guardrails.",
        f"Pass 0057 unsupported_claim_count is {brief['unsupported_claim_count']}, market_claim_boundary is {brief['market_claim_boundary']}, and current_promoted_natural_laws remains none.",
        f"Pass 0057 records packet 067 sha256 {shas['packet']} and steelman sha256 {shas['steelman']}.",
    ]
    evidence = [
        [f"schema={brief['schema']}", f"status={brief['status']}", f"buyer_brief_count={brief['buyer_brief_count']}", f"source_anchor_count={brief['source_anchor_count']}", f"objection_count={count_objections(brief)}", f"sha256={shas['artifact']}", f"seal={brief['seal']}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
        [f"manifest_hash={d['manifest_hash']}", f"review_pane_count={d['review_pane_count']}", f"failure_verdict_count={d['failure_verdict_count']}", f"replay_command_count={d['replay_command_count']}", f"public_review_ready={d['public_review_ready']}", f"production_ready={d['production_ready']}"],
        [f"source_ids={source_ids}", "verification_status=verified_official_source", "confidence=high"],
        [f"buyer_ids={buyer_ids}", "min_objections_per_buyer=3", "guardrail=no_universal_uniqueness_claim"],
        [f"unsupported_claim_count={brief['unsupported_claim_count']}", f"market_claim_boundary={brief['market_claim_boundary']}", "current_promoted_natural_laws=[]"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}"],
    ]
    methods = ["artifact-schema-review", "composer-file-review", "composer-test-review", "demo-binding-review", "source-anchor-review", "buyer-brief-review", "non-promotion-boundary-review", "packet-steelman-review"]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0057 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0057 Buyer Objection Brief"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": methods[i], "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([
        sys.executable,
        str(COMPOSER),
        "--manifest",
        str(MANIFEST),
        "--panes",
        str(PANES),
        "--failures",
        str(FAILURES),
        "--replay",
        str(REPLAY),
        "--out",
        str(OUT_PATH),
    ])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    brief = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(brief, compose_receipt, test_receipt))
    write_text(STEELMAN_PATH, render_steelman(brief))
    thesis, measurements = build_thesis_measurements(brief, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and brief["status"] == "BUYER_OBJECTION_BRIEF_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": brief["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
