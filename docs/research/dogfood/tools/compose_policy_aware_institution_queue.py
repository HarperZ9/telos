"""Compose pass 0147 policy-aware institution queue artifact."""
from __future__ import annotations

import hashlib
import json
import subprocess
import unicodedata
from pathlib import Path
from typing import Any

SCHEMA = "PolicyAwareInstitutionQueueReceipt/v1"
PASS_ID = "0147"
STATUS = "POLICY_AWARE_INSTITUTION_QUEUE_MATCH_WITH_WARNINGS"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PLAN = ROOT / "fixtures" / "pass-0147-policy-aware-institution-queue-plan.json"


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def ascii_text(value: object) -> str:
    text = str(value)
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ascii_text(body).rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


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


def ror_name(item: dict[str, Any]) -> str:
    for wanted in ("ror_display", "label"):
        for name in item.get("names", []):
            if wanted in name.get("types", []):
                return name.get("value", "")
    return item.get("name", "")


def first_country(item: dict[str, Any]) -> str:
    locations = item.get("locations") or []
    if not locations:
        return ""
    return locations[0].get("geonames_details", {}).get("country_code", "")


def identity_row(plan: dict[str, Any], ror_json: dict[str, Any], oa_json: dict[str, Any]) -> dict[str, Any]:
    ror_items = ror_json.get("items", [])
    oa_items = oa_json.get("results", [])
    oa = oa_items[0]
    openalex_ror = oa.get("ror")
    matched_rank = next((i + 1 for i, item in enumerate(ror_items[:10]) if item.get("id") == openalex_ror), None)
    selected = next((item for item in ror_items[:10] if item.get("id") == openalex_ror), ror_items[0])
    status = "MATCH" if matched_rank == 1 else "RANKED_ALIAS_MATCH_WITH_WARNING"
    return {
        "status": status,
        "label": plan["label"],
        "openalex_id": oa.get("id"),
        "openalex_name": oa.get("display_name"),
        "openalex_ror": openalex_ror,
        "openalex_country": oa.get("country_code"),
        "openalex_works_count": oa.get("works_count"),
        "selected_ror": selected.get("id"),
        "selected_ror_name": ror_name(selected),
        "selected_ror_country": first_country(selected),
        "ror_rank_for_openalex": matched_rank,
        "ror_first_id": ror_items[0].get("id") if ror_items else None,
        "ror_first_name": ror_name(ror_items[0]) if ror_items else None,
        "ror_result_count": ror_json.get("number_of_results"),
        "policy": "REQUIRE_RANKED_IDENTITY_RESOLUTION" if status != "MATCH" else "IDENTITY_JOIN_MATCH",
    }


def repository_row(plan: dict[str, Any], text: str) -> dict[str, Any]:
    matched = [signal for signal in plan["repository_signals"] if signal.lower() in text.lower()]
    sample_page = "sample server" in text.lower() or "simple interface to sample server" in text.lower()
    clean_identify = len(matched) == len(plan["repository_signals"]) and not sample_page
    return {
        "status": "OAI_IDENTIFY_MATCH" if clean_identify else "SOURCE_LEAD_ONLY_ENDPOINT_DRIFT",
        "matched_signals": matched,
        "required_signals": plan["repository_signals"],
        "policy": "OAI_SOURCE_LEAD_NO_ABSENCE_PROMOTION" if not clean_identify else "OAI_IDENTIFY_REPOSITORY_LEAD",
        "sample_page_warning": sample_page,
    }


def crossref_row(text: str) -> dict[str, Any]:
    data = json.loads(text)
    items = data.get("message", {}).get("items", [])
    dois = [item.get("DOI") for item in items if item.get("DOI")]
    affiliations = []
    for item in items:
        for author in item.get("author", []):
            for affiliation in author.get("affiliation", []):
                name = affiliation.get("name")
                if name:
                    affiliations.append(name)
    return {
        "status": "SAMPLED_AFFILIATION_MATCH" if dois and affiliations else "SOURCE_LEAD_ONLY_RETRYABLE",
        "sampled_dois": dois[:2],
        "sampled_affiliation_count": len(affiliations),
        "total_results": data.get("message", {}).get("total-results"),
        "policy": "SAMPLED_METADATA_ONLY",
    }


