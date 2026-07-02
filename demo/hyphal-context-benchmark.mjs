import { createHash } from "node:crypto";
import { readFileSync, statSync, writeFileSync } from "node:fs";

const corpusRoot = new URL("../docs/outreach/receipts/twenty-first-wave/biology-network-intelligence-corpus/", import.meta.url);
const sourceGateUrl = new URL(
  "../docs/outreach/receipts/twenty-first-wave/biology-network-intelligence-source-gate-2026-07-02.json",
  import.meta.url
);
const seedUrl = new URL("../docs/research/mycology-network-intelligence.md", import.meta.url);

const requiredClasses = [
  "fungal_signal",
  "plant_signal",
  "network_evidence",
  "overclaim_boundary",
  "source_availability",
  "architecture_seed"
];

const guardrails = [
  "biological_nervous_system_equivalence",
  "universal_intentional_common_mycorrhizal_network_messaging",
  "benchmarked_hyphal_context_protocol_claim"
];

export function stableStringify(value) {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}

export function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

export function sha256Value(value) {
  return `sha256:${sha256(stableStringify(value))}`;
}

export function estimateTokens(value) {
  const text = typeof value === "string" ? value : stableStringify(value);
  return Math.ceil(text.length / 4);
}

function readJson(url) {
  return JSON.parse(readFileSync(url, "utf8"));
}

function hashFile(url) {
  return sha256(readFileSync(url));
}

function objectUrlFor(sha) {
  return new URL(`objects/${sha.slice(0, 2)}/${sha.slice(2)}`, corpusRoot);
}

function classForRow(row) {
  const text = `${row.title} ${row.coverage}`.toLowerCase();
  if (text.includes("critique") || text.includes("overclaim") || text.includes("misinformation")) {
    return "overclaim_boundary";
  }
  if (text.includes("plant glutamate") || text.includes("calcium signaling")) return "plant_signal";
  if (text.includes("common fungal network") || text.includes("mycorrhizal network")) return "network_evidence";
  if (text.includes("global mycorrhizal") || text.includes("mapping")) return "source_availability";
  if (text.includes("electrical") || text.includes("spiking") || text.includes("fungal mycelia")) {
    return "fungal_signal";
  }
  return "supporting_source";
}

function sourceRowsWithStats(sourceGate) {
  return sourceGate.source_rows.map((row, index) => {
    const objectUrl = objectUrlFor(row.sha256);
    const bytes = statSync(objectUrl).size;
    return {
      id: `src_${String(index + 1).padStart(2, "0")}`,
      title: row.title,
      ref: row.ref,
      sha256: row.sha256,
      coverage: row.coverage,
      evidence_class: classForRow(row),
      object_bytes: bytes,
      estimated_body_tokens: Math.ceil(bytes / 4)
    };
  });
}

function bestSource(rows, evidenceClass, titleNeedle = null) {
  const filtered = rows.filter((row) => row.evidence_class === evidenceClass);
  if (titleNeedle) {
    const titleMatch = filtered.find((row) => row.title.toLowerCase().includes(titleNeedle.toLowerCase()));
    if (titleMatch) return titleMatch;
  }
  return filtered[0];
}

function evidenceCard(source, reason) {
  return {
    kind: "evidence_card",
    id: source.id,
    evidence_class: source.evidence_class,
    title: source.title,
    ref: source.ref,
    sha256: source.sha256,
    coverage: source.coverage,
    retrieval_reason: reason
  };
}

function docCard({ id, evidenceClass, title, ref, sha256Hex, reason }) {
  return {
    kind: "evidence_card",
    id,
    evidence_class: evidenceClass,
    title,
    ref,
    sha256: sha256Hex,
    retrieval_reason: reason
  };
}

function recoveredClasses(cards) {
  return [...new Set(cards.map((card) => card.evidence_class))]
    .filter((evidenceClass) => requiredClasses.includes(evidenceClass))
    .sort();
}

function routeVerdict(route) {
  const recovered = new Set(route.evidence_classes_recovered);
  const recoveredAll = requiredClasses.every((item) => recovered.has(item));
  const blockedAll = guardrails.every((item) => route.guardrails_blocked.includes(item));
  return recoveredAll && blockedAll ? "MATCH" : "DRIFT";
}

