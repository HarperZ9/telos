"""Gather-backed YouTube source leads for pass 0115."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
YOUTUBE_LEAD_STORE = ROOT / "gather" / "pass-0115-youtube-leads"
YOUTUBE_LEADS = [
    ("HbKzqvey5PA", "https://www.youtube.com/watch?v=HbKzqvey5PA", 0, "quantum_foundations_born_rule_entropy"),
    ("4MQbd5wTlI8", "https://www.youtube.com/watch?v=4MQbd5wTlI8", 0, "higher_category_theory_homotopy_ai_math"),
    ("EdVG5qNm2rY", "https://www.youtube.com/watch?v=EdVG5qNm2rY&t=337s", 337, "theoretical_cs_belief_revision"),
    ("nYwid6Q5HXk", "https://www.youtube.com/watch?v=nYwid6Q5HXk", 0, "looped_llm_reasoning_architecture"),
]


def read_gather_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return json.loads(path.read_text(encoding="utf-16"))


def lead_spec(video_id: str, url: str, start_seconds: int, topic_hypothesis: str) -> dict[str, Any]:
    return {"video_id": video_id, "url": url, "start_seconds": start_seconds, "topic_hypothesis": topic_hypothesis}


def gather_youtube_source_leads() -> list[dict[str, Any]]:
    leads: list[dict[str, Any]] = []
    for video_id, url, start_seconds, topic in YOUTUBE_LEADS:
        spec = lead_spec(video_id, url, start_seconds, topic)
        path = YOUTUBE_LEAD_STORE / f"gather-{video_id}.json"
        if not path.exists():
            leads.append({**spec, "source_status": "GATHER_RECEIPT_MISSING", "claim_status": "SOURCE_LEAD_ONLY", "raw_transcript_included": False, "verified": False})
            continue
        data = read_gather_json(path)
        catalog = data.get("catalog", [])
        receipts = data.get("digest", {}).get("receipts", [])
        by_kind = {row.get("kind"): row for row in receipts}
        catalog_by_kind = {row.get("kind"): row for row in catalog}
        metadata = by_kind.get("metadata", {})
        transcript = by_kind.get("transcript", {})
        transcript_catalog = catalog_by_kind.get("transcript", {})
        leads.append({
            **spec,
            "source_status": "GATHER_VERIFIED_RECEIPT",
            "claim_status": "SOURCE_LEAD_ONLY",
            "semantic_gap_status": "inferred",
            "verified": bool(data.get("verified")),
            "title": metadata.get("title"),
            "metadata_method": metadata.get("method"),
            "metadata_sha256": metadata.get("sha256"),
            "transcript_method": transcript.get("method"),
            "transcript_sha256": transcript.get("sha256"),
            "transcript_chars": transcript_catalog.get("chars"),
            "receipt_count": len(receipts),
            "digest_seal": data.get("digest", {}).get("seal"),
            "store_path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "raw_transcript_included": False,
        })
    return leads
