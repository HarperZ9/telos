"""Validate pass 0029 executable research claim packet receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "research-claim-packet-pass-0029.json"
PUBLIC_SOURCE_PATH = ROOT / "fixtures" / "pipeline-math-source-receipt-pass-0029.json"
SOURCE_BINDING_PATH = ROOT / "schemas" / "source-evidence-binding-pass-0028.json"
RESULT_PATH = ROOT / "schemas" / "pass-0029-research-claim-packet-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = load_json(SCHEMA_PATH)
    public_source = load_json(PUBLIC_SOURCE_PATH)
    source_binding = load_json(SOURCE_BINDING_PATH)
    errors: list[str] = []

    require(data.get("schema") == "ResearchClaimPacket/v1", errors, "wrong schema")
    require(data.get("pass") == "0029", errors, "wrong pass")
    require(data.get("status") == "RESEARCH_CLAIM_PACKET_MATCH", errors, "wrong status")
    require(data.get("seal") == sha256_obj({key: value for key, value in data.items() if key != "seal"}), errors, "seal mismatch")

    public_receipt = data.get("public_source_receipt", {})
    require(public_receipt.get("path") == "fixtures/pipeline-math-source-receipt-pass-0029.json", errors, "wrong public source path")
    require(public_receipt.get("sha256") == sha256_file(PUBLIC_SOURCE_PATH), errors, "public source sha mismatch")
    require(public_receipt.get("seal") == public_source.get("seal"), errors, "public source seal mismatch")
    require(public_receipt.get("url") == public_source.get("url"), errors, "public source URL mismatch")
    require(public_receipt.get("verification_status") == "verified", errors, "public source not verified")
    require(public_receipt.get("confidence") == "high", errors, "public source confidence mismatch")
    require(public_source.get("seal") == sha256_obj({key: value for key, value in public_source.items() if key != "seal"}), errors, "public source self seal mismatch")
    require(public_source.get("raw_page_material_required_for_replay") is False, errors, "public source requires raw page material")
    require(len(public_source.get("evidence_locators", [])) == 3, errors, "wrong source locator count")

    prior = data.get("prior_source_evidence_binding", {})
    require(prior.get("path") == "schemas/source-evidence-binding-pass-0028.json", errors, "wrong prior binding path")
    require(prior.get("sha256") == sha256_file(SOURCE_BINDING_PATH), errors, "prior binding sha mismatch")
    require(prior.get("seal") == source_binding.get("seal"), errors, "prior seal mismatch")
    require(prior.get("schema") == "SourceEvidenceBindingSet/v1", errors, "wrong prior schema")
    require(prior.get("network_summary_verdict") == "UNVERIFIABLE", errors, "prior network verdict promoted")
    require(prior.get("console_summary_verdict") == "UNVERIFIABLE", errors, "prior console verdict promoted")

    proposal = data.get("action_receipt_proposal", {})
    require(proposal.get("schema") == "ActionReceiptResearchClaimProposal/v1", errors, "wrong proposal schema")
    require(proposal.get("event_type") == "research_claim_packet_created", errors, "wrong proposal event type")
    require(proposal.get("raw_source_material_required") is False, errors, "proposal raw source required")
    require(proposal.get("raw_browser_payload_required") is False, errors, "proposal raw browser required")
    require(proposal.get("model_reasoning_required_for_replay") is False, errors, "proposal requires model reasoning")
    require(f"sha256:{sha256_file(PUBLIC_SOURCE_PATH)}" in proposal.get("input_digests", []), errors, "proposal missing public source digest")
    require(f"sha256:{sha256_file(SOURCE_BINDING_PATH)}" in proposal.get("input_digests", []), errors, "proposal missing prior binding digest")
    require(proposal.get("verification", {}).get("verdict") == "MATCH", errors, "proposal verification mismatch")

    claims = data.get("claims", [])
    claim_ids = {claim.get("id") for claim in claims}
    required_claim_ids = {
        "rc_pipeline_math_scope",
        "rc_pipeline_math_prover_verifier",
        "rc_pipeline_math_lean_formalization",
        "rc_pipeline_math_proof_correctness",
        "rc_pipeline_math_future_currentness",
    }
    require(required_claim_ids == claim_ids, errors, "claim id set mismatch")
    verified_claims = [claim for claim in claims if claim.get("verification_status") == "verified"]
    unverifiable_claims = [claim for claim in claims if claim.get("verification_status") == "UNVERIFIABLE"]
    blocked_claims = [claim for claim in claims if claim.get("promotion_state") == "BLOCKED"]
    require(len(verified_claims) == 3, errors, "wrong verified claim count")
    require(len(unverifiable_claims) == 2, errors, "wrong unverifiable claim count")
    require(len(blocked_claims) == 2, errors, "wrong blocked claim count")
    for claim in verified_claims:
        require(claim.get("evidence_url") == public_source.get("url"), errors, f"verified claim missing source URL {claim.get('id')}")
        require(claim.get("evidence_receipt_sha256") == sha256_file(PUBLIC_SOURCE_PATH), errors, f"verified claim source sha mismatch {claim.get('id')}")
        require(claim.get("confidence") == "high", errors, f"verified claim confidence mismatch {claim.get('id')}")
        require(claim.get("promotion_state") == "SOURCE_VERIFIED", errors, f"verified claim promotion mismatch {claim.get('id')}")
    for claim in unverifiable_claims:
        require(claim.get("confidence") == "unknown", errors, f"unverifiable confidence mismatch {claim.get('id')}")
        require(claim.get("promotion_state") == "BLOCKED", errors, f"unverifiable not blocked {claim.get('id')}")
    correctness_claim = next((claim for claim in claims if claim.get("id") == "rc_pipeline_math_proof_correctness"), {})
    future_claim = next((claim for claim in claims if claim.get("id") == "rc_pipeline_math_future_currentness"), {})
    require(correctness_claim.get("verification_status") == "UNVERIFIABLE", errors, "proof correctness promoted")
    require(future_claim.get("verification_status") == "UNVERIFIABLE", errors, "future currentness promoted")

    measurements = data.get("verifier_measurements", {})
    require(measurements.get("schema") == "ResearchClaimVerifierMeasurements/v1", errors, "wrong measurements schema")
    require(measurements.get("claim_count") == len(claims), errors, "measurement claim count mismatch")
    require(measurements.get("verified_claim_count") == len(verified_claims), errors, "measurement verified count mismatch")
    require(measurements.get("unverifiable_claim_count") == len(unverifiable_claims), errors, "measurement unverifiable count mismatch")
    require(measurements.get("blocked_claim_count") == len(blocked_claims), errors, "measurement blocked count mismatch")
    require(measurements.get("unsupported_claim_promotion_rejected") is True, errors, "unsupported promotion not rejected")
    require(measurements.get("network_console_unverifiable_preserved") is True, errors, "network console gap not preserved")
    require(measurements.get("measurement_status") == "MATCH", errors, "measurement status mismatch")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 10, errors, "expected at least ten negatives")
    require(all(item.get("expected_validator_status") == "REJECT" for item in negatives), errors, "negative not rejected")
    required_negative_ids = {
        "negative-proof-correctness-promoted",
        "negative-future-currentness-promoted",
        "negative-broad-science-generalization",
        "negative-source-url-missing",
        "negative-source-receipt-sha-drift",
        "negative-pass-0028-binding-drift",
        "negative-unverifiable-network-promoted",
        "negative-unverifiable-console-promoted",
        "negative-action-receipt-proposal-missing",
        "negative-verifier-measurement-missing",
    }
    require(required_negative_ids == {item.get("fixture_id") for item in negatives}, errors, "negative id set mismatch")

    market = data.get("market_implication", {})
    require(market.get("uniqueness_status") == "hypothesis", errors, "uniqueness treated as fact")
    require("wedge_hypothesis" in market, errors, "missing wedge hypothesis")
    require(data.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    non_promotion = data.get("non_promotion_statement", "")
    require("does not prove" in non_promotion, errors, "missing non-promotion statement")

    result = {
        "schema": "Pass0029ResearchClaimPacketValidatorRun/v1",
        "pass": "0029",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "ResearchClaimPacket",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "claim_count": len(claims),
                "verified_claim_count": len(verified_claims),
                "unverifiable_claim_count": len(unverifiable_claims),
                "blocked_claim_count": len(blocked_claims),
                "negative_fixture_count": len(negatives),
                "public_source_sha256": public_receipt.get("sha256"),
                "prior_source_binding_sha256": prior.get("sha256"),
                "unsupported_claim_promotion_rejected": measurements.get("unsupported_claim_promotion_rejected"),
                "network_summary_verdict": prior.get("network_summary_verdict"),
                "console_summary_verdict": prior.get("console_summary_verdict"),
                "errors": errors,
            }
        ],
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
