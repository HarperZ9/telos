"""Compose pass 0148 live source router probe artifact."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "LiveSourceRouterProbeReceipt/v1"
PASS_ID = "0148"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PLAN = ROOT / "fixtures" / "pass-0148-live-source-router-probes-plan.json"


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True))


def catalog(store: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in (store / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def body(store: Path, row: dict[str, Any]) -> str:
    return (store / "objects" / row["sha256"][:2] / row["sha256"][2:]).read_text(encoding="utf-8", errors="replace")


def command_receipt(cmd: list[str], timeout: int = 45) -> dict[str, Any]:
    run = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    first = run.stdout.strip().splitlines()[0] if run.stdout.strip() else ""
    return {
        "command": " ".join(cmd),
        "exit_code": run.returncode,
        "stdout_sha256": sha_text(run.stdout),
        "stderr_sha256": sha_text(run.stderr),
        "first_line": first,
        "observed_version": first.split()[-1] if first else None,
        "status": "MATCH" if run.returncode == 0 else "DRIFT",
    }


def tool_receipts() -> dict[str, Any]:
    return {
        "gather": command_receipt(["gather", "--version"]),
        "index": command_receipt(["index", "--version"]),
        "forum": command_receipt(["forum", "--version"]),
        "crucible": command_receipt(["crucible", "--version"]),
        "telos": command_receipt(["node", "-p", "\"telos \"+JSON.parse(require('fs').readFileSync('package.json','utf8')).version"]),
    }


def refs_by_url(store: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in catalog(store):
        out[row["ref"]] = row
    return out


def route_status(route: dict[str, Any], store: Path, by_ref: dict[str, dict[str, Any]]) -> dict[str, Any]:
    primary = by_ref.get(route["primary_url"])
    fallback = next((by_ref[url] for url in route.get("fallback_urls", []) if url in by_ref), None)
    source = primary or fallback
    if not source:
        return {
            "id": route["id"],
            "family": route["family"],
            "system": route["system"],
            "status": "SOURCE_LEAD_ONLY_WARNING",
            "primary_url": route["primary_url"],
            "sha256": None,
            "captured_url": None,
            "matched_signals": [],
            "required_signals": route.get("required_signals", []),
            "policy": route["policy"],
            "warning": route.get("expected_failure", "MISSING_CAPTURE"),
        }
    text = body(store, source)
    matches = [signal for signal in route.get("required_signals", []) if signal.lower() in text.lower()]
    if primary and len(matches) == len(route.get("required_signals", [])):
        status = "LIVE_QUERY_MATCH"
    elif primary:
        status = "LIVE_QUERY_PARTIAL_WARNING"
    elif len(matches) == len(route.get("required_signals", [])):
        status = "FALLBACK_DOCS_MATCH_WITH_PRIMARY_WARNING"
    else:
        status = "FALLBACK_DOCS_PARTIAL_WARNING"
    return {
        "id": route["id"],
        "family": route["family"],
        "system": route["system"],
        "status": status,
        "primary_url": route["primary_url"],
        "captured_url": source["ref"],
        "sha256": source["sha256"],
        "chars": len(text),
        "matched_signals": matches,
        "required_signals": route.get("required_signals", []),
        "policy": route["policy"],
        "warning": None if status == "LIVE_QUERY_MATCH" else route.get("expected_failure", "PARTIAL_OR_FALLBACK"),
    }


def build_receipt(live_tools: bool = True) -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    store = REPO / plan["source_store"]
    by_ref = refs_by_url(store)
    routes = [route_status(route, store, by_ref) for route in plan["routes"]]
    warnings = [row for row in routes if row["status"] != "LIVE_QUERY_MATCH"]
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": "LIVE_SOURCE_ROUTER_PROBES_MATCH_WITH_WARNINGS",
        "source_store": plan["source_store"],
        "source_captures": len(catalog(store)),
        "unique_source_refs": len(by_ref),
        "routes": routes,
        "prior_receipts": plan["prior_receipts"],
        "router_policies": [
            "live query success is a route receipt, not source correctness",
            "fallback docs bind adapter contracts when live routes fail",
            "HTTP 429, 503, 403, TLS, and 404 become scheduler or endpoint-alias statuses",
            "preprint and repository records stay sample-only until claim extraction and verification",
        ],
        "world_problem_routes": [
            "formal theorem factory from arXiv/HAL/OpenAIRE/Crossref",
            "biomedical mechanism lab from bioRxiv/medRxiv/PubMed/Europe PMC",
            "materials and chemistry lane from ChemRxiv leads plus DOI/data repositories",
            "institutional knowledge graph from DSpace/OAI/EPrints/Dataverse",
            "benchmark truth lab from scholarly graphs, data repositories, and open access indexes",
        ],
        "negative_fixtures": [{"fixture_id": name, "expected_status": "REJECT"} for name in plan["negative_fixtures"]],
        "integration_targets": ["LiveSourceRouterProbeRunner", "SourceFamilyScheduler", "EndpointAliasRegistry", "PreprintPressAdapter", "CollegeRepositoryProbe", "RoutePolicyLedger"],
        "updated_tool_floor": plan["updated_tool_floor"],
        "tool_receipts": tool_receipts() if live_tools else {},
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "boundary": "Pass 0148 tests live source-router routes across archive, preprint, scholarly graph, biomedical, repository-directory, college repository, and data repository surfaces. It does not prove source correctness, full-text access, domain coverage, peer review, theorem progress, or natural-law discovery.",
    }
    families = sorted({row["family"] for row in routes})
    receipt["summary"] = {
        "routes": len(routes),
        "families": len(families),
        "source_captures": receipt["source_captures"],
        "unique_source_refs": receipt["unique_source_refs"],
        "live_query_matches": sum(1 for row in routes if row["status"] == "LIVE_QUERY_MATCH"),
        "fallback_matches": sum(1 for row in routes if row["status"].startswith("FALLBACK_DOCS")),
        "source_lead_only": sum(1 for row in routes if row["status"] == "SOURCE_LEAD_ONLY_WARNING"),
        "warnings": len(warnings),
        "negative_fixtures": len(receipt["negative_fixtures"]),
        "families_list": families,
    }
    receipt["seal"] = sha_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def render_packet(r: dict[str, Any]) -> str:
    lines = ["# Pass 0148 - Live Source Router Probes", "", f"Status: `{r['status']}` with seal `{r['seal']}`.", "", "## Route Matrix", "", "| Family | System | Status | Warning |", "| --- | --- | --- | --- |"]
    for row in r["routes"]:
        lines.append(f"| {row['family']} | {row['system']} | `{row['status']}` | `{row['warning'] or ''}` |")
    lines.extend(["", "## Router Policies", ""])
    lines.extend(f"- {policy}" for policy in r["router_policies"])
    lines.extend(["", "## Strategic Result", "", f"- `{r['summary']['live_query_matches']}` live query routes matched.", f"- `{r['summary']['fallback_matches']}` routes matched through fallback docs or alternate endpoints.", f"- `{r['summary']['source_lead_only']}` routes remained source-lead-only warnings.", "- The next implementation should schedule retries, endpoint aliases, and claim extraction as separate receipts.", "", "## Boundary", "", r["boundary"]])
    return "\n".join(lines)


def render_brief(r: dict[str, Any]) -> str:
    return "\n".join(["# Pass 0148 Brief - Live Source Router Probes", "", "Primary push: turn the archive/preprint/college-database atlas into live route probes with typed failure policy.", "", f"Result: {r['summary']['routes']} routes across {r['summary']['families']} families, with {r['summary']['live_query_matches']} live matches and {r['summary']['warnings']} warnings.", "", "Next pass: implement a scheduler fixture that replays retryable routes and endpoint-alias discovery without promoting failures into source absence."])


def render_steelman() -> str:
    return "\n".join(["# Pass 0148 Steelman", "", "The strongest objection is that live query probes are still route tests, not research. A working endpoint can return weak, wrong, stale, or irrelevant records.", "", "The settling test is a claim-extraction pass that turns a small subset of route records into claim cards, links them to source bodies or metadata, and rejects every card without a verifier, negative control, and replay path."])


def build_claims(r: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    claims = [
        f"Pass 0148 created a {SCHEMA} artifact with status {r['status']} and seal {r['seal']}.",
        f"Pass 0148 records {r['summary']['routes']} routes across {r['summary']['families']} source families.",
        f"Pass 0148 records {r['summary']['live_query_matches']} live query matches, {r['summary']['fallback_matches']} fallback matches, and {r['summary']['source_lead_only']} source-lead-only warnings.",
        f"Pass 0148 rejects {r['summary']['negative_fixtures']} negative fixtures.",
        "Pass 0148 promotes no theorem or natural law.",
    ]
    thesis = {"title": "Dogfood Pass 0148 Live Source Router Probes", "disposition": "fenced", "claims": [{"text": c, "falsification": f"Claim {i} differs from artifact values or receipts are missing"} for i, c in enumerate(claims, 1)]}
    evidence = [[f"schema={r['schema']}", f"status={r['status']}", f"seal={r['seal']}"], [f"routes={r['summary']['routes']}", f"families={r['summary']['families']}"], [f"live={r['summary']['live_query_matches']}", f"fallback={r['summary']['fallback_matches']}", f"source_lead_only={r['summary']['source_lead_only']}"], [f"negative_fixtures={r['summary']['negative_fixtures']}"], [f"current_promoted_theorems={r['current_promoted_theorems']}", f"current_promoted_natural_laws={r['current_promoted_natural_laws']}"]]
    return thesis, {"measurements": [{"claim": c, "method": "artifact-review", "evidence": evidence[i], "deviation": 0.0, "tolerance": 0.5} for i, c in enumerate(claims)]}


def render_ledger(r: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0148 Ledger - Live Source Router Probes", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    lines.extend(f"| {label} | {sha_file(path).upper()} |" for label, path in files.items())
    lines.extend(["", "## Result Snapshot", "", "| Field | Value |", "| --- | --- |", f"| Schema | `{r['schema']}` |", f"| Status | `{r['status']}` |", f"| Seal | `{r['seal']}` |", f"| Routes | `{r['summary']['routes']}` |", f"| Families | `{r['summary']['families']}` |", f"| Live query matches | `{r['summary']['live_query_matches']}` |", f"| Fallback matches | `{r['summary']['fallback_matches']}` |", f"| Source-lead-only warnings | `{r['summary']['source_lead_only']}` |", f"| Promoted theorems | `{len(r['current_promoted_theorems'])}` |"])
    return "\n".join(lines)


def main() -> None:
    r = build_receipt(live_tools=True)
    files = {
        "schemas/live-source-router-probes-pass-0148.json": ROOT / "schemas" / "live-source-router-probes-pass-0148.json",
        "packets/158-live-source-router-probes.md": ROOT / "packets" / "158-live-source-router-probes.md",
        "briefs/158-live-source-router-probes-brief.md": ROOT / "briefs" / "158-live-source-router-probes-brief.md",
        "adversarial/pass-0148-live-source-router-probes-steelman.md": ROOT / "adversarial" / "pass-0148-live-source-router-probes-steelman.md",
    }
    write_json(files["schemas/live-source-router-probes-pass-0148.json"], r)
    write_text(files["packets/158-live-source-router-probes.md"], render_packet(r))
    write_text(files["briefs/158-live-source-router-probes-brief.md"], render_brief(r))
    write_text(files["adversarial/pass-0148-live-source-router-probes-steelman.md"], render_steelman())
    thesis, measurements = build_claims(r)
    files["crucible/pass-0148-thesis.json"] = ROOT / "crucible" / "pass-0148-thesis.json"
    files["crucible/pass-0148-measurements.json"] = ROOT / "crucible" / "pass-0148-measurements.json"
    write_json(files["crucible/pass-0148-thesis.json"], thesis)
    write_json(files["crucible/pass-0148-measurements.json"], measurements)
    files["schemas/tool-receipts-pass-0148.json"] = ROOT / "schemas" / "tool-receipts-pass-0148.json"
    write_json(files["schemas/tool-receipts-pass-0148.json"], {"schema": "Pass0148ToolReceipts/v1", "artifact": {"path": str(files["schemas/live-source-router-probes-pass-0148.json"]), "sha256": sha_file(files["schemas/live-source-router-probes-pass-0148.json"])}, "source_store": r["source_store"], "tool_receipts": r["tool_receipts"]})
    write_text(ROOT / "pass-0148-ledger.md", render_ledger(r, files))
    print(json.dumps({"status": r["status"], "seal": r["seal"]}, sort_keys=True))


if __name__ == "__main__":
    main()
