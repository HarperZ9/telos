"""Rendering helpers for pass 0145 multi-institution claim graph."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

SCHEMA = "MultiInstitutionClaimGraphReceipt/v1"


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_packet(r: dict[str, Any]) -> str:
    lines = [
        "# Pass 0145 - Multi-Institution Claim Graph",
        "",
        "## Summary",
        "",
        f"Status: `{r['status']}` with seal `{r['seal']}`.",
        f"The replay covers `{r['summary']['institutions']}` institutions and `{r['summary']['stored_captures']}` stored Gather captures.",
        "",
        "## Institution Verdicts",
        "",
        "| Institution | Identity | Repository | Crossref |",
        "| --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| {item['name']} | `{item['identity_status']}` | `{item['repository_status']}` | `{item['crossref_status']}` |"
        for item in r["institutions"]
    )
    lines.extend(
        [
            "",
            "## What Promoted",
            "",
            "- Four ROR/OpenAlex identity joins matched expected institution identifiers.",
            "- Four repository `Identify` captures matched expected OAI-PMH identity and protocol signals.",
            "- Three Crossref affiliation samples matched expected affiliation strings.",
            "",
            "## What Stayed Fenced",
            "",
            "- Cornell Crossref stayed `SOURCE_LEAD_ONLY` after rate limiting.",
            "- Caltech OAI endpoint documentation drift stayed a warning, not a silent normalization.",
            "- No publication truth, full-text access, repository completeness, theorem, or natural law was promoted.",
            "",
            "## Market Implication",
            "",
            r["market_implication"],
            "",
            "## Boundary",
            "",
            r["boundary"],
        ]
    )
    return "\n".join(lines)


def render_brief(r: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Pass 0145 Brief - Multi-Institution Claim Graph",
            "",
            "Primary push: turn one-institution source proof into a replayable registry adapter for research labs.",
            "",
            f"Result: {r['summary']['identity_matches']} identity joins, {r['summary']['repository_matches']} repository joins, and {r['summary']['crossref_matches']} Crossref joins matched across four institutions, with warnings preserved.",
            "",
            "Product lesson: the proof packet wedge is not the source fetch alone. It is the refusal to promote rate-limited, endpoint-drifted, or sample-only evidence into stronger claims.",
            "",
            "Next pass: add pagination and retry policy fixtures, then run the same contract over a broader institution queue.",
        ]
    )


def render_steelman() -> str:
    return "\n".join(
        [
            "# Pass 0145 Steelman",
            "",
            "The strongest objection is that four elite institutions are still a narrow, English-heavy, API-friendly sample. A stronger registry adapter must survive non-US institutions, multilingual names, repository redirects, OAI set partitions, affiliation ambiguity, and source systems that block anonymous clients.",
            "",
            "The settling test is an adapter runner that treats every source family as typed evidence: identity, repository protocol, sampled work metadata, dataset relation, full-text relation, license, and negative fixtures all need separate verdicts before any claim can promote.",
        ]
    )


def build_claims(r: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    claims = [
        f"Pass 0145 created a {SCHEMA} artifact with status {r['status']} and seal {r['seal']}.",
        f"Pass 0145 records {r['summary']['institutions']} institutions and {r['summary']['stored_captures']} stored captures.",
        f"Pass 0145 records {r['summary']['identity_matches']} identity matches, {r['summary']['repository_matches']} repository matches, and {r['summary']['crossref_matches']} Crossref matches.",
        f"Pass 0145 rejects {len(r['negative_fixtures'])} negative fixtures and records {len(r['source_warnings'])} warnings.",
        "Pass 0145 promotes no theorem or natural law.",
    ]
    thesis = {
        "title": "Dogfood Pass 0145 Multi-Institution Claim Graph",
        "disposition": "fenced",
        "claims": [
            {"text": claim, "falsification": f"Claim {i} differs from artifact values or receipts are missing"}
            for i, claim in enumerate(claims, 1)
        ],
    }
    evidence = [
        [f"schema={r['schema']}", f"status={r['status']}", f"seal={r['seal']}"],
        [f"summary={r['summary']}"],
        [f"join_verdicts={r['join_verdicts']}"],
        [f"negative_fixtures={len(r['negative_fixtures'])}", f"source_warnings={len(r['source_warnings'])}"],
        [f"current_promoted_theorems={r['current_promoted_theorems']}", f"current_promoted_natural_laws={r['current_promoted_natural_laws']}"],
    ]
    return thesis, {
        "measurements": [
            {"claim": claim, "method": "artifact-review", "evidence": evidence[i], "deviation": 0.0, "tolerance": 0.5}
            for i, claim in enumerate(claims)
        ]
    }


def render_ledger(r: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0145 Ledger - Multi-Institution Claim Graph", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    lines.extend(f"| {label} | {sha_file(path).upper()} |" for label, path in files.items())
    lines.extend(
        [
            "",
            "## Result Snapshot",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Schema | `{r['schema']}` |",
            f"| Status | `{r['status']}` |",
            f"| Seal | `{r['seal']}` |",
            f"| Institutions | `{r['summary']['institutions']}` |",
            f"| Stored captures | `{r['summary']['stored_captures']}` |",
            f"| Identity matches | `{r['summary']['identity_matches']}` |",
            f"| Repository matches | `{r['summary']['repository_matches']}` |",
            f"| Crossref matches | `{r['summary']['crossref_matches']}` |",
            f"| Warnings | `{r['summary']['warnings']}` |",
            f"| Promoted theorems | `{len(r['current_promoted_theorems'])}` |",
        ]
    )
    return "\n".join(lines)
