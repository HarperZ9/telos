"""Generate pass 0073 receipts for Telos domain-focus envelope."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_telos_domain_focus_envelope.py"
TEST_SCRIPT = ROOT / "tools" / "test_telos_domain_focus_envelope.py"
OUT_PATH = ROOT / "schemas" / "telos-domain-focus-envelope-pass-0073.json"
PACKET_PATH = ROOT / "packets" / "083-telos-domain-focus-envelope.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0073-telos-domain-focus-envelope-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0073-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0073-measurements.json"


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
    domains = "\n".join(f"- `{row['domain_id']}`: route `{row['route_decision']}`, root fallback `{row['root_context_fallback']}`, path scoped `{row['path_scoped_context']}`" for row in artifact["domain_envelopes"])
    negatives = "\n".join(f"- `{row['fixture_id']}` -> `{row['reject_reason']}`" for row in artifact["negative_fixtures"])
    return f"""# Packet 083: Telos Domain-Focus Envelope

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: turn the pass 0072 domain-focus adapter experiment into a replayable
Telos envelope set that joins source intake, workspace context, routing,
verification, continuity, and action receipts for each domain.

```text
domain_count = {artifact['domain_count']}
root_fallback_envelopes = {artifact['root_fallback_envelopes']}
path_scoped_envelopes = {artifact['path_scoped_envelopes']}
negative_fixture_count = {len(artifact['negative_fixtures'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Domain Envelopes

{domains}

## Negative Fixtures

{negatives}

Current promoted natural laws: none.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0073 Steelman: Telos Domain-Focus Envelope

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass creates a product-shaped envelope set over existing receipts. It is a
useful megatool integration target, but it still uses root context fallback for
all domains. It should not be sold internally as domain-aware retrieval until
Index emits path-scoped source refs and the envelope joins those refs to each
domain claim.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    claims = [
        f"Pass 0073 created a TelosDomainFocusEnvelopeSet/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0073 contains {artifact['domain_count']} TelosDomainFocusEnvelope/v1 domain envelopes.",
        f"Pass 0073 has root_fallback_envelopes {artifact['root_fallback_envelopes']} and path_scoped_envelopes {artifact['path_scoped_envelopes']}.",
        f"Pass 0073 envelopes require source_intake, workspace_context, routing, verification, continuity, and action layers.",
        f"Pass 0073 contains {len(artifact['negative_fixtures'])} negative fixtures and {len(artifact['ablation_results'])} ablation results.",
        f"Pass 0073 unsupported_claim_count is {artifact['unsupported_claim_count']}.",
        f"Pass 0073 uses base source component {artifact['base_components']['source_intake']['component_id']} and workspace component {artifact['base_components']['workspace_context']['component_id']}.",
        f"Pass 0073 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"domain_count={artifact['domain_count']}"],
        [f"root_fallback_envelopes={artifact['root_fallback_envelopes']}", f"path_scoped_envelopes={artifact['path_scoped_envelopes']}"],
        [f"required_layers={artifact['domain_envelopes'][0]['required_layers']}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"ablation_count={len(artifact['ablation_results'])}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}"],
        [f"source_component={artifact['base_components']['source_intake']['component_id']}", f"workspace_component={artifact['base_components']['workspace_context']['component_id']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0073 Telos Domain Focus Envelope", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0073 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "TELOS_DOMAIN_FOCUS_ENVELOPE_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
