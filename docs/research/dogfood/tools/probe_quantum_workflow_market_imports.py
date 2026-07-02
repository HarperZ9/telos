"""Generate pass 0020 quantum workflow market and import-audit receipts."""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


SOURCE_ANCHORS = [
    {"source": "IBM Quantum Qiskit Runtime docs", "url": "https://quantum.cloud.ibm.com/docs/guides/qiskit-runtime"},
    {"source": "IBM Quantum bit-ordering guide", "url": "https://quantum.cloud.ibm.com/docs/guides/bit-ordering"},
    {"source": "Amazon Braket documentation", "url": "https://docs.aws.amazon.com/braket/"},
    {"source": "Amazon Braket Hybrid Jobs", "url": "https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html"},
    {"source": "Azure Quantum documentation", "url": "https://learn.microsoft.com/en-us/azure/quantum/"},
    {"source": "Google Quantum AI Cirq docs", "url": "https://quantumai.google/cirq"},
    {"source": "Cirq Result API", "url": "https://quantumai.google/reference/python/cirq/Result"},
    {"source": "PennyLane documentation", "url": "https://docs.pennylane.ai/"},
    {"source": "PennyLane measurement docs", "url": "https://docs.pennylane.ai/en/stable/code/qp_measurements.html"},
    {"source": "NVIDIA CUDA-Q documentation", "url": "https://nvidia.github.io/cuda-quantum/latest/"},
    {"source": "Quantinuum Nexus documentation", "url": "https://docs.quantinuum.com/nexus/"},
    {"source": "D-Wave Leap documentation", "url": "https://docs.dwavesys.com/docs/latest/"},
    {"source": "Covalent documentation", "url": "https://docs.covalent.xyz/docs/"},
    {"source": "Classiq documentation", "url": "https://docs.classiq.io/"},
    {"source": "Pulser documentation", "url": "https://pulser.readthedocs.io/"},
    {"source": "QIR specification", "url": "https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md"},
    {"source": "pytket documentation", "url": "https://docs.quantinuum.com/tket/"},
    {"source": "OpenQASM documentation", "url": "https://openqasm.com/"},
    {"source": "MLflow Tracking docs", "url": "https://mlflow.org/docs/latest/tracking.html"},
    {"source": "Weights & Biases Artifacts docs", "url": "https://docs.wandb.ai/guides/artifacts/"},
    {"source": "DVC documentation", "url": "https://dvc.org/doc"},
    {"source": "OpenTelemetry documentation", "url": "https://opentelemetry.io/docs/"},
    {"source": "Prefect documentation", "url": "https://docs.prefect.io/"},
    {"source": "Flyte documentation", "url": "https://docs.flyte.org/"},
    {"source": "Nextflow documentation", "url": "https://www.nextflow.io/docs/latest/"},
    {"source": "Snakemake documentation", "url": "https://snakemake.readthedocs.io/"},
]


def row(
    category: str,
    company_tool: str,
    buyer: str,
    official_claim: str,
    capabilities: list[str],
    gaps: list[str],
    source_urls: list[str],
    gap_status: str = "inferred",
    confidence: str = "moderate",
) -> dict[str, object]:
    return {
        "schema": "MarketRow/v1",
        "category": category,
        "company_tool": company_tool,
        "buyer": buyer,
        "official_claim": official_claim,
        "capabilities": capabilities,
        "missing_proof_layer_features": gaps,
        "market_gap_status": gap_status,
        "sources": source_urls,
        "confidence": confidence,
        "uniqueness_claim_policy": "HYPOTHESIS_ONLY_UNLESS_MATRIX_PROVES_EXCLUSION",
    }


COMMON_GAPS = [
    "portable claim-to-receipt packet across source, circuit/program, compiler/runtime, provider metadata, result hash, and verification verdict",
    "cross-provider negative fixtures that make layout, shot, calibration, and post-processing ambiguity fail closed",
    "agent/tool action provenance bound to the scientific workflow record",
]


