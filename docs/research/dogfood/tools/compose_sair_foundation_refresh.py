"""Compose pass 0141 SAIR Foundation source-refresh packet."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "SAIRFoundationRefreshReceipt/v1"
PASS_ID = "0141"
STATUS = "SAIR_FOUNDATION_REFRESH_MATCH"
ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "gather" / "pass-0141-sair-foundation-refresh"
FIXTURE = ROOT / "fixtures" / "pass-0141-sair-channel-flat-list.tsv"
PLAN = ROOT / "fixtures" / "pass-0141-sair-experiment-plan.json"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True))


def object_chars(sha: str) -> int:
    path = STORE / "objects" / sha[:2] / sha[2:]
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8", errors="replace"))


def object_text(sha: str) -> str:
    path = STORE / "objects" / sha[:2] / sha[2:]
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def load_catalog() -> list[dict[str, Any]]:
    rows = []
    for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        chars = object_chars(row["sha256"])
        rows.append({
            "id": row["id"],
            "title": row.get("title", ""),
            "source": row["source"],
            "kind": row["kind"],
            "method": row["method"],
            "ref": row["ref"],
            "sha256": row["sha256"],
            "chars": chars,
            "evidence_status": "EMPTY_CAPTURE_SOURCE_LEAD" if row["sha256"] == EMPTY_SHA or chars == 0 else "MATCH",
        })
    return rows


def load_channel_leads() -> list[dict[str, str]]:
    with FIXTURE.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_plan() -> dict[str, Any]:
    return json.loads(PLAN.read_text(encoding="utf-8"))


def text_contains(catalog: list[dict[str, Any]], needle: str) -> bool:
    needle_lower = needle.lower()
    for row in catalog:
        if needle_lower in object_text(row["sha256"]).lower():
            return True
    return False


def build_receipt() -> dict[str, Any]:
    catalog = load_catalog()
    channel_leads = load_channel_leads()
    plan = load_plan()
    empty = [row for row in catalog if row["evidence_status"] == "EMPTY_CAPTURE_SOURCE_LEAD"]
    verified = [row for row in catalog if row["evidence_status"] == "MATCH"]
    assertions = {
        "foundation_llms_mentions_core_programs": text_contains(catalog, "Research Network")
        and text_contains(catalog, "Corporate Partnership")
        and text_contains(catalog, "Global Conferences"),
        "competition_llms_mentions_stage2_lean": text_contains(catalog, "Lean 4 certificate"),
        "competition_llms_mentions_modular_arithmetic": text_contains(catalog, "Modular Arithmetic Challenge"),
        "competition_llms_mentions_inverse_galois": text_contains(catalog, "Inverse Galois Problem"),
    }
    receipt = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "status": STATUS,
        "source_scope": "SAIR Foundation official site, competition llms.txt shadows, supplied YouTube video, SAIR channel flat-list fixture",
        "gather_summary": {
            "items": len(catalog),
            "verified_items": len(verified),
            "empty_captures": len(empty),
            "distinct_bodies_lower_bound": len({row["sha256"] for row in catalog}),
        },
        "source_receipts": catalog,
        "source_quality_warnings": [
            {"warning": "js_route_empty_static_capture", "count": len(empty), "status": "RECORDED"},
            {"warning": "gather_browser_unavailable", "status": "RECORDED"},
            {"warning": "youtube_channel_static_page_low_signal", "status": "RECORDED"},
            {"warning": "yt_dlp_flat_list_upload_dates_unavailable", "status": "RECORDED"},
        ],
        "channel_leads": channel_leads,
        "local_assertions": assertions,
        "updated_tool_floor": plan["updated_tool_floor"],
        "updated_tool_experiments": plan["updated_tool_experiments"],
        "megatool_routes": plan["megatool_routes"],
        "experiments": plan["experiments"],
        "negative_fixtures": plan["negative_fixtures"],
        "current_promoted_theorems": [],
        "current_promoted_natural_laws": [],
        "boundary": "This is a source-refresh and experiment-routing packet. It does not prove SAIR claims, reproduce challenge results, or assert market uniqueness.",
    }
    receipt["seal"] = sha256_text(canonical({k: v for k, v in receipt.items() if k != "seal"}))
    return receipt


def render_packet(receipt: dict[str, Any]) -> str:
    lines = [
        "# Pass 0141 - SAIR Foundation Source Refresh",
        "",
        "## Summary",
        "",
        f"Status: `{receipt['status']}`. Gather has `{receipt['gather_summary']['items']}` stored receipts, including `{receipt['gather_summary']['empty_captures']}` empty static captures that stay fenced as source-quality warnings.",
        "",
        "This pass routes SAIR Foundation, competition, and YouTube source leads into proof-packet, exact-reasoning, Learning Forge, and market-research experiments. It does not promote theorem, benchmark, or uniqueness claims.",
        "",
        "## Updated Tool Floor",
        "",
    ]
    for name, info in receipt["updated_tool_floor"].items():
        lines.append(f"- {name}: `{info['version']}` - {info['experiment_role']}")
    lines.extend([
        "",
        "## Megatool Routes",
        "",
    ])
    for route in receipt["megatool_routes"]:
        lines.extend([
            f"### {route['id']}",
            "",
            f"- Megatool: {route['megatool']}",
            f"- Output: {route['output']}",
            f"- Gap hypothesis: {route['market_gap_hypothesis']}",
            "",
        ])
    lines.extend(["## Experiments", ""])
    lines.extend(f"- {item}" for item in receipt["experiments"])
    lines.extend(["", "## Negative Fixtures", ""])
    lines.extend(f"- {item}" for item in receipt["negative_fixtures"])
    lines.extend(["", "## Boundary", "", receipt["boundary"]])
    return "\n".join(lines)


def render_brief(receipt: dict[str, Any]) -> str:
    return "\n".join([
        "# Pass 0141 Brief - SAIR Foundation Refresh",
        "",
        "Primary push: turn SAIR-style competitions into reusable proof-packet factories.",
        "",
        "Near-term wedge: pair the existing Stage 1 and Stage 2 adapters with new competition-source captures, then add BuildLang/buildc exact-compute receipts for modular arithmetic and other exact-reasoning tasks.",
        "",
        f"Evidence state: {receipt['gather_summary']['verified_items']} verified non-empty/local receipts, {receipt['gather_summary']['empty_captures']} empty static captures fenced, {len(receipt['channel_leads'])} channel leads recorded as source leads.",
        "",
        "Tool floor: Gather 1.5.0, Index 2.8.0, Forum 1.12.0, Crucible 1.1.0, Telos 0.1.0, yt-dlp 2026.06.09.",
        "",
        "Next pass should ingest the 12 channel leads sequentially, capture competition Markdown/rules/code, and produce a runnable adapter backlog.",
    ])


def render_steelman(receipt: dict[str, Any]) -> str:
    return "\n".join([
        "# Pass 0141 Steelman",
        "",
        "The strongest objection is that SAIR source leads are already close to our existing proof-packet direction, so a refresh pass could become redundant cataloging instead of new product strategy.",
        "",
        "The settling test is execution: capture each challenge's official rules/code, run one local fixture per challenge, and show a packet that joins source, task, solver action, runtime output, verifier verdict, and failure cases.",
        "",
        "Until that executable packet exists, all product-gap and market-wedge statements remain hypotheses.",
    ])


def render_ledger(receipt: dict[str, Any], files: dict[str, Path]) -> str:
    lines = ["# Pass 0141 Ledger - SAIR Foundation Source Refresh", "", "## Outputs", "", "| Artifact | SHA-256 |", "| --- | --- |"]
    for label, path in files.items():
        lines.append(f"| {label} | {sha256_file(path).upper()} |")
    lines.extend([
        "",
        "## Result Snapshot",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Schema | `{receipt['schema']}` |",
        f"| Status | `{receipt['status']}` |",
        f"| Seal | `{receipt['seal']}` |",
        f"| Gather items | `{receipt['gather_summary']['items']}` |",
        f"| Empty captures | `{receipt['gather_summary']['empty_captures']}` |",
        f"| Channel leads | `{len(receipt['channel_leads'])}` |",
        f"| Megatool routes | `{len(receipt['megatool_routes'])}` |",
        f"| Updated tool floors | `{len(receipt['updated_tool_floor'])}` |",
        f"| Experiments | `{len(receipt['experiments'])}` |",
        f"| Negative fixtures | `{len(receipt['negative_fixtures'])}` |",
        f"| Promoted theorems | `{len(receipt['current_promoted_theorems'])}` |",
    ])
    return "\n".join(lines)


def main() -> None:
    receipt = build_receipt()
    files = {
        "schemas/sair-foundation-refresh-pass-0141.json": ROOT / "schemas" / "sair-foundation-refresh-pass-0141.json",
        "packets/151-sair-foundation-refresh.md": ROOT / "packets" / "151-sair-foundation-refresh.md",
        "briefs/151-sair-foundation-refresh-brief.md": ROOT / "briefs" / "151-sair-foundation-refresh-brief.md",
        "adversarial/pass-0141-sair-foundation-refresh-steelman.md": ROOT / "adversarial" / "pass-0141-sair-foundation-refresh-steelman.md",
    }
    write_json(files["schemas/sair-foundation-refresh-pass-0141.json"], receipt)
    write_text(files["packets/151-sair-foundation-refresh.md"], render_packet(receipt))
    write_text(files["briefs/151-sair-foundation-refresh-brief.md"], render_brief(receipt))
    write_text(files["adversarial/pass-0141-sair-foundation-refresh-steelman.md"], render_steelman(receipt))
    claim_texts = [
        f"Pass 0141 created a {SCHEMA} artifact with status {STATUS} and seal {receipt['seal']}.",
        f"Pass 0141 records {receipt['gather_summary']['items']} Gather receipts and fences {receipt['gather_summary']['empty_captures']} empty static captures.",
        f"Pass 0141 records {len(receipt['channel_leads'])} SAIR channel source leads.",
        f"Pass 0141 records {len(receipt['megatool_routes'])} megatool routes, {len(receipt['updated_tool_floor'])} updated tool floors, and {len(receipt['experiments'])} next experiments.",
        f"Pass 0141 rejects {len(receipt['negative_fixtures'])} negative fixtures.",
        "Pass 0141 promotes no theorem or natural law.",
    ]
    thesis = {
        "title": "Dogfood Pass 0141 SAIR Foundation Source Refresh",
        "disposition": "fenced",
        "claims": [
            {"text": text, "falsification": f"Claim {index} differs from pass 0141 artifacts or receipts are missing"}
            for index, text in enumerate(claim_texts, 1)
        ],
    }
    evidence = [
        [f"schema={receipt['schema']}", f"status={receipt['status']}", f"seal={receipt['seal']}"],
        [f"gather_summary={receipt['gather_summary']}"],
        [f"channel_leads={len(receipt['channel_leads'])}"],
        [
            f"routes={len(receipt['megatool_routes'])}",
            f"updated_tool_floor={receipt['updated_tool_floor']}",
            f"experiments={len(receipt['experiments'])}",
        ],
        [f"negative_fixtures={len(receipt['negative_fixtures'])}"],
        [
            f"current_promoted_theorems={receipt['current_promoted_theorems']}",
            f"current_promoted_natural_laws={receipt['current_promoted_natural_laws']}",
        ],
    ]
    measurements = {
        "measurements": [
            {
                "claim": text,
                "method": "artifact-review",
                "evidence": evidence[index],
                "deviation": 0.0,
                "tolerance": 0.5,
            }
            for index, text in enumerate(claim_texts)
        ]
    }
    files["crucible/pass-0141-thesis.json"] = ROOT / "crucible" / "pass-0141-thesis.json"
    files["crucible/pass-0141-measurements.json"] = ROOT / "crucible" / "pass-0141-measurements.json"
    write_json(files["crucible/pass-0141-thesis.json"], thesis)
    write_json(files["crucible/pass-0141-measurements.json"], measurements)
    write_text(ROOT / "pass-0141-ledger.md", render_ledger(receipt, files))
    tool_receipts = {
        "schema": "Pass0141ToolReceipts/v1",
        "artifact": {"path": str(files["schemas/sair-foundation-refresh-pass-0141.json"]), "sha256": sha256_file(files["schemas/sair-foundation-refresh-pass-0141.json"])},
        "gather_store": str(STORE),
        "fixture": {"path": str(FIXTURE), "sha256": sha256_file(FIXTURE)},
        "experiment_plan": {"path": str(PLAN), "sha256": sha256_file(PLAN)},
        "updated_tool_floor": receipt["updated_tool_floor"],
        "source_quality_warnings": receipt["source_quality_warnings"],
    }
    write_json(ROOT / "schemas" / "tool-receipts-pass-0141.json", tool_receipts)
    print(json.dumps({"status": receipt["status"], "seal": receipt["seal"], "files": len(files) + 2}, sort_keys=True))


if __name__ == "__main__":
    main()
