"""Validate pass 0112 Lyapunov stability certificate receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "lyapunov-stability-certificate-receipt-pass-0112.json"
RESULT = ROOT / "schemas" / "pass-0112-lyapunov-stability-certificate-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    stable = artifact.get("stable_certificate", {})
    neg = artifact.get("negative_fixtures", {})
    youtube = artifact.get("youtube_binding", {})
    errors: list[str] = []

    if artifact.get("schema") != "LyapunovStabilityCertificateReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "LYAPUNOV_STABILITY_CERTIFICATE_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("runtime_suite_pass") != "0111":
        errors.append("runtime_suite_pass")
    if artifact.get("source_bindings", {}).get("youtube_roadmap_pass") != "0102":
        errors.append("youtube_roadmap_pass")
    if len(artifact.get("source_anchors", [])) < 8:
        errors.append("source_anchors")
    if stable.get("A") != [["1/2", "0"], ["0", "1/3"]]:
        errors.append("A")
    if stable.get("P") != [["4/3", "0"], ["0", "9/8"]]:
        errors.append("P")
    if stable.get("positive_definite") is not True or stable.get("max_identity_residual") != "0":
        errors.append("stable_certificate")
    if any(row.get("status") != "MATCH" for row in stable.get("energy_samples", [])):
        errors.append("energy_samples")
    unstable = neg.get("unstable_spectral_fixture", {})
    if unstable.get("classification") != "PD_FAIL_EXPECTED" or unstable.get("positive_definite") is not False:
        errors.append("unstable_fixture")
    bad = neg.get("bad_certificate_fixture", {})
    if bad.get("classification") != "RESIDUAL_DRIFT_EXPECTED" or bad.get("max_identity_residual") == "0":
        errors.append("bad_certificate_fixture")
    if artifact.get("market_surface", {}).get("tool_count", 0) < 8:
        errors.append("market")
    if youtube.get("valid_video_count") != 19 or youtube.get("raw_transcript_included") is not False:
        errors.append("youtube")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0112LyapunovStabilityCertificateValidatorRun/v1",
        "pass": "0112",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "LyapunovStabilityCertificateReceipt",
            "errors": errors,
            "path": "schemas/lyapunov-stability-certificate-receipt-pass-0112.json",
            "max_identity_residual": stable.get("max_identity_residual"),
            "source_anchor_count": len(artifact.get("source_anchors", [])),
            "youtube_valid_video_count": youtube.get("valid_video_count"),
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
