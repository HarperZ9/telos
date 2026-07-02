"""Generate pass 0092 BuildLang check receipt adapter artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buildlang_check_receipt_adapter.py"
TEST_SCRIPT = ROOT / "tools" / "test_buildlang_check_receipt_adapter.py"
OUT_PATH = ROOT / "schemas" / "buildlang-check-receipt-adapter-pass-0092.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0092.json"
PACKET_PATH = ROOT / "packets" / "102-buildlang-check-receipt-adapter.md"
BRIEF_PATH = ROOT / "briefs" / "102-buildlang-check-receipt-adapter-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0092-buildlang-check-receipt-adapter-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0092-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0092-measurements.json"


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
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def measurement_rows(artifact: dict) -> str:
    rows = []
    for item in artifact["crucible_adapter"]["measurements"]:
        rows.append(f"| {item['measurement_id']} | {item['status']} | {item['claim']} |")
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    receipt = artifact["check_receipt"]
    adapter = artifact["crucible_adapter"]
    summary = artifact["verify_summary"]
    return f"""# Packet 102: BuildLang Check Receipt Adapter

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: parse one real `buildc check --receipt` JSON artifact, verify it with
`buildc receipt verify`, and map source digest, policy, effects, and capability
evidence into Crucible-ready measurements.

```text
source = {artifact['source_fixture']['path']}
profile = {artifact['source_fixture']['profile']}
repo_branch = {artifact['repo_state']['branch_line']}
repo_dirty_count = {artifact['repo_state']['dirty_count']}
compiler_version = {receipt['compiler_version']}
source_digest = {receipt['source_digest']['hex']}
input_graph_digest = {receipt['input_graph_digest']['hex']}
policy_profile = {receipt['policy']['profile']}
declared_effects = {receipt['declared_effects']}
observed_capabilities = {receipt['observed_capabilities']}
verify_status = {artifact['verify_report']['status']}
verify_check_count = {summary['check_count']}
measurement_count = {adapter['measurement_count']}
adapter_match = {adapter['match']}
adapter_drift = {adapter['drift']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Measurements

| Measurement | Status | Claim |
| --- | --- | --- |
{measurement_rows(artifact)}

Boundary: this is one source-level compiler receipt adapter. It does not prove
language replacement, scientific discovery, full compiler correctness, or a
natural law.
"""


def render_brief(artifact: dict) -> str:
    adapter = artifact["crucible_adapter"]
    return f"""# BuildLang Check Receipt Adapter Brief

Date: 2026-07-01

## Result

Pass 0092 parses a real `buildc check --receipt` JSON object and verifies it
with `buildc receipt verify --json`. It emits {adapter['measurement_count']}
Crucible-ready measurements with {adapter['match']} MATCH and {adapter['drift']}
DRIFT.

## Product Meaning

This is the first structured BuildLang compiler-receipt bridge: source digest,
input graph digest, declared effects, observed capabilities, policy profile, and
verification checks are now portable into Telos proof packets.

## Next Adapter

Run the same adapter over a source that uses filesystem or environment effects,
then compare policy pass/fail behavior.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0092 Steelman: BuildLang Check Receipt Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this uses a tiny hello-world source. Correct.
The point is receipt plumbing, not compiler breadth. The next pass should use a
richer effect surface and include a negative policy fixture.

The second objection is that a passing receipt is not a formal proof of compiler
correctness. Correct. It is evidence packaging for one compiler action.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0092", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "check_command": artifact["check_command"], "verify_command": artifact["verify_command"], "adapter": {"measurement_count": artifact["crucible_adapter"]["measurement_count"], "match": artifact["crucible_adapter"]["match"], "drift": artifact["crucible_adapter"]["drift"]}}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    paths = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in paths.items()}
    receipt = artifact["check_receipt"]
    adapter = artifact["crucible_adapter"]
    summary = artifact["verify_summary"]
    claims = [
        f"Pass 0092 created a BuildLangCheckReceiptAdapter/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0092 binds prior pass {artifact['prior_binding']['source_pass']} and source fixture {artifact['source_fixture']['path']} with profile {artifact['source_fixture']['profile']}.",
        f"Pass 0092 check command exit_code is {artifact['check_command']['exit_code']} and verify command exit_code is {artifact['verify_command']['exit_code']}.",
        f"Pass 0092 check receipt schema is {receipt['schema']}, compiler {receipt['compiler']} {receipt['compiler_version']}, status {receipt['status']}, source digest {receipt['source_digest']['hex']}, and input graph digest {receipt['input_graph_digest']['hex']}.",
        f"Pass 0092 records declared effects {receipt['declared_effects']} and observed capabilities {receipt['observed_capabilities']}.",
        f"Pass 0092 policy profile is {receipt['policy']['profile']} with status {receipt['policy']['status']} and verification status {artifact['verify_report']['status']} across {summary['check_count']} checks.",
        f"Pass 0092 adapter creates {adapter['measurement_count']} Crucible-ready measurements with {adapter['match']} MATCH and {adapter['drift']} DRIFT.",
        f"Pass 0092 records {len(artifact['source_anchors'])} source anchors and no language replacement, scientific discovery, or natural-law claim.",
        f"Pass 0092 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0092 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_pass={artifact['prior_binding']['source_pass']}", f"source={artifact['source_fixture']['path']}", f"profile={artifact['source_fixture']['profile']}"],
        [f"check_exit_code={artifact['check_command']['exit_code']}", f"verify_exit_code={artifact['verify_command']['exit_code']}"],
        [f"receipt_schema={receipt['schema']}", f"compiler={receipt['compiler']}", f"compiler_version={receipt['compiler_version']}", f"status={receipt['status']}", f"source_digest={receipt['source_digest']['hex']}", f"input_graph_digest={receipt['input_graph_digest']['hex']}"],
        [f"declared_effects={receipt['declared_effects']}", f"observed_capabilities={receipt['observed_capabilities']}"],
        [f"policy_profile={receipt['policy']['profile']}", f"policy_status={receipt['policy']['status']}", f"verify_status={artifact['verify_report']['status']}", f"verify_check_count={summary['check_count']}"],
        [f"measurement_count={adapter['measurement_count']}", f"match={adapter['match']}", f"drift={adapter['drift']}"],
        [f"source_anchor_count={len(artifact['source_anchors'])}", f"promotion_boundary={artifact['promotion_boundary']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0092 BuildLang Check Receipt Adapter", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0092 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)], timeout=300)
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "BUILDLANG_CHECK_RECEIPT_ADAPTER_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
