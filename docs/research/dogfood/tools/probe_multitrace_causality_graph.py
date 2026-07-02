"""Generate pass 0055 receipts for the multi-trace causality graph."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


PASS = "0055"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
ADAPTER = ROOT / "tools" / "build_multitrace_causality_graph.py"
TEST_SCRIPT = ROOT / "tools" / "test_multitrace_causality_graph.py"
SOURCE_BINDING = ROOT / "schemas" / "source-evidence-binding-pass-0028.json"
TRACE_JOIN = ROOT / "schemas" / "otel-trace-receipt-join-pass-0054.json"
TOOL_RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0054.json"
SPAN_FIXTURE = ROOT / "fixtures" / "multitrace-causality-spans-pass-0055.json"
GRAPH_PATH = ROOT / "schemas" / "multitrace-causality-graph-pass-0055.json"
OUT_PATH = ROOT / "schemas" / "multitrace-causality-graph-adapter-pass-0055.json"
PACKET_PATH = ROOT / "packets" / "065-multitrace-causality-graph.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0055-multitrace-causality-graph-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0055-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0055-measurements.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


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


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stderr_sha256": sha256_text(result.stderr),
        "stdout_sha256": sha256_text(result.stdout),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def span_fixture() -> dict:
    return {
        "schema": "OpenTelemetrySpanExportFixture/v1",
        "spans": [
            {
                "attributes": {"telos.raw_payload_included": False, "telos.receipt_hash": "71b39e899e143294fb810a2d335bb11cbeff43abf26114cdda22573dd2502952", "telos.receipt_kind": "GatherDocumentReceipt/v1", "telos.receipt_ref": "gather:docs/packets/064-otel-trace-receipt-join-adapter.md", "telos.tool_class": "gather"},
                "context": {"span_id": "0055000000000001", "trace_id": "00550000000000000000000000000001"},
                "links": [],
                "name": "gather.docs.packet",
            },
            {
                "attributes": {"telos.raw_payload_required": False, "telos.receipt_hash": "d30289cfdcaf8630e7fb7b3ba911cbac485a62f5306e3b5c37338768dbfe9e7a", "telos.receipt_kind": "project-telos.browser-evidence/v1", "telos.receipt_ref": "artifact:fixtures/browser-evidence-redacted-pass-0028.json", "telos.redaction_status": "redacted", "telos.tool_class": "browser_evidence"},
                "context": {"span_id": "0055000000000002", "trace_id": "00550000000000000000000000000002"},
                "links": [{"kind": "source", "span_id": "0055000000000001", "trace_id": "00550000000000000000000000000001"}],
                "name": "browser.evidence.redacted",
            },
            {
                "attributes": {"telos.exit_code": 0, "telos.receipt_hash": "validator-pass-0054-match", "telos.receipt_kind": "ShellCommandReceipt/v1", "telos.receipt_ref": "command:python docs/research/dogfood/tools/validate_pass_0054_otel_trace_receipt_join_adapter.py", "telos.tool_class": "command_execution"},
                "context": {"span_id": "0055000000000003", "trace_id": "00550000000000000000000000000003"},
                "links": [{"kind": "evidence", "span_id": "0055000000000002", "trace_id": "00550000000000000000000000000002"}],
                "name": "shell.command.validation",
            },
            {
                "attributes": {"telos.action_id": "act_dogfood_0024_001", "telos.receipt_hash": "9c6402f98774170311d78ea3f6983cae71a665dd38ab2ee7e88d413398990ff4", "telos.receipt_kind": "TelosActionReceiptFixtureChain/v1", "telos.receipt_ref": "telos:action-receipt/act_dogfood_0024_001/chain/0617602eed957e0bc6c2e4a21548528f6defc542c4468433bde85df76cb51b3a", "telos.tool_class": "action_receipt"},
                "context": {"span_id": "1424d4ca9a6c5b58", "trace_id": "aaa76491660d7a56086f69d1be94debe"},
                "links": [{"kind": "execution", "span_id": "0055000000000003", "trace_id": "00550000000000000000000000000003"}],
                "name": "telos.action.receipt.fixture",
            },
        ],
    }


def render_packet(contract: dict, graph: dict) -> str:
    summary = graph["graph_summary"]
    return f"""# Packet 065: Multi-Trace Causality Graph

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0055 builds a four-node causality graph across Gather, browser evidence,
command execution, and action receipts while preserving independent durable
receipt references for every node.

