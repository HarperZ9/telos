"""Generate pass 0084 Forum native lane-fixture proposal artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_forum_native_lane_fixture_proposal.py"
TEST_SCRIPT = ROOT / "tools" / "test_forum_native_lane_fixture_proposal.py"
OUT_PATH = ROOT / "schemas" / "forum-native-lane-fixture-proposal-pass-0084.json"
PACKET_PATH = ROOT / "packets" / "094-forum-native-lane-fixture-proposal.md"
BRIEF_PATH = ROOT / "briefs" / "094-forum-native-lane-fixture-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0084-forum-native-lane-fixture-proposal-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0084-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0084-measurements.json"


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


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    results = artifact["route_test_results"]
    return f"""# Packet 094: Forum Native Lane-Fixture Proposal

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: convert the pass 0083 prompt bridge into native Forum lane fixtures
with primary owners, proof owners, domain handoffs, and over-routing tests.

```text
lane_fixtures = {len(artifact['lane_fixtures'])}
positive_matches = {results['positive_match']} / {results['positive_count']}
negative_matches = {results['negative_match']} / {results['negative_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

Boundary: this is a fixture proposal, not a Forum source patch or production
routing claim.
"""


def render_brief(artifact: dict) -> str:
    return f"""# Forum Native Lane-Fixture Brief

Date: 2026-07-01

## Proposal

Add native Forum route fixtures for proof-packet lanes. Each route should emit
`primary_owner`, `proof_owner`, `domain_handoff`, confidence, escalation status,
and rationale terms.

## Gate

The proposed fixture suite passes {artifact['route_test_results']['positive_match']}
positive lane tests and {artifact['route_test_results']['negative_match']}
over-routing negative tests. Production claims remain blocked until Forum source
or catalog metadata implements the proposal.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0084 Steelman: Forum Native Lane-Fixture Proposal

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The proposal is still a local matcher and fixture contract. It proves the shape
of the patch, not that Forum's production route engine has changed. The valuable
part is the negative suite: generic compiler, render, CI, market, and SDK tasks
must not over-route to project-telos merely because Project Telos exists.

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
    results = artifact["route_test_results"]
    claims = [
        f"Pass 0084 created a ForumNativeLaneFixtureProposal/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0084 binds upstream pass 0083 with sha256 {artifact['upstream']['sha256']} and seal {artifact['upstream']['seal']}.",
        f"Pass 0084 defines {len(artifact['lane_fixtures'])} lane fixtures with primary owner, proof owner, and handoff fields.",
        f"Pass 0084 route fixture tests matched {results['positive_match']} of {results['positive_count']} positive tests and {results['negative_match']} of {results['negative_count']} negative tests.",
        f"Pass 0084 contains unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0084 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"upstream_path={artifact['upstream']['path']}", f"upstream_sha256={artifact['upstream']['sha256']}", f"upstream_seal={artifact['upstream']['seal']}"],
        [f"lane_fixture_count={len(artifact['lane_fixtures'])}", "required_output_fields=primary_owner,proof_owner,domain_handoff"],
        [f"positive_match={results['positive_match']}", f"positive_count={results['positive_count']}", f"negative_match={results['negative_match']}", f"negative_count={results['negative_count']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0084 Forum Native Lane Fixture Proposal", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0084 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "FORUM_NATIVE_LANE_FIXTURE_PROPOSAL_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
