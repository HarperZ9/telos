"""Compose pass 0151 frontier problem source federation artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "FrontierProblemSourceFederationReceipt/v1"
PASS_ID = "0151"
STATUS = "FRONTIER_PROBLEM_SOURCE_FEDERATION_MATCH_WITH_WARNINGS"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PLAN = ROOT / "fixtures" / "pass-0151-frontier-problem-source-federation-plan.json"
PRIOR_0149 = ROOT / "schemas" / "cross-domain-substrate-expansion-pass-0149.json"


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object, compact: bool = False) -> None:
    body = canonical(value) if compact else json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True)
    write_text(path, body)


def read_plan() -> dict[str, Any]:
    return json.loads(PLAN.read_text(encoding="utf-8"))


def catalog(store: Path) -> list[dict[str, Any]]:
    path = store / "catalog.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def body_info(store: Path, sha: str) -> tuple[int, str]:
    body = (store / "objects" / sha[:2] / sha[2:]).read_text(encoding="utf-8", errors="replace")
    stripped = body.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        kind = "json"
    elif stripped.startswith("<"):
        kind = "xml_or_html"
    else:
        kind = "text"
    return len(body), kind


def command_receipt(cmd: list[str], timeout: int = 45) -> dict[str, Any]:
    run = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    first = run.stdout.strip().splitlines()[0] if run.stdout.strip() else ""
    return {"command": " ".join(cmd), "exit_code": run.returncode, "stdout_sha256": sha_text(run.stdout), "stderr_sha256": sha_text(run.stderr), "first_line": first, "observed_version": first.split()[-1] if first else None, "status": "MATCH" if run.returncode == 0 else "DRIFT"}


def tool_receipts() -> dict[str, Any]:
    return {
        "gather": command_receipt(["gather", "--version"]),
        "index": command_receipt(["index", "--version"]),
        "forum": command_receipt(["forum", "--version"]),
        "crucible": command_receipt(["crucible", "--version"]),
        "telos": command_receipt(["node", "-e", "console.log('telos '+require('./package.json').version)"]),
    }


def candidate_rows(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(zip(plan["candidate_columns"], row)) for row in plan["candidate_rows"]]


def capture_attempts(plan: dict[str, Any], store: Path) -> list[dict[str, Any]]:
    by_ref = {row["ref"]: row for row in catalog(store)}
    failures = {row[0]: row[1] for row in plan["capture_failures"]}
    out = []
    for ident, source_id, url in plan["capture_jobs"]:
        row = by_ref.get(url)
        if row:
            chars, kind = body_info(store, row["sha256"])
            status = "GATHER_VERIFIED" if chars > 0 else "GATHER_EMPTY_WARNING"
            out.append({"id": ident, "source_id": source_id, "url": url, "status": status, "sha256": row["sha256"], "chars": chars, "body_kind": kind})
        else:
            out.append({"id": ident, "source_id": source_id, "url": url, "status": failures.get(ident, "GATHER_DROPPED_WARNING"), "sha256": None, "chars": 0, "body_kind": None})
    return out


def join_candidates(candidates: list[dict[str, Any]], captures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_source: dict[str, list[dict[str, Any]]] = {}
    for row in captures:
        by_source.setdefault(row["source_id"], []).append(row)
    out = []
    for row in candidates:
        caps = by_source.get(row["id"], [])
        statuses = {cap["status"] for cap in caps}
        merged = dict(row)
        if "GATHER_VERIFIED" in statuses and len(statuses) > 1:
            merged["evidence_status"] = "GATHER_VERIFIED_WITH_WARNINGS"
        elif "GATHER_VERIFIED" in statuses:
            merged["evidence_status"] = "GATHER_VERIFIED"
        elif statuses:
            merged["evidence_status"] = sorted(statuses)[0]
        else:
            merged["evidence_status"] = "SOURCE_LEAD_ONLY"
        merged["capture_ids"] = [cap["id"] for cap in caps]
        out.append(merged)
    return out


def prior_count() -> int:
    if not PRIOR_0149.exists():
        return 0
    return json.loads(PRIOR_0149.read_text(encoding="utf-8"))["summary"]["candidate_substrates"]


def build_receipt(live_tools: bool = True) -> dict[str, Any]:
    plan = read_plan()
    store = REPO / plan["source_store"]
    captures = capture_attempts(plan, store)
    candidates = join_candidates(candidate_rows(plan), captures)
    families = sorted({row["family"] for row in candidates})
    domains = sorted({row["domain"] for row in candidates})
    warnings = [row for row in captures if row["status"] != "GATHER_VERIFIED"]
    p0149_count = prior_count()
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": STATUS,
        "source_store": plan["source_store"],
        "prior_receipts": plan["prior_receipts"],
        "candidate_sources": candidates,
        "capture_attempts": captures,
        "problem_lanes": [{"id": row[0], "substrates": row[1], "first_experiment": row[2], "packet_type": row[3]} for row in plan["problem_lanes"]],
        "admission_gates": [{"gate": row[0], "rule": row[1]} for row in plan["admission_gates"]],
        "negative_fixtures": [{"fixture_id": row, "expected_status": "REJECT"} for row in plan["negative_fixtures"]],
        "updated_tool_floor": plan["updated_tool_floor"],
        "tool_receipts": tool_receipts() if live_tools else {},
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "current_promoted_world_solutions": [],
        "boundary": "Pass 0151 federates source and problem-substrate routes. It does not prove complete global coverage, source truth, theorem resolution, experimental validity, clinical efficacy, market adoption, or a natural law.",
    }
    receipt["summary"] = {
        "candidate_sources": len(candidates),
        "families": len(families),
        "domains": len(domains),
        "capture_jobs": len(captures),
        "gather_verified": sum(1 for row in captures if row["status"] == "GATHER_VERIFIED"),
        "capture_warnings": len(warnings),
        "source_lead_only": sum(1 for row in candidates if row["evidence_status"] == "SOURCE_LEAD_ONLY"),
        "college_database_sources": sum(1 for row in candidates if row["family"] in {"college_repository", "general_data_repository"} and row["domain"] == "university"),
        "preprint_sources": sum(1 for row in candidates if row["family"] == "preprint_press"),
        "scholarly_graph_sources": sum(1 for row in candidates if row["family"] == "scholarly_graph"),
        "problem_lanes": len(receipt["problem_lanes"]),
        "admission_gates": len(receipt["admission_gates"]),
        "negative_fixtures": len(receipt["negative_fixtures"]),
        "prior_pass_0149_candidate_substrates": p0149_count,
        "combined_nondeduplicated_substrate_context": p0149_count + len(candidates),
        "families_list": families,
        "domains_list": domains,
    }
    receipt["seal"] = sha_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def render_packet(r: dict[str, Any]) -> str:
    s = r["summary"]
    lines = ["# Pass 0151 - Frontier Problem Source Federation", "", f"Status: `{r['status']}` with seal `{r['seal']}`.", "", "## Federation Snapshot", "", "| Metric | Value |", "| --- | --- |"]
    for key in ["candidate_sources", "families", "domains", "capture_jobs", "gather_verified", "capture_warnings", "college_database_sources", "preprint_sources", "scholarly_graph_sources", "combined_nondeduplicated_substrate_context"]:
        lines.append(f"| {key} | `{s[key]}` |")
    lines.extend(["", "## Problem Lanes", ""])
    lines.extend(f"- `{row['id']}` -> `{row['packet_type']}`: {row['first_experiment']}" for row in r["problem_lanes"])
    lines.extend(["", "## Warning Policy", "", "A failed probe is not source absence. Rate limits, query-shape failures, and service outages remain adapter work items until a later pass rejects them with evidence.", "", "## Boundary", "", r["boundary"]])
    return "\n".join(lines)


def render_brief(r: dict[str, Any]) -> str:
    s = r["summary"]
    return "\n".join(["# Pass 0151 Brief - Frontier Problem Source Federation", "", "Primary push: turn the massive archive/preprint/college/source ambition into a reusable source federation that routes hard problems into field-specific proof-packet factories.", "", f"Result: {s['candidate_sources']} candidate sources across {s['families']} families and {s['domains']} domains; {s['gather_verified']} verified live captures from {s['capture_jobs']} probes; {s['problem_lanes']} problem lanes; combined non-deduplicated substrate context with pass 0149 is {s['combined_nondeduplicated_substrate_context']}.", "", "Next experiment: pick one frontier lane where source joins can be verified without domain overclaim, then build a packet with source body, extraction, verifier, negative fixture, and replay receipt."])


def render_steelman() -> str:
    return "\n".join(["# Pass 0151 Steelman", "", "The strongest objection is that broad federation can decay into list-making. A source atlas is only valuable if it forces the next experiment into a smaller proof packet with falsifiers and field-specific promotion gates.", "", "The settling test is whether the next pass chooses one lane, extracts one bounded claim from verified source bodies, rejects at least one false promotion, and produces a replayable verifier receipt."])


def build_claims(r: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    s = r["summary"]
    claims = [
        f"Pass 0151 created a {SCHEMA} artifact with status {r['status']} and seal {r['seal']}.",
        f"Pass 0151 records {s['candidate_sources']} candidate sources across {s['families']} families and {s['domains']} domains.",
        f"Pass 0151 records {s['capture_jobs']} capture probes, {s['gather_verified']} Gather-verified captures, and {s['capture_warnings']} warning probes.",
        f"Pass 0151 records {s['college_database_sources']} college/database sources, {s['preprint_sources']} preprint sources, and {s['scholarly_graph_sources']} scholarly graph sources.",
        f"Pass 0151 combines pass 0149 context and current candidates into {s['combined_nondeduplicated_substrate_context']} non-deduplicated substrate references.",
        "Pass 0151 promotes no theorem, natural law, or world solution.",
    ]
    thesis = {"title": "Dogfood Pass 0151 Frontier Problem Source Federation", "disposition": "fenced", "claims": [{"text": c, "falsification": f"Claim {i} differs from pass 0151 artifact values or source receipts are missing"} for i, c in enumerate(claims, 1)]}
    evidence = [[f"schema={r['schema']}", f"status={r['status']}", f"seal={r['seal']}"], [f"candidate_sources={s['candidate_sources']}", f"families={s['families']}", f"domains={s['domains']}"], [f"capture_jobs={s['capture_jobs']}", f"gather_verified={s['gather_verified']}", f"capture_warnings={s['capture_warnings']}"], [f"college_database_sources={s['college_database_sources']}", f"preprint_sources={s['preprint_sources']}", f"scholarly_graph_sources={s['scholarly_graph_sources']}"], [f"prior_pass_0149_candidate_substrates={s['prior_pass_0149_candidate_substrates']}", f"combined_nondeduplicated_substrate_context={s['combined_nondeduplicated_substrate_context']}"], [f"current_promoted_theorems={r['current_promoted_theorems']}", f"current_promoted_world_solutions={r['current_promoted_world_solutions']}"]]
    measurements = {"measurements": [{"claim": c, "method": "artifact-review", "evidence": evidence[i], "deviation": 0.0, "tolerance": 0.5} for i, c in enumerate(claims)]}
    return thesis, measurements


def render_ledger(r: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0151 Ledger - Frontier Problem Source Federation", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    lines.extend(f"| {label} | {sha_file(path).upper()} |" for label, path in files.items())
    s = r["summary"]
    lines.extend(["", "## Result Snapshot", "", "| Field | Value |", "| --- | --- |", f"| Schema | `{r['schema']}` |", f"| Status | `{r['status']}` |", f"| Seal | `{r['seal']}` |", f"| Candidate sources | `{s['candidate_sources']}` |", f"| Families | `{s['families']}` |", f"| Domains | `{s['domains']}` |", f"| Capture probes | `{s['capture_jobs']}` |", f"| Gather verified | `{s['gather_verified']}` |", f"| Warning probes | `{s['capture_warnings']}` |", f"| Combined substrate context | `{s['combined_nondeduplicated_substrate_context']}` |", "", "## Boundary", "", r["boundary"]])
    return "\n".join(lines)


def main() -> None:
    r = build_receipt(live_tools=True)
    files = {
        "schemas/frontier-problem-source-federation-pass-0151.json": ROOT / "schemas" / "frontier-problem-source-federation-pass-0151.json",
        "packets/161-frontier-problem-source-federation.md": ROOT / "packets" / "161-frontier-problem-source-federation.md",
        "briefs/161-frontier-problem-source-federation-brief.md": ROOT / "briefs" / "161-frontier-problem-source-federation-brief.md",
        "adversarial/pass-0151-frontier-problem-source-federation-steelman.md": ROOT / "adversarial" / "pass-0151-frontier-problem-source-federation-steelman.md",
    }
    write_json(files["schemas/frontier-problem-source-federation-pass-0151.json"], r, compact=True)
    write_text(files["packets/161-frontier-problem-source-federation.md"], render_packet(r))
    write_text(files["briefs/161-frontier-problem-source-federation-brief.md"], render_brief(r))
    write_text(files["adversarial/pass-0151-frontier-problem-source-federation-steelman.md"], render_steelman())
    thesis, measurements = build_claims(r)
    files["crucible/pass-0151-thesis.json"] = ROOT / "crucible" / "pass-0151-thesis.json"
    files["crucible/pass-0151-measurements.json"] = ROOT / "crucible" / "pass-0151-measurements.json"
    write_json(files["crucible/pass-0151-thesis.json"], thesis)
    write_json(files["crucible/pass-0151-measurements.json"], measurements)
    files["schemas/tool-receipts-pass-0151.json"] = ROOT / "schemas" / "tool-receipts-pass-0151.json"
    write_json(files["schemas/tool-receipts-pass-0151.json"], {"schema": "Pass0151ToolReceipts/v1", "artifact": {"path": str(files["schemas/frontier-problem-source-federation-pass-0151.json"]), "sha256": sha_file(files["schemas/frontier-problem-source-federation-pass-0151.json"])}, "source_store": r["source_store"], "tool_receipts": r["tool_receipts"]}, compact=True)
    write_text(ROOT / "pass-0151-ledger.md", render_ledger(r, files))
    print(json.dumps({"status": r["status"], "seal": r["seal"], "candidate_sources": r["summary"]["candidate_sources"], "gather_verified": r["summary"]["gather_verified"]}, sort_keys=True))


if __name__ == "__main__":
    main()
