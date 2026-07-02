"""Generate pass 0080 receipts for BuildLang proof-packet demo surface."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buildlang_proof_packet_demo_surface.py"
TEST_SCRIPT = ROOT / "tools" / "test_buildlang_proof_packet_demo_surface.py"
OUT_PATH = ROOT / "schemas" / "buildlang-proof-packet-demo-surface-pass-0080.json"
PACKET_PATH = ROOT / "packets" / "090-buildlang-proof-packet-demo-surface.md"
BRIEF_PATH = ROOT / "briefs" / "090-buildlang-proof-packet-demo-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0080-buildlang-proof-packet-demo-surface-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0080-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0080-measurements.json"


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
    return f"""# Packet 090: BuildLang Proof-Packet Demo Surface

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: package the BuildLang proof-packet demo surface by binding source
intake, path-scoped workspace context, live `buildc` corpus verification, Forum
route evidence, and negative fixtures.

```text
source_refs = {artifact['source_intake']['source_ref_count']}
workspace_refs = {artifact['workspace_context']['source_ref_count']}
live_buildc = {artifact['live_buildc_corpus']['status']}
forum_route = {artifact['forum_route']['status']}
path_scoped_context = {artifact['workspace_context']['path_scoped_context']}
adapter_fixture = {artifact['workspace_context']['adapter_fixture']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

Boundary: this is a proof-packet surface demo. It does not prove Julia
replacement, all backend maturity, native Index path selection, Build Universe
coverage, market adoption, scientific discovery, or a natural law.
"""


def render_brief(artifact: dict) -> str:
    route = artifact["forum_route"]
    return f"""# BuildLang Proof-Packet Demo Brief

Date: 2026-07-01

## Offer

BuildLang proof packets are portable evidence chains for compiler and
scientific-compute work. This demo binds source refs, selected workspace
context, a live `buildc` corpus receipt, routing evidence, negative fixtures,
and verifier verdicts into one product-facing surface.

## Why It Matters

Most language, compiler, and scientific-compute tools can show logs, tests, or
benchmarks. The differentiated wedge is a cross-layer proof packet that records
what was inspected, what was executed, what was rejected, and what can be
rechecked.

## Current Evidence

- Source intake: {artifact['source_intake']['source_ref_count']} refs from pass 0074.
- Workspace context: {artifact['workspace_context']['source_ref_count']} path-scoped refs from pass 0079.
- Live compiler receipt: `{artifact['live_buildc_corpus']['status']}` with {artifact['live_buildc_corpus']['match']} expected lines matched.
- Forum route: needs escalation `{route['needs_escalation']}` with top candidate `{route['top_candidates'][0]['agent']}`.

## Boundaries

This demo does not claim Julia replacement, all backend maturity, native Index
path selection, Build Universe coverage, or a scientific discovery.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0080 Steelman: BuildLang Proof-Packet Demo Surface

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest version of this demo is not that BuildLang is already a full
Julia replacement. The strongest version is narrower and more defensible:
BuildLang/buildc can carry proof-packet evidence across source refs, selected
workspace context, corpus receipts, routes, negative fixtures, and verifier
verdicts. The current weakness remains native Index path selection and broader
backend maturity.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "brief": sha256_file(BRIEF_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    claims = [
        f"Pass 0080 created a BuildLangProofPacketDemoSurface/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0080 binds source intake pass 0074 with source_ref_count {artifact['source_intake']['source_ref_count']}.",
        f"Pass 0080 binds workspace context pass 0079 with source_ref_count {artifact['workspace_context']['source_ref_count']} and path_scoped_context {artifact['workspace_context']['path_scoped_context']}.",
        f"Pass 0080 live buildc corpus status is {artifact['live_buildc_corpus']['status']} with match {artifact['live_buildc_corpus']['match']} and drift {artifact['live_buildc_corpus']['drift']}.",
        f"Pass 0080 forum route status is {artifact['forum_route']['status']} with needs_escalation {artifact['forum_route']['needs_escalation']}.",
        f"Pass 0080 buyer brief sha256 is {shas['brief']}.",
        f"Pass 0080 contains {len(artifact['negative_fixtures'])} negative fixtures, unsupported_claim_count {artifact['unsupported_claim_count']}, and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0080 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_pass={artifact['source_intake']['source_pass']}", f"source_ref_count={artifact['source_intake']['source_ref_count']}"],
        [f"workspace_pass={artifact['workspace_context']['source_pass']}", f"workspace_refs={artifact['workspace_context']['source_ref_count']}", f"path_scoped={artifact['workspace_context']['path_scoped_context']}"],
        [f"live_status={artifact['live_buildc_corpus']['status']}", f"match={artifact['live_buildc_corpus']['match']}", f"drift={artifact['live_buildc_corpus']['drift']}"],
        [f"route_status={artifact['forum_route']['status']}", f"needs_escalation={artifact['forum_route']['needs_escalation']}"],
        [f"brief_sha256={shas['brief']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0080 BuildLang Proof Packet Demo Surface", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0080 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    artifact = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "BUILDLANG_PROOF_PACKET_DEMO_SURFACE_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