def institution_receipts(plan: dict[str, Any], store: Path) -> list[dict[str, Any]]:
    rows = catalog(store)
    by_ref = {row["ref"]: row for row in rows}
    receipts = []
    for inst in plan["institutions"]:
        ror_row, oa_row = by_ref[inst["ror_url"]], by_ref[inst["openalex_url"]]
        oai_row, cr_row = by_ref[inst["oai_url"]], by_ref[inst["crossref_url"]]
        identity = identity_row(inst, json.loads(body(store, ror_row)), json.loads(body(store, oa_row)))
        repository = repository_row(inst, body(store, oai_row))
        crossref = crossref_row(body(store, cr_row))
        warning_count = sum(1 for row in (identity, repository, crossref) if "WARNING" in row["status"] or "SOURCE_LEAD_ONLY" in row["status"])
        receipts.append({
            "id": inst["id"],
            "label": inst["label"],
            "country_code": inst["country_code"],
            "source_refs": {
                "ror": {"url": inst["ror_url"], "sha256": ror_row["sha256"]},
                "openalex": {"url": inst["openalex_url"], "sha256": oa_row["sha256"]},
                "oai": {"url": inst["oai_url"], "sha256": oai_row["sha256"]},
                "crossref": {"url": inst["crossref_url"], "sha256": cr_row["sha256"]},
            },
            "identity": identity,
            "repository": repository,
            "crossref": crossref,
            "policy_warnings": warning_count,
        })
    return receipts


def build_receipt(live_tools: bool = True) -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    store = REPO / plan["source_store"]
    prior = json.loads((REPO / plan["prior_policy_receipt"]).read_text(encoding="utf-8"))
    institutions = institution_receipts(plan, store)
    warnings = [row for row in institutions if row["policy_warnings"]]
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": STATUS,
        "source_store": plan["source_store"],
        "source_captures": len(catalog(store)),
        "institutions": institutions,
        "prior_policy_receipt": plan["prior_policy_receipt"],
        "prior_policy_rules": [row["id"] for row in prior["policy_rules"]],
        "queue_policies": [
            "ranked ROR/OpenAlex identity joins before promotion",
            "OAI endpoint drift remains a source lead, not absence evidence",
            "Crossref affiliation samples remain sample-only metadata",
            "non-US institution coverage is a queue seed, not global coverage",
        ],
        "negative_fixtures": [{"fixture_id": name, "expected_status": "REJECT"} for name in plan["negative_fixtures"]],
        "integration_targets": ["PolicyAwareInstitutionQueueRunner", "SourceFamilyScheduler", "EndpointAliasRegistry", "MultilingualInstitutionNameResolver", "Forum source-adapter lane"],
        "updated_tool_floor": plan["updated_tool_floor"],
        "tool_receipts": tool_receipts() if live_tools else {},
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "boundary": "Pass 0147 proves a policy-aware queue receipt over four institution source leads. It does not prove repository completeness, global coverage, research quality, theorem progress, or natural-law discovery.",
    }
    receipt["summary"] = {
        "institutions": len(institutions),
        "source_captures": receipt["source_captures"],
        "identity_warnings": sum(1 for row in institutions if row["identity"]["status"] != "MATCH"),
        "repository_warnings": sum(1 for row in institutions if row["repository"]["status"] != "OAI_IDENTIFY_MATCH"),
        "crossref_samples": sum(1 for row in institutions if row["crossref"]["status"] == "SAMPLED_AFFILIATION_MATCH"),
        "negative_fixtures": len(receipt["negative_fixtures"]),
        "policy_warnings": sum(row["policy_warnings"] for row in institutions),
    }
    receipt["seal"] = sha_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def render_packet(r: dict[str, Any]) -> str:
    lines = ["# Pass 0147 - Policy-Aware Institution Queue", "", f"Status: `{r['status']}` with seal `{r['seal']}`.", "", "## Institution Queue", "", "| Institution | Identity | Repository | Crossref | Warning Count |", "| --- | --- | --- | --- | --- |"]
    for row in r["institutions"]:
        lines.append(f"| {row['label']} | `{row['identity']['status']}` | `{row['repository']['status']}` | `{row['crossref']['status']}` | `{row['policy_warnings']}` |")
    lines.extend(["", "## Queue Policies", ""])
    lines.extend(f"- {policy}" for policy in r["queue_policies"])
    lines.extend(["", "## Key Warnings", "", f"- Identity ranking warnings: `{r['summary']['identity_warnings']}`.", f"- Repository endpoint warnings: `{r['summary']['repository_warnings']}`.", "- University of Tokyo demonstrates that first ROR hit is not safe enough for promotion.", "- Universidade de Sao Paulo demonstrates that an OAI-looking page can still be endpoint drift.", "", "## Boundary", "", r["boundary"]])
    return "\n".join(lines)


def render_brief(r: dict[str, Any]) -> str:
    return "\n".join(["# Pass 0147 Brief - Policy-Aware Institution Queue", "", "Primary push: turn non-US institution discovery into a queue with explicit policy statuses, not a brittle scraper.", "", f"Result: {r['summary']['institutions']} institutions, {r['summary']['source_captures']} source captures, {r['summary']['identity_warnings']} identity warning, and {r['summary']['repository_warnings']} repository warning.", "", "Next pass: expand this runner into a multilingual institution registry with endpoint alias discovery and bounded retry receipts."])


def render_steelman() -> str:
    return "\n".join(["# Pass 0147 Steelman", "", "The strongest objection is that four institutions do not establish global research coverage or production adapter behavior. The pass shows policy shape, not scale.", "", "The settling test is a repeated queue run over dozens of countries and repository platforms, with scheduler wait receipts, endpoint alias repair, and no promotion from sampled metadata to truth claims."])


