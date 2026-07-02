"""Generate pass 0069 receipts for the Telos multi-receipt joiner."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_telos_multireceipt_joiner.py"
TEST_SCRIPT = ROOT / "tools" / "test_telos_multireceipt_joiner.py"
OUT_PATH = ROOT / "schemas" / "telos-multireceipt-joiner-pass-0069.json"
PACKET_PATH = ROOT / "packets" / "079-telos-multireceipt-joiner.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0069-telos-multireceipt-joiner-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0069-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0069-measurements.json"


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
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stderr_sha256": sha256_text(result.stderr),
        "stdout_sha256": sha256_text(result.stdout),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    components = "\n".join(f"- `{row['kind']}`: `{row['component_id']}`" for row in artifact["component_receipts"])
    negatives = "\n".join(f"- `{row['fixture_id']}` -> `{row['reject_reason']}`" for row in artifact["negative_fixtures"])
    ablations = "\n".join(f"- `{row['case_id']}`: {row['verdict']} ({row['reason']})" for row in artifact["ablation_results"])
    return f"""# Packet 079: Telos Multi-Receipt Joiner

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: promote the pass 0068 `p0068-telos-upgrade-ablation` queue item into
a concrete joiner fixture. The full packet must bind source intake, workspace
context, routing, verification, continuity, and action receipts.

```text
component_count = {len(artifact['component_receipts'])}
negative_fixture_count = {len(artifact['negative_fixtures'])}
ablation_count = {len(artifact['ablation_results'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Components

{components}

## Negative Fixtures

{negatives}

## Ablations

{ablations}

Current promoted natural laws: none.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0069 Steelman: Telos Multi-Receipt Joiner

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass proves only a local fixture. The strongest objection is that a joiner
can become a pretty envelope over weak components. The next promotion must
replace at least one synthetic fragment with a live tool receipt, preserve all
negative fixtures, and show that the product packet answers a buyer or research
workflow that a single incumbent log cannot answer.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    claims = [
        f"Pass 0069 created a TelosMultiReceiptJoiner/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0069 contains {len(artifact['component_receipts'])} component receipts covering required classes {artifact['product_packet']['required_classes']}.",
        f"Pass 0069 product packet has component_count {artifact['product_packet']['component_count']} and unsupported_claim_count {artifact['product_packet']['unsupported_claim_count']}.",
        f"Pass 0069 contains {len(artifact['negative_fixtures'])} negative fixtures and {len(artifact['ablation_results'])} ablation results.",
        f"Pass 0069 raw_private_payload_required is {artifact['product_packet']['raw_private_payload_required']} and model_reasoning_required_for_replay is {artifact['product_packet']['model_reasoning_required_for_replay']}.",
        f"Pass 0069 previous_pass_binding seal is {artifact['previous_pass_binding']}.",
        f"Pass 0069 composer sha256 is {shas['composer']} and compose_receipt status is {compose_receipt['status']}.",
        f"Pass 0069 packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"component_count={len(artifact['component_receipts'])}", f"required_classes={artifact['product_packet']['required_classes']}"],
        [f"component_count={artifact['product_packet']['component_count']}", f"unsupported_claim_count={artifact['product_packet']['unsupported_claim_count']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"ablation_count={len(artifact['ablation_results'])}"],
        [f"raw_private_payload_required={artifact['product_packet']['raw_private_payload_required']}", f"model_reasoning_required_for_replay={artifact['product_packet']['model_reasoning_required_for_replay']}"],
        [f"previous_pass_binding={artifact['previous_pass_binding']}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
    ]
    thesis = {
        "title": "Dogfood Pass 0069 Telos Multi-Receipt Joiner",
        "disposition": "fenced",
        "claims": [{"text": claim, "falsification": f"Claim {i + 1} differs from pass 0069 artifact values or required files are missing"} for i, claim in enumerate(claims)],
    }
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": "artifact-review", "tolerance": 0.5} for i, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "TELOS_MULTIRECEIPT_JOINER_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
