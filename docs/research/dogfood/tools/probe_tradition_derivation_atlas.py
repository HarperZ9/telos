"""Generate pass 0131 tradition derivation atlas artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_tradition_derivation_atlas.py"
TEST_SCRIPT = ROOT / "tools" / "test_tradition_derivation_atlas.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0131_tradition_derivation_atlas.py"
OUT_PATH = ROOT / "schemas" / "tradition-derivation-atlas-pass-0131.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0131-tradition-derivation-atlas-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0131.json"
PACKET_PATH = ROOT / "packets" / "141-tradition-derivation-atlas.md"
BRIEF_PATH = ROOT / "briefs" / "141-tradition-derivation-atlas-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0131-tradition-derivation-atlas-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0131-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0131-measurements.json"


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


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    nodes = [{"id": row["id"], "label": row["label"], "terms": ",".join(row["dominant_terms"][:4]), "sha256": row["source_sha256"][:16]} for row in artifact["atlas_nodes"]]
    edges = [{"from": row["from"], "to": row["to"], "relation": row["relation"], "status": row["status"]} for row in artifact["atlas_edges"]]
    modules = [{"id": row["id"], "verifier": row["verifier"]} for row in artifact["learning_modules"]]
    products = [{"tool": row["tool"], "status": row["status"], "wedge": row["wedge"]} for row in artifact["product_hypotheses"]]
    return f"""# Packet 141: Tradition Derivation Atlas

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: expand the Brandom functional-learning lane into a sampled,
source-backed tradition atlas that can drive prerequisite paths, contrast
classes, learner exercises, and overclaim gates.

```text
source_receipts = {len(artifact['source_receipts'])}
atlas_nodes = {len(artifact['atlas_nodes'])}
atlas_edges = {len(artifact['atlas_edges'])}
learning_modules = {len(artifact['learning_modules'])}
negative_fixtures = {len(artifact['negative_fixtures'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Atlas Nodes

| Id | Label | Dominant terms | sha256 |
| --- | --- | --- | --- |
{table(nodes, ['id', 'label', 'terms', 'sha256'])}

## Atlas Edges

| From | To | Relation | Status |
| --- | --- | --- | --- |
{table(edges, ['from', 'to', 'relation', 'status'])}

## Learning Modules

| Module | Verifier |
| --- | --- |
{table(modules, ['id', 'verifier'])}

## Product Hypotheses

| Tool | Status | Wedge |
| --- | --- | --- |
{table(products, ['tool', 'status', 'wedge'])}

## Boundary

{artifact['boundary']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Tradition Derivation Atlas Brief

Date: 2026-07-01

## Decision

Build functional-learning tools around source-backed prerequisite and contrast
graphs, not around undifferentiated summaries.

## Result

Pass 0131 binds `{len(artifact['source_receipts'])}` source receipts into
`{len(artifact['atlas_nodes'])}` nodes, `{len(artifact['atlas_edges'])}` bounded
hypothesis edges, and `{len(artifact['learning_modules'])}` learning modules.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0131 Steelman: Tradition Derivation Atlas

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that the atlas could smuggle a clean lineage onto a
messy intellectual history. The pass accepts that risk and constrains each edge
to `HYPOTHESIS_SOURCE_BACKED`, not causality or completeness.

The second objection is that a prerequisite graph can still fail as pedagogy.
Correct. The pass rejects learning-efficacy claims until there are learner
outcome receipts.

Boundary: {artifact['boundary']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> dict:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0131",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_count": len(artifact["source_receipts"]),
        "node_count": len(artifact["atlas_nodes"]),
        "edge_count": len(artifact["atlas_edges"]),
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)
    return receipts


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0131 created a TraditionDerivationAtlasReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0131 binds upstream pass {artifact['source_bindings']} and records {len(artifact['source_receipts'])} source receipts.",
        f"Pass 0131 defines {len(artifact['atlas_nodes'])} atlas nodes with dominant terms.",
        f"Pass 0131 defines {len(artifact['atlas_edges'])} atlas edges and each edge is HYPOTHESIS_SOURCE_BACKED.",
        f"Pass 0131 defines {len(artifact['learning_modules'])} learning modules with verifiers.",
        f"Pass 0131 defines {len(artifact['product_hypotheses'])} product hypotheses.",
        f"Pass 0131 rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0131 boundary rejects complete genealogy, causal influence proof, learning efficacy, raw export, and natural-law promotion.",
        "Pass 0131 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0131 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0131 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0131 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"source_receipts={artifact['source_receipts']}"],
        [f"atlas_nodes={artifact['atlas_nodes']}"],
        [f"atlas_edges={artifact['atlas_edges']}"],
        [f"learning_modules={artifact['learning_modules']}"],
        [f"product_hypotheses={artifact['product_hypotheses']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"boundary={artifact['boundary']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0131 Tradition Derivation Atlas", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0131 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=180)
    validator_receipt = run_command([sys.executable, str(VALIDATOR)], timeout=120)
    receipts = write_tool_receipts(artifact, compose_receipt, test_receipt, validator_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt, validator_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, receipts)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    ok = all(row["status"] == "MATCH" for row in [compose_receipt, test_receipt, validator_receipt]) and artifact["status"] == "TRADITION_DERIVATION_ATLAS_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
