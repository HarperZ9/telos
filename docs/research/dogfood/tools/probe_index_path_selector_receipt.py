"""Generate pass 0078 receipts for Index path-selector receipt fixture."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_index_path_selector_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_index_path_selector_receipt.py"
OUT_PATH = ROOT / "schemas" / "index-path-selector-receipt-pass-0078.json"
PACKET_PATH = ROOT / "packets" / "088-index-path-selector-receipt.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0078-index-path-selector-receipt-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0078-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0078-measurements.json"


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
    results = "\n".join(f"- `{row['selector']}` -> `{row['status']}` ({row['reason']}) refs `{row['source_ref_count']}`" for row in artifact["selector_results"])
    return f"""# Packet 088: Index Path-Selector Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: emit an executable `IndexPathSelectorReceipt/v1` adapter fixture over
the external BuildLang checkout.

```text
selected_selectors = {artifact['selected_selector_count']}
rejected_selectors = {artifact['rejected_selector_count']}
source_refs = {artifact['source_ref_count']}
raw_source_included = {artifact['raw_source_included']}
source_refs_only = {artifact['source_refs_only']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Selector Results

{results}

## Boundary

This is an adapter fixture, not native Index path-selection support. It excludes
generated build outputs such as `target` and rejects missing `build-universe`
coverage.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0078 Steelman: Index Path-Selector Receipt

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass closes the immediate proof-packet gap with a fixture, not a native
Index implementation. That is still useful because downstream Telos envelopes
can now consume the exact shape expected from native Index later. The risk is
that fixture behavior diverges from eventual Index behavior; the next pass
should join this receipt into the BuildLang envelope and keep the adapter label
visible.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    results = {row["selector"]: row for row in artifact["selector_results"]}
    claims = [
        f"Pass 0078 created an IndexPathSelectorReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0078 selector buildlang status is {results['buildlang']['status']} with source_ref_count {results['buildlang']['source_ref_count']}.",
        f"Pass 0078 selector compiler status is {results['compiler']['status']} with source_ref_count {results['compiler']['source_ref_count']}.",
        f"Pass 0078 selector build-universe status is {results['build-universe']['status']} with reason {results['build-universe']['reason']}.",
        f"Pass 0078 selected_selector_count is {artifact['selected_selector_count']} and rejected_selector_count is {artifact['rejected_selector_count']}.",
        f"Pass 0078 source_ref_count is {artifact['source_ref_count']} with raw_source_included {artifact['raw_source_included']} and source_refs_only {artifact['source_refs_only']}.",
        f"Pass 0078 excluded dirs include target and unsupported_claim_count is {artifact['unsupported_claim_count']}.",
        f"Pass 0078 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"buildlang_status={results['buildlang']['status']}", f"buildlang_refs={results['buildlang']['source_ref_count']}"],
        [f"compiler_status={results['compiler']['status']}", f"compiler_refs={results['compiler']['source_ref_count']}"],
        [f"build_universe_status={results['build-universe']['status']}", f"reason={results['build-universe']['reason']}"],
        [f"selected_selector_count={artifact['selected_selector_count']}", f"rejected_selector_count={artifact['rejected_selector_count']}"],
        [f"source_ref_count={artifact['source_ref_count']}", f"raw_source_included={artifact['raw_source_included']}", f"source_refs_only={artifact['source_refs_only']}"],
        [f"target_excluded={'target' in artifact['excluded_dirs']}", f"unsupported_claim_count={artifact['unsupported_claim_count']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0078 Index Path Selector Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0078 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "INDEX_PATH_SELECTOR_RECEIPT_FIXTURE_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
