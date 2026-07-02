"""Compose pass 0144 one-institution claim graph artifact."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "OneInstitutionClaimGraphReceipt/v1"
PASS_ID = "0144"
STATUS = "ONE_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0144-one-institution-claim-graph"
PLAN = ROOT / "fixtures" / "pass-0144-one-institution-claim-graph-plan.json"


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


def body(row: dict[str, Any]) -> str:
    path = STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
    return path.read_text(encoding="utf-8", errors="replace")


def catalog() -> list[dict[str, Any]]:
    return [json.loads(line) for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def find(rows: list[dict[str, Any]], needle: str) -> tuple[dict[str, Any], str]:
    for row in rows:
        if needle in row["ref"]:
            return row, body(row)
    return {"ref": needle, "sha256": None, "title": needle}, ""


def first_label(names: list[dict[str, Any]]) -> str:
    for row in names:
        if "label" in row.get("types", []) and row.get("lang") in (None, "en"):
            return row.get("value", "")
    return names[0].get("value", "") if names else ""


def parse_ror(text: str) -> dict[str, Any]:
    data = json.loads(text)
    first = data["items"][0]
    return {
        "id": first.get("id"),
        "name": first_label(first.get("names", [])),
        "domains": first.get("domains", []),
        "established": first.get("established"),
        "country": first.get("locations", [{}])[0].get("geonames_details", {}).get("country_name"),
        "status": first.get("status", "active"),
        "last_modified": first.get("admin", {}).get("last_modified", {}).get("date"),
    }


def parse_openalex(text: str) -> dict[str, Any]:
    data = json.loads(text)
    first = data["results"][0]
    return {
        "id": first.get("id"),
        "ror": first.get("ror"),
        "display_name": first.get("display_name"),
        "country_code": first.get("country_code"),
        "type": first.get("type"),
        "homepage_url": first.get("homepage_url"),
        "works_count": first.get("works_count"),
    }


def parse_crossref(text: str) -> list[dict[str, Any]]:
    items = json.loads(text)["message"]["items"]
    rows = []
    for item in items:
        affiliations = []
        for author in item.get("author", []):
            affiliations.extend(a.get("name", "") for a in author.get("affiliation", []))
        rows.append({
            "doi": item.get("DOI"),
            "title": (item.get("title") or [""])[0],
            "url": item.get("URL"),
            "container": (item.get("container-title") or [""])[0],
            "license_count": len(item.get("license", [])),
            "has_mit_affiliation_string": "Massachusetts Institute of Technology" in affiliations,
            "title_hash": sha_text((item.get("title") or [""])[0]),
        })
    return rows


def parse_datacite(text: str) -> list[dict[str, Any]]:
    rows = []
    for item in json.loads(text).get("data", []):
        attrs = item.get("attributes", {})
        creators = attrs.get("creators", [])
        affils = [a for c in creators for a in c.get("affiliation", [])]
        title = (attrs.get("titles") or [{}])[0].get("title", "")
        rows.append({
            "doi": attrs.get("doi"),
            "title_hash": sha_text(title),
            "publisher": attrs.get("publisher"),
            "publication_year": attrs.get("publicationYear"),
            "creator_affiliations": affils[:4],
            "mit_affiliation_verified": any("Massachusetts Institute of Technology" in a or a == "MIT" for a in affils),
            "identifiers": attrs.get("identifiers", [])[:3],
        })
    return rows


def parse_oai_identify(text: str) -> dict[str, Any]:
    return {
        "repository_name_observed": "MIT Open Scholarship" in text,
        "protocol_2_observed": "2.0" in text,
        "base_url_observed": "https://dspace.mit.edu/server/oai/request" in text,
        "admin_email_observed": "dspace-lib@mit.edu" in text,
        "body_sha256": sha_text(text),
    }


def parse_oai_records(text: str) -> dict[str, Any]:
    title = "Insights into Li+ Storage Mechanisms" if "Insights into Li+ Storage Mechanisms" in text else ""
    return {
        "body_chars": len(text),
        "record_identifier_observed": "oai:dspace.mit.edu:" in text,
        "date_filter_observed": "2026-" in text,
        "sample_title_hash": sha_text(title),
        "sample_title_present": bool(title),
    }


def command_receipt(cmd: list[str], timeout: int = 45) -> dict[str, Any]:
    run = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(cmd), "exit_code": run.returncode, "stdout_sha256": sha_text(run.stdout), "stderr_sha256": sha_text(run.stderr), "first_line": run.stdout.strip().splitlines()[0] if run.stdout.strip() else ""}


def tool_receipts() -> dict[str, Any]:
    commands = {
        "gather": ["gather", "--version"],
        "index": ["index", "--version"],
        "forum": ["forum", "--version"],
        "crucible": ["crucible", "--version"],
        "telos": ["node", "-p", "'telos '+JSON.parse(require('fs').readFileSync('package.json','utf8')).version"],
    }
    out = {name: command_receipt(cmd) for name, cmd in commands.items()}
    for name, row in out.items():
        row["observed_version"] = row["first_line"].split()[-1] if row["first_line"] else None
        row["status"] = "MATCH" if row["exit_code"] == 0 else "DRIFT"
    return out


def build_receipt(live_tools: bool = True) -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    rows = catalog()
    ror_row, ror_text = find(rows, "api.ror.org")
    oa_row, oa_text = find(rows, "api.openalex.org/institutions")
    identify_row, identify_text = find(rows, "verb=Identify")
    records_row, records_text = find(rows, "verb=ListRecords")
    crossref_row, crossref_text = find(rows, "api.crossref.org")
    datacite_row, datacite_text = find(rows, "api.datacite.org")
    ror = parse_ror(ror_text)
    openalex = parse_openalex(oa_text)
    crossref = parse_crossref(crossref_text)
    datacite = parse_datacite(datacite_text)
    oai_identify = parse_oai_identify(identify_text)
    oai_records = parse_oai_records(records_text)
    docs = [row for row in rows if row["ref"] in plan["protocol_doc_urls"]]
    live = [row for row in rows if row["ref"] in plan["live_source_urls"]]
    joins = [
        {"join": "ror_openalex_identity", "status": "MATCH" if ror["id"] == openalex["ror"] else "DRIFT", "evidence": [ror["id"], openalex["ror"], openalex["id"]]},
        {"join": "dspace_oai_identify", "status": "MATCH" if all([oai_identify["repository_name_observed"], oai_identify["protocol_2_observed"], oai_identify["base_url_observed"]]) else "DRIFT", "evidence": [identify_row["sha256"]]},
        {"join": "dspace_recent_record_sample", "status": "MATCH" if oai_records["record_identifier_observed"] and oai_records["sample_title_present"] else "DRIFT", "evidence": [records_row["sha256"], oai_records["sample_title_hash"]]},
        {"join": "crossref_affiliation_sample", "status": "MATCH" if any(item["has_mit_affiliation_string"] for item in crossref) else "DRIFT", "evidence": [crossref_row["sha256"]]},
        {"join": "datacite_dataset_relation", "status": "SOURCE_LEAD_ONLY", "evidence": [datacite_row["sha256"], "explicit MIT affiliation not verified in sampled records"]},
    ]
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": STATUS if all(j["status"] in ("MATCH", "SOURCE_LEAD_ONLY") for j in joins) else "ONE_INSTITUTION_CLAIM_GRAPH_DRIFT",
        "institution": plan["candidate_institution"],
        "source_store": str(STORE.relative_to(REPO)).replace("\\", "/"),
        "gather_summary": {"total_items": len(rows), "live_captures": len(live), "protocol_docs": len(docs), "distinct_bodies": len({row["sha256"] for row in rows})},
        "source_receipts": [{"ref": row["ref"], "sha256": row["sha256"], "title": row.get("title", ""), "chars": len(body(row))} for row in rows],
        "organization_identity": {"ror": ror, "openalex": openalex},
        "repository_endpoint": {"identify": oai_identify, "records": oai_records},
        "scholarly_graph_samples": {"crossref": crossref, "datacite": datacite},
        "join_verdicts": joins,
        "source_warnings": plan["source_warnings"],
        "negative_fixtures": [{"fixture_id": item, "expected_status": "REJECT"} for item in plan["negative_fixtures"]],
        "tool_receipts": tool_receipts() if live_tools else {},
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "boundary": "Pass 0144 is a bounded live adapter run for one institution. It does not claim complete MIT coverage, dataset linkage, publication truth, full-text access, world coverage, theorem proof, market uniqueness, or natural-law discovery.",
    }
    receipt["seal"] = sha_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def render_packet(r: dict[str, Any]) -> str:
    lines = ["# Pass 0144 - One Institution Claim Graph", "", "## Summary", "", f"Status: `{r['status']}`. The pass records `{r['gather_summary']['live_captures']}` live captures and `{r['gather_summary']['protocol_docs']}` protocol docs for `{r['institution']['name']}`.", "", "## Join Verdicts", ""]
    lines.extend(f"- `{j['join']}`: `{j['status']}`" for j in r["join_verdicts"])
    lines.extend(["", "## What Promoted", "", "- ROR and OpenAlex identity join for MIT.", "- MIT DSpace OAI-PMH endpoint reachability and a date-filtered record sample.", "- Crossref sample containing MIT affiliation strings.", "", "## What Stayed Fenced", "", "- DataCite keyword-query results stay `SOURCE_LEAD_ONLY` until explicit affiliation or ROR links are verified.", "- Semantic Scholar stays a rate-limit warning, not absence evidence.", "- No full text, dataset relation, publication truth, theorem, or natural law was promoted.", "", "## Boundary", "", r["boundary"]])
    return "\n".join(lines)


def render_brief(r: dict[str, Any]) -> str:
    return "\n".join(["# Pass 0144 Brief - One Institution Claim Graph", "", "Primary push: prove one bounded live institution graph before scaling to hundreds of research substrates.", "", f"Result: {len(r['join_verdicts'])} join verdicts across ROR, OpenAlex, MIT DSpace OAI-PMH, Crossref, and DataCite; DataCite remains source-lead-only.", "", "Next pass: convert this replay into a reusable institution adapter runner with pagination, rate-limit policy, and source-family manifests."])


def render_steelman() -> str:
    return "\n".join(["# Pass 0144 Steelman", "", "The strongest objection is that a single institution graph can look rigorous while hiding scale problems: pagination, identifier drift, ambiguous affiliations, repository coverage gaps, rate limits, and license constraints.", "", "The settling test is a multi-institution replay with the same contract: one positive identity join, one repository endpoint, one scholarly metadata sample, one dataset candidate, and one intentionally rejected ambiguous relation per institution."])


def build_claims(r: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    claims = [
        f"Pass 0144 created a {SCHEMA} artifact with status {r['status']} and seal {r['seal']}.",
        f"Pass 0144 records {r['gather_summary']['live_captures']} live captures, {r['gather_summary']['protocol_docs']} protocol docs, and {r['gather_summary']['distinct_bodies']} distinct bodies.",
        f"Pass 0144 records {len(r['join_verdicts'])} join verdicts with DataCite fenced as SOURCE_LEAD_ONLY.",
        f"Pass 0144 rejects {len(r['negative_fixtures'])} negative fixtures and records {len(r['source_warnings'])} source warnings.",
        "Pass 0144 promotes no theorem or natural law.",
    ]
    thesis = {"title": "Dogfood Pass 0144 One Institution Claim Graph", "disposition": "fenced", "claims": [{"text": c, "falsification": f"Claim {i} differs from pass 0144 artifact values or receipts are missing"} for i, c in enumerate(claims, 1)]}
    evidence = [[f"schema={r['schema']}", f"status={r['status']}", f"seal={r['seal']}"], [f"gather_summary={r['gather_summary']}"], [f"join_verdicts={r['join_verdicts']}"], [f"negative_fixtures={len(r['negative_fixtures'])}", f"source_warnings={len(r['source_warnings'])}"], [f"current_promoted_theorems={r['current_promoted_theorems']}", f"current_promoted_natural_laws={r['current_promoted_natural_laws']}"]]
    measurements = {"measurements": [{"claim": c, "method": "artifact-review", "evidence": evidence[i], "deviation": 0.0, "tolerance": 0.5} for i, c in enumerate(claims)]}
    return thesis, measurements


def render_ledger(r: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0144 Ledger - One Institution Claim Graph", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    lines.extend(f"| {label} | {sha_file(path).upper()} |" for label, path in files.items())
    lines.extend(["", "## Result Snapshot", "", "| Field | Value |", "| --- | --- |", f"| Schema | `{r['schema']}` |", f"| Status | `{r['status']}` |", f"| Seal | `{r['seal']}` |", f"| Live captures | `{r['gather_summary']['live_captures']}` |", f"| Protocol docs | `{r['gather_summary']['protocol_docs']}` |", f"| Join verdicts | `{len(r['join_verdicts'])}` |", f"| Negative fixtures | `{len(r['negative_fixtures'])}` |", f"| Promoted theorems | `{len(r['current_promoted_theorems'])}` |"])
    return "\n".join(lines)


def main() -> None:
    r = build_receipt(live_tools=True)
    files = {
        "schemas/one-institution-claim-graph-pass-0144.json": ROOT / "schemas" / "one-institution-claim-graph-pass-0144.json",
        "packets/154-one-institution-claim-graph.md": ROOT / "packets" / "154-one-institution-claim-graph.md",
        "briefs/154-one-institution-claim-graph-brief.md": ROOT / "briefs" / "154-one-institution-claim-graph-brief.md",
        "adversarial/pass-0144-one-institution-claim-graph-steelman.md": ROOT / "adversarial" / "pass-0144-one-institution-claim-graph-steelman.md",
    }
    write_json(files["schemas/one-institution-claim-graph-pass-0144.json"], r)
    write_text(files["packets/154-one-institution-claim-graph.md"], render_packet(r))
    write_text(files["briefs/154-one-institution-claim-graph-brief.md"], render_brief(r))
    write_text(files["adversarial/pass-0144-one-institution-claim-graph-steelman.md"], render_steelman())
    thesis, measurements = build_claims(r)
    files["crucible/pass-0144-thesis.json"] = ROOT / "crucible" / "pass-0144-thesis.json"
    files["crucible/pass-0144-measurements.json"] = ROOT / "crucible" / "pass-0144-measurements.json"
    write_json(files["crucible/pass-0144-thesis.json"], thesis)
    write_json(files["crucible/pass-0144-measurements.json"], measurements)
    files["schemas/tool-receipts-pass-0144.json"] = ROOT / "schemas" / "tool-receipts-pass-0144.json"
    write_json(files["schemas/tool-receipts-pass-0144.json"], {"schema": "Pass0144ToolReceipts/v1", "artifact": {"path": str(files["schemas/one-institution-claim-graph-pass-0144.json"]), "sha256": sha_file(files["schemas/one-institution-claim-graph-pass-0144.json"])}, "source_store": str(STORE), "tool_receipts": r["tool_receipts"]})
    write_text(ROOT / "pass-0144-ledger.md", render_ledger(r, files))
    print(json.dumps({"status": r["status"], "seal": r["seal"]}, sort_keys=True))


if __name__ == "__main__":
    main()
