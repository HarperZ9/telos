"""Compose pass 0077 path-selector contract and growth scorecard."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "PathSelectorContractGrowthScorecard/v1"
PASS_ID = "0077"
STATUS_MATCH = "PATH_SELECTOR_CONTRACT_SCORECARD_MATCH"
STATUS_DRIFT = "PATH_SELECTOR_CONTRACT_SCORECARD_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = {
    "urgency": 0.18,
    "buyer_budget": 0.14,
    "proof_advantage": 0.2,
    "demo_readiness": 0.2,
    "adoption_ease": 0.1,
    "integration_readiness": 0.1,
    "strategic_upside": 0.08,
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def evidence_ref(path: str, description: str) -> dict[str, Any]:
    full = ROOT / path
    data = read_json(full)
    return {
        "path": f"docs/research/dogfood/{path}",
        "schema": data.get("schema"),
        "status": data.get("status", "UNLABELED"),
        "sha256": sha256_file(full),
        "description": description,
    }


def weighted_score(scores: dict[str, int]) -> float:
    return round(sum(scores[name] * weight for name, weight in WEIGHTS.items()), 2)


def score_row(row_id: str, label: str, scores: dict[str, int], evidence: list[str], rationale: str, risk: str) -> dict[str, Any]:
    return {
        "id": row_id,
        "label": label,
        "scores": scores,
        "weighted_score": weighted_score(scores),
        "evidence_paths": evidence,
        "rationale": rationale,
        "primary_risk": risk,
        "uniqueness_status": "hypothesis",
    }


def contract() -> dict[str, Any]:
    return {
        "schema": "IndexPathSelectorReceipt/v1",
        "purpose": "Produce source-ref-only context receipts for explicit path selectors under a workspace root.",
        "required_fields": [
            "root",
            "selectors",
            "selector_results",
            "source_refs",
            "graph_pack_sha256",
            "freshness_root_sha256",
            "raw_source_included",
            "source_refs_only",
            "missing_selector_rejections",
            "join_key",
        ],
        "acceptance_rules": [
            "Existing directory selectors produce source refs with path, repo, sha256, and expansion handle.",
            "Missing selectors produce explicit REJECT entries, not silent omissions.",
            "Receipts include graph and freshness hashes for the selected path manifest.",
            "Raw private payload is not included; downstream tools expand refs locally.",
            "The receipt can replace or refine a Telos domain-envelope workspace_context layer.",
        ],
        "negative_rules": [
            "Do not treat repo-root context as path-scoped context.",
            "Do not promote missing paths such as build-universe as covered.",
            "Do not call the bridge implemented until Index emits the receipt natively or an adapter emits equivalent receipts.",
        ],
    }


def growth_vectors() -> list[dict[str, Any]]:
    return [
        {
            "vector": "path_scoped_source_ref_receipts",
            "why": "Large monorepos and scientific codebases need proof packets around selected subsystems, not only repo roots.",
            "unlocks": ["BuildLang domain packets", "color/rendering packets", "AI4Science source packets"],
            "next_experiment": "Emit an IndexPathSelectorReceipt fixture for buildlang and compiler, while rejecting build-universe.",
        },
        {
            "vector": "proof_packet_builder_cli",
            "why": "The research surface needs one command that joins Gather source, Index context, Forum route, action receipts, and Crucible verdicts.",
            "unlocks": ["public demos", "buyer pilots", "repeatable packet generation"],
            "next_experiment": "Define a telos proof build command over one existing packet and one BuildLang receipt.",
        },
        {
            "vector": "negative_fixture_market_positioning",
            "why": "Buyers trust systems that refuse overclaims; repeated REJECT fixtures are a product asset, not internal ceremony.",
            "unlocks": ["regulated AI ops", "scientific reproducibility", "compiler/runtime credibility"],
            "next_experiment": "Expose rejected claims alongside MATCH claims in a public-safe proof packet viewer.",
        },
        {
            "vector": "visual_truth_foundry",
            "why": "Color, rendering, display, and perception evidence is under-integrated with AI and research proof systems.",
            "unlocks": ["color calibration proof kits", "scientific visualization packets", "UI/browser evidence"],
            "next_experiment": "Recheck the pass 0011 Build Color proof kit through the same path-selector contract shape.",
        },
        {
            "vector": "ai4science_claim_ledger",
            "why": "AI4Science tools generate claims across literature, model runs, proof attempts, and experiments; the market gap is claim-level verification continuity.",
            "unlocks": ["pipeline-math++ packets", "formal math forge", "biology evidence packets"],
            "next_experiment": "Bind one AI4Science source map row to a claim packet with explicit unverified boundaries.",
        },
    ]


def product_motions() -> list[dict[str, Any]]:
    rows = [
        score_row(
            "buildlang_proof_packets",
            "BuildLang/buildc proof packets",
            {"urgency": 4, "buyer_budget": 4, "proof_advantage": 5, "demo_readiness": 5, "adoption_ease": 3, "integration_readiness": 4, "strategic_upside": 5},
            [
                "schemas/buildlang-source-ref-receipt-pass-0074.json",
                "schemas/buildlang-domain-envelope-join-pass-0075.json",
                "schemas/buildlang-index-focus-bridge-pass-0076.json",
            ],
            "Best near-term proof surface: live buildc corpus receipt, domain-envelope join, and a crisp path-selector gap.",
            "Compiler ecosystem adoption is hard; the first wedge must sell accountability, not broad Julia replacement.",
        ),
        score_row(
            "visual_truth_packets",
            "Color/rendering measurement packets",
            {"urgency": 3, "buyer_budget": 3, "proof_advantage": 5, "demo_readiness": 4, "adoption_ease": 4, "integration_readiness": 4, "strategic_upside": 4},
            [
                "schemas/build-color-calibration-proof-kit-pass-0011.json",
                "schemas/color-calibration-market-map-pass-0011.json",
                "schemas/competitor-proof-gap-matrix-pass-0048.json",
            ],
            "Distinctive trust layer with bounded software metrics and clear non-hardware-calibration boundaries.",
            "Hardware calibration claims need sensor-backed receipts before promotion.",
        ),
        score_row(
            "ai4science_research_packets",
            "AI4Science research proof packets",
            {"urgency": 5, "buyer_budget": 4, "proof_advantage": 5, "demo_readiness": 3, "adoption_ease": 2, "integration_readiness": 3, "strategic_upside": 5},
            [
                "schemas/ai4science-frontier-map-pass-0008.json",
                "schemas/ai4science-proof-market-sources-pass-0047.json",
                "schemas/competitor-proof-gap-matrix-pass-0048.json",
            ],
            "Highest mission upside and strong market need, but independent domain validation remains harder than compiler/color demos.",
            "A research packet that cannot satisfy domain reviewers becomes ceremony; start with formal/math sources before wet-lab claims.",
        ),
    ]
    return sorted(rows, key=lambda row: row["weighted_score"], reverse=True)


def compose() -> dict[str, Any]:
    evidence = [
        evidence_ref("schemas/buildlang-source-ref-receipt-pass-0074.json", "BuildLang source refs and live buildc corpus receipt."),
        evidence_ref("schemas/buildlang-domain-envelope-join-pass-0075.json", "BuildLang source receipt joined into domain envelope."),
        evidence_ref("schemas/buildlang-index-focus-bridge-pass-0076.json", "Index focus bridge requirement from live path probes."),
        evidence_ref("schemas/build-color-calibration-proof-kit-pass-0011.json", "Build Color software proof kit with bounded metrics."),
        evidence_ref("schemas/color-calibration-market-map-pass-0011.json", "Color calibration and rendering market map."),
        evidence_ref("schemas/ai4science-proof-market-sources-pass-0047.json", "AI4Science source anchor set."),
        evidence_ref("schemas/competitor-proof-gap-matrix-pass-0048.json", "Three-track competitor proof-gap matrix."),
        evidence_ref("schemas/frontier-problem-to-proof-opportunity-map-pass-0063.json", "Frontier problem and megatool opportunity map."),
    ]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "contract": contract(),
        "weights": WEIGHTS,
        "evidence": evidence,
        "growth_vectors": growth_vectors(),
        "product_motions": product_motions(),
        "primary_30_day_push": {
            "motion": "buildlang_proof_packets",
            "hypothesis": "Ship the Index path-selector receipt and wrap the live buildc corpus receipt into a public BuildLang proof-packet demo first.",
            "reason": "It has the strongest current proof advantage and demo readiness while directly improving the shared substrate needed by color/rendering and AI4Science packets.",
        },
        "negative_fixtures": [
            {"fixture_id": "claims_index_path_selector_already_native", "expected_status": "REJECT"},
            {"fixture_id": "claims_market_uniqueness_as_fact", "expected_status": "REJECT"},
            {"fixture_id": "claims_ai4science_domain_validation_complete", "expected_status": "REJECT"},
            {"fixture_id": "claims_color_hardware_calibration_complete", "expected_status": "REJECT"},
            {"fixture_id": "claims_buildlang_julia_replacement_proven", "expected_status": "REJECT"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0077 defines a contract and ranked hypotheses. It does not implement Index path selection, prove market uniqueness, validate AI4Science discoveries, calibrate hardware, prove Julia replacement, or promote a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("contract", {}).get("schema") != "IndexPathSelectorReceipt/v1":
        errors.append("contract_schema")
    if len(artifact.get("evidence", [])) < 8:
        errors.append("evidence_count")
    if len(artifact.get("growth_vectors", [])) < 5:
        errors.append("growth_vector_count")
    motions = artifact.get("product_motions", [])
    if len(motions) != 3:
        errors.append("motion_count")
    if motions and motions[0].get("id") != artifact.get("primary_30_day_push", {}).get("motion"):
        errors.append("primary_push_not_top_ranked")
    if any(row.get("uniqueness_status") != "hypothesis" for row in motions):
        errors.append("uniqueness_status")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    if len(artifact.get("negative_fixtures", [])) < 5:
        errors.append("negative_fixture_count")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"out": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
