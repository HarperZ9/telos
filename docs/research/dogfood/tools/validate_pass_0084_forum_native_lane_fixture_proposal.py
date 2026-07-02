"""Validate pass 0084 Forum native lane-fixture proposal."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "forum-native-lane-fixture-proposal-pass-0084.json"
RESULT = ROOT / "schemas" / "pass-0084-forum-native-lane-fixture-proposal-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


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
    results = artifact.get("route_test_results", {})
    if artifact.get("schema") != "ForumNativeLaneFixtureProposal/v1":
        errors.append("schema")
    if artifact.get("status") != "FORUM_NATIVE_LANE_FIXTURE_PROPOSAL_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("upstream", {}).get("pass") != "0083":
        errors.append("upstream")
    if results.get("positive_match") != results.get("positive_count"):
        errors.append("positive_tests")
    if results.get("negative_match") != results.get("negative_count"):
        errors.append("negative_tests")
    if len(artifact.get("lane_fixtures", [])) < 8:
        errors.append("lane_fixtures")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0084ForumNativeLaneFixtureProposalValidatorRun/v1",
        "pass": "0084",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "ForumNativeLaneFixtureProposal",
            "errors": errors,
            "path": "schemas/forum-native-lane-fixture-proposal-pass-0084.json",
            "lane_fixture_count": len(artifact.get("lane_fixtures", [])),
            "positive_match": results.get("positive_match"),
            "negative_match": results.get("negative_match"),
            "status": status,
        }],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
