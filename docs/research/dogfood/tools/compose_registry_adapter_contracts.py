"""Compose pass 0143 registry adapter contract artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "RegistryAdapterContractsReceipt/v1"
PASS_ID = "0143"
STATUS = "REGISTRY_ADAPTER_CONTRACTS_MATCH"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
FIXTURE = ROOT / "fixtures" / "pass-0143-adapter-contract-fixtures.json"
SOURCE_REGISTRY = ROOT / "schemas" / "source-registry-federation-pass-0142.json"


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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_match(sources: list[dict[str, Any]], needle: str) -> dict[str, Any]:
    low = needle.lower()
    for row in sources:
        hay = f"{row.get('system', '')} {row.get('url', '')}".lower()
        if low in hay:
            return row
    return {"system": needle, "url": None, "sha256": None, "family": "source_lead", "evidence_status": "SOURCE_NOT_FOUND"}


def attach_source(record: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    row = source_match(sources, record["source_system_contains"])
    out = dict(record)
    out["source_system"] = row.get("system")
    out["source_url"] = row.get("url")
    out["source_family"] = row.get("family")
    out["source_body_sha256"] = row.get("sha256")
    out["evidence_status"] = row.get("evidence_status")
    out["license_or_terms_ref"] = "required_before_reuse"
    out["freshness_time"] = "capture_or_endpoint_time_required"
    out["endpoint_url_ref"] = "must_be_verified_before_harvest"
    out["failure_codes"] = [] if row.get("evidence_status") == "GATHER_VERIFIED" else ["SOURCE_LEAD_OR_WARNING"]
    out["verifier_ref"] = "pass-0143-validator"
    return out


def command_receipt(cmd: list[str], timeout: int = 30) -> dict[str, Any]:
    try:
        run = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        stdout = run.stdout.strip()
        return {
            "command": " ".join(cmd),
            "exit_code": run.returncode,
            "stdout_first_line": stdout.splitlines()[0] if stdout else "",
            "stdout_sha256": sha_text(run.stdout),
            "stderr_sha256": sha_text(run.stderr),
        }
    except Exception as exc:  # pragma: no cover - defensive receipt path
        return {"command": " ".join(cmd), "exit_code": 999, "stdout_first_line": "", "stdout_sha256": sha_text(""), "stderr_sha256": sha_text(str(exc))}


def observed_tool_floor() -> dict[str, Any]:
    commands = {
        "gather": ["gather", "--version"],
        "index": ["index", "--version"],
        "forum": ["forum", "--version"],
        "crucible": ["crucible", "--version"],
        "telos": ["node", "-p", "'telos '+JSON.parse(require('fs').readFileSync('package.json','utf8')).version"],
    }
    receipts = {name: command_receipt(cmd) for name, cmd in commands.items()}
    for name, row in receipts.items():
        parts = row["stdout_first_line"].split()
        row["observed_version"] = parts[-1] if parts else None
        row["status"] = "MATCH" if row["exit_code"] == 0 and row["observed_version"] else "UNVERIFIABLE"
        row["tool"] = name
    return receipts


def build_receipt(live_tools: bool = True) -> dict[str, Any]:
    fixture = load_json(FIXTURE)
    source_registry = load_json(SOURCE_REGISTRY)
    sources = source_registry["source_rows"]
    repo_records = [attach_source(row, sources) for row in fixture["repository_directory_fixtures"]]
    graph_records = [attach_source(row, sources) for row in fixture["scholarly_graph_fixtures"]]
    observed = observed_tool_floor() if live_tools else {}
    expected = fixture["updated_tool_floor"]
    mismatches = [
        name for name, info in observed.items()
        if name in expected and info.get("observed_version") != expected[name]["version"]
    ]
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": STATUS if not mismatches else "REGISTRY_ADAPTER_CONTRACTS_TOOL_FLOOR_DRIFT",
        "fixture_schema": fixture["schema"],
        "source_registry_ref": {
            "schema": source_registry["schema"],
            "pass": source_registry["pass"],
            "status": source_registry["status"],
            "seal": source_registry["seal"],
            "source_rows": source_registry["gather_summary"]["total_source_rows"],
            "usable_captures": source_registry["gather_summary"]["usable_captures"],
        },
        "contracts": fixture["contracts"],
        "repository_directory_records": repo_records,
        "scholarly_graph_records": graph_records,
        "join_keys": fixture["join_keys"],
        "negative_fixtures": fixture["negative_fixtures"],
        "updated_tool_floor_expected": expected,
        "updated_tool_floor_observed": observed,
        "tool_floor_mismatches": mismatches,
        "adapter_pipeline": [
            {"stage": "Gather", "role": "capture source URL, body hash, local docs, and warning state"},
            {"stage": "Index", "role": "bind adapter contract to workspace and source-registry context"},
            {"stage": "Forum", "role": "route source, domain, legal/license, and proof-packet validation lanes"},
            {"stage": "Telos", "role": "record adapter actions, admission decisions, and loop-ledger receipts"},
            {"stage": "Crucible", "role": "reject negative fixtures and verify contract measurements"},
        ],
        "first_workbench": {
            "name": "one_institution_claim_graph",
            "steps": [
                "choose one university or lab",
                "resolve ROR identity",
                "discover repositories through directory records",
                "harvest OAI-PMH or REST endpoint candidates",
                "join works through Crossref/DataCite/OpenAlex/Semantic Scholar",
                "emit claim-to-experiment packet with negative fixtures"
            ],
        },
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "boundary": "Pass 0143 defines adapter contracts and fixtures. It does not certify live repository coverage, DOI correctness, full-text access, market uniqueness, theorem proof, or natural-law discovery.",
    }
    receipt["seal"] = sha_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def render_packet(r: dict[str, Any]) -> str:
    lines = [
        "# Pass 0143 - Registry Adapter Contracts",
        "",
        "## Summary",
        "",
        f"Status: `{r['status']}`. This pass turns pass 0142 source-registry breadth into `{len(r['contracts'])}` adapter contracts, `{len(r['repository_directory_records'])}` repository-directory fixtures, `{len(r['scholarly_graph_records'])}` scholarly-graph fixtures, and `{len(r['negative_fixtures'])}` rejection fixtures.",
        "",
        "The practical goal is a reusable intake spine for massive research: every source row must carry a source hash, identifier policy, freshness boundary, license/terms reference, verifier ref, and explicit failure codes before it can feed proof packets.",
        "",
        "## Contracts",
        "",
    ]
    for contract in r["contracts"]:
        lines.extend([
            f"### {contract['adapter']}",
            "",
            f"- Product: `{contract['market_product']}`",
            f"- Purpose: {contract['purpose']}",
            f"- Required fields: `{len(contract['required_fields'])}`",
            f"- Rejects: {', '.join(contract['rejects'])}",
            "",
        ])
    lines.extend(["## First Workbench", ""])
    lines.append(f"`{r['first_workbench']['name']}`")
    for step in r["first_workbench"]["steps"]:
        lines.append(f"- {step}")
    lines.extend(["", "## Pipeline", ""])
    lines.extend(f"- {item['stage']}: {item['role']}" for item in r["adapter_pipeline"])
    lines.extend(["", "## Boundary", "", r["boundary"]])
    return "\n".join(lines)


def render_brief(r: dict[str, Any]) -> str:
    return "\n".join([
        "# Pass 0143 Brief - Registry Adapter Contracts",
        "",
        "Primary push: implement the adapter contract layer before attempting larger source crawling or theorem solving.",
        "",
        f"Shape: {len(r['repository_directory_records'])} repository-directory fixtures, {len(r['scholarly_graph_records'])} scholarly-graph fixtures, {len(r['join_keys'])} join keys, and {len(r['negative_fixtures'])} negative fixtures.",
        "",
        "Why it matters: large-scale research tools fail when source discovery, identifier joins, license state, version state, and verification verdicts are separated. These contracts make each join replayable before downstream AI, BuildLang/buildc kernels, or proof assistants consume it.",
        "",
        "Next pass: instantiate one live, bounded institution graph from ROR plus repository-directory plus scholarly-graph adapters, while preserving all non-promotion boundaries.",
    ])


def render_steelman() -> str:
    return "\n".join([
        "# Pass 0143 Steelman",
        "",
        "The strongest objection is that adapter contracts can become schema theater: precise fields without proving that real APIs, stale records, rate limits, licensing terms, and broken identifiers can be joined at scale.",
        "",
        "The settling test is a bounded live run: select one institution, one repository endpoint, one DOI work, and one dataset; produce a packet where every join has a source receipt, freshness time, failure mode, and Crucible verdict.",
        "",
        "Until that live run exists, pass 0143 should be read as integration design and negative-control scaffolding, not proof of coverage or correctness.",
    ])


def render_ledger(r: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0143 Ledger - Registry Adapter Contracts", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    for label, path in files.items():
        lines.append(f"| {label} | {sha_file(path).upper()} |")
    lines.extend(["", "## Result Snapshot", "", "| Field | Value |", "| --- | --- |"])
    rows = {
        "Schema": r["schema"],
        "Status": r["status"],
        "Seal": r["seal"],
        "Contracts": len(r["contracts"]),
        "Repository fixtures": len(r["repository_directory_records"]),
        "Scholarly fixtures": len(r["scholarly_graph_records"]),
        "Join keys": len(r["join_keys"]),
        "Negative fixtures": len(r["negative_fixtures"]),
        "Tool floor mismatches": len(r["tool_floor_mismatches"]),
        "Promoted theorems": 0,
    }
    for key, value in rows.items():
        lines.append(f"| {key} | `{value}` |")
    return "\n".join(lines)


def build_claims(r: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    claims = [
        f"Pass 0143 created a {SCHEMA} artifact with status {r['status']} and seal {r['seal']}.",
        f"Pass 0143 records {len(r['contracts'])} adapter contracts, {len(r['repository_directory_records'])} repository fixtures, and {len(r['scholarly_graph_records'])} scholarly graph fixtures.",
        f"Pass 0143 records {len(r['join_keys'])} join keys and {len(r['negative_fixtures'])} negative fixtures.",
        f"Pass 0143 references pass 0142 source registry seal {r['source_registry_ref']['seal']} with {r['source_registry_ref']['source_rows']} source rows.",
        f"Pass 0143 observed {len(r['updated_tool_floor_observed'])} updated tool-floor receipts with {len(r['tool_floor_mismatches'])} version mismatches.",
        "Pass 0143 promotes no theorem or natural law.",
    ]
    thesis = {"title": "Dogfood Pass 0143 Registry Adapter Contracts", "disposition": "fenced", "claims": [{"text": text, "falsification": f"Claim {i} differs from pass 0143 artifact values or receipts are missing"} for i, text in enumerate(claims, 1)]}
    evidence = [
        [f"schema={r['schema']}", f"status={r['status']}", f"seal={r['seal']}"],
        [f"contracts={len(r['contracts'])}", f"repo_records={len(r['repository_directory_records'])}", f"graph_records={len(r['scholarly_graph_records'])}"],
        [f"join_keys={len(r['join_keys'])}", f"negative_fixtures={len(r['negative_fixtures'])}"],
        [f"source_registry_ref={r['source_registry_ref']}"],
        [f"observed_tool_floor={r['updated_tool_floor_observed']}", f"mismatches={r['tool_floor_mismatches']}"],
        [f"current_promoted_theorems={r['current_promoted_theorems']}", f"current_promoted_natural_laws={r['current_promoted_natural_laws']}"],
    ]
    measurements = {"measurements": [{"claim": text, "method": "artifact-review", "evidence": evidence[i], "deviation": 0.0, "tolerance": 0.5} for i, text in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    r = build_receipt(live_tools=True)
    files = {
        "schemas/registry-adapter-contracts-pass-0143.json": ROOT / "schemas" / "registry-adapter-contracts-pass-0143.json",
        "packets/153-registry-adapter-contracts.md": ROOT / "packets" / "153-registry-adapter-contracts.md",
        "briefs/153-registry-adapter-contracts-brief.md": ROOT / "briefs" / "153-registry-adapter-contracts-brief.md",
        "adversarial/pass-0143-registry-adapter-contracts-steelman.md": ROOT / "adversarial" / "pass-0143-registry-adapter-contracts-steelman.md",
    }
    write_json(files["schemas/registry-adapter-contracts-pass-0143.json"], r)
    write_text(files["packets/153-registry-adapter-contracts.md"], render_packet(r))
    write_text(files["briefs/153-registry-adapter-contracts-brief.md"], render_brief(r))
    write_text(files["adversarial/pass-0143-registry-adapter-contracts-steelman.md"], render_steelman())
    thesis, measurements = build_claims(r)
    files["crucible/pass-0143-thesis.json"] = ROOT / "crucible" / "pass-0143-thesis.json"
    files["crucible/pass-0143-measurements.json"] = ROOT / "crucible" / "pass-0143-measurements.json"
    write_json(files["crucible/pass-0143-thesis.json"], thesis)
    write_json(files["crucible/pass-0143-measurements.json"], measurements)
    tool = {"schema": "Pass0143ToolReceipts/v1", "artifact": {"path": str(files["schemas/registry-adapter-contracts-pass-0143.json"]), "sha256": sha_file(files["schemas/registry-adapter-contracts-pass-0143.json"])}, "fixture": {"path": str(FIXTURE), "sha256": sha_file(FIXTURE)}, "source_registry": r["source_registry_ref"], "updated_tool_floor_observed": r["updated_tool_floor_observed"]}
    files["schemas/tool-receipts-pass-0143.json"] = ROOT / "schemas" / "tool-receipts-pass-0143.json"
    write_json(files["schemas/tool-receipts-pass-0143.json"], tool)
    write_text(ROOT / "pass-0143-ledger.md", render_ledger(r, files))
    print(json.dumps({"status": r["status"], "seal": r["seal"]}, sort_keys=True))


if __name__ == "__main__":
    main()