MARKET_ROWS = [
    row(
        "quantum cloud runtime",
        "IBM Qiskit Runtime",
        "quantum researchers, enterprise quantum teams, educators",
        "Cloud runtime for executing Qiskit primitive workloads against IBM quantum systems and simulators.",
        ["primitive execution", "sessions and jobs", "IBM backend metadata", "bit-ordering guidance"],
        COMMON_GAPS,
        ["https://quantum.cloud.ibm.com/docs/guides/qiskit-runtime", "https://quantum.cloud.ibm.com/docs/guides/bit-ordering"],
        confidence="high",
    ),
    row(
        "quantum cloud runtime",
        "Amazon Braket",
        "quantum algorithm teams, cloud R&D groups, enterprise research programs",
        "Managed AWS service for designing, testing, and running quantum algorithms on simulators and quantum hardware.",
        ["quantum tasks", "managed simulators", "provider hardware access", "hybrid jobs"],
        COMMON_GAPS,
        ["https://docs.aws.amazon.com/braket/", "https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html"],
        confidence="high",
    ),
    row(
        "quantum cloud runtime",
        "Azure Quantum",
        "enterprise quantum teams, cloud research groups, quantum education programs",
        "Azure cloud service for quantum computing, resource estimation, and multiple quantum toolchains/providers.",
        ["workspace service", "provider integration", "resource estimation", "toolchain support"],
        COMMON_GAPS,
        ["https://learn.microsoft.com/en-us/azure/quantum/"],
        confidence="high",
    ),
    row(
        "quantum programming framework",
        "Cirq / Google Quantum AI",
        "quantum software researchers and algorithm developers",
        "Python framework for creating, editing, simulating, and running quantum circuits.",
        ["circuit model", "simulators", "result objects", "histogram/fold policies"],
        COMMON_GAPS,
        ["https://quantumai.google/cirq", "https://quantumai.google/reference/python/cirq/Result"],
        confidence="high",
    ),
    row(
        "quantum programming and QML",
        "PennyLane",
        "quantum ML researchers, differentiable programming teams, quantum chemistry groups",
        "Python framework for quantum programming, quantum machine learning, and differentiable quantum workflows.",
        ["QNodes", "devices", "measurements", "differentiable workflows"],
        COMMON_GAPS,
        ["https://docs.pennylane.ai/", "https://docs.pennylane.ai/en/stable/code/qp_measurements.html"],
        confidence="high",
    ),
    row(
        "quantum programming and HPC",
        "NVIDIA CUDA-Q",
        "HPC centers, quantum simulation teams, heterogeneous compute teams",
        "Programming model and toolchain for quantum-classical heterogeneous computing.",
        ["C++/Python APIs", "simulators", "GPU acceleration path", "compiler/runtime tooling"],
        COMMON_GAPS,
        ["https://nvidia.github.io/cuda-quantum/latest/"],
        confidence="high",
    ),
    row(
        "quantum platform",
        "Quantinuum Nexus",
        "enterprise quantum teams and hardware users",
        "Quantum computing platform for developing, managing, and running quantum workflows against Quantinuum resources.",
        ["workflow platform", "hardware access", "compiler/tool integration"],
        COMMON_GAPS,
        ["https://docs.quantinuum.com/nexus/"],
        confidence="moderate",
    ),
    row(
        "quantum cloud and annealing",
        "D-Wave Leap",
        "optimization researchers, operations research teams, quantum annealing users",
        "Cloud access to D-Wave quantum computers, hybrid solvers, examples, and tooling.",
        ["quantum annealing access", "hybrid solvers", "Ocean tooling", "problem submission"],
        COMMON_GAPS,
        ["https://docs.dwavesys.com/docs/latest/"],
        confidence="high",
    ),
    row(
        "workflow orchestration",
        "Covalent",
        "computational scientists, quantum workflow teams, HPC/cloud users",
        "Python workflow orchestration for computational workloads across local, cloud, and HPC execution targets.",
        ["workflow graph", "executor abstraction", "result collection", "distributed execution"],
        COMMON_GAPS,
        ["https://docs.covalent.xyz/docs/"],
        confidence="moderate",
    ),
    row(
        "quantum software engineering",
        "Classiq",
        "enterprise quantum application teams and algorithm designers",
        "Quantum software platform for designing, synthesizing, analyzing, and executing quantum programs.",
        ["high-level synthesis", "circuit analysis", "execution integrations", "application templates"],
        COMMON_GAPS,
        ["https://docs.classiq.io/"],
        confidence="moderate",
    ),
    row(
        "neutral-atom quantum programming",
        "Pasqal Pulser",
        "neutral-atom researchers and quantum control developers",
        "Python framework for composing, simulating, and studying pulse sequences for neutral-atom devices.",
        ["pulse sequence design", "device models", "simulation hooks", "register/control abstractions"],
        COMMON_GAPS,
        ["https://pulser.readthedocs.io/"],
        confidence="high",
    ),
    row(
        "quantum intermediate representation",
        "QIR Alliance / QIR",
        "compiler teams, quantum language implementers, runtime builders",
        "LLVM-based intermediate representation specification for interoperable quantum programs.",
        ["IR contract", "runtime model", "compiler interface", "language interoperability"],
        COMMON_GAPS,
        ["https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md"],
        confidence="high",
    ),
    row(
        "quantum compiler toolkit",
        "TKET / pytket",
        "quantum compiler engineers and multi-provider algorithm teams",
        "Quantum SDK and compiler toolkit for circuit optimization, transformation, and backend targeting.",
        ["circuit transformations", "routing", "backend targeting", "Python SDK"],
        COMMON_GAPS,
        ["https://docs.quantinuum.com/tket/"],
        confidence="high",
    ),
    row(
        "quantum circuit language",
        "OpenQASM",
        "language implementers, quantum developers, standardization teams",
        "Open quantum assembly language for describing quantum programs and circuits.",
        ["portable program representation", "classical control constructs", "hardware-adjacent circuit expression"],
        COMMON_GAPS,
        ["https://openqasm.com/"],
        confidence="high",
    ),
    row(
        "ML experiment tracking",
        "MLflow Tracking",
        "ML platform teams, research engineers, data science teams",
        "Experiment tracking system for parameters, metrics, artifacts, models, and runs.",
        ["run tracking", "parameters and metrics", "artifact logging", "model registry ecosystem"],
        [
            "quantum-specific circuit layout, calibration, shot, and provider result canonicalization",
            "formal proof packet binding model/tool action receipts to scientific claims",
            "cross-provider negative fixtures for scientific evidence ambiguity",
        ],
        ["https://mlflow.org/docs/latest/tracking.html"],
        confidence="high",
    ),
    row(
        "ML experiment tracking",
        "Weights & Biases Artifacts",
        "ML platform teams, research labs, MLOps teams",
        "Artifact system for versioning datasets, models, and outputs used by ML experiments.",
        ["artifact versioning", "lineage", "experiment tracking integration", "dashboard review"],
        [
            "quantum/scientific compiler and runtime receipts",
            "formal verification verdicts bound into a portable proof object",
            "agent action admission and authority receipts",
        ],
        ["https://docs.wandb.ai/guides/artifacts/"],
        confidence="high",
    ),
    row(
        "data and pipeline versioning",
        "DVC",
        "ML/data teams and reproducible research groups",
        "Version-control adjunct for datasets, models, experiments, and reproducible data pipelines.",
        ["data versioning", "pipeline stages", "experiment tracking", "remote storage"],
        [
            "provider runtime receipt schema for quantum/scientific execution",
            "verifier verdict layer for research claims",
            "agent/tool action provenance receipts",
        ],
        ["https://dvc.org/doc"],
        confidence="high",
    ),
    row(
        "observability",
        "OpenTelemetry",
        "platform engineering, SRE, AI infrastructure teams",
        "Vendor-neutral observability framework for traces, metrics, and logs.",
        ["tracing", "metrics", "logs", "semantic conventions"],
        [
            "domain-specific scientific proof packet semantics",
            "quantum result canonicalization and compiler/runtime evidence receipts",
            "claim/verdict promotion ladder",
        ],
        ["https://opentelemetry.io/docs/"],
        confidence="high",
    ),
    row(
        "workflow orchestration",
        "Prefect",
        "data engineering and platform teams",
        "Python workflow orchestration for scheduling, observing, and managing data workflows.",
        ["flow orchestration", "task state", "deployment", "observability"],
        [
            "quantum/scientific result canonicalization",
            "proof verdicts and falsification fixtures",
            "source-to-action-to-output portable receipt packet",
        ],
        ["https://docs.prefect.io/"],
        confidence="high",
    ),
    row(
        "workflow orchestration",
        "Flyte",
        "ML, data, and AI platform teams",
        "Workflow orchestrator for data, ML, and analytics pipelines with reproducible execution concerns.",
        ["typed workflows", "reproducible tasks", "workflow execution", "data/ML pipeline focus"],
        [
            "quantum provider receipt profiles",
            "formal proof and claim-verdict packet",
            "agent authority/action ledger binding",
        ],
        ["https://docs.flyte.org/"],
        confidence="high",
    ),
    row(
        "scientific workflow orchestration",
        "Nextflow",
        "bioinformatics, HPC, and scientific pipeline teams",
        "Workflow system for scalable, portable, and reproducible computational pipelines.",
        ["portable workflows", "container/runtime integration", "HPC/cloud execution", "scientific pipeline focus"],
        [
            "quantum-specific compiler/runtime and provider evidence receipts",
            "LLM/tool action provenance",
            "formal verdict promotion ladder for claims",
        ],
        ["https://www.nextflow.io/docs/latest/"],
        confidence="high",
    ),
    row(
        "scientific workflow orchestration",
        "Snakemake",
        "bioinformatics, HPC, and reproducible data-analysis teams",
        "Workflow management system for reproducible and scalable data analyses.",
        ["rule-based workflows", "DAG execution", "HPC/cloud execution paths", "reproducibility support"],
        [
            "quantum provider receipt profiles",
            "agent/model action receipts",
            "portable proof-packet evidence object with verifier verdicts",
        ],
        ["https://snakemake.readthedocs.io/"],
        confidence="high",
    ),
]


