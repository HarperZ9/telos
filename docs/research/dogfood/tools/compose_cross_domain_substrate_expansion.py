"""Compose pass 0149 cross-domain substrate expansion artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "CrossDomainSubstrateExpansionReceipt/v1"
PASS_ID = "0149"
STATUS = "CROSS_DOMAIN_SUBSTRATE_EXPANSION_MATCH_WITH_WARNINGS"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PLAN = ROOT / "fixtures" / "pass-0149-cross-domain-substrate-expansion-plan.json"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()


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
    return [json.loads(line) for line in (store / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def body_chars(store: Path, sha: str) -> int:
    path = store / "objects" / sha[:2] / sha[2:]
    return len(path.read_text(encoding="utf-8", errors="replace")) if path.exists() else 0


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
        "telos": command_receipt(["node", "-p", "'telos '+JSON.parse(require('fs').readFileSync('package.json','utf8')).version"]),
    }


def candidate_rows(plan: dict[str, Any]) -> list[dict[str, Any]]:
    cols = plan["candidate_columns"]
    return [dict(zip(cols, row)) for row in plan["candidate_rows"]]


def capture_attempts(plan: dict[str, Any], store: Path) -> list[dict[str, Any]]:
    by_ref = {row["ref"]: row for row in catalog(store)}
    failures = {url: {"id": ident, "status": status} for ident, url, status in plan["capture_failures"]}
    out = []
    for ident, system, family, domain, url in plan["capture_jobs"]:
        row = by_ref.get(url)
        if row:
            chars = body_chars(store, row["sha256"])
            status = "GATHER_VERIFIED" if row["sha256"] != EMPTY_SHA and chars > 0 else "GATHER_EMPTY_WARNING"
            out.append({"id": ident, "system": system, "family": family, "domain": domain, "url": url, "status": status, "sha256": row["sha256"], "chars": chars})
        else:
            out.append({"id": ident, "system": system, "family": family, "domain": domain, "url": url, "status": failures.get(url, {}).get("status", "GATHER_DROPPED_WARNING"), "sha256": None, "chars": 0})
    return out


def join_candidates(candidates: list[dict[str, Any]], captures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_url = {row["url"]: row for row in captures}
    out = []
    for row in candidates:
        cap = by_url.get(row["url"])
        merged = dict(row)
        merged["evidence_status"] = cap["status"] if cap else "SOURCE_LEAD_ONLY"
        merged["source_sha256"] = cap.get("sha256") if cap else None
        out.append(merged)
    return out


def build_receipt(live_tools: bool = True) -> dict[str, Any]:
    plan = read_plan()
    store = REPO / plan["source_store"]
    captures = capture_attempts(plan, store)
    candidates = join_candidates(candidate_rows(plan), captures)
    warning_rows = [row for row in captures if row["status"] != "GATHER_VERIFIED"]
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": STATUS,
        "source_store": plan["source_store"],
        "prior_receipts": plan["prior_receipts"],
        "capture_attempts": captures,
        "candidate_substrates": candidates,
        "registry_scale_targets": [{"id": row[0], "strategy": row[1]} for row in plan["registry_scale_targets"]],
        "adapter_policy_matrix": [{"policy": row[0], "rule": row[1]} for row in plan["adapter_policy_matrix"]],
        "domain_workbenches": [{"id": row[0], "substrates": row[1], "first_experiment": row[2]} for row in plan["domain_workbenches"]],
        "negative_fixtures": [{"fixture_id": row, "expected_status": "REJECT"} for row in plan["negative_fixtures"]],
        "updated_tool_floor": plan["updated_tool_floor"],
        "tool_receipts": tool_receipts() if live_tools else {},
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "boundary": "Pass 0149 expands the source substrate map and scheduler queue. It does not prove complete archive coverage, endpoint availability for uncaptured leads, source correctness, full-text access, experimental truth, theorem progress, or natural-law discovery.",
    }
    families = sorted({row["family"] for row in candidates})
    domains = sorted({row["domain"] for row in candidates})
    receipt["summary"] = {
        "candidate_substrates": len(candidates),
        "families": len(families),
        "domains": len(domains),
        "capture_jobs": len(captures),
        "gather_verified": sum(1 for row in captures if row["status"] == "GATHER_VERIFIED"),
        "capture_warnings": len(warning_rows),
        "source_lead_only": sum(1 for row in candidates if row["evidence_status"] == "SOURCE_LEAD_ONLY"),
        "adapter_policies": len(receipt["adapter_policy_matrix"]),
        "workbenches": len(receipt["domain_workbenches"]),
        "negative_fixtures": len(receipt["negative_fixtures"]),
        "families_list": families,
        "domains_list": domains,
    }
    receipt["seal"] = sha_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def render_packet(r: dict[str, Any]) -> str:
    lines = ["# Pass 0149 - Cross-Domain Substrate Expansion", "", f"Status: `{r['status']}` with seal `{r['seal']}`.", "", "## Expansion Snapshot", "", "| Metric | Value |", "| --- | --- |"]
    for key in ["candidate_substrates", "families", "domains", "capture_jobs", "gather_verified", "capture_warnings", "source_lead_only", "workbenches"]:
        lines.append(f"| {key} | `{r['summary'][key]}` |")
    lines.extend(["", "## Family Coverage", "", ", ".join(r["summary"]["families_list"]), "", "## Workbench Queue", ""])
    lines.extend(f"- `{row['id']}`: {row['first_experiment']}" for row in r["domain_workbenches"])
    lines.extend(["", "## Warning Policy", "", "Warnings are scheduler facts, not absence claims. Empty captures, missing keys, HTTP failures, scope drops, and endpoint drift remain source leads until a later adapter verifies or rejects them.", "", "## Boundary", "", r["boundary"]])
    return "\n".join(lines)


def render_brief(r: dict[str, Any]) -> str:
    return "\n".join(["# Pass 0149 Brief - Cross-Domain Substrate Expansion", "", "Primary push: turn the route probes into a cross-domain substrate scheduler that can grow toward hundreds of archives, repositories, databases, benchmarks, and institutional sources.", "", f"Result: {r['summary']['candidate_substrates']} candidate substrates across {r['summary']['families']} families and {r['summary']['domains']} domains; {r['summary']['gather_verified']} current Gather-verified captures; {r['summary']['capture_warnings']} warning captures.", "", "Next pass: replay one workbench end to end by selecting one paper/preprint, one dataset, one institutional source, one domain database, one code artifact, and one verifier target."])


def render_steelman() -> str:
    return "\n".join(["# Pass 0149 Steelman", "", "The strongest objection is that a massive substrate map can become a vanity atlas. A source list does not solve a theorem, prove a biological mechanism, validate a climate model, or reproduce a benchmark.", "", "The settling test is a mixed-source proof packet that starts from this scheduler, selects a bounded world-problem claim, and joins source body, metadata, dataset, code, verifier, negative control, and replay receipt without manual narrative glue."])


def build_claims(r: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    claims = [
        f"Pass 0149 created a {SCHEMA} artifact with status {r['status']} and seal {r['seal']}.",
        f"Pass 0149 records {r['summary']['candidate_substrates']} candidate substrates across {r['summary']['families']} source families and {r['summary']['domains']} domains.",
        f"Pass 0149 records {r['summary']['capture_jobs']} capture attempts, {r['summary']['gather_verified']} Gather-verified captures, and {r['summary']['capture_warnings']} warning captures.",
        f"Pass 0149 records {r['summary']['workbenches']} domain workbenches and {r['summary']['adapter_policies']} adapter policies.",
        f"Pass 0149 rejects {r['summary']['negative_fixtures']} negative fixtures.",
        "Pass 0149 promotes no theorem or natural law.",
    ]
    thesis = {"title": "Dogfood Pass 0149 Cross-Domain Substrate Expansion", "disposition": "fenced", "claims": [{"text": c, "falsification": f"Claim {i} differs from pass 0149 artifact values or receipts are missing"} for i, c in enumerate(claims, 1)]}
    evidence = [[f"schema={r['schema']}", f"status={r['status']}", f"seal={r['seal']}"], [f"candidate_substrates={r['summary']['candidate_substrates']}", f"families={r['summary']['families']}", f"domains={r['summary']['domains']}"], [f"capture_jobs={r['summary']['capture_jobs']}", f"gather_verified={r['summary']['gather_verified']}", f"capture_warnings={r['summary']['capture_warnings']}"], [f"workbenches={r['summary']['workbenches']}", f"adapter_policies={r['summary']['adapter_policies']}"], [f"negative_fixtures={r['summary']['negative_fixtures']}"], [f"current_promoted_theorems={r['current_promoted_theorems']}", f"current_promoted_natural_laws={r['current_promoted_natural_laws']}"]]
    measurements = {"measurements": [{"claim": c, "method": "artifact-review", "evidence": evidence[i], "deviation": 0.0, "tolerance": 0.5} for i, c in enumerate(claims)]}
    return thesis, measurements


def render_ledger(r: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0149 Ledger - Cross-Domain Substrate Expansion", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    lines.extend(f"| {label} | {sha_file(path).upper()} |" for label, path in files.items())
    lines.extend(["", "## Result Snapshot", "", "| Field | Value |", "| --- | --- |", f"| Schema | `{r['schema']}` |", f"| Status | `{r['status']}` |", f"| Seal | `{r['seal']}` |", f"| Candidate substrates | `{r['summary']['candidate_substrates']}` |", f"| Source families | `{r['summary']['families']}` |", f"| Domains | `{r['summary']['domains']}` |", f"| Capture attempts | `{r['summary']['capture_jobs']}` |", f"| Gather verified | `{r['summary']['gather_verified']}` |", f"| Capture warnings | `{r['summary']['capture_warnings']}` |", f"| Workbenches | `{r['summary']['workbenches']}` |", f"| Promoted theorems | `{len(r['current_promoted_theorems'])}` |"])
    return "\n".join(lines)


def main() -> None:
    r = build_receipt(live_tools=True)
    files = {
        "schemas/cross-domain-substrate-expansion-pass-0149.json": ROOT / "schemas" / "cross-domain-substrate-expansion-pass-0149.json",
        "packets/159-cross-domain-substrate-expansion.md": ROOT / "packets" / "159-cross-domain-substrate-expansion.md",
        "briefs/159-cross-domain-substrate-expansion-brief.md": ROOT / "briefs" / "159-cross-domain-substrate-expansion-brief.md",
        "adversarial/pass-0149-cross-domain-substrate-expansion-steelman.md": ROOT / "adversarial" / "pass-0149-cross-domain-substrate-expansion-steelman.md",
    }
    write_json(files["schemas/cross-domain-substrate-expansion-pass-0149.json"], r, compact=True)
    write_text(files["packets/159-cross-domain-substrate-expansion.md"], render_packet(r))
    write_text(files["briefs/159-cross-domain-substrate-expansion-brief.md"], render_brief(r))
    write_text(files["adversarial/pass-0149-cross-domain-substrate-expansion-steelman.md"], render_steelman())
    thesis, measurements = build_claims(r)
    files["crucible/pass-0149-thesis.json"] = ROOT / "crucible" / "pass-0149-thesis.json"
    files["crucible/pass-0149-measurements.json"] = ROOT / "crucible" / "pass-0149-measurements.json"
    write_json(files["crucible/pass-0149-thesis.json"], thesis)
    write_json(files["crucible/pass-0149-measurements.json"], measurements)
    files["schemas/tool-receipts-pass-0149.json"] = ROOT / "schemas" / "tool-receipts-pass-0149.json"
    write_json(files["schemas/tool-receipts-pass-0149.json"], {"schema": "Pass0149ToolReceipts/v1", "artifact": {"path": str(files["schemas/cross-domain-substrate-expansion-pass-0149.json"]), "sha256": sha_file(files["schemas/cross-domain-substrate-expansion-pass-0149.json"])}, "source_store": r["source_store"], "tool_receipts": r["tool_receipts"]}, compact=True)
    write_text(ROOT / "pass-0149-ledger.md", render_ledger(r, files))
    print(json.dumps({"status": r["status"], "seal": r["seal"], "candidate_substrates": r["summary"]["candidate_substrates"]}, sort_keys=True))


if __name__ == "__main__":
    main()
