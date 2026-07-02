"""Generate pass 0067 receipts for the Forum routing repair experiment."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_forum_routing_repair_experiment.py"
TEST_SCRIPT = ROOT / "tools" / "test_forum_routing_repair_experiment.py"
OUT_PATH = ROOT / "schemas" / "forum-routing-repair-experiment-pass-0067.json"
PACKET_PATH = ROOT / "packets" / "077-forum-routing-repair-experiment.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0067-forum-routing-repair-experiment-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0067-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0067-measurements.json"


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


def render_packet(packet: dict, compose_receipt: dict, test_receipt: dict) -> str:
    probes = "\n".join(f"- `{row['probe_id']}`: decided `{row['decided']}`, escalation `{row['needs_escalation']}`, project-telos score `{row['project_telos_score']}`" for row in packet["route_probes"])
    return f"""# Packet 077: Forum Routing Repair Experiment

Date: 2026-07-01

Status: `{packet['status']}`

Purpose: promote the pass 0066 `routing_repair_spine` growth vector into a live route-probe experiment.

```text
baseline_project_telos_score = {packet['repair_metrics']['baseline_project_telos_score']}
best_repaired_project_telos_score = {packet['repair_metrics']['best_repaired_project_telos_score']}
project_telos_score_lift = {packet['repair_metrics']['project_telos_score_lift']}
repaired_no_escalation_count = {packet['repair_metrics']['repaired_no_escalation_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Route Probes

{probes}

Current promoted natural laws: none.
"""


def render_steelman(packet: dict) -> str:
    return f"""# Pass 0067 Steelman: Forum Routing Repair Experiment

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass proves prompt-shaping can avoid escalation for two sampled prompts.
It does not modify Forum source code, prove routing robustness for all broad
cross-domain prompts, or eliminate the need for a real router vocabulary patch.

Non-promotion statement: {packet['non_promotion_statement']}
"""


def build_thesis_measurements(packet: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {"artifact": sha256_file(OUT_PATH), "composer": sha256_file(COMPOSER), "packet": sha256_file(PACKET_PATH), "steelman": sha256_file(STEELMAN_PATH), "test": sha256_file(TEST_SCRIPT)}
    metrics = packet["repair_metrics"]
    claims = [
        f"Pass 0067 created a ForumRoutingRepairExperiment/v1 artifact with status {packet['status']}, sha256 {shas['artifact']}, and seal {packet['seal']}.",
        f"Pass 0067 route probes count is {len(packet['route_probes'])} with baseline needs_escalation {packet['route_probes'][0]['needs_escalation']}.",
        f"Pass 0067 repaired prompts route to project-telos with repaired_no_escalation_count {metrics['repaired_no_escalation_count']}.",
        f"Pass 0067 project_telos_score_lift is {metrics['project_telos_score_lift']} from baseline {metrics['baseline_project_telos_score']} to best repaired {metrics['best_repaired_project_telos_score']}.",
        f"Pass 0067 repair rule requires prefix {packet['repair_rule']['required_prefix']} and tool chain {','.join(packet['repair_rule']['required_tool_chain'])}.",
        f"Pass 0067 binds previous pass {packet['previous_pass_binding']['pass']} with sha256 {packet['previous_pass_binding']['sha256']}.",
        f"Pass 0067 composer sha256 is {shas['composer']} and compose_receipt status is {compose_receipt['status']}.",
        f"Pass 0067 packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={packet['schema']}", f"status={packet['status']}", f"sha256={shas['artifact']}", f"seal={packet['seal']}"],
        [f"probe_count={len(packet['route_probes'])}", f"baseline_needs_escalation={packet['route_probes'][0]['needs_escalation']}"],
        [f"repaired_no_escalation_count={metrics['repaired_no_escalation_count']}", "decided=project-telos"],
        [f"project_telos_score_lift={metrics['project_telos_score_lift']}", f"baseline={metrics['baseline_project_telos_score']}", f"best={metrics['best_repaired_project_telos_score']}"],
        [f"prefix={packet['repair_rule']['required_prefix']}", ",".join(packet["repair_rule"]["required_tool_chain"])],
        [f"previous_pass={packet['previous_pass_binding']['pass']}", f"previous_sha256={packet['previous_pass_binding']['sha256']}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
    ]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0067 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0067 Forum Routing Repair Experiment"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": "artifact-review", "tolerance": 0.5} for i, claim in enumerate(claims)]}
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
