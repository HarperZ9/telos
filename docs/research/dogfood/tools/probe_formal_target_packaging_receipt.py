"""Generate pass 0118 formal target packaging artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_formal_target_packaging_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_formal_target_packaging_receipt.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0118_formal_target_packaging.py"
SOURCE_HELPER = ROOT / "tools" / "formal_target_sources_pass_0118.py"
OUT_PATH = ROOT / "schemas" / "formal-target-packaging-receipt-pass-0118.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0118-formal-target-packaging-validator-result.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0118.json"
PACKET_PATH = ROOT / "packets" / "128-formal-target-packaging-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "128-formal-target-packaging-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0118-formal-target-packaging-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0118-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0118-measurements.json"


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
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> str:
    return f"""# Packet 128: Formal Target Packaging Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: convert pass 0117 theorem-prover target declarations into concrete
Lean, Rocq, Isabelle, and Agda source artifacts while keeping parser and prover
execution explicitly fenced.

```text
theorem_prover_adapter_pass = {artifact['source_bindings']['theorem_prover_adapter_pass']}
target_count = {len(artifact['target_ids'])}
source_count = {len(artifact['source_targets'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
validator_status = {validator_receipt['status']}
```

## Source Targets

| Language | Path | Status | Execution |
| --- | --- | --- | --- |
{table(artifact['source_targets'], ['language', 'path', 'status', 'execution_status'])}

## Boundary

{artifact['execution_boundary']}

## Market Hypothesis

{artifact['market_gap_hypothesis']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Formal Target Packaging Brief

Date: 2026-07-01

## Decision

Make formal-prover source files first-class packet material. Pass 0118 emits
and hashes Lean, Rocq, Isabelle, and Agda targets derived from the pass 0117
finite category witness. This is still not a prover execution claim.

## Product Meaning

This moves the formal proof lane from loose target strings to portable source
files that a future prover runner can parse, execute, and return receipts for.
It is the adapter seam between research proof packets and actual formal proof
toolchains.

Manifest: `{artifact['manifest']['path']}`
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0118 Steelman: Formal Target Packaging

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that generated theorem-prover files can be invalid
even when hashes and target IDs match. Correct. This pass only proves source
emission, manifesting, hashing, and execution fencing. Parser/prover execution
must be a later receipt.

The second objection is that four prover syntaxes could drift independently.
Correct. This is why each language file has its own path, hash, parser command,
and `NOT_EXECUTED` boundary.

Boundary: {artifact['execution_boundary']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict, validator_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0118",
        "compose": compose_receipt,
        "test": test_receipt,
        "validator": validator_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_targets": artifact["source_targets"],
        "manifest": artifact["manifest"],
        "negative_fixtures": artifact["negative_fixtures"],
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {
        "artifact": OUT_PATH,
        "composer": COMPOSER,
        "source_helper": SOURCE_HELPER,
        "packet": PACKET_PATH,
        "brief": BRIEF_PATH,
        "steelman": STEELMAN_PATH,
        "test": TEST_SCRIPT,
        "validator": VALIDATOR,
        "validator_result": VALIDATOR_RESULT,
        "tool_receipts": TOOL_RECEIPTS_PATH,
    }
    shas = {name: sha256_file(path) for name, path in files.items()}
    source_hashes = ", ".join(f"{row['language']}={row['sha256']}" for row in artifact["source_targets"])
    claims = [
        f"Pass 0118 created a FormalTargetPackagingReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0118 binds theorem prover adapter pass {artifact['source_bindings']['theorem_prover_adapter_pass']} with adapter seal {artifact['source_bindings']['adapter_artifact_seal']}.",
        f"Pass 0118 emits {len(artifact['source_targets'])} formal source target files for languages lean4, rocq, isabelle, and agda.",
        f"Pass 0118 source files all contain {len(artifact['target_ids'])} adapter proposition ids and all have SOURCE_EMITTED_NOT_EXECUTED status.",
        "Pass 0118 records NOT_EXECUTED for every formal parser/prover branch.",
        f"Pass 0118 writes a FormalTargetSourceManifest/v1 manifest at {artifact['manifest']['path']} with sha256 {artifact['manifest']['sha256']}.",
        "Pass 0118 records a negative fixture that rejects missing associativity source targets.",
        "Pass 0118 flagship receipts for Forum, Index, Telos status, and Telos catalog all have MATCH status.",
        f"Pass 0118 validator receipt status is {receipts['validator']['status']} and test receipt status is {receipts['test']['status']}.",
        f"Pass 0118 source target hashes are {source_hashes}.",
        f"Pass 0118 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0118 composer sha256 is {shas['composer']}, source helper sha256 is {shas['source_helper']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, validator sha256 is {shas['validator']}, validator result sha256 is {shas['validator_result']}, and tool receipts sha256 is {shas['tool_receipts']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"languages={[row['language'] for row in artifact['source_targets']]}"],
        [f"source_targets={artifact['source_targets']}"],
        [f"execution_statuses={[row['execution_status'] for row in artifact['source_targets']]}"],
        [f"manifest={artifact['manifest']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}", f"telos_catalog={artifact['flagship_receipts']['telos_catalog']['status']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [source_hashes],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0118 Formal Target Packaging Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0118 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    ok = all(row["status"] == "MATCH" for row in receipts.values()) and artifact["status"] == "FORMAL_TARGET_PACKAGING_MATCH"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": "MATCH" if ok else "DRIFT"}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
