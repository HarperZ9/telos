# Telos 0.9.0

Telos 0.9.0 lets an agent read the web. Public pages, feeds, Reddit, single X posts and a set of official APIs come back as structured JSON with a receipt for every request. It is our own code on Node built-ins, with no dependency, no paid service and no scraping relay.

## Try it

```
npm install -g project-telos-mcp@0.9.0
telos reach doctor
telos reach fetch https://example.com/
telos reach x oembed https://x.com/XDevelopers/status/1861111969639481848
telos reach api hackernews top limit=5
```

Over MCP the same reads are `telos.reach.doctor`, `telos.crawl.fetch`, `telos.crawl.site`, `telos.reddit.listing`, `telos.reddit.comments`, `telos.x.oembed`, `telos.x.api`, `telos.reach.api` and `telos.reach.menu`. The full guide is `docs/REACH.md`.

## What each channel covers

| Channel | Route | You need | Covers | Leaves out |
|---|---|---|---|---|
| Web | crawler that reads robots.txt first | nothing | pages, RSS, Atom, sitemaps, JSON | disallowed pages, logins, bot checks |
| Reddit | official Data API over OAuth | your own Reddit app | listings, posts, comment trees | commercial use without a Reddit agreement |
| X single posts | public oEmbed endpoint | nothing | text, author and date of one post | search, timelines, replies, metrics |
| X API | official API v2 | your own bearer token, billed by X | lookup, recent search, a user's posts | what your plan does not cover |
| X pages you open | browser read verbs at T1 | you, signed in | the page in front of you | background or bulk reading |
| Hacker News, GitHub, V2EX, Wikipedia, arXiv | official APIs | nothing | stories, repositories, topics, summaries, papers | per-channel limits in the guide |
| YouTube, Brave Search | official APIs | your own key | video metadata, web search | captions, downloads, past your plan |

X closed its free API tier to new developers in 2026. Free bulk search and timelines on X have no permitted route, so Telos does not offer them.

## How it stays welcome

- robots.txt is read per site and obeyed on every URL and redirect hop, Crawl-delay included.
- One User-Agent names Telos and its project URL; `TELOS_REACH_CONTACT` adds yours.
- Each host gets at least one second between requests. A 429 or 503 waits for Retry-After, and Telos gives up after two retries.
- A bot check stops the read. Telos never tries to pass one.
- Reddit reads pace themselves from Reddit's rate-limit headers.
- Telos never logs in for you, copies browser cookies, rotates identities or proxies, or calls private endpoints. Staying inside each site's rules is what keeps your accounts in good standing.

## Receipts

Each read returns `telos.reach-receipt/v1`: URL, time, status, robots.txt decision, cache state and SHA-256 of the bytes per request, a cost estimate for paid APIs, and a line naming which model provider saw the session's trace. Keys travel in headers and never appear in a receipt. Nothing is written to disk unless you pass `--receipt`, `--memory` or set `TELOS_REACH_CACHE_DIR`.

## Measured

Release checks, run before this release on one Windows machine with Node 25:

- 51 behaviour tests on a fake network pass.
- 7 of 7 live smoke calls pass against the keyless endpoints (example.com, X oEmbed, Hacker News, GitHub, V2EX, Wikipedia, arXiv) on 2026-10-03. Reddit, the X API, YouTube and Brave have no keyless endpoint and were tested on the fake network only.
- `bench/reach/run-mutations.mjs` breaks 13 guarded behaviours one at a time; the tests catch 13 of 13.
- The reach doctor makes no network call, and its CLI writes no file even with cache, receipt and memory variables set.

## Limits

- A ready doctor row means the credentials are present. Only a real call shows whether a platform accepts them.
- Prices and terms were checked on 2026-10-03 and can change.
- The crawler parses HTML with its own tolerant reader. Pages that build their content in JavaScript come back thin; open those yourself and use the browser read verbs.
