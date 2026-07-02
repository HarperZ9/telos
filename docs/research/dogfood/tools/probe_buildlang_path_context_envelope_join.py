"""Generate pass 0079 receipts for BuildLang path-context envelope join."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buildlang_path_context_envelope_join.py"
TEST_SCRIPT = ROOT / "tools" / "test_buildlang_path_context_envelope_join.py"
OUT_PATH = ROOT / "schemas" / "buildlang-path-context-envelope-join-pass-0079.json"
PACKET_PATH = ROOT / "packets" / "089-buildlang-path-context-envelope-join.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0079-buildlang-path-context-envelope-join-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0079-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0079-measurements.json"


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
    context = artifact["path_context_component"]
    joined = artifact["joined_envelope"]
    return f"""# Packet 089: BuildLang Path-Context Envelope Join

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: join the pass 0078 path-selector receipt into the BuildLang domain
envelope as the workspace-context layer.

```text
joined_envelope = {joined['envelope_id']}
workspace_context = {context['component_id']}
source_refs = {context['source_ref_count']}
root_context_fallback = {joined['root_context_fallback']}
path_scoped_context = {joined['path_scoped_context']}
adapter_fixture = {joined['adapter_fixture']}
native_index_path_selector = {joined['native_index_path_selector']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

Boundary: this proves a path-context envelope join using an adapter fixture. It
does not prove native Index path selection or Build Universe coverage.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0079 Steelman: BuildLang Path-Context Envelope Join

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass is a real integration step: root-context fallback is replaced by a
path-selector receipt. The strongest objection is that the receipt is still an
adapter fixture. That boundary is preserved in the joined envelope with
`adapter_fixture=true` and `native_index_path_selector=false`.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    context = artifact["path_context_component"]
    joined = artifact["joined_envelope"]
    claims = [
        f"Pass 0079 created a BuildLangPathContextEnvelopeJoin/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0079 joins workspace context component {context['component_id']} into envelope {joined['envelope_id']}.",
        f"Pass 0079 workspace context source_ref_count is {context['source_ref_count']} and missing selector rejections include build-universe.",
        f"Pass 0079 joined envelope root_context_fallback is {joined['root_context_fallback']} and path_scoped_context is {joined['path_scoped_context']}.",
        f"Pass 0079 joined envelope adapter_fixture is {joined['adapter_fixture']} and native_index_path_selector is {joined['native_index_path_selector']}.",
        f"Pass 0079 workspace_context digest is {joined['component_digests']['workspace_context']}.",
        f"Pass 0079 contains {len(artifact['negative_fixtures'])} negative fixtures and unsupported_claim_count {artifact['unsupported_claim_count']}.",
        f"Pass 0079 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"component_id={context['component_id']}", f"envelope_id={joined['envelope_id']}"],
        [f"source_ref_count={context['source_ref_count']}", f"missing={context['missing_selector_rejections']}"],
        [f"root_context_fallback={joined['root_context_fallback']}", f"path_scoped_context={joined['path_scoped_context']}"],
        [f"adapter_fixture={joined['adapter_fixture']}", f"native_index_path_selector={joined['native_index_path_selector']}"],
        [f"workspace_context_digest={joined['component_digests']['workspace_context']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0079 BuildLang Path Context Envelope Join", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0079 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "BUILDLANG_PATH_CONTEXT_ENVELOPE_JOIN_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
