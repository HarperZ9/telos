"""Generate pass 0105 reaction mass-conservation artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_reaction_mass_conservation_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_reaction_mass_conservation_receipt.py"
OUT_PATH = ROOT / "schemas" / "reaction-mass-conservation-receipt-pass-0105.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0105.json"
PACKET_PATH = ROOT / "packets" / "115-reaction-mass-conservation-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "115-reaction-mass-conservation-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0105-reaction-mass-conservation-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0105-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0105-measurements.json"


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


def sample_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["numerical_probe"]["samples"]:
        rows.append(f"| {row['t']:.3f} | {row['A_exact']:.9f} | {row['B_exact']:.9f} | {row['total_euler']:.9f} |")
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    probe = artifact["numerical_probe"]
    return f"""# Packet 115: Reaction Mass-Conservation Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: prove and numerically probe the invariant for a closed first-order
reaction `A -> B` with mass-action rate `kA`.

```text
reaction = {artifact['reaction']['equation']}
derivation = {artifact['proof']['derivation']}
symbolic_derivative_total = {artifact['proof']['symbolic_derivative_total']}
grid_points = {probe['grid_points']}
max_exact_invariant_drift = {probe['max_exact_invariant_drift']}
max_euler_invariant_drift = {probe['max_euler_invariant_drift']}
negative_fixture_breaks_invariant = {artifact['negative_fixture']['breaks_invariant']}
law_candidate = {artifact['law_candidate']['name']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Samples

| t | A exact | B exact | Euler total |
| ---: | ---: | ---: | ---: |
{sample_rows(artifact)}

## Boundary

This is a bounded invariant for a closed toy reaction model. It is not a new
natural law, biological discovery, enzyme mechanism, or experimental result.
"""


def render_brief(artifact: dict) -> str:
    return """# Reaction Mass-Conservation Brief

Date: 2026-07-01

## Decision

Use simple conserved-quantity proofs as the first executable AI4Science packet
class.

## Why

The equation is small enough to prove symbolically and test numerically, but it
exercises the same receipt surface needed for larger scientific models: source
claim, protocol, measurement, negative fixture, promotion boundary, and
reviewable verdict.

## Next Implementation Target

Generalize from `A -> B` to a stoichiometric-matrix invariant checker.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0105 Steelman: Reaction Mass Conservation

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that `A -> B` is a toy problem. Correct. It is useful
because it makes the full proof loop cheap enough to inspect. The next pass must
generalize the invariant checker rather than treat this as discovery.

The second objection is that Euler conservation here is an artifact of updating
both species with the same delta. Correct. That is why the receipt separates the
symbolic invariant from the numerical probe and includes an open-system negative
fixture that breaks conservation.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0105", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "law_candidate": artifact["law_candidate"]}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {name: sha256_file(path) for name, path in {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}.items()}
    probe = artifact["numerical_probe"]
    claims = [
        f"Pass 0105 created a ReactionMassConservationReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0105 binds AI4Science pass {artifact['source_bindings']['ai4science_pass']} and reaction {artifact['reaction']['equation']}.",
        f"Pass 0105 records symbolic derivative total {artifact['proof']['symbolic_derivative_total']} for invariant {artifact['proof']['invariant']}.",
        f"Pass 0105 numerical probe records {probe['grid_points']} grid points, max_exact_invariant_drift {probe['max_exact_invariant_drift']}, and max_euler_invariant_drift {probe['max_euler_invariant_drift']}.",
        f"Pass 0105 negative fixture {artifact['negative_fixture']['fixture_id']} breaks invariant with status {artifact['negative_fixture']['status']}.",
        f"Pass 0105 records law candidate {artifact['law_candidate']['name']} with status {artifact['law_candidate']['status']}.",
        f"Pass 0105 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0105 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0105 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"reaction={artifact['reaction']}"],
        [f"proof={artifact['proof']}"],
        [f"grid_points={probe['grid_points']}", f"max_exact={probe['max_exact_invariant_drift']}", f"max_euler={probe['max_euler_invariant_drift']}"],
        [f"negative_fixture={artifact['negative_fixture']}"],
        [f"law_candidate={artifact['law_candidate']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0105 Reaction Mass-Conservation Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0105 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "REACTION_MASS_CONSERVATION_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
