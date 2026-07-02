"""Generate pass 0049 wedge budget-signal scorecard receipts."""
from __future__ import annotations

import hashlib
import json
import urllib.request
from collections import Counter
from pathlib import Path


PASS = "0049"
ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PACKET = ROOT / "schemas" / "competitor-proof-gap-matrix-pass-0048.json"
OUT_PATH = ROOT / "schemas" / "wedge-budget-signal-scorecard-pass-0049.json"
FIXTURE_PATH = ROOT / "fixtures" / "wedge-budget-signal-scorecard-pass-0049.json"
PACKET_PATH = ROOT / "packets" / "059-wedge-budget-signal-scorecard.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0049-wedge-budget-signal-scorecard-steelman.md"


SOURCES = [
    ("agent_action_proof_packets", "LangSmith pricing", "https://www.langchain.com/pricing-langsmith", ["LangSmith", "pricing", "Free"]),
    ("agent_action_proof_packets", "Langfuse pricing", "https://langfuse.com/pricing", ["Langfuse", "pricing", "Pro"]),
    ("agent_action_proof_packets", "Braintrust pricing", "https://www.braintrust.dev/pricing", ["Braintrust", "pricing", "Free"]),
    ("agent_action_proof_packets", "Arize pricing", "https://arize.com/pricing", ["Arize", "pricing", "Enterprise"]),
    ("agent_action_proof_packets", "Humanloop pricing", "https://humanloop.com/pricing", ["Humanloop", "pricing", "Enterprise"]),
    ("agent_action_proof_packets", "Helicone pricing", "https://www.helicone.ai/pricing", ["Helicone", "pricing", "Free"]),
    ("agent_action_proof_packets", "promptfoo pricing", "https://www.promptfoo.dev/pricing", ["promptfoo", "pricing", "Enterprise"]),
    ("research_proof_packets", "Elicit pricing", "https://elicit.com/pricing", ["Elicit", "pricing", "Plus"]),
    ("research_proof_packets", "Consensus pricing", "https://consensus.app/pricing", ["Consensus", "pricing", "Pro"]),
    ("research_proof_packets", "Benchling pricing", "https://www.benchling.com/pricing", ["Benchling", "pricing", "demo"]),
    ("buildlang_runtime_receipts", "Calman products", "https://www.portrait.com/products/", ["Calman", "color", "calibration"]),
    ("buildlang_runtime_receipts", "ColourSpace products", "https://lightillusion.com/colourspace.html", ["ColourSpace", "colour", "calibration"]),
    ("buildlang_runtime_receipts", "JupyterHub", "https://jupyter.org/hub", ["JupyterHub", "users", "notebook"]),
    ("buildlang_runtime_receipts", "JuliaHub", "https://juliahub.com/", ["JuliaHub", "Julia", "cloud"]),
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
    market, label, url, needles = source
    request = urllib.request.Request(url, headers={"User-Agent": "telos-dogfood/0049"})
    with urllib.request.urlopen(request, timeout=35) as response:
        body = response.read()
    text = body.decode("utf-8", errors="replace").lower()
    contains = {needle: needle.lower() in text for needle in needles}
    return {
        "bytes": len(body),
        "contains": contains,
        "id": label.lower().replace(" ", "_"),
        "market": market,
        "sha256": sha256_bytes(body),
        "status": "MATCH" if all(contains.values()) else "DRIFT",
        "source_label": label,
        "url": url,
    }


def wedge_scores(budget_signal_counts: dict[str, int]) -> list[dict]:
    rows = [
        {
            "market": "agent_action_proof_packets",
            "urgency": 5,
            "budget": 5,
            "competitor_saturation": 4,
            "adoption_friction": 3,
            "demo_readiness": 5,
            "proof_advantage": 5,
            "distribution_path": 4,
            "strategic_upside": 5,
            "budget_signal_sources": budget_signal_counts.get("agent_action_proof_packets", 0),
            "primary_30_day_push": True,
        },
        {
            "market": "research_proof_packets",
            "urgency": 5,
            "budget": 4,
            "competitor_saturation": 3,
            "adoption_friction": 4,
            "demo_readiness": 4,
            "proof_advantage": 5,
            "distribution_path": 3,
            "strategic_upside": 5,
            "budget_signal_sources": budget_signal_counts.get("research_proof_packets", 0),
            "primary_30_day_push": False,
        },
        {
            "market": "buildlang_runtime_receipts",
            "urgency": 4,
            "budget": 4,
            "competitor_saturation": 3,
            "adoption_friction": 5,
            "demo_readiness": 3,
            "proof_advantage": 5,
            "distribution_path": 3,
            "strategic_upside": 5,
            "budget_signal_sources": budget_signal_counts.get("buildlang_runtime_receipts", 0),
            "primary_30_day_push": False,
        },
    ]
    for row in rows:
        row["weighted_rank_score"] = (
            row["urgency"]
            + row["budget"]
            + (6 - row["competitor_saturation"])
            + (6 - row["adoption_friction"])
            + row["demo_readiness"]
            + row["proof_advantage"]
            + row["distribution_path"]
            + row["strategic_upside"]
        )
    return sorted(rows, key=lambda row: row["weighted_rank_score"], reverse=True)


def thirty_day_plan() -> list[dict]:
    return [
        {"day_range": "1-7", "work": "Package an agent action proof packet around one real multi-tool task with source refs, workspace refs, model/tool calls, admission decision, and Crucible verdict."},
        {"day_range": "8-14", "work": "Turn the packet into a buyer-facing demo for AI infra teams, with LangSmith/Langfuse/Phoenix-style trace import/export as the bridge."},
        {"day_range": "15-21", "work": "Run pipeline-math++ through the same packet shape: source intake, proof artifact binding, adversarial review, and formal replay boundary."},
        {"day_range": "22-30", "work": "Add BuildLang/color/runtime receipts as the third demo path, proving measured output and compiler/runtime state can attach to the same proof object."},
    ]


def render_packet(contract: dict) -> str:
    lines = [
        "# Packet 059: Wedge Budget-Signal Scorecard",
        "",
        "Date: 2026-07-01",
        "",
        f"Status: `{contract['status']}`",
        "",
        "This pass converts the 45-row market matrix into a ranked buyer-urgency",
        "and budget-access scorecard. Pricing pages verify budget signaling;",
        "they do not prove willingness to buy Telos.",
        "",
        "| Rank | Market | Score | Budget signals | Primary push |",
        "| ---: | --- | ---: | ---: | --- |",
    ]
    for index, row in enumerate(contract["wedge_scores"], start=1):
        lines.append(f"| {index} | `{row['market']}` | {row['weighted_rank_score']} | {row['budget_signal_sources']} | `{row['primary_30_day_push']}` |")
    lines.extend([
        "",
        "Primary 30-day market push: `agent_action_proof_packets`.",
        "",
        "Reason: it has the strongest combination of urgent buyer pain, existing",
        "pricing/budget signals, demo readiness, and direct reuse as the substrate",
        "for research proof packets and BuildLang/runtime receipts.",
        "",
        "Current promoted natural laws: none.",
    ])
    return "\n".join(lines) + "\n"


def render_steelman() -> str:
    return """# Pass 0049 Steelman: Wedge Budget-Signal Scorecard

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

Pricing pages prove only that adjacent vendors package and sell into a market.
They do not prove Telos demand, procurement access, or uniqueness. The scorecard
is a prioritization artifact. It should be falsified by buyer interviews,
prototype usage, conversion data, and direct competitor feature comparison.
"""


def main() -> None:
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    receipts = [fetch_source(source) for source in SOURCES]
    budget_signal_counts = dict(Counter(row["market"] for row in receipts))
    scores = wedge_scores(budget_signal_counts)
    all_match = all(row["status"] == "MATCH" for row in receipts)
    fixture = with_seal({
        "budget_signal_source_receipts": receipts,
        "generated_on": "2026-07-01",
        "pass": PASS,
        "schema": "WedgeBudgetSignalScorecardFixture/v1",
        "wedge_scores": scores,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "budget_signal_counts": budget_signal_counts,
        "budget_signal_source_receipts": receipts,
        "current_promoted_natural_laws": [],
        "fixture": {"path": "fixtures/wedge-budget-signal-scorecard-pass-0049.json", "schema": fixture["schema"], "seal": fixture["seal"], "sha256": fixture_sha},
        "generated_on": "2026-07-01",
        "non_promotion_statement": "Pass 0049 ranks market wedges from source-backed pricing signals and explicit scoring assumptions. It does not prove product-market fit, uniqueness, buyer adoption, scientific truth, or any natural law.",
        "pass": PASS,
        "previous_pass_binding": {"path": "schemas/competitor-proof-gap-matrix-pass-0048.json", "seal": previous["seal"], "sha256": previous_sha, "source_status": previous["status"]},
        "primary_30_day_market_push": "agent_action_proof_packets",
        "schema": "WedgeBudgetSignalScorecardSet/v1",
        "scoring_note": "competitor_saturation and adoption_friction are inverted in weighted_rank_score because high raw values are headwinds.",
        "status": "WEDGE_BUDGET_SIGNAL_SCORECARD_MATCH" if all_match else "WEDGE_BUDGET_SIGNAL_SCORECARD_DRIFT",
        "thirty_day_plan": thirty_day_plan(),
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "verifier_measurements": {"budget_signal_source_count": len(receipts), "budget_signal_source_match_count": sum(1 for row in receipts if row["status"] == "MATCH"), "wedge_score_count": len(scores)},
        "wedge_scores": scores,
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "path": str(OUT_PATH),
        "primary_30_day_market_push": contract["primary_30_day_market_push"],
        "seal": contract["seal"],
        "source_match_count": contract["verifier_measurements"]["budget_signal_source_match_count"],
        "status": contract["status"],
        "wedge_order": [row["market"] for row in scores],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
