"""Validate pass 0058 Forum route-vocabulary bridge artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "forum-route-vocabulary-bridge-pass-0058.json"
BRIEF = ROOT / "schemas" / "buyer-objection-brief-pass-0057.json"
RESULT = ROOT / "schemas" / "pass-0058-forum-route-vocabulary-bridge-validator-result.json"
COMPOSER = ROOT / "tools" / "compose_forum_route_vocabulary_bridge.py"
TEST_SCRIPT = ROOT / "tools" / "test_forum_route_vocabulary_bridge.py"
PROBE = ROOT / "tools" / "probe_forum_route_vocabulary_bridge.py"
PACKET = ROOT / "packets" / "068-forum-route-vocabulary-bridge.md"
STEELMAN = ROOT / "adversarial" / "pass-0058-forum-route-vocabulary-bridge-steelman.md"
LANES = {"project-telos", "deep-research", "technical-writing"}


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
    brief = read_json(BRIEF)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    lane_ids = {row.get("lane_id") for row in artifact.get("lane_taxonomy", [])}
    script = artifact.get("buyer_discovery_script", {})
    if artifact.get("schema") != "ForumRouteVocabularyBridge/v1":
        errors.append("schema")
    if artifact.get("status") != "FORUM_ROUTE_VOCABULARY_BRIDGE_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if lane_ids != LANES:
        errors.append("lane_ids")
    if len(artifact.get("rewrite_fixtures", [])) < 5:
        errors.append("rewrite_count")
    if script.get("prompt_count") != 9 or script.get("source_objection_count") != 9:
        errors.append("discovery_counts")
    if artifact.get("observed_forum_gap", {}).get("status") != "ROUTE_ESCALATION_OBSERVED":
        errors.append("forum_gap")
    if artifact.get("upstream_brief", {}).get("seal") != brief.get("seal"):
        errors.append("upstream_brief_seal")
    if artifact.get("market_claim_boundary") != "HYPOTHESIS_ONLY":
        errors.append("market_boundary")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    if artifact.get("route_readiness", {}).get("ready_for_operator_use") is not True:
        errors.append("operator_ready")
    if artifact.get("route_readiness", {}).get("ready_for_forum_patch") is not False:
        errors.append("forum_patch_boundary")
    for path, label in [(COMPOSER, "composer"), (TEST_SCRIPT, "test"), (PROBE, "probe"), (PACKET, "packet"), (STEELMAN, "steelman")]:
        if not path.exists():
            errors.append(f"{label}_missing")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0058ForumRouteVocabularyBridgeValidatorRun/v1",
        "pass": "0058",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "ForumRouteVocabularyBridge",
                "errors": errors,
                "lane_count": len(lane_ids),
                "path": "schemas/forum-route-vocabulary-bridge-pass-0058.json",
                "prompt_count": script.get("prompt_count"),
                "rewrite_fixture_count": len(artifact.get("rewrite_fixtures", [])),
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
