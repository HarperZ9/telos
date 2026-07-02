"""Generate pass 0053 receipts for the executable agent action packet composer."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


PASS = "0053"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PREVIOUS_PACKET = ROOT / "schemas" / "agent-action-packet-composer-build-contract-pass-0052.json"
FIXTURE_PATH = ROOT / "fixtures" / "agent-action-proof-packet-negative-fixtures-pass-0051.json"
BUNDLE_DIR = ROOT / "demo-bundles" / "agent-action-proof-packet-pass-0053"
COMPOSER = ROOT / "tools" / "compose_agent_action_proof_packet_demo.py"
TEST_SCRIPT = ROOT / "tools" / "test_agent_action_packet_composer_demo.py"
OUT_PATH = ROOT / "schemas" / "agent-action-packet-composer-implementation-pass-0053.json"
PACKET_PATH = ROOT / "packets" / "063-agent-action-packet-composer-implementation.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0053-agent-action-packet-composer-implementation-steelman.md"
EXPECTED_OUTPUTS = [
    "packet.json",
    "packet.md",
    "receipts.json",
    "negative-fixture-report.json",
    "index.html",
    "replay-commands.md",
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


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stderr_sha256": hashlib.sha256(result.stderr.encode("utf-8")).hexdigest(),
        "stdout_sha256": hashlib.sha256(result.stdout.encode("utf-8")).hexdigest(),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def bundle_outputs() -> list[dict]:
    rows = []
    for rel_path in EXPECTED_OUTPUTS:
        path = BUNDLE_DIR / rel_path
        rows.append({
            "bytes": path.stat().st_size if path.exists() else 0,
            "exists": path.exists(),
            "path": f"demo-bundles/agent-action-proof-packet-pass-0053/{rel_path}",
            "sha256": sha256_file(path) if path.exists() else None,
        })
    return rows


def render_packet(contract: dict) -> str:
    return f"""# Packet 063: Agent Action Packet Composer Implementation

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0053 implements the first executable local packet composer for the agent
action proof-packet demo.

```text
implementation_status = {contract['implementation_status']}
output_count = {contract['verifier_measurements']['output_count']}
output_match_count = {contract['verifier_measurements']['output_match_count']}
negative_fixture_count = {contract['verifier_measurements']['negative_fixture_count']}
negative_match_count = {contract['verifier_measurements']['negative_match_count']}
negative_pass_observed_count = {contract['verifier_measurements']['negative_pass_observed_count']}
test_status = {contract['test_receipt']['status']}
```

Bundle directory:

```text
docs/research/dogfood/demo-bundles/agent-action-proof-packet-pass-0053
```

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0053 Steelman: Agent Action Packet Composer Implementation

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This implementation proves a local synthetic demo bundle only. It does not yet
import real external traces, run a live browser action, publish a buyer-facing
site, or prove adoption. The next passes should connect real trace adapters and
domain demos.
"""


def main() -> None:
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    compose_command = [sys.executable, str(COMPOSER), "--fixture", str(FIXTURE_PATH), "--out", str(BUNDLE_DIR)]
    compose_receipt = run_command(compose_command)
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    packet = read_json(BUNDLE_DIR / "packet.json")
    negative = read_json(BUNDLE_DIR / "negative-fixture-report.json")
    receipts = read_json(BUNDLE_DIR / "receipts.json")
    outputs = bundle_outputs()
    all_outputs = all(row["exists"] for row in outputs)
    all_match = (
        compose_receipt["status"] == "MATCH"
        and test_receipt["status"] == "MATCH"
        and all_outputs
        and packet["verification"]["verdict"] == "MATCH"
        and negative["negative_match_count"] == 8
        and negative["negative_pass_observed_count"] == 0
        and receipts["status"] == "MATCH"
    )
    contract = with_seal({
        "bundle_outputs": outputs,
        "compose_receipt": compose_receipt,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "implementation_status": "IMPLEMENTED_LOCAL_DEMO_BUNDLE",
        "non_promotion_statement": "Pass 0053 proves a local synthetic packet composer bundle only. It does not prove real trace import, live browser execution, product-market fit, buyer adoption, scientific truth, or any natural law.",
        "pass": PASS,
        "previous_pass_binding": {"path": "schemas/agent-action-packet-composer-build-contract-pass-0052.json", "seal": previous["seal"], "sha256": previous_sha, "source_status": previous["status"]},
        "schema": "AgentActionPacketComposerImplementationSet/v1",
        "status": "AGENT_ACTION_PACKET_COMPOSER_IMPLEMENTATION_MATCH" if all_match else "AGENT_ACTION_PACKET_COMPOSER_IMPLEMENTATION_DRIFT",
        "test_receipt": test_receipt,
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "verifier_measurements": {
            "negative_fixture_count": negative["negative_fixture_count"],
            "negative_match_count": negative["negative_match_count"],
            "negative_pass_observed_count": negative["negative_pass_observed_count"],
            "output_count": len(outputs),
            "output_match_count": sum(1 for row in outputs if row["exists"]),
        },
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "implementation_status": contract["implementation_status"],
        "output_match_count": contract["verifier_measurements"]["output_match_count"],
        "path": str(OUT_PATH),
        "seal": contract["seal"],
        "status": contract["status"],
    }, indent=2, sort_keys=True))
    if contract["status"].endswith("_DRIFT"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
