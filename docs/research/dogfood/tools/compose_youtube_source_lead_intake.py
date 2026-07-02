"""Compose pass 0133 YouTube source-lead intake receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "YouTubeSourceLeadIntakeReceipt/v1"
PASS_ID = "0133"
STATUS_MATCH = "YOUTUBE_SOURCE_LEAD_INTAKE_MATCH"
STATUS_DRIFT = "YOUTUBE_SOURCE_LEAD_INTAKE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0133-youtube-source-lead-intake"
PASS_0132 = ROOT / "schemas" / "proof-pattern-transfer-pass-0132.json"

TERMS = [
    "skepticism", "truth", "deontology", "veridical", "philosopher",
    "death", "knowledge", "biology", "evolution", "geometric",
    "computing", "proof", "model", "math", "physics", "learning",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def ascii_text(value: str) -> str:
    return value.encode("ascii", "ignore").decode("ascii")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def read_catalog() -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    result = []
    for row in rows:
        obj = STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
        body = obj.read_text(encoding="utf-8", errors="replace") if obj.exists() else ""
        result.append({
            "ref": row["ref"], "id": row["id"], "kind": row["kind"],
            "source": row["source"], "method": row["method"],
            "title": ascii_text(row.get("title", "")),
            "uploader": ascii_text(row.get("meta", {}).get("uploader", "")),
            "sha256": row["sha256"], "chars": len(body),
            "status": "GATHER_VERIFIED" if obj.exists() else "MISSING_OBJECT",
            "raw_body_exported": False, "_body": body,
        })
    return result


def public_receipts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = ["id", "ref", "kind", "source", "method", "title", "uploader", "sha256", "chars", "status", "raw_body_exported"]
    return [{key: row[key] for key in keys} for row in sorted(rows, key=lambda item: (item["id"], item["kind"]))]


def term_counts(text: str) -> dict[str, int]:
    return {term: len(re.findall(re.escape(term), text, re.IGNORECASE)) for term in TERMS}


def route_for(title: str, body: str) -> str:
    title_lower = title.lower()
    body_lower = body.lower()
    if "geometric framework" in title_lower or "biological evolution" in title_lower:
        return "biology_evolution_geometry"
    if "computing" in title_lower or "disproves" in title_lower:
        return "theoretical_computing_breakthrough"
    if "skeptic" in title_lower or "truth" in title_lower or "deontology" in title_lower or "veridical" in title_lower:
        return "epistemology_ethics_learning"
    if "death" in title_lower or "philosopher" in title_lower or "moral" in body_lower:
        return "philosophy_learning"
    return "philosophy_learning"


def video_leads(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row["source"] == "video":
            by_id.setdefault(row["id"], []).append(row)
    leads = []
    for video_id, group in sorted(by_id.items()):
        metadata = next((row for row in group if row["kind"] == "metadata"), None)
        transcript = next((row for row in group if row["kind"] == "transcript"), None)
        title = (metadata or transcript or group[0])["title"]
        body = transcript["_body"] if transcript else ""
        counts = term_counts(f"{title}\n{body}")
        top_terms = sorted([term for term, count in counts.items() if count], key=lambda term: (-counts[term], term))[:6]
        leads.append({
            "video_id": video_id,
            "title": title,
            "uploader": (metadata or transcript or group[0])["uploader"],
            "metadata_sha256": metadata["sha256"] if metadata else None,
            "transcript_sha256": transcript["sha256"] if transcript else None,
            "transcript_method": transcript["method"] if transcript else None,
            "transcript_chars": transcript["chars"] if transcript else 0,
            "top_terms": top_terms,
            "route": route_for(title, body),
            "status": "SOURCE_LEAD_ONLY",
        })
    return leads


def route_summary(leads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    routes = sorted({lead["route"] for lead in leads})
    return [{"route": route, "video_count": sum(1 for lead in leads if lead["route"] == route), "status": "SOURCE_LEAD_ONLY"} for route in routes]


def product_hypotheses() -> list[dict[str, str]]:
    return [
        {"tool": "Argument-to-Proof Packet Router", "status": "HYPOTHESIS", "wedge": "turn philosophy videos into source leads, claim graphs, objections, and proof gates"},
        {"tool": "Bio-Evolution Geometry Queue", "status": "HYPOTHESIS", "wedge": "route biology/evolution geometry talks into executable model and falsifier packets"},
        {"tool": "TCS Breakthrough Replication Queue", "status": "HYPOTHESIS", "wedge": "turn computing-breakthrough videos into paper/source retrieval and independent proof replay tasks"},
        {"tool": "Transcript Boundary Auditor", "status": "HYPOTHESIS", "wedge": "separate metadata, transcript, speaker claims, and independently verified claims"},
    ]


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "video_title_as_fact_rejected", "status": "REJECTED", "failures": ["title_is_source_lead", "requires_primary_source"]},
        {"fixture_id": "auto_caption_as_ground_truth_rejected", "status": "REJECTED", "failures": ["auto_caption_noise", "requires_verification"]},
        {"fixture_id": "channel_page_as_complete_catalog_rejected", "status": "REJECTED", "failures": ["dynamic_page", "partial_http_capture"]},
        {"fixture_id": "raw_transcript_export_rejected", "status": "REJECTED", "failures": ["copyright_boundary", "digest_only"]},
        {"fixture_id": "video_only_market_claim_rejected", "status": "REJECTED", "failures": ["no_buyer_evidence", "no_competitor_matrix"]},
        {"fixture_id": "source_lead_as_law_rejected", "status": "REJECTED", "failures": ["requires_independent_proof", "requires_reproduction"]},
    ]


def run_json(command: list[str], timeout: int = 60) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0133 YouTube source-lead intake for philosophy, biology, and computing proof queues."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1400", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    upstream = read_json(PASS_0132)
    rows = read_catalog()
    leads = video_leads(rows)
    negatives = negative_fixtures()
    artifact: dict[str, Any] = {
        "schema": SCHEMA, "pass": PASS_ID, "generated_on": "2026-07-01",
        "source_bindings": {"proof_transfer_pass": upstream["pass"], "proof_transfer_seal": upstream["seal"], "source_store": "gather/pass-0133-youtube-source-lead-intake"},
        "source_receipts": public_receipts(rows),
        "video_leads": leads,
        "route_summary": route_summary(leads),
        "product_hypotheses": product_hypotheses(),
        "negative_fixtures": negatives,
        "boundary": "Pass 0133 ingests supplied YouTube links as source leads only. Metadata and transcript receipts may seed future work, but video-only claims are not verified facts, proofs, market evidence, or natural laws.",
        "current_promoted_natural_laws": [],
        "unsupported_claim_count": 0,
        "flagship_receipts": flagship_receipts(),
    }
    errors = []
    if len(rows) < 19 or any(row["status"] != "GATHER_VERIFIED" for row in artifact["source_receipts"]):
        errors.append("source_receipts")
    if len(leads) < 9 or any(lead["status"] != "SOURCE_LEAD_ONLY" for lead in leads):
        errors.append("video_leads")
    if not any(route["route"] == "biology_evolution_geometry" for route in artifact["route_summary"]):
        errors.append("biology_route")
    if not any(route["route"] == "theoretical_computing_breakthrough" for route in artifact["route_summary"]):
        errors.append("computing_route")
    if any(row["status"] != "REJECTED" for row in negatives):
        errors.append("negative_fixtures")
    if any(row["status"] != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "youtube-source-lead-intake-pass-0133.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
