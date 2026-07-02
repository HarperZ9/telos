"""Generate pass 0052 agent action proof-packet composer build contract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


PASS = "0052"
ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PACKET = ROOT / "schemas" / "agent-action-proof-packet-negative-fixtures-pass-0051.json"
OUT_PATH = ROOT / "schemas" / "agent-action-packet-composer-build-contract-pass-0052.json"
FIXTURE_PATH = ROOT / "fixtures" / "agent-action-packet-composer-build-contract-pass-0052.json"
PACKET_PATH = ROOT / "packets" / "062-agent-action-packet-composer-build-contract.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0052-agent-action-packet-composer-build-contract-steelman.md"


INPUT_SCHEMAS = [
    ("source_refs", "required", "Gather/source URL, repo path, or local source-ref hashes"),
    ("workspace_context_ref", "required", "Index context envelope or graph-pack hash"),
    ("admission_record", "required", "Telos admission decision with action_intent_id"),
    ("action_receipt", "required", "Action receipt joined to admission action_intent_id"),
    ("browser_evidence_ref", "conditional", "Browser evidence when browser or page state is involved"),
    ("loop_ledger_entry", "required", "Loop ledger entry with sequence and chain continuity"),
    ("crucible_verdict", "required", "Crucible assessment or validator verdict"),
    ("redaction_status", "required", "Private-payload boundary and hash-only indicators"),
]

OUTPUT_ARTIFACTS = [
    ("packet.json", "canonical JSON proof packet"),
    ("packet.md", "human-readable buyer/reviewer packet"),
    ("receipts.json", "tool and validation receipts"),
    ("negative-fixture-report.json", "negative fixture verdict summary"),
    ("index.html", "static review page with no remote dependencies"),
    ("replay-commands.md", "local commands to re-run validators and Crucible"),
]

BUILD_GATES = [
    ("schema_gate", "all required input sections present"),
    ("linkage_gate", "admission action_intent_id matches action receipt action_intent_id"),
    ("ledger_gate", "ledger chain flag and hash refs are present"),
    ("redaction_gate", "raw private payload flag is false"),
    ("negative_fixture_gate", "pass 0051 negative fixtures fail as expected"),
    ("crucible_gate", "Crucible returns MATCH for bundled measurable claims"),
]

MILESTONES = [
    ("day_1_3", "write packet composer fixture loader and canonical JSON bundle writer"),
    ("day_4_7", "add markdown and static HTML exporters"),
    ("day_8_14", "add validator runner and negative fixture report"),
    ("day_15_21", "add trace import adapters for OpenTelemetry-style spans"),
    ("day_22_30", "ship public demo packet and buyer walkthrough"),
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def render_packet(contract: dict) -> str:
    return f"""# Packet 062: Agent Action Packet Composer Build Contract

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0052 defines the build contract for the first public demo composer.

```text
implementation_status = {contract['implementation_status']}
input_schema_count = {contract['verifier_measurements']['input_schema_count']}
output_artifact_count = {contract['verifier_measurements']['output_artifact_count']}
build_gate_count = {contract['verifier_measurements']['build_gate_count']}
milestone_count = {contract['verifier_measurements']['milestone_count']}
```

The proposed one-command runner is:

```text
{contract['one_command_runner']['command']}
```

This pass does not implement the runner. It defines the exact contract the
runner must satisfy before the public proof-packet demo can be claimed.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0052 Steelman: Agent Action Packet Composer Build Contract

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass is a build contract, not an implementation. It does not prove the
composer exists or that external trace imports work. The next implementation
pass must create executable code and make the negative fixtures fail under the
real runner, not only under the synthetic validator.
"""


def main() -> None:
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    fixture = with_seal({
        "build_gates": [{"id": gate_id, "criterion": criterion} for gate_id, criterion in BUILD_GATES],
        "generated_on": "2026-07-01",
        "input_schemas": [{"id": field, "mode": mode, "description": description} for field, mode, description in INPUT_SCHEMAS],
        "milestones": [{"id": day_range, "work": work} for day_range, work in MILESTONES],
        "output_artifacts": [{"path": path, "role": role} for path, role in OUTPUT_ARTIFACTS],
        "pass": PASS,
        "schema": "AgentActionPacketComposerBuildContractFixture/v1",
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "build_gates": fixture["build_gates"],
        "current_promoted_natural_laws": [],
        "fixture": {"path": "fixtures/agent-action-packet-composer-build-contract-pass-0052.json", "schema": fixture["schema"], "seal": fixture["seal"], "sha256": fixture_sha},
        "generated_on": "2026-07-01",
        "implementation_status": "CONTRACT_ONLY_NOT_IMPLEMENTED",
        "input_schemas": fixture["input_schemas"],
        "milestones": fixture["milestones"],
        "non_promotion_statement": "Pass 0052 is a build contract only. It does not prove the packet composer exists, product-market fit, buyer adoption, scientific truth, or any natural law.",
        "one_command_runner": {
            "command": "python docs/research/dogfood/tools/compose_agent_action_proof_packet_demo.py --fixture docs/research/dogfood/fixtures/agent-action-proof-packet-negative-fixtures-pass-0051.json --out docs/research/dogfood/demo-bundles/agent-action-proof-packet",
            "status": "proposed",
        },
        "output_artifacts": fixture["output_artifacts"],
        "pass": PASS,
        "previous_pass_binding": {"path": "schemas/agent-action-proof-packet-negative-fixtures-pass-0051.json", "seal": previous["seal"], "sha256": previous_sha, "source_status": previous["status"]},
        "schema": "AgentActionPacketComposerBuildContractSet/v1",
        "status": "AGENT_ACTION_PACKET_COMPOSER_BUILD_CONTRACT_MATCH",
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "verifier_measurements": {"build_gate_count": len(BUILD_GATES), "input_schema_count": len(INPUT_SCHEMAS), "milestone_count": len(MILESTONES), "output_artifact_count": len(OUTPUT_ARTIFACTS)},
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "implementation_status": contract["implementation_status"],
        "path": str(OUT_PATH),
        "seal": contract["seal"],
        "status": contract["status"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
