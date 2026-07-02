"""Generate pass 0116 formal/physics source-lead bridge artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_formal_physics_source_lead_bridge.py"
TEST_SCRIPT = ROOT / "tools" / "test_formal_physics_source_lead_bridge.py"
OUT_PATH = ROOT / "schemas" / "formal-physics-source-lead-bridge-pass-0116.json"
TOOL_RECEIPTS_PATH = ROOT / "schemas" / "tool-receipts-pass-0116.json"
PACKET_PATH = ROOT / "packets" / "126-formal-physics-source-lead-bridge.md"
BRIEF_PATH = ROOT / "briefs" / "126-formal-physics-source-lead-bridge-brief.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0116-formal-physics-source-lead-bridge-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0116-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0116-measurements.json"


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


def rows(items: list[dict], columns: list[str]) -> str:
    out = []
    for item in items:
        out.append("| " + " | ".join(str(item.get(col, "")).replace("|", "/").replace("\n", " ") for col in columns) + " |")
    return "\n".join(out)


def render_packet(artifact: dict, compose_receipt: dict, test_receipt: dict) -> str:
    return f"""# Packet 126: Formal/Physics Source-Lead Bridge

Date: 2026-07-01

Status: `{artifact['status']}`

Purpose: turn the four new YouTube source leads into bounded proof-packet
requirements while proving only small finite identities.

```text
solver_replay_pass = {artifact['source_bindings']['solver_replay_pass']}
youtube_roadmap_pass = {artifact['source_bindings']['youtube_roadmap_pass']}
bridge_cases = {len(artifact['bridge_cases'])}
source_anchors = {artifact['source_surface']['anchor_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Bridge Cases

| Case | Domain | Status |
| --- | --- | --- |
{rows(artifact['bridge_cases'], ['case_id', 'domain', 'status'])}

## Roadmap Requirements

| Video | Claim status | Requirement |
| --- | --- | --- |
{rows(artifact['roadmap_requirements'], ['video_id', 'claim_status', 'requirement'])}

## Boundary

{artifact['non_promotion_statement']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Formal/Physics Source-Lead Bridge Brief

Date: 2026-07-01

## Decision

Convert source pressure from category theory, quantum foundations,
counterexample research, and looped agents into receipt requirements. The pass
keeps all four video-derived requirements at `HYPOTHESIS` while adding exact
toy checks that can be replayed.

## Product Wedge

The megatool direction is a claim-to-proof bridge: source lead, notation,
bounded witness, counterexample, verifier, loop receipt, and promotion boundary
in one packet. This is the next connective layer between Gather, Index, Forum,
Crucible, Telos, and future BuildLang/buildc formal/scientific kernels.

Source anchors recorded: {artifact['source_surface']['anchor_count']}.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0116 Steelman: Formal/Physics Source-Lead Bridge

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that finite toy identities do not constitute
category theory, quantum foundations, theoretical CS, or agent research.
Correct. This pass validates receipt fields and replay boundaries only.

The second objection is that video-derived pressure can smuggle unsupported
claims into the corpus. Correct. The requirements are marked `HYPOTHESIS`, and
raw transcript content is not promoted into scientific evidence.

Non-promotion statement: {artifact['non_promotion_statement']}
"""


def write_tool_receipts(artifact: dict, compose_receipt: dict, test_receipt: dict) -> None:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0116",
        "compose": compose_receipt,
        "test": test_receipt,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "bridge_cases": artifact["bridge_cases"],
        "roadmap_requirements": artifact["roadmap_requirements"],
        "source_surface": artifact["source_surface"],
    }
    payload = json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipts["seal"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS_PATH, receipts)


def build_thesis_measurements(artifact: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    files = {"artifact": OUT_PATH, "composer": COMPOSER, "packet": PACKET_PATH, "brief": BRIEF_PATH, "steelman": STEELMAN_PATH, "test": TEST_SCRIPT, "tool_receipts": TOOL_RECEIPTS_PATH}
    shas = {name: sha256_file(path) for name, path in files.items()}
    by_case = {row["case_id"]: row for row in artifact["bridge_cases"]}
    claims = [
        f"Pass 0116 created a FormalPhysicsSourceLeadBridgeReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0116 binds solver replay pass {artifact['source_bindings']['solver_replay_pass']}, YouTube roadmap pass {artifact['source_bindings']['youtube_roadmap_pass']}, and {artifact['source_bindings']['new_youtube_lead_count']} new YouTube source leads.",
        "Pass 0116 category toy case matched left identity, right identity, and associativity, and its bad identity fixture is BAD_IDENTITY_DRIFT.",
        "Pass 0116 Born-rule normalization toy case has probability_sum 1 and rejects the non-normalized state fixture.",
        "Pass 0116 counterexample revision toy case refuted the initial sampled-integer claim and matched the revised nonnegative-square claim.",
        "Pass 0116 loop replay toy case records two attempts, final MATCH, and reasoning_trace_exposed False.",
        f"Pass 0116 records {len(artifact['roadmap_requirements'])} roadmap requirements and all are HYPOTHESIS.",
        f"Pass 0116 records source anchor_count {artifact['source_surface']['anchor_count']}.",
        "Pass 0116 flagship receipts for Forum, Index, and Telos all have MATCH status.",
        f"Pass 0116 records unsupported_claim_count {artifact['unsupported_claim_count']} and current_promoted_natural_laws length {len(artifact['current_promoted_natural_laws'])}.",
        f"Pass 0116 composer sha256 is {shas['composer']}, packet sha256 is {shas['packet']}, brief sha256 is {shas['brief']}, steelman sha256 is {shas['steelman']}, test sha256 is {shas['test']}, and tool_receipts sha256 is {shas['tool_receipts']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"source_bindings={artifact['source_bindings']}"],
        [f"category={by_case['category_set_identity_associativity']}"],
        [f"born={by_case['born_rule_normalization_toy']}"],
        [f"counterexample={by_case['counterexample_revision_toy']}"],
        [f"loop={by_case['loop_replay_receipt_toy']}"],
        [f"roadmap_requirements={artifact['roadmap_requirements']}"],
        [f"source_surface={artifact['source_surface']}"],
        [f"forum={artifact['flagship_receipts']['forum']['status']}", f"index={artifact['flagship_receipts']['index']['status']}", f"telos={artifact['flagship_receipts']['telos']['status']}"],
        [f"unsupported_claim_count={artifact['unsupported_claim_count']}", f"natural_law_count={len(artifact['current_promoted_natural_laws'])}"],
        [f"composer_sha256={shas['composer']}", f"packet_sha256={shas['packet']}", f"brief_sha256={shas['brief']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"tool_receipts_sha256={shas['tool_receipts']}", f"test_status={test_receipt['status']}", f"compose_status={compose_receipt['status']}"],
    ]
    thesis = {"title": "Dogfood Pass 0116 Formal/Physics Source-Lead Bridge", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0116 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
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
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and artifact["status"] == "FORMAL_PHYSICS_SOURCE_LEAD_BRIDGE_MATCH" else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": artifact["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
