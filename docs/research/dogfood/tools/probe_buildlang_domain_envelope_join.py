"""Generate pass 0075 receipts for BuildLang domain-envelope join."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buildlang_domain_envelope_join.py"
TEST_SCRIPT = ROOT / "tools" / "test_buildlang_domain_envelope_join.py"
OUT_PATH = ROOT / "schemas" / "buildlang-domain-envelope-join-pass-0075.json"
PACKET_PATH = ROOT / "packets" / "085-buildlang-domain-envelope-join.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0075-buildlang-domain-envelope-join-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0075-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0075-measurements.json"


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
    source = artifact["buildlang_source_component"]
    joined = artifact["joined_envelope"]
    negatives = "\n".join(f"- `{row['fixture_id']}` -> `{row['reject_reason']}`" for row in artifact["negative_fixtures"])
    return f"""# Packet 085: BuildLang Domain-Envelope Join

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: join the BuildLang source-ref receipt from pass 0074 into the
`buildlang_buildc` Telos domain-focus envelope from pass 0073.

```text
domain_id = {artifact['domain_id']}
source_component = {source['component_id']}
source_ref_count = {source['source_ref_count']}
corpus_verify_status = {source['corpus_verify_status']}
joined_envelope = {joined['envelope_id']}
root_context_fallback = {joined['root_context_fallback']}
path_scoped_context = {joined['path_scoped_context']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Boundary

The source-intake layer is now domain-specific for BuildLang/buildc. The
workspace-context layer is still the live root Index envelope, not path-scoped
BuildLang context.

## Negative Fixtures

{negatives}

Current promoted natural laws: none.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0075 Steelman: BuildLang Domain-Envelope Join

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass improves the `buildlang_buildc` domain envelope by replacing a generic
source-intake digest with a BuildLang-specific source-ref and corpus-verifier
receipt. It still leaves workspace context at root fallback. The next credible
promotion is not a bigger claim; it is an Index path-scoped context receipt for
the BuildLang checkout and Build Universe.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    source = artifact["buildlang_source_component"]
    joined = artifact["joined_envelope"]
    claims = [
        f"Pass 0075 created a BuildLangDomainEnvelopeJoin/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0075 joins domain {artifact['domain_id']} with source component {source['component_id']}.",
        f"Pass 0075 joined envelope {joined['envelope_id']} has source digest {joined['component_digests']['source_intake']}.",
        f"Pass 0075 BuildLang source component has source_ref_count {source['source_ref_count']} and corpus_verify_status {source['corpus_verify_status']}.",
        f"Pass 0075 preserves root_context_fallback {joined['root_context_fallback']} and path_scoped_context {joined['path_scoped_context']}.",
        f"Pass 0075 production backend claim is {source['production_backend_claim']}.",
        f"Pass 0075 contains {len(artifact['negative_fixtures'])} negative fixtures and unsupported_claim_count {artifact['unsupported_claim_count']}.",
        f"Pass 0075 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"domain_id={artifact['domain_id']}", f"source_component={source['component_id']}"],
        [f"joined_envelope={joined['envelope_id']}", f"source_digest={joined['component_digests']['source_intake']}"],
        [f"source_ref_count={source['source_ref_count']}", f"corpus_verify_status={source['corpus_verify_status']}"],
        [f"root_context_fallback={joined['root_context_fallback']}", f"path_scoped_context={joined['path_scoped_context']}"],
        [f"production_backend_claim={source['production_backend_claim']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0075 BuildLang Domain Envelope Join", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0075 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "BUILDLANG_DOMAIN_ENVELOPE_JOIN_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