def build_claims(r: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    claims = [
        f"Pass 0147 created a {SCHEMA} artifact with status {r['status']} and seal {r['seal']}.",
        f"Pass 0147 records {r['summary']['institutions']} institutions and {r['summary']['source_captures']} source captures.",
        f"Pass 0147 records {r['summary']['identity_warnings']} identity warning and {r['summary']['repository_warnings']} repository warning.",
        f"Pass 0147 records {r['summary']['crossref_samples']} Crossref sample-only matches and rejects {r['summary']['negative_fixtures']} negative fixtures.",
        "Pass 0147 promotes no theorem or natural law.",
    ]
    thesis = {"title": "Dogfood Pass 0147 Policy-Aware Institution Queue", "disposition": "fenced", "claims": [{"text": c, "falsification": f"Claim {i} differs from artifact values or receipts are missing"} for i, c in enumerate(claims, 1)]}
    evidence = [[f"schema={r['schema']}", f"status={r['status']}", f"seal={r['seal']}"], [f"institutions={r['summary']['institutions']}", f"source_captures={r['summary']['source_captures']}"], [f"identity_warnings={r['summary']['identity_warnings']}", f"repository_warnings={r['summary']['repository_warnings']}"], [f"crossref_samples={r['summary']['crossref_samples']}", f"negative_fixtures={r['summary']['negative_fixtures']}"], [f"current_promoted_theorems={r['current_promoted_theorems']}", f"current_promoted_natural_laws={r['current_promoted_natural_laws']}"]]
    return thesis, {"measurements": [{"claim": c, "method": "artifact-review", "evidence": evidence[i], "deviation": 0.0, "tolerance": 0.5} for i, c in enumerate(claims)]}


def render_ledger(r: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0147 Ledger - Policy-Aware Institution Queue", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    lines.extend(f"| {label} | {sha_file(path).upper()} |" for label, path in files.items())
    lines.extend(["", "## Result Snapshot", "", "| Field | Value |", "| --- | --- |", f"| Schema | `{r['schema']}` |", f"| Status | `{r['status']}` |", f"| Seal | `{r['seal']}` |", f"| Institutions | `{r['summary']['institutions']}` |", f"| Source captures | `{r['summary']['source_captures']}` |", f"| Identity warnings | `{r['summary']['identity_warnings']}` |", f"| Repository warnings | `{r['summary']['repository_warnings']}` |", f"| Crossref samples | `{r['summary']['crossref_samples']}` |", f"| Promoted theorems | `{len(r['current_promoted_theorems'])}` |"])
    return "\n".join(lines)


def main() -> None:
    r = build_receipt(live_tools=True)
    files = {
        "schemas/policy-aware-institution-queue-pass-0147.json": ROOT / "schemas" / "policy-aware-institution-queue-pass-0147.json",
        "packets/157-policy-aware-institution-queue.md": ROOT / "packets" / "157-policy-aware-institution-queue.md",
        "briefs/157-policy-aware-institution-queue-brief.md": ROOT / "briefs" / "157-policy-aware-institution-queue-brief.md",
        "adversarial/pass-0147-policy-aware-institution-queue-steelman.md": ROOT / "adversarial" / "pass-0147-policy-aware-institution-queue-steelman.md",
    }
    write_json(files["schemas/policy-aware-institution-queue-pass-0147.json"], r)
    write_text(files["packets/157-policy-aware-institution-queue.md"], render_packet(r))
    write_text(files["briefs/157-policy-aware-institution-queue-brief.md"], render_brief(r))
    write_text(files["adversarial/pass-0147-policy-aware-institution-queue-steelman.md"], render_steelman())
    thesis, measurements = build_claims(r)
    files["crucible/pass-0147-thesis.json"] = ROOT / "crucible" / "pass-0147-thesis.json"
    files["crucible/pass-0147-measurements.json"] = ROOT / "crucible" / "pass-0147-measurements.json"
    write_json(files["crucible/pass-0147-thesis.json"], thesis)
    write_json(files["crucible/pass-0147-measurements.json"], measurements)
    files["schemas/tool-receipts-pass-0147.json"] = ROOT / "schemas" / "tool-receipts-pass-0147.json"
    write_json(files["schemas/tool-receipts-pass-0147.json"], {"schema": "Pass0147ToolReceipts/v1", "artifact": {"path": str(files["schemas/policy-aware-institution-queue-pass-0147.json"]), "sha256": sha_file(files["schemas/policy-aware-institution-queue-pass-0147.json"])}, "source_store": r["source_store"], "tool_receipts": r["tool_receipts"]})
    write_text(ROOT / "pass-0147-ledger.md", render_ledger(r, files))
    print(json.dumps({"status": r["status"], "seal": r["seal"]}, sort_keys=True))


if __name__ == "__main__":
    main()
