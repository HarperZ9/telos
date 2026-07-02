"""Compose the public agent action proof-packet demo bundle."""
from __future__ import annotations

import argparse
import copy
import html
import hashlib
import json
from pathlib import Path


SCHEMA = "project-telos.agent-action-proof-packet.bundle/v1"
REPORT_SCHEMA = "project-telos.agent-action-proof-packet.negative-report/v1"
RECEIPTS_SCHEMA = "project-telos.agent-action-proof-packet.bundle-receipts/v1"
EXPECTED_OUTPUTS = [
    "packet.json",
    "packet.md",
    "receipts.json",
    "negative-fixture-report.json",
    "index.html",
    "replay-commands.md",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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


def validate_packet(packet: dict) -> dict:
    required = [
        ("source_refs", "source_refs_missing", "UNVERIFIABLE"),
        ("workspace_context_ref", "workspace_context_ref_missing", "UNVERIFIABLE"),
        ("admission_record", "admission_record_missing", "UNVERIFIABLE"),
        ("action_receipt", "action_receipt_missing", "UNVERIFIABLE"),
        ("browser_evidence_ref", "browser_evidence_missing", "UNVERIFIABLE"),
        ("loop_ledger_entry", "loop_ledger_entry_missing", "UNVERIFIABLE"),
        ("crucible_verdict", "crucible_verdict_missing", "UNVERIFIABLE"),
    ]
    for component, failure_code, verdict in required:
        if not packet.get(component):
            return {"component": component, "failure_code": failure_code, "verdict": verdict}
    if packet["admission_record"]["action_intent_id"] != packet["action_receipt"]["action_intent_id"]:
        return {"component": "action_receipt", "failure_code": "action_receipt_linkage_broken", "verdict": "DRIFT"}
    if packet["browser_evidence_ref"]["action_receipt_ref"] != packet["action_receipt"]["action_id"]:
        return {"component": "browser_evidence_ref", "failure_code": "browser_action_ref_broken", "verdict": "DRIFT"}
    if packet["loop_ledger_entry"].get("chain") is not True:
        return {"component": "loop_ledger_entry", "failure_code": "ledger_continuity_broken", "verdict": "DRIFT"}
    if packet["crucible_verdict"].get("status") != "MATCH":
        return {"component": "crucible_verdict", "failure_code": "crucible_verdict_not_match", "verdict": "DRIFT"}
    if packet["redaction_status"].get("raw_private_payloads_included") is not False:
        return {"component": "redaction_status", "failure_code": "private_payload_boundary_violation", "verdict": "DRIFT"}
    return {"component": "packet", "failure_code": None, "verdict": "MATCH"}


def mutate_packet(base: dict, fixture_id: str) -> dict:
    packet = copy.deepcopy(base)
    if fixture_id == "missing_source_refs":
        packet.pop("source_refs", None)
    elif fixture_id == "missing_workspace_context":
        packet.pop("workspace_context_ref", None)
    elif fixture_id == "missing_admission_record":
        packet.pop("admission_record", None)
    elif fixture_id == "broken_action_receipt_linkage":
        packet["action_receipt"]["action_intent_id"] = "intent-mismatch"
    elif fixture_id == "missing_browser_evidence":
        packet.pop("browser_evidence_ref", None)
    elif fixture_id == "broken_ledger_continuity":
        packet["loop_ledger_entry"]["chain"] = False
    elif fixture_id == "missing_crucible_verdict":
        packet.pop("crucible_verdict", None)
    elif fixture_id == "raw_private_payload_leak":
        packet["redaction_status"]["raw_private_payloads_included"] = True
    else:
        raise ValueError(f"unknown negative fixture: {fixture_id}")
    packet["packet_hash"] = sha256_obj({k: v for k, v in packet.items() if k != "packet_hash"})
    return packet


def negative_report(fixture: dict) -> dict:
    base = fixture["positive_fixture"]
    rows = []
    for expected in fixture["negative_fixtures"]:
        mutated = mutate_packet(base, expected["fixture_id"])
        observed = validate_packet(mutated)
        status = "MATCH" if (
            observed["failure_code"] == expected["expected_failure_code"]
            and observed["verdict"] == expected["expected_verdict"]
        ) else "DRIFT"
        rows.append({
            "expected_failure_code": expected["expected_failure_code"],
            "expected_verdict": expected["expected_verdict"],
            "fixture_id": expected["fixture_id"],
            "observed": observed,
            "packet_hash": mutated["packet_hash"],
            "status": status,
        })
    return {
        "schema": REPORT_SCHEMA,
        "negative_fixture_count": len(rows),
        "negative_match_count": sum(1 for row in rows if row["status"] == "MATCH"),
        "negative_pass_observed_count": sum(1 for row in rows if row["observed"]["verdict"] == "MATCH"),
        "rows": rows,
        "status": "MATCH" if all(row["status"] == "MATCH" for row in rows) else "DRIFT",
    }


def packet_bundle(fixture_path: Path, fixture: dict, report: dict) -> dict:
    positive = fixture["positive_fixture"]
    verification = validate_packet(positive)
    packet = {
        "schema": SCHEMA,
        "bundle_id": "agent-action-proof-packet-demo-0053",
        "fixture_ref": {"path": str(fixture_path), "sha256": sha256_file(fixture_path)},
        "proof_packet": positive,
        "verification": verification,
        "redaction_status": positive["redaction_status"],
        "negative_fixture_summary": {
            "negative_fixture_count": report["negative_fixture_count"],
            "negative_match_count": report["negative_match_count"],
            "negative_pass_observed_count": report["negative_pass_observed_count"],
        },
        "exports": {"json_bundle": True, "markdown_packet": True, "static_html": True},
        "non_promotion_statement": "This demo bundle proves local packet composition and negative fixture replay only. It does not prove buyer adoption, scientific truth, or a natural law.",
    }
    packet["bundle_hash"] = sha256_obj(packet)
    return packet


def render_markdown(packet: dict, report: dict) -> str:
    rows = "\n".join(
        f"| `{row['fixture_id']}` | `{row['observed']['failure_code']}` | `{row['observed']['verdict']}` | `{row['status']}` |"
        for row in report["rows"]
    )
    return f"""# Agent Action Proof Packet Demo

Status: `{packet['verification']['verdict']}`

Bundle hash: `{packet['bundle_hash']}`

| Fixture | Failure code | Verdict | Status |
| --- | --- | --- | --- |
{rows}

Current promoted natural laws: none.
"""


def render_html(packet: dict, report: dict) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(row['fixture_id'])}</td>"
        f"<td>{html.escape(row['observed']['failure_code'] or '')}</td>"
        f"<td>{html.escape(row['observed']['verdict'])}</td>"
        f"<td>{html.escape(row['status'])}</td>"
        "</tr>"
        for row in report["rows"]
    )
    return f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>Agent Action Proof Packet Demo</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem; color: #111; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border: 1px solid #bbb; padding: .45rem; text-align: left; }}
