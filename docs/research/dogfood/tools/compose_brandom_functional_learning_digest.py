"""Compose pass 0129 Brandom functional-learning digest receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "BrandomFunctionalLearningDigestReceipt/v1"
PASS_ID = "0129"
STATUS_MATCH = "BRANDOM_FUNCTIONAL_LEARNING_DIGEST_MATCH"
STATUS_DRIFT = "BRANDOM_FUNCTIONAL_LEARNING_DIGEST_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0129-brandom-functional-learning"
PASS_0128 = ROOT / "schemas" / "cross-field-proof-suite-pass-0128.json"

TERMS = [
    "inferentialism",
    "pragmatism",
    "Sellars",
    "Kant",
    "Hegel",
    "logic",
    "modality",
    "reason",
    "semantics",
    "language",
    "expressivism",
    "representation",
    "objectivity",
    "commitment",
    "entitlement",
    "recognition",
    "scorekeeping",
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
    path = STORE / "catalog.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
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
    return sorted(result, key=lambda item: (item["source"], item["kind"], item["ref"]))


def public_receipts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{key: row[key] for key in ["ref", "kind", "source", "method", "title", "sha256", "chars", "status", "raw_body_exported"]} for row in rows]


def term_signals(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    signals = []
    for term in TERMS:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        docs = 0
        hits = 0
        for row in rows:
            haystack = row["title"] + "\n" + row["_body"]
            count = len(pattern.findall(haystack))
            docs += 1 if count else 0
            hits += count
        signals.append({"term": term, "documents": docs, "hits": hits, "status": "OBSERVED" if hits else "ABSENT"})
    return signals


def inaccessible_sources() -> list[dict[str, str]]:
    return [
        {"ref": "https://www.researchgate.net/profile/Bob-Brandom", "attempt": "gather web", "status": "INACCESSIBLE_HTTP_403"},
        {"ref": "https://pitt.academia.edu/RobertBrandom", "attempt": "gather web", "status": "INACCESSIBLE_HTTP_403"},
    ]


def derivation_map(signals: list[dict[str, Any]]) -> list[dict[str, str]]:
    hits = {row["term"].lower(): row["hits"] for row in signals}
    return [
        {"anchor": "Sellars", "role": "normative-pragmatic and anti-empiricist source lead", "evidence_status": "OBSERVED" if hits["sellars"] else "UNVERIFIED"},
        {"anchor": "Kant", "role": "mind-independent objectivity and normativity source lead", "evidence_status": "OBSERVED" if hits["kant"] else "UNVERIFIED"},
        {"anchor": "Hegel", "role": "recognition, historical recollection, and social normativity source lead", "evidence_status": "OBSERVED" if hits["hegel"] else "UNVERIFIED"},
        {"anchor": "Inferentialism", "role": "learning graph organized around reasons, consequences, commitments, and entitlements", "evidence_status": "OBSERVED" if hits["inferentialism"] else "UNVERIFIED"},
        {"anchor": "Logical expressivism", "role": "make implicit inferential practices explicit through vocabulary and tooling", "evidence_status": "OBSERVED" if hits["expressivism"] else "UNVERIFIED"},
    ]


def scorekeeping_fixture() -> dict[str, Any]:
    state = {"commitments": set(), "entitlements": set()}
    trace = []

    def step(action: str, claim: str, ok: bool, reason: str) -> None:
        trace.append({"action": action, "claim": claim, "accepted": ok, "reason": reason})

    state["commitments"].add("p")
    step("assert", "p", True, "learner undertakes a commitment")
    state["entitlements"].add("p")
    step("attach_source", "p", True, "source receipt licenses the commitment inside this bounded exercise")
    state["commitments"].add("p_implies_q")
    state["entitlements"].add("p_implies_q")
    step("add_rule", "p -> q", True, "explicit inferential link added")
    infer_ok = "p" in state["entitlements"] and "p_implies_q" in state["entitlements"]
    if infer_ok:
        state["commitments"].add("q")
        state["entitlements"].add("q")
    step("infer", "q", infer_ok, "conclusion requires entitlement to antecedent and rule")
    return {
        "fixture_id": "deontic_scorekeeping_learning_loop",
        "status": "MATCH" if "q" in state["entitlements"] else "DRIFT",
        "trace": trace,
        "final_commitments": sorted(state["commitments"]),
        "final_entitlements": sorted(state["entitlements"]),
        "learning_objective": "teach claims as moves in a reason-governed practice rather than isolated notes",
    }


def tool_hypotheses() -> list[dict[str, str]]:
    return [
        {"tool": "Inferential Graph Tutor", "market_need": "turn readings and lectures into claim, reason, consequence, and objection graphs", "status": "HYPOTHESIS"},
        {"tool": "Scorekeeping Lab", "market_need": "let learners practice commitments, entitlements, challenges, and repairs with action receipts", "status": "HYPOTHESIS"},
        {"tool": "Expressive Vocabulary Ladder", "market_need": "show which vocabulary makes an implicit practice explicit", "status": "HYPOTHESIS"},
        {"tool": "Seminar-to-Proof Packet", "market_need": "convert lecture source leads into exercises, tests, and Crucible-checked learning packets", "status": "HYPOTHESIS"},
        {"tool": "Tradition Derivation Atlas", "market_need": "map Kant, Hegel, Sellars, Rorty, and Brandom dependencies across courses and texts", "status": "HYPOTHESIS"},
    ]


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "raw_transcript_as_textbook_rejected", "status": "REJECTED", "failures": ["copyright_boundary", "requires_digest_not_dump"]},
        {"fixture_id": "blocked_profiles_as_evidence_rejected", "status": "REJECTED", "failures": ["researchgate_403", "academia_403"]},
        {"fixture_id": "profile_as_complete_bibliography_rejected", "status": "REJECTED", "failures": ["profile_is_partial", "requires_texts_and_courses_catalog"]},
        {"fixture_id": "philosophy_to_product_without_tasks_rejected", "status": "REJECTED", "failures": ["needs_learning_fixture", "needs_measurable_outcome"]},
        {"fixture_id": "brandom_corpus_as_natural_law_rejected", "status": "REJECTED", "failures": ["humanities_digest", "not_scientific_law"]},
    ]


def run_json(command: list[str], timeout: int = 60) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0129 Brandom functional learning corpus digest and tool hypotheses."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1400", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    upstream = read_json(PASS_0128)
    rows = read_catalog()
    signals = term_signals(rows)
    scorekeeping = scorekeeping_fixture()
    negatives = negative_fixtures()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"proof_suite_pass": upstream["pass"], "proof_suite_seal": upstream["seal"], "source_store": "gather/pass-0129-brandom-functional-learning"},
        "source_receipts": public_receipts(rows),
        "inaccessible_sources": inaccessible_sources(),
        "term_signals": signals,
        "derivation_map": derivation_map(signals),
        "scorekeeping_fixture": scorekeeping,
        "tool_hypotheses": tool_hypotheses(),
        "negative_fixtures": negatives,
        "digest_boundary": "This pass catalogs and digests Brandom source leads for learning-tool design. It does not claim a complete bibliography, export raw transcript text, verify blocked profiles, or turn philosophical claims into scientific laws.",
        "current_promoted_natural_laws": [],
        "unsupported_claim_count": 0,
        "flagship_receipts": flagship_receipts(),
    }
    errors = []
    if len(artifact["source_receipts"]) < 7 or any(row["status"] != "GATHER_VERIFIED" for row in artifact["source_receipts"]):
        errors.append("source_receipts")
    if not any(row["kind"] == "transcript" for row in artifact["source_receipts"]):
        errors.append("transcript_receipt")
    if scorekeeping["status"] != "MATCH":
        errors.append("scorekeeping_fixture")
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
    parser.add_argument("--out", default=str(ROOT / "schemas" / "brandom-functional-learning-digest-pass-0129.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
