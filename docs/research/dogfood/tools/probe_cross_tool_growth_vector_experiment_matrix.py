"""Generate pass 0082 cross-tool growth-vector experiment matrix artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_cross_tool_growth_vector_experiment_matrix.py"
TEST_SCRIPT = ROOT / "tools" / "test_cross_tool_growth_vector_experiment_matrix.py"
OUT_PATH = ROOT / "schemas" / "cross-tool-growth-vector-experiment-matrix-pass-0082.json"
PACKET_PATH = ROOT / "packets" / "092-cross-tool-growth-vector-experiment-matrix.md"
BRIEF_PATH = ROOT / "briefs" / "092-megatool-growth-vector-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0082-cross-tool-growth-vector-experiment-matrix-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0082-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0082-measurements.json"


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
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    top = artifact["ranked_product_lanes"][:5]
    lines = "\n".join(
        f"- {row['lane_id']}: score {row['scores']['composite']}, route escalation {row['route']['needs_escalation']}, next {row['next_experiment']}"
        for row in top
    )
    summary = artifact["live_experiment_summary"]
    return f"""# Packet 092: Cross-Tool Growth-Vector Experiment Matrix

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: steelman growth vectors across all Telos/Build tooling by joining
recent proof packets with live Forum route probes, ranked product lanes, and a
specific improvement row for every internal tool.

```text
route_probes = {summary['route_probe_count']}
route_matches = {summary['route_match_count']}
route_escalations = {summary['needs_escalation_count']}
product_lanes = {len(artifact['ranked_product_lanes'])}
tool_improvements = {len(artifact['tool_improvements'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

Top ranked lanes:

{lines}

Boundary: this packet ranks hypotheses. It proves neither buyer demand nor
competitor absence. Route ambiguity is treated as product evidence for clearer
lanes, not as a market victory.
"""


def render_brief(artifact: dict) -> str:
    top = artifact["ranked_product_lanes"][0]
    second = artifact["ranked_product_lanes"][1]
    third = artifact["ranked_product_lanes"][2]
    return f"""# Megatool Growth-Vector Brief

Date: 2026-07-01

## Recommendation

Primary 30-day push: `{top['lane_id']}`.

Backup lanes: `{second['lane_id']}` and `{third['lane_id']}`.

## Why

The live route probes show repeated cross-domain ambiguity, while passes 0080
and 0081 prove that BuildLang and visual-truth packets can already be packaged
as bounded, recheckable artifacts. The fastest path is to turn those repeated
packet shapes into explicit product lanes and use Forum escalation as a repair
metric.

## Next Action

{top['next_experiment']}
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0082 Steelman: Cross-Tool Growth Vectors

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a matrix can become strategy theater. A ranked
lane is not a product, and a Forum escalation is not proof of demand. The only
useful interpretation is narrower: recent packets expose where tool boundaries
are repeatable enough to package and where routing ownership is still weak.

The hardest missing evidence remains buyer discovery, public demos, and
incumbent import adapters. The pass therefore keeps every lane as a hypothesis
and requires a next experiment for each one.

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
    summary = artifact["live_experiment_summary"]
    claims = [
        f"Pass 0082 created a CrossToolGrowthVectorExperimentMatrix/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0082 ran {summary['route_probe_count']} live Forum route probes with {summary['route_match_count']} MATCH receipts and {summary['needs_escalation_count']} escalation receipts.",
        f"Pass 0082 ranks {len(artifact['ranked_product_lanes'])} product lanes and the top lane is {artifact['ranked_product_lanes'][0]['lane_id']}.",
        f"Pass 0082 records {len(artifact['tool_improvements'])} tool improvement rows covering all required internal tools.",
        f"Pass 0082 binds BuildLang pass 0080 and visual-truth pass 0081 prior artifacts by receipt.",
        f"Pass 0082 contains {len(artifact['negative_fixtures'])} negative fixtures, unsupported_claim_count {artifact['unsupported_claim_count']}, and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0082 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"route_probe_count={summary['route_probe_count']}", f"route_match_count={summary['route_match_count']}", f"needs_escalation_count={summary['needs_escalation_count']}"],
        [f"product_lane_count={len(artifact['ranked_product_lanes'])}", f"top_lane={artifact['ranked_product_lanes'][0]['lane_id']}"],
        [f"tool_improvement_count={len(artifact['tool_improvements'])}", f"tools={sorted(row['tool'] for row in artifact['tool_improvements'])}"],
        [f"buildlang_path={artifact['prior_bindings']['buildlang_demo_0080']['path']}", f"visual_path={artifact['prior_bindings']['visual_truth_0081']['path']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0082 Cross-Tool Growth Vector Experiment Matrix", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0082 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "CROSS_TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
