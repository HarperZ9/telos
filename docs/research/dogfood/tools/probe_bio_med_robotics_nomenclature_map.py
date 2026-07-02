"""Generate pass 0135 broad research substrate artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_bio_med_robotics_nomenclature_map.py"
TEST_SCRIPT = ROOT / "tools" / "test_bio_med_robotics_nomenclature_map.py"
VALIDATOR = ROOT / "tools" / "validate_pass_0135_bio_med_robotics_nomenclature_map.py"
ARTIFACT = ROOT / "schemas" / "bio-med-robotics-nomenclature-map-pass-0135.json"
VALIDATOR_RESULT = ROOT / "schemas" / "pass-0135-bio-med-robotics-nomenclature-map-validator-result.json"
TOOL_RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0135.json"
PACKET = ROOT / "packets" / "145-bio-med-robotics-nomenclature-map.md"
BRIEF = ROOT / "briefs" / "145-wide-research-substrate-brief.md"
STEELMAN = ROOT / "adversarial" / "pass-0135-wide-research-substrate-steelman.md"
THESIS = ROOT / "crucible" / "pass-0135-thesis.json"
MEASUREMENTS = ROOT / "crucible" / "pass-0135-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.encode("ascii", "ignore").decode("ascii"), encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_command(command: list[str], timeout: int = 180) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "status": "MATCH" if result.returncode == 0 else "DRIFT"}


def table(rows: list[dict], cols: list[str]) -> str:
    return "\n".join("| " + " | ".join(str(row.get(col, "")).replace("|", "/") for col in cols) + " |" for row in rows)


def render_packet(artifact: dict, receipts: dict) -> str:
    lanes = [{"lane": row["lane_id"], "bio": ", ".join(row["biology_terms"][:2]), "med": ", ".join(row["medicine_terms"][:2]), "robotics": ", ".join(row["robotics_terms"][:2]), "tool": row["tool_product_hypothesis"]} for row in artifact["domain_lanes"]]
    archives = [{"name": row["name"], "kind": row["kind"], "coverage": row["coverage"]} for row in artifact["archive_substrate_catalog"]]
    domains = [{"domain": row["domain"], "target": row["first_tooling_target"]} for row in artifact["domain_expansion_queue"]]
    warnings = [{"title": row["title"], "warning": row["warning"]} for row in artifact["source_quality_warnings"]]
    return f"""# Packet 145: Wide Research Substrate and Bio/Med/Robotics Nomenclature Map

Date: 2026-07-02

Status: `{artifact['status']}`

Purpose: turn the current request into a scalable source substrate: current
biology, medicine, robotics, and adjacent research signals, plus archive and
database intake routes for future hundreds-source pulls across domains.

```text
source_receipts = {artifact['gather_summary']['source_count']}
usable_sources = {artifact['gather_summary']['usable_source_count']}
source_warnings = {len(artifact['source_quality_warnings'])}
archive_substrates = {len(artifact['archive_substrate_catalog'])}
domain_lanes = {len(artifact['domain_lanes'])}
domain_queue = {len(artifact['domain_expansion_queue'])}
terminology_bridges = {len(artifact['terminology_bridges'])}
compose_status = {receipts['compose']['status']}
test_status = {receipts['test']['status']}
validator_status = {receipts['validator']['status']}
```

## Domain Lanes

| Lane | Biology terms | Medicine terms | Robotics terms | Tool target |
| --- | --- | --- | --- | --- |
{table(lanes, ['lane', 'bio', 'med', 'robotics', 'tool'])}

## Archive Substrates

| Source | Kind | Coverage |
| --- | --- | --- |
{table(archives, ['name', 'kind', 'coverage'])}

## Expansion Queue

| Domain | First tooling target |
| --- | --- |
{table(domains, ['domain', 'target'])}

## Source Quality Warnings

| Source | Warning |
| --- | --- |
{table(warnings, ['title', 'warning'])}

## Boundary

{artifact['boundary']}
"""


def render_brief(artifact: dict) -> str:
    return f"""# Wide Research Substrate Brief

Date: 2026-07-02

## Decision

Treat research as a routed substrate, not a reading list. The system now needs
archive adapters, nomenclature translation, source-quality gates, and proof
packet factories that can move from source discovery to executable falsifiers.

## Result

Pass 0135 gathered `{artifact['gather_summary']['source_count']}` source rows,
identified `{len(artifact['archive_substrate_catalog'])}` archive/database
substrates, and queued `{len(artifact['domain_expansion_queue'])}` domains for
future pulls.
"""


def render_steelman(artifact: dict) -> str:
    return f"""# Pass 0135 Steelman: Wide Research Substrate

Date: 2026-07-02

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a broad archive map can become performative
breadth: lots of sources, little solved. The pass therefore records archive
substrates and nomenclature bridges as `SOURCE_SUBSTRATE` and
`HYPOTHESIS_SOURCE_MAP`, not proof.

The second objection is source quality. Correct: some sources were blocked or
empty captures. Those are counted as warnings, not evidence.

