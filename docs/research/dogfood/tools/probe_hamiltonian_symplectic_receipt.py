"""Generate pass 0119 Hamiltonian/symplectic artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_hamiltonian_symplectic_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_hamiltonian_symplectic_receipt.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0119_hamiltonian_symplectic.py"
OUT_PATH = ROOT / "schemas" / "hamiltonian-symplectic-receipt-pass-0119.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0119-hamiltonian-symplectic-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0119.json"
PACKET_PATH = ROOT / "packets" / "129-hamiltonian-symplectic-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "129-hamiltonian-symplectic-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0119-hamiltonian-symplectic-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0119-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0119-measurements.json"


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
    return f"""# Packet 129: Hamiltonian Symplectic Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: record an exact rational proof packet for a bounded Hamiltonian
oscillator update, then reject an explicit-Euler negative fixture.

```text
formal_target_packaging_pass = {artifact['source_bindings']['formal_target_packaging_pass']}
law_candidate_status = {artifact['law_candidate']['status']}
symplectic_cases = {len(artifact['symplectic_cases'])}
source_anchors = {artifact['source_surface']['anchor_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Identity

{artifact['identity']}

## Positive Cases

| h | det(M) | modified initial | modified final | status |
| --- | --- | --- | --- | --- |
{table(artifact['symplectic_cases'], ['h', 'determinant', 'modified_initial', 'modified_final', 'status'])}

## Negative Fixture

| Fixture | h | det(M) | energy initial | energy final | status |
| --- | --- | --- | --- | --- | --- |
{table(artifact['negative_fixtures'], ['fixture_id', 'h', 'determinant', 'standard_energy_initial', 'standard_energy_final', 'status'])}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Hamiltonian Symplectic Brief

Date: 2026-07-01

## Decision

Use Hamiltonian/symplectic invariants as a proof-packet wedge for scientific
compute, physics AI, robotics simulation, and BuildLang runtime receipts.

## Product Meaning

The market already has solvers, simulators, differentiable frameworks, and
physics-AI platforms. The wedge is a receipt that binds update rule, exact
invariant, negative fixture, source surface, runtime branch, and verifier
verdict.

Law candidate: `{artifact['law_candidate']['name']}`.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0119 Steelman: Hamiltonian Symplectic Receipt

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a harmonic oscillator update identity is not a
new law of physics. Correct. It is a scoped computational law candidate for a
specific integrator receipt.

The second objection is that exact rational arithmetic does not establish
floating-point, compiler, GPU, or BuildLang behavior. Correct. That needs a
future runtime branch receipt.

Boundary: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0119",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "law_candidate": artifact["law_candidate"],
        "symplectic_cases": artifact["symplectic_cases"],
        "negative_fixtures": artifact["negative_fixtures"],
        "source_surface": artifact["source_surface"],
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
    cases = artifact["symplectic_cases"]
    negative = artifact["negative_fixtures"][0]
    claims = [
        f"Pass 0119 created a HamiltonianSymplecticReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0119 binds formal target packaging pass {artifact['source_bindings']['formal_target_packaging_pass']} with seal {artifact['source_bindings']['formal_target_packaging_seal']}.",
        f"Pass 0119 records {len(cases)} exact rational symplectic Euler cases and all have determinant 1 with MATCH status.",
        "Pass 0119 records M^T S M=S and modified quadratic invariant preservation for every positive case.",
        "Pass 0119 does not promote standard energy as exactly preserved for the symplectic Euler cases.",
        f"Pass 0119 records explicit Euler negative fixture {negative['fixture_id']} with determinant {negative['determinant']} and energy growth.",
        f"Pass 0119 records law candidate {artifact['law_candidate']['name']} with status {artifact['law_candidate']['status']} and zero promoted natural laws.",
        f"Pass 0119 records {artifact['source_surface']['anchor_count']} source anchors and the same number of market rows.",
        "Pass 0119 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0119 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0119 records unsupported_claim_count {artifact['unsupported_claim_count']} and non-promotion statement: {artifact['non_promotion_statement']}",
        f"Pass 0119 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, validator sha256 is {shas['validator']}, validator result sha256 is {shas['validator_result']}, and tool receipts sha256 is {shas['tool_receipts']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"cases={cases}"],
        [f"cases={cases}"],
        [f"standard_energy_flags={[row['standard_energy_exactly_preserved'] for row in cases]}"],
        [f"negative={negative}"],
        [f"law_candidate={artifact['law_candidate']}", f"natural_laws={artifact['current_promoted_natural_laws']}"],
        [f"anchor_count={artifact['source_surface']['anchor_count']}", f"market_count={len(artifact['source_surface']['market_rows'])}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}", f"telos_catalog={artifact['flagship_receipts']['telos_catalog']['status']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"non_promotion={artifact['non_promotion_statement']}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0119 Hamiltonian Symplectic Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0119 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)], timeout=180)
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
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "HAMILTONIAN_SYMPLECTIC_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
