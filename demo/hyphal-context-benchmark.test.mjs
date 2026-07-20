import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { buildHyphalBenchmark, sha256 } from "./hyphal-context-benchmark.mjs";
import * as hyphalBenchmark from "./hyphal-context-benchmark.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, "..");
const packet = buildHyphalBenchmark();

assert.equal(
  hyphalBenchmark.canonicalText?.("line one\r\nline two\rline three\n"),
  "line one\nline two\nline three\n",
  "canonical text must collapse CRLF and CR to LF"
);
const lfStats = hyphalBenchmark.canonicalSourceStats?.("alpha\nbeta\n");
assert.equal(
  typeof hyphalBenchmark.canonicalSourceStats,
  "function",
  "benchmark must expose the canonical source-stat contract"
);
assert.deepEqual(
  hyphalBenchmark.canonicalSourceStats?.("alpha\r\nbeta\r\n"),
  lfStats,
  "CRLF corpus bodies must produce the same hash and token count as LF"
);
assert.deepEqual(
  hyphalBenchmark.canonicalSourceStats?.("alpha\rbeta\r"),
  lfStats,
  "bare-CR corpus bodies must produce the same hash and token count as LF"
);

function canonicalTextHash(relativePath) {
  const text = readFileSync(path.join(here, "..", relativePath), "utf8");
  return sha256(text.replace(/\r\n?/g, "\n"));
}

assert.equal(
  packet.input_sources.source_gate.sha256,
  canonicalTextHash(packet.input_sources.source_gate.path),
  "source-gate provenance must be stable across LF and CRLF checkouts"
);
assert.equal(
  packet.input_sources.architecture_seed.sha256,
  canonicalTextHash(packet.input_sources.architecture_seed.path),
  "architecture-seed provenance must be stable across LF and CRLF checkouts"
);

assert.equal(packet.schema, "project-telos.hyphal-context-benchmark/v1");
assert.equal(packet.benchmark_id, "twenty-second-wave-hyphal-context-benchmark");
assert.equal(packet.comparison.result, "HYPHAL_CONTEXT_FIXTURE_MATCH");
assert.equal(packet.routes.full_context.verdict, "MATCH");
assert.equal(packet.routes.hyphal_context.verdict, "MATCH");
assert.match(packet.receipt_hash, /^sha256:[a-f0-9]{64}$/);

assert.equal(packet.routes.full_context.candidate_source_count, 10);
assert.equal(packet.routes.full_context.delivered_source_bodies, 10);
assert.equal(packet.routes.hyphal_context.gradient_envelope_count, 10);
assert.equal(packet.routes.hyphal_context.rehydrated_card_count, 6);
assert.ok(packet.comparison.hyphal_context_tokens < packet.comparison.full_context_tokens);
assert.ok(packet.comparison.token_savings_ratio >= 0.5);
assert.equal(packet.comparison.evidence_recall_delta, 0);
assert.equal(packet.comparison.guardrail_delta, 0);

const required = new Set(packet.required_evidence_classes);
for (const route of [packet.routes.full_context, packet.routes.hyphal_context]) {
  const recovered = new Set(route.evidence_classes_recovered);
  for (const evidenceClass of required) {
    assert.ok(recovered.has(evidenceClass), `${route.route_id} missed ${evidenceClass}`);
  }
  assert.deepEqual(route.guardrails_blocked, [
    "biological_nervous_system_equivalence",
    "universal_intentional_common_mycorrhizal_network_messaging",
    "benchmarked_hyphal_context_protocol_claim"
  ]);
}

function scanNoRawBodies(value, pathSoFar = "$") {
  if (!value || typeof value !== "object") return;
  if (Array.isArray(value)) {
    value.forEach((item, index) => scanNoRawBodies(item, `${pathSoFar}[${index}]`));
    return;
  }
  for (const [key, child] of Object.entries(value)) {
    assert.notEqual(key, "raw_source_body", `${pathSoFar}.${key} leaks a raw source body`);
    assert.notEqual(key, "raw_context", `${pathSoFar}.${key} leaks raw context`);
    scanNoRawBodies(child, `${pathSoFar}.${key}`);
  }
}
scanNoRawBodies(packet);