code {{ background: #f2f2f2; padding: .1rem .25rem; }}
</style>
<h1>Agent Action Proof Packet Demo</h1>
<p>Verification: <code>{html.escape(packet['verification']['verdict'])}</code></p>
<p>Bundle hash: <code>{html.escape(packet['bundle_hash'])}</code></p>
<table>
<thead><tr><th>Fixture</th><th>Failure code</th><th>Verdict</th><th>Status</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</html>
"""


def render_replay(fixture_path: Path, out_dir: Path) -> str:
    return f"""# Replay Commands

```powershell
python docs\\research\\dogfood\\tools\\compose_agent_action_proof_packet_demo.py --fixture {fixture_path} --out {out_dir}
python docs\\research\\dogfood\\tools\\test_agent_action_packet_composer_demo.py
```
"""


def build_bundle(fixture_path: Path, out_dir: Path) -> dict:
    fixture = read_json(fixture_path)
    report = negative_report(fixture)
    packet = packet_bundle(fixture_path, fixture, report)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "packet.json", packet)
    write_json(out_dir / "negative-fixture-report.json", report)
    write_text(out_dir / "packet.md", render_markdown(packet, report))
    write_text(out_dir / "index.html", render_html(packet, report))
    write_text(out_dir / "replay-commands.md", render_replay(fixture_path, out_dir))
    receipts = {
        "schema": RECEIPTS_SCHEMA,
        "outputs": [{"path": rel, "sha256": sha256_file(out_dir / rel)} for rel in EXPECTED_OUTPUTS if rel != "receipts.json"],
        "status": "MATCH" if packet["verification"]["verdict"] == "MATCH" and report["status"] == "MATCH" else "DRIFT",
    }
    write_json(out_dir / "receipts.json", receipts)
    return {"out_dir": str(out_dir), "outputs": EXPECTED_OUTPUTS, "status": receipts["status"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = build_bundle(Path(args.fixture), Path(args.out))
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
