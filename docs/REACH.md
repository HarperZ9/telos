# Telos reach: read the web, Reddit and X from an agent

Telos reach gives an agent one way to read public web pages, feeds, Reddit, X posts and a set of official APIs. It is our own code on Node built-ins, with no dependency, no paid service and no scraping relay. Every read returns a receipt that records the URL, the time, the status, the robots.txt decision and a SHA-256 hash of the bytes.

## Start here

```bash
npx project-telos-mcp            # or: node demo/telos-mcp.mjs
telos reach doctor               # which channels work for you right now
telos reach fetch https://example.com/
telos reach site https://simonwillison.net/ --depth 1 --budget 5
telos reach x oembed https://x.com/XDevelopers/status/1861111969639481848
telos reach api hackernews top limit=10
```

The doctor reads environment variable names and nothing else. It makes no network call, writes no file and starts no process.

## Channels and what each one covers

| Channel | How Telos reaches it | You need | Cost | Covers | Leaves out |
|:--|:--|:--|:--|:--|:--|
| Web | Crawler that reads robots.txt first | nothing | free | public pages, RSS, Atom, sitemaps, JSON endpoints | pages robots.txt disallows, logins, bot checks |
| Reddit | Official Data API over OAuth | your own Reddit app | free for personal, non-commercial use | subreddit listings, posts, comment trees | anything without an approved app; commercial use needs a Reddit agreement |
| X single posts | X's public oEmbed endpoint | nothing | free | text, author and date of one public post | search, timelines, replies, metrics, media |
| X API | Official X API v2 | your own bearer token | X bills per read | post lookup, recent search, a user's recent posts | anything your plan does not cover |
| X pages you open | Browser read verbs under a T1 grant | a browser you signed into | free | the page you have open | background or bulk reading |
| Hacker News | Official Firebase API | nothing | free | stories, items, users | search |
| GitHub | Official REST API | optional `GITHUB_TOKEN` | free | repositories, issues, repository search | private repositories without a token |
| V2EX | Documented public API | nothing | free | hot and latest topics | replies |
| Wikipedia | Wikimedia REST API | nothing | free | page summaries | article history |
| arXiv | arXiv export API, one call per 3 seconds | nothing | free | paper search with abstracts | PDF bodies (use the web channel) |
| YouTube | YouTube Data API v3 | `YOUTUBE_API_KEY` | free daily quota | video search and metadata | captions and downloads |
| Web search | Brave Search API | `BRAVE_SEARCH_API_KEY` | free allowance, then paid | search results | past your plan |

Prices and terms were checked on 2026-10-03. Platforms change them; the doctor shows the cost line it knows.

## How the crawler stays welcome

- It fetches `robots.txt` once per site and obeys `Disallow`, `Allow` and `Crawl-delay` as RFC 9309 describes. A missing file means no limits. A server error or an unreachable host means Telos reads nothing from that site.
- Each redirect hop gets the same robots.txt check.
- It sends one User-Agent, `Telos/<version> (+https://github.com/HarperZ9/telos; reach crawler)`. Set `TELOS_REACH_CONTACT` to add your email or URL so site owners can reach you.
- It waits at least one second between requests to the same host, longer when the site asks. On a 429 or 503 it waits for `Retry-After` or doubles its wait, and gives up after two retries.
- It reads sitemaps and feeds before it follows links, honours `rel=nofollow` and the robots meta tag, stays on the start host, and stops at the depth (up to 3) and page budget (up to 50) you set.
- When a site answers with a bot check, Telos records that and stops. It never tries to pass one.
- Responses are cached in memory, and conditional requests use `ETag` and `Last-Modified`. Set `TELOS_REACH_CACHE_DIR` to keep the cache on disk.

## Why your accounts stay in good standing

Telos stays inside each site's published rules and rate limits. That is the whole method. It does not log in for you, copy cookies out of your browser, rotate identities or proxies, pretend to be a browser, or call any platform's private endpoints. Reddit and X are read only through their official APIs with credentials you created, at the pace those APIs publish. A site can still block any client at its discretion; Telos makes that unlikely by behaving the way the site asked.

