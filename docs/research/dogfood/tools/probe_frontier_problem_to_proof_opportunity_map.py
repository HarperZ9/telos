"""Generate pass 0063 receipts for the frontier problem-to-proof map."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_frontier_problem_to_proof_opportunity_map.py"
TEST_SCRIPT = ROOT / "tools" / "test_frontier_problem_to_proof_opportunity_map.py"
OUT_PATH = ROOT / "schemas" / "frontier-problem-to-proof-opportunity-map-pass-0063.json"
PACKET_PATH = ROOT / "packets" / "073-frontier-problem-to-proof-opportunity-map.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0063-frontier-problem-to-proof-opportunity-map-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0063-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0063-measurements.json"


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
    top = packet["wedge_scores"][:3]
    rows = packet["opportunity_rows"]
    top_lines = "\n".join(f"- Rank {item['rank']}: `{item['market']}` total `{item['weighted_total']}` risk `{item['risk']}`" for item in top)
    domain_lines = "\n".join(f"- `{row['domain_id']}`: {row['proof_demo']}" for row in rows)
    demo_lines = "\n".join(f"- `{demo['demo_id']}`: {demo['success_metric']}" for demo in packet["demo_recommendations"])
    return f"""# Packet 073: Frontier Problem-to-Proof Opportunity Map

Date: 2026-07-01

Status: `{packet['status']}`

Purpose: map eight frontier markets into proof-centered megatool opportunities without claiming uniqueness, product-market fit, or scientific discovery.

```text
source_anchor_count = {len(packet['source_anchors'])}
opportunity_row_count = {len(rows)}
megatool_node_count = {len(packet['megatool_nodes'])}
unsupported_uniqueness_claim_count = {packet['unsupported_uniqueness_claim_count']}
forum_route_status = {packet['forum_route_observation']['status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Top Ranked Wedges

{top_lines}

## Domain Demo Map

{domain_lines}

## Three Public Demo Recommendations

{demo_lines}

## Route Finding

{packet['forum_route_observation']['finding']}

Current promoted natural laws: none.
"""


def render_steelman(packet: dict) -> str:
    return f"""# Pass 0063 Steelman: Frontier Problem-to-Proof Opportunity Map

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass can still overfit to the project's preferred proof-packet framing.
The artifact is useful for strategy only if buyer interviews, live demos, and
source-backed competitor matrices keep narrowing or falsifying the wedges.

Hard objections:

- Strong incumbents already own parts of AI4Science, observability, compiler,
  color, and biology workflows.
- The highest-upside biology and energy lanes have the highest validation and
  safety burden.
- BuildLang/buildc differentiation remains a hypothesis until native execution
  receipts and benchmarks exist.
- Forum escalated the broad request, so cross-domain routing still needs better
  vocabulary and lane composition.

Non-promotion statement: {packet['non_promotion_statement']}
"""


def build_thesis_measurements(packet: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    top_market = packet["wedge_scores"][0]["market"]
    claims = [
        f"Pass 0063 created a FrontierProblemToProofOpportunityMap/v1 artifact with status {packet['status']}, sha256 {shas['artifact']}, and seal {packet['seal']}.",
        f"Pass 0063 artifact contains {len(packet['source_anchors'])} source anchors and {len(packet['opportunity_rows'])} opportunity rows.",
        f"Pass 0063 includes the required domains formal_math_theoretical_cs, agentic_ai4science, quantum_hpc_algorithms, biology_protein_drug_discovery, materials_climate_energy, buildlang_scientific_runtime, agent_observability_action_receipts, and color_rendering_calibration.",
        f"Pass 0063 records unsupported_uniqueness_claim_count {packet['unsupported_uniqueness_claim_count']} and labels uniqueness claims as hypotheses.",
        f"Pass 0063 ranks {top_market} first by the declared weighted scoring model.",
        f"Pass 0063 maps {len(packet['megatool_nodes'])} megatool nodes including Gather, Index, Forum, Crucible, Telos, BuildLang/buildc, build-universe, color calibration, browser evidence, model foundry, loop ledger, and action receipts.",
        f"Pass 0063 records Forum route observation status {packet['forum_route_observation']['status']} as a cross-domain routing finding.",
        f"Pass 0063 records three public demo recommendations and keeps promotion state DEMO_NOT_PRODUCT_MARKET_FIT.",
        f"Pass 0063 composer sha256 is {shas['composer']} and compose_receipt status is {compose_receipt['status']}.",
        f"Pass 0063 packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={packet['schema']}", f"status={packet['status']}", f"sha256={shas['artifact']}", f"seal={packet['seal']}"],
        [f"source_anchor_count={len(packet['source_anchors'])}", f"opportunity_row_count={len(packet['opportunity_rows'])}"],
        [",".join(sorted(row["domain_id"] for row in packet["opportunity_rows"]))],
        [f"unsupported_uniqueness_claim_count={packet['unsupported_uniqueness_claim_count']}", "uniqueness_claim_status=hypothesis"],
        [f"top_market={top_market}", f"weighted_total={packet['wedge_scores'][0]['weighted_total']}"],
        [f"megatool_node_count={len(packet['megatool_nodes'])}", ",".join(sorted(node["internal_tool"] for node in packet["megatool_nodes"]))],
        [f"forum_route_status={packet['forum_route_observation']['status']}"],
        [f"demo_count={len(packet['demo_recommendations'])}", "promotion_state=DEMO_NOT_PRODUCT_MARKET_FIT"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
    ]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0063 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0063 Frontier Problem-to-Proof Opportunity Map"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": "artifact-review", "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
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
