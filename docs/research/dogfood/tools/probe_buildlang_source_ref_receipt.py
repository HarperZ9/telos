"""Generate pass 0074 receipts for BuildLang source-ref receipt."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buildlang_source_ref_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_buildlang_source_ref_receipt.py"
OUT_PATH = ROOT / "schemas" / "buildlang-source-ref-receipt-pass-0074.json"
PACKET_PATH = ROOT / "packets" / "084-buildlang-source-ref-receipt.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0074-buildlang-source-ref-receipt-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0074-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0074-measurements.json"


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
    refs = "\n".join(f"- `{row['relative_path']}` sha256 `{row['sha256']}`" for row in artifact["source_refs"][:6])
    checks = "\n".join(f"- `{key}`: {value}" for key, value in artifact["corpus_verify"]["expected_line_checks"].items())
    return f"""# Packet 084: BuildLang Source-Ref Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: bind BuildLang/buildc source refs to a live executable corpus
verification receipt.

```text
source_ref_count = {artifact['source_ref_count']}
program_count = {artifact['program_count']}
corpus_verify_status = {artifact['corpus_verify']['status']}
corpus_verify_match = {artifact['corpus_verify']['match']}
corpus_verify_drift = {artifact['corpus_verify']['drift']}
production_backend_claim = {artifact['production_backend_claim']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Source Refs

{refs}

## Corpus Verify Lines

{checks}

Current promoted natural laws: none.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0074 Steelman: BuildLang Source-Ref Receipt

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass gives BuildLang a stronger evidence bundle than a strategy note: real
source refs plus a live `buildc corpus verify` receipt. It still must not be
over-promoted. The verified production backend claim is C backend only, the
self-hosted compiler remains aspirational, and the corpus covers 8 semantic
programs rather than arbitrary scientific workloads.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    claims = [
        f"Pass 0074 created a BuildLangSourceRefReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0074 binds {artifact['source_ref_count']} BuildLang source refs.",
        f"Pass 0074 ran {artifact['corpus_verify']['command']} with status {artifact['corpus_verify']['status']} and drift {artifact['corpus_verify']['drift']}.",
        f"Pass 0074 corpus verification covers {artifact['program_count']} semantic programs.",
        f"Pass 0074 records receipt surfaces {artifact['receipt_surfaces']}.",
        f"Pass 0074 production backend claim is {artifact['production_backend_claim']}.",
        f"Pass 0074 contains {len(artifact['negative_fixtures'])} negative fixtures and unsupported_claim_count {artifact['unsupported_claim_count']}.",
        f"Pass 0074 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_ref_count={artifact['source_ref_count']}"],
        [f"command={artifact['corpus_verify']['command']}", f"status={artifact['corpus_verify']['status']}", f"drift={artifact['corpus_verify']['drift']}"],
        [f"program_count={artifact['program_count']}"],
        [f"receipt_surfaces={artifact['receipt_surfaces']}"],
        [f"production_backend_claim={artifact['production_backend_claim']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0074 BuildLang Source Ref Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0074 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "BUILDLANG_SOURCE_REF_RECEIPT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
