"""Compose pass 0140 global research archive substrate atlas."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "ResearchArchiveSubstrateAtlasReceipt/v1"
PASS_ID = "0140"
STATUS_MATCH = "RESEARCH_ARCHIVE_SUBSTRATE_ATLAS_MATCH"
STATUS_DRIFT = "RESEARCH_ARCHIVE_SUBSTRATE_ATLAS_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0140-research-archive-substrate-atlas"
OUT = ROOT / "schemas" / "research-archive-substrate-atlas-pass-0140.json"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()

FAILED_STATIC = [
    ("DSpace@MIT", "https://dspace.mit.edu/", "university_repository", "STATIC_CAPTURE_FAILED_SOURCE_LEAD"),
    ("BASE", "https://www.base-search.net/", "academic_search_index", "STATIC_CAPTURE_FAILED_SOURCE_LEAD"),
]

SOURCE_INFO = {
    "arxiv": ("arXiv", "preprint_archive", "math_physics_cs_quantbio_stats", "api_oai_bulk"),
    "biorxiv": ("bioRxiv", "preprint_archive", "biology", "api_interval_cursor"),
    "medrxiv": ("medRxiv", "preprint_archive", "medicine_health", "api_interval_cursor"),
    "crossref": ("Crossref", "publisher_metadata_graph", "cross_domain_publication_metadata", "rest_json"),
    "openalex": ("OpenAlex", "scholarly_graph", "works_authors_sources_institutions_topics", "rest_json_snapshot"),
    "semanticscholar": ("Semantic Scholar", "scholarly_graph", "papers_authors_citations_datasets", "rest_json_datasets"),
    "core.ac.uk": ("CORE", "open_access_aggregator", "repository_metadata_and_full_text_routes", "api_bulk"),
    "ncbi.nlm.nih.gov/home/develop": ("NCBI E-utilities", "biomedical_api", "pubmed_pmc_gene_nuccore_protein", "entrez_api"),
    "pmc.ncbi.nlm.nih.gov/tools/oai": ("PMC OAI-PMH", "full_text_open_access", "pmc_metadata_and_reusable_full_text", "oai_pmh"),
    "clinicaltrials": ("ClinicalTrials.gov", "clinical_registry", "trial_protocols_results_records", "rest_json_openapi"),
    "zenodo": ("Zenodo", "research_data_repository", "records_files_deposits", "rest_oai"),
    "datacite": ("DataCite", "doi_metadata_graph", "data_doi_metadata", "rest_jsonapi"),
    "adsabs": ("NASA ADS", "domain_literature_index", "astronomy_physics_search_metrics_export", "rest_json_api_key"),
    "data.rcsb": ("RCSB PDB Data API", "structure_database", "pdb_metadata_sequences_experimental_details", "rest_graphql"),
    "search.rcsb": ("RCSB PDB Search API", "structure_search", "pdb_search_queries", "rest_json"),
    "ncbi.nlm.nih.gov/sra": ("NCBI SRA", "genomics_archive", "raw_sequencing_alignment_metadata", "ncbi_cloud_tools"),
    "ncbi.nlm.nih.gov/geo": ("NCBI GEO", "functional_genomics_repository", "expression_arrays_sequence_profiles", "web_api_download"),
    "ebi.ac.uk/ena": ("ENA", "nucleotide_archive", "raw_sequence_assembly_annotation", "browser_api"),
    "uniprot": ("UniProt", "protein_knowledgebase", "protein_sequence_function", "rest_download"),
    "materialsproject": ("Materials Project", "materials_database", "computed_material_properties", "python_client_api"),
    "openml": ("OpenML", "ml_dataset_benchmark_repository", "datasets_tasks_flows_runs", "rest_api"),
    "huggingface": ("Hugging Face Dataset Viewer", "ml_dataset_hub", "dataset_splits_rows_parquet_stats", "rest_api"),
    "openarchives": ("OAI-PMH", "repository_interop_protocol", "metadata_harvesting_protocol", "oai_pmh"),
    "dash.harvard": ("Harvard DASH", "university_repository", "harvard_open_access_scholarship", "repository_oai"),
    "sdr.library.stanford": ("Stanford Digital Repository", "university_repository", "stanford_scholarly_objects", "repository_web"),
    "caltech": ("Caltech repository OAI endpoints", "university_repository", "caltech_authors_thesis_metadata", "oai_pmh"),
    "developer.osf": ("OSF API", "open_science_repository", "projects_registrations_files", "rest_json"),
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def classify(ref: str) -> tuple[str, str, str, str]:
    for needle, info in SOURCE_INFO.items():
        if needle in ref.lower():
            return info
    return ("Unclassified source", "source_lead", "cross_domain", "web")


def read_catalog() -> list[dict[str, Any]]:
    rows = []
    for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        body_path = STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
        chars = len(body_path.read_text(encoding="utf-8", errors="replace")) if body_path.exists() else 0
        system, category, coverage, protocol = classify(row["ref"])
        evidence = "GATHER_VERIFIED_EMPTY_CAPTURE" if row["sha256"] == EMPTY_SHA or chars == 0 else "GATHER_VERIFIED"
        rows.append({
            "system": system,
            "url": row["ref"],
            "title": row.get("title", ""),
            "category": category,
            "coverage": coverage,
            "ingestion_protocol": protocol,
            "sha256": row["sha256"],
            "chars": chars,
            "evidence_status": evidence,
            "market_use": market_use(category),
        })
    for system, url, category, evidence in FAILED_STATIC:
        rows.append({
            "system": system,
            "url": url,
            "title": system,
            "category": category,
            "coverage": "institutional_or_academic_repository",
            "ingestion_protocol": "browser_or_oai_followup_required",
            "sha256": None,
            "chars": 0,
            "evidence_status": evidence,
            "market_use": market_use(category),
        })
    return sorted(rows, key=lambda item: (item["category"], item["system"], item["url"]))


def market_use(category: str) -> str:
    if "preprint" in category:
        return "frontier_claim_intake"
    if "metadata" in category or "graph" in category:
        return "claim_context_and_citation_graph"
    if "clinical" in category:
        return "trial_endpoint_and_protocol_receipts"
    if "genomics" in category or "protein" in category or "structure" in category:
        return "bio_ai_experiment_packet"
    if "materials" in category:
        return "materials_property_replay_packet"
    if "university" in category or "repository" in category:
        return "institutional_repository_harvest"
    if "ml_dataset" in category:
        return "benchmark_contamination_and_dataset_receipts"
    return "research_substrate_route"


def substrate_families() -> list[dict[str, str]]:
    rows = [
        ("preprint_archives", "arXiv, bioRxiv, medRxiv, ChemRxiv, SSRN, Research Square", "rapid frontier claim intake"),
        ("publisher_metadata_graphs", "Crossref, DataCite, DOI registration agencies", "provenance, references, licenses, funders"),
        ("scholarly_graphs", "OpenAlex, Semantic Scholar, CORE, BASE", "literature graph and institutional coverage"),
        ("open_full_text", "PMC OAI, CORE, repository full text", "text mining and claim extraction"),
        ("clinical_registries", "ClinicalTrials.gov and related registries", "protocol and endpoint receipts"),
        ("biomedical_databases", "NCBI, PMC, GEO, SRA, UniProt, RCSB PDB", "bio/medicine experiment substrate"),
        ("materials_chemistry", "Materials Project, chemistry preprints, molecule databases", "property prediction and simulation receipts"),
        ("ml_dataset_hubs", "OpenML, Hugging Face, Kaggle-style hubs", "benchmark provenance and contamination checks"),
        ("general_data_repositories", "Zenodo, OSF, Dataverse, Figshare, Dryad", "data DOI and reproducibility packets"),
        ("university_repositories", "MIT, Harvard, Stanford, Caltech, Oxford, Cambridge", "institutional thesis/report/article harvesting"),
        ("government_science_data", "NASA, NOAA, DOE, NIH, NSF portals", "public measurement substrates"),
        ("formal_math_repositories", "Lean mathlib, theorem prover repos, problem archives", "machine-checkable proof receipts"),
        ("standards_and_patents", "NIST, W3C, ISO metadata, patent offices", "engineering constraints and prior art"),
        ("policy_and_law", "regulators, courts, legislation portals", "governance claim provenance"),
    ]
    return [{"family": f, "examples": ex, "tooling_target": target, "status": "SUBSTRATE_FAMILY"} for f, ex, target in rows]


def domain_queue() -> list[dict[str, str]]:
    domains = [
        ("math_formal_methods", "proof assistants, arXiv math, theorem archives", "ProofPacket and LeanProofReceipt"),
        ("physics_quantum_cosmology", "arXiv physics, NASA ADS, HEPData", "simulator and law-boundary receipts"),
        ("biology_genomics", "bioRxiv, NCBI, ENA, GEO, SRA", "claim-to-experiment packets"),
        ("medicine_clinical", "medRxiv, PubMed, PMC, ClinicalTrials.gov", "clinical endpoint receipts"),
        ("materials_chemistry", "Materials Project, RCSB, ChemRxiv", "property replay packets"),
        ("robotics_embodied_ai", "OpenReview, arXiv cs.RO, robot datasets", "embodied action receipts"),
        ("ai_ml", "arXiv cs.LG, OpenML, Hugging Face, Papers with Code", "dataset/model contamination receipts"),
        ("climate_energy", "NASA, NOAA, DOE, arXiv physics", "earth/energy simulation receipts"),
        ("security_cryptography", "ePrint, CVE, GitHub advisories, arXiv", "exploit/fix proof packets"),
        ("finance_economics", "SSRN, NBER, FRED, SEC EDGAR", "risk and causal evidence packets"),
        ("education_learning", "ERIC, university repos, lesson datasets", "learning graph receipts"),
        ("law_policy_governance", "court/regulator portals, legislation APIs", "decision provenance receipts"),
        ("neuroscience_bci", "PubMed, bioRxiv, OpenNeuro", "closed-loop experiment packets"),
        ("agriculture_food", "USDA, FAO, genomics repositories", "crop/system optimization receipts"),
        ("transportation_cities", "DOT, city open data, simulation papers", "infrastructure optimization packets"),
        ("semiconductors_hpc", "DOE, arXiv, MLIR/OpenXLA repos", "compiler/runtime receipts"),
        ("color_rendering_media", "ACES/OCIO, display datasets, standards", "measurement truth kits"),
        ("philosophy_cognitive_science", "university repos, PhilPapers, archives", "functional learning maps"),
    ]
    return [{"domain": d, "source_targets": targets, "first_product": product, "status": "EXPANSION_QUEUE"} for d, targets, product in domains]


def megatool_routes() -> list[dict[str, Any]]:
    return [
        {"route": "archive_to_claim_packet", "tools": ["Gather", "Index", "Crucible"], "output": "source-backed claim with verification state"},
        {"route": "claim_to_experiment_packet", "tools": ["Gather", "Telos", "Crucible", "BuildLang/buildc"], "output": "protocol, runtime receipt, measurement, verifier"},
        {"route": "dataset_to_model_receipt", "tools": ["Gather", "Index", "Model Foundry", "Crucible"], "output": "dataset lineage, contamination gate, eval receipt"},
        {"route": "paper_to_formal_proof", "tools": ["Gather", "Index", "Lean/ATP adapter", "Crucible"], "output": "machine-checkable theorem replay packet"},
        {"route": "university_repo_to_learning_graph", "tools": ["Gather", "Index", "Forum", "Learning Forge"], "output": "source-backed lesson and prerequisite graph"},
        {"route": "domain_database_to_build_kernel", "tools": ["Gather", "BuildLang/buildc", "Crucible"], "output": "compiled scientific kernel with data provenance"},
    ]


def negative_fixtures() -> list[dict[str, Any]]:
    rows = [
        ("source_breadth_as_truth", "REJECTED", ["many_sources", "no_verifier"]),
        ("preprint_as_peer_review", "REJECTED", ["preprint_state", "needs_publication_or_replication"]),
        ("metadata_as_full_text", "REJECTED", ["metadata_only", "no_claim_body"]),
        ("empty_capture_as_evidence", "REJECTED", ["empty_capture", "needs_browser_or_api_followup"]),
        ("failed_static_capture_as_verified", "REJECTED", ["static_capture_failed", "source_lead_only"]),
        ("clinical_trial_record_as_efficacy", "REJECTED", ["registry_record", "needs_results_analysis"]),
        ("dataset_presence_as_benchmark_validity", "REJECTED", ["dataset_found", "needs_schema_and_task_receipt"]),
        ("university_repo_as_complete_corpus", "REJECTED", ["institutional_subset", "coverage_unknown"]),
        ("api_docs_as_license_clearance", "REJECTED", ["api_docs_only", "needs_license_terms"]),
        ("taxonomy_as_natural_law", "REJECTED", ["classification_only", "needs_proof_or_reproduction"]),
    ]
    return [{"fixture_id": fid, "status": status, "failures": failures} for fid, status, failures in rows]


def run_json(command: list[str], timeout: int = 120) -> dict[str, Any]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return {"exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "parsed": parsed}


def flagship_receipts() -> dict[str, Any]:
    forum = run_json(["forum", "route", "--json", "Global research archive substrate atlas across preprints, publishing metadata, domain databases, and university repositories."])
    index = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=180)
    telos = run_json(["node", "demo/status.mjs", "--summary"])
    catalog = subprocess.run(["node", "demo/catalog.mjs", "--summary"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    return {
        "forum": {"status": "MATCH_WITH_ROUTE_GAP" if forum["exit_code"] == 0 else "DRIFT", "needs_escalation": forum["parsed"].get("needs_escalation"), "confidence": forum["parsed"].get("confidence"), "stdout_sha256": forum["stdout_sha256"], "stderr_sha256": forum["stderr_sha256"]},
        "index": {"status": "MATCH" if index["exit_code"] == 0 and index["parsed"].get("verification_verdict") == "MATCH" else "DRIFT", "verification_verdict": index["parsed"].get("verification_verdict"), "stdout_sha256": index["stdout_sha256"], "stderr_sha256": index["stderr_sha256"]},
        "telos": {"status": "MATCH" if telos["exit_code"] == 0 and telos["parsed"].get("status") == "MATCH" else "DRIFT", "tool_version": telos["parsed"].get("tool_version"), "stdout_sha256": telos["stdout_sha256"], "stderr_sha256": telos["stderr_sha256"]},
        "telos_catalog": {"status": "MATCH" if catalog.returncode == 0 and "Project Telos MCP Catalog" in catalog.stdout else "DRIFT", "stdout_sha256": sha256_text(catalog.stdout), "stderr_sha256": sha256_text(catalog.stderr)},
    }


def validate(artifact: dict[str, Any]) -> list[str]:
    failures = []
    if artifact["gather_summary"]["captured_sources"] < 28:
        failures.append("captured_source_count")
    if artifact["gather_summary"]["usable_captures"] < 26:
        failures.append("usable_capture_count")
    if len(artifact["source_systems"]) < 30:
        failures.append("source_systems")
    if len(artifact["source_quality_warnings"]) < 4:
        failures.append("source_quality_warnings")
    if len(artifact["substrate_families"]) < 14:
        failures.append("substrate_families")
    if len(artifact["domain_expansion_queue"]) < 18:
        failures.append("domain_expansion_queue")
    if len(artifact["negative_fixtures"]) < 10 or any(row["status"] != "REJECTED" for row in artifact["negative_fixtures"]):
        failures.append("negative_fixtures")
    if any(not row["status"].startswith("MATCH") for row in artifact["flagship_receipts"].values()):
        failures.append("flagship_receipts")
    if artifact["current_promoted_natural_laws"]:
        failures.append("natural_laws")
    return failures


def compose() -> dict[str, Any]:
    systems = read_catalog()
    warnings = [row for row in systems if row["evidence_status"] != "GATHER_VERIFIED"]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-02",
        "source_store": str(STORE.relative_to(REPO)).replace("\\", "/"),
        "source_systems": systems,
        "gather_summary": {"captured_sources": len([r for r in systems if r["evidence_status"].startswith("GATHER_VERIFIED")]), "usable_captures": len([r for r in systems if r["evidence_status"] == "GATHER_VERIFIED"]), "warning_count": len(warnings), "distinct_body_count": len({r["sha256"] for r in systems if r["sha256"]})},
        "source_quality_warnings": warnings,
        "substrate_families": substrate_families(),
        "domain_expansion_queue": domain_queue(),
        "megatool_routes": megatool_routes(),
        "adapter_requirements": ["source_url", "source_system", "ingestion_protocol", "body_or_metadata_hash", "license_or_terms_ref", "freshness_time", "claim_extraction_state", "negative_controls", "verifier", "promotion_boundary"],
        "negative_fixtures": negative_fixtures(),
        "market_vectors": ["Research Substrate Router", "Archive Adapter SDK", "Claim-to-Experiment Packet", "Dataset/Benchmark Provenance Kit", "University Repository Learning Graph", "BuildLang Scientific Kernel Receipt"],
        "flagship_receipts": flagship_receipts(),
        "current_promoted_natural_laws": [],
        "boundary": "Pass 0140 is a first-wave archive substrate atlas. It does not claim complete world coverage, source correctness, publication validity, market demand, theorem proof, experimental truth, or natural-law promotion.",
    }
    errors = validate(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def main() -> None:
    artifact = compose()
    write_json(OUT, artifact)
    print(json.dumps({"path": str(OUT), "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
