"""Compose a buyer-facing demo manifest from a multi-trace graph."""
from __future__ import annotations

import argparse
import html
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "BuyerDemoManifest/v1"
PANES_SCHEMA = "BuyerDemoReviewPanes/v1"
FAILURES_SCHEMA = "BuyerDemoFailureVerdicts/v1"
RECEIPTS_SCHEMA = "BuyerDemoReceipts/v1"
OUTPUTS = [
    "manifest.json",
    "review-panes.json",
    "failure-verdicts.json",
    "replay-commands.md",
    "index.html",
    "receipts.json",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def pane_title(tool_class: str) -> str:
    titles = {
        "action_receipt": "Action Receipt",
        "browser_evidence": "Browser Evidence",
        "command_execution": "Command Execution",
        "gather": "Source Intake",
    }
    return titles.get(tool_class, tool_class.replace("_", " ").title())


def display_redaction(node: dict[str, Any]) -> str:
    if node.get("redaction_status") == "redacted":
        return "redacted"
    return "hash_only"


def review_panes(graph: dict[str, Any]) -> dict[str, Any]:
    panes = []
    for order, node in enumerate(graph["nodes"], start=1):
        panes.append({
            "display_redaction": display_redaction(node),
            "durable_receipt_hash": node["durable_receipt_hash"],
            "durable_receipt_kind": node["durable_receipt_kind"],
            "durable_receipt_ref": node["durable_receipt_ref"],
            "order": order,
            "pane_id": f"pane-{order:02d}-{node['tool_class']}",
            "span_ref": node["span_ref"],
            "title": pane_title(node["tool_class"]),
            "tool_class": node["tool_class"],
            "verdict": "MATCH",
        })
    return {"schema": PANES_SCHEMA, "panes": panes, "status": "MATCH"}


def failure_verdicts(graph: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for row in graph["negative_report"]["rows"]:
        rows.append({
            "fixture_id": row["fixture_id"],
            "observed_failure_codes": row["observed_failure_codes"],
            "observed_status": row["observed_status"],
            "public_label": row["fixture_id"].replace("_", " "),
            "status": row["status"],
        })
    return {
        "schema": FAILURES_SCHEMA,
        "negative_fixture_count": graph["negative_fixture_count"],
        "negative_match_count": graph["negative_match_count"],
        "negative_pass_observed_count": graph["negative_pass_observed_count"],
        "rows": rows,
        "status": "MATCH" if all(row["status"] == "MATCH" for row in rows) else "DRIFT",
    }


def replay_commands(graph_path: Path, out_dir: Path) -> str:
    return f"""# Replay Commands

```powershell
python docs\\research\\dogfood\\tools\\build_multitrace_causality_graph.py --spans docs\\research\\dogfood\\fixtures\\multitrace-causality-spans-pass-0055.json --source-binding docs\\research\\dogfood\\schemas\\source-evidence-binding-pass-0028.json --trace-join docs\\research\\dogfood\\schemas\\otel-trace-receipt-join-pass-0054.json --tool-receipts docs\\research\\dogfood\\schemas\\tool-receipts-pass-0054.json --out docs\\research\\dogfood\\schemas\\multitrace-causality-graph-pass-0055.json
python docs\\research\\dogfood\\tools\\compose_buyer_demo_manifest.py --graph {graph_path} --out {out_dir}
python docs\\research\\dogfood\\tools\\test_buyer_demo_manifest.py
```
"""


def render_html(manifest: dict[str, Any], panes: dict[str, Any], failures: dict[str, Any]) -> str:
    pane_rows = "\n".join(
        "<tr>"
        f"<td>{pane['order']}</td>"
        f"<td>{html.escape(pane['title'])}</td>"
        f"<td><code>{html.escape(pane['durable_receipt_kind'])}</code></td>"
        f"<td>{html.escape(pane['display_redaction'])}</td>"
        f"<td>{html.escape(pane['verdict'])}</td>"
        "</tr>"
        for pane in panes["panes"]
    )
    failure_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(row['fixture_id'])}</td>"
        f"<td>{html.escape(', '.join(row['observed_failure_codes']))}</td>"
        f"<td>{html.escape(row['status'])}</td>"
        "</tr>"
        for row in failures["rows"]
    )
    return f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>Multi-Trace Causality Demo</title>