Boundary: {artifact['boundary']}
"""


def write_receipts(compose: dict, test: dict, validator: dict, artifact: dict) -> dict:
    receipts = {
        "schema": "DogfoodToolReceipts/v1",
        "pass": "0135",
        "compose": compose,
        "test": test,
        "validator": validator,
        "forum": artifact["flagship_receipts"]["forum"],
        "index": artifact["flagship_receipts"]["index"],
        "telos": artifact["flagship_receipts"]["telos"],
        "telos_catalog": artifact["flagship_receipts"]["telos_catalog"],
        "source_count": artifact["gather_summary"]["source_count"],
        "archive_substrate_count": len(artifact["archive_substrate_catalog"]),
        "domain_queue_count": len(artifact["domain_expansion_queue"]),
    }
    receipts["seal"] = hashlib.sha256(json.dumps(receipts, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()
    write_json(TOOL_RECEIPTS, receipts)
    return receipts


def thesis_measurements(artifact: dict, receipts: dict) -> tuple[dict, dict]:
    files = {"artifact": ARTIFACT, "composer": COMPOSER, "packet": PACKET, "brief": BRIEF, "steelman": STEELMAN, "test": TEST_SCRIPT, "validator": VALIDATOR, "validator_result": VALIDATOR_RESULT, "tool_receipts": TOOL_RECEIPTS}
    shas = {name: sha256_file(path) for name, path in files.items()}
    claims = [
        f"Pass 0135 created a BioMedRoboticsNomenclatureMapReceipt/v1 artifact with status {artifact['status']}, sha256 {shas['artifact']}, and seal {artifact['seal']}.",
        f"Pass 0135 gathered {artifact['gather_summary']['source_count']} source receipts with {artifact['gather_summary']['usable_source_count']} usable captures.",
        f"Pass 0135 records {len(artifact['source_quality_warnings'])} source-quality warnings for blocked or empty captures.",
        f"Pass 0135 catalogs {len(artifact['archive_substrate_catalog'])} archive/database substrates for broad research intake.",
        f"Pass 0135 maps {len(artifact['domain_lanes'])} biology/medicine/robotics correlated lanes.",
        f"Pass 0135 queues {len(artifact['domain_expansion_queue'])} broader domains for future source pulls.",
        f"Pass 0135 records {len(artifact['terminology_bridges'])} nomenclature bridges.",
        f"Pass 0135 defines {len(artifact['market_hypotheses'])} product hypotheses and rejects {len(artifact['negative_fixtures'])} negative fixtures.",
        "Pass 0135 does not promote shared terminology, market signals, reviews, demos, or archive coverage into natural laws.",
        f"Pass 0135 validator status is {receipts['validator']['status']} and test status is {receipts['test']['status']}.",
        f"Pass 0135 file hashes are {shas}.",
    ]
    evidence = [
        [f"schema={artifact['schema']}", f"status={artifact['status']}", f"sha256={shas['artifact']}", f"seal={artifact['seal']}"],
        [f"gather_summary={artifact['gather_summary']}"],
        [f"source_quality_warnings={artifact['source_quality_warnings']}"],
        [f"archive_substrate_catalog={artifact['archive_substrate_catalog']}"],
        [f"domain_lanes={artifact['domain_lanes']}"],
        [f"domain_expansion_queue={artifact['domain_expansion_queue']}"],
        [f"terminology_bridges={artifact['terminology_bridges']}"],
        [f"market_hypotheses={artifact['market_hypotheses']}", f"negative_fixtures={artifact['negative_fixtures']}"],
        [f"boundary={artifact['boundary']}", f"current_promoted_natural_laws={artifact['current_promoted_natural_laws']}"],
        [f"validator={receipts['validator']}", f"test={receipts['test']}"],
        [f"file_hashes={shas}"],
    ]
    thesis = {"title": "Dogfood Pass 0135 Wide Research Substrate", "disposition": "fenced", "claims": [{"text": claim, "falsification": f"Claim {idx + 1} differs from pass 0135 artifacts or receipts are missing"} for idx, claim in enumerate(claims)]}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[idx], "method": "artifact-review", "tolerance": 0.5} for idx, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose = run_command([sys.executable, str(COMPOSER), "--out", str(ARTIFACT)])
    artifact = read_json(ARTIFACT)
    test = run_command([sys.executable, str(TEST_SCRIPT)])
    validator = run_command([sys.executable, str(VALIDATOR)])
    receipts = write_receipts(compose, test, validator, artifact)
    write_text(PACKET, render_packet(artifact, receipts))
    write_text(BRIEF, render_brief(artifact))
    write_text(STEELMAN, render_steelman(artifact))
    thesis, measurements = thesis_measurements(artifact, receipts)
    write_json(THESIS, thesis)
    write_json(MEASUREMENTS, measurements)
    ok = artifact["status"] == "BIO_MED_ROBOTICS_NOMENCLATURE_MAP_MATCH" and all(row["status"] == "MATCH" for row in [compose, test, validator])
    print(json.dumps({"status": "MATCH" if ok else "DRIFT", "artifact": str(ARTIFACT), "sources": artifact["gather_summary"]["source_count"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
