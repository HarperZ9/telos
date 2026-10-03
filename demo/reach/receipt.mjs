// Reach receipts. Each fetch becomes one record (URL, time, status, robots
// decision, byte hash); each tool call wraps its records in a receipt that also
// names which model provider saw the session's trace. Writing to disk happens
// only when the user names a file (--receipt PATH or TELOS_REACH_RECEIPTS).
import { appendFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { TELOS_VERSION } from "../version.mjs";
import { BOUNDARY, userAgent } from "./identity.mjs";

export const RECEIPT_SCHEMA = "telos.reach-receipt/v1";

// Host client names map to the provider whose model reads the tool results.
// Retention is not checked by Telos; the receipt says so instead of guessing.
const PROVIDERS = [
  { match: /claude|anthropic/i, provider: "Anthropic", terms: "https://www.anthropic.com/legal/privacy" },
  { match: /codex|openai|chatgpt/i, provider: "OpenAI", terms: "https://openai.com/policies/privacy-policy" },
  { match: /gemini|google/i, provider: "Google", terms: "https://policies.google.com/privacy" },
  { match: /cursor/i, provider: "Cursor (model vendor set by the user)", terms: "https://cursor.com/privacy" },
  { match: /ollama|llama\.cpp|lm ?studio|local/i, provider: "local model (no remote provider)", terms: null },
];

/**
 * Which provider saw this session's trace. TELOS_TRACE_PROVIDER, set by the
 * user, wins; then the MCP client name the server received at initialize;
 * otherwise "unknown". A CLI run with neither is reported as unknown too.
 */
export function traceProvider(env = process.env) {
  const declared = typeof env.TELOS_TRACE_PROVIDER === "string" ? env.TELOS_TRACE_PROVIDER.trim() : "";
  const client = typeof env.TELOS_MCP_CLIENT === "string" ? env.TELOS_MCP_CLIENT.trim() : "";
  const source = declared ? "TELOS_TRACE_PROVIDER" : client ? "mcp clientInfo.name" : "none";
  const name = declared || client;
  const known = name ? PROVIDERS.find((p) => p.match.test(name)) : null;
  return {
    provider: known?.provider ?? (name || "unknown"),
    client: client || null,
    source,
    terms_url: known?.terms ?? null,
    retention: "unknown: Telos does not check provider retention terms",
    line: `Trace seen by: ${known?.provider ?? (name || "unknown")} (source: ${source})`,
  };
}

/** One fetch record. `robots` is the decision string or null for API calls. */
export function fetchRecord(result, { robots = null, channel = "web", at = new Date() } = {}) {
  return {
    url: result.url,
    channel,
    at: at.toISOString(),
    status: result.status,
    robots,
    refused: result.refused ?? null,
    bot_check: Boolean(result.bot_check),
    cache: result.cache ?? null,
    bytes: result.bytes ?? 0,
    bytes_sha256: result.bytes_sha256 ?? null,
  };
}

/** Wrap records into the receipt a tool returns. */
export function reachReceipt({ tool, records, cost = null, env = process.env, at = new Date() }) {
  return {
    schema: RECEIPT_SCHEMA,
    tool,
    telos_version: TELOS_VERSION,
    at: at.toISOString(),
    user_agent: userAgent(env),
    fetches: records,
    cost,
    trace: traceProvider(env),
    boundary: BOUNDARY,
  };
}

/** Append the receipt as one JSON line when the user asked for a file. */
export function writeReceipt(receipt, file) {
  if (!file) return null;
  const resolved = path.resolve(file);
  mkdirSync(path.dirname(resolved), { recursive: true });
  appendFileSync(resolved, `${JSON.stringify(receipt)}\n`);
  return resolved;
}