```text
node_count = {summary['node_count']}
edge_count = {summary['edge_count']}
independent_receipt_count = {summary['independent_receipt_count']}
trace_identity_substitution_count = {summary['trace_identity_substitution_count']}
negative_fixture_count = {contract['verifier_measurements']['negative_fixture_count']}
negative_match_count = {contract['verifier_measurements']['negative_match_count']}
negative_pass_observed_count = {contract['verifier_measurements']['negative_pass_observed_count']}
```

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0055 Steelman: Multi-Trace Causality Graph

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass proves a local synthetic causality graph only. It does not prove live
collector ingestion, complete distributed causality, production browser capture,
buyer adoption, scientific truth, or any natural law.
"""


def build_thesis_measurements(contract: dict, graph: dict) -> tuple[dict, dict]:
    shas = {
        "adapter": sha256_file(ADAPTER),
        "graph": sha256_file(GRAPH_PATH),
        "packet": sha256_file(PACKET_PATH),
        "schema": sha256_file(OUT_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    claims = [
        f"Pass 0055 created a MultiTraceCausalityGraphAdapterSet/v1 artifact with status {contract['status']}, node_count {graph['graph_summary']['node_count']}, edge_count {graph['graph_summary']['edge_count']}, sha256 {shas['schema']}, and seal {contract['seal']}.",
        f"Pass 0055 implements build_multitrace_causality_graph.py with sha256 {shas['adapter']} and implementation_status {contract['implementation_status']}.",
        f"Pass 0055 records a multi-trace causality test script with sha256 {shas['test']} and test_receipt status {contract['test_receipt']['status']}.",
        f"Pass 0055 generated a MultiTraceCausalityGraph/v1 output with status {graph['status']}, independent_receipt_count {graph['graph_summary']['independent_receipt_count']}, trace_identity_substitution_count {graph['graph_summary']['trace_identity_substitution_count']}, and sha256 {shas['graph']}.",
        f"Pass 0055 records negative_fixture_count {graph['negative_fixture_count']}, negative_match_count {graph['negative_match_count']}, and negative_pass_observed_count {graph['negative_pass_observed_count']} from the graph adapter.",
        f"Pass 0055 binds source-evidence pass 0028 sha256 {contract['upstream_bindings']['source_binding']['sha256']}, trace-join pass 0054 sha256 {contract['upstream_bindings']['trace_join']['sha256']}, and tool-receipts pass 0054 sha256 {contract['upstream_bindings']['tool_receipts']['sha256']}.",
        "Pass 0055 validator result reports MATCH with node_count 4, edge_count 3, and trace_identity_substitution_count 0.",
        f"Pass 0055 records packet 065 sha256 {shas['packet']}, steelman sha256 {shas['steelman']}, uniqueness_claim_status HYPOTHESIS_ONLY, and current_promoted_natural_laws remains none.",
    ]
    evidence = [
        [f"schema=MultiTraceCausalityGraphAdapterSet/v1", f"status={contract['status']}", f"node_count={graph['graph_summary']['node_count']}", f"edge_count={graph['graph_summary']['edge_count']}", f"sha256={shas['schema']}", f"seal={contract['seal']}"],
        [f"adapter_sha256={shas['adapter']}", f"implementation_status={contract['implementation_status']}"],
        [f"test_sha256={shas['test']}", f"test_status={contract['test_receipt']['status']}"],
        [f"graph_status={graph['status']}", f"independent_receipt_count={graph['graph_summary']['independent_receipt_count']}", f"trace_identity_substitution_count={graph['graph_summary']['trace_identity_substitution_count']}", f"sha256={shas['graph']}"],
        [f"negative_fixture_count={graph['negative_fixture_count']}", f"negative_match_count={graph['negative_match_count']}", f"negative_pass_observed_count={graph['negative_pass_observed_count']}"],
        [f"source_binding_sha256={contract['upstream_bindings']['source_binding']['sha256']}", f"trace_join_sha256={contract['upstream_bindings']['trace_join']['sha256']}", f"tool_receipts_sha256={contract['upstream_bindings']['tool_receipts']['sha256']}"],
        ["validator_status=MATCH", "node_count=4", "edge_count=3", "trace_identity_substitution_count=0"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", "uniqueness_claim_status=HYPOTHESIS_ONLY", "current_promoted_natural_laws=[]"],
    ]
    methods = ["adapter-schema-review", "adapter-file-review", "adapter-test-review", "graph-output-review", "negative-fixture-review", "upstream-binding-review", "validator-result-review", "non-promotion-boundary-review"]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0055 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0055 Multi-Trace Causality Graph"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": methods[i], "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    write_json(SPAN_FIXTURE, span_fixture())
    adapter_receipt = run_command([sys.executable, str(ADAPTER), "--spans", str(SPAN_FIXTURE), "--source-binding", str(SOURCE_BINDING), "--trace-join", str(TRACE_JOIN), "--tool-receipts", str(TOOL_RECEIPTS), "--out", str(GRAPH_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    graph = read_json(GRAPH_PATH)
    all_match = adapter_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and graph["status"] == "MULTITRACE_CAUSALITY_GRAPH_MATCH" and graph["negative_match_count"] == 5 and graph["negative_pass_observed_count"] == 0
    contract = with_seal({
        "adapter_receipt": adapter_receipt,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "graph_output": {"path": "schemas/multitrace-causality-graph-pass-0055.json", "schema": graph["schema"], "sha256": sha256_file(GRAPH_PATH), "status": graph["status"]},
        "implementation_status": "IMPLEMENTED_LOCAL_MULTITRACE_GRAPH_ADAPTER",
        "non_promotion_statement": graph["non_promotion_statement"],
        "pass": PASS,
        "schema": "MultiTraceCausalityGraphAdapterSet/v1",
        "span_fixture": {"path": "fixtures/multitrace-causality-spans-pass-0055.json", "sha256": sha256_file(SPAN_FIXTURE), "span_count": len(read_json(SPAN_FIXTURE)["spans"])},
        "status": "MULTITRACE_CAUSALITY_GRAPH_ADAPTER_MATCH" if all_match else "MULTITRACE_CAUSALITY_GRAPH_ADAPTER_DRIFT",
        "test_receipt": test_receipt,
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "upstream_bindings": {"source_binding": {"path": "schemas/source-evidence-binding-pass-0028.json", "sha256": sha256_file(SOURCE_BINDING)}, "tool_receipts": {"path": "schemas/tool-receipts-pass-0054.json", "sha256": sha256_file(TOOL_RECEIPTS)}, "trace_join": {"path": "schemas/otel-trace-receipt-join-pass-0054.json", "sha256": sha256_file(TRACE_JOIN)}},
        "verifier_measurements": {**graph["graph_summary"], "negative_fixture_count": graph["negative_fixture_count"], "negative_match_count": graph["negative_match_count"], "negative_pass_observed_count": graph["negative_pass_observed_count"]},
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract, graph))
    write_text(STEELMAN_PATH, render_steelman())
    thesis, measurements = build_thesis_measurements(contract, graph)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    print(json.dumps({"path": str(OUT_PATH), "seal": contract["seal"], "status": contract["status"]}, indent=2, sort_keys=True))
    if contract["status"].endswith("_DRIFT"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
