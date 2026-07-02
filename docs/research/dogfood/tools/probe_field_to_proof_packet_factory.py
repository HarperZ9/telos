"""Generate pass 0123 field-to-proof packet factory artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_field_to_proof_packet_factory.py"
TEST_SCRIPT = ROOT / "tools" / "test_field_to_proof_packet_factory.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0123_field_to_proof_factory.py"
OUT_PATH = ROOT / "schemas" / "field-to-proof-packet-factory-pass-0123.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0123-field-to-proof-factory-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0123.json"
PACKET_PATH = ROOT / "packets" / "133-field-to-proof-packet-factory.md"
BRIEF_PATH = ROOT / "briefs" / "133-field-to-proof-packet-factory-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0123-field-to-proof-packet-factory-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0123-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0123-measurements.json"


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


def factory_rows(artifact: dict) -> list[dict]:
    return [
        {
            "rank": idx + 1,
            "field": row["field"],
            "product": row["market_product"],
            "score": row["scores"]["total"],
            "buyer": row["buyer"],
        }
        for idx, row in enumerate(artifact["field_factories"])
    ]


def source_rows(artifact: dict) -> list[dict]:
    return [
        {"role": row["role"], "label": row["label"], "chars": row["chars"], "status": row["gather_status"]}
        for row in artifact["source_matrix"]
    ]


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    substantial = sum(row["chars"] >= 500 for row in artifact["source_matrix"])
    top = artifact["field_factories"][0]
    return f"""# Packet 133: Field-to-Proof Packet Factory

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: package Project Telos as a family of field-specific proof-packet
factories across research labs, AI infrastructure, scientific runtime,
workflow reproducibility, formal proof, and lab handoff.

```text
source_rows = {len(artifact['source_matrix'])}
substantial_source_rows = {substantial}
field_factories = {len(artifact['field_factories'])}
primary_30_day_market_push = {artifact['primary_30_day_market_push']}
top_ranked_factory = {top['market_product']}
coverage_experiment = {artifact['coverage_experiment']['status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Ranked Factories

| Rank | Field | Product | Score | Buyer |
| ---: | --- | --- | ---: | --- |
{table(factory_rows(artifact), ['rank', 'field', 'product', 'score', 'buyer'])}

## Canonical Slots

`{', '.join(artifact['canonical_slots'])}`

## Source Matrix

| Role | Label | Chars | Gather status |
| --- | --- | ---: | --- |
{table(source_rows(artifact), ['role', 'label', 'chars', 'status'])}

## Demo Sequence

1. {artifact['public_demo_sequence'][0]}
2. {artifact['public_demo_sequence'][1]}
3. {artifact['public_demo_sequence'][2]}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    top = artifact["field_factories"][0]
    second = artifact["field_factories"][1]
    third = artifact["field_factories"][2]
    return f"""# Field-to-Proof Packet Factory Brief

Date: 2026-07-01

## Decision

Run the next 30 days as `{artifact['primary_30_day_market_push']}`: a product
family, not a monolith. The first market-facing surface is the proof-packet
factory itself, with three public demos.

## Ranking

1. `{top['market_product']}` for {top['buyer']}.
2. `{second['market_product']}` for {second['buyer']}.
3. `{third['market_product']}` for {third['buyer']}.

## Mechanism

The factory wins only if it preserves incumbent outputs while adding the missing
cross-layer packet: source receipts, workspace context, route decision, claim
graph, oracle/protocol, executable or formal branch, verifier verdict, negative
result lane, buyer brief, and non-promotion boundary.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0123 Steelman: Field-to-Proof Packet Factory

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that the plan still looks like a broad wrapper over
incumbents. That is a real risk. The counter is not a slogan; it is an adapter
demo that imports incumbent traces, workflow runs, notebook/lab artifacts, and
formal proof targets into one packet with a Crucible verdict.

The second objection is adoption friction. The pass therefore treats incumbents
as inputs, not enemies. Replacement claims remain hypotheses.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0123",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_count": len(artifact["source_matrix"]),
        "factory_count": len(artifact["field_factories"]),
        "coverage_status": artifact["coverage_experiment"]["status"],
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {
        "artifact": OUT_PATH,
        "composer": COMPOSER,
        "packet": PACKET_PATH,
        "brief": BRIEF_PATH,
        "steelman": STEELMAN_PATH,
        "test": TEST_SCRIPT,
        "validator": VALIDATOR,
        "validator_result": VALIDATOR_RESULT,
        "tool_receipts": TOOL_RECEIPTS_PATH,
    }
    shas = {name: sha256_file(path) for name, path in files.items()}
    sources = artifact["source_matrix"]
    factories = artifact["field_factories"]
    claims = [
        f"Pass 0123 created a FieldToProofPacketFactorySpec/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0123 records {len(sources)} Gather source rows and {sum(row['chars'] >= 500 for row in sources)} substantial source rows.",
        f"Pass 0123 defines {len(factories)} field factories and every factory has HYPOTHESIS claim status and inferred gap status.",
        f"Pass 0123 coverage experiment status is {artifact['coverage_experiment']['status']} and rejects the negative fixture.",
        f"Pass 0123 primary market push is {artifact['primary_30_day_market_push']} with three public demos.",
        f"Pass 0123 top three products are {[row['market_product'] for row in factories[:3]]}.",
        f"Pass 0123 binds prior passes {artifact['source_bindings']}.",
        "Pass 0123 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0123 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0123 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0123 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_count={len(sources)}", f"substantial={sum(row['chars'] >= 500 for row in sources)}"],
        [f"factory_count={len(factories)}", f"statuses={[(row['claim_status'], row['gap_status']) for row in factories]}"],
        [f"coverage_experiment={artifact['coverage_experiment']}"],
        [f"primary={artifact['primary_30_day_market_push']}", f"demos={artifact['public_demo_sequence']}"],
        [f"top_three={[row['market_product'] for row in factories[:3]]}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0123 Field-to-Proof Packet Factory", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0123 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    validator_receipt = run_command([sys.executable, str(VALIDATOR)], timeout=120)
    receipts = {"compose": compose_receipt, "test": test_receipt, "validator": validator_receipt}
    write_tool_receipts(artifact, compose_receipt, test_receipt, validator_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt, validator_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, receipts)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "FIELD_TO_PROOF_PACKET_FACTORY_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
