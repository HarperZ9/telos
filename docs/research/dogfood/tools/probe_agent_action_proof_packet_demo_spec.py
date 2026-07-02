"""Generate pass 0050 agent action proof-packet demo spec receipts."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


PASS = "0050"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PREVIOUS_PACKET = ROOT / "schemas" / "wedge-budget-signal-scorecard-pass-0049.json"
OUT_PATH = ROOT / "schemas" / "agent-action-proof-packet-demo-spec-pass-0050.json"
FIXTURE_PATH = ROOT / "fixtures" / "agent-action-proof-packet-demo-spec-pass-0050.json"
PACKET_PATH = ROOT / "packets" / "060-agent-action-proof-packet-demo-spec.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0050-agent-action-proof-packet-demo-spec-steelman.md"


LOCAL_COMPONENTS = [
    ("action_receipt", "demo/integrations/action-receipt-conventions.json", "project-telos.action-receipt/v1", "existing"),
    ("admission_telemetry", "demo/integrations/admission-telemetry-conventions.json", "project-telos.admission-telemetry/v1", "existing"),
    ("browser_evidence", "demo/integrations/browser-evidence.json", "project-telos.browser-evidence/v1", "existing"),
    ("loop_ledger", "demo/integrations/loop-ledger-conventions.json", "project-telos.loop-ledger/v1", "existing"),
    ("workstation_substrate", "demo/integrations/workstation-substrate.json", "project-telos.workstation-substrate/v1", "existing"),
    ("model_foundry", "demo/model-foundry.mjs", "project-telos.model-foundry/v1", "existing_executable"),
    ("flagship_action", "demo/flagship-action.mjs", "project-telos.flagship-action/v1", "existing_module"),
    ("context_pack", "demo/context-pack.mjs", "project-telos.context-pack/v1", "existing_module"),
    ("telos_mcp", "demo/telos-mcp.mjs", "telos.mcp", "existing_module"),
    ("operator_doctor", "demo/operator-doctor.mjs", "telos.operator.doctor", "existing_module"),
    ("display_calibration", "demo/display-calibration.mjs", "project-telos.display-calibration/v1", "follow_on_domain"),
]


SUMMARY_COMMANDS = [
    ("browser_evidence", ["node", "demo/browser-evidence.mjs", "--summary"], ["verdict  MATCH", "valid    MATCH"]),
    ("workstation_substrate", ["node", "demo/workstation-substrate.mjs", "--summary"], ["verdict      MATCH"]),
    ("model_foundry", ["node", "demo/model-foundry.mjs", "--summary"], ["verdict MATCH"]),
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def component_receipts() -> list[dict]:
    receipts = []
    for component, rel_path, schema_hint, status in LOCAL_COMPONENTS:
        path = REPO / rel_path
        exists = path.exists()
        parsed_schema = None
        if exists and path.suffix == ".json":
            parsed_schema = read_json(path).get("schema")
        receipts.append({
            "component": component,
            "exists": exists,
            "line_count": len(path.read_text(encoding="utf-8").splitlines()) if exists else 0,
            "path": rel_path,
            "schema_hint": schema_hint,
            "schema_match": parsed_schema in {None, schema_hint},
            "sha256": sha256_file(path) if exists else None,
            "status": status,
        })
    return receipts


def summary_receipts() -> list[dict]:
    rows = []
    for component, command, needles in SUMMARY_COMMANDS:
        result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, check=False)
        output = result.stdout
        contains = {needle: needle in output for needle in needles}
        rows.append({
            "command": " ".join(command),
            "component": component,
            "contains": contains,
            "exit_code": result.returncode,
            "output_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
            "status": "MATCH" if result.returncode == 0 and all(contains.values()) else "DRIFT",
        })
    return rows


def integration_gaps() -> list[dict]:
    return [
        {"id": "trace_ingest_adapter", "need": "Import LangSmith/Langfuse/Phoenix/OpenTelemetry traces into proof packet source refs.", "status": "needs_integration"},
        {"id": "packet_composer", "need": "Join source refs, workspace refs, admission telemetry, action receipt, browser evidence, loop ledger, and Crucible verdict.", "status": "needs_integration"},
        {"id": "public_demo_fixture", "need": "Create one sanitized multi-tool action fixture with no private payloads and stable hashes.", "status": "needs_packaging"},
        {"id": "redaction_policy", "need": "Define field-level public/private boundaries for evidence, screenshots, page state, and tool outputs.", "status": "needs_integration"},
        {"id": "verifier_runner", "need": "Run validator and Crucible from one command and emit a portable proof bundle.", "status": "needs_packaging"},
        {"id": "export_bundle", "need": "Emit markdown, JSON, and small static web view for buyer review.", "status": "needs_packaging"},
    ]


def demo_flow() -> list[str]:
    return [
        "Gather source refs and task input without raw private payload export.",
        "Index workspace context into a lossless-by-reference envelope.",
        "Forum routes the proposed action and records route confidence.",
        "Telos records proposed action intent and admission decision.",
        "Action executes through a bounded tool or browser step.",
        "Browser evidence captures redacted before/after state when relevant.",
        "Loop ledger appends the action, result, and continuation boundary.",
        "Crucible checks the packet against measurements and negative fixtures.",
        "Packet composer emits portable JSON and markdown proof bundle.",
        "Demo UI shows source refs, action refs, verdicts, gaps, and replay commands.",
    ]


def render_packet(contract: dict) -> str:
    lines = [
        "# Packet 060: Agent Action Proof Packet Demo Spec",
        "",
        "Date: 2026-07-01",
        "",
        f"Status: `{contract['status']}`",
        "",
        "This pass defines the first 30-day public demo: an observability-to-action",
        "receipt proof packet for AI infrastructure teams.",
        "",
        "```text",
        f"component_count = {contract['verifier_measurements']['component_count']}",
        f"summary_match_count = {contract['verifier_measurements']['summary_match_count']}",
        f"integration_gap_count = {contract['verifier_measurements']['integration_gap_count']}",
        f"demo_flow_step_count = {contract['verifier_measurements']['demo_flow_step_count']}",
        f"primary_market = {contract['primary_market']}",
        "```",
        "",
        "Existing pieces: action receipts, admission telemetry, browser evidence,",
        "loop ledger, workstation substrate, model foundry, flagship action envelopes,",
        "and Telos MCP/operator surfaces.",
        "",
        "Missing work: trace ingest, packet composer, public fixture, redaction policy,",
        "one-command verifier runner, and export bundle.",
        "",
        "Current promoted natural laws: none.",
    ]
    return "\n".join(lines) + "\n"


def render_steelman() -> str:
    return """# Pass 0050 Steelman: Agent Action Proof Packet Demo Spec

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass proves the demo is mappable to existing local components and that a
few summary commands run. It does not prove the integrated demo exists yet,
that buyers will adopt it, or that trace import/export with external tools is
complete. Integration gaps remain explicit.
"""


def main() -> None:
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    components = component_receipts()
    summaries = summary_receipts()
    gaps = integration_gaps()
    flow = demo_flow()
    all_match = all(row["exists"] and row["schema_match"] for row in components) and all(row["status"] == "MATCH" for row in summaries)
    fixture = with_seal({
        "component_receipts": components,
        "generated_on": "2026-07-01",
        "pass": PASS,
        "schema": "AgentActionProofPacketDemoSpecFixture/v1",
        "summary_receipts": summaries,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "component_receipts": components,
        "current_promoted_natural_laws": [],
        "demo_flow": flow,
        "fixture": {"path": "fixtures/agent-action-proof-packet-demo-spec-pass-0050.json", "schema": fixture["schema"], "seal": fixture["seal"], "sha256": fixture_sha},
        "generated_on": "2026-07-01",
        "integration_gaps": gaps,
        "non_promotion_statement": "Pass 0050 is a demo architecture and packaging spec. It does not prove the integrated public demo exists, product-market fit, buyer adoption, scientific truth, or any natural law.",
        "pass": PASS,
        "previous_pass_binding": {"path": "schemas/wedge-budget-signal-scorecard-pass-0049.json", "seal": previous["seal"], "sha256": previous_sha, "source_status": previous["status"]},
        "primary_market": "agent_action_proof_packets",
        "schema": "AgentActionProofPacketDemoSpecSet/v1",
        "status": "AGENT_ACTION_PROOF_PACKET_DEMO_SPEC_MATCH" if all_match else "AGENT_ACTION_PROOF_PACKET_DEMO_SPEC_DRIFT",
        "summary_receipts": summaries,
        "thirty_day_acceptance_checks": [
            "one command builds JSON and markdown proof bundle",
            "bundle contains source refs, workspace refs, admission, action receipt, browser evidence, ledger entry, and Crucible verdict",
            "all private payloads are replaced by hashes or source refs",
            "negative fixture produces DRIFT or UNVERIFIABLE",
        ],
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "verifier_measurements": {"component_count": len(components), "component_match_count": sum(1 for row in components if row["exists"] and row["schema_match"]), "demo_flow_step_count": len(flow), "integration_gap_count": len(gaps), "summary_match_count": sum(1 for row in summaries if row["status"] == "MATCH")},
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "component_count": contract["verifier_measurements"]["component_count"],
        "integration_gap_count": contract["verifier_measurements"]["integration_gap_count"],
        "path": str(OUT_PATH),
        "seal": contract["seal"],
        "status": contract["status"],
        "summary_match_count": contract["verifier_measurements"]["summary_match_count"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
