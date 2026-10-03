// The channel register the reach doctor reports from. Each row says how Telos
// reaches the source, what credentials it needs (by variable name only), what
// it costs, what it covers and what it leaves out. Prices and terms are as
// checked on the date in CHECKED_ON; a platform can change them at any time.

export const CHECKED_ON = "2026-10-03";

const row = (id, fields) => Object.freeze({ id, env: [], optionalEnv: [], ...fields });

export const CHANNELS = Object.freeze([
  row("web", {
    name: "Any public web page", route: "crawler: robots.txt, Crawl-delay, honest User-Agent", tool: "telos.crawl.fetch, telos.crawl.site", cost: "free",
    covers: "public pages, RSS and Atom feeds, sitemaps, documented JSON endpoints",
    leaves_out: "pages robots.txt disallows, pages behind a login or a bot check",
  }),
  row("reddit", {
    name: "Reddit", route: "official Data API over OAuth with your own app", tool: "telos.reddit.listing, telos.reddit.comments",
    env: ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"], optionalEnv: ["REDDIT_USERNAME", "REDDIT_USER_AGENT"],
    cost: "free for personal, non-commercial use within 100 queries a minute per app; commercial use needs an agreement with Reddit",
    covers: "subreddit listings (hot, new, top, rising, controversial), posts, comment trees to depth 10",
    leaves_out: "anything without your own approved Reddit app; bulk archives; private or quarantined communities",
  }),
  row("x-oembed", {
    name: "X single posts", route: "X's public oEmbed endpoint", tool: "telos.x.oembed", cost: "free, no key",
    covers: "text, author and date of one public post per URL",
    leaves_out: "search, timelines, replies, metrics, media, deleted or protected posts",
  }),
  row("x-api", {
    name: "X API", route: "official X API v2 with your own bearer token", tool: "telos.x.api", env: ["X_BEARER_TOKEN"], optionalEnv: ["X_API_COST_PER_READ_USD"],
    cost: "paid: X bills per read (about $0.005 a post as reported in 2026); each receipt shows an estimate",
    covers: "post lookup, recent search, a user's recent posts, within your plan",
    leaves_out: "anything your plan or credit balance does not cover",
  }),
  row("x-session", {
    name: "X pages you open yourself", route: "native-control browser read verbs under a T1 grant, in a browser you signed into", tool: "telos native-control browser.gettext and browser.snapshot-text",
    cost: "free", covers: "the page you have open, as you see it",
    leaves_out: "background or bulk reading; Telos never signs in for you or copies your cookies",
  }),
  row("hackernews", { name: "Hacker News", route: "official Firebase API", tool: "telos.reach.api hackernews", cost: "free, no key", covers: "top stories, items, comments, users", leaves_out: "search (use the web channel on a search page you are allowed to read)" }),
  row("github", { name: "GitHub", route: "official REST API", tool: "telos.reach.api github", optionalEnv: ["GITHUB_TOKEN"], cost: "free; a token raises the hourly limit", covers: "repositories, issues, repository search", leaves_out: "private repositories without a token that can see them" }),
  row("v2ex", { name: "V2EX", route: "documented public API", tool: "telos.reach.api v2ex", cost: "free, no key", covers: "hot and latest topics", leaves_out: "replies and member pages" }),
  row("wikipedia", { name: "Wikipedia", route: "Wikimedia REST API", tool: "telos.reach.api wikipedia", cost: "free, no key", covers: "page summaries", leaves_out: "full article history" }),
  row("arxiv", { name: "arXiv", route: "arXiv export API, paced to one call per 3 seconds", tool: "telos.reach.api arxiv", cost: "free, no key", covers: "paper search with abstracts", leaves_out: "PDF bodies (fetch them with the web channel)" }),
  row("youtube", { name: "YouTube metadata", route: "YouTube Data API v3 with your own key", tool: "telos.reach.api youtube", env: ["YOUTUBE_API_KEY"], cost: "free daily quota from Google", covers: "video search and video metadata", leaves_out: "captions and media downloads" }),
  row("brave", { name: "Web search", route: "Brave Search API with your own key", tool: "telos.reach.api brave", env: ["BRAVE_SEARCH_API_KEY"], cost: "free monthly allowance, then paid", covers: "web search results", leaves_out: "anything past your plan" }),
]);

/** Sources Telos has no permitted route to, stated so nobody has to guess. */
export const NO_ROUTE = Object.freeze([
  { name: "X bulk search and timelines without a paid key", reason: "X offers no free API tier for new developers; reading X pages in bulk without permission breaks X's terms" },
  { name: "LinkedIn, Facebook and Instagram public content", reason: "partner or researcher programmes only; open the page yourself and use the x-session style browser read" },
  { name: "Sites that answer with a bot check", reason: "Telos stops at a bot check and never tries to pass one" },
]);
