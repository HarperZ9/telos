"""Generate pass 0076 receipts for BuildLang Index focus bridge."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buildlang_index_focus_bridge.py"
TEST_SCRIPT = ROOT / "tools" / "test_buildlang_index_focus_bridge.py"
OUT_PATH = ROOT / "schemas" / "buildlang-index-focus-bridge-pass-0076.json"
PACKET_PATH = ROOT / "packets" / "086-buildlang-index-focus-bridge.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0076-buildlang-index-focus-bridge-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0076-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0076-measurements.json"


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
    presence = artifact["index_map"]["requested_path_presence"]
    focus_rows = "\n".join(f"- `{row['command']}` -> `{row['verdict']}`" for row in artifact["focus_probes"])
    negative_rows = "\n".join(f"- `{row['fixture_id']}` -> `{row['reject_reason']}`" for row in artifact["negative_fixtures"])
    return f"""# Packet 086: BuildLang Index Focus Bridge

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: test whether Index can produce path-scoped context for BuildLang
today, then specify the bridge required when it cannot.

```text
root_context_status = {artifact['root_context']['status']}
root_context_source_refs = {artifact['root_context']['source_ref_count']}
path_scoped_context = {artifact['path_scoped_context']}
bridge_required = {artifact['bridge_required']}
buildlang_present = {presence['buildlang']['present']}
compiler_present = {presence['compiler']['present']}
build_universe_present = {presence['build-universe']['present']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Focus Probes

{focus_rows}

## Bridge

`{artifact['bridge_strategy']['name']}` should convert explicit path selectors
into source-ref manifests, preserve source-ref-only privacy, and reject missing
paths until a concrete source root exists.

## Negative Fixtures

{negative_rows}

Current promoted natural laws: none.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0076 Steelman: BuildLang Index Focus Bridge

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest finding is negative: Index already gives a valid repo-root
context envelope for the BuildLang checkout, but the focus interface rejects
the path selectors needed for BuildLang/buildc/build-universe domain work. The
market implication is that proof-centered megatools need path-selector receipts,
not only repo-level context.

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
    presence = artifact["index_map"]["requested_path_presence"]
    focus_count = len(artifact["focus_probes"])
    expected_reject_count = sum(1 for row in artifact["focus_probes"] if row["verdict"] == "EXPECTED_REJECT")
    claims = [
        f"Pass 0076 created a BuildLangIndexFocusBridge/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0076 root Index context status is {artifact['root_context']['status']} with source_ref_count {artifact['root_context']['source_ref_count']}.",
        f"Pass 0076 records path_scoped_context {artifact['path_scoped_context']} and bridge_required {artifact['bridge_required']}.",
        f"Pass 0076 focus probes contain {focus_count} probes and {expected_reject_count} expected rejections.",
        f"Pass 0076 Index map presence is buildlang={presence['buildlang']['present']}, compiler={presence['compiler']['present']}, build-universe={presence['build-universe']['present']}.",
        f"Pass 0076 source receipt pass is {artifact['source_ref_receipt']['receipt_pass']} with source_ref_count {artifact['source_ref_receipt']['source_ref_count']}.",
        f"Pass 0076 contains {len(artifact['negative_fixtures'])} negative fixtures and unsupported_claim_count {artifact['unsupported_claim_count']}.",
        f"Pass 0076 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"root_context_status={artifact['root_context']['status']}", f"source_ref_count={artifact['root_context']['source_ref_count']}"],
        [f"path_scoped_context={artifact['path_scoped_context']}", f"bridge_required={artifact['bridge_required']}"],
        [f"focus_probe_count={focus_count}", f"expected_reject_count={expected_reject_count}"],
        [f"buildlang={presence['buildlang']['present']}", f"compiler={presence['compiler']['present']}", f"build-universe={presence['build-universe']['present']}"],
        [f"source_receipt_pass={artifact['source_ref_receipt']['receipt_pass']}", f"source_ref_count={artifact['source_ref_receipt']['source_ref_count']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0076 BuildLang Index Focus Bridge", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0076 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "BUILDLANG_INDEX_FOCUS_BRIDGE_REQUIRED" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
