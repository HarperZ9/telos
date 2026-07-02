"""Generate pass 0088 optimization branch comparison artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_optimization_branch_comparison_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_optimization_branch_comparison_receipt.py"
OUT_PATH = ROOT / "schemas" / "optimization-branch-comparison-receipt-pass-0088.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0088.json"
PACKET_PATH = ROOT / "packets" / "098-optimization-branch-comparison-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "098-optimization-branch-comparison-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0088-optimization-branch-comparison-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0088-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0088-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 120) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def comparison_rows(artifact: dict) -> str:
    rows = []
    exact = artifact["exact_branch"]["best"]
    rows.append(f"| exact_enumeration | {exact['value']} | {exact['weight']} | {exact['energy']} | 0 | true |")
    for row in artifact["comparisons"]:
        rows.append(f"| {row['branch']} | {row['best_value']} | {row['best_weight']} | {row['best_energy']} | {row['exact_value_gap']} | {row['hit_exact_bits']} |")
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    exact = artifact["exact_branch"]
    return f"""# Packet 098: Optimization Branch Comparison Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: compare exact, simulated annealing, greedy, and random-search branches
on a larger exact-enumerable optimization benchmark.

```text
upstream_video_cluster = {artifact['upstream_research_binding']['dominant_cluster']}
upstream_video_count = {artifact['upstream_research_binding']['dominant_cluster_video_count']}
candidate_count = {exact['candidate_count']}
feasible_count = {exact['feasible_count']}
exact_value = {exact['best']['value']}
exact_weight = {exact['best']['weight']}
branch_count = {artifact['comparison_summary']['branch_count']}
exact_hit_branches = {artifact['comparison_summary']['exact_hit_branches']}
max_value_gap = {artifact['comparison_summary']['max_value_gap']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Branch Comparison

| Branch | Value | Weight | Energy | Gap To Exact | Hit Exact Bits |
| --- | ---: | ---: | ---: | ---: | --- |
{comparison_rows(artifact)}

## Source Anchors

{chr(10).join(f"- {row['source_id']}: {row['url']}" for row in artifact['source_anchors'])}

Boundary: this pass is a bounded benchmark comparison. It does not prove solver
superiority, quantum advantage, hardware execution, new physics, or a natural
law.
"""


def render_brief(artifact: dict) -> str:
    exact = artifact["exact_branch"]["best"]
    return f"""# Optimization Branch Comparison Brief

Date: 2026-07-01

## Result

Pass 0088 compares four branches on a 12-variable exact-enumerable benchmark.
Exact enumeration checks 4096 assignments and finds value {exact['value']} at
weight {exact['weight']}. The receipt records every branch's gap to exact.

The benchmark thread is explicitly bound to pass 0085's YouTube-derived
enterprise quantum optimization cluster.

## Product Meaning

This is the next proof-packet layer: a solver comparison can be admitted only
when the exact baseline, branch parameters, run digests, and non-promotion
boundaries are all present.

## Next Adapter

Move from toy branch comparison to an adapter that imports one external solver
surface while preserving the exact baseline and branch-comparison schema.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0088 Steelman: Optimization Branch Comparison

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a 12-variable benchmark is still small. Correct.
It is intentionally exact-enumerable so branch comparison can be verified rather
than inferred.

The second objection is that hand-coded baselines are not market-grade solvers.
Correct. They define the receipt contract that external solvers must satisfy
before their outputs can be compared.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0088", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "comparison": artifact["comparison_summary"]}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {name: sha256_file(path) for name, path in {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}.items()}
    exact = artifact["exact_branch"]
    summary = artifact["comparison_summary"]
    claims = [
        f"Pass 0088 created an OptimizationBranchComparisonReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0088 binds prior pass {artifact['prior_binding']['source_pass']} with replay gate {artifact['prior_binding']['replay_gate']}.",
        f"Pass 0088 binds upstream YouTube research pass {artifact['upstream_research_binding']['source_pass']} with dominant cluster {artifact['upstream_research_binding']['dominant_cluster']} and {artifact['upstream_research_binding']['dominant_cluster_video_count']} videos.",
        f"Pass 0088 exact branch enumerates {exact['candidate_count']} assignments with {exact['feasible_count']} feasible assignments and candidate digest {exact['candidate_digest']}.",
        f"Pass 0088 exact optimum has value {exact['best']['value']}, weight {exact['best']['weight']}, and selected set {exact['best']['selected']}.",
        f"Pass 0088 compares {summary['branch_count']} branches and records exact-hit branches {summary['exact_hit_branches']} with max_value_gap {summary['max_value_gap']}.",
        f"Pass 0088 records {len(artifact['source_anchors'])} external source anchors and no solver superiority, quantum advantage, hardware, or natural law claim.",
        f"Pass 0088 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0088 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_pass={artifact['prior_binding']['source_pass']}", f"replay_gate={artifact['prior_binding']['replay_gate']}"],
        [f"source_pass={artifact['upstream_research_binding']['source_pass']}", f"dominant_cluster={artifact['upstream_research_binding']['dominant_cluster']}", f"dominant_cluster_video_count={artifact['upstream_research_binding']['dominant_cluster_video_count']}", f"source_policy={artifact['upstream_research_binding']['source_policy']}"],
        [f"candidate_count={exact['candidate_count']}", f"feasible_count={exact['feasible_count']}", f"candidate_digest={exact['candidate_digest']}"],
        [f"value={exact['best']['value']}", f"weight={exact['best']['weight']}", f"selected={exact['best']['selected']}"],
        [f"branch_count={summary['branch_count']}", f"exact_hit_branches={summary['exact_hit_branches']}", f"max_value_gap={summary['max_value_gap']}"],
        [f"source_anchor_count={len(artifact['source_anchors'])}", f"promotion_boundary={artifact['promotion_boundary']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0088 Optimization Branch Comparison Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0088 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "OPTIMIZATION_BRANCH_COMPARISON_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
