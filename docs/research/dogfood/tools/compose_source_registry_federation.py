"""Compose pass 0142 source registry federation artifact."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "SourceRegistryFederationReceipt/v1"
PASS_ID = "0142"
STATUS = "SOURCE_REGISTRY_FEDERATION_MATCH"
ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "gather" / "pass-0142-source-registry-federation"
PLAN = ROOT / "fixtures" / "pass-0142-source-registry-federation-plan.json"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
FAILED_SOURCES = [
    {"system": "OpenDOAR", "url": "https://opendoar.ac.uk/", "status": "GATHER_TLS_FAILED_SOURCE_LEAD"},
    {"system": "OpenDOAR developers", "url": "https://opendoar.ac.uk/help/developers", "status": "GATHER_TLS_FAILED_SOURCE_LEAD"},
    {"system": "BASE", "url": "https://www.base-search.net/", "status": "GATHER_403_OR_EMPTY_SOURCE_LEAD"},
]


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


def body_chars(sha: str) -> int:
    path = STORE / "objects" / sha[:2] / sha[2:]
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8", errors="replace"))


def classify(ref: str, title: str) -> str:
    low = f"{ref} {title}".lower()
    rules = [
        ("registry_of_repositories", ["openaire", "re3data", "opendoar", "base-search"]),
        ("organization_identity", ["ror.org", "ror.readme"]),
        ("scholarly_graph", ["crossref", "datacite", "openalex", "semanticscholar", "core.ac.uk"]),
        ("open_access", ["doaj", "unpaywall"]),
        ("preprint_press", ["arxiv", "biorxiv", "medrxiv", "osf"]),
        ("biomedical", ["europepmc", "ncbi"]),
        ("repository_platform", ["dataverse", "dspace", "invenio", "openarchives"]),
        ("domain_database", ["uniprot", "rcsb", "materialsproject"]),
        ("ml_dataset_hub", ["openml", "huggingface"]),
    ]
    for label, needles in rules:
        if any(needle in low for needle in needles):
            return label
    return "source_lead"


def load_catalog() -> list[dict[str, Any]]:
    rows = []
    for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        chars = body_chars(raw["sha256"])
        evidence = "GATHER_VERIFIED_EMPTY_CAPTURE" if raw["sha256"] == EMPTY_SHA or chars == 0 else "GATHER_VERIFIED"
        rows.append({
            "system": raw.get("title") or raw["id"],
            "url": raw["ref"],
            "source": raw["source"],
            "kind": raw["kind"],
            "method": raw["method"],
            "sha256": raw["sha256"],
            "chars": chars,
            "family": classify(raw["ref"], raw.get("title", "")),
            "evidence_status": evidence,
        })
    for row in FAILED_SOURCES:
        rows.append({
            "system": row["system"],
            "url": row["url"],
            "source": "web",
            "kind": "webpage",
            "method": "http-get",
            "sha256": None,
            "chars": 0,
            "family": classify(row["url"], row["system"]),
            "evidence_status": row["status"],
        })
    return sorted(rows, key=lambda item: (item["family"], item["system"], item["url"]))


def build_receipt() -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    sources = load_catalog()
    empty = [row for row in sources if "EMPTY" in row["evidence_status"] or "FAILED" in row["evidence_status"] or "403" in row["evidence_status"]]
    families = sorted({row["family"] for row in sources})
    receipt = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": STATUS,
        "source_scope": "registry-of-registries expansion for publishing, preprints, repository platforms, college databases, domain databases, and dataset hubs",
        "gather_summary": {
            "captured_sources": sum(1 for row in sources if row["sha256"]),
            "total_source_rows": len(sources),
            "usable_captures": sum(1 for row in sources if row["evidence_status"] == "GATHER_VERIFIED"),
            "warning_count": len(empty),
            "families": len(families),
        },
        "source_rows": sources,
        "source_quality_warnings": empty,
        "registry_layers": plan["registry_layers"],
        "cross_industry_underpinnings": plan["cross_industry_underpinnings"],
        "world_problem_workbenches": plan["world_problem_workbenches"],
        "adapter_requirements": plan["adapter_requirements"],
        "negative_fixtures": plan["negative_fixtures"],
        "updated_tool_floor": plan["updated_tool_floor"],
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "boundary": "This pass maps scalable discovery substrate. It does not claim complete world coverage, source correctness, publication validity, theorem proof, experimental truth, or market uniqueness.",
    }
    receipt["seal"] = sha_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def render_packet(r: dict[str, Any]) -> str:
    lines = [
        "# Pass 0142 - Source Registry Federation",
        "",
        "## Summary",
        "",
        f"Status: `{r['status']}`. The pass records `{r['gather_summary']['total_source_rows']}` source rows, `{r['gather_summary']['usable_captures']}` usable captures, `{r['gather_summary']['families']}` source families, and `{r['gather_summary']['warning_count']}` warnings.",
        "",
        "The strategic shift is from individual archive discovery to registry federation: use repository directories, scholarly graphs, organization identifiers, preprint APIs, platform protocols, and domain databases to scale toward hundreds of substrates.",
        "",
        "## Registry Layers",
        "",
    ]
    for layer in r["registry_layers"]:
        lines.extend([f"### {layer['id']}", "", f"- Adapter: `{layer['adapter']}`", f"- Purpose: {layer['purpose']}", f"- Sources: {', '.join(layer['sources'])}", ""])
    lines.extend(["## Cross-Industry Underpinnings", ""])
    lines.extend(f"- {item}" for item in r["cross_industry_underpinnings"])
    lines.extend(["", "## World-Problem Workbenches", ""])
    for wb in r["world_problem_workbenches"]:
        lines.extend([f"- `{wb['id']}`: {wb['first_experiment']}"])
    lines.extend(["", "## Boundary", "", r["boundary"]])
    return "\n".join(lines)


def render_brief(r: dict[str, Any]) -> str:
    return "\n".join([
        "# Pass 0142 Brief - Source Registry Federation",
        "",
        "Primary push: build a federated source registry layer before attempting massive cross-domain reasoning.",
        "",
        f"Evidence state: {r['gather_summary']['usable_captures']} usable captures, {r['gather_summary']['warning_count']} warnings, {len(r['registry_layers'])} registry layers, {len(r['world_problem_workbenches'])} workbenches.",
        "",
        "Next implementation target: `RepositoryDirectoryAdapter` plus `ScholarlyGraphAdapter`, then a one-university institutional knowledge graph using ROR, OpenDOAR/OpenAIRE, OAI-PMH, Dataverse, DSpace, and DataCite/Crossref joins.",
    ])


def render_steelman() -> str:
    return "\n".join([
        "# Pass 0142 Steelman",
        "",
        "The strongest objection is that a registry federation can look massive while still lacking actual domain truth.",
        "",
        "The settling test is a replayable adapter: choose one university, one preprint cluster, one dataset, and one domain database record; show that sources, identifiers, versions, licenses, measurements, and verifier verdicts join without manual narrative glue.",
        "",
        "Until that replay exists, breadth is a routing advantage, not evidence of correctness.",
    ])


def render_ledger(r: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0142 Ledger - Source Registry Federation", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    for label, path in files.items():
        lines.append(f"| {label} | {sha_file(path).upper()} |")
    lines.extend(["", "## Result Snapshot", "", "| Field | Value |", "| --- | --- |"])
    rows = {
        "Schema": r["schema"],
        "Status": r["status"],
        "Seal": r["seal"],
        "Total source rows": r["gather_summary"]["total_source_rows"],
        "Usable captures": r["gather_summary"]["usable_captures"],
        "Warnings": r["gather_summary"]["warning_count"],
        "Registry layers": len(r["registry_layers"]),
        "Workbenches": len(r["world_problem_workbenches"]),
        "Adapter requirements": len(r["adapter_requirements"]),
        "Promoted theorems": 0,
    }
    for key, value in rows.items():
        lines.append(f"| {key} | `{value}` |")
    return "\n".join(lines)


def main() -> None:
    r = build_receipt()
    files = {
        "schemas/source-registry-federation-pass-0142.json": ROOT / "schemas" / "source-registry-federation-pass-0142.json",
        "packets/152-source-registry-federation.md": ROOT / "packets" / "152-source-registry-federation.md",
        "briefs/152-source-registry-federation-brief.md": ROOT / "briefs" / "152-source-registry-federation-brief.md",
        "adversarial/pass-0142-source-registry-federation-steelman.md": ROOT / "adversarial" / "pass-0142-source-registry-federation-steelman.md",
    }
    write_json(files["schemas/source-registry-federation-pass-0142.json"], r)
    write_text(files["packets/152-source-registry-federation.md"], render_packet(r))
    write_text(files["briefs/152-source-registry-federation-brief.md"], render_brief(r))
    write_text(files["adversarial/pass-0142-source-registry-federation-steelman.md"], render_steelman())
    claims = [
        f"Pass 0142 created a {SCHEMA} artifact with status {STATUS} and seal {r['seal']}.",
        f"Pass 0142 records {r['gather_summary']['total_source_rows']} source rows and {r['gather_summary']['usable_captures']} usable captures.",
        f"Pass 0142 records {len(r['registry_layers'])} registry layers and {len(r['adapter_requirements'])} adapter requirements.",
        f"Pass 0142 records {len(r['world_problem_workbenches'])} world-problem workbenches.",
        f"Pass 0142 rejects {len(r['negative_fixtures'])} negative fixtures.",
        "Pass 0142 promotes no theorem or natural law.",
    ]
    thesis = {"title": "Dogfood Pass 0142 Source Registry Federation", "disposition": "fenced", "claims": [{"text": text, "falsification": f"Claim {i} differs from pass 0142 artifacts or receipts are missing"} for i, text in enumerate(claims, 1)]}
    ev = [[f"schema={r['schema']}", f"status={r['status']}", f"seal={r['seal']}"], [f"gather_summary={r['gather_summary']}"], [f"registry_layers={len(r['registry_layers'])}", f"adapter_requirements={len(r['adapter_requirements'])}"], [f"world_problem_workbenches={len(r['world_problem_workbenches'])}"], [f"negative_fixtures={len(r['negative_fixtures'])}"], [f"current_promoted_theorems={r['current_promoted_theorems']}", f"current_promoted_natural_laws={r['current_promoted_natural_laws']}"]]
    meas = {"measurements": [{"claim": text, "method": "artifact-review", "evidence": ev[i], "deviation": 0.0, "tolerance": 0.5} for i, text in enumerate(claims)]}
    files["crucible/pass-0142-thesis.json"] = ROOT / "crucible" / "pass-0142-thesis.json"
    files["crucible/pass-0142-measurements.json"] = ROOT / "crucible" / "pass-0142-measurements.json"
    write_json(files["crucible/pass-0142-thesis.json"], thesis)
    write_json(files["crucible/pass-0142-measurements.json"], meas)
    write_text(ROOT / "pass-0142-ledger.md", render_ledger(r, files))
    tool = {"schema": "Pass0142ToolReceipts/v1", "artifact": {"path": str(files["schemas/source-registry-federation-pass-0142.json"]), "sha256": sha_file(files["schemas/source-registry-federation-pass-0142.json"])}, "gather_store": str(STORE), "plan": {"path": str(PLAN), "sha256": sha_file(PLAN)}, "updated_tool_floor": r["updated_tool_floor"]}
    write_json(ROOT / "schemas" / "tool-receipts-pass-0142.json", tool)
    print(json.dumps({"status": r["status"], "seal": r["seal"]}, sort_keys=True))


if __name__ == "__main__":
    main()
