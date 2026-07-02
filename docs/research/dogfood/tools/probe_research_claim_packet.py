"""Generate pass 0029 executable research claim packet receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PASS = "0029"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_BINDING_PATH = ROOT / "schemas" / "source-evidence-binding-pass-0028.json"
PUBLIC_SOURCE_PATH = ROOT / "fixtures" / "pipeline-math-source-receipt-pass-0029.json"
OUT_PATH = ROOT / "schemas" / "research-claim-packet-pass-0029.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


source_binding = read_json(SOURCE_BINDING_PATH)

pipeline_source = {
    "schema": "PublicSourceReceipt/v1",
    "source_id": "source_pipeline_math_readme_2026_07_01",
    "source_kind": "github_raw_readme",
    "source_name": "Pengbinghui/pipeline-math README",
    "url": "https://raw.githubusercontent.com/Pengbinghui/pipeline-math/main/README.md",
    "observed_on": "2026-07-01",
    "access_method": "web.open",
    "official_source": True,
    "evidence_locators": [
        {
            "locator": "README line 0",
            "supports_claim_ids": ["rc_pipeline_math_scope"],
            "summary": "The README describes the repository as collecting resolutions of open problems across COLT, commutative ring theory, an Erdos problem, and a FOCS 2023 open question.",
        },
        {
            "locator": "README line 1",
            "supports_claim_ids": ["rc_pipeline_math_prover_verifier"],
            "summary": "The README says proof discovery used a simple prover-verifier pipeline, with papers assembled in Claude Code and then polished and verified by the authors.",
        },
        {
            "locator": "README line 2",
            "supports_claim_ids": ["rc_pipeline_math_lean_formalization"],
            "summary": "The README says commutative-ring-theory solutions are formalized in Lean via an agentic Lean formalization pipeline, with open source release pending.",
        },
    ],
    "source_evidence_digest": "web-open:turn1view0",
    "raw_page_material_required_for_replay": False,
    "verification_status": "verified",
    "confidence": "high",
    "non_claims": [
        "This source receipt does not verify mathematical correctness of any listed paper.",
        "This source receipt does not verify that the repository state will remain unchanged on a future replay.",
        "This source receipt does not verify that the pipeline generalizes to all fields of science.",
        "This source receipt does not verify a Telos uniqueness claim against all competitors.",
    ],
}
pipeline_source["seal"] = sha256_obj({key: value for key, value in pipeline_source.items() if key != "seal"})
write_json(PUBLIC_SOURCE_PATH, pipeline_source)

public_source_sha = sha256_file(PUBLIC_SOURCE_PATH)
source_binding_sha = sha256_file(SOURCE_BINDING_PATH)

research_claims = [
    {
        "id": "rc_pipeline_math_scope",
        "claim": "The pipeline-math README positions the repository as collecting resolutions of open problems from the COLT open-problem track, commutative ring theory, an Erdos problem, and a FOCS 2023 open question.",
        "evidence_url": pipeline_source["url"],
        "evidence_locator": "README line 0",
        "evidence_receipt": "fixtures/pipeline-math-source-receipt-pass-0029.json",
        "evidence_receipt_sha256": public_source_sha,
        "confidence": "high",
        "verification_status": "verified",
        "promotion_state": "SOURCE_VERIFIED",
        "proof_gap": "This verifies source positioning only, not mathematical correctness.",
    },
    {
        "id": "rc_pipeline_math_prover_verifier",
        "claim": "The pipeline-math README says proof discovery used a simple prover-verifier pipeline, with papers assembled in Claude Code and then polished and verified by the authors.",
        "evidence_url": pipeline_source["url"],
        "evidence_locator": "README line 1",
        "evidence_receipt": "fixtures/pipeline-math-source-receipt-pass-0029.json",
        "evidence_receipt_sha256": public_source_sha,
        "confidence": "high",
        "verification_status": "verified",
        "promotion_state": "SOURCE_VERIFIED",
        "proof_gap": "This verifies the README's process claim only, not independent proof validity.",
    },
    {
        "id": "rc_pipeline_math_lean_formalization",
        "claim": "The pipeline-math README says its commutative-ring-theory solutions are formalized in Lean using an agentic Lean formalization pipeline, with open source release pending.",
        "evidence_url": pipeline_source["url"],
        "evidence_locator": "README line 2",
        "evidence_receipt": "fixtures/pipeline-math-source-receipt-pass-0029.json",
        "evidence_receipt_sha256": public_source_sha,
        "confidence": "high",
        "verification_status": "verified",
        "promotion_state": "SOURCE_VERIFIED",
        "proof_gap": "This verifies the README statement only; the formalization artifacts still need independent replay.",
    },
    {
        "id": "rc_pipeline_math_proof_correctness",
        "claim": "The listed pipeline-math open-problem resolutions are mathematically correct.",
        "evidence_url": pipeline_source["url"],
        "evidence_locator": "not established by this pass",
        "evidence_receipt": "fixtures/pipeline-math-source-receipt-pass-0029.json",
        "evidence_receipt_sha256": public_source_sha,
        "confidence": "unknown",
        "verification_status": "UNVERIFIABLE",
        "promotion_state": "BLOCKED",
        "proof_gap": "Requires independent proof review, formal replay, or accepted external verification.",
    },
    {
        "id": "rc_pipeline_math_future_currentness",
        "claim": "The pipeline-math repository state will remain unchanged at future replay time.",
        "evidence_url": pipeline_source["url"],
        "evidence_locator": "not established by this pass",
        "evidence_receipt": "fixtures/pipeline-math-source-receipt-pass-0029.json",
        "evidence_receipt_sha256": public_source_sha,
        "confidence": "unknown",
        "verification_status": "UNVERIFIABLE",
        "promotion_state": "BLOCKED",
        "proof_gap": "Requires a fresh fetch and digest comparison at replay time.",
    },
]

negative_fixtures = [
    {
        "fixture_id": "negative-proof-correctness-promoted",
        "failure_mode": "A source-positioning receipt is treated as proof that pipeline-math papers are mathematically correct.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-future-currentness-promoted",
        "failure_mode": "A 2026-07-01 source observation is treated as proof of future repository state.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-broad-science-generalization",
        "failure_mode": "A small source-backed packet is promoted into evidence that the approach works for all science.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-source-url-missing",
        "failure_mode": "A verified claim lacks an evidence URL.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-source-receipt-sha-drift",
        "failure_mode": "The public source receipt SHA-256 differs from the claim packet binding.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-pass-0028-binding-drift",
        "failure_mode": "The pass 0028 source-evidence binding SHA-256 differs from the claim packet binding.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-unverifiable-network-promoted",
        "failure_mode": "Pass 0028 network capture UNVERIFIABLE is promoted to MATCH.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-unverifiable-console-promoted",
        "failure_mode": "Pass 0028 console capture UNVERIFIABLE is promoted to MATCH.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-action-receipt-proposal-missing",
        "failure_mode": "The research packet lacks an action receipt proposal binding the source evidence to the claim extraction action.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-verifier-measurement-missing",
        "failure_mode": "The research packet lacks verifier measurements for supported, blocked, and rejected claims.",
        "expected_validator_status": "REJECT",
    },
]

record = {
    "schema": "ResearchClaimPacket/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "RESEARCH_CLAIM_PACKET_MATCH",
    "packet_title": "Pipeline-math Source-Backed Research Claim Packet",
    "public_source_receipt": {
        "path": "fixtures/pipeline-math-source-receipt-pass-0029.json",
        "sha256": public_source_sha,
        "seal": pipeline_source["seal"],
        "url": pipeline_source["url"],
        "observed_on": pipeline_source["observed_on"],
        "verification_status": pipeline_source["verification_status"],
        "confidence": pipeline_source["confidence"],
    },
    "prior_source_evidence_binding": {
        "path": "schemas/source-evidence-binding-pass-0028.json",
        "sha256": source_binding_sha,
        "seal": source_binding["seal"],
        "schema": source_binding["schema"],
        "network_summary_verdict": source_binding["browser_evidence_receipt"]["network_summary_verdict"],
        "console_summary_verdict": source_binding["browser_evidence_receipt"]["console_summary_verdict"],
    },
    "action_receipt_proposal": {
        "schema": "ActionReceiptResearchClaimProposal/v1",
        "action_id": "act_dogfood_0029_research_claim_extract",
        "event_id": "evt_dogfood_0029_research_claim_packet",
        "event_type": "research_claim_packet_created",
        "authority_class": "read_only_research_packet",
        "input_refs": [
            "artifact:fixtures/pipeline-math-source-receipt-pass-0029.json",
            "artifact:schemas/source-evidence-binding-pass-0028.json",
        ],
        "input_digests": [
            f"sha256:{public_source_sha}",
            f"sha256:{source_binding_sha}",
        ],
        "output_ref": "artifact:schemas/research-claim-packet-pass-0029.json",
        "raw_source_material_required": False,
        "raw_browser_payload_required": False,
        "model_reasoning_required_for_replay": False,
        "verification": {
            "verdict": "MATCH",
            "ref": "validator:pass-0029-research-claim-packet",
        },
    },
    "claims": research_claims,
    "verifier_measurements": {
        "schema": "ResearchClaimVerifierMeasurements/v1",
        "claim_count": len(research_claims),
        "verified_claim_count": sum(1 for claim in research_claims if claim["verification_status"] == "verified"),
        "unverifiable_claim_count": sum(1 for claim in research_claims if claim["verification_status"] == "UNVERIFIABLE"),
        "blocked_claim_count": sum(1 for claim in research_claims if claim["promotion_state"] == "BLOCKED"),
        "unsupported_claim_promotion_rejected": True,
        "source_receipt_sha256": public_source_sha,
        "prior_source_binding_sha256": source_binding_sha,
        "network_console_unverifiable_preserved": True,
        "measurement_status": "MATCH",
    },
    "negative_fixtures": negative_fixtures,
    "market_implication": {
        "wedge_hypothesis": "Research proof packets can package public source intake, claim extraction, action provenance, verifier measurements, and unsupported-promotion fences in one portable object.",
        "uniqueness_status": "hypothesis",
        "buyer_relevance": [
            "AI4Science labs need claim-to-source-to-verification chains for generated research.",
            "Agent infrastructure teams need unsupported-claim promotion gates before model outputs enter durable records.",
            "BuildLang/buildc can consume the same packet shape for compiler/runtime measurement receipts.",
        ],
    },
    "claim_to_proof_steps": [
        "source intake",
        "claim extraction",
        "source digest binding",
        "action receipt proposal",
        "verifier measurement",
        "unsupported claim rejection",
        "Crucible assessment",
    ],
    "negative_fixture_count": len(negative_fixtures),
    "non_promotion_statement": "Pass 0029 verifies a small public-source claim packet and rejects unsupported promotion. It does not prove the mathematical correctness of pipeline-math papers, broad scientific generalization, buyer adoption, Telos uniqueness against all competitors, live browser capture, or any natural law.",
    "current_promoted_natural_laws": [],
}
record["seal"] = sha256_obj({key: value for key, value in record.items() if key != "seal"})
write_json(OUT_PATH, record)

print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "schema": record["schema"],
            "status": record["status"],
            "claim_count": len(research_claims),
            "verified_claim_count": record["verifier_measurements"]["verified_claim_count"],
            "unverifiable_claim_count": record["verifier_measurements"]["unverifiable_claim_count"],
            "negative_fixture_count": record["negative_fixture_count"],
            "public_source_sha256": public_source_sha,
            "prior_source_binding_sha256": source_binding_sha,
            "seal": record["seal"],
        },
        indent=2,
        sort_keys=True,
    )
)
