// Tier-limited action menus with memory. The menu lists only the reach verbs
// the caller's grant tier allows and whose credentials are present, plus the
// browser read verbs for pages the user has open. Memory is an append-only
// JSON-lines file the user names; the menu shows what was already read so an
// agent does not fetch the same thing twice.
import { existsSync, readFileSync, appendFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { TIERS, VERBS, tierRank } from "../broker/tiers.mjs";
import { CHANNELS } from "./channels.mjs";
import { channelStatus } from "./doctor.mjs";

export const MENU_SCHEMA = "telos.reach-menu/v1";
export const MEMORY_SCHEMA = "telos.reach-memory/v1";

export const REACH_VERBS = Object.freeze([
  { verb: "reach.doctor", tier: "T0", channel: null, does: "report which channels work, with no side effects" },
  { verb: "crawl.fetch", tier: "T1", channel: "web", does: "read one public URL after a robots.txt check" },
  { verb: "crawl.site", tier: "T1", channel: "web", does: "read a site within a depth and page budget, feeds and sitemaps first" },
  { verb: "reddit.listing", tier: "T1", channel: "reddit", does: "list a subreddit through the official API" },
  { verb: "reddit.comments", tier: "T1", channel: "reddit", does: "read a post and its comment tree through the official API" },
  { verb: "x.oembed", tier: "T1", channel: "x-oembed", does: "read one public X post from its URL" },
  { verb: "x.api", tier: "T1", channel: "x-api", does: "read X through the official API; billed per read" },
  { verb: "reach.api", tier: "T1", channel: null, does: "call one official API operation (hackernews, github, v2ex, wikipedia, arxiv, youtube, brave)" },
]);

/** Browser verbs that only read a page the user already has open. */
export function browserReadVerbs() {
  return Object.entries(VERBS)
    .filter(([name, spec]) => name.startsWith("browser.") && spec.sense === "page_text")
    .map(([verb, spec]) => ({ verb, tier: spec.tier, channel: "x-session", does: "read the text of a page you opened and signed into yourself" }));
}

/** Read memory entries; a missing file is an empty memory. */
export function readMemory(file) {
  if (!file || !existsSync(file)) return [];
  return readFileSync(file, "utf8")
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    })
    .filter((entry) => entry && entry.schema === MEMORY_SCHEMA);
}

/** Append one memory entry. Only called when the user named a memory file. */
export function remember(file, { verb, target, status, bytes_sha256 = null, at = new Date() }) {
  if (!file) return null;
  const resolved = path.resolve(file);
  mkdirSync(path.dirname(resolved), { recursive: true });
  const entry = { schema: MEMORY_SCHEMA, verb, target, status, bytes_sha256, at: at.toISOString() };
  appendFileSync(resolved, `${JSON.stringify(entry)}\n`);
  return entry;
}

function availability(item, env) {
  if (!item.channel) return { available: true, why: null };
  const channel = CHANNELS.find((c) => c.id === item.channel);
  const status = channelStatus(channel, env);
  if (status.status === "needs credentials") return { available: false, why: `set ${status.missing.join(", ")}` };
  return { available: true, why: null };
}

/** Build the menu for a tier. Verbs above the tier are omitted, not greyed. */
export function reachMenu({ tier = "T1", env = process.env, memory = [] } = {}) {
  if (!TIERS.includes(tier)) throw new Error(`tier must be one of ${TIERS.join(", ")}`);
  const rank = tierRank(tier);
  const items = [...REACH_VERBS, ...browserReadVerbs()].filter((item) => tierRank(item.tier) <= rank);
  const verbs = items.map((item) => {
    const recent = memory.filter((m) => m.verb === item.verb).slice(-3);
    return { ...item, ...availability(item, env), recent };
  });
  const alreadyRead = [...new Set(memory.filter((m) => m.status >= 200 && m.status < 300).map((m) => m.target))];
  return { schema: MENU_SCHEMA, tier, verbs, already_read: alreadyRead, memory_entries: memory.length };
}