const run = spawnSync(process.execPath, [path.join(here, "hyphal-context-benchmark.mjs")], {
  cwd: repoRoot,
  encoding: "utf8"
});
assert.equal(run.status, 0, run.stderr || run.stdout);
assert.deepEqual(JSON.parse(run.stdout), packet);

const frozenReceipt = JSON.parse(
  readFileSync(
    path.join(here, "..", "docs", "outreach", "receipts", "twenty-second-wave", "hyphal-context-benchmark-2026-07-02.json"),
    "utf8"
  )
);
assert.deepEqual(frozenReceipt, packet);

const correctionRelativePath =
  "docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-correction-2026-07-18.json";

function readRepoText(relativePath) {
  return readFileSync(path.join(repoRoot, relativePath), "utf8");
}

function canonicalFileSha256(relativePath) {
  return sha256(readRepoText(relativePath).replace(/\r\n?/g, "\n"));
}

function runGit(args, encoding = "utf8") {
  const result = spawnSync("git", args, { cwd: repoRoot, encoding });
  assert.equal(result.status, 0, result.stderr || result.stdout || `git ${args.join(" ")} failed`);
  return result.stdout;
}

function gitTextAt(commit, relativePath) {
  return runGit(["show", `${commit}:${relativePath}`], "utf8");
}

function gitBufferAt(commit, relativePath) {
  return runGit(["show", `${commit}:${relativePath}`], null);
}

assert.match(
  readRepoText(".github/workflows/ci.yml"),
  /path:\s*telos[\s\S]*?fetch-depth:\s*0/,
  "CI must fetch Telos history so provenance claims are reverified"
);

const correction = JSON.parse(readRepoText(correctionRelativePath));
assert.equal(correction.schema, "project-telos.hyphal-context-benchmark-correction/v1");
const history = correction.source_history;

for (const commit of [
  history.source_packet_commit,
  history.benchmark_packet_commit,
  history.evaluated_through_commit,
  correction.canonical_receipt.merge_commit
]) {
  runGit(["cat-file", "-e", `${commit}^{commit}`]);
}

const sourceDiff = spawnSync(
  "git",
  [
    "diff",
    "--quiet",
    history.benchmark_packet_commit,
    history.evaluated_through_commit,
    "--",
    ...Object.values(history.source_paths)
  ],
  { cwd: repoRoot, encoding: "utf8" }
);
assert.equal(
  sourceDiff.status,
  0,
  sourceDiff.stderr || "source content changed between the benchmark and evaluated correction commits"
);
assert.equal(correction.source_history.source_content_changed_after_benchmark, false);
assert.equal(correction.historical_receipt.recoverable_at_commit, history.benchmark_packet_commit);
assert.equal(correction.canonical_receipt.merge_commit, history.evaluated_through_commit);

const historicalArtifactPaths = {
  generator: "demo/hyphal-context-benchmark.mjs",
  test: "demo/hyphal-context-benchmark.test.mjs",
  receipt: "docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-2026-07-02.json"
};
for (const [artifact, relativePath] of Object.entries(historicalArtifactPaths)) {
  assert.equal(
    correction.historical_receipt.artifact_canonical_text_sha256[artifact],
    sha256(gitTextAt(history.benchmark_packet_commit, relativePath).replace(/\r\n?/g, "\n"))
  );
}

const historicalPacket = JSON.parse(
  gitTextAt(history.benchmark_packet_commit, historicalArtifactPaths.receipt)
);
assert.deepEqual(correction.historical_receipt.comparison, {
  full_context_tokens: historicalPacket.comparison.full_context_tokens,
  hyphal_context_tokens: historicalPacket.comparison.hyphal_context_tokens,
  token_savings: historicalPacket.comparison.token_savings,
  token_savings_ratio: historicalPacket.comparison.token_savings_ratio
});
assert.equal(correction.historical_receipt.receipt_hash, historicalPacket.receipt_hash);

