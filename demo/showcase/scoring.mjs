import { assertCandidate } from "./schema.mjs";

const DAY_MS = 24 * 60 * 60 * 1000;

export function scoreCandidate(candidate, now = new Date()) {
  assertCandidate(candidate);
  const reasons = [];
  let patchability = 0;
  let showcaseValue = 0;
  let risk = 0;

  if (candidate.signals.has_reproduction) {
    patchability += 30;
    reasons.push("has reproduction");
  }
  if (candidate.signals.has_expected_behavior) {
    patchability += 20;
    reasons.push("has expected behavior");
  }
  const updatedAt = new Date(candidate.issue.updated_at);
  if (!Number.isNaN(updatedAt.valueOf()) && now - updatedAt <= 14 * DAY_MS) {
    patchability += 10;
    reasons.push("updated within 14 days");
  }
  if (candidate.signals.maintainer_invited_pr) {
    showcaseValue += 25;
    reasons.push("maintainer invited PR");
  }
  if (candidate.repository.stars >= 100000) {
    showcaseValue += 10;
    reasons.push("repository has over 100k stars");
  }
  if (candidate.signals.requires_gpu_or_large_model) {
    risk += 35;
    reasons.push("requires GPU or large model");
  }
  if (candidate.signals.security_sensitive) {
    risk += 40;
    reasons.push("security sensitive");
  }
  if (candidate.signals.ambiguous_expected_behavior) {
    risk += 25;
    reasons.push("ambiguous expected behavior");
  }

  const priority = candidate.signals.has_reproduction
    ? Math.max(0, patchability + showcaseValue - risk)
    : 0;

  return {
    patchability,
    showcase_value: showcaseValue,
    risk,
    priority,
    reasons
  };
}

export function attachScore(candidate, now = new Date()) {
  return {
    ...candidate,
    score: scoreCandidate(candidate, now)
  };
}
