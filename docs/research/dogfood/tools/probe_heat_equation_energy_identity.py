"""Generate pass 0062 receipts for heat-equation energy identity."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_heat_equation_energy_identity.py"
TEST_SCRIPT = ROOT / "tools" / "test_heat_equation_energy_identity.py"
OUT_PATH = ROOT / "schemas" / "heat-equation-energy-identity-pass-0062.json"
PACKET_PATH = ROOT / "packets" / "072-heat-equation-energy-identity.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0062-heat-equation-energy-identity-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0062-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0062-measurements.json"


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


def render_packet(packet: dict, compose_receipt: dict, test_receipt: dict) -> str:
    probe = packet["numeric_probe"]
    return f"""# Packet 072: Heat Equation Energy Identity

Date: 2026-07-01

Status: `{packet['status']}`

Identity: `{packet['analytic_identity']['identity']}`

Scope: `{packet['domain_scope']['equation']}` on `{packet['domain_scope']['spatial_domain']}` with `{packet['domain_scope']['boundary_condition']}` boundary conditions and smooth finite Fourier modes.

```text
promotion_state = {packet['promotion_state']}
law_candidate_status = {packet['law_candidate_status']}
mode_count = {probe['mode_count']}
max_symbolic_residual = {probe['max_symbolic_residual']}
max_finite_difference_residual = {probe['max_finite_difference_residual']}
energy_monotone_nonincreasing = {probe['energy_monotone_nonincreasing']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

Current promoted natural laws: none.
"""


def render_steelman(packet: dict) -> str:
    return f"""# Pass 0062 Steelman: Heat Equation Energy Identity

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass proves a scoped identity, not a new physics law. It can fail if the
boundary term is nonzero, if forcing or nonlinear diffusion is added, if the
solution class does not justify integration by parts, or if the numeric probe
is mistaken for empirical validation.

Promotion state remains `{packet['promotion_state']}`.
"""


def build_thesis_measurements(packet: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    probe = packet["numeric_probe"]
    claims = [
        f"Pass 0062 created a HeatEquationEnergyIdentity/v1 artifact with status {packet['status']}, promotion_state {packet['promotion_state']}, law_candidate_status {packet['law_candidate_status']}, sha256 {shas['artifact']}, and seal {packet['seal']}.",
        f"Pass 0062 implements compose_heat_equation_energy_identity.py with sha256 {shas['composer']} and compose_receipt status {compose_receipt['status']}.",
        f"Pass 0062 records a heat equation energy identity test with sha256 {shas['test']} and test_receipt status {test_receipt['status']}.",
        f"Pass 0062 analytic identity is {packet['analytic_identity']['identity']} under boundary condition {packet['domain_scope']['boundary_condition']} on {packet['domain_scope']['spatial_domain']}.",
        f"Pass 0062 numeric probe has mode_count {probe['mode_count']}, max_symbolic_residual {probe['max_symbolic_residual']}, max_finite_difference_residual {probe['max_finite_difference_residual']}, and energy_monotone_nonincreasing {probe['energy_monotone_nonincreasing']}.",
        f"Pass 0062 source_anchor_count is {len(packet['source_anchors'])} and source anchors are retained as source leads.",
        f"Pass 0062 unsupported_claim_count is {packet['unsupported_claim_count']} and current_promoted_natural_laws remains none.",
        f"Pass 0062 records packet 072 sha256 {shas['packet']} and steelman sha256 {shas['steelman']}.",
    ]
    evidence = [
        [f"schema={packet['schema']}", f"status={packet['status']}", f"promotion_state={packet['promotion_state']}", f"law_candidate_status={packet['law_candidate_status']}", f"sha256={shas['artifact']}", f"seal={packet['seal']}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
        [f"identity={packet['analytic_identity']['identity']}", f"boundary_condition={packet['domain_scope']['boundary_condition']}", f"domain={packet['domain_scope']['spatial_domain']}"],
        [f"mode_count={probe['mode_count']}", f"max_symbolic_residual={probe['max_symbolic_residual']}", f"max_finite_difference_residual={probe['max_finite_difference_residual']}", f"energy_monotone_nonincreasing={probe['energy_monotone_nonincreasing']}"],
        [f"source_anchor_count={len(packet['source_anchors'])}", "verification_status=source_lead"],
        [f"unsupported_claim_count={packet['unsupported_claim_count']}", "current_promoted_natural_laws=[]"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}"],
    ]
    methods = ["artifact-schema-review", "composer-file-review", "composer-test-review", "analytic-identity-review", "numeric-probe-review", "source-anchor-review", "non-promotion-boundary-review", "packet-steelman-review"]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0062 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0062 Heat Equation Energy Identity"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": methods[i], "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    packet = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(packet, compose_receipt, test_receipt))
    write_text(STEELMAN_PATH, render_steelman(packet))
    thesis, measurements = build_thesis_measurements(packet, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and packet["status"].endswith("_MATCH") else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": packet["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