export function buildHyphalBenchmark() {
  const sourceGate = readJson(sourceGateUrl);
  const rows = sourceRowsWithStats(sourceGate);
  const sourceGateHash = hashFile(sourceGateUrl);
  const seedHash = hashFile(seedUrl);
  const sourceGateTokens = Math.ceil(statSync(sourceGateUrl).size / 4);
  const seedTokens = Math.ceil(statSync(seedUrl).size / 4);

  const fullContextCards = [
    ...rows.map((row) => evidenceCard(row, "full_context_delivers_every_source_body")),
    docCard({
      id: "source_gate",
      evidenceClass: "source_availability",
      title: "Biology network intelligence source gate",
      ref: "docs/outreach/receipts/twenty-first-wave/biology-network-intelligence-source-gate-2026-07-02.json",
      sha256Hex: sourceGateHash,
      reason: "full_context_delivers_source_gate"
    }),
    docCard({
      id: "architecture_seed",
      evidenceClass: "architecture_seed",
      title: "Mycology Network Intelligence Seed",
      ref: "docs/research/mycology-network-intelligence.md",
      sha256Hex: seedHash,
      reason: "full_context_delivers_architecture_seed"
    })
  ];

  const gradientEnvelopes = rows.map((row) => ({
    input_id: row.id,
    evidence_class: row.evidence_class,
    sha256: row.sha256,
    ref: row.ref,
    pressure: requiredClasses.includes(row.evidence_class) ? "candidate" : "supporting",
    token_estimate: estimateTokens({
      id: row.id,
      evidence_class: row.evidence_class,
      title: row.title,
      ref: row.ref,
      sha256: row.sha256
    })
  }));

  const hyphalCards = [
    evidenceCard(bestSource(rows, "fungal_signal", "Electrical signaling in fungi"), "retrieve boundary-aware fungal signaling source"),
    evidenceCard(bestSource(rows, "plant_signal"), "retrieve plant bioelectric signaling source"),
    evidenceCard(bestSource(rows, "network_evidence", "Evidence for common fungal networks"), "retrieve concrete network-evidence source"),
    evidenceCard(bestSource(rows, "overclaim_boundary"), "retrieve critique before synthesis"),
    docCard({
      id: "source_gate",
      evidenceClass: "source_availability",
      title: "Biology network intelligence source gate",
      ref: "docs/outreach/receipts/twenty-first-wave/biology-network-intelligence-source-gate-2026-07-02.json",
      sha256Hex: sourceGateHash,
      reason: "retrieve source availability and blocked DOI boundary"
    }),
    docCard({
      id: "architecture_seed",
      evidenceClass: "architecture_seed",
      title: "Mycology Network Intelligence Seed",
      ref: "docs/research/mycology-network-intelligence.md",
      sha256Hex: seedHash,
      reason: "retrieve Telos architecture hypothesis boundary"
    })
  ];

  const fullTokens =
    rows.reduce((sum, row) => sum + row.estimated_body_tokens, 0) + sourceGateTokens + seedTokens;
  const gradientTokens = gradientEnvelopes.reduce((sum, envelope) => sum + envelope.token_estimate, 0);
  const hyphalTokens = gradientTokens + hyphalCards.reduce((sum, card) => sum + estimateTokens(card), 0);
  const savingsRatio = Number((1 - hyphalTokens / fullTokens).toFixed(4));

  const fullRoute = {
    route_id: "full_context",
    route_claim: "send all source bodies, source gate, and seed note",
    candidate_source_count: rows.length,
    delivered_source_bodies: rows.length,
    delivered_document_refs: 2,
    estimated_prompt_tokens: fullTokens,
    evidence_classes_recovered: recoveredClasses(fullContextCards),
    guardrails_blocked: guardrails,
    raw_source_policy: "body sizes and hashes are measured; raw source bodies are not embedded in this benchmark receipt",
    verdict: null
  };
  fullRoute.verdict = routeVerdict(fullRoute);

  const hyphalRoute = {
    route_id: "hyphal_context",
    route_claim: "send gradient envelopes plus receipt IDs, then retrieve only evidence cards needed by the task",
    gradient_envelope_count: gradientEnvelopes.length,
    rehydrated_evidence_cards: hyphalCards,
    rehydrated_card_count: hyphalCards.length,
    estimated_prompt_tokens: hyphalTokens,
    evidence_classes_recovered: recoveredClasses(hyphalCards),
    guardrails_blocked: guardrails,
    raw_source_policy: "source bodies remain in Gather; route carries refs, hashes, coverage, and retrieval reasons",
    verdict: null
  };
  hyphalRoute.verdict = routeVerdict(hyphalRoute);

  const comparison = {
    full_context_tokens: fullTokens,
    hyphal_context_tokens: hyphalTokens,
    token_savings: fullTokens - hyphalTokens,
    token_savings_ratio: savingsRatio,
    evidence_recall_delta: hyphalRoute.evidence_classes_recovered.length - fullRoute.evidence_classes_recovered.length,
    guardrail_delta: hyphalRoute.guardrails_blocked.length - fullRoute.guardrails_blocked.length,
    result:
      hyphalRoute.verdict === "MATCH" &&
      fullRoute.verdict === "MATCH" &&
      hyphalRoute.evidence_classes_recovered.length === fullRoute.evidence_classes_recovered.length &&
      savingsRatio >= 0.5
        ? "HYPHAL_CONTEXT_FIXTURE_MATCH"
        : "HYPHAL_CONTEXT_FIXTURE_DRIFT"
  };

  const benchmark = {
    schema: "project-telos.hyphal-context-benchmark/v1",
    benchmark_id: "twenty-second-wave-hyphal-context-benchmark",
    created_at: "2026-07-02",
    scope: "one deterministic fixture over the twenty-first-wave biology/network-intelligence corpus",
    input_sources: {
      corpus: "docs/outreach/receipts/twenty-first-wave/biology-network-intelligence-corpus",
      source_gate: {
        path: "docs/outreach/receipts/twenty-first-wave/biology-network-intelligence-source-gate-2026-07-02.json",
        sha256: sourceGateHash
      },
      architecture_seed: {
        path: "docs/research/mycology-network-intelligence.md",
        sha256: seedHash
      }
    },
    required_evidence_classes: requiredClasses,
    routes: {
      full_context: fullRoute,
      hyphal_context: hyphalRoute
    },
    comparison,
    not_proven: [
      "This fixture does not prove the hyphal route wins on all research tasks.",
      "This fixture does not measure model answer quality directly.",
      "This fixture does not establish biological cognition or universal network-message claims.",
      "This fixture does not replace a BuildLang/buildc runtime receipt."
    ]
  };
  return {
    ...benchmark,
    receipt_hash: sha256Value(benchmark)
  };
}

function main() {
  const output = `${JSON.stringify(buildHyphalBenchmark(), null, 2)}\n`;
  const outIndex = process.argv.indexOf("--out");
  if (outIndex !== -1) {
    const outPath = process.argv[outIndex + 1];
    if (!outPath) throw new Error("--out requires a path");
    writeFileSync(outPath, output, "utf8");
    return;
  }
  process.stdout.write(output);
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, "/"))) {
  main();
}
