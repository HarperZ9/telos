"""Compose pass 0146 adapter retry policy artifact."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "AdapterRetryPolicyReceipt/v1"
PASS_ID = "0146"
STATUS = "ADAPTER_RETRY_POLICY_MATCH"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PLAN = ROOT / "fixtures" / "pass-0146-adapter-retry-policy-plan.json"


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
    path = store / "objects" / row["sha256"][:2] / row["sha256"][2:]
    return path.read_text(encoding="utf-8", errors="replace")


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


def source_evidence(plan: dict[str, Any], store: Path) -> list[dict[str, Any]]:
    rows = catalog(store)
    by_ref = {row["ref"]: row for row in rows}
    evidence = []
    for source in plan["policy_sources"]:
        row = by_ref[source["url"]]
        text = body(store, row).lower()
        matches = [signal for signal in source["required_signals"] if signal.lower() in text]
        evidence.append(
            {
                "id": source["id"],
                "system": source["system"],
                "url": source["url"],
                "sha256": row["sha256"],
                "title": row.get("title", ""),
                "required_signals": source["required_signals"],
                "matched_signals": matches,
                "status": "MATCH" if len(matches) == len(source["required_signals"]) else "PARTIAL",
            }
        )
    return evidence


def policy_rules() -> list[dict[str, Any]]:
    return [
        {"id": "RATE_LIMITED_429", "status": "SOURCE_LEAD_ONLY_RETRYABLE", "action": "honor Retry-After if present; otherwise exponential backoff and lower concurrency"},
        {"id": "RETRY_AFTER_PARSE", "status": "SCHEDULER_REQUIRED", "action": "accept HTTP-date or delay-seconds and record the parsed wait"},
        {"id": "NO_AUTO_RETRY_ON_HEADERLESS_503", "status": "HALT_OR_OPERATOR_POLICY", "action": "do not tight-loop when a repository omits Retry-After"},
        {"id": "CROSSREF_POLITE_MAILTO", "status": "CONTACTABILITY_REQUIRED", "action": "include mailto or user-agent for Crossref public/polite pool accountability"},
        {"id": "CROSSREF_403_BLOCKED", "status": "ACCESS_ESCALATION", "action": "stop retries and record block/support path"},
        {"id": "OPENALEX_API_KEY_CURRENT", "status": "AUTH_POLICY", "action": "treat mailto-only OpenAlex polite-pool logic as stale after the API-key shift"},
        {"id": "OPENALEX_BACKOFF", "status": "SCHEDULER_REQUIRED", "action": "read rate headers and use exponential backoff on 429"},
        {"id": "ROR_CLIENT_ID_READY", "status": "AUTH_POLICY", "action": "prepare client-id field for Q3 2026 rate-limit split"},
        {"id": "ROR_LOCAL_DOCKER_FALLBACK", "status": "BULK_FALLBACK", "action": "route high-volume ROR work to local Docker mirror when needed"},
        {"id": "OAI_RESUMPTION_TOKEN_CHAIN", "status": "PAGINATION_CONTRACT", "action": "persist token, cursor, completeListSize, and expiration when supplied"},
        {"id": "OAI_BAD_RESUMPTION_RESTART", "status": "CHECKPOINT_REQUIRED", "action": "restart from bounded date/set checkpoint, not from an arbitrary token"},
        {"id": "INDEX_SELECTOR_ROOT_FALLBACK", "status": "CONTEXT_SELECTOR_DRIFT", "action": "retry root-only context and record selector failure as tool-interface evidence"},
    ]


def scenarios(plan: dict[str, Any], rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rule_ids = {rule["id"] for rule in rules}
    mapping = {
        "crossref_429_no_retry_after": "RATE_LIMITED_429",
        "crossref_403_blocked": "CROSSREF_403_BLOCKED",
        "openalex_429_with_headers": "OPENALEX_BACKOFF",
        "openalex_mailto_only": "OPENALEX_API_KEY_CURRENT",
        "ror_anonymous_high_volume": "ROR_CLIENT_ID_READY",
        "oai_503_retry_after": "RETRY_AFTER_PARSE",
        "oai_503_without_retry_after": "NO_AUTO_RETRY_ON_HEADERLESS_503",
        "oai_bad_resumption_token": "OAI_BAD_RESUMPTION_RESTART",
        "stale_repository_endpoint_404": "INDEX_SELECTOR_ROOT_FALLBACK",
        "index_unknown_focus_repo": "INDEX_SELECTOR_ROOT_FALLBACK",
    }
    out = []
    for item in plan["scenario_fixtures"]:
        rule = mapping[item["id"]]
        out.append({**item, "rule": rule, "status": "MATCH" if rule in rule_ids else "DRIFT", "promotion_allowed": False})
    return out


def build_receipt(live_tools: bool = True) -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    store = REPO / plan["source_store"]
    prior = json.loads((REPO / plan["prior_receipt"]).read_text(encoding="utf-8"))
    evidence = source_evidence(plan, store)
    rules = policy_rules()
    scenario_rows = scenarios(plan, rules)
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": STATUS if all(row["status"] in ("MATCH", "PARTIAL") for row in evidence) and all(row["status"] == "MATCH" for row in scenario_rows) else "ADAPTER_RETRY_POLICY_DRIFT",
        "source_store": plan["source_store"],
        "source_captures": len(evidence),
        "source_systems": sorted({row["system"] for row in evidence} | {"Index"}),
        "source_evidence": evidence,
        "policy_rules": rules,
        "scenario_fixtures": scenario_rows,
        "prior_pass_warnings": prior["source_warnings"],
        "negative_fixtures": [{"fixture_id": name, "expected_status": "REJECT"} for name in plan["negative_fixtures"]],
        "integration_targets": ["RateLimitLedger", "EndpointAliasRegistry", "SourceFamilyScheduler", "IndexSelectorFallbackReceipt"],
        "market_implication": "A research substrate product becomes more defensible when source-family flow control is captured as evidence, because rate limits and stale endpoints stop masquerading as missing knowledge.",
        "updated_tool_floor": plan["updated_tool_floor"],
        "tool_receipts": tool_receipts() if live_tools else {},
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "boundary": "Pass 0146 defines scheduler and promotion policy for source adapters. It does not prove source correctness, complete coverage, market uniqueness, theorem progress, or natural-law discovery.",
    }
    receipt["summary"] = {
        "policy_sources": receipt["source_captures"],
        "source_systems": len(receipt["source_systems"]),
        "policy_rules": len(rules),
        "scenario_fixtures": len(scenario_rows),
        "negative_fixtures": len(receipt["negative_fixtures"]),
        "prior_warnings": len(receipt["prior_pass_warnings"]),
    }
    receipt["seal"] = sha_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def render_packet(r: dict[str, Any]) -> str:
    lines = ["# Pass 0146 - Adapter Retry Policy", "", f"Status: `{r['status']}` with seal `{r['seal']}`.", "", "## Policy Rows", "", "| Rule | Status | Action |", "| --- | --- | --- |"]
    lines.extend(f"| `{row['id']}` | `{row['status']}` | {row['action']} |" for row in r["policy_rules"])
    lines.extend(["", "## What Changed", "", "- Cornell-style 429s become retryable source leads, not absence evidence.", "- Caltech-style endpoint drift becomes an endpoint alias warning, not repository absence.", "- OpenAlex mailto-only logic is rejected as stale after its API-key shift.", "- OAI-PMH resumption tokens become checkpointed pagination state.", "- Index selector failures become context-selector drift receipts with root fallback.", "", "## Boundary", "", r["boundary"]])
    return "\n".join(lines)


def render_brief(r: dict[str, Any]) -> str:
    return "\n".join(["# Pass 0146 Brief - Adapter Retry Policy", "", "Primary push: make source adapters robust enough for registry-scale research without turning access failures into false knowledge claims.", "", f"Result: {r['summary']['policy_rules']} rules over {r['summary']['policy_sources']} source-policy captures and {r['summary']['scenario_fixtures']} scenario fixtures.", "", "Next pass: implement a broader institution queue that uses these policy statuses as first-class receipt fields."])


def render_steelman() -> str:
    return "\n".join(["# Pass 0146 Steelman", "", "The strongest objection is that policy receipts are still not a scheduler. They define how an adapter should behave, but they do not prove sustained load behavior, fairness, or archive completeness.", "", "The settling test is a runner that executes bounded retries against a mixed institution queue, records waits and fallbacks, and proves no rate-limit or endpoint error is promoted into a stronger research claim."])


def build_claims(r: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    claims = [
        f"Pass 0146 created an {SCHEMA} artifact with status {r['status']} and seal {r['seal']}.",
        f"Pass 0146 records {r['summary']['policy_sources']} source-policy captures across {r['summary']['source_systems']} source systems.",
        f"Pass 0146 records {r['summary']['policy_rules']} policy rules and {r['summary']['scenario_fixtures']} scenario fixtures.",
        f"Pass 0146 rejects {r['summary']['negative_fixtures']} negative fixtures and carries {r['summary']['prior_warnings']} prior warnings forward.",
        "Pass 0146 promotes no theorem or natural law.",
    ]
    thesis = {"title": "Dogfood Pass 0146 Adapter Retry Policy", "disposition": "fenced", "claims": [{"text": c, "falsification": f"Claim {i} differs from artifact values or receipts are missing"} for i, c in enumerate(claims, 1)]}
    evidence = [[f"schema={r['schema']}", f"status={r['status']}", f"seal={r['seal']}"], [f"source_evidence={len(r['source_evidence'])}", f"source_systems={r['source_systems']}"], [f"rules={len(r['policy_rules'])}", f"scenarios={len(r['scenario_fixtures'])}"], [f"negative_fixtures={len(r['negative_fixtures'])}", f"prior_warnings={len(r['prior_pass_warnings'])}"], [f"current_promoted_theorems={r['current_promoted_theorems']}", f"current_promoted_natural_laws={r['current_promoted_natural_laws']}"]]
    return thesis, {"measurements": [{"claim": c, "method": "artifact-review", "evidence": evidence[i], "deviation": 0.0, "tolerance": 0.5} for i, c in enumerate(claims)]}


def render_ledger(r: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0146 Ledger - Adapter Retry Policy", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    lines.extend(f"| {label} | {sha_file(path).upper()} |" for label, path in files.items())
    lines.extend(["", "## Result Snapshot", "", "| Field | Value |", "| --- | --- |", f"| Schema | `{r['schema']}` |", f"| Status | `{r['status']}` |", f"| Seal | `{r['seal']}` |", f"| Policy sources | `{r['summary']['policy_sources']}` |", f"| Source systems | `{r['summary']['source_systems']}` |", f"| Policy rules | `{r['summary']['policy_rules']}` |", f"| Scenario fixtures | `{r['summary']['scenario_fixtures']}` |", f"| Negative fixtures | `{r['summary']['negative_fixtures']}` |", f"| Promoted theorems | `{len(r['current_promoted_theorems'])}` |"])
    return "\n".join(lines)


def main() -> None:
    r = build_receipt(live_tools=True)
    files = {
        "schemas/adapter-retry-policy-pass-0146.json": ROOT / "schemas" / "adapter-retry-policy-pass-0146.json",
        "packets/156-adapter-retry-policy.md": ROOT / "packets" / "156-adapter-retry-policy.md",
        "briefs/156-adapter-retry-policy-brief.md": ROOT / "briefs" / "156-adapter-retry-policy-brief.md",
        "adversarial/pass-0146-adapter-retry-policy-steelman.md": ROOT / "adversarial" / "pass-0146-adapter-retry-policy-steelman.md",
    }
    write_json(files["schemas/adapter-retry-policy-pass-0146.json"], r)
    write_text(files["packets/156-adapter-retry-policy.md"], render_packet(r))
    write_text(files["briefs/156-adapter-retry-policy-brief.md"], render_brief(r))
    write_text(files["adversarial/pass-0146-adapter-retry-policy-steelman.md"], render_steelman())
    thesis, measurements = build_claims(r)
    files["crucible/pass-0146-thesis.json"] = ROOT / "crucible" / "pass-0146-thesis.json"
    files["crucible/pass-0146-measurements.json"] = ROOT / "crucible" / "pass-0146-measurements.json"
    write_json(files["crucible/pass-0146-thesis.json"], thesis)
    write_json(files["crucible/pass-0146-measurements.json"], measurements)
    files["schemas/tool-receipts-pass-0146.json"] = ROOT / "schemas" / "tool-receipts-pass-0146.json"
    write_json(files["schemas/tool-receipts-pass-0146.json"], {"schema": "Pass0146ToolReceipts/v1", "artifact": {"path": str(files["schemas/adapter-retry-policy-pass-0146.json"]), "sha256": sha_file(files["schemas/adapter-retry-policy-pass-0146.json"])}, "source_store": r["source_store"], "tool_receipts": r["tool_receipts"]})
    write_text(ROOT / "pass-0146-ledger.md", render_ledger(r, files))
    print(json.dumps({"status": r["status"], "seal": r["seal"]}, sort_keys=True))


if __name__ == "__main__":
    main()
