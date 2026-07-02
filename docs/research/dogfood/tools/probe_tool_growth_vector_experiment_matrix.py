"""Generate pass 0066 receipts for the tool growth-vector experiment matrix."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_tool_growth_vector_experiment_matrix.py"
TEST_SCRIPT = ROOT / "tools" / "test_tool_growth_vector_experiment_matrix.py"
OUT_PATH = ROOT / "schemas" / "tool-growth-vector-experiment-matrix-pass-0066.json"
PACKET_PATH = ROOT / "packets" / "076-tool-growth-vector-experiment-matrix.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0066-tool-growth-vector-experiment-matrix-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0066-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0066-measurements.json"


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


def render_packet(packet: dict, compose_receipt: dict, test_receipt: dict) -> str:
    top_nodes = ", ".join(packet["synergy_graph"]["top_nodes"])
    bundles = "\n".join(f"- `{row['bundle_id']}`: {row['market']} via {', '.join(row['tools'])}" for row in packet["top_growth_bundles"])
    experiments = "\n".join(f"- `{row['experiment_id']}` -> `{row['expected_receipt']}`" for row in packet["cross_tool_experiments"])
    return f"""# Packet 076: Tool Growth-Vector Experiment Matrix

Date: 2026-07-01

Status: `{packet['status']}`

Purpose: pressure-test growth vectors across the Telos/Build substrate instead of optimizing one tool in isolation.

```text
internal_tool_count = {len(packet['internal_tools'])}
source_anchor_count = {len(packet['source_anchors'])}
growth_vector_count = {len(packet['growth_vectors'])}
cross_tool_experiment_count = {len(packet['cross_tool_experiments'])}
top_synergy_nodes = {top_nodes}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Top Growth Bundles

{bundles}

## Cross-Tool Experiments

{experiments}

Current promoted natural laws: none.
"""


def render_steelman(packet: dict) -> str:
    return f"""# Pass 0066 Steelman: Tool Growth-Vector Experiment Matrix

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass scores and organizes experiments; it does not prove that the
experiments will win markets or that the tools are technically complete. The
strongest objection is that a matrix can feel rigorous while still avoiding
hard integration work. The next passes should promote only rows that become
executable adapters, benchmarks, buyer interviews, or mathematical proof
packets with failing negative fixtures.

Non-promotion statement: {packet['non_promotion_statement']}
"""


def build_thesis_measurements(packet: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    centrality = packet["synergy_graph"]["centrality"]
    claims = [
        f"Pass 0066 created a ToolGrowthVectorExperimentMatrix/v1 artifact with status {packet['status']}, sha256 {shas['artifact']}, and seal {packet['seal']}.",
        f"Pass 0066 contains {len(packet['internal_tools'])} internal tools, {len(packet['source_anchors'])} source anchors, and {len(packet['growth_vectors'])} growth vectors.",
        f"Pass 0066 contains {len(packet['cross_tool_experiments'])} cross-tool experiments and top bundle {packet['top_growth_bundles'][0]['bundle_id']}.",
        f"Pass 0066 centrality counts include Telos {centrality['Telos']} and Crucible {centrality['Crucible']}.",
        f"Pass 0066 binds previous pass {packet['previous_pass_binding']['pass']} with sha256 {packet['previous_pass_binding']['sha256']}.",
        f"Pass 0066 unsupported_claim_count is {packet['unsupported_claim_count']} and promotion_state is {packet['promotion_state']}.",
        f"Pass 0066 composer sha256 is {shas['composer']} and compose_receipt status is {compose_receipt['status']}.",
        f"Pass 0066 packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={packet['schema']}", f"status={packet['status']}", f"sha256={shas['artifact']}", f"seal={packet['seal']}"],
        [f"tool_count={len(packet['internal_tools'])}", f"source_anchor_count={len(packet['source_anchors'])}", f"growth_vector_count={len(packet['growth_vectors'])}"],
        [f"cross_tool_experiment_count={len(packet['cross_tool_experiments'])}", f"top_bundle={packet['top_growth_bundles'][0]['bundle_id']}"],
        [f"Telos={centrality['Telos']}", f"Crucible={centrality['Crucible']}"],
        [f"previous_pass={packet['previous_pass_binding']['pass']}", f"previous_sha256={packet['previous_pass_binding']['sha256']}"],
        [f"unsupported_claim_count={packet['unsupported_claim_count']}", f"promotion_state={packet['promotion_state']}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
    ]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0066 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0066 Tool Growth Vector Experiment Matrix"}
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
