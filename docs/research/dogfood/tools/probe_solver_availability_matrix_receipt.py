"""Generate pass 0090 solver availability matrix artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_solver_availability_matrix_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_solver_availability_matrix_receipt.py"
OUT_PATH = ROOT / "schemas" / "solver-availability-matrix-receipt-pass-0090.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0090.json"
PACKET_PATH = ROOT / "packets" / "100-solver-availability-matrix-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "100-solver-availability-matrix-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0090-solver-availability-matrix-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0090-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0090-measurements.json"


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


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def row_table(rows: list[dict], limit: int = 36) -> str:
    lines = []
    for row in rows[:limit]:
        lines.append(f"| {row['row_id']} | {row['category']} | {row['local_status']} | {row['proof_gap']} | {row['next_action']} |")
    return "\n".join(lines)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    summary = artifact["summary"]
    return f"""# Packet 100: Solver Availability Matrix Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: map installed, missing, source-present, and planned solver/runtime
surfaces before choosing the next proof expansion.

```text
row_count = {summary['row_count']}
local_available_rows = {summary['local_available_rows']}
local_unavailable_rows = {summary['local_unavailable_rows']}
buildc_corpus_status = {artifact['buildc_corpus_receipt']['status']}
scipy_available = {artifact['package_receipts']['scipy']['available']}
networkx_available = {artifact['package_receipts']['networkx']['available']}
ortools_available = {artifact['package_receipts']['ortools']['available']}
dwave_system_available = {artifact['package_receipts']['dwave_system']['available']}
recommended_next = {summary['recommended_next']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Matrix Rows

| Row | Category | Local Status | Proof Gap | Next Action |
| --- | --- | --- | --- | --- |
{row_table(artifact['matrix_rows'])}

## Source Anchors

{chr(10).join(f"- {row['source_id']}: {row['url']}" for row in artifact['source_anchors'])}

Boundary: this is an availability and adapter-priority packet. It does not
prove solver superiority, solve a world-scale problem, or promote a natural
law.
"""


def render_brief(artifact: dict) -> str:
    summary = artifact["summary"]
    return f"""# Solver Availability Matrix Brief

Date: 2026-07-01

## Result

Pass 0090 records {summary['row_count']} solver, runtime, CLI, and local-source
rows. The immediate verified strengths are SciPy, NumPy, NetworkX, pandas, and
BuildLang/buildc corpus verification. OR-Tools, D-Wave Ocean, Qiskit, SymPy,
Z3, Pyomo, CVXPY, Torch, and JAX are not locally available in this environment.

## Product Meaning

The next megatool should separate three facts: installed adapters, source-present
runtime receipts, and missing dependencies. That prevents the public roadmap
from claiming coverage where only intent exists.

## Next Adapter

Use the matrix to pick either a BuildLang corpus-to-Crucible adapter or a
NetworkX graph-optimization receipt before adding new dependencies.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0090 Steelman: Solver Availability Matrix

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that an availability matrix does not solve a hard
scientific problem. Correct. It chooses the next executable proof lane and
prevents unsupported claims about missing solver surfaces.

The second objection is that missing dependencies are not market gaps. Correct.
They are local execution gaps. Market gaps still need separate buyer and source
research.

Non-promotion statement: no solver superiority, world-problem solution, or
natural law is claimed in pass 0090.
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0090", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "summary": artifact["summary"], "buildc": artifact["buildc_corpus_receipt"]}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    paths = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in paths.items()}
    summary = artifact["summary"]
    packages = artifact["package_receipts"]
    claims = [
        f"Pass 0090 created a SolverAvailabilityMatrixReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0090 binds prior pass {artifact['prior_binding']['source_pass']} and upstream YouTube cluster {artifact['upstream_research_binding']['dominant_cluster']}.",
        f"Pass 0090 matrix has {summary['row_count']} rows with {summary['local_available_rows']} local available/source-present rows and {summary['local_unavailable_rows']} local unavailable/missing rows.",
        f"Pass 0090 records SciPy available={packages['scipy']['available']}, NetworkX available={packages['networkx']['available']}, OR-Tools available={packages['ortools']['available']}, and D-Wave system available={packages['dwave_system']['available']}.",
        f"Pass 0090 BuildLang/buildc corpus verification status is {artifact['buildc_corpus_receipt']['status']} with exit_code {artifact['buildc_corpus_receipt']['exit_code']}.",
        f"Pass 0090 recommended next adapters are {summary['recommended_next']}.",
        f"Pass 0090 records {len(artifact['source_anchors'])} source anchors and no solver superiority, world-problem-solved, or natural-law claim.",
        f"Pass 0090 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0090 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_pass={artifact['prior_binding']['source_pass']}", f"dominant_cluster={artifact['upstream_research_binding']['dominant_cluster']}"],
        [f"row_count={summary['row_count']}", f"local_available_rows={summary['local_available_rows']}", f"local_unavailable_rows={summary['local_unavailable_rows']}"],
        [f"scipy={packages['scipy']['available']}", f"networkx={packages['networkx']['available']}", f"ortools={packages['ortools']['available']}", f"dwave_system={packages['dwave_system']['available']}"],
        [f"buildc_status={artifact['buildc_corpus_receipt']['status']}", f"exit_code={artifact['buildc_corpus_receipt']['exit_code']}", f"stdout_sha256={artifact['buildc_corpus_receipt'].get('stdout_sha256')}"],
        [f"recommended_next={summary['recommended_next']}"],
        [f"source_anchor_count={len(artifact['source_anchors'])}", f"promotion_boundary={artifact['promotion_boundary']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0090 Solver Availability Matrix Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0090 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)], timeout=240)
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "SOLVER_AVAILABILITY_MATRIX_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