const lfReproduction = correction.reproduction.clean_lf_checkout;
const lfSourceGate = gitBufferAt(lfReproduction.source_commit, history.source_paths.source_gate);
const lfSourceGateJson = JSON.parse(lfSourceGate.toString("utf8"));
const lfCorpusTokens = lfSourceGateJson.source_rows.reduce((total, row) => {
  const relativePath = `${history.source_paths.corpus_objects}/${row.sha256.slice(0, 2)}/${row.sha256.slice(2)}`;
  return total + Math.ceil(gitBufferAt(lfReproduction.source_commit, relativePath).length / 4);
}, 0);
const lfSeed = gitBufferAt(lfReproduction.source_commit, history.source_paths.architecture_seed);
const lfFullContextTokens =
  lfCorpusTokens + Math.ceil(lfSourceGate.length / 4) + Math.ceil(lfSeed.length / 4);
assert.equal(lfReproduction.comparison.full_context_tokens, lfFullContextTokens);
assert.equal(lfReproduction.architecture_seed_sha256, sha256(lfSeed));

assert.deepEqual(correction.canonical_receipt.comparison, {
  full_context_tokens: packet.comparison.full_context_tokens,
  hyphal_context_tokens: packet.comparison.hyphal_context_tokens,
  token_savings: packet.comparison.token_savings,
  token_savings_ratio: packet.comparison.token_savings_ratio
});
assert.equal(correction.canonical_receipt.receipt_hash, packet.receipt_hash);
assert.equal(
  correction.canonical_receipt.artifact_canonical_text_sha256.generator,
  canonicalFileSha256("demo/hyphal-context-benchmark.mjs")
);
assert.equal(
  correction.canonical_receipt.artifact_canonical_text_sha256.receipt,
  canonicalFileSha256(
    "docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-2026-07-02.json"
  )
);

function formatInteger(value) {
  return String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function includesNumericValue(text, value) {
  const escaped = value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(^|[^\\d])${escaped}(?!\\d)`, "m").test(text);
}

assert.equal(includesNumericValue("historical ratio 0.9892", "0.989"), false);
assert.equal(includesNumericValue("current ratio 0.989", "0.989"), true);

const publicDocs = [
  {
    path: "docs/outreach/TWENTY-SECOND-WAVE-HYPHAL-CONTEXT-BENCHMARK-2026-07-02.md",
    currentValues: [
      formatInteger(packet.comparison.full_context_tokens),
      formatInteger(packet.comparison.token_savings),
      String(packet.comparison.token_savings_ratio)
    ],
    historicalValues: ["123,413", "122,075", "0.9892"]
  },
  {
    path: "docs/research/official/HYPHAL-CONTEXT-BENCHMARK-FOR-RECEIPT-ROUTING-2026-07-02.md",
    currentValues: [
      String(packet.comparison.full_context_tokens),
      String(packet.comparison.token_savings),
      String(packet.comparison.token_savings_ratio)
    ],
    historicalValues: ["123413", "122075", "0.9892"],
    requiresArtifactDigests: true
  },
  {
    path: "docs/research/whitepapers/HYPHAL-CONTEXT-BENCHMARK-FOR-RECEIPT-ROUTING-2026-07-02.md",
    currentValues: [
      formatInteger(packet.comparison.full_context_tokens),
      String(packet.comparison.token_savings),
      String(packet.comparison.token_savings_ratio)
    ],
    historicalValues: ["123,413", "122075", "0.9892"],
    requiresArtifactDigests: true
  }
];

for (const document of publicDocs) {
  const text = readRepoText(document.path);
  assert.match(text, /Reproducibility correction \(2026-07-18\)/);
  assert.ok(text.includes(correctionRelativePath), `${document.path} must link the correction receipt`);
  for (const value of document.currentValues) {
    assert.ok(includesNumericValue(text, value), `${document.path} must include current value ${value}`);
  }
  for (const value of document.historicalValues) {
    assert.ok(
      includesNumericValue(text, value),
      `${document.path} must preserve historical value ${value}`
    );
  }
  if (document.requiresArtifactDigests) {
    for (const relativePath of [
      "demo/hyphal-context-benchmark.mjs",
      "demo/hyphal-context-benchmark.test.mjs",
      "docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-2026-07-02.json"
    ]) {
      assert.ok(
        text.includes(canonicalFileSha256(relativePath)),
        `${document.path} must include the current canonical digest for ${relativePath}`
      );
    }
  }
}
