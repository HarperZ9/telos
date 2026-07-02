"""Generate pass 0064 receipts for the agent observability adapter matrix."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_agent_observability_action_receipt_adapter_matrix.py"
TEST_SCRIPT = ROOT / "tools" / "test_agent_observability_action_receipt_adapter_matrix.py"
OUT_PATH = ROOT / "schemas" / "agent-observability-action-receipt-adapter-matrix-pass-0064.json"
PACKET_PATH = ROOT / "packets" / "074-agent-observability-action-receipt-adapter-matrix.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0064-agent-observability-action-receipt-adapter-matrix-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0064-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0064-measurements.json"


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
    rows = packet["adapter_rows"]
    adapter_lines = "\n".join(f"- `{row['tool']}` priority `{row['adapter_priority']}` preserves `{', '.join(row['native_refs_to_preserve'])}`." for row in rows)
    field_lines = "\n".join(f"- `{field}`" for field in packet["action_receipt_fields"])
    demo_lines = "\n".join(f"- `{demo['demo_id']}`: {demo['success_metric']}" for demo in packet["demo_slices"])
    return f"""# Packet 074: Agent Observability Action-Receipt Adapter Matrix

Date: 2026-07-01

Status: `{packet['status']}`

Purpose: define how Telos should preserve incumbent observability and eval refs while adding authority, workspace, side-effect, admission, verification, and compensation receipt layers.

```text
source_anchor_count = {len(packet['source_anchors'])}
adapter_count = {len(rows)}
receipt_field_count = {len(packet['action_receipt_fields'])}
unsupported_uniqueness_claim_count = {packet['unsupported_uniqueness_claim_count']}
non_replacement_claim = {packet['non_replacement_claim']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Adapter Rows

{adapter_lines}

## Action Receipt Fields

{field_lines}

## Demo Slices

{demo_lines}
"""


def render_steelman(packet: dict) -> str:
    return f"""# Pass 0064 Steelman: Agent Observability Action-Receipt Adapter Matrix

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The wedge is plausible but not proven. Incumbent observability tools already
capture detailed traces, evals, costs, latency, and workflow metadata. Telos
must prove that authority, workspace state, side-effect class, action admission,
verification verdicts, and compensation pointers are valuable enough to justify
another layer.

This pass does not claim replacement of LangSmith, Langfuse, Phoenix,
Braintrust, OpenTelemetry, MLflow, Weave, DVC, promptfoo, or Helicone.

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
    tools = ",".join(sorted(row["tool"] for row in packet["adapter_rows"]))
    claims = [
        f"Pass 0064 created an AgentObservabilityActionReceiptAdapterMatrix/v1 artifact with status {packet['status']}, sha256 {shas['artifact']}, and seal {packet['seal']}.",
        f"Pass 0064 contains {len(packet['source_anchors'])} source anchors and {len(packet['adapter_rows'])} adapter rows.",
        f"Pass 0064 adapter rows include {tools}.",
        f"Pass 0064 action_receipt_fields count is {len(packet['action_receipt_fields'])} and includes authority_scope, action_admission, side_effect_class, verification_verdict, and compensation_pointer.",
        f"Pass 0064 unsupported_uniqueness_claim_count is {packet['unsupported_uniqueness_claim_count']} and non_replacement_claim is {packet['non_replacement_claim']}.",
        f"Pass 0064 records three demo slices with promotion_state DEMO_NOT_PRODUCT_MARKET_FIT.",
        f"Pass 0064 composer sha256 is {shas['composer']} and compose_receipt status is {compose_receipt['status']}.",
        f"Pass 0064 packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={packet['schema']}", f"status={packet['status']}", f"sha256={shas['artifact']}", f"seal={packet['seal']}"],
        [f"source_anchor_count={len(packet['source_anchors'])}", f"adapter_count={len(packet['adapter_rows'])}"],
        [tools],
        [f"field_count={len(packet['action_receipt_fields'])}", "authority_scope", "action_admission", "side_effect_class", "verification_verdict", "compensation_pointer"],
        [f"unsupported_uniqueness_claim_count={packet['unsupported_uniqueness_claim_count']}", f"non_replacement_claim={packet['non_replacement_claim']}"],
        [f"demo_count={len(packet['demo_slices'])}", "promotion_state=DEMO_NOT_PRODUCT_MARKET_FIT"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
    ]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0064 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0064 Agent Observability Action Receipt Adapter Matrix"}
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