def audit_imports() -> list[dict[str, object]]:
    packages = [
        ("qiskit", "qiskit"),
        ("qiskit-ibm-runtime", "qiskit_ibm_runtime"),
        ("amazon-braket-sdk", "braket"),
        ("cirq", "cirq"),
        ("pennylane", "pennylane"),
        ("pyqir", "pyqir"),
        ("pytket", "pytket"),
        ("cudaq", "cudaq"),
        ("qnexus", "qnexus"),
        ("pulser", "pulser"),
        ("covalent", "covalent"),
        ("mlflow", "mlflow"),
        ("wandb", "wandb"),
        ("dvc", "dvc"),
        ("opentelemetry-api", "opentelemetry"),
    ]
    rows: list[dict[str, object]] = []
    for distribution, module in packages:
        spec = importlib.util.find_spec(module)
        version: str | None = None
        version_status = "NOT_INSTALLED"
        try:
            version = importlib.metadata.version(distribution)
            version_status = "FOUND"
        except importlib.metadata.PackageNotFoundError:
            pass
        receipt = {
            "schema": "LocalPackageImportAuditReceipt/v1",
            "distribution": distribution,
            "module": module,
            "find_spec_available": spec is not None,
            "version": version,
            "version_status": version_status,
            "import_attempted": False,
            "audit_method": "importlib.util.find_spec plus importlib.metadata.version",
            "promotion_status": "AVAILABLE_FOR_OTEL_BRIDGE_ONLY" if distribution == "opentelemetry-api" and spec is not None else "NOT_PROMOTED_TO_FRAMEWORK_IMPORT_FIXTURE",
        }
        receipt["receipt_hash"] = sha256_obj(receipt)
        rows.append(receipt)
    return rows


