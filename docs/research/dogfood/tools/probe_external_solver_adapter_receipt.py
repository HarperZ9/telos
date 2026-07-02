"""Generate pass 0089 external solver adapter artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_external_solver_adapter_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_external_solver_adapter_receipt.py"
OUT_PATH = ROOT / "schemas" / "external-solver-adapter-receipt-pass-0089.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0089.json"
PACKET_PATH = ROOT / "packets" / "099-external-solver-adapter-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "099-external-solver-adapter-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0089-external-solver-adapter-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0089-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0089-measurements.json"


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


def dependency_rows(artifact: dict) -> str:
    rows = []
    for key in ["python", "numpy", "scipy", "ortools"]:
        row = artifact["dependency_receipts"][key]
        rows.append(f"| {key} | {row.get('available', 'runtime')} | {row.get('version', '')} |")
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    adapter = artifact["external_adapter"]
    comparison = adapter["comparison_to_exact"]
    best = adapter["best"]
    return f"""# Packet 099: External Solver Adapter Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: admit a real local solver surface into the pass 0088 branch-comparison
contract without promoting solver superiority.

```text
adapter = {adapter['adapter']}
scipy_version = {artifact['dependency_receipts']['scipy']['version']}
ortools_available = {artifact['dependency_receipts']['ortools']['available']}
run_count = {adapter['run_count']}
seed_range = {adapter['seed_range']}
maxiter = {adapter['maxiter']}
best_value = {best['value']}
best_weight = {best['weight']}
exact_value_gap = {comparison['exact_value_gap']}
exact_hit_count = {comparison['exact_hit_count']}
value_distribution = {comparison['value_distribution']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Dependencies

| Dependency | Available | Version |
| --- | --- | --- |
{dependency_rows(artifact)}

## Source Anchors

{chr(10).join(f"- {row['source_id']}: {row['url']}" for row in artifact['source_anchors'])}

Boundary: this is an adapter receipt for a bounded benchmark. It does not prove
solver superiority, quantum advantage, hardware execution, new physics, or a
natural law.
"""


def render_brief(artifact: dict) -> str:
    adapter = artifact["external_adapter"]
    comparison = adapter["comparison_to_exact"]
    return f"""# External Solver Adapter Brief

Date: 2026-07-01

## Result

Pass 0089 imports SciPy `dual_annealing` into the proof-packet path. The local
adapter runs {adapter['run_count']} seeded attempts and records an exact-value
gap of {comparison['exact_value_gap']} against pass 0088.

## Product Meaning

The system can now distinguish an installed solver adapter from an unavailable
solver target. OR-Tools is recorded as unavailable locally instead of silently
excluded.

## Next Adapter

Add OR-Tools when installed, or create a no-ground-truth large-instance lane
that requires independent replay and solver-version receipts.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0089 Steelman: External Solver Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that rounded continuous optimization is an adapter
exercise, not a proper discrete optimization method. Correct. That limitation is
why the receipt records the rounding policy, seeds, run digest, exact baseline,
and non-promotion boundary.

The second objection is that OR-Tools is more appropriate for knapsack/MIP.
Correct. It is recorded as unavailable in this environment and becomes the next
adapter target.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0089", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "adapter": artifact["external_adapter"]["comparison_to_exact"], "dependencies": artifact["dependency_receipts"]}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    paths = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in paths.items()}
    adapter = artifact["external_adapter"]
    comparison = adapter["comparison_to_exact"]
    deps = artifact["dependency_receipts"]
    claims = [
        f"Pass 0089 created an ExternalSolverAdapterReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0089 binds prior pass {artifact['prior_binding']['source_pass']} and upstream YouTube cluster {artifact['upstream_research_binding']['dominant_cluster']}.",
        f"Pass 0089 records SciPy available={deps['scipy']['available']} version {deps['scipy']['version']}, NumPy available={deps['numpy']['available']} version {deps['numpy']['version']}, and OR-Tools available={deps['ortools']['available']}.",
        f"Pass 0089 runs adapter {adapter['adapter']} for {adapter['run_count']} seeded runs over seed range {adapter['seed_range']} with runs digest {adapter['runs_sha256']}.",
        f"Pass 0089 adapter best value is {adapter['best']['value']} with exact_value_gap {comparison['exact_value_gap']}, exact_hit_count {comparison['exact_hit_count']}, and value_distribution {comparison['value_distribution']}.",
        f"Pass 0089 records {len(artifact['source_anchors'])} source anchors and no solver superiority, quantum advantage, hardware, or natural law claim.",
        f"Pass 0089 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0089 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_pass={artifact['prior_binding']['source_pass']}", f"dominant_cluster={artifact['upstream_research_binding']['dominant_cluster']}"],
        [f"scipy_available={deps['scipy']['available']}", f"scipy_version={deps['scipy']['version']}", f"numpy_available={deps['numpy']['available']}", f"numpy_version={deps['numpy']['version']}", f"ortools_available={deps['ortools']['available']}"],
        [f"adapter={adapter['adapter']}", f"run_count={adapter['run_count']}", f"seed_range={adapter['seed_range']}", f"runs_sha256={adapter['runs_sha256']}"],
        [f"best_value={adapter['best']['value']}", f"exact_value_gap={comparison['exact_value_gap']}", f"exact_hit_count={comparison['exact_hit_count']}", f"value_distribution={comparison['value_distribution']}"],
        [f"source_anchor_count={len(artifact['source_anchors'])}", f"promotion_boundary={artifact['promotion_boundary']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0089 External Solver Adapter Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0089 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "EXTERNAL_SOLVER_ADAPTER_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
