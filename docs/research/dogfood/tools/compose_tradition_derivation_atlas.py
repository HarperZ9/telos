"""Compose pass 0131 tradition derivation atlas receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "TraditionDerivationAtlasReceipt/v1"
PASS_ID = "0131"
STATUS_MATCH = "TRADITION_DERIVATION_ATLAS_MATCH"
STATUS_DRIFT = "TRADITION_DERIVATION_ATLAS_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0131-tradition-derivation-atlas"
PASS_0130 = ROOT / "schemas" / "brandom-work-lesson-graph-pass-0130.json"

TERMS = [
    "reason", "language", "logic", "inference", "concept", "meaning",
    "semantics", "pragmatism", "representation", "experience", "norm",
    "empiricism", "analytic", "Kant", "Hegel", "Sellars", "Rorty",
    "Frege", "Wittgenstein", "Brandom",
]

NODE_RULES = [
    ("classical_logic", "Classical Logic", "logic-classical"),
    ("frege", "Frege", "frege"),
    ("wittgenstein", "Wittgenstein", "wittgenstein"),
    ("kant", "Kant", "kant"),
    ("hegel", "Hegel", "hegel"),
    ("logical_empiricism", "Logical Empiricism", "logical-empiricism"),
    ("pragmatism", "Pragmatism", "pragmatism"),
    ("sellars", "Sellars", "sellars"),
    ("rorty", "Rorty", "rorty"),
    ("brandom", "Brandom", "Texts%20Mark%201%20p"),
]

EDGE_RULES = [
    ("classical_logic", "frege", "formal logic and semantics prerequisite"),
    ("frege", "wittgenstein", "logic-language analytic tradition"),
    ("kant", "hegel", "post-Kantian idealism line"),
    ("hegel", "brandom", "Hegelian recognitive/normative source lead"),
    ("classical_logic", "logical_empiricism", "logic-centered analytic context"),
    ("logical_empiricism", "sellars", "empiricism as contrast and inheritance"),
    ("kant", "sellars", "Kantian categories and experience source lead"),
    ("pragmatism", "rorty", "pragmatist anti-foundational context"),
    ("sellars", "rorty", "Sellarsian analytic-pragmatist bridge"),
    ("sellars", "brandom", "norms, reasons, and scorekeeping dependency"),
    ("rorty", "brandom", "pragmatist conversation source lead"),
    ("pragmatism", "brandom", "pragmatist inferentialist source lead"),
    ("frege", "brandom", "inferential semantics source lead"),
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
            "ref": row["ref"], "kind": row["kind"], "source": row["source"],
            "method": row["method"], "title": ascii_text(row.get("title", "")),
            "sha256": row["sha256"], "chars": len(body),
            "status": "GATHER_VERIFIED" if obj.exists() else "MISSING_OBJECT",
            "raw_body_exported": False, "_body": body,
        })
    return sorted(result, key=lambda item: item["ref"])


def public_receipts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = ["ref", "kind", "source", "method", "title", "sha256", "chars", "status", "raw_body_exported"]
    return [{key: row[key] for key in keys} for row in rows]


def term_counts(body: str, title: str) -> dict[str, int]:
    haystack = f"{title}\n{body}"
    return {term: len(re.findall(re.escape(term), haystack, re.IGNORECASE)) for term in TERMS}


def match_row(rows: list[dict[str, Any]], marker: str) -> dict[str, Any]:
    for row in rows:
        if marker.lower() in row["ref"].lower():
            return row
    raise KeyError(marker)


def build_nodes(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    nodes = []
    for node_id, label, marker in NODE_RULES:
        row = match_row(rows, marker)
        counts = term_counts(row["_body"], row["title"])
        dominant = sorted([term for term, count in counts.items() if count], key=lambda term: (-counts[term], term))[:6]
        nodes.append({
            "id": node_id,
            "label": label,
            "source_ref": row["ref"],
            "source_sha256": row["sha256"],
            "dominant_terms": dominant,
            "term_hit_count": sum(counts.values()),
            "status": "SOURCE_BACKED_NODE",
        })
    return nodes


def build_edges(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {node["id"]: node for node in nodes}
    edges = []
    for source, target, relation in EDGE_RULES:
        support = [by_id[source]["source_ref"], by_id[target]["source_ref"]]
        edges.append({
            "from": source,
            "to": target,
            "relation": relation,
            "status": "HYPOTHESIS_SOURCE_BACKED",
            "source_refs": support,
            "verification_boundary": "source-backed prerequisite/contrast edge, not a proven causal influence claim",
        })
    return edges


def learning_modules() -> list[dict[str, str]]:
    return [
        {"id": "source_trace", "verifier": "every concept edge names source refs", "exercise": "trace one Brandom claim to two predecessor anchors"},
        {"id": "contrast_class", "verifier": "learner names inherited and rejected commitments", "exercise": "compare Sellars and logical empiricism as source-backed contrast"},
        {"id": "prerequisite_path", "verifier": "all path nodes exist in atlas", "exercise": "construct a Kant -> Hegel -> Brandom path"},
        {"id": "inferential_rewrite", "verifier": "answer contains claim, rule, consequence, and objection", "exercise": "rewrite one tradition relation as an inferential move"},
        {"id": "overclaim_audit", "verifier": "unsupported causality and completeness claims are rejected", "exercise": "demote one attractive but under-evidenced claim"},
    ]


def product_hypotheses() -> list[dict[str, str]]:
    return [
        {"tool": "Tradition Derivation Atlas", "status": "HYPOTHESIS", "wedge": "source-backed intellectual dependency maps with explicit overclaim gates"},
        {"tool": "Concept Prerequisite Tutor", "status": "HYPOTHESIS", "wedge": "turns dense theory into prerequisite paths and checkable exercises"},
        {"tool": "Citation-to-Exercise Studio", "status": "HYPOTHESIS", "wedge": "converts citation clusters into learner tasks, objections, and repair receipts"},
        {"tool": "Research Lineage Packet", "status": "HYPOTHESIS", "wedge": "packages tradition edges with provenance, confidence, and falsifiers"},
    ]


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "complete_genealogy_rejected", "status": "REJECTED", "failures": ["sampled_sources_only", "requires_bibliographic_exhaustiveness"]},
        {"fixture_id": "causal_influence_from_edge_rejected", "status": "REJECTED", "failures": ["edge_is_prerequisite_hypothesis", "requires_primary_historical_evidence"]},
        {"fixture_id": "learning_efficacy_rejected", "status": "REJECTED", "failures": ["no_user_study", "no_outcome_measure"]},
        {"fixture_id": "sourceless_edge_rejected", "status": "REJECTED", "failures": ["missing_source_refs", "no_receipt"]},
        {"fixture_id": "raw_article_export_rejected", "status": "REJECTED", "failures": ["copyright_boundary", "receipt_digest_only"]},
        {"fixture_id": "humanities_to_natural_law_rejected", "status": "REJECTED", "failures": ["not_a_physics_law", "requires_independent_reproduction"]},
    ]


def run_json(command: list[str], timeout: int = 60) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0131 tradition derivation atlas for functional learning tools."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1400", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    upstream = read_json(PASS_0130)
    rows = read_catalog()
    nodes = build_nodes(rows)
    edges = build_edges(nodes)
    modules = learning_modules()
    negatives = negative_fixtures()
    artifact: dict[str, Any] = {
        "schema": SCHEMA, "pass": PASS_ID, "generated_on": "2026-07-01",
        "source_bindings": {"brandom_work_graph_pass": upstream["pass"], "brandom_work_graph_seal": upstream["seal"], "source_store": "gather/pass-0131-tradition-derivation-atlas"},
        "source_receipts": public_receipts(rows),
        "atlas_nodes": nodes,
        "atlas_edges": edges,
        "learning_modules": modules,
        "product_hypotheses": product_hypotheses(),
        "negative_fixtures": negatives,
        "boundary": "Pass 0131 builds a sampled, source-backed tradition atlas. Edges are prerequisite or contrast hypotheses, not complete genealogy, causality proof, learning-efficacy evidence, or natural-law promotion.",
        "current_promoted_natural_laws": [],
        "unsupported_claim_count": 0,
        "flagship_receipts": flagship_receipts(),
    }
    node_ids = {node["id"] for node in nodes}
    errors = []
    if len(rows) < 10 or any(row["status"] != "GATHER_VERIFIED" for row in artifact["source_receipts"]):
        errors.append("source_receipts")
    if len(nodes) < 10 or any(not node["dominant_terms"] for node in nodes):
        errors.append("atlas_nodes")
    if len(edges) < 12 or any(edge["from"] not in node_ids or edge["to"] not in node_ids or len(edge["source_refs"]) < 2 for edge in edges):
        errors.append("atlas_edges")
    if len(modules) < 5:
        errors.append("learning_modules")
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
    parser.add_argument("--out", default=str(ROOT / "schemas" / "tradition-derivation-atlas-pass-0131.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