def score(name: str, urgency: int, budget: int, differentiation: int, feasibility: int, demo: int, risk: int) -> dict[str, object]:
    return {
        "schema": "WedgeScore/v1",
        "market": name,
        "urgency": urgency,
        "budget": budget,
        "differentiation": differentiation,
        "feasibility": feasibility,
        "proof_demo_readiness": demo,
        "risk": risk,
        "ranking_note": "Scores are working hypotheses from the current comparison matrix, not market proof.",
    }


MEGATOOL_NODES = [
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "Gather",
        "external_analogs": ["web research", "crawler/intake", "literature collection"],
        "inputs": ["official docs", "papers", "repos", "local files"],
        "outputs": ["source receipts", "source-anchor catalog"],
        "receipts": ["ResearchClaim/v1", "SourceAnchor/v1"],
        "verification_layer": "strict URL/source availability and evidence confidence labels",
        "market_facing_product": "research intake proof packet",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "Index",
        "external_analogs": ["code search", "catalog", "knowledge graph"],
        "inputs": ["monorepo files", "tool manifests", "docs"],
        "outputs": ["workspace catalog", "scope map"],
        "receipts": ["IndexReceipt/v1"],
        "verification_layer": "catalog checksum and status checks",
        "market_facing_product": "workspace context spine",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "Forum",
        "external_analogs": ["review board", "adversarial planner", "model debate"],
        "inputs": ["claims", "plans", "draft packets"],
        "outputs": ["steelman objections", "planner witness", "ledger checkpoint"],
        "receipts": ["ForumLedgerReceipt/v1"],
        "verification_layer": "ledger chain verification; submit currently gated by executor JSON validity",
        "market_facing_product": "adversarial review layer",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "Crucible",
        "external_analogs": ["eval harness", "formal review", "evidence gate"],
        "inputs": ["thesis JSON", "measurement JSON"],
        "outputs": ["MATCH/DRIFT/UNVERIFIABLE verdicts"],
        "receipts": ["CrucibleAssessment/v1"],
        "verification_layer": "seal rederivation and claim-by-claim verdicts",
        "market_facing_product": "claim verification gate",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "Telos",
        "external_analogs": ["operator console", "control plane", "tool catalog"],
        "inputs": ["tool statuses", "operator manifests", "native-control surfaces"],
        "outputs": ["operator receipts", "catalog rows", "readiness checks"],
        "receipts": ["TelosOperatorReceipt/v1"],
        "verification_layer": "doctor/catalog/status checks",
        "market_facing_product": "proof-centered operator workbench",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "BuildLang/buildc",
        "external_analogs": ["Julia", "Mojo", "CUDA-Q", "MLIR/OpenXLA-adjacent stacks"],
        "inputs": ["scientific source", "compiler flags", "runtime targets"],
        "outputs": ["deterministic compute outputs", "compiler/runtime receipts"],
        "receipts": ["ScientificRuntimeReceipt/v1", "BuildReceipt/v1"],
        "verification_layer": "numeric precision, canonical output, resource, and executable provenance checks",
        "market_facing_product": "accountable scientific compute language/runtime",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "build-universe",
        "external_analogs": ["package registry", "toolchain distribution", "environment manager"],
        "inputs": ["toolchain packages", "benchmarks", "adapters"],
        "outputs": ["reproducible environment receipts", "adapter availability map"],
        "receipts": ["ToolchainUniverseReceipt/v1"],
        "verification_layer": "version, hash, and environment compatibility checks",
        "market_facing_product": "scientific toolchain universe",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "Build Color / calibration tools",
        "external_analogs": ["ACES/OCIO", "Calman", "ColourSpace", "DaVinci Resolve"],
        "inputs": ["patch measurements", "display/profile metadata", "render outputs"],
        "outputs": ["measured color receipts", "render fidelity packets"],
        "receipts": ["ColorMeasurementReceipt/v1"],
        "verification_layer": "delta metrics, profile hashes, calibration state, display chain metadata",
        "market_facing_product": "rendering/color measurement proof kit",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "browser evidence",
        "external_analogs": ["browser automation", "web capture", "RPA evidence"],
        "inputs": ["web pages", "screenshots", "DOM snapshots"],
        "outputs": ["source capture receipts", "interaction transcripts"],
        "receipts": ["BrowserEvidenceReceipt/v1"],
        "verification_layer": "URL, timestamp, content hash, screenshot hash, and action sequence checks",
        "market_facing_product": "web-evidence proof capture",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "model foundry",
        "external_analogs": ["model registry", "eval platform", "agent runtime"],
        "inputs": ["model configs", "prompts", "tool grants", "evals"],
        "outputs": ["model-use receipts", "eval verdicts", "policy gates"],
        "receipts": ["ModelRunReceipt/v1"],
        "verification_layer": "model identity, prompt hash, tool authority, and output verifier checks",
        "market_facing_product": "model provenance layer",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "loop ledger",
        "external_analogs": ["audit log", "experiment notebook", "ADR log"],
        "inputs": ["passes", "validator results", "tool receipts"],
        "outputs": ["persistent dogfood chain", "promotion history"],
        "receipts": ["LoopLedgerReceipt/v1"],
        "verification_layer": "pass ledger, artifact checksums, and status progression",
        "market_facing_product": "research accountability ledger",
    },
    {
        "schema": "MegatoolNode/v1",
        "internal_tool": "action receipts",
        "external_analogs": ["agent observability", "OpenTelemetry traces", "workflow event logs"],
        "inputs": ["tool calls", "workspace state", "authority/admission checks"],
        "outputs": ["accountable action events", "span/action bridges"],
        "receipts": ["ActionReceipt/v1"],
        "verification_layer": "authority, admission, execution, result, and verifier binding",
        "market_facing_product": "agent action proof packet",
    },
]


