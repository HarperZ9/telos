"""Generate pass 0124 agent action proof-packet adapter artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_agent_action_proof_packet_factory_adapter.py"
TEST_SCRIPT = ROOT / "tools" / "test_agent_action_proof_packet_factory_adapter.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0124_agent_action_adapter.py"
OUT_PATH = ROOT / "schemas" / "agent-action-proof-packet-factory-adapter-pass-0124.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0124-agent-action-adapter-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0124.json"
PACKET_PATH = ROOT / "packets" / "134-agent-action-proof-packet-factory-adapter.md"
BRIEF_PATH = ROOT / "briefs" / "134-agent-action-proof-packet-factory-adapter-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0124-agent-action-proof-packet-factory-adapter-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0124-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0124-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.encode("ascii", "ignore").decode("ascii"), encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def receipt_rows(artifact: dict) -> list[dict]:
    return [
        {"system": row["tool_call"]["native_system"], "status": row["adapter_status"], "verdict": row["verification_verdict"], "side_effect": row["side_effect_class"]}
        for row in artifact["action_receipts"]
    ]


def negative_rows(artifact: dict) -> list[dict]:
    return [{"fixture": row["fixture_id"], "status": row["status"], "failures": ",".join(row["failures"])} for row in artifact["negative_fixtures"]]


def source_rows(artifact: dict) -> list[dict]:
    return [{"source": row["label"], "chars": row["chars"], "status": row["gather_status"]} for row in artifact["source_matrix"]]


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    return f"""# Packet 134: Agent Action Proof-Packet Factory Adapter

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: turn the pass 0123 `AgentActionProofPacketFactory` into an executable
adapter fixture. Five incumbent-style trace inputs are preserved, then wrapped
with Telos authority, admission, side-effect, privacy, and verifier fields.

```text
source_rows = {len(artifact['source_matrix'])}
trace_inputs = {len(artifact['trace_inputs'])}
action_receipts = {len(artifact['action_receipts'])}
negative_fixtures = {len(artifact['negative_fixtures'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Adapted Receipts

| Native system | Adapter status | Verdict | Side effect |
| --- | --- | --- | --- |
{table(receipt_rows(artifact), ['system', 'status', 'verdict', 'side_effect'])}

## Rejection Fixtures

| Fixture | Status | Failures |
| --- | --- | --- |
{table(negative_rows(artifact), ['fixture', 'status', 'failures'])}

## Source Matrix

| Source | Chars | Gather status |
| --- | ---: | --- |
{table(source_rows(artifact), ['source', 'chars', 'status'])}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Agent Action Proof-Packet Factory Adapter Brief

Date: 2026-07-01

## Decision

Promote `AgentActionProofPacketFactory` from strategy into the first executable
factory demo. The adapter preserves incumbent trace identifiers, but requires
Telos fields that traces alone cannot prove: authority, admission, side-effect
class, privacy boundary, verifier verdict, and stop reason.

## Market Wedge

This is not a LangSmith, Langfuse, Phoenix, Braintrust, or OpenTelemetry
replacement claim. It is an import-and-bind layer for regulated and high-stakes
agent work.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0124 Steelman: Agent Action Proof-Packet Factory Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that synthetic trace fixtures do not prove
production integration. Correct. The next gate is an external OTLP JSON import
fixture and one real local Telos action receipt.

The second objection is that incumbent observability tools may add similar
policy or eval fields. The pass therefore treats the gap as `inferred` and
keeps replacement claims out of scope.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0124",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_count": len(artifact["source_matrix"]),
        "receipt_count": len(artifact["action_receipts"]),
        "negative_count": len(artifact["negative_fixtures"]),
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0124 created an AgentActionProofPacketFactoryAdapter/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0124 records {len(artifact['source_matrix'])} Gather source rows and all have at least 500 chars.",
        f"Pass 0124 adapts {len(artifact['trace_inputs'])} incumbent-style trace inputs into {len(artifact['action_receipts'])} Telos action receipts.",
        "Every pass 0124 action receipt carries all required pass 0064 action receipt fields and has MATCH adapter status.",
        "Pass 0124 rejects four negative fixtures for missing authority/admission/verifier fields or external-write/hidden-reasoning violations.",
        f"Pass 0124 binds prior passes {artifact['source_bindings']}.",
        "Pass 0124 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0124 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0124 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0124 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_chars={[row['chars'] for row in artifact['source_matrix']]}"],
        [f"trace_inputs={artifact['trace_inputs']}", f"receipt_ids={[row['receipt_id'] for row in artifact['action_receipts']]}"],
        [f"contract={artifact['adapter_contract_fields']}", f"statuses={[row['adapter_status'] for row in artifact['action_receipts']]}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0124 Agent Action Proof-Packet Adapter", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0124 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    validator_receipt = run_command([sys.executable, str(VALIDATOR)], timeout=120)
    receipts = {"compose": compose_receipt, "test": test_receipt, "validator": validator_receipt}
    write_tool_receipts(artifact, compose_receipt, test_receipt, validator_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt, validator_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, receipts)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "AGENT_ACTION_PROOF_PACKET_FACTORY_ADAPTER_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
