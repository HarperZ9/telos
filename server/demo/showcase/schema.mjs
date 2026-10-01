export const OSS_CANDIDATE_SCHEMA = "project-telos.oss-candidate/v1";
export const OSS_PACKET_SCHEMA = "project-telos.oss-pr-readiness/v1";

export function assertCandidate(candidate) {
  if (candidate?.schema !== OSS_CANDIDATE_SCHEMA) {
    throw new Error(`bad candidate schema: ${candidate?.schema}`);
  }
  for (const key of ["repository", "issue", "signals", "score", "next_actions"]) {
    if (!(key in candidate)) {
      throw new Error(`missing candidate key: ${key}`);
    }
  }
  for (const key of ["full_name", "url", "stars", "language", "open_issues"]) {
    if (!(key in candidate.repository)) {
      throw new Error(`missing repository key: ${key}`);
    }
  }
  for (const key of ["number", "url", "title", "labels", "comments_count", "updated_at"]) {
    if (!(key in candidate.issue)) {
      throw new Error(`missing issue key: ${key}`);
    }
  }
  return true;
}

export function assertPacket(packet) {
  if (packet?.schema !== OSS_PACKET_SCHEMA) {
    throw new Error(`bad packet schema: ${packet?.schema}`);
  }
  for (const key of ["candidate", "evidence", "verdict", "operator_next_action", "pr_ready"]) {
    if (!(key in packet)) {
      throw new Error(`missing packet key: ${key}`);
    }
  }
  assertNoSensitivePaths(packet);
  return true;
}

export function assertNoSensitivePaths(value) {
  const text = JSON.stringify(value);
  if (/C:\\\\Users\\\\[^"\\]+/i.test(text)) {
    throw new Error("sensitive local path detected");
  }
  if (/\.env(?:\.|["\\/\s]|$)/i.test(text)) {
    throw new Error("environment file reference detected");
  }
  if (/(api[_-]?key|access[_-]?token|password)\s*[:=]\s*[^"'\s]{8,}/i.test(text)) {
    throw new Error("token-like field detected");
  }
  return true;
}
