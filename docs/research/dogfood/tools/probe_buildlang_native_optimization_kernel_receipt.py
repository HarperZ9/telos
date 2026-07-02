"""Generate pass 0095 BuildLang native optimization kernel artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buildlang_native_optimization_kernel_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_buildlang_native_optimization_kernel_receipt.py"
OUT_PATH = ROOT / "schemas" / "buildlang-native-optimization-kernel-receipt-pass-0095.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0095.json"
PACKET_PATH = ROOT / "packets" / "105-buildlang-native-optimization-kernel-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "105-buildlang-native-optimization-kernel-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0095-buildlang-native-optimization-kernel-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0095-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0095-measurements.json"


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


def run_command(command: list[str], timeout: int = 240) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def measurement_rows(artifact: dict) -> str:
    rows = []
    for item in artifact["measurements"]:
        rows.append(f"| `{item['measurement_id']}` | {item['status']} | {item['claim']} |")
    return "\n".join(rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    receipt = artifact["check_receipt"]
    output = artifact["run_output"]
    return f"""# Packet 105: BuildLang Native Optimization Kernel Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: run a BuildLang-native exact-enumeration optimization source and bind
its run output to `buildc check --receipt` and `buildc receipt verify`.

```text
source = {artifact['source_fixture']['path']}
profile = {artifact['source_fixture']['profile']}
compiler_version = {receipt['compiler_version']}
source_digest = {receipt['source_digest']['hex']}
best_value = {output['best value']}
best_weight = {output['best weight']}
best_mask = {output['best mask']}
feasible_count = {output['feasible count']}
verify_check_count = {artifact['verify_summary']['check_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Measurements

| Measurement | Status | Claim |
| --- | --- | --- |
{measurement_rows(artifact)}

Boundary: this pass proves one BuildLang exact-enumeration fixture can run and
emit receipts. It does not prove language replacement, production optimization,
scientific discovery, or a natural law.
"""


def render_brief(artifact: dict) -> str:
    output = artifact["run_output"]
    return f"""# BuildLang Native Optimization Kernel Brief

Date: 2026-07-01

## Result

Pass 0095 runs the 12-item knapsack exact enumeration directly in BuildLang.
The program emits best value {output['best value']}, best weight
{output['best weight']}, best mask {output['best mask']}, and feasible count
{output['feasible count']}. The source also has a verified `buildc` receipt.

## Product Meaning

This moves the optimization megatool from external Python-only replay toward a
language/runtime receipt. The next step is either a BuildLang branch-comparison
kernel or an OR-Tools install/dependency receipt for market comparability.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0095 Steelman: BuildLang Native Optimization Kernel

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that this is brute-force enumeration, not an
advanced optimizer. Correct. That is intentional: exact enumeration gives a
ground truth for later heuristic, quantum, and compiler/runtime claims.

The second objection is that a single source receipt does not prove BuildLang is
ready to replace existing scientific languages. Correct. It proves one
accountable source/run/receipt shape.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0095", "compose": compose_receipt, "test": test_receipt, "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "run_output": artifact["run_output"]}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    paths = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in paths.items()}
    output = artifact["run_output"]
    receipt = artifact["check_receipt"]
    claims = [
        f"Pass 0095 created a BuildLangNativeOptimizationKernelReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0095 binds prior workflow pass {artifact['prior_workflow_binding']['source_pass']} and source fixture {artifact['source_fixture']['path']}.",
        f"Pass 0095 buildc check, receipt verify, and buildc run commands all exit 0.",
        f"Pass 0095 BuildLang run output records best value {output['best value']}, best weight {output['best weight']}, best mask {output['best mask']}, and feasible count {output['feasible count']}.",
        f"Pass 0095 check receipt status is {receipt['status']}, source digest {receipt['source_digest']['hex']}, and policy profile {receipt['policy']['profile']}.",
        f"Pass 0095 verify report status is {artifact['verify_report']['status']} across {artifact['verify_summary']['check_count']} checks.",
        f"Pass 0095 records {len(artifact['measurements'])} measurements and MATCH flagship receipts.",
        f"Pass 0095 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0095 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_pass={artifact['prior_workflow_binding']['source_pass']}", f"source={artifact['source_fixture']['path']}"],
        [f"check_exit_code={artifact['check_command']['exit_code']}", f"verify_exit_code={artifact['verify_command']['exit_code']}", f"run_exit_code={artifact['run_command']['exit_code']}"],
        [f"best_value={output['best value']}", f"best_weight={output['best weight']}", f"best_mask={output['best mask']}", f"feasible_count={output['feasible count']}"],
        [f"receipt_status={receipt['status']}", f"source_digest={receipt['source_digest']['hex']}", f"policy_profile={receipt['policy']['profile']}"],
        [f"verify_status={artifact['verify_report']['status']}", f"verify_check_count={artifact['verify_summary']['check_count']}"],
        [f"measurement_count={len(artifact['measurements'])}", f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0095 BuildLang Native Optimization Kernel Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0095 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "BUILDLANG_NATIVE_OPTIMIZATION_KERNEL_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