## Reddit setup

1. Create an app at https://www.reddit.com/prefs/apps (type "script" for personal use). Reddit now asks developers to register and may require approval before an app can call the API.
2. Export the app's credentials:

   ```bash
   export REDDIT_CLIENT_ID=...
   export REDDIT_CLIENT_SECRET=...
   export REDDIT_USERNAME=your_name        # optional, used in the User-Agent
   ```

3. Read:

   ```bash
   telos reach reddit listing rust --sort top --time week --limit 25
   telos reach reddit comments 1abcde --depth 4
   ```

Telos uses the application-only OAuth grant, sends the User-Agent form Reddit asks for (`node:telos-reach.<app id>:<version> (by /u/<name>)`), and waits when Reddit's `X-Ratelimit-Remaining` header reaches zero. Reddit's published limit is 100 queries a minute per app. Telos only reads; it never posts, votes or messages.

## X: what you can read and what you cannot

- **One public post, free:** `telos reach x oembed <post URL>` uses X's public oEmbed endpoint.
- **The official API, paid:** set `X_BEARER_TOKEN` from your X developer app, then `telos reach x post <id>`, `telos reach x search "<query>"` or `telos reach x user <name>`. X moved to pay-per-use billing in 2026 and closed its free tier to new developers. Each receipt carries a cost estimate (`X_API_COST_PER_READ_USD` overrides the default of $0.005 a read). Your X developer console is the bill of record.
- **A page you open yourself:** open the page in the Telos browser, signed in as you, and read it with the native-control verbs `browser.gettext` or `browser.snapshot-text` under a T1 grant. You are present; Telos reads what you see.

What this leaves out: free bulk search, timelines, follower graphs and reply trees. X offers no free permitted route to them, and reading X in bulk without permission breaks X's terms. Tools that do it rely on copied session cookies, rotated accounts or private endpoints, and those are the methods that get accounts suspended. Telos does not ship them.

## Receipts, memory and the trace line

Every networked command returns a `telos.reach-receipt/v1` object:

- `fetches`: one record per request with URL, time, status, robots.txt decision, cache state, byte count and SHA-256 hash. Keys and tokens travel in headers and never appear in a record.
- `cost`: the estimate for paid APIs.
- `trace`: which model provider saw this session's trace. Telos takes it from `TELOS_TRACE_PROVIDER` when you set it, otherwise from the MCP client name, otherwise it says `unknown`. Telos does not check provider retention terms and says so.

Pass `--receipt FILE` (or set `TELOS_REACH_RECEIPTS`) to append receipts as JSON lines. Pass `--memory FILE` (or set `TELOS_REACH_MEMORY`) to record what was read; `telos reach menu --tier T1 --memory FILE` then lists the verbs your grant tier allows, which ones lack credentials, and what you already read. Without these flags nothing is written.

## MCP tools

| Tool | What it does |
|:--|:--|
| `telos.reach.doctor` | Channel status with no side effects |
| `telos.reach.menu` | Verbs your tier allows, with memory |
| `telos.crawl.fetch` | One URL through robots.txt and the crawler |
| `telos.crawl.site` | A small site within depth and page budget |
| `telos.reddit.listing` | Subreddit posts through the official API |
| `telos.reddit.comments` | One post and its comments |
| `telos.x.oembed` | One public X post |
| `telos.x.api` | Official X API reads with your token |
| `telos.reach.api` | One operation on an official API channel |

The network tools carry `openWorldHint: true`. All of them are read-only.

## What this does not prove

A green doctor row means the credentials are present. Only a real call shows whether the platform accepts them. The live smoke tests (`TELOS_REACH_LIVE=1 npm test`) call the keyless endpoints once each; Reddit, the X API, YouTube and Brave have no keyless endpoint, so their tests run against a recorded fake network.
