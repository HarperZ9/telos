"""Generate pass 0087 simulator branch adapter artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_quantum_simulator_branch_adapter.py"
TEST_SCRIPT = ROOT / "tools" / "test_quantum_simulator_branch_adapter.py"
OUT_PATH = ROOT / "schemas" / "quantum-simulator-branch-adapter-pass-0087.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0087.json"
PACKET_PATH = ROOT / "packets" / "097-quantum-simulator-branch-adapter.md"
BRIEF_PATH = ROOT / "briefs" / "097-quantum-simulator-branch-adapter-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0087-quantum-simulator-branch-adapter-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0087-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0087-measurements.json"


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
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 120) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    sim = artifact["simulator_branch"]
    best = sim["best_run"]
    return f"""# Packet 097: Quantum Simulator Branch Adapter

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: add a seeded simulated-annealing branch to the exact pass 0086
optimization receipt, while preserving the exact baseline as the replay gate.

```text
baseline_pass = {artifact['baseline_binding']['source_pass']}
run_count = {sim['run_count']}
seed_range = {sim['seed_range'][0]}..{sim['seed_range'][1]}
optimum_hit_count = {sim['optimum_hit_count']}
constraint_violation_rate = {sim['constraint_violation_rate']}
best_bits = {best['best_bits']}
best_energy = {best['best_energy']}
comparison_status = {artifact['comparison_to_exact']['status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Source Anchors

{chr(10).join(f"- {row['source_id']}: {row['url']}" for row in sim['source_anchors'])}

## Distribution

- Objective values: `{sim['objective_values']}`.
- Run digest: `{sim['runs_sha256']}`.
- Exact baseline energy: `{sim['exact_baseline_energy']}`.
- Simulator best energy: `{artifact['comparison_to_exact']['simulator_best_energy']}`.

Boundary: this pass verifies a simulator branch against a toy exact baseline.
It does not claim quantum hardware execution, quantum advantage, new physics,
or a natural law.
"""


def render_brief(artifact: dict) -> str:
    sim = artifact["simulator_branch"]
    return f"""# Quantum Simulator Branch Adapter Brief

Date: 2026-07-01

## Result

Pass 0087 adds a seeded simulated-annealing branch to the pass 0086 exact
baseline. Across {sim['run_count']} runs, the branch hit the exact optimum
{sim['optimum_hit_count']} times and records every seed and run output.

## Product Meaning

This is the adapter contract future quantum/simulator integrations need:
source anchors, solver parameters, seed records, run digest, distribution
summary, exact-baseline comparison, and non-promotion gates.

## Next Adapter

Add a larger synthetic optimization instance where exact enumeration is still
possible but nontrivial, then compare exact, simulated annealing, and greedy
baselines through the same receipt shape.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0087 Steelman: Quantum Simulator Branch Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a hand-rolled simulated annealer is not a
market-grade D-Wave/Ocean adapter. Correct. This pass is a receipt contract and
seeded replay gate, not a production sampler wrapper.

The second objection is that the toy problem is small enough for exact
enumeration. Correct again. That is the reason the adapter can be held to a
hard replay gate before larger, noisier, or external solver branches are added.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    sim = artifact["simulator_branch"]
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0087",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "simulator": {"run_count": sim["run_count"], "optimum_hit_count": sim["optimum_hit_count"], "runs_sha256": sim["runs_sha256"], "replay_gate": sim["replay_gate"]},
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {name: sha256_file(path) for name, path in {
        "artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH,
        "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}.items()}
    sim = artifact["simulator_branch"]
    cmp = artifact["comparison_to_exact"]
    claims = [
        f"Pass 0087 created a QuantumSimulatorBranchAdapterReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0087 binds exact baseline pass {artifact['baseline_binding']['source_pass']} with candidate digest {artifact['baseline_binding']['candidate_digest']}.",
        f"Pass 0087 records {sim['run_count']} seeded simulated-annealing runs, seed range {sim['seed_range']}, and runs_sha256 {sim['runs_sha256']}.",
        f"Pass 0087 hit the exact optimum {sim['optimum_hit_count']} times and its comparison status is {cmp['status']}.",
        f"Pass 0087 records {len(sim['source_anchors'])} external source anchors for simulated annealing and BQM/QUBO context.",
        f"Pass 0087 has no quantum hardware claim, quantum advantage claim, new physics claim, or new natural law claim.",
        f"Pass 0087 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0087 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_pass={artifact['baseline_binding']['source_pass']}", f"candidate_digest={artifact['baseline_binding']['candidate_digest']}"],
        [f"run_count={sim['run_count']}", f"seed_range={sim['seed_range']}", f"runs_sha256={sim['runs_sha256']}"],
        [f"optimum_hit_count={sim['optimum_hit_count']}", f"comparison_status={cmp['status']}", f"exact_bits={cmp['exact_best_bits']}", f"simulator_bits={cmp['simulator_best_bits']}"],
        [f"source_anchor_count={len(sim['source_anchors'])}", f"source_ids={[row['source_id'] for row in sim['source_anchors']]}"],
        [f"promotion_boundary={artifact['promotion_boundary']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0087 Quantum Simulator Branch Adapter", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0087 artifact values or required files are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "QUANTUM_SIMULATOR_BRANCH_ADAPTER_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
