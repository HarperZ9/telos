"""Compose pass 0145 multi-institution claim graph artifact."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from multi_institution_claim_graph_render import build_claims, render_brief, render_ledger, render_packet, render_steelman

SCHEMA = "MultiInstitutionClaimGraphReceipt/v1"
PASS_ID = "0145"
STATUS = "MULTI_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0145-multi-institution-claim-graph"
PLAN = ROOT / "fixtures" / "pass-0145-multi-institution-claim-graph-plan.json"


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, body_text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body_text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True))


def catalog() -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def stored_body(row: dict[str, Any]) -> str:
    path = STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
    return path.read_text(encoding="utf-8", errors="replace")


def find_body(rows: list[dict[str, Any]], ref: str) -> tuple[dict[str, Any] | None, str]:
    for row in rows:
        if row["ref"] == ref:
            return row, stored_body(row)
    return None, ""


def first_result(text: str, key: str) -> dict[str, Any]:
    data = json.loads(text)
    return data[key][0]


def parse_ror(text: str, expected_ror: str) -> dict[str, Any]:
    if not text:
        return {"id": None, "status": "MISSING_CAPTURE", "expected_match": False}
    first = first_result(text, "items")
    return {
        "id": first.get("id"),
        "status": first.get("status"),
        "domains": first.get("domains", []),
        "country": first.get("locations", [{}])[0].get("geonames_details", {}).get("country_name"),
        "established": first.get("established"),
        "last_modified": first.get("admin", {}).get("last_modified", {}).get("date"),
        "expected_match": first.get("id") == expected_ror,
    }


def parse_openalex(text: str, expected_openalex: str, expected_ror: str) -> dict[str, Any]:
    if not text:
        return {"id": None, "ror": None, "status": "MISSING_CAPTURE", "expected_match": False}
    first = first_result(text, "results")
    return {
        "id": first.get("id"),
        "ror": first.get("ror"),
        "display_name": first.get("display_name"),
        "country_code": first.get("country_code"),
        "type": first.get("type"),
        "works_count": first.get("works_count"),
        "updated_date": first.get("updated_date"),
        "expected_match": first.get("id") == expected_openalex and first.get("ror") == expected_ror,
    }


def parse_repository(text: str, expected_phrase: str) -> dict[str, Any]:
    if not text:
        return {"status": "MISSING_CAPTURE", "phrase_match": False, "protocol_2_observed": False}
    return {
        "status": "MATCH" if expected_phrase in text and "2.0" in text else "DRIFT",
        "phrase_match": expected_phrase in text,
        "protocol_2_observed": "2.0" in text,
        "body_sha256": sha_text(text),
        "body_chars": len(text),
    }


def parse_crossref(text: str, expected_affiliation: str) -> dict[str, Any]:
    if not text:
        return {
            "status": "SOURCE_LEAD_ONLY",
            "item_count": 0,
            "doi_count": 0,
            "has_expected_affiliation": False,
            "samples": [],
        }
    items = json.loads(text)["message"]["items"]
    samples = []
    has_expected = False
    for item in items:
        affils = [
            affiliation.get("name", "")
            for author in item.get("author", [])
            for affiliation in author.get("affiliation", [])
        ]
        match = any(expected_affiliation in value for value in affils)
        has_expected = has_expected or match
        title = (item.get("title") or [""])[0]
        samples.append(
            {
                "doi": item.get("DOI"),
                "title_hash": sha_text(title),
                "affiliation_match": match,
                "license_count": len(item.get("license", [])),
            }
        )
    return {
        "status": "MATCH" if has_expected else "DRIFT",
        "item_count": len(items),
        "doi_count": sum(1 for item in items if item.get("DOI")),
        "has_expected_affiliation": has_expected,
        "samples": samples,
    }


def command_receipt(cmd: list[str], timeout: int = 45) -> dict[str, Any]:
    run = subprocess.run(
        cmd,
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
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
        "telos": command_receipt(
            ["node", "-p", "'telos '+JSON.parse(require('fs').readFileSync('package.json','utf8')).version"]
        ),
    }


def build_institution(rows: list[dict[str, Any]], item: dict[str, Any]) -> dict[str, Any]:
    ror_row, ror_text = find_body(rows, item["ror_url"])
    oa_row, oa_text = find_body(rows, item["openalex_url"])
    repo_row, repo_text = find_body(rows, item["repository_url"])
    crossref_row, crossref_text = find_body(rows, item["crossref_url"])
    ror = parse_ror(ror_text, item["expected_ror"])
    openalex = parse_openalex(oa_text, item["expected_openalex"], item["expected_ror"])
    repository = parse_repository(repo_text, item["expected_repository_phrase"])
    crossref = parse_crossref(crossref_text, item["expected_crossref_affiliation"])
    identity_status = "MATCH" if ror["expected_match"] and openalex["expected_match"] else "DRIFT"
    return {
        "id": item["id"],
        "name": item["name"],
        "domain_lane": item["domain_lane"],
        "identity_status": identity_status,
        "repository_status": repository["status"],
        "crossref_status": crossref["status"],
        "identity": {"ror": ror, "openalex": openalex},
        "repository": repository,
        "crossref": crossref,
        "source_receipts": {
            "ror": ror_row["sha256"] if ror_row else None,
            "openalex": oa_row["sha256"] if oa_row else None,
            "repository": repo_row["sha256"] if repo_row else None,
            "crossref": crossref_row["sha256"] if crossref_row else None,
        },
    }


def join_verdicts(institutions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for item in institutions:
        for field in ("identity", "repository", "crossref"):
            out.append({"institution": item["id"], "join": field, "status": item[f"{field}_status"]})
    return out


def build_receipt(live_tools: bool = True) -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    rows = catalog()
    institutions = [build_institution(rows, item) for item in plan["institutions"]]
    docs = [row for row in rows if row["ref"] in plan["repository_support_docs"]]
    summary = {
        "institutions": len(institutions),
        "stored_captures": len(rows),
        "distinct_bodies": len({row["sha256"] for row in rows}),
        "support_docs": len(docs),
        "identity_matches": sum(1 for item in institutions if item["identity_status"] == "MATCH"),
        "repository_matches": sum(1 for item in institutions if item["repository_status"] == "MATCH"),
        "crossref_matches": sum(1 for item in institutions if item["crossref_status"] == "MATCH"),
        "warnings": len(plan["source_warnings"]),
    }
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": STATUS
        if summary["identity_matches"] == 4 and summary["repository_matches"] == 4 and summary["crossref_matches"] >= 3
        else "MULTI_INSTITUTION_CLAIM_GRAPH_DRIFT",
        "source_store": str(STORE.relative_to(REPO)).replace("\\", "/"),
        "summary": summary,
        "institutions": institutions,
        "join_verdicts": join_verdicts(institutions),
        "source_receipts": [
            {"ref": row["ref"], "sha256": row["sha256"], "title": row.get("title", ""), "chars": len(stored_body(row))}
            for row in rows
        ],
        "source_warnings": plan["source_warnings"],
        "negative_fixtures": [{"fixture_id": name, "expected_status": "REJECT"} for name in plan["negative_fixtures"]],
        "updated_tool_floor": plan["updated_tool_floor"],
        "tool_receipts": tool_receipts() if live_tools else {},
        "market_implication": "A registry-scale research proof product needs reusable institution adapters with source-family receipts, rate-limit policy, endpoint-drift handling, and per-claim promotion gates.",
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "boundary": "Pass 0145 is a bounded four-institution replay over identity, repository Identify, and sampled scholarly graph surfaces. It does not claim complete institutional coverage, publication truth, repository harvest completeness, solved theorem status, market uniqueness, or natural-law discovery.",
    }
    receipt["seal"] = sha_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def main() -> None:
    receipt = build_receipt(live_tools=True)
    files = {
        "schemas/multi-institution-claim-graph-pass-0145.json": ROOT / "schemas" / "multi-institution-claim-graph-pass-0145.json",
        "packets/155-multi-institution-claim-graph.md": ROOT / "packets" / "155-multi-institution-claim-graph.md",
        "briefs/155-multi-institution-claim-graph-brief.md": ROOT / "briefs" / "155-multi-institution-claim-graph-brief.md",
        "adversarial/pass-0145-multi-institution-claim-graph-steelman.md": ROOT / "adversarial" / "pass-0145-multi-institution-claim-graph-steelman.md",
    }
    write_json(files["schemas/multi-institution-claim-graph-pass-0145.json"], receipt)
    write_text(files["packets/155-multi-institution-claim-graph.md"], render_packet(receipt))
    write_text(files["briefs/155-multi-institution-claim-graph-brief.md"], render_brief(receipt))
    write_text(files["adversarial/pass-0145-multi-institution-claim-graph-steelman.md"], render_steelman())
    thesis, measurements = build_claims(receipt)
    files["crucible/pass-0145-thesis.json"] = ROOT / "crucible" / "pass-0145-thesis.json"
    files["crucible/pass-0145-measurements.json"] = ROOT / "crucible" / "pass-0145-measurements.json"
    write_json(files["crucible/pass-0145-thesis.json"], thesis)
    write_json(files["crucible/pass-0145-measurements.json"], measurements)
    files["schemas/tool-receipts-pass-0145.json"] = ROOT / "schemas" / "tool-receipts-pass-0145.json"
    write_json(files["schemas/tool-receipts-pass-0145.json"], {"schema": "Pass0145ToolReceipts/v1", "artifact": {"path": str(files["schemas/multi-institution-claim-graph-pass-0145.json"]), "sha256": sha_file(files["schemas/multi-institution-claim-graph-pass-0145.json"])}, "source_store": str(STORE), "tool_receipts": receipt["tool_receipts"]})
    write_text(ROOT / "pass-0145-ledger.md", render_ledger(receipt, files))
    print(json.dumps({"status": receipt["status"], "seal": receipt["seal"]}, sort_keys=True))


if __name__ == "__main__":
    main()
