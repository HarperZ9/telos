"""Generate pass 0077 receipts for path-selector contract scorecard."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_path_selector_contract_scorecard.py"
TEST_SCRIPT = ROOT / "tools" / "test_path_selector_contract_scorecard.py"
OUT_PATH = ROOT / "schemas" / "path-selector-contract-scorecard-pass-0077.json"
PACKET_PATH = ROOT / "packets" / "087-path-selector-contract-scorecard.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0077-path-selector-contract-scorecard-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0077-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0077-measurements.json"


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
    motions = "\n".join(f"- `{row['id']}` score `{row['weighted_score']}`: {row['rationale']}" for row in artifact["product_motions"])
    vectors = "\n".join(f"- `{row['vector']}`: {row['next_experiment']}" for row in artifact["growth_vectors"])
    return f"""# Packet 087: Path-Selector Contract Scorecard

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: define the minimum `IndexPathSelectorReceipt/v1` contract and rank
three near-term product motions using local evidence from prior dogfood passes.

```text
contract = {artifact['contract']['schema']}
evidence_count = {len(artifact['evidence'])}
growth_vectors = {len(artifact['growth_vectors'])}
top_motion = {artifact['primary_30_day_push']['motion']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Ranked Motions

{motions}

## Growth Vectors

{vectors}

## Boundary

All uniqueness claims remain hypotheses. This packet does not implement path
selection, certify a market, validate a science result, calibrate hardware, or
promote a natural law.
"""


def render_steelman(artifact: dict) -> str:
    top = artifact["product_motions"][0]
    return f"""# Pass 0077 Steelman: Path-Selector Contract Scorecard

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The ranking favors `{top['id']}` because the current evidence is strongest
there, not because the total mission is narrower. The objection is that
BuildLang is only one pillar; the response is to use it as the fastest proof of
the shared substrate: selected source refs, compiler receipts, negative
fixtures, and claim packets. The same path-selector contract then improves
color/rendering and AI4Science packets.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    top = artifact["product_motions"][0]
    claims = [
        f"Pass 0077 created a PathSelectorContractGrowthScorecard/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0077 defines contract schema {artifact['contract']['schema']} with {len(artifact['contract']['required_fields'])} required fields.",
        f"Pass 0077 binds {len(artifact['evidence'])} prior evidence artifacts.",
        f"Pass 0077 defines {len(artifact['growth_vectors'])} growth vectors.",
        f"Pass 0077 ranks {len(artifact['product_motions'])} product motions and top motion {top['id']} with score {top['weighted_score']}.",
        f"Pass 0077 primary 30-day push is {artifact['primary_30_day_push']['motion']}.",
        f"Pass 0077 keeps unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0077 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"contract_schema={artifact['contract']['schema']}", f"required_fields={len(artifact['contract']['required_fields'])}"],
        [f"evidence_count={len(artifact['evidence'])}"],
        [f"growth_vectors={len(artifact['growth_vectors'])}"],
        [f"motion_count={len(artifact['product_motions'])}", f"top_motion={top['id']}", f"top_score={top['weighted_score']}"],
        [f"primary_30_day_push={artifact['primary_30_day_push']['motion']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0077 Path Selector Contract Scorecard", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0077 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    artifact = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "PATH_SELECTOR_CONTRACT_SCORECARD_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
