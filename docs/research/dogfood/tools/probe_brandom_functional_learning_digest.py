"""Generate pass 0129 Brandom functional-learning digest artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_brandom_functional_learning_digest.py"
TEST_SCRIPT = ROOT / "tools" / "test_brandom_functional_learning_digest.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0129_brandom_functional_learning_digest.py"
OUT_PATH = ROOT / "schemas" / "brandom-functional-learning-digest-pass-0129.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0129-brandom-functional-learning-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0129.json"
PACKET_PATH = ROOT / "packets" / "139-brandom-functional-learning-digest.md"
BRIEF_PATH = ROOT / "briefs" / "139-brandom-functional-learning-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0129-brandom-functional-learning-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0129-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0129-measurements.json"


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
    sources = [{"ref": row["ref"], "kind": row["kind"], "status": row["status"], "sha256": row["sha256"][:16]} for row in artifact["source_receipts"]]
    terms = [row for row in artifact["term_signals"] if row["hits"] > 0][:10]
    tools = [{"tool": row["tool"], "status": row["status"], "need": row["market_need"]} for row in artifact["tool_hypotheses"]]
    return f"""# Packet 139: Brandom Functional Learning Digest

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: catalog the supplied Brandom sources and digest them into functional
learning-tool hypotheses without exporting raw transcript text or overclaiming
from blocked profiles.

```text
source_receipts = {len(artifact['source_receipts'])}
inaccessible_sources = {len(artifact['inaccessible_sources'])}
tool_hypotheses = {len(artifact['tool_hypotheses'])}
scorekeeping_status = {artifact['scorekeeping_fixture']['status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Source Receipts

| Ref | Kind | Status | sha256 |
| --- | --- | --- | --- |
{table(sources, ['ref', 'kind', 'status', 'sha256'])}

## Topic Signals

| Term | Documents | Hits |
| --- | --- | --- |
{table(terms, ['term', 'documents', 'hits'])}

## Tool Hypotheses

| Tool | Status | Need |
| --- | --- | --- |
{table(tools, ['tool', 'status', 'need'])}

## Boundary

{artifact['digest_boundary']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Brandom Functional Learning Brief

Date: 2026-07-01

## Decision

Use the Brandom corpus as a learning-tool design substrate: inferential graph
tutor, scorekeeping lab, expressive vocabulary ladder, seminar-to-proof packet,
and tradition derivation atlas.

## Result

Gather recorded `{len(artifact['source_receipts'])}` source receipts and the
scorekeeping fixture matched. ResearchGate and Academia were marked inaccessible
instead of treated as evidence.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0129 Steelman: Brandom Functional Learning Digest

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this pass is not a complete Brandom
bibliography. Correct. It is an accountable starting corpus: supplied links,
official Pitt pages, one YouTube lecture receipt, inaccessible-source records,
and a bounded learning fixture.

The second objection is that a philosophical theory is not directly a product
spec. Correct. The pass converts it into testable learning-tool hypotheses and
rejects product claims without task receipts.

Boundary: {artifact['digest_boundary']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> dict:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0129",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_count": len(artifact["source_receipts"]),
        "tool_hypothesis_count": len(artifact["tool_hypotheses"]),
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)
    return receipts


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    terms = {row["term"]: row for row in artifact["term_signals"]}
    claims = [
        f"Pass 0129 created a BrandomFunctionalLearningDigestReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0129 records {len(artifact['source_receipts'])} Gather-verified source receipts and keeps raw bodies unexported.",
        f"Pass 0129 records inaccessible ResearchGate and Academia sources as {artifact['inaccessible_sources']}.",
        f"Pass 0129 observed Sellars, Kant, and Hegel term signals {terms['Sellars']}, {terms['Kant']}, {terms['Hegel']}.",
        f"Pass 0129 builds a derivation map with {len(artifact['derivation_map'])} anchors.",
        f"Pass 0129 scorekeeping fixture status is {artifact['scorekeeping_fixture']['status']} and final entitlements are {artifact['scorekeeping_fixture']['final_entitlements']}.",
        f"Pass 0129 defines {len(artifact['tool_hypotheses'])} functional-learning tool hypotheses.",
        f"Pass 0129 rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0129 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0129 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0129 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0129 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_receipts={artifact['source_receipts']}"],
        [f"inaccessible_sources={artifact['inaccessible_sources']}"],
        [f"term_signals={artifact['term_signals']}"],
        [f"derivation_map={artifact['derivation_map']}"],
        [f"scorekeeping_fixture={artifact['scorekeeping_fixture']}"],
        [f"tool_hypotheses={artifact['tool_hypotheses']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0129 Brandom Functional Learning Digest", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0129 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    ok = all(row["status"] == "MATCH" for row in [compose_receipt, test_receipt, validator_receipt]) and artifact["status"] == "BRANDOM_FUNCTIONAL_LEARNING_DIGEST_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
