"""Generate pass 0072 receipts for domain-focus adapter experiment."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_domain_focus_adapter_experiment.py"
TEST_SCRIPT = ROOT / "tools" / "test_domain_focus_adapter_experiment.py"
OUT_PATH = ROOT / "schemas" / "domain-focus-adapter-experiment-pass-0072.json"
PACKET_PATH = ROOT / "packets" / "082-domain-focus-adapter-experiment.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0072-domain-focus-adapter-experiment-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0072-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0072-measurements.json"


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
    domains = "\n".join(f"- `{row['domain_id']}`: route `{row['forum_status']}`, strategy `{row['index_strategy']}`" for row in artifact["adapter_rows"])
    improvements = "\n".join(f"- `{row['tool']}`: {row['gap']} -> {row['next']}" for row in artifact["tool_improvement_queue"])
    negatives = "\n".join(f"- `{row['fixture_id']}` -> `{row['reject_reason']}`" for row in artifact["negative_fixtures"])
    return f"""# Packet 082: Domain-Focus Adapter Experiment

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: test whether domain-specific growth vectors can be routed and
packaged across Gather, Index, Forum, Crucible, and Telos as one adapter layer.

```text
domain_count = {artifact['domain_count']}
adapted_project_telos = {artifact['route_summary']['adapted_project_telos']}
adapted_escalations = {artifact['route_summary']['adapted_escalations']}
valid_index_focuses = {artifact['index_summary']['valid_focuses']}
rejected_index_focus_count = {artifact['index_summary']['rejected_focus_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Domain Rows

{domains}

## Tool Improvement Queue

{improvements}

## Negative Fixtures

{negatives}

Current promoted natural laws: none.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0072 Steelman: Domain-Focus Adapter Experiment

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass demonstrates a route vocabulary bridge and an adapter contract. It
does not implement true Index path focus, semantic repo slicing, or market
proof. The adapter is useful only because it records current failure modes:
raw domain prompts can escalate, and Index rejects domain/path focus labels
except the root `telos` repo focus.

The strongest next move is therefore implementation-oriented: make domain focus
a first-class substrate primitive, then rerun the same experiment with actual
domain-specific source refs instead of root fallback.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    claims = [
        f"Pass 0072 created a DomainFocusAdapterExperiment/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0072 covers {artifact['domain_count']} domain-focus rows.",
        f"Pass 0072 adapted Forum route probes decide project-telos for {artifact['route_summary']['adapted_project_telos']} domains with adapted_escalations {artifact['route_summary']['adapted_escalations']}.",
        f"Pass 0072 Index focus probes have valid focuses {artifact['index_summary']['valid_focuses']} and rejected_focus_count {artifact['index_summary']['rejected_focus_count']}.",
        f"Pass 0072 defines {len(artifact['tool_improvement_queue'])} tool improvement rows across Index, Forum, Gather, Crucible, and Telos.",
        f"Pass 0072 contains {len(artifact['negative_fixtures'])} negative fixtures and unsupported_claim_count {artifact['unsupported_claim_count']}.",
        f"Pass 0072 average Project Telos route score lift is {artifact['route_summary']['average_project_telos_score_lift']:.6f}.",
        f"Pass 0072 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"domain_count={artifact['domain_count']}"],
        [f"adapted_project_telos={artifact['route_summary']['adapted_project_telos']}", f"adapted_escalations={artifact['route_summary']['adapted_escalations']}"],
        [f"valid_focuses={artifact['index_summary']['valid_focuses']}", f"rejected_focus_count={artifact['index_summary']['rejected_focus_count']}"],
        [f"tool_improvement_count={len(artifact['tool_improvement_queue'])}"],
        [f"negative_fixture_count={len(artifact['negative_fixtures'])}", f"unsupported_claim_count={artifact['unsupported_claim_count']}"],
        [f"average_project_telos_score_lift={artifact['route_summary']['average_project_telos_score_lift']:.6f}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0072 Domain Focus Adapter Experiment", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0072 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "DOMAIN_FOCUS_ADAPTER_EXPERIMENT_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
