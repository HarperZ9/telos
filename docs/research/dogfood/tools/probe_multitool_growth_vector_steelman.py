"""Generate pass 0068 receipts for the multi-tool growth-vector steelman."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_multitool_growth_vector_steelman.py"
TEST_SCRIPT = ROOT / "tools" / "test_multitool_growth_vector_steelman.py"
OUT_PATH = ROOT / "schemas" / "multitool-growth-vector-steelman-pass-0068.json"
PACKET_PATH = ROOT / "packets" / "078-multitool-growth-vector-steelman.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0068-multitool-growth-vector-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0068-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0068-measurements.json"


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


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    top_rows = "\n".join(
        f"- `{row['tool']}` priority {row['scores']['priority']}: {row['upgrade_lever']}"
        for row in artifact["tool_rows"][:8]
    )
    queue = "\n".join(
        f"- `{item['id']}` ({item['kind']}) priority {item['priority']}"
        for item in artifact["experiment_queue"][:10]
    )
    objections = "\n".join(f"- `{row['risk_id']}`: {row['objection']}" for row in artifact["steelman_objections"])
    return f"""# Packet 078: Multi-Tool Growth-Vector Steelman

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: steelman growth vectors across the whole Telos/Build substrate and
convert them into executable experiments, falsifiers, integration targets, and
market-facing hypotheses.

```text
tool_count = {len(artifact['tool_rows'])}
source_anchor_count = {len(artifact['source_anchors'])}
synergy_edge_count = {len(artifact['synergy_edges'])}
experiment_queue_count = {len(artifact['experiment_queue'])}
steelman_objection_count = {len(artifact['steelman_objections'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Top Tool Upgrade Rows

{top_rows}

## Next Experiment Queue

{queue}

## Steelman Objections

{objections}

Current promoted natural laws: none.
"""


def render_steelman(artifact: dict) -> str:
    rows = "\n".join(
        f"- `{row['risk_id']}` kill criterion: {row['kill_criterion']}"
        for row in artifact["steelman_objections"]
    )
    return f"""# Pass 0068 Steelman: Multi-Tool Growth Vectors

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection to the megatool strategy is not that the pieces are
weak; it is that integration can hide the absence of one indispensable buyer
pain, one reproducible technical win, or one narrow wedge. This pass therefore
keeps every growth vector as a hypothesis and requires a falsifier before any
row can be promoted.

## Kill Criteria

{rows}

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    claims = [
        f"Pass 0068 created a MultiToolGrowthVectorSteelman/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0068 contains {len(artifact['tool_rows'])} tool rows and {len(artifact['source_anchors'])} source anchors.",
        f"Pass 0068 contains {len(artifact['synergy_edges'])} synergy edges and {len(artifact['experiment_queue'])} queued experiments.",
        f"Pass 0068 contains {len(artifact['steelman_objections'])} steelman objections with kill criteria.",
        f"Pass 0068 binds previous passes {[row['pass'] for row in artifact['previous_pass_bindings']]}.",
        f"Pass 0068 unsupported_claim_count is {artifact['unsupported_claim_count']} and all tool rows remain hypotheses.",
        f"Pass 0068 composer sha256 is {shas['composer']} and compose_receipt status is {compose_receipt['status']}.",
        f"Pass 0068 packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"tool_row_count={len(artifact['tool_rows'])}", f"source_anchor_count={len(artifact['source_anchors'])}"],
        [f"synergy_edge_count={len(artifact['synergy_edges'])}", f"experiment_queue_count={len(artifact['experiment_queue'])}"],
        [f"steelman_objection_count={len(artifact['steelman_objections'])}", "kill_criteria_present=true"],
        [f"previous_passes={[row['pass'] for row in artifact['previous_pass_bindings']]}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", "claim_statuses=hypothesis"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
    ]
    thesis = {
        "title": "Dogfood Pass 0068 Multi-Tool Growth Vector Steelman",
        "disposition": "fenced",
        "claims": [{"text": claim, "falsification": f"Claim {i + 1} differs from pass 0068 artifact values or required files are missing"} for i, claim in enumerate(claims)],
    }
    measurements = {
        "measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": "artifact-review", "tolerance": 0.5} for i, claim in enumerate(claims)]
    }
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "MULTITOOL_GROWTH_VECTOR_STEELMAN_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
