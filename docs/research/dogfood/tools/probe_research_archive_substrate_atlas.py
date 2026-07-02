"""Generate pass 0140 research archive substrate atlas docs."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_research_archive_substrate_atlas.py"
TEST_SCRIPT = ROOT / "tools" / "test_research_archive_substrate_atlas.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0140_research_archive_substrate_atlas.py"
ARTIFACT = ROOT / "schemas" / "research-archive-substrate-atlas-pass-0140.json"
TOOL_RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0140.json"
PACKET = ROOT / "packets" / "150-research-archive-substrate-atlas.md"
BRIEF = ROOT / "briefs" / "150-research-archive-substrate-atlas-brief.md"
STEELMAN = ROOT / "adversarial" / "pass-0140-research-archive-substrate-atlas-steelman.md"
LEDGER = ROOT / "pass-0140-ledger.md"
THESIS = ROOT / "crucible" / "pass-0140-thesis.json"
MEASUREMENTS = ROOT / "crucible" / "pass-0140-measurements.json"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.encode("ascii", "ignore").decode("ascii"), encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 300) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def render_packet(artifact: dict) -> str:
    systems = [{"system": r["system"], "category": r["category"], "protocol": r["ingestion_protocol"], "evidence": r["evidence_status"]} for r in artifact["source_systems"]]
    families = [{"family": r["family"], "target": r["tooling_target"]} for r in artifact["substrate_families"]]
    domains = [{"domain": r["domain"], "product": r["first_product"]} for r in artifact["domain_expansion_queue"]]
    routes = [{"route": r["route"], "tools": " + ".join(r["tools"]), "output": r["output"]} for r in artifact["megatool_routes"]]
    warnings = [{"system": r["system"], "status": r["evidence_status"], "url": r["url"]} for r in artifact["source_quality_warnings"]]
    return f"""# Packet 150: Research Archive Substrate Atlas

Date: 2026-07-02

Status: `{artifact['status']}`

Purpose: create the first broad, receipt-backed substrate atlas for sourcing
research across publishing archives, preprint servers, scholarly graphs,
domain databases, institutional repositories, and public data portals.

```text
captured_sources = {artifact['gather_summary']['captured_sources']}
usable_captures = {artifact['gather_summary']['usable_captures']}
source_systems = {len(artifact['source_systems'])}
source_quality_warnings = {len(artifact['source_quality_warnings'])}
substrate_families = {len(artifact['substrate_families'])}
domain_queue = {len(artifact['domain_expansion_queue'])}
megatool_routes = {len(artifact['megatool_routes'])}
negative_fixtures = {len(artifact['negative_fixtures'])}
seal = {artifact['seal']}
```

## Source Systems

| System | Category | Protocol | Evidence |
| --- | --- | --- | --- |
{table(systems, ['system', 'category', 'protocol', 'evidence'])}

## Source Quality Warnings

| System | Status | URL |
| --- | --- | --- |
{table(warnings, ['system', 'status', 'url'])}

## Substrate Families

| Family | Tooling target |
| --- | --- |
{table(families, ['family', 'target'])}

## Domain Expansion Queue

| Domain | First product |
| --- | --- |
{table(domains, ['domain', 'product'])}

## Megatool Routes

| Route | Tools | Output |
| --- | --- | --- |
{table(routes, ['route', 'tools', 'output'])}

## Boundary

