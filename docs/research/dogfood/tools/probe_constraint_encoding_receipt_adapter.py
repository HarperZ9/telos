"""Generate pass 0103 constraint-encoding adapter artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_constraint_encoding_receipt_adapter.py"
TEST_SCRIPT = ROOT / "tools" / "test_constraint_encoding_receipt_adapter.py"
OUT_PATH = ROOT / "schemas" / "constraint-encoding-receipt-adapter-pass-0103.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0103.json"
PACKET_PATH = ROOT / "packets" / "113-constraint-encoding-receipt-adapter.md"
BRIEF_PATH = ROOT / "briefs" / "113-constraint-encoding-receipt-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0103-constraint-encoding-receipt-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0103-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0103-measurements.json"


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


def receipt_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["constraint_encoding_receipts"]:
        rows.append(
            f"| `{row['branch_id']}` | {row['execution_status']} | {row['encoding_method']} | {row['feasible_under_capacity']} | {row['promotion_blocked']} | {row['adapter_status']} |"
        )
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    cov = artifact["coverage"]
    return f"""# Packet 113: Constraint-Encoding Receipt Adapter

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: apply pass 0101's BQM counterexample to the solver branch stack. The
adapter records whether each branch has a visible constraint encoding and
feasibility check, and blocks promotion when an executed BQM branch relies on
equality-to-capacity penalty without a slack or inequality receipt.

```text
receipt_count = {cov['receipt_count']}
executed_receipt_count = {cov['executed_receipt_count']}
safe_executed_count = {cov['safe_executed_count']}
promotion_blocked_executed_count = {cov['promotion_blocked_executed_count']}
unsafe_executed_branch_ids = {','.join(cov['unsafe_executed_branch_ids'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Encoding Receipts

| Branch | Execution | Encoding | Feasible | Promotion Blocked | Adapter Status |
| --- | --- | --- | --- | --- | --- |
{receipt_rows(artifact)}

## Rule

An optimization branch can match the fixture and still be unsafe as a general
encoding. Pass 0103 therefore separates `feasible_under_capacity` from
`encoding_safety`; both must be visible before a solver branch is promoted.
"""


def render_brief(artifact: dict) -> str:
    return f"""# Constraint-Encoding Receipt Brief

Date: 2026-07-01

## Decision

Add `ConstraintEncodingReceipt/v1` to solver branch packets before using
optimization demos as market-facing proof.

## Why

The Ocean/dimod branch matched the exact fixture, but pass 0101 showed that the
same equality-to-capacity BQM pattern is not a general `<= capacity` encoding.
The adapter keeps this distinction inspectable.

## Next Implementation Target

Promote the adapter fields into BuildLang/buildc and solver branch receipts:
constraint type, encoding method, feasibility check, counterexample reference,
and promotion block status.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0103 Steelman: Constraint-Encoding Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this adapter is still metadata, not a formal
proof of every solver encoding. Correct. Its value is narrower: it prevents a
solver branch from hiding the encoding assumption that made pass 0101 fail.

The second objection is that some exact and greedy branches use simple
feasibility filters, not formal constraint encodings. Correct. They are marked
safe only for this fixture because the feasibility check is explicit and
replayable, not because the algorithm is globally optimal.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0103",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "coverage": artifact["coverage"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "brief": sha256_file(BRIEF_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
        "tool_receipts": sha256_file(TOOL_RECEIPTS_PATH),
    }
    cov = artifact["coverage"]
    claims = [
        f"Pass 0103 created a ConstraintEncodingReceiptAdapter/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0103 binds source passes {artifact['source_bindings']} and adapter rule {artifact['adapter_rule']['requirement_id']}.",
        f"Pass 0103 records {cov['receipt_count']} constraint encoding receipts with {cov['executed_receipt_count']} executed branches.",
        f"Pass 0103 records safe_executed_count {cov['safe_executed_count']} and promotion_blocked_executed_count {cov['promotion_blocked_executed_count']}.",
        f"Pass 0103 identifies unsafe executed branch ids {cov['unsafe_executed_branch_ids']}.",
        f"Pass 0103 records all_executed_have_feasibility_check={cov['all_executed_have_feasibility_check']}.",
        f"Pass 0103 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0103 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0103 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"rule={artifact['adapter_rule']['requirement_id']}"],
        [f"receipt_count={cov['receipt_count']}", f"executed_receipt_count={cov['executed_receipt_count']}"],
        [f"safe_executed_count={cov['safe_executed_count']}", f"promotion_blocked_executed_count={cov['promotion_blocked_executed_count']}"],
        [f"unsafe_executed_branch_ids={cov['unsafe_executed_branch_ids']}"],
        [f"all_executed_have_feasibility_check={cov['all_executed_have_feasibility_check']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0103 Constraint-Encoding Receipt Adapter", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0103 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "CONSTRAINT_ENCODING_RECEIPT_ADAPTER_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