PROMOTION_LADDER = [
    {
        "state": "SYNTHETIC_ADAPTER_FIXTURE",
        "entry_criteria": "Adapter runs over synthetic provider-shaped output and hashes raw plus normalized results.",
        "exit_criteria": "Local framework package is available and fixture can use a real framework object without cloud execution.",
    },
    {
        "state": "FRAMEWORK_IMPORT_FIXTURE",
        "entry_criteria": "Package availability receipt is FOUND and local fixture imports the framework under pinned environment receipt.",
        "exit_criteria": "Provider/cloud credentials and read-only safety boundary are established, with content-addressed result retrieval.",
    },
    {
        "state": "LIVE_PROVIDER_FIXTURE",
        "entry_criteria": "A real provider job/task/result is captured with job id, backend, calibration/version references, shots, timestamps, result hash, and verifier verdict.",
        "exit_criteria": "Independent reproduction or a second backend/provider comparison is captured.",
    },
    {
        "state": "PUBLIC_PROOF_DEMO",
        "entry_criteria": "The packet contains source, code, environment, compiler/runtime, provider, result, verifier, and negative-fixture receipts.",
        "exit_criteria": "Buyer-facing demo can be re-run without secrets and without unsupported scientific claims.",
    },
]


DEMO_RECOMMENDATIONS = [
    {
        "demo": "Quantum workflow proof packet",
        "shape": "Take a simple Bell/no-cloning-style circuit through source intake, framework adapter, canonical result, negative fixtures, and Crucible verdict.",
        "near_term_blocker": "Quantum framework packages are not promoted until local import receipts show availability or a pinned environment is added.",
    },
    {
        "demo": "Observability-to-action proof packet",
        "shape": "Bridge OpenTelemetry-style spans to Telos action receipts and bind them to workspace, source, verifier, and admission records.",
        "near_term_blocker": "Requires a concrete agent workflow trace with stable tool-action schema.",
    },
    {
        "demo": "BuildLang scientific runtime receipt",
        "shape": "Run a deterministic numerical/color/rendering kernel and emit source, compiler, runtime, numeric precision, and measured-output receipts.",
        "near_term_blocker": "Requires BuildLang/buildc executable receipt implementation rather than shape-only market architecture.",
    },
]


