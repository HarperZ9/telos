import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";

import { attachScore } from "./scoring.mjs";
import { assertCandidate } from "./schema.mjs";

const fixtureUrl = new URL("./fixtures/pandas-66050.json", import.meta.url);

export function scoutFixture({ now = new Date() } = {}) {
  const candidate = attachScore(JSON.parse(readFileSync(fixtureUrl, "utf8")), now);
  return {
    schema: "project-telos.oss-scout/v1",
    captured_at: now.toISOString(),
    source: {
      kind: "fixture",
      query: "pandas-dev/pandas#66050"
    },
    candidates: [candidate]
  };
}

export function scoutLive({ query, limit = 5, now = new Date(), run = spawnSync } = {}) {
  const searchQuery = query || "repo:pandas-dev/pandas is:issue is:open label:Bug pd.array masked array";
  const result = run("gh", [
    "search",
    "issues",
    searchQuery,
    "--limit",
    String(limit),
    "--json",
    "title,number,url,updatedAt,labels,commentsCount,repository"
  ], { encoding: "utf8" });
  if (result.status !== 0) {
    return {
      schema: "project-telos.oss-scout/v1",
      captured_at: now.toISOString(),
      status: "UNVERIFIABLE",
      source: { kind: "github", query: searchQuery },
      candidates: [],
      diagnostics: [{ message: result.stderr || result.stdout || "gh search failed" }]
    };
  }
  const rows = JSON.parse(result.stdout);
  const candidates = rows.map((row) => attachScore(candidateFromIssue(row, now), now));
  return {
    schema: "project-telos.oss-scout/v1",
    captured_at: now.toISOString(),
    status: "MATCH",
    source: { kind: "github", query: searchQuery },
    candidates
  };
}

export function candidateFromIssue(row, now = new Date()) {
  const fullName = row.repository?.nameWithOwner || "unknown/unknown";
  const labels = (row.labels || []).map((label) => label.name || label);
  const candidate = {
    schema: "project-telos.oss-candidate/v1",
    captured_at: now.toISOString(),
    repository: {
      full_name: fullName,
      url: `https://github.com/${fullName}`,
      stars: 0,
      language: "unknown",
      open_issues: 0
    },
    issue: {
      number: row.number,
      url: row.url,
      title: row.title,
      labels,
      comments_count: row.commentsCount ?? 0,
      updated_at: row.updatedAt
    },
    signals: inferSignals(row),
    score: {
      patchability: 0,
      showcase_value: 0,
      risk: 0,
      priority: 0,
      reasons: []
    },
    next_actions: []
  };
  assertCandidate(candidate);
  return candidate;
}

function inferSignals(row) {
  const text = `${row.title || ""}\n${row.body || ""}`.toLowerCase();
  return {
    has_reproduction: /repro|reproduction|steps to reproduce|example/.test(text),
    has_expected_behavior: /expected/.test(text),
    maintainer_invited_pr: /sure thing|pr welcome|pull request welcome/.test(text),
    likely_docs_only: /doc|readme|typo/.test(text),
    requires_gpu_or_large_model: /gpu|cuda|large model|oom/.test(text),
    security_sensitive: /security|cve|credential|token/.test(text),
    ambiguous_expected_behavior: !/expected/.test(text)
  };
}

export function renderScoutTable(payload) {
  const lines = ["OSS Proof Showcase Candidates", "priority  repo#issue  title"];
  for (const candidate of payload.candidates) {
    lines.push(
      `${String(candidate.score.priority).padStart(8)}  ${candidate.repository.full_name}#${candidate.issue.number}  ${candidate.issue.title}`
    );
  }
  return `${lines.join("\n")}\n`;
}
