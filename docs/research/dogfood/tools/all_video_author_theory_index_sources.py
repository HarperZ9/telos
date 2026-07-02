"""Source scanner for pass 0134 all-video author/theory index."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SOURCE_FILES = {
    "pass_0085_youtube_compounding": ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json",
    "pass_0102_youtube_roadmap": ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json",
    "pass_0121_youtube_growth": ROOT / "schemas" / "youtube-megatool-growth-vector-receipt-pass-0121.json",
    "pass_0125_youtube_router": ROOT / "schemas" / "youtube-experiment-router-pass-0125.json",
    "pass_0129_brandom_digest": ROOT / "schemas" / "brandom-functional-learning-digest-pass-0129.json",
    "pass_0133_youtube_intake": ROOT / "schemas" / "youtube-source-lead-intake-pass-0133.json",
    "demo_learning_forge": REPO / "demo" / "research" / "youtube-learning-forge-receipts.json",
    "demo_math_educator": REPO / "demo" / "research" / "youtube-math-educator-receipts.json",
    "demo_bgoertzel": REPO / "demo" / "research" / "youtube-bgoertzel-receipts.json",
}
KNOWN_AUTHORS = [
    "Robert Brandom", "Kane B", "Vitaly Vanchurin", "Michael Levin",
    "Emily Riehl", "Gabriele Carcassi", "Thomas Ahle",
    "Thomas Dybdahl Ahle", "Inigo Quilez", "Francois Chollet",
    "Nathan Seiberg", "Neil Turok", "Joscha Bach", "Konrad Kording",
    "Grant Sanderson", "Leslie Lamport", "Ben Goertzel",
    "Yuval Noah Harari", "Tom Oxley", "John Jumper", "Brad Carson",
    "Michael I. Jordan", "Blaise Aguera y Arcas",
]
LANE_CHAINS = {
    "ai_model_eval_search": ["source lead", "benchmark or model claim", "contamination boundary", "replay attempt", "verifier verdict"],
    "ai4science_biology": ["source lead", "paper or model lineage", "simulation or assay target", "negative result lane", "claim-to-experiment packet"],
    "brandom_functional_learning": ["source lead", "author work catalog", "reference lineage", "commitment/entitlement exercise", "learning receipt"],
    "formal_compute_language": ["source lead", "definition boundary", "theorem or program target", "counterexample lane", "proof/runtime receipt"],
    "physics_foundations": ["source lead", "mathematical object", "normalization or invariant", "interpretation boundary", "runtime receipt"],
    "quantum_optimization": ["source lead", "problem encoding", "solver branch", "calibration or backend context", "objective receipt"],
    "quant_finance": ["source lead", "identity or risk model", "stress fixture", "tolerance receipt", "promotion gate"],
    "rendering_compute_kernels": ["source lead", "formula/kernel", "measured artifact", "visual/calibration receipt", "replay handle"],
    "societal_governance": ["source lead", "assumption ledger", "stakeholder/authority boundary", "review lane", "decision receipt"],
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def ascii_text(value: object) -> str:
    return str(value or "").encode("ascii", "ignore").decode("ascii")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def video_id_from_url(url: str) -> str:
    match = re.search(r"[?&]v=([^&]+)", url)
    return match.group(1) if match else ""


def lane_for(title: str, topics: list[str], uploader: str) -> str:
    text = " ".join([title, uploader, *topics]).lower()
    checks = [
        ("brandom_functional_learning", ["brandom", "kane b", "skeptic", "truth", "deontology", "philosopher", "kant", "sellars", "hegel"]),
        ("quantum_optimization", ["d-wave", "qubo", "quantum optimization", "anneal", "qubit"]),
        ("quant_finance", ["finance", "quantitative"]),
        ("rendering_compute_kernels", ["shader", "procedural", "render", "gemm", "gpu", "cuda", "blackwell"]),
        ("ai4science_biology", ["biology", "evolution", "brain", "neuron", "morphosyntactic", "skull"]),
        ("formal_compute_language", ["category", "homotopy", "disproves", "distributed", "programming language", "computers work"]),
        ("physics_foundations", ["born rule", "entropy", "entanglement", "symmetry", "anomaly", "time", "universe", "cosmology"]),
        ("societal_governance", ["harari", "risk", "catastrophe", "civilization", "weapons"]),
    ]
    for lane, terms in checks:
        if any(term in text for term in terms):
            return lane
    return "ai_model_eval_search"


def topic_terms(title: str, extra: list[str] | None = None) -> list[str]:
    candidates = ["agent", "agi", "ai", "biology", "brain", "category", "compiler", "computing", "cryptography", "deontology", "distributed", "entropy", "evolution", "finance", "geometry", "gpu", "homotopy", "language", "learning", "math", "physics", "proof", "quantum", "rendering", "risk", "skepticism", "symmetry", "truth"]
    found = [term for term in candidates if term in title.lower()]
    for term in extra or []:
        clean = ascii_text(term).lower().strip()
        if clean and clean not in found:
            found.append(clean)
    return found[:8]


def author_candidates(title: str, uploader: str) -> list[dict[str, str]]:
    authors: list[dict[str, str]] = []
    if uploader:
        authors.append({"name": uploader, "evidence": "uploader_or_channel", "confidence": "moderate"})
    text = ascii_text(title)
    for name in KNOWN_AUTHORS:
        if name.lower() in text.lower() and name.lower() != uploader.lower():
            authors.append({"name": name, "evidence": "title_mention", "confidence": "moderate"})
    for pattern in [r"\bby ([A-Z][A-Za-z .'-]{3,40})", r"\bDr\. ([A-Z][A-Za-z .'-]{3,40})", r"\bProf\. ([A-Z][A-Za-z .'-]{3,40})", r"\bft\. ([A-Z][A-Za-z .'-]{3,40})"]:
        for match in re.finditer(pattern, text):
            name = match.group(1).strip(" .-'")
            if 1 < len(name.split()) <= 5:
                authors.append({"name": name, "evidence": "title_pattern", "confidence": "low"})
    dedup: dict[str, dict[str, str]] = {}
    for row in authors:
        dedup.setdefault(row["name"], row)
    return sorted(dedup.values(), key=lambda item: item["name"].lower())


def add_video(videos: dict[str, dict[str, Any]], source: str, row: dict[str, Any]) -> None:
    url = ascii_text(row.get("url") or row.get("webpage_url"))
    vid = ascii_text(row.get("video_id") or row.get("id") or video_id_from_url(url))
    if not vid:
        return
    title = ascii_text(row.get("title"))
    uploader = ascii_text(row.get("uploader") or row.get("channel"))
    entry = videos.setdefault(vid, {"video_id": vid, "urls": set(), "titles": set(), "uploaders": set(), "topics": set(), "source_artifacts": set(), "receipt_hashes": set()})
    for field, value in [("urls", url), ("titles", title), ("uploaders", uploader)]:
        if value:
            entry[field].add(value)
    entry["topics"].update(topic_terms(title, row.get("lead_topics") or row.get("top_terms") or []))
    entry["source_artifacts"].add(source)
    for key in ["metadata_sha256", "transcript_sha256", "sha256", "stored_object_sha256"]:
        if row.get(key):
            entry["receipt_hashes"].add(ascii_text(row[key]))


def add_channel(channels: dict[str, dict[str, Any]], source: str, row: dict[str, Any]) -> None:
    url = ascii_text(row.get("url") or row.get("webpage_url"))
    if not url or "youtube.com/@" not in url:
        return
    entry = channels.setdefault(url, {"url": url, "channel": "", "source_artifacts": set(), "captured_entries": 0, "entry_titles": set()})
    entry["channel"] = ascii_text(row.get("channel") or row.get("title") or entry["channel"])
    entry["source_artifacts"].add(source)
    entry["captured_entries"] = max(entry["captured_entries"], int(row.get("captured_entries") or 0))
    for item in row.get("entries", []):
        entry["entry_titles"].add(ascii_text(item.get("title")))


def collect_corpus() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    videos: dict[str, dict[str, Any]] = {}
    channels: dict[str, dict[str, Any]] = {}
    invalid: list[dict[str, Any]] = []
    for name, path in SOURCE_FILES.items():
        data = read_json(path)
        rows = data.get("source_cards", []) + data.get("video_cards", []) + data.get("youtube_source_leads", []) + data.get("video_leads", []) + data.get("results", [])
        for row in rows:
            if row.get("status") == "INVALID_URL":
                invalid.append({"source_artifact": name, "url": ascii_text(row.get("url")), "reason": ascii_text(row.get("reason"))})
            else:
                add_video(videos, name, row)
        for result in data.get("video_results", []):
            catalog = result.get("catalog", [])
            meta = next((item for item in catalog if item.get("kind") == "metadata"), {})
            transcript = next((item for item in catalog if item.get("kind") == "transcript"), {})
            add_video(videos, name, {"url": result.get("url"), "id": meta.get("id"), "title": meta.get("title"), "metadata_sha256": meta.get("sha256"), "transcript_sha256": transcript.get("sha256")})
        for receipt in data.get("source_receipts", []):
            if receipt.get("source") == "video" and receipt.get("kind") == "metadata":
                add_video(videos, name, {"id": receipt.get("ref"), "title": receipt.get("title"), "uploader": receipt.get("uploader"), "metadata_sha256": receipt.get("sha256")})
            elif "youtube.com/@" in ascii_text(receipt.get("ref")):
                add_channel(channels, name, {"url": receipt.get("ref"), "title": receipt.get("title")})
        for row in data.get("channel_leads", []) + data.get("channel_results", []):
            add_channel(channels, name, row)
    return public_videos(videos), public_channels(channels), invalid


def public_videos(videos: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for vid, row in sorted(videos.items()):
        title = sorted(row["titles"])[0] if row["titles"] else ""
        uploader = sorted(row["uploaders"])[0] if row["uploaders"] else ""
        topics = sorted(row["topics"])
        rows.append({
            "video_id": vid,
            "url": sorted(row["urls"])[0] if row["urls"] else f"https://www.youtube.com/watch?v={vid}",
            "title": title,
            "uploader": uploader,
            "authors": author_candidates(title, uploader),
            "lane": lane_for(title, topics, uploader),
            "topics": topics,
            "source_artifacts": sorted(row["source_artifacts"]),
            "receipt_hashes": sorted(row["receipt_hashes"])[:6],
            "claim_status": "SOURCE_LEAD_ONLY",
        })
    return rows


def public_channels(channels: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted([{**row, "source_artifacts": sorted(row["source_artifacts"]), "entry_titles": sorted(row["entry_titles"])[:12]} for row in channels.values()], key=lambda item: item["url"])


def author_nodes(videos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    authors: dict[str, dict[str, Any]] = {}
    for video in videos:
        for author in video["authors"]:
            node = authors.setdefault(author["name"], {"name": author["name"], "video_ids": set(), "lanes": set(), "evidence": set()})
            node["video_ids"].add(video["video_id"])
            node["lanes"].add(video["lane"])
            node["evidence"].add(author["evidence"])
    rows = [{"name": node["name"], "video_count": len(node["video_ids"]), "video_ids": sorted(node["video_ids"]), "lanes": sorted(node["lanes"]), "evidence": sorted(node["evidence"]), "status": "AUTHOR_SOURCE_NODE"} for node in authors.values()]
    return sorted(rows, key=lambda item: (-item["video_count"], item["name"].lower()))


def next_experiment(lane: str) -> str:
    special = {
        "brandom_functional_learning": "Build author-work-reference graph and scorekeeping exercises over Brandom/Kane B source leads.",
        "ai4science_biology": "Retrieve primary papers and make a falsifiable model/reproduction queue for biology/evolution/neuro leads.",
        "formal_compute_language": "Extract theorem/program targets and run counterexample or formal-runtime fixtures.",
        "physics_foundations": "Separate normalization/invariant arithmetic from interpretation claims with negative fixtures.",
        "quantum_optimization": "Normalize problem encoding, solver branch, calibration context, and objective receipts.",
        "rendering_compute_kernels": "Attach formulas/kernels to measured rendered artifacts and calibration receipts.",
    }
    return special.get(lane, "Convert source lead into primary-source retrieval, claim boundary, executable probe, and Crucible gate.")


def market_tool(lane: str) -> str:
    tools = {
        "brandom_functional_learning": "Functional Learning and Theory Graph Workbench",
        "ai4science_biology": "Bio/Neuro Claim-to-Experiment Packet",
        "formal_compute_language": "Counterexample and Formal Runtime Workbench",
        "physics_foundations": "Physics Claim Boundary Kit",
        "quantum_optimization": "Optimization Proof Workbench",
        "rendering_compute_kernels": "Visual/Compute Kernel Proof Kit",
    }
    return tools.get(lane, "Source-to-Proof Packet Factory")


def theory_lanes(videos: list[dict[str, Any]], authors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_author = {author["name"] for author in authors}
    lanes = []
    for lane, chain in LANE_CHAINS.items():
        lane_videos = [video for video in videos if video["lane"] == lane]
        source_authors = sorted({author["name"] for video in lane_videos for author in video["authors"] if author["name"] in by_author})
        lanes.append({"lane_id": lane, "video_count": len(lane_videos), "source_video_ids": [video["video_id"] for video in lane_videos], "source_authors": source_authors[:20], "theory_chain": chain, "next_experiment": next_experiment(lane), "market_tool_hypothesis": market_tool(lane), "status": "HYPOTHESIS_SOURCE_LEAD", "gap_status": "inferred"})
    return sorted(lanes, key=lambda item: (-item["video_count"], item["lane_id"]))


def reference_queue(authors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"author": author["name"], "source_video_ids": author["video_ids"][:8], "lanes": author["lanes"], "required_work_corpus": ["official profile or bibliography", "primary papers/books/repos", "lecture/course materials", "explicit citations or references", "known critiques or counterexamples"], "promotion_gate": "No theory edge promotes beyond HYPOTHESIS until primary source receipts and at least one executable or textual negative-control fixture exist.", "status": "REFERENCE_DISCOVERY_REQUIRED"} for author in authors[:40]]


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "title_mention_as_authority_rejected", "status": "REJECTED", "failures": ["title_mentions_are_source_leads", "requires_primary_author_source"]},
        {"fixture_id": "video_claim_as_theory_edge_rejected", "status": "REJECTED", "failures": ["video_only_claim", "requires_independent_source"]},
        {"fixture_id": "thread_history_as_complete_corpus_rejected", "status": "REJECTED", "failures": ["local_thread_search_incomplete", "requires_repo_or_exported_receipts"]},
        {"fixture_id": "channel_page_as_complete_works_rejected", "status": "REJECTED", "failures": ["dynamic_playlist", "partial_capture"]},
        {"fixture_id": "raw_transcript_export_rejected", "status": "REJECTED", "failures": ["copyright_boundary", "digest_only"]},
        {"fixture_id": "reference_without_source_rejected", "status": "REJECTED", "failures": ["citation_not_gathered", "no_receipt"]},
        {"fixture_id": "theory_chain_as_natural_law_rejected", "status": "REJECTED", "failures": ["planning_graph_only", "requires_proof_and_reproduction"]},
    ]
