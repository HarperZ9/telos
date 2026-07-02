"""Compose pass 0135 biology/medicine/robotics nomenclature map."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "BioMedRoboticsNomenclatureMapReceipt/v1"
PASS_ID = "0135"
STATUS_MATCH = "BIO_MED_ROBOTICS_NOMENCLATURE_MAP_MATCH"
STATUS_DRIFT = "BIO_MED_ROBOTICS_NOMENCLATURE_MAP_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0135-bio-med-robotics-nomenclature"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def ascii_text(value: str) -> str:
    return value.encode("ascii", "ignore").decode("ascii")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def read_catalog() -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    result = []
    for row in rows:
        obj = STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
        body = obj.read_text(encoding="utf-8", errors="replace") if obj.exists() else ""
        challenge = "required part of this site" in body.lower() or row.get("title") == "Client Challenge"
        empty = obj.exists() and not body.strip()
        result.append({
            "ref": row["ref"],
            "title": ascii_text(row.get("title", "")),
            "kind": row["kind"],
            "method": row["method"],
            "sha256": row["sha256"],
            "chars": len(body),
            "status": "GATHER_VERIFIED" if obj.exists() else "MISSING_OBJECT",
            "source_quality": "EMPTY_CAPTURE" if empty else ("CLIENT_CHALLENGE" if challenge else classify_quality(row["ref"])),
            "raw_body_exported": False,
        })
    return sorted(result, key=lambda item: item["ref"])


def classify_quality(ref: str) -> str:
    if "github.com" in ref:
        return "CURATED_REPO_OR_CODE_SIGNAL"
    if "pmc.ncbi" in ref or "pubmed.ncbi" in ref:
        return "OPEN_BIOMEDICAL_RECORD"
    if "normalcomputing.com" in ref or "pi.website" in ref or "nvidia.com" in ref:
        return "INDUSTRY_RESEARCH_SIGNAL"
    if "drmichaellevin" in ref or "berkeley.edu" in ref:
        return "LAB_OR_UNIVERSITY_SOURCE"
    return "WEB_SOURCE"


def run_json(command: list[str], timeout: int = 90) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Project Telos biology medicine robotics nomenclature source map for deep research."])
    candidates = parsed.get("candidates") or []
    top = candidates[0]["agent"] if candidates else None
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided"), "top_candidate": top}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1600", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def domain_lanes() -> list[dict[str, Any]]:
    return [
        lane("morphogenesis_bioelectricity_collective_intelligence", ["bioelectricity", "morphogenesis", "collective intelligence"], ["regenerative medicine", "morphoceutics", "cancer suppression"], ["swarm intelligence", "morphogenetic robotics"], "Morphogenesis claim-to-experiment packet"),
        lane("virtual_cell_single_cell_spatial_omics", ["single-cell foundation model", "spatial omics", "virtual cell"], ["patient stratification", "preclinical virtual cell"], ["world model", "state representation"], "Virtual-cell evidence packet"),
        lane("bioelectronic_closed_loop_therapy", ["bioelectronic medicine", "neuromodulation", "autonomic control"], ["closed-loop therapy", "adaptive stimulation"], ["feedback control", "sensor-actuator loop"], "Therapy action receipt"),
        lane("organ_chip_organoid_human_on_chip", ["microphysiological system", "organoid", "organ-on-chip"], ["drug testing", "toxicity", "aging model"], ["sim-to-real testbed", "embodied benchmark"], "Experiment reproducibility packet"),
        lane("physical_ai_robot_foundation_models", ["VLA", "robot foundation model", "diffusion policy"], ["assistive robotics", "rehabilitation robotics"], ["generalist policy", "embodied AI"], "Robot policy proof packet"),
        lane("surgical_ai_medical_robotics_continuum", ["continuum robot", "soft robot", "endoluminal intervention"], ["minimally invasive surgery", "surgical autonomy"], ["compliant body control", "teleoperation"], "Operating-room evidence packet"),
        lane("thermodynamic_probabilistic_biophysical_compute", ["stochastic dynamics", "thermodynamic compute"], ["Bayesian medicine", "scientific simulation"], ["probabilistic controller", "sampling hardware"], "Stochastic compute receipt"),
        lane("translation_and_nomenclature", ["same mechanism, different vocabulary"], ["clinical endpoint", "regulatory evidence"], ["task success", "safety case"], "Cross-domain nomenclature resolver"),
    ]


def lane(lane_id: str, bio: list[str], medicine: list[str], robotics: list[str], product: str) -> dict[str, Any]:
    return {
        "lane_id": lane_id,
        "biology_terms": bio,
        "medicine_terms": medicine,
        "robotics_terms": robotics,
        "tool_product_hypothesis": product,
        "gap_status": "inferred",
        "promotion_gate": "Requires primary source receipts, task fixture, negative control, and independent verifier before proof or law promotion.",
        "status": "HYPOTHESIS_SOURCE_MAP",
    }


def terminology_bridges() -> list[dict[str, Any]]:
    rows = [
        ("feedback_control", "homeostasis / bioelectric control", "closed-loop therapy", "policy feedback / controller"),
        ("world_model", "virtual cell / tissue state model", "digital twin / patient model", "robot scene or dynamics model"),
        ("intervention", "perturbation / morphogenetic signal", "therapy / stimulation / drug", "action / motor command"),
        ("fitness_or_loss", "fitness landscape / viability", "clinical endpoint / safety outcome", "reward / cost function"),
        ("embodiment", "cell collective / body plan", "anatomy / implant interface", "morphology / robot body"),
        ("benchmark", "atlas / organoid / perturb-seq", "trial endpoint / assay", "task suite / sim-to-real evaluation"),
        ("uncertainty", "heterogeneity / stochastic cell state", "risk / confidence interval", "domain randomization / policy entropy"),
        ("proof_packet", "source plus experiment plus assay", "source plus protocol plus safety gate", "source plus run plus replay verifier"),
    ]
    return [{"concept": c, "biology_name": b, "medicine_name": m, "robotics_name": r, "status": "NOMENCLATURE_BRIDGE"} for c, b, m, r in rows]


def market_hypotheses() -> list[dict[str, str]]:
    return [
        {"product": "Cross-Domain Nomenclature Resolver", "buyer": "research labs and venture studios", "wedge": "map equivalent concepts across biology, medicine, robotics, AI, and controls with source receipts", "status": "HYPOTHESIS"},
        {"product": "Bio-Med-Robotics Claim Packet", "buyer": "AI4Science and translational medicine teams", "wedge": "bind paper, assay, model, intervention, negative control, and verifier before promotion", "status": "HYPOTHESIS"},
        {"product": "Closed-Loop Therapy Action Receipt", "buyer": "bioelectronic medicine and medical device teams", "wedge": "separate sensor evidence, controller policy, stimulation action, safety gate, and clinical endpoint", "status": "HYPOTHESIS"},
        {"product": "Embodied Experiment Replay Kit", "buyer": "robotics and organ-chip platform teams", "wedge": "treat organ chips, robot testbeds, and surgical data factories as replayable embodied evidence surfaces", "status": "HYPOTHESIS"},
        {"product": "BuildLang Multiscale Dynamics Kernel", "buyer": "scientific compute groups", "wedge": "compile and receipt bounded dynamical systems shared by morphogenesis, therapy control, robotics, and stochastic compute", "status": "HYPOTHESIS"},
    ]


def archive_substrate_catalog() -> list[dict[str, str]]:
    return [
        archive("OpenAlex", "global scholarly graph", "works, authors, sources, institutions, topics", "metadata_graph"),
        archive("Crossref", "publisher DOI metadata", "works, funders, licenses, references, ORCID/ROR", "metadata_graph"),
        archive("Semantic Scholar", "AI-linked scholarly graph", "papers, authors, citations, recommendations, datasets", "metadata_graph"),
        archive("CORE", "open-access aggregation", "repository metadata and open full-text access points", "full_text_aggregator"),
        archive("arXiv", "preprint archive", "math, physics, computer science, quantitative biology, statistics", "preprint_archive"),
        archive("bioRxiv/medRxiv", "life-science and medical preprints", "preprints, publication links, interval feeds", "preprint_archive"),
        archive("NCBI/PubMed/PMC", "biomedical literature and databases", "PubMed, PMC, Gene, Nuccore, Protein", "biomedical_archive"),
        archive("NASA ADS", "astronomy and physics literature", "search, metrics, export functions", "domain_archive"),
        archive("Dataverse", "research data repository network", "datasets, files, metadata, permissions", "data_repository"),
        archive("Zenodo", "general research outputs", "records, files, deposits, OAI-PMH", "data_repository"),
        archive("OSF", "open science workflow repository", "projects, study designs, data, manuscripts, materials", "data_repository"),
        archive("Materials Project", "materials discovery database", "computed material properties and API client", "domain_database"),
    ]


def archive(name: str, scope: str, coverage: str, kind: str) -> dict[str, str]:
    return {"name": name, "scope": scope, "coverage": coverage, "kind": kind, "status": "SOURCE_SUBSTRATE"}


def domain_expansion_queue() -> list[dict[str, str]]:
    rows = [
        ("biology", "morphogenesis, evolution, omics, synthetic biology", "claim-to-experiment packets"),
        ("medicine", "clinical evidence, devices, drug discovery, trials", "safety and endpoint receipts"),
        ("robotics", "physical AI, surgical robotics, soft robotics", "embodied action replay"),
        ("mathematics", "open problems, proof assistants, theorem graphs", "prover-verifier packets"),
        ("physics", "foundations, quantum, statistical mechanics, cosmology", "law-boundary and simulator receipts"),
        ("materials", "crystals, molecules, batteries, catalysts", "materials property proof packets"),
        ("chemistry", "reaction networks, synthesis, molecular design", "stoichiometry and synthesis receipts"),
        ("climate_energy", "earth systems, grid, fusion, storage", "simulation provenance packets"),
        ("security", "formal methods, systems, cryptography", "exploit/fix proof packets"),
        ("finance", "risk, markets, optimization, fraud", "model-risk and optimization receipts"),
        ("education", "learning science, tutoring, curriculum graphs", "source-backed lesson receipts"),
        ("governance_law", "policy, regulation, institutional design", "claim provenance and decision receipts"),
        ("neuroscience", "BCI, cognition, neural dynamics", "closed-loop experiment receipts"),
        ("economics", "mechanism design, labor, macro systems", "causal evidence packets"),
    ]
    return [{"domain": d, "search_terms": terms, "first_tooling_target": target, "status": "EXPANSION_QUEUE"} for d, terms, target in rows]


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "same_word_same_mechanism_rejected", "status": "REJECTED", "failures": ["nomenclature_overlap_only", "requires_mechanistic_bridge"]},
        {"fixture_id": "review_as_validated_intervention_rejected", "status": "REJECTED", "failures": ["review_article", "no_protocol_replay"]},
        {"fixture_id": "foundation_model_as_clinical_validity_rejected", "status": "REJECTED", "failures": ["benchmark_only", "requires_clinical_endpoint"]},
        {"fixture_id": "nature_client_challenge_as_article_rejected", "status": "REJECTED", "failures": ["blocked_capture", "not_article_body"]},
        {"fixture_id": "robot_demo_as_safety_case_rejected", "status": "REJECTED", "failures": ["demo_signal_only", "requires_hazard_analysis"]},
        {"fixture_id": "market_signal_as_efficacy_rejected", "status": "REJECTED", "failures": ["industry_claim", "requires_independent_measurement"]},
        {"fixture_id": "nomenclature_map_as_natural_law_rejected", "status": "REJECTED", "failures": ["taxonomy_only", "requires_proof_and_reproduction"]},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    receipts = artifact["source_receipts"]
    if len(receipts) < 18:
        errors.append("source_count")
    if artifact["gather_summary"]["usable_source_count"] < 15:
        errors.append("usable_sources")
    if len(artifact["source_quality_warnings"]) < 3:
        errors.append("source_quality_warnings")
    if len(artifact["archive_substrate_catalog"]) < 12:
        errors.append("archive_substrate_catalog")
    if len(artifact["domain_expansion_queue"]) < 12:
        errors.append("domain_expansion_queue")
    if len(artifact["domain_lanes"]) < 8:
        errors.append("domain_lanes")
    if len(artifact["terminology_bridges"]) < 8:
        errors.append("terminology_bridges")
    if any(row["status"] != "REJECTED" for row in artifact["negative_fixtures"]):
        errors.append("negative_fixtures")
    if any(row["status"] != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagship_receipts")
    if artifact["current_promoted_natural_laws"]:
        errors.append("natural_laws")
    return errors


def compose() -> dict[str, Any]:
    receipts = read_catalog()
    warnings = [row for row in receipts if row["source_quality"] in {"CLIENT_CHALLENGE", "EMPTY_CAPTURE"}]
    usable = [row for row in receipts if row["source_quality"] not in {"CLIENT_CHALLENGE", "EMPTY_CAPTURE"}]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-02",
        "source_store": str(STORE.relative_to(REPO)),
        "source_receipts": receipts,
        "gather_summary": {
            "source_count": len(receipts),
            "usable_source_count": len(usable),
            "client_challenge_count": len([row for row in warnings if row["source_quality"] == "CLIENT_CHALLENGE"]),
            "empty_capture_count": len([row for row in warnings if row["source_quality"] == "EMPTY_CAPTURE"]),
            "distinct_body_count": len({row["sha256"] for row in receipts}),
        },
        "source_quality_warnings": [{"ref": row["ref"], "title": row["title"], "sha256": row["sha256"], "warning": row["source_quality"].lower()} for row in warnings],
        "archive_substrate_catalog": archive_substrate_catalog(),
        "domain_expansion_queue": domain_expansion_queue(),
        "domain_lanes": domain_lanes(),
        "terminology_bridges": terminology_bridges(),
        "market_hypotheses": market_hypotheses(),
        "negative_fixtures": negative_fixtures(),
        "boundary": "Pass 0135 maps current source terminology across biology, medicine, robotics, AI, controls, and scientific compute. It does not claim that shared vocabulary proves shared mechanism, clinical efficacy, robot safety, or natural law.",
        "current_promoted_natural_laws": [],
        "unsupported_claim_count": 0,
        "flagship_receipts": flagship_receipts(),
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "bio-med-robotics-nomenclature-map-pass-0135.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "status": artifact["status"], "seal": artifact["seal"], "sources": len(artifact["source_receipts"])}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
