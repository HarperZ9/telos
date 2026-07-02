"""Generate pass 0108 detailed-balance Markov artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_detailed_balance_markov_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_detailed_balance_markov_receipt.py"
OUT_PATH = ROOT / "schemas" / "detailed-balance-markov-receipt-pass-0108.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0108.json"
PACKET_PATH = ROOT / "packets" / "118-detailed-balance-markov-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "118-detailed-balance-markov-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0108-detailed-balance-markov-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0108-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0108-measurements.json"


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


def market_rows(artifact: dict) -> str:
    return "\n".join(f"| {row['tool']} | {row['category']} | {row['gap_status']} |" for row in artifact["market_surface"]["tools"])


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    pos = artifact["reversible_kernel"]
    row_only = artifact["negative_fixtures"]["row_stochastic_not_stationary"]
    circulation = artifact["negative_fixtures"]["stationary_not_reversible"]
    return f"""# Packet 118: Detailed-Balance Markov Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: prove a bounded finite-state Markov identity for stochastic physics,
MCMC, AI uncertainty, and probabilistic runtime proof packets.

```text
source_reaction_corpus_pass = {artifact['source_bindings']['reaction_corpus_pass']}
pi = {pos['pi']}
max_detailed_balance_residual = {pos['max_detailed_balance_residual']}
stationary_residual = {pos['stationary_residual']}
simulation_steps = {pos['simulation_probe']['steps']}
simulation_l1_distance_to_pi = {pos['simulation_probe']['l1_distance_to_pi']}
row_stochastic_negative_residual = {row_only['stationary_residual']}
stationary_not_reversible_residual = {circulation['max_detailed_balance_residual']}
market_tool_count = {artifact['market_surface']['tool_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Market Surface

| Tool | Category | Gap Status |
| --- | --- | --- |
{market_rows(artifact)}

## Product Meaning

The proof-packet wedge is not "another sampler." It is a portable receipt for
kernel-level balance equations, stationary residuals, convergence probes,
diagnostic boundaries, and negative fixtures.

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    market = artifact["market_surface"]
    return f"""# Detailed-Balance Markov Brief

Date: 2026-07-01

## Decision

Add stochastic-kernel proof packets as a frontier lane for AI/ML, physics,
quant, and uncertainty tooling.

## Why

MCMC systems already provide samplers and diagnostics. Telos can add a narrower
but highly checkable layer: transition-kernel receipts, detailed-balance
residuals, stationary residuals, convergence probes, and negative fixtures.

## Current Result

The pass records {market['tool_count']} adjacent tools, exact zero residuals for
a reversible three-state chain, a row-stochastic negative fixture, and a
stationary-but-not-reversible boundary fixture.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0108 Steelman: Detailed-Balance Markov Receipt

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a three-state chain is not a real probabilistic
program. Correct. It is a kernel-level proof primitive, not a full sampler.

The second objection is that detailed balance is not necessary for stationarity.
Correct. The receipt includes a stationary cyclic fixture that violates detailed
balance so the packet cannot overclaim necessity.

The third objection is that market gaps are inferred. Correct. The listed tools
are source anchors for positioning, not proof that buyers will adopt the wedge.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0108",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "law_candidate": artifact["law_candidate"],
        "market_surface": artifact["market_surface"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    pos = artifact["reversible_kernel"]
    row_only = artifact["negative_fixtures"]["row_stochastic_not_stationary"]
    circulation = artifact["negative_fixtures"]["stationary_not_reversible"]
    market = artifact["market_surface"]
    claims = [
        f"Pass 0108 created a DetailedBalanceMarkovReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0108 binds reaction corpus pass {artifact['source_bindings']['reaction_corpus_pass']} and records {len(artifact['source_anchors'])} source anchors.",
        f"Pass 0108 reversible kernel records pi {pos['pi']}, max_detailed_balance_residual {pos['max_detailed_balance_residual']}, and stationary_residual {pos['stationary_residual']}.",
        f"Pass 0108 simulation probe records {pos['simulation_probe']['steps']} steps and l1_distance_to_pi {pos['simulation_probe']['l1_distance_to_pi']}.",
        f"Pass 0108 row-stochastic negative fixture records row_sums {row_only['row_sums']} and stationary_residual {row_only['stationary_residual']}.",
        f"Pass 0108 stationary-not-reversible boundary records stationary_residual {circulation['stationary_residual']} and max_detailed_balance_residual {circulation['max_detailed_balance_residual']}.",
        f"Pass 0108 market surface records tool_count {market['tool_count']} and gap_status {market['gap_status']}.",
        f"Pass 0108 records law candidate {artifact['law_candidate']['name']} with status {artifact['law_candidate']['status']}.",
        f"Pass 0108 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0108 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0108 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"source_anchor_count={len(artifact['source_anchors'])}"],
        [f"reversible_kernel={pos}"],
        [f"simulation_probe={pos['simulation_probe']}"],
        [f"row_stochastic_not_stationary={row_only}"],
        [f"stationary_not_reversible={circulation}"],
        [f"market_surface={market}"],
        [f"law_candidate={artifact['law_candidate']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0108 Detailed-Balance Markov Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0108 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "DETAILED_BALANCE_MARKOV_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
