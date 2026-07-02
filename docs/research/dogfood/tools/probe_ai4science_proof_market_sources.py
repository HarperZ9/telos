"""Generate pass 0047 AI4Science proof-market source receipts."""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path


PASS = "0047"
ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PACKET = ROOT / "schemas" / "elan-controlled-install-plan-pass-0046.json"
OUT_PATH = ROOT / "schemas" / "ai4science-proof-market-sources-pass-0047.json"
FIXTURE_PATH = ROOT / "fixtures" / "ai4science-proof-market-sources-pass-0047.json"
PACKET_PATH = ROOT / "packets" / "057-ai4science-proof-market-sources.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0047-ai4science-proof-market-sources-steelman.md"
SOURCES = [
    ("pipeline_math", "formal-math", "https://github.com/Pengbinghui/pipeline-math", ["prover", "verifier", "Lean"]),
    ("sakana_ai_scientist", "automated-research", "https://sakana.ai/ai-scientist/", ["fully automatic scientific discovery", "research lifecycle", "automated peer review"]),
    ("futurehouse", "scientific-agents", "https://www.futurehouse.org/", ["FutureHouse", "scientific discovery", "agents"]),
    ("microsoft_discovery", "enterprise-rd", "https://azure.microsoft.com/en-us/blog/transforming-rd-with-agentic-ai-introducing-microsoft-discovery/", ["Microsoft Discovery", "agentic AI", "research"]),
    ("nvidia_bionemo", "bio-platform", "https://www.nvidia.com/en-us/industries/healthcare-life-sciences/", ["BioNeMo", "healthcare", "life sciences"]),
    ("leandojo", "formal-proving", "https://leandojo.org/", ["LeanDojo", "theorem proving", "Lean"]),
    ("deepmind_alphaproof", "formal-math", "https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/", ["AlphaProof", "AlphaGeometry", "International Mathematical Olympiad"]),
    ("openalex_docs", "literature-graph", "https://docs.openalex.org/", ["works", "authors", "sources"]),
    ("semantic_scholar_api", "literature-api", "https://www.semanticscholar.org/product/api", ["Semantic Scholar", "API", "paper"]),
    ("nextflow", "scientific-workflows", "https://www.nextflow.io/", ["Nextflow", "workflows", "data"]),
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def fetch_source(source: tuple[str, str, str, list[str]]) -> dict:
    source_id, category, url, needles = source
    request = urllib.request.Request(url, headers={"User-Agent": "telos-dogfood/0047"})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
    text = body.decode("utf-8", errors="replace").lower()
    contains = {needle: needle.lower() in text for needle in needles}
    return {
        "bytes": len(body),
        "category": category,
        "contains": contains,
        "id": source_id,
        "sha256": sha256_bytes(body),
        "status": "MATCH" if all(contains.values()) else "DRIFT",
        "url": url,
    }


def matrix_rows() -> list[dict]:
    return [
        {"market": "research-proof-packets", "urgency": 5, "proof_advantage": 5, "demo_readiness": 4, "risk": "formal replay and external review still gated"},
        {"market": "agentic-rd-ledgers", "urgency": 4, "proof_advantage": 5, "demo_readiness": 4, "risk": "buyer education and workflow integration"},
        {"market": "bio-workflow-provenance", "urgency": 4, "proof_advantage": 4, "demo_readiness": 3, "risk": "domain validation and compliance depth"},
        {"market": "literature-to-claim-graphs", "urgency": 3, "proof_advantage": 4, "demo_readiness": 5, "risk": "crowded retrieval market"},
        {"market": "scientific-workflow-receipts", "urgency": 4, "proof_advantage": 4, "demo_readiness": 4, "risk": "integration with existing workflow engines"},
    ]


def render_packet(contract: dict) -> str:
    m = contract["verifier_measurements"]
    return f"""# Packet 057: AI4Science Proof-Market Sources

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0047 gathers ten current source anchors for the research-proof market:
automated research systems, formal math/proof systems, scientific agents,
bio/R&D platforms, literature graphs, and workflow engines.

```text
source_count = {m['source_count']}
source_match_count = {m['source_match_count']}
category_count = {m['category_count']}
wedge_count = {m['wedge_count']}
uniqueness_claim_status = HYPOTHESIS_ONLY
```

Primary wedge hypothesis: competitors increasingly automate pieces of research,
but the market still needs portable claim-to-proof packets that bind sources,
model/tool actions, workspace state, verification verdicts, and reproducibility
receipts. This is a hypothesis until tested against deeper competitor matrices.

Top market push: publish a public `pipeline-math++` proof packet demo that shows
source intake, formal artifact binding, adversarial steelman, and Crucible
verdicts without claiming unsolved semantic proof.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0047 Steelman: AI4Science Proof-Market Sources

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This source matrix does not prove market demand, product-market fit, or
technical uniqueness. It proves that the named public sources exist and support
the classification used in the packet. Any statement that Telos is uniquely
positioned remains a hypothesis until a full competitor-by-feature comparison
and buyer interviews are added.
"""


def main() -> None:
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    receipts = [fetch_source(source) for source in SOURCES]
    rows = matrix_rows()
    fixture = with_seal({
        "generated_on": "2026-07-01",
        "pass": PASS,
        "schema": "AI4ScienceProofMarketSourcesFixture/v1",
        "source_receipts": receipts,
        "wedge_rows": rows,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    categories = sorted({row["category"] for row in receipts})
    all_match = all(row["status"] == "MATCH" for row in receipts)
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0047_ai4science_proof_market_sources",
            "authority_class": "read_only_external_source_fetch",
            "event_id": "evt_dogfood_0047_ai4science_proof_market_sources",
            "event_type": "ai4science_proof_market_sources_verified",
            "external_call_performed": True,
            "external_write_performed": False,
            "verification_verdict": "MATCH" if all_match else "DRIFT",
        },
        "controlled_install_plan_binding": {
            "path": "schemas/elan-controlled-install-plan-pass-0046.json",
            "seal": previous["seal"],
            "sha256": previous_sha,
            "source_status": previous["status"],
        },
        "current_promoted_natural_laws": [],
        "fixture": {
            "path": "fixtures/ai4science-proof-market-sources-pass-0047.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "generated_on": "2026-07-01",
        "non_promotion_statement": "Pass 0047 is a source-backed market/research matrix only. It does not prove product-market fit, uniqueness, buyer adoption, scientific truth, or any natural law.",
        "pass": PASS,
        "schema": "AI4ScienceProofMarketSourcesSet/v1",
        "source_receipts": receipts,
        "status": "AI4SCIENCE_PROOF_MARKET_SOURCES_MATCH" if all_match else "AI4SCIENCE_PROOF_MARKET_SOURCES_DRIFT",
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "verifier_measurements": {
            "category_count": len(categories),
            "source_count": len(receipts),
            "source_match_count": sum(1 for row in receipts if row["status"] == "MATCH"),
            "wedge_count": len(rows),
        },
        "wedge_rows": rows,
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "path": str(OUT_PATH),
        "schema": contract["schema"],
        "seal": contract["seal"],
        "source_match_count": contract["verifier_measurements"]["source_match_count"],
        "status": contract["status"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
