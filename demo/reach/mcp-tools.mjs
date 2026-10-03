// MCP tool definitions for the reach layer. telos-mcp.mjs appends these to its
// list. They differ from the other Telos tools in one stated way: all but the
// doctor and the menu reach the network, so they carry openWorldHint true and
// say so in their descriptions.

const str = (description) => ({ type: "string", description });
const num = (description, minimum, maximum) => ({ type: "integer", description, minimum, maximum });
const schema = (properties, required = []) => ({ type: "object", properties, required, additionalProperties: false });

const NET = "Reaches the network: one honest Telos User-Agent, per-host pacing with backoff on 429 and 503, no login, no cookies.";

export const reachTools = [
  {
    name: "telos.reach.doctor",
    title: "Reach channel check",
    script: ["reach.mjs", "doctor", "--json"],
    network: false,
    description: "Use before any reach call to see which channels (web crawler, Reddit, X, official APIs) work for this user and what each one costs and leaves out. Read-only, zero-auth, no external side effects: reads environment variable names only, with no network, file writes or processes. Returns a JSON doctor report.",
    inputSchema: schema({}),
  },
  {
    name: "telos.reach.menu",
    title: "Reach action menu",
    script: ["reach.mjs", "menu", "--json"],
    network: false,
    description: "Use when an agent needs the reach verbs its grant tier allows, with credentials checked and a memory of what was already read. Read-only, zero-auth, no external side effects; reads the memory file named by `memory` or TELOS_REACH_MEMORY. Returns a JSON menu.",
    inputSchema: schema({ tier: { type: "string", enum: ["T0", "T1", "T2", "T3", "T4", "T5"] }, memory: str("path to a reach memory JSON-lines file") }),
  },
  {
    name: "telos.crawl.fetch",
    title: "Read one web page",
    script: ["reach.mjs", "fetch"],
    network: true,
    description: `Use when an agent needs the text, feed items, sitemap URLs or JSON of one public URL. Read-only and zero-auth; checks robots.txt first and stops at a bot check. ${NET} Returns JSON with the parsed page and a receipt of every fetch.`,
    inputSchema: schema({ url: str("http or https URL") }, ["url"]),
  },
  {
    name: "telos.crawl.site",
    title: "Read a small site",
    script: ["reach.mjs", "site"],
    network: true,
    description: `Use when an agent needs several pages of one site; sitemaps and feeds are read before links, inside a depth (0 to 3) and page budget (1 to 50). Read-only and zero-auth; obeys robots.txt and Crawl-delay. ${NET} Returns JSON page summaries and a receipt.`,
    inputSchema: schema({ url: str("start URL"), depth: num("link depth", 0, 3), page_budget: num("maximum pages", 1, 50), same_host: { type: "boolean" } }, ["url"]),
  },
  {
    name: "telos.reddit.listing",
    title: "Reddit subreddit listing",
    script: ["reach.mjs", "reddit-listing"],
    network: true,
    description: `Use when an agent needs posts from a subreddit through Reddit's official Data API. Read-only; auth is the user's own Reddit app credentials from environment variables named by telos.reach.doctor, paced from Reddit's rate-limit headers. ${NET} Returns JSON posts and a receipt.`,
    inputSchema: schema({ subreddit: str("name without r/"), sort: { type: "string", enum: ["hot", "new", "top", "rising", "controversial"] }, limit: num("posts", 1, 100), time: { type: "string", enum: ["hour", "day", "week", "month", "year", "all"] } }, ["subreddit"]),
  },
  {
    name: "telos.reddit.comments",
    title: "Reddit post and comments",
    script: ["reach.mjs", "reddit-comments"],
    network: true,
    description: `Use when an agent needs one Reddit post and its comment tree through the official Data API. Read-only; auth is the user's own Reddit app credentials from environment variables named by telos.reach.doctor. ${NET} Returns JSON comments with depth and a receipt.`,
    inputSchema: schema({ post_id: str("post id, with or without t3_"), depth: num("comment depth", 1, 10), limit: num("comments", 1, 500) }, ["post_id"]),
  },
  {
    name: "telos.x.oembed",
    title: "Read one X post",
    script: ["reach.mjs", "x-oembed"],
    network: true,
    description: `Use when an agent needs the text, author and date of one public X post from its URL, through X's public oEmbed endpoint. Read-only and zero-auth; no search or timelines. ${NET} Returns JSON and a receipt.`,
    inputSchema: schema({ url: str("https://x.com/<user>/status/<id>") }, ["url"]),
  },
  {
    name: "telos.x.api",
    title: "X official API read",
    script: ["reach.mjs", "x-api"],
    network: true,
    description: `Use when the user has an X developer key and wants a post lookup, recent search or a user's recent posts through the official X API v2. Read-only; auth is X_BEARER_TOKEN, and X bills each read, so the receipt carries a cost estimate. ${NET} Returns JSON and a receipt.`,
    inputSchema: schema({ op: { type: "string", enum: ["post", "search_recent", "user_posts"] }, id: str("post id"), query: str("search query"), username: str("X username"), max: num("results", 5, 100) }, ["op"]),
  },
  {
    name: "telos.reach.api",
    title: "Official API read",
    script: ["reach.mjs", "api"],
    network: true,
    description: `Use when an agent needs one operation from an official API: hackernews, github, v2ex, wikipedia, arxiv (zero-auth), or youtube and brave (auth is the user's own key in YOUTUBE_API_KEY or BRAVE_SEARCH_API_KEY). Read-only; keys travel in headers and never in receipts. ${NET} Returns JSON and a receipt.`,
    inputSchema: schema({ channel: { type: "string", enum: ["hackernews", "github", "v2ex", "wikipedia", "arxiv", "youtube", "brave"] }, op: str("operation, for example top, item, repo, search"), params: { type: "object", description: "operation parameters, for example {\"q\": \"robots.txt\"}" } }, ["channel", "op"]),
  },
];

export const reachToolNames = new Set(reachTools.map((tool) => tool.name));
export const networkToolNames = new Set(reachTools.filter((tool) => tool.network).map((tool) => tool.name));
