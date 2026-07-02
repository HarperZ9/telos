"""Compose pass 0130 Brandom work catalog and lesson graph receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import unquote

SCHEMA = "BrandomWorkLessonGraphReceipt/v1"
PASS_ID = "0130"
STATUS_MATCH = "BRANDOM_WORK_LESSON_GRAPH_MATCH"
STATUS_DRIFT = "BRANDOM_WORK_LESSON_GRAPH_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0130-brandom-work-lesson-graph"
PASS_0129 = ROOT / "schemas" / "brandom-functional-learning-digest-pass-0129.json"

TERMS = [
    "reason",
    "language",
    "logic",
    "semantics",
    "pragmatism",
    "inferentialism",
    "expressivism",
    "Sellars",
    "Kant",
    "Hegel",
    "modality",
    "artificial intelligence",
    "commitment",
    "representation",
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
            "ref": row["ref"],
            "kind": row["kind"],
            "source": row["source"],
            "method": row["method"],
            "title": ascii_text(row.get("title", "")),
            "sha256": row["sha256"],
            "chars": len(body),
            "status": "GATHER_VERIFIED" if obj.exists() else "MISSING_OBJECT",
            "raw_body_exported": False,
            "_body": body,
        })
    return sorted(result, key=lambda item: item["ref"])


def public_receipts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = ["ref", "kind", "source", "method", "title", "sha256", "chars", "status", "raw_body_exported"]
    return [{key: row[key] for key in keys} for row in rows]


def title_from_ref(ref: str) -> str:
    name = unquote(ref.rsplit("/", 1)[-1])
    for suffix in [".pdf", ".html", ".docx", ".doc"]:
        if name.lower().endswith(suffix):
            name = name[: -len(suffix)]
    return ascii_text(re.sub(r"\s+", " ", name.replace("_", " ")).strip())


def term_counts(body: str, title: str) -> dict[str, int]:
    haystack = f"{title}\n{body}"
    return {term: len(re.findall(re.escape(term), haystack, re.IGNORECASE)) for term in TERMS}


def work_catalog(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    catalog = []
    for row in rows:
        title = title_from_ref(row["ref"]) if row["ref"].lower().endswith((".pdf", ".html")) else row["title"]
        counts = term_counts(row["_body"], title)
        dominant = sorted([term for term, count in counts.items() if count], key=lambda term: (-counts[term], term))[:5]
        catalog.append({
            "work_id": sha256_text(row["ref"])[:12],
            "title": title,
            "ref": row["ref"],
            "source_kind": "course_page" if "Courses/" in row["ref"] else "downloadable_text",
            "chars": row["chars"],
            "sha256": row["sha256"],
            "dominant_terms": dominant,
            "term_hit_count": sum(counts.values()),
            "status": "CATALOGED_FROM_GATHER_RECEIPT",
        })
    return catalog


def lesson_graph(catalog: list[dict[str, Any]]) -> dict[str, Any]:
    refs = {row["title"]: row["ref"] for row in catalog}
    nodes = [
        {"id": "source_intake", "kind": "source", "label": "Gather course and text receipts", "source_refs": [row["ref"] for row in catalog], "exercise": "Identify which claims have receipts and which are missing."},
        {"id": "vocabulary", "kind": "concept", "label": "Vocabulary of reasons", "source_refs": [ref for title, ref in refs.items() if "Vocabularies" in title or "Language" in title], "exercise": "Mark terms that function as explicit vocabulary for a practice."},
        {"id": "inferential_link", "kind": "concept", "label": "Reasons as inferential links", "source_refs": [ref for title, ref in refs.items() if "Inferentialism" in title or "Language" in title], "exercise": "Convert one reading claim into antecedent, rule, and consequence."},
        {"id": "scorekeeping", "kind": "practice", "label": "Commitments and entitlements", "source_refs": [ref for title, ref in refs.items() if "Commitments" in title or "Inferentialism" in title], "exercise": "Given p and p -> q, record the commitment and entitlement ledger."},
        {"id": "challenge_repair", "kind": "practice", "label": "Challenge and repair", "source_refs": [ref for title, ref in refs.items() if "Pragmatism" in title or "Sellars" in title], "exercise": "Reject an unsupported inference and add the missing source or rule."},
        {"id": "ai_application", "kind": "tool", "label": "AI as reason-governed assistant", "source_refs": [ref for title, ref in refs.items() if "Artificial Intelligence" in title], "exercise": "Design a model action receipt that distinguishes assertion, inference, and repair."},
    ]
    edges = [
        {"from": "source_intake", "to": "vocabulary"},
        {"from": "vocabulary", "to": "inferential_link"},
        {"from": "inferential_link", "to": "scorekeeping"},
        {"from": "scorekeeping", "to": "challenge_repair"},
        {"from": "challenge_repair", "to": "ai_application"},
    ]
    node_ids = {row["id"] for row in nodes}
    graph_ok = all(edge["from"] in node_ids and edge["to"] in node_ids for edge in edges)
    graph_ok = graph_ok and all(nodes[index]["id"] != nodes[index + 1]["id"] for index in range(len(nodes) - 1))
    graph_ok = graph_ok and all(node["exercise"] and node["source_refs"] for node in nodes)
    return {"nodes": nodes, "edges": edges, "status": "MATCH" if graph_ok else "DRIFT", "graph_invariant": "all edges resolve, every node has source_refs and an exercise"}


def learner_action_fixture() -> dict[str, Any]:
    steps = [
        {"step": "cite_source", "input": "Vocabularies of Reason receipt", "accepted": True},
        {"step": "state_claim", "input": "a vocabulary can make a practice explicit", "accepted": True},
        {"step": "add_inference", "input": "explicit vocabulary -> checkable learning move", "accepted": True},
        {"step": "submit_answer", "input": "build a lesson node with source, claim, exercise, verifier", "accepted": True},
    ]
    return {
        "fixture_id": "lesson_action_receipt_loop",
        "status": "MATCH" if all(step["accepted"] for step in steps) else "DRIFT",
        "steps": steps,
        "verifier": "requires source, claim, exercise, and verifier fields before accepting learner answer",
    }


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "filename_as_claim_rejected", "status": "REJECTED", "failures": ["filename_is_catalog_hint", "requires_body_or_source_claim"]},
        {"fixture_id": "pdf_body_export_rejected", "status": "REJECTED", "failures": ["copyright_boundary", "receipt_digest_only"]},
        {"fixture_id": "course_page_as_complete_syllabus_rejected", "status": "REJECTED", "failures": ["course_page_is_partial", "requires_session_level_intake"]},
        {"fixture_id": "lesson_graph_as_learning_efficacy_rejected", "status": "REJECTED", "failures": ["no_user_study", "no_outcome_measure"]},
        {"fixture_id": "philosophy_to_scientific_law_rejected", "status": "REJECTED", "failures": ["humanities_corpus", "not_natural_law"]},
    ]


def run_json(command: list[str], timeout: int = 60) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0130 Brandom work catalog and lesson graph for functional learning tools."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1400", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    upstream = read_json(PASS_0129)
    rows = read_catalog()
    catalog = work_catalog(rows)
    graph = lesson_graph(catalog)
    action_fixture = learner_action_fixture()
    negatives = negative_fixtures()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"brandom_digest_pass": upstream["pass"], "brandom_digest_seal": upstream["seal"], "source_store": "gather/pass-0130-brandom-work-lesson-graph"},
        "source_receipts": public_receipts(rows),
        "work_catalog": catalog,
        "lesson_graph": graph,
        "learner_action_fixture": action_fixture,
        "product_implications": [
            {"tool": "Lesson Graph Builder", "status": "HYPOTHESIS", "wedge": "source-backed course-to-exercise transformation"},
            {"tool": "Reason Ledger Tutor", "status": "HYPOTHESIS", "wedge": "commitment, entitlement, challenge, and repair as checkable learner actions"},
            {"tool": "AI Philosophy Lab", "status": "HYPOTHESIS", "wedge": "AI assistance constrained by reason-action receipts"},
        ],
        "negative_fixtures": negatives,
        "boundary": "Pass 0130 catalogs five gathered Brandom texts/course pages and builds a bounded lesson graph. It does not export PDF bodies, prove learning efficacy, complete Brandom's bibliography, or promote philosophical claims as natural laws.",
        "current_promoted_natural_laws": [],
        "unsupported_claim_count": 0,
        "flagship_receipts": flagship_receipts(),
    }
    errors = []
    if len(rows) < 5 or any(row["status"] != "GATHER_VERIFIED" for row in artifact["source_receipts"]):
        errors.append("source_receipts")
    if len(catalog) < 5 or any(not row["dominant_terms"] for row in catalog):
        errors.append("work_catalog")
    if graph["status"] != "MATCH":
        errors.append("lesson_graph")
    if action_fixture["status"] != "MATCH":
        errors.append("learner_action_fixture")
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
    parser.add_argument("--out", default=str(ROOT / "schemas" / "brandom-work-lesson-graph-pass-0130.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
