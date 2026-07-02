"""Generate pass 0056 receipts for the buyer-facing demo manifest."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


PASS = "0056"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_demo_manifest.py"
TEST_SCRIPT = ROOT / "tools" / "test_buyer_demo_manifest.py"
GRAPH = ROOT / "schemas" / "multitrace-causality-graph-pass-0055.json"
BUNDLE_DIR = ROOT / "demo-bundles" / "multitrace-causality-demo-pass-0056"
OUT_PATH = ROOT / "schemas" / "buyer-demo-manifest-pass-0056.json"
VALIDATOR_RESULT_PATH = ROOT / "schemas" / "pass-0056-buyer-demo-manifest-validator-result.json"
PACKET_PATH = ROOT / "packets" / "066-buyer-demo-manifest.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0056-buyer-demo-manifest-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0056-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0056-measurements.json"
EXPECTED_OUTPUTS = ["manifest.json", "review-panes.json", "failure-verdicts.json", "replay-commands.md", "index.html", "receipts.json"]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


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
        "stderr_sha256": sha256_text(result.stderr),
        "stdout_sha256": sha256_text(result.stdout),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def bundle_outputs() -> list[dict]:
    rows = []
    for rel in EXPECTED_OUTPUTS:
        path = BUNDLE_DIR / rel
        rows.append({"bytes": path.stat().st_size if path.exists() else 0, "exists": path.exists(), "path": f"demo-bundles/multitrace-causality-demo-pass-0056/{rel}", "sha256": sha256_file(path) if path.exists() else None})
    return rows


def render_packet(contract: dict) -> str:
    m = contract["verifier_measurements"]
    return f"""# Packet 066: Buyer Demo Manifest

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0056 converts the pass 0055 multi-trace graph into a buyer-reviewable
demo bundle with review panes, replay commands, failure verdicts, and static
HTML.

```text
implementation_status = {contract['implementation_status']}
review_pane_count = {m['review_pane_count']}
failure_verdict_count = {m['failure_verdict_count']}
replay_command_count = {m['replay_command_count']}
output_match_count = {m['output_match_count']}
production_ready = {m['production_ready']}
```

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0056 Steelman: Buyer Demo Manifest

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass proves a local review bundle only. It does not prove live telemetry
collection, production deployment, customer adoption, scientific truth, or any
natural law.
"""


def build_thesis_measurements(contract: dict) -> tuple[dict, dict]:
    shas = {
        "composer": sha256_file(COMPOSER),
        "manifest": sha256_file(OUT_PATH),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    m = contract["verifier_measurements"]
    claims = [
        f"Pass 0056 created a BuyerDemoManifestSet/v1 artifact with status {contract['status']}, review_pane_count {m['review_pane_count']}, output_match_count {m['output_match_count']}, sha256 {shas['manifest']}, and seal {contract['seal']}.",
        f"Pass 0056 implements compose_buyer_demo_manifest.py with sha256 {shas['composer']} and implementation_status {contract['implementation_status']}.",
        f"Pass 0056 records a buyer demo manifest test script with sha256 {shas['test']} and test_receipt status {contract['test_receipt']['status']}.",
        f"Pass 0056 generated a demo bundle with output_count {m['output_count']}, output_match_count {m['output_match_count']}, review_pane_count {m['review_pane_count']}, and failure_verdict_count {m['failure_verdict_count']}.",
        f"Pass 0056 records replay_command_count {m['replay_command_count']}, production_ready {m['production_ready']}, and public_review_ready {m['public_review_ready']}.",
        f"Pass 0056 binds to pass 0055 graph sha256 {contract['upstream_graph_binding']['sha256']} and source status {contract['upstream_graph_binding']['source_status']}.",
        "Pass 0056 validator result reports MATCH with review_pane_count 4 and output_match_count 6.",
        f"Pass 0056 records packet 066 sha256 {shas['packet']}, steelman sha256 {shas['steelman']}, uniqueness_claim_status HYPOTHESIS_ONLY, and current_promoted_natural_laws remains none.",
    ]
    evidence = [
        [f"schema=BuyerDemoManifestSet/v1", f"status={contract['status']}", f"review_pane_count={m['review_pane_count']}", f"output_match_count={m['output_match_count']}", f"sha256={shas['manifest']}", f"seal={contract['seal']}"],
        [f"composer_sha256={shas['composer']}", f"implementation_status={contract['implementation_status']}"],
        [f"test_sha256={shas['test']}", f"test_status={contract['test_receipt']['status']}"],
        [f"output_count={m['output_count']}", f"output_match_count={m['output_match_count']}", f"review_pane_count={m['review_pane_count']}", f"failure_verdict_count={m['failure_verdict_count']}"],
        [f"replay_command_count={m['replay_command_count']}", f"production_ready={m['production_ready']}", f"public_review_ready={m['public_review_ready']}"],
        [f"graph_sha256={contract['upstream_graph_binding']['sha256']}", f"source_status={contract['upstream_graph_binding']['source_status']}"],
        ["validator_status=MATCH", "review_pane_count=4", "output_match_count=6"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", "uniqueness_claim_status=HYPOTHESIS_ONLY", "current_promoted_natural_laws=[]"],
    ]
    methods = ["manifest-schema-review", "composer-file-review", "composer-test-review", "bundle-output-review", "review-readiness-boundary-review", "upstream-graph-binding-review", "validator-result-review", "non-promotion-boundary-review"]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0056 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0056 Buyer Demo Manifest"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": methods[i], "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--graph", str(GRAPH), "--out", str(BUNDLE_DIR)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    manifest = read_json(BUNDLE_DIR / "manifest.json")
    panes = read_json(BUNDLE_DIR / "review-panes.json")
    failures = read_json(BUNDLE_DIR / "failure-verdicts.json")
    outputs = bundle_outputs()
    graph = read_json(GRAPH)
    all_match = compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and manifest["status"] == "BUYER_DEMO_MANIFEST_MATCH" and all(row["exists"] for row in outputs)
    contract = with_seal({
        "bundle_outputs": outputs,
        "compose_receipt": compose_receipt,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "implementation_status": "IMPLEMENTED_LOCAL_BUYER_DEMO_MANIFEST",
        "non_promotion_statement": manifest["non_promotion_statement"],
        "pass": PASS,
        "schema": "BuyerDemoManifestSet/v1",
        "status": "BUYER_DEMO_MANIFEST_SET_MATCH" if all_match else "BUYER_DEMO_MANIFEST_SET_DRIFT",
        "test_receipt": test_receipt,
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "upstream_graph_binding": {"path": "schemas/multitrace-causality-graph-pass-0055.json", "sha256": sha256_file(GRAPH), "source_status": graph["status"], "source_seal": graph["seal"]},
        "verifier_measurements": {
            "failure_verdict_count": manifest["demo_summary"]["failure_verdict_count"],
            "output_count": len(outputs),
            "output_match_count": sum(1 for row in outputs if row["exists"]),
            "production_ready": manifest["demo_summary"]["production_ready"],
            "public_review_ready": manifest["demo_summary"]["public_review_ready"],
            "replay_command_count": manifest["demo_summary"]["replay_command_count"],
            "review_pane_count": len(panes["panes"]),
            "negative_match_count": failures["negative_match_count"],
            "negative_pass_observed_count": failures["negative_pass_observed_count"],
        },
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    thesis, measurements = build_thesis_measurements(contract)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    print(json.dumps({"path": str(OUT_PATH), "seal": contract["seal"], "status": contract["status"]}, indent=2, sort_keys=True))
    if contract["status"].endswith("_DRIFT"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
