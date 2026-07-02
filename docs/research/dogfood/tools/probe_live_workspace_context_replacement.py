"""Generate pass 0071 receipts for live workspace-context replacement."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_live_workspace_context_replacement.py"
TEST_SCRIPT = ROOT / "tools" / "test_live_workspace_context_replacement.py"
OUT_PATH = ROOT / "schemas" / "live-workspace-context-replacement-pass-0071.json"
PACKET_PATH = ROOT / "packets" / "081-live-workspace-context-replacement.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0071-live-workspace-context-replacement-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0071-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0071-measurements.json"


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
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    return {"command": " ".join(command), "exit_code": result.returncode, "stderr_sha256": sha256_text(result.stderr), "stdout_sha256": sha256_text(result.stdout), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    workspace = [row for row in artifact["component_receipts"] if row["kind"] == "workspace_context"][0]
    negatives = "\n".join(f"- `{row['fixture_id']}` -> `{row['reject_reason']}`" for row in artifact["negative_fixtures"])
    checks = "\n".join(f"- `{key}`: {value}" for key, value in artifact["index_surface_checks"]["checks"].items())
    surface = artifact["live_surface"]
    summary = surface["summary"]
    return f"""# Packet 081: Live Workspace-Context Replacement

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: replace the pass 0070 synthetic workspace-context component with a
live local Index context envelope while retaining the live Telos action
component from pass 0070.

```text
live_surface_status = {surface['status']}
context_schema = {summary['schema']}
verification_verdict = {summary['verification_verdict']}
retained_count = {summary['retained_count']}
receipt_count = {summary['receipt_count']}
workspace_component = {workspace['component_id']}
component_count = {len(artifact['component_receipts'])}
negative_fixture_count = {len(artifact['negative_fixtures'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Index Surface Checks

{checks}

## Negative Fixtures

{negatives}

## Growth-Vector Finding

The root context envelope is usable as a live workspace-context receipt. The
path-focused probe currently rejects `docs/research/dogfood` as an unknown
focus repo, which marks a concrete ergonomic gap: Index needs a path-focus mode
or repo/path disambiguation layer before it can cleanly route field-specific
research packets inside a large monorepo.

Current promoted natural laws: none.
"""


def render_steelman(artifact: dict) -> str:
    probe = artifact["live_surface"]["focus_path_probe"]
    return f"""# Pass 0071 Steelman: Live Workspace-Context Replacement

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass improves the proof-packet spine by replacing the synthetic
workspace-context component with a live Index context envelope. The steelman
against overclaiming is direct: one budgeted root envelope with one retained
context item is not equivalent to complete monorepo understanding, semantic
retrieval, domain decomposition, or proof of market readiness.

The most useful growth vector surfaced by the experiment is not only that Index
can emit a receipt-backed context envelope. It is that path-level focus failed:
`{probe['observed_error']}`. For research megatools, this should become a
first-class path/domain focus mode so a biology, physics, color, buildc, or
agent-ops pass can bind only the relevant workspace slice without losing the
root receipt chain.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    workspace = [row for row in artifact["component_receipts"] if row["kind"] == "workspace_context"][0]
    summary = artifact["live_surface"]["summary"]
    claims = [
        f"Pass 0071 created a LiveWorkspaceContextReplacement/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0071 loaded live Index context envelope command {artifact['live_surface']['command']} with status {artifact['live_surface']['status']} and schema {summary['schema']}.",
        f"Pass 0071 Index surface checks have match {artifact['index_surface_checks']['match']} and drift {artifact['index_surface_checks']['drift']}.",
        f"Pass 0071 replaced the workspace_context component with {workspace['component_id']} and digest {workspace['digest']}.",
        f"Pass 0071 product packet has component_count {artifact['product_packet']['component_count']} and unsupported_claim_count {artifact['product_packet']['unsupported_claim_count']}.",
        f"Pass 0071 contains {len(artifact['negative_fixtures'])} negative fixtures and {len(artifact['ablation_results'])} ablation results.",
        f"Pass 0071 focus path probe exits {artifact['live_surface']['focus_path_probe']['exit_code']} with status {artifact['live_surface']['focus_path_probe']['status']}.",
        f"Pass 0071 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"command={artifact['live_surface']['command']}", f"status={artifact['live_surface']['status']}", f"schema={summary['schema']}"],
        [f"match={artifact['index_surface_checks']['match']}", f"drift={artifact['index_surface_checks']['drift']}"],
        [f"workspace_component={workspace['component_id']}", f"workspace_digest={workspace['digest']}"],
        [f"component_count={artifact['product_packet']['component_count']}", f"unsupported_claim_count={artifact['product_packet']['unsupported_claim_count']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"ablation_count={len(artifact['ablation_results'])}"],
        [f"focus_exit_code={artifact['live_surface']['focus_path_probe']['exit_code']}", f"focus_status={artifact['live_surface']['focus_path_probe']['status']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0071 Live Workspace Context Replacement", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0071 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    artifact = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "LIVE_WORKSPACE_CONTEXT_REPLACEMENT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
