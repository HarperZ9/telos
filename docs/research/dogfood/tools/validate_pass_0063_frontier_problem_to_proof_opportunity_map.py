"""Validate pass 0063 frontier problem-to-proof opportunity map."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "frontier-problem-to-proof-opportunity-map-pass-0063.json"
RESULT = ROOT / "schemas" / "pass-0063-frontier-problem-to-proof-opportunity-map-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    source_ids = {row.get("source_id") for row in artifact.get("source_anchors", [])}
    domain_ids = {row.get("domain_id") for row in artifact.get("opportunity_rows", [])}
    score_markets = {row.get("market") for row in artifact.get("wedge_scores", [])}
    nodes = {node.get("internal_tool") for node in artifact.get("megatool_nodes", [])}
    required_domains = {
        "formal_math_theoretical_cs",
        "agentic_ai4science",
        "quantum_hpc_algorithms",
        "biology_protein_drug_discovery",
        "materials_climate_energy",
        "buildlang_scientific_runtime",
        "agent_observability_action_receipts",
        "color_rendering_calibration",
    }
    required_nodes = {"Gather", "Index", "Forum", "Crucible", "Telos", "BuildLang/buildc", "build-universe", "color calibration", "browser evidence", "model foundry", "loop ledger", "action receipts"}
    if artifact.get("schema") != "FrontierProblemToProofOpportunityMap/v1":
        errors.append("schema")
    if artifact.get("status") != "FRONTIER_PROBLEM_TO_PROOF_OPPORTUNITY_MAP_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if len(source_ids) < 16:
        errors.append("source_anchor_count")
    if not required_domains.issubset(domain_ids):
        errors.append("required_domains")
    if score_markets != domain_ids:
        errors.append("score_markets")
    if not required_nodes.issubset(nodes):
        errors.append("required_nodes")
    if artifact.get("unsupported_uniqueness_claim_count") != 0:
        errors.append("unsupported_uniqueness_claim_count")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    if len(artifact.get("demo_recommendations", [])) != 3:
        errors.append("demo_recommendations")
    for row in artifact.get("opportunity_rows", []):
        if row.get("gap_status") not in {"verified", "inferred", "unverified"}:
            errors.append(f"gap_status:{row.get('domain_id')}")
        if row.get("uniqueness_claim_status") != "hypothesis":
            errors.append(f"uniqueness:{row.get('domain_id')}")
        if not set(row.get("source_ids", [])).issubset(source_ids):
            errors.append(f"sources:{row.get('domain_id')}")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0063FrontierProblemToProofOpportunityMapValidatorRun/v1",
        "pass": "0063",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "FrontierProblemToProofOpportunityMap",
                "domain_count": len(domain_ids),
                "errors": errors,
                "megatool_node_count": len(nodes),
                "path": "schemas/frontier-problem-to-proof-opportunity-map-pass-0063.json",
                "source_anchor_count": len(source_ids),
                "status": status,
                "top_ranked_market": artifact.get("wedge_scores", [{}])[0].get("market"),
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