<style>
body {{ color: #111; font-family: system-ui, sans-serif; margin: 2rem; }}
table {{ border-collapse: collapse; margin-block: 1rem 2rem; width: 100%; }}
td, th {{ border: 1px solid #bbb; padding: .45rem; text-align: left; vertical-align: top; }}
code {{ background: #f1f1f1; padding: .1rem .25rem; }}
</style>
<h1>Multi-Trace Causality Demo</h1>
<p>Status: <code>{html.escape(manifest['status'])}</code></p>
<p>Production ready: <code>{str(manifest['demo_summary']['production_ready']).lower()}</code></p>
<h2>Review Panes</h2>
<table><thead><tr><th>#</th><th>Pane</th><th>Receipt kind</th><th>Display</th><th>Verdict</th></tr></thead><tbody>{pane_rows}</tbody></table>
<h2>Failure Verdicts</h2>
<table><thead><tr><th>Fixture</th><th>Failure code</th><th>Status</th></tr></thead><tbody>{failure_rows}</tbody></table>
</html>
"""


def manifest(graph_path: Path, graph: dict[str, Any], panes: dict[str, Any], failures: dict[str, Any]) -> dict[str, Any]:
    replay_count = 3
    demo_summary = {
        "failure_verdict_count": failures["negative_fixture_count"],
        "production_ready": False,
        "public_review_ready": graph["status"] == "MULTITRACE_CAUSALITY_GRAPH_MATCH" and panes["status"] == "MATCH",
        "replay_command_count": replay_count,
        "review_pane_count": len(panes["panes"]),
    }
    value = {
        "schema": SCHEMA,
        "current_promoted_natural_laws": [],
        "demo_id": "multitrace-causality-demo-pass-0056",
        "demo_summary": demo_summary,
        "generated_on": "2026-07-01",
        "graph_ref": {"path": str(graph_path), "sha256": sha256_file(graph_path), "status": graph["status"]},
        "non_promotion_statement": "Pass 0056 proves a local buyer-facing demo manifest over existing dogfood receipts. It does not prove live production telemetry, customer adoption, scientific truth, or any natural law.",
        "pass": "0056",
        "status": "BUYER_DEMO_MANIFEST_MATCH" if demo_summary["public_review_ready"] and failures["status"] == "MATCH" else "BUYER_DEMO_MANIFEST_DRIFT",
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
    }
    value["manifest_hash"] = sha256_obj(value)
    return value


def compose(graph_path: Path, out_dir: Path) -> dict[str, Any]:
    graph = read_json(graph_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    panes = review_panes(graph)
    failures = failure_verdicts(graph)
    demo_manifest = manifest(graph_path, graph, panes, failures)
    write_json(out_dir / "manifest.json", demo_manifest)
    write_json(out_dir / "review-panes.json", panes)
    write_json(out_dir / "failure-verdicts.json", failures)
    write_text(out_dir / "replay-commands.md", replay_commands(graph_path, out_dir))
    write_text(out_dir / "index.html", render_html(demo_manifest, panes, failures))
    receipts = {
        "schema": RECEIPTS_SCHEMA,
        "outputs": [{"path": rel, "sha256": sha256_file(out_dir / rel)} for rel in OUTPUTS if rel != "receipts.json"],
        "status": "MATCH" if demo_manifest["status"] == "BUYER_DEMO_MANIFEST_MATCH" else "DRIFT",
    }
    write_json(out_dir / "receipts.json", receipts)
    return {"out_dir": str(out_dir), "outputs": OUTPUTS, "status": receipts["status"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = compose(Path(args.graph), Path(args.out))
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
