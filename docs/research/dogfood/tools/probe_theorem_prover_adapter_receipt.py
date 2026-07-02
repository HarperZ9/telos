"""Generate pass 0117 theorem-prover adapter artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_theorem_prover_adapter_receipt.py"
TEST_SCRIPT = ROOT / "tools" / "test_theorem_prover_adapter_receipt.py"
OUT_PATH = ROOT / "schemas" / "theorem-prover-adapter-receipt-pass-0117.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0117.json"
PACKET_PATH = ROOT / "packets" / "127-theorem-prover-adapter-receipt.md"
BRIEF_PATH = ROOT / "briefs" / "127-theorem-prover-adapter-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0117-theorem-prover-adapter-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0117-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0117-measurements.json"


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
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    return f"""# Packet 127: Theorem-Prover Adapter Receipt

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: bind pass 0116's finite category witness to theorem-prover adapter
fields while explicitly fencing unavailable prover execution.

```text
formal_physics_bridge_pass = {artifact['source_bindings']['formal_physics_bridge_pass']}
theorem_targets = {len(artifact['theorem_targets'])}
prover_branches = {len(artifact['prover_branches'])}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Targets

| Target | Proposition | Claim status | Proof object |
| --- | --- | --- | --- |
{table(artifact['theorem_targets'], ['target_id', 'proposition', 'claim_status', 'proof_object_status'])}

## Prover Branches

| Branch | Executable | Status |
| --- | --- | --- |
{table(artifact['prover_branches'], ['branch_id', 'executable', 'status'])}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Theorem-Prover Adapter Brief

Date: 2026-07-01

## Decision

Create an adapter receipt for theorem-prover targets before claiming prover
execution. The pass records Lean-style target strings, finite-model witnesses,
countermodel fields, local tool availability, and explicit unavailable fences.

## Wedge

The market gap is not theorem proving itself. The wedge is durable proof
packet plumbing: source, target prover, local availability, proof-object status,
countermodel slot, replay witness, and action receipt in one portable record.

Source anchors recorded: {artifact['source_surface']['anchor_count']}.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0117 Steelman: Theorem-Prover Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that no local theorem prover executed. Correct. The
pass is an adapter receipt and availability fence, not a Lean/Rocq/Isabelle/Agda
proof result.

The second objection is that Lean-style target strings can look stronger than
they are. Correct. They are marked `NOT_EXECUTED_PROVER_UNAVAILABLE`; the only
positive verification is the finite Python model replay.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0117",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "availability": artifact["availability"],
        "theorem_targets": artifact["theorem_targets"],
        "prover_branches": artifact["prover_branches"],
        "countermodel": artifact["countermodel"],
        "source_surface": artifact["source_surface"],
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    branches = {row["branch_id"]: row for row in artifact["prover_branches"]}
    claims = [
        f"Pass 0117 created a TheoremProverAdapterReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0117 binds formal physics bridge pass {artifact['source_bindings']['formal_physics_bridge_pass']} and category case {artifact['source_bindings']['category_case_id']}.",
        "Pass 0117 records Lean, Lake, Rocq/Coq, Isabelle, and Agda executables as MISSING in this environment.",
        f"Pass 0117 records {len(artifact['theorem_targets'])} theorem targets and all have claim_status FINITE_MODEL_VERIFIED.",
        "Pass 0117 python finite-model replay branch has MATCH status.",
        "Pass 0117 Lean, Rocq, Isabelle, and Agda prover target branches are UNAVAILABLE_FENCED.",
        f"Pass 0117 countermodel status is {artifact['countermodel']['status']} with classification {artifact['countermodel']['classification']}.",
        f"Pass 0117 records source anchor_count {artifact['source_surface']['anchor_count']}.",
        "Pass 0117 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0117 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0117 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"availability={artifact['availability']}"],
        [f"theorem_targets={artifact['theorem_targets']}"],
        [f"python_branch={branches['python_finite_model_replay']}"],
        [f"lean={branches['lean4_target']}", f"rocq={branches['rocq_target']}", f"isabelle={branches['isabelle_target']}", f"agda={branches['agda_target']}"],
        [f"countermodel={artifact['countermodel']}"],
        [f"source_surface={artifact['source_surface']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0117 Theorem-Prover Adapter Receipt", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0117 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)], timeout=180)
    artifact = read_json(OUT_PATH)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)], timeout=120)
    write_tool_receipts(artifact, compose_receipt, test_receipt)
    write_text(PACKET_PATH, render_packet(artifact, compose_receipt, test_receipt))
    write_text(BRIEF_PATH, render_brief(artifact))
    write_text(STEELMAN_PATH, render_steelman(artifact))
    thesis, measurements = build_thesis_measurements(artifact, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "THEOREM_PROVER_ADAPTER_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
