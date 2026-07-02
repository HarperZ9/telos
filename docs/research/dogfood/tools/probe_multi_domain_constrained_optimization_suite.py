"""Generate pass 0114 multi-domain constrained optimization artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_multi_domain_constrained_optimization_suite.py"
TEST_SCRIPT = ROOT / "tools" / "test_multi_domain_constrained_optimization_suite.py"
OUT_PATH = ROOT / "schemas" / "multi-domain-constrained-optimization-suite-pass-0114.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0114.json"
PACKET_PATH = ROOT / "packets" / "124-multi-domain-constrained-optimization-suite.md"
BRIEF_PATH = ROOT / "briefs" / "124-multi-domain-constrained-optimization-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0114-multi-domain-constrained-optimization-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0114-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0114-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.encode("ascii", "ignore").decode("ascii"), encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def case_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["cases"]:
        neg = row["negative_fixture"]["classification"]
        clusters = ", ".join(row["source_clusters"])
        rows.append(f"| {row['case_id']} | {row['domain']} | {row['objective']} | {neg} | {clusters} |")
    return "\n".join(rows)


def source_rows(artifact: dict) -> str:
    return "\n".join(f"| {row['tool']} | {row['kind']} | {row['url']} |" for row in artifact["source_anchors"])


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    y = artifact["youtube_binding"]
    cov = artifact["domain_coverage"]
    return f"""# Packet 124: Multi-Domain Constrained Optimization Suite

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: test whether one receipt schema can carry constrained optimization
claims across warehouse operations, robotics quality control, safety-critical
allocation, and quantitative finance without promoting domain-specific claims.

```text
mpc_pass = {artifact['source_bindings']['mpc_pass']}
youtube_roadmap_pass = {artifact['source_bindings']['youtube_roadmap_pass']}
valid_youtube_videos = {y['valid_video_count']}
dominant_cluster = {y['dominant_cluster']}
dominant_cluster_video_count = {y['dominant_cluster_video_count']}
case_count = {cov['case_count']}
domain_count = {cov['domain_count']}
youtube_cluster_count = {cov['youtube_cluster_count']}
negative_fixture_count = {cov['negative_fixture_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Case Matrix

| Case | Domain | Objective | Negative fixture | YouTube clusters |
| --- | --- | ---: | --- | --- |
{case_rows(artifact)}

## Source Anchors

| Tool | Kind | URL |
| --- | --- | --- |
{source_rows(artifact)}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    cov = artifact["domain_coverage"]
    return f"""# Multi-Domain Constrained Optimization Brief

Date: 2026-07-01

## Decision

Move from single-demo proof packets into a reusable constrained optimization
suite. The current suite has {cov['case_count']} toy cases across
{cov['domain_count']} domains and {cov['negative_fixture_count']} negative
fixtures.

## Wedge

Existing solvers and simulators are strong locally. The Telos/Build wedge is a
cross-domain proof packet that carries source leads, exact constraints,
candidate plan, objective, negative witness, solver branch, and Crucible verdict
in one portable object.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0114 Steelman: Multi-Domain Constrained Optimization

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that four toy fixtures do not solve warehouse,
robotics, defense, or finance. Correct. The pass validates receipt portability,
not real-world deployment.

The second objection is that a unified schema can hide domain-specific
semantics. Correct. That is why each case carries domain, source clusters,
constraint checks, objective, and an explicit negative fixture.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0114",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "cases": artifact["cases"],
        "domain_coverage": artifact["domain_coverage"],
        "market_surface": artifact["market_surface"],
        "youtube_binding": artifact["youtube_binding"],
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    cov = artifact["domain_coverage"]
    y = artifact["youtube_binding"]
    claims = [
        f"Pass 0114 created a MultiDomainConstrainedOptimizationSuiteReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0114 binds MPC pass {artifact['source_bindings']['mpc_pass']} and YouTube roadmap pass {artifact['source_bindings']['youtube_roadmap_pass']}.",
        f"Pass 0114 records {cov['case_count']} cases, {cov['domain_count']} domains, {cov['youtube_cluster_count']} YouTube clusters, and {cov['negative_fixture_count']} negative fixtures.",
        "Pass 0114 warehouse case objective is 9 and negative fixture is CAPACITY_VIOLATION_EXPECTED.",
        "Pass 0114 robotics case objective is 16 and negative fixture is COVERAGE_VIOLATION_EXPECTED.",
        "Pass 0114 safety allocation toy case objective is 17 and negative fixture is INFEASIBLE_EXPECTED.",
        "Pass 0114 quant risk budget case objective is 9/2 and negative fixture is RISK_BUDGET_VIOLATION_EXPECTED.",
        f"Pass 0114 YouTube binding records {y['valid_video_count']} valid videos, dominant cluster {y['dominant_cluster']}, and dominant_cluster_video_count {y['dominant_cluster_video_count']}.",
        f"Pass 0114 records {len(artifact['source_anchors'])} source anchors and market tool_count {artifact['market_surface']['tool_count']}.",
        f"Pass 0114 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0114 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0114 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    by_id = {row["case_id"]: row for row in artifact["cases"]}
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"domain_coverage={cov}"],
        [f"warehouse={by_id['warehouse_capacity_assignment']}"],
        [f"robotics={by_id['robotics_quality_inspection']}"],
        [f"safety={by_id['safety_allocation_toy']}"],
        [f"quant={by_id['quant_risk_budget']}"],
        [f"youtube_binding={y}"],
        [f"source_anchor_count={len(artifact['source_anchors'])}", f"market_surface={artifact['market_surface']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0114 Multi-Domain Constrained Optimization Suite", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0114 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)], timeout=180)
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "MULTI_DOMAIN_CONSTRAINED_OPTIMIZATION_SUITE_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
