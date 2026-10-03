// One entry point for every reach command, shared by the CLI and the MCP
// server. Dependencies (fetch, sleep, clock, env) are injectable so tests run
// with no network. Every networked command returns { result, receipt }.
import { callApi } from "./apis.mjs";
import { ResponseCache } from "./cache.mjs";
import { Crawler } from "./crawler.mjs";
import { reachDoctor } from "./doctor.mjs";
import { ReachHttp } from "./http.mjs";
import { HostLimiter } from "./limiter.mjs";
import { reachMenu, readMemory, remember } from "./menu.mjs";
import { reachReceipt, writeReceipt } from "./receipt.mjs";
import { RedditReader } from "./reddit.mjs";
import { XReader } from "./x.mjs";

export const COMMANDS = ["doctor", "menu", "fetch", "site", "reddit-listing", "reddit-comments", "x-oembed", "x-api", "api"];

function makeHttp(deps) {
  const limiter = new HostLimiter({ sleep: deps.sleep, now: deps.now });
  const cache = deps.cache ?? ResponseCache.fromEnv(deps.env, { now: deps.now });
  return new ReachHttp({ fetchImpl: deps.fetchImpl ?? globalThis.fetch, limiter, cache, env: deps.env });
}

async function crawlFetch(params, http) {
  const crawler = new Crawler({ http });
  const result = await crawler.fetchPage(params.url);
  return { result, records: crawler.records, verb: "crawl.fetch", target: params.url, status: result.status };
}

async function crawlSite(params, http) {
  const crawler = new Crawler({ http });
  const result = await crawler.crawlSite(params.url, { depth: params.depth, pageBudget: params.page_budget ?? params.budget, sameHost: params.same_host !== false });
  return { result, records: crawler.records, verb: "crawl.site", target: params.url, status: 200 };
}

async function reddit(params, http, env, mode) {
  const reader = new RedditReader({ http, env });
  const result = mode === "listing"
    ? await reader.listing(params.subreddit, { sort: params.sort, limit: params.limit, time: params.time })
    : await reader.comments(params.post_id ?? params.id, { depth: params.depth, limit: params.limit });
  return { result, records: reader.records, verb: `reddit.${mode}`, target: params.subreddit ?? params.post_id ?? params.id, status: 200 };
}

async function xOembed(params, http, env) {
  const reader = new XReader({ http, env });
  const result = await reader.oembed(params.url);
  return { result, records: reader.records, verb: "x.oembed", target: params.url, status: result.available ? 200 : 404 };
}

async function xApi(params, http, env) {
  const reader = new XReader({ http, env });
  const op = params.op ?? "post";
  let result;
  if (op === "post") result = await reader.post(params.id);
  else if (op === "search_recent") result = await reader.searchRecent(params.query, { max: params.max });
  else if (op === "user_posts") result = await reader.userPosts(params.username, { max: params.max });
  else throw new Error("x api op must be post, search_recent or user_posts");
  return { result, records: reader.records, cost: result.cost, verb: "x.api", target: params.id ?? params.query ?? params.username, status: 200 };
}

async function officialApi(params, http, env) {
  const { data, error, record } = await callApi(http, params.channel, params.op, params.params ?? {}, env);
  return { result: { channel: params.channel, op: params.op, data, error: error ?? null }, records: [record], verb: "reach.api", target: record.url, status: record.status };
}

const NETWORKED = {
  fetch: crawlFetch,
  site: crawlSite,
  "reddit-listing": (p, h, e) => reddit(p, h, e, "listing"),
  "reddit-comments": (p, h, e) => reddit(p, h, e, "comments"),
  "x-oembed": xOembed,
  "x-api": xApi,
  api: officialApi,
};

/**
 * Run a reach command. Options: env, fetchImpl, sleep, now, receiptFile,
 * memoryFile. Files are written only when the caller names them.
 */
export async function runReach(command, params = {}, deps = {}) {
  const env = deps.env ?? process.env;
  const memoryFile = deps.memoryFile ?? env.TELOS_REACH_MEMORY ?? null;
  if (command === "doctor") return reachDoctor(env);
  if (command === "menu") return reachMenu({ tier: params.tier ?? "T1", env, memory: readMemory(params.memory ?? memoryFile) });
  const handler = NETWORKED[command];
  if (!handler) throw new Error(`unknown reach command ${command}; known: ${COMMANDS.join(", ")}`);
  const http = makeHttp({ ...deps, env });
  const out = await handler(params, http, env);
  const receipt = reachReceipt({ tool: out.verb, records: out.records, cost: out.cost ?? null, env });
  const written = writeReceipt(receipt, deps.receiptFile ?? env.TELOS_REACH_RECEIPTS ?? null);
  const last = out.records.at(-1);
  remember(memoryFile, { verb: out.verb, target: String(out.target ?? ""), status: out.status, bytes_sha256: last?.bytes_sha256 ?? null });
  return { result: out.result, receipt, receipt_file: written };
}
