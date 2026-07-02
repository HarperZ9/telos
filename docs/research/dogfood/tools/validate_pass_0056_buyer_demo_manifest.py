"""Validate pass 0056 buyer demo manifest artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buyer-demo-manifest-pass-0056.json"
GRAPH = ROOT / "schemas" / "multitrace-causality-graph-pass-0055.json"
BUNDLE = ROOT / "demo-bundles" / "multitrace-causality-demo-pass-0056"
RESULT = ROOT / "schemas" / "pass-0056-buyer-demo-manifest-validator-result.json"
EXPECTED_OUTPUTS = ["manifest.json", "review-panes.json", "failure-verdicts.json", "replay-commands.md", "index.html", "receipts.json"]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    graph = read_json(GRAPH)
    manifest = read_json(BUNDLE / "manifest.json")
    panes = read_json(BUNDLE / "review-panes.json")
    failures = read_json(BUNDLE / "failure-verdicts.json")
    receipts = read_json(BUNDLE / "receipts.json")
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    if artifact.get("schema") != "BuyerDemoManifestSet/v1":
        errors.append("schema")
    if artifact.get("status") != "BUYER_DEMO_MANIFEST_SET_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if manifest.get("status") != "BUYER_DEMO_MANIFEST_MATCH":
        errors.append("manifest_status")
    if manifest.get("demo_summary", {}).get("review_pane_count") != 4:
        errors.append("review_pane_count")
    if manifest.get("demo_summary", {}).get("failure_verdict_count") != 5:
        errors.append("failure_verdict_count")
    if manifest.get("demo_summary", {}).get("public_review_ready") is not True:
        errors.append("public_review_ready")
    if manifest.get("demo_summary", {}).get("production_ready") is not False:
        errors.append("production_boundary")
    if len(panes.get("panes", [])) != 4:
        errors.append("pane_count")
    if failures.get("negative_match_count") != 5 or failures.get("negative_pass_observed_count") != 0:
        errors.append("failure_replay")
    if artifact.get("upstream_graph_binding", {}).get("sha256") != sha256_file(GRAPH):
        errors.append("graph_sha")
    if artifact.get("upstream_graph_binding", {}).get("source_seal") != graph.get("seal"):
        errors.append("graph_seal")
    if any(not (BUNDLE / rel).exists() for rel in EXPECTED_OUTPUTS):
        errors.append("outputs_missing")
    if len(receipts.get("outputs", [])) != 5 or receipts.get("status") != "MATCH":
        errors.append("receipts")
    if artifact.get("current_promoted_natural_laws") != [] or manifest.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0056BuyerDemoManifestValidatorRun/v1",
        "pass": "0056",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "BuyerDemoManifestSet",
                "errors": errors,
                "output_match_count": artifact.get("verifier_measurements", {}).get("output_match_count"),
                "path": "schemas/buyer-demo-manifest-pass-0056.json",
                "review_pane_count": manifest.get("demo_summary", {}).get("review_pane_count"),
                "status": status,
            }
        ],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