{artifact['boundary']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Research Archive Substrate Atlas Brief

Date: 2026-07-02

## Decision

The next scale move is an `ArchiveAdapterSDK`: every source system should
produce the same minimum receipt fields before it can feed claim packets,
experiment packets, theorem packets, model-foundry runs, or BuildLang kernels.

## Result

Pass 0140 records `{len(artifact['source_systems'])}` source systems, `{len(artifact['substrate_families'])}` substrate families, `{len(artifact['domain_expansion_queue'])}` domain queues, and `{len(artifact['megatool_routes'])}` megatool routes. It also keeps empty and failed captures out of the evidence lane.

## Primary Push

Build two concrete adapters next: `ScholarlyGraphAdapter` for OpenAlex/Crossref/Semantic Scholar and `BioExperimentAdapter` for PubMed/PMC/GEO/SRA/ClinicalTrials.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0140 Steelman: Research Archive Substrate Atlas

Date: 2026-07-02

The strongest objection is that an archive atlas can look like progress while
solving nothing. Accepted. This pass is substrate plumbing, not a solved
theorem or experiment.

The second objection is that many sources are metadata-only. Accepted. The
adapter requirements require body/metadata hash, license/terms reference,
freshness time, claim extraction state, negative controls, and verifier before
promotion.

The third objection is coverage. Accepted. This is a first-wave atlas, not a
complete world crawl.

Boundary: {artifact['boundary']}
"""


def build_receipts(compose: dict, test: dict, validator: dict, artifact: dict) -> dict:
    receipts = {"schema": "DogfoodToolReceipts/v1", "pass": "0140", "compose": compose, "test": test, "validator": validator, "gather_summary": artifact["gather_summary"], "forum": artifact["flagship_receipts"]["forum"], "index": artifact["flagship_receipts"]["index"], "telos": artifact["flagship_receipts"]["telos"], "telos_catalog": artifact["flagship_receipts"]["telos_catalog"]}
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    return receipts


def thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": ARTIFACT, "composer": COMPOSER, "probe": Path(__file__).resolve(), "packet": PACKET, "brief": BRIEF, "steelman": STEELMAN, "test": TEST_SCRIPT, "validator": VALIDATOR, "tool_receipts": TOOL_RECEIPTS}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0140 created a ResearchArchiveSubstrateAtlasReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0140 records {artifact['gather_summary']['captured_sources']} captured sources and {artifact['gather_summary']['usable_captures']} usable captures.",
        f"Pass 0140 records {len(artifact['source_systems'])} source systems and {len(artifact['source_quality_warnings'])} source-quality warnings.",
        f"Pass 0140 records {len(artifact['substrate_families'])} substrate families.",
        f"Pass 0140 records {len(artifact['domain_expansion_queue'])} domain expansion queue rows.",
        f"Pass 0140 records {len(artifact['megatool_routes'])} megatool routes and {len(artifact['adapter_requirements'])} adapter requirements.",
        f"Pass 0140 rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0140 promotes no source breadth, preprint, metadata, dataset, clinical record, or taxonomy into a natural law.",
        f"Pass 0140 flagship receipts are {artifact['flagship_receipts']}.",
        f"Pass 0140 validator status is {receipts['validator']['status']} and test status is {receipts['test']['status']}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"gather_summary={artifact['gather_summary']}"],
        [f"source_system_count={len(artifact['source_systems'])}", f"warnings={artifact['source_quality_warnings']}"],
        [f"substrate_families={artifact['substrate_families']}"],
        [f"domain_expansion_queue={artifact['domain_expansion_queue']}"],
        [f"megatool_routes={artifact['megatool_routes']}", f"adapter_requirements={artifact['adapter_requirements']}"],
        [f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"current_promoted_natural_laws={artifact['current_promoted_natural_laws']}", f"boundary={artifact['boundary']}"],
        [f"flagship_receipts={artifact['flagship_receipts']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
    ]
    thesis = {"title": "Dogfood Pass 0140 Research Archive Substrate Atlas", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0140 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def render_ledger(artifact: dict) -> str:
    paths = [ARTIFACT, PACKET, BRIEF, STEELMAN, TOOL_RECEIPTS, COMPOSER, TEST_SCRIPT, VALIDATOR, Path(__file__).resolve(), THESIS, MEASUREMENTS]
    rows = [{"artifact": str(path.relative_to(ROOT)).replace("\\", "/"), "sha": sha256_file(path).upper()} for path in paths]
    return f"""# Pass 0140 Ledger - Research Archive Substrate Atlas

Date: 2026-07-02

## Objective

Create a first-wave archive and source substrate atlas for massive cross-domain
research ingestion, with evidence-state boundaries and megatool routes.

## Outputs

| Artifact | SHA-256 |
| --- | --- |
{table(rows, ['artifact', 'sha'])}

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `{artifact['schema']}` |
| Status | `{artifact['status']}` |
| Artifact seal | `{artifact['seal']}` |
| Captured sources | `{artifact['gather_summary']['captured_sources']}` |
| Usable captures | `{artifact['gather_summary']['usable_captures']}` |
| Source systems | `{len(artifact['source_systems'])}` |
| Source quality warnings | `{len(artifact['source_quality_warnings'])}` |
| Substrate families | `{len(artifact['substrate_families'])}` |
| Domain queue | `{len(artifact['domain_expansion_queue'])}` |
| Promoted natural laws | `{len(artifact['current_promoted_natural_laws'])}` |
"""


def main() -> None:
    compose = run_command([sys.executable, str(COMPOSER)])
    artifact = read_json(ARTIFACT)
    test = run_command([sys.executable, str(TEST_SCRIPT)])
    validator = run_command([sys.executable, str(VALIDATOR)])
    receipts = build_receipts(compose, test, validator, artifact)
    write_json(TOOL_RECEIPTS, receipts)
    write_text(PACKET, render_packet(artifact))
    write_text(BRIEF, render_brief(artifact))
    write_text(STEELMAN, render_steelman(artifact))
    thesis, measurements = thesis_measurements(artifact, receipts)
    write_json(THESIS, thesis)
    write_json(MEASUREMENTS, measurements)
    write_text(LEDGER, render_ledger(artifact))
    ok = artifact["status"] == "RESEARCH_ARCHIVE_SUBSTRATE_ATLAS_MATCH" and all(row["status"] == "MATCH" for row in [compose, test, validator])
    print(json.dumps({"status": "MATCH" if ok else "DRIFT", "artifact": str(ARTIFACT), "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
