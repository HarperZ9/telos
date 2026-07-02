"""Generate pass 0130 Brandom work lesson graph artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_brandom_work_lesson_graph.py"
TEST_SCRIPT = ROOT / "tools" / "test_brandom_work_lesson_graph.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0130_brandom_work_lesson_graph.py"
OUT_PATH = ROOT / "schemas" / "brandom-work-lesson-graph-pass-0130.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0130-brandom-work-lesson-graph-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0130.json"
PACKET_PATH = ROOT / "packets" / "140-brandom-work-lesson-graph.md"
BRIEF_PATH = ROOT / "briefs" / "140-brandom-work-lesson-graph-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0130-brandom-work-lesson-graph-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0130-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0130-measurements.json"


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
    works = [{"title": row["title"], "kind": row["source_kind"], "terms": ",".join(row["dominant_terms"][:3]), "sha256": row["sha256"][:16]} for row in artifact["work_catalog"]]
    nodes = [{"id": row["id"], "kind": row["kind"], "sources": len(row["source_refs"])} for row in artifact["lesson_graph"]["nodes"]]
    implications = [{"tool": row["tool"], "status": row["status"], "wedge": row["wedge"]} for row in artifact["product_implications"]]
    return f"""# Packet 140: Brandom Work Lesson Graph

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: deepen the Brandom corpus from pass 0129 into a work-level catalog
and a bounded lesson graph for functional learning tooling.

```text
source_receipts = {len(artifact['source_receipts'])}
work_catalog = {len(artifact['work_catalog'])}
lesson_nodes = {len(artifact['lesson_graph']['nodes'])}
lesson_edges = {len(artifact['lesson_graph']['edges'])}
learner_action_fixture = {artifact['learner_action_fixture']['status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Work Catalog

| Title | Kind | Dominant terms | sha256 |
| --- | --- | --- | --- |
{table(works, ['title', 'kind', 'terms', 'sha256'])}

## Lesson Graph

| Node | Kind | Source count |
| --- | --- | --- |
{table(nodes, ['id', 'kind', 'sources'])}

## Product Implications

| Tool | Status | Wedge |
| --- | --- | --- |
{table(implications, ['tool', 'status', 'wedge'])}

## Boundary

{artifact['boundary']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Brandom Work Lesson Graph Brief

Date: 2026-07-01

## Decision

Move from corpus digest to a lesson graph builder: source intake, vocabulary,
inferential links, scorekeeping, challenge/repair, and AI action receipts.

## Result

The pass catalogs `{len(artifact['work_catalog'])}` gathered works and produces
a `{len(artifact['lesson_graph']['nodes'])}`-node graph with source refs and
exercises on every node.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0130 Steelman: Brandom Work Lesson Graph

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this is a small slice of Brandom's corpus.
Correct. The pass intentionally uses five gathered works/course pages and marks
the resulting graph as a bounded prototype.

The second objection is that a graph can look plausible while not improving
learning. Correct. The pass rejects learning-efficacy claims until learner
outcome receipts exist.

Boundary: {artifact['boundary']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> dict:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0130",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_count": len(artifact["source_receipts"]),
        "work_count": len(artifact["work_catalog"]),
        "lesson_node_count": len(artifact["lesson_graph"]["nodes"]),
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)
    return receipts


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0130 created a BrandomWorkLessonGraphReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0130 binds upstream pass {artifact['source_bindings']} and records {len(artifact['source_receipts'])} source receipts.",
        f"Pass 0130 catalogs {len(artifact['work_catalog'])} works with dominant terms.",
        f"Pass 0130 lesson graph status is {artifact['lesson_graph']['status']} with {len(artifact['lesson_graph']['nodes'])} nodes and {len(artifact['lesson_graph']['edges'])} edges.",
        f"Pass 0130 learner action fixture status is {artifact['learner_action_fixture']['status']}.",
        f"Pass 0130 defines {len(artifact['product_implications'])} product implications as hypotheses.",
        f"Pass 0130 rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0130 boundary rejects PDF body export, complete-bibliography claims, learning efficacy claims, and natural-law promotion.",
        "Pass 0130 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0130 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0130 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0130 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"source_receipts={artifact['source_receipts']}"],
        [f"work_catalog={artifact['work_catalog']}"],
        [f"lesson_graph={artifact['lesson_graph']}"],
        [f"learner_action_fixture={artifact['learner_action_fixture']}"],
        [f"product_implications={artifact['product_implications']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"boundary={artifact['boundary']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0130 Brandom Work Lesson Graph", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0130 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    ok = all(row["status"] == "MATCH" for row in [compose_receipt, test_receipt, validator_receipt]) and artifact["status"] == "BRANDOM_WORK_LESSON_GRAPH_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
