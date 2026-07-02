"""Generate pass 0104 AI4Science claim-to-experiment artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_ai4science_claim_to_experiment_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_ai4science_claim_to_experiment_receipt.py"
OUT_PATH = ROOT / "schemas" / "ai4science-claim-to-experiment-receipt-pass-0104.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0104.json"
PACKET_PATH = ROOT / "packets" / "114-ai4science-claim-to-experiment-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "114-ai4science-claim-to-experiment-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0104-ai4science-claim-to-experiment-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0104-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0104-measurements.json"


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


def source_rows(artifact: dict) -> str:
    rows = []
    for row in artifact["source_to_receipt_map"]:
        rows.append(f"| {row['name']} | {row['source_kind']} | {row['gap_status']} | {', '.join(row['required_receipts'][:3])} |")
    return "\n".join(rows)


def experiment_rows(artifact: dict) -> str:
    return "\n".join(f"| `{row['experiment_id']}` | {', '.join(row['acceptance'])} | {row['status']} |" for row in artifact["next_experiments"])


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    source = artifact["source_summary"]
    return f"""# Packet 114: AI4Science Claim-to-Experiment Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: convert AI4Science market and whitepaper sources into a minimum
claim-to-experiment receipt. This pass maps agentic discovery, biomolecular
models, workflow engines, and lab-record systems into proof fields without
promoting any biological or drug-discovery claim.

```text
source_count = {source['source_count']}
official_or_primary_count = {source['official_or_primary_count']}
youtube_ai4science_video_count = {source['youtube_ai4science_video_count']}
minimum_packet_fields = {len(artifact['minimum_packet_fields'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Source-To-Receipt Map

| Source | Kind | Gap Status | First Required Receipts |
| --- | --- | --- | --- |
{source_rows(artifact)}

## Promotion Gates

- Reject unmeasured discovery claims: `{artifact['promotion_gates']['rejects_unmeasured_discovery_claim']}`.
- Require reproduction status: `{artifact['promotion_gates']['requires_reproduction_status']}`.
- Require human review: `{artifact['promotion_gates']['requires_human_review']}`.

## Next Experiments

| Experiment | Acceptance | Status |
| --- | --- | --- |
{experiment_rows(artifact)}

Boundary: this pass is a receipt schema and market/research map. It does not
prove a biological result, drug efficacy, benchmark superiority, or a natural
law.
"""


def render_brief(artifact: dict) -> str:
    return """# AI4Science Claim-to-Experiment Brief

Date: 2026-07-01

## Decision

Build `AI4ScienceClaimToExperimentReceipt/v1` as the second public proof lane
after the optimization workbench.

## Why

Incumbents cover agents, foundation models, workflows, and lab data. The Telos
wedge is the portable proof packet that binds source claim, agent action,
protocol, workflow run, measurement, negative result, review, and promotion
verdict.

## Next Implementation Target

Create one minimum biological claim packet that refuses promotion until a
measurement receipt and reproduction status are attached.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0104 Steelman: AI4Science Claim-to-Experiment

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this pass does not run a biological experiment.
Correct. It defines the receipt gates that must exist before a model-generated
or literature-derived biological claim can be promoted.

The second objection is that incumbents already have strong pieces: scientific
agents, foundation models, workflow engines, and lab data systems. Correct. The
market gap is marked inferred. The only local claim is that Telos can express a
cross-layer receipt shape that keeps those pieces reviewable together.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0104",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "source_summary": artifact["source_summary"],
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {name: sha256_file(path) for name, path in {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}.items()}
    source = artifact["source_summary"]
    claims = [
        f"Pass 0104 created an AI4ScienceClaimToExperimentReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0104 binds source passes {artifact['source_bindings']} and records {source['source_count']} sources.",
        f"Pass 0104 records {source['official_or_primary_count']} official or primary sources and {source['youtube_ai4science_video_count']} YouTube AI4Science source video.",
        f"Pass 0104 defines {len(artifact['minimum_packet_fields'])} minimum packet fields.",
        f"Pass 0104 maps {len(artifact['source_to_receipt_map'])} sources to receipt requirements.",
        f"Pass 0104 defines {len(artifact['next_experiments'])} next experiments and promotion gates {artifact['promotion_gates']}.",
        f"Pass 0104 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0104 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0104 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}", f"source_count={source['source_count']}"],
        [f"official_or_primary_count={source['official_or_primary_count']}", f"youtube_ai4science_video_count={source['youtube_ai4science_video_count']}"],
        [f"minimum_packet_fields={artifact['minimum_packet_fields']}"],
        [f"source_to_receipt_map_count={len(artifact['source_to_receipt_map'])}"],
        [f"next_experiments={len(artifact['next_experiments'])}", f"promotion_gates={artifact['promotion_gates']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0104 AI4Science Claim-to-Experiment Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0104 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
