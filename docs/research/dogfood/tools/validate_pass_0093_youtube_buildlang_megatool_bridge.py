"""Validate pass 0093 YouTube-to-BuildLang megatool bridge."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "youtube-buildlang-megatool-bridge-pass-0093.json"
RESULT = ROOT / "schemas" / "pass-0093-youtube-buildlang-megatool-bridge-validator-result.json"


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
    nodes = artifact.get("megatool_nodes", [])
    summary = artifact.get("solver_summary", {})
    buildlang = artifact.get("buildlang_summary", {})
    if artifact.get("schema") != "YouTubeBuildLangMegatoolBridge/v1":
        errors.append("schema")
    if artifact.get("status") != "YOUTUBE_BUILDLANG_MEGATOOL_BRIDGE_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("youtube_pass") != "0085":
        errors.append("youtube_binding")
    if artifact.get("source_bindings", {}).get("buildc_pass") != "0092":
        errors.append("buildc_binding")
    if artifact.get("source_summary", {}).get("valid_video_count") != 19:
        errors.append("video_count")
    if artifact.get("source_summary", {}).get("dominant_cluster_video_count") != 13:
        errors.append("dominant_cluster")
    if summary.get("exact_optimum_value") != 162 or summary.get("scipy_exact_hit_count", 0) < 1:
        errors.append("solver_summary")
    if buildlang.get("buildc_verify_check_count") != 18 or buildlang.get("buildc_measurement_count") != 10:
        errors.append("buildlang_summary")
    if len(nodes) != 7 or artifact.get("primary_30_day_push", {}).get("cluster_id") != "enterprise_quantum_optimization":
        errors.append("ranking")
    if any(row.get("verification_status") != "HYPOTHESIS_WITH_LOCAL_RECEIPTS" for row in nodes):
        errors.append("node_status")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0093YouTubeBuildLangMegatoolBridgeValidatorRun/v1",
        "pass": "0093",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "YouTubeBuildLangMegatoolBridge",
            "errors": errors,
            "path": "schemas/youtube-buildlang-megatool-bridge-pass-0093.json",
            "node_count": len(nodes),
            "primary_push": artifact.get("primary_30_day_push", {}).get("market_facing_product"),
            "valid_video_count": artifact.get("source_summary", {}).get("valid_video_count"),
            "buildc_verify_check_count": buildlang.get("buildc_verify_check_count"),
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
