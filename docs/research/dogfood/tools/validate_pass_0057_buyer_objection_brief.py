"""Validate pass 0057 buyer-objection brief artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buyer-objection-brief-pass-0057.json"
RESULT = ROOT / "schemas" / "pass-0057-buyer-objection-brief-validator-result.json"
COMPOSER = ROOT / "tools" / "compose_buyer_objection_brief.py"
TEST_SCRIPT = ROOT / "tools" / "test_buyer_objection_brief.py"
PROBE = ROOT / "tools" / "probe_buyer_objection_brief.py"
PACKET = ROOT / "packets" / "067-buyer-objection-brief.md"
STEELMAN = ROOT / "adversarial" / "pass-0057-buyer-objection-brief-steelman.md"
REQUIRED_URLS = {
    "https://www.nist.gov/itl/ai-risk-management-framework",
    "https://opentelemetry.io/docs/concepts/signals/traces/",
    "https://docs.langchain.com/langsmith/observability",
    "https://langfuse.com/docs/observability/overview",
    "https://azure.microsoft.com/en-us/solutions/discovery",
}


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
    buyers = artifact.get("buyer_briefs", [])
    source_urls = {row.get("url") for row in artifact.get("source_anchors", [])}
    objection_count = sum(len(row.get("objections", [])) for row in buyers)
    if artifact.get("schema") != "BuyerObjectionBrief/v1":
        errors.append("schema")
    if artifact.get("status") != "BUYER_OBJECTION_BRIEF_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("buyer_brief_count") != 3 or len(buyers) != 3:
        errors.append("buyer_count")
    if {row.get("buyer_id") for row in buyers} != {"research_lab", "ai_infra", "regulated_agent"}:
        errors.append("buyer_ids")
    if objection_count < 9:
        errors.append("objection_count")
    if artifact.get("source_anchor_count") < 5 or not REQUIRED_URLS.issubset(source_urls):
        errors.append("source_urls")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if artifact.get("market_claim_boundary") != "HYPOTHESIS_ONLY":
        errors.append("market_claim_boundary")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    bindings = artifact.get("demo_bindings", {})
    if bindings.get("review_pane_count") != 4 or bindings.get("failure_verdict_count") != 5:
        errors.append("demo_counts")
    if bindings.get("public_review_ready") is not True or bindings.get("production_ready") is not False:
        errors.append("review_boundary")
    for buyer in buyers:
        if len(buyer.get("objections", [])) < 3:
            errors.append(f"{buyer.get('buyer_id')}_objection_count")
        for row in buyer.get("objections", []):
            if not row.get("evidence_refs") or not row.get("demo_refs"):
                errors.append(f"{row.get('objection_id')}_evidence")
            if "no_universal_uniqueness_claim" not in row.get("guardrails", []):
                errors.append(f"{row.get('objection_id')}_guardrail")
    for path, label in [(COMPOSER, "composer"), (TEST_SCRIPT, "test"), (PROBE, "probe"), (PACKET, "packet"), (STEELMAN, "steelman")]:
        if not path.exists():
            errors.append(f"{label}_missing")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0057BuyerObjectionBriefValidatorRun/v1",
        "pass": "0057",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "BuyerObjectionBrief",
                "buyer_brief_count": len(buyers),
                "errors": errors,
                "objection_count": objection_count,
                "path": "schemas/buyer-objection-brief-pass-0057.json",
                "source_anchor_count": artifact.get("source_anchor_count"),
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
