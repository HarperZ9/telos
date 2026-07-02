"""Generate pass 0083 Forum proof-lane vocabulary repair artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_forum_proof_lane_vocabulary_repair.py"
TEST_SCRIPT = ROOT / "tools" / "test_forum_proof_lane_vocabulary_repair.py"
OUT_PATH = ROOT / "schemas" / "forum-proof-lane-vocabulary-repair-pass-0083.json"
PACKET_PATH = ROOT / "packets" / "093-forum-proof-lane-vocabulary-repair.md"
BRIEF_PATH = ROOT / "briefs" / "093-forum-proof-lane-repair-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0083-forum-proof-lane-vocabulary-repair-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0083-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0083-measurements.json"


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
    summary = artifact["repair_summary"]
    persistent = ", ".join(summary["persistent_escalation_lanes"]) or "none"
    return f"""# Packet 093: Forum Proof-Lane Vocabulary Repair

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: test whether explicit proof-packet vocabulary and a Project Telos
primary owner reduces the route escalations observed in pass 0082.

```text
baseline_non_escalated = {artifact['baseline']['non_escalated_count']}
repaired_non_escalated = {summary['non_escalated_count']}
improvement = {summary['improvement_over_baseline']}
persistent_escalations = {persistent}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

Boundary: this pass is a prompt-level bridge and taxonomy proposal. It does not
patch Forum source code or prove all routes are fixed.
"""


def render_brief(artifact: dict) -> str:
    summary = artifact["repair_summary"]
    caveat = artifact["repair_caveats"][0]["caveat"]
    return f"""# Forum Proof-Lane Repair Brief

Date: 2026-07-01

## Result

Forum proof-lane bridge prompts moved non-escalated routes from
{artifact['baseline']['non_escalated_count']} to {summary['non_escalated_count']}
out of {summary['route_probe_count']}.

## Remaining Work

Package ecosystem and world-scale strategy still need explicit ownership:
package work should split `sdk-platform` / `ci-cd` / `project-telos`, while
world-scale work should decompose into narrower proof-packet lanes.

Main caveat: {caveat}
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0083 Steelman: Forum Proof-Lane Vocabulary Repair

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The repair works by making the prompt easier for Forum, not by changing Forum's
native routing model. That is still useful because it identifies terms that
should become real lane vocabulary, but it is not a production patch.

Persistent escalations are more important than the improvement: they show where
package ownership and world-scale decomposition need separate routing contracts.

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
    summary = artifact["repair_summary"]
    claims = [
        f"Pass 0083 created a ForumProofLaneVocabularyRepair/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0083 compares against pass 0082 baseline with {artifact['baseline']['non_escalated_count']} non-escalated routes and {artifact['baseline']['escalation_count']} escalated routes.",
        f"Pass 0083 repaired routes produced {summary['non_escalated_count']} non-escalated routes, {summary['escalation_count']} escalated routes, and improvement_over_baseline {summary['improvement_over_baseline']}.",
        f"Pass 0083 records {len(artifact['taxonomy_patch_candidates'])} taxonomy patch candidates, {len(artifact['remaining_gaps'])} remaining route gaps, and {len(artifact['repair_caveats'])} repair caveats.",
        f"Pass 0083 contains {len(artifact['negative_fixtures'])} negative fixtures, unsupported_claim_count {artifact['unsupported_claim_count']}, and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0083 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"baseline_source={artifact['baseline']['source_path']}", f"baseline_non_escalated={artifact['baseline']['non_escalated_count']}", f"baseline_escalations={artifact['baseline']['escalation_count']}"],
        [f"repaired_non_escalated={summary['non_escalated_count']}", f"repaired_escalations={summary['escalation_count']}", f"improvement={summary['improvement_over_baseline']}"],
        [f"taxonomy_patch_candidates={len(artifact['taxonomy_patch_candidates'])}", f"remaining_gaps={len(artifact['remaining_gaps'])}", f"repair_caveats={len(artifact['repair_caveats'])}", f"persistent={summary['persistent_escalation_lanes']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0083 Forum Proof Lane Vocabulary Repair", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0083 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "FORUM_PROOF_LANE_VOCABULARY_REPAIR_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
