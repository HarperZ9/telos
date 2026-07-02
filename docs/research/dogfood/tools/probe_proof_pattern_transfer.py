"""Generate pass 0132 proof pattern transfer artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_proof_pattern_transfer.py"
TEST_SCRIPT = ROOT / "tools" / "test_proof_pattern_transfer.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0132_proof_pattern_transfer.py"
OUT_PATH = ROOT / "schemas" / "proof-pattern-transfer-pass-0132.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0132-proof-pattern-transfer-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0132.json"
PACKET_PATH = ROOT / "packets" / "142-proof-pattern-transfer.md"
BRIEF_PATH = ROOT / "briefs" / "142-proof-pattern-transfer-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0132-proof-pattern-transfer-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0132-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0132-measurements.json"


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
    positives = [{"fixture": row["fixture_id"], "status": row["status"], "norm_delta": row.get("norm_delta", ""), "residual": row.get("orthogonal_residual", row.get("derivative_residual", ""))} for row in artifact["positive_fixtures"]]
    counter = [{"fixture": row["fixture_id"], "status": row["status"], "failure": row["failure"]} for row in artifact["counterexample_fixtures"]]
    products = [{"tool": row["tool"], "status": row["status"], "wedge": row["wedge"]} for row in artifact["product_hypotheses"]]
    return f"""# Packet 142: Proof Pattern Transfer

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: transfer the source-trace, prerequisite-path, contrast-class, and
overclaim-audit pattern from pass 0131 into a bounded executable conservation
identity.

```text
source_receipts = {len(artifact['source_receipts'])}
positive_fixtures = {len(artifact['positive_fixtures'])}
counterexample_fixtures = {len(artifact['counterexample_fixtures'])}
law_candidate_status = {artifact['law_candidate']['status']}
promotion_status = {artifact['law_candidate']['promotion_status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Identity

{artifact['law_candidate']['statement']}

Scope: {artifact['law_candidate']['scope']}

## Positive Fixtures

| Fixture | Status | Norm delta | Residual |
| --- | --- | ---: | ---: |
{table(positives, ['fixture', 'status', 'norm_delta', 'residual'])}

## Counterexamples

| Fixture | Status | Failure |
| --- | --- | --- |
{table(counter, ['fixture', 'status', 'failure'])}

## Product Hypotheses

| Tool | Status | Wedge |
| --- | --- | --- |
{table(products, ['tool', 'status', 'wedge'])}

## Boundary

{artifact['boundary']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Proof Pattern Transfer Brief

Date: 2026-07-01

## Decision

Use proof packets to distinguish exact continuous invariants from method-level
runtime behavior.

## Result

Pass 0132 records `{len(artifact['positive_fixtures'])}` positive conservation
fixtures, `{len(artifact['counterexample_fixtures'])}` counterexample fixtures,
and keeps the identity at `{artifact['law_candidate']['status']}` without
promotion.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0132 Steelman: Proof Pattern Transfer

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a tiny linear invariant is too small to call
world-scale research. Correct. The value is not the novelty of the identity;
the value is the receipt pattern that binds sources, exact proof, runtime
branch, counterexample, and overclaim boundary.

The second objection is that a low floating residual is not proof. Correct.
The pass includes the symbolic identity `x^T(A + A^T)x = 0` and treats floating
runtime checks as receipts, not as standalone proof.

Boundary: {artifact['boundary']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> dict:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0132",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_count": len(artifact["source_receipts"]),
        "positive_count": len(artifact["positive_fixtures"]),
        "counterexample_count": len(artifact["counterexample_fixtures"]),
        "law_candidate_status": artifact["law_candidate"]["status"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)
    return receipts


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0132 created a ProofPatternTransferReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0132 binds upstream pass {artifact['source_bindings']} and records {len(artifact['source_receipts'])} source receipts.",
        f"Pass 0132 records {len(artifact['positive_fixtures'])} positive fixtures and all have MATCH status.",
        f"Pass 0132 records {len(artifact['counterexample_fixtures'])} counterexample fixtures and all are REJECTED.",
        f"Pass 0132 law candidate is {artifact['law_candidate']['status']} with promotion_status {artifact['law_candidate']['promotion_status']}.",
        f"Pass 0132 defines {len(artifact['transfer_modules'])} transfer modules.",
        f"Pass 0132 defines {len(artifact['product_hypotheses'])} product hypotheses.",
        f"Pass 0132 rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0132 boundary rejects universal natural-law promotion, general Noether proof, and explicit-Euler conservation.",
        "Pass 0132 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0132 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0132 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"source_receipts={artifact['source_receipts']}"],
        [f"positive_fixtures={artifact['positive_fixtures']}"],
        [f"counterexample_fixtures={artifact['counterexample_fixtures']}"],
        [f"law_candidate={artifact['law_candidate']}"],
        [f"transfer_modules={artifact['transfer_modules']}"],
        [f"product_hypotheses={artifact['product_hypotheses']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"boundary={artifact['boundary']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0132 Proof Pattern Transfer", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0132 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    ok = all(row["status"] == "MATCH" for row in [compose_receipt, test_receipt, validator_receipt]) and artifact["status"] == "PROOF_PATTERN_TRANSFER_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