record = {
    "schema": "QuantumWorkflowMarketImportSet/v1",
    "pass": "0020",
    "generated_on": "2026-07-01",
    "status": "MARKET_IMPORT_AUDIT_MATCH",
    "market_rows": MARKET_ROWS,
    "wedge_scorecard": [
        score("quantum workflow proof packets", 4, 4, 5, 4, 4, 3),
        score("cross-provider quantum result canonicalization", 4, 3, 5, 5, 5, 2),
        score("scientific workflow provenance bridge", 5, 4, 4, 4, 5, 3),
        score("BuildLang accountable scientific runtime", 4, 5, 5, 3, 3, 4),
    ],
    "package_import_audit": audit_imports(),
    "megatool_integration_map": MEGATOOL_NODES,
    "promotion_ladder": PROMOTION_LADDER,
    "demo_recommendations": DEMO_RECOMMENDATIONS,
    "source_anchors": SOURCE_ANCHORS,
    "primary_market_push": {
        "rank": 1,
        "market": "scientific workflow provenance bridge with quantum as the public proof domain",
        "thirty_day_motion": "Ship a rerunnable Bell/no-cloning quantum proof packet demo using synthetic adapters first, add pinned framework imports second, and use the same packet shape for BuildLang/color/runtime receipts.",
        "why_now": "Existing quantum, workflow, and observability products each cover part of the path, while the Telos wedge is the cross-layer receipt object. This is a hypothesis pending buyer interviews and demo tests.",
    },
    "non_promotion_statement": "Pass 0020 performs market mapping and local find_spec/version import audits only. It does not install packages, import unavailable frameworks, run quantum hardware, execute a provider job, or promote a scientific result.",
}
record["market_row_count"] = len(MARKET_ROWS)
record["source_anchor_count"] = len(SOURCE_ANCHORS)
record["audit_row_count"] = len(record["package_import_audit"])
record["seal"] = sha256_obj(record)

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "schemas" / "quantum-workflow-market-import-audit-pass-0020.json"
OUT_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"path": str(OUT_PATH), "schema": record["schema"], "seal": record["seal"], "market_row_count": record["market_row_count"], "audit_row_count": record["audit_row_count"], "source_anchor_count": record["source_anchor_count"]}, indent=2, sort_keys=True))
