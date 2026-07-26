# Thirty-Sixth Social Auth Surface Inventory Gather Report - 2026-07-03Z

## Gather Docs

| Field | Value |
| --- | --- |
| Path | `C:\dev\public\telos\docs\outreach\receipts\thirty-sixth-social-auth-surface-inventory-2026-07-03Z.md` |
| Verified | true |
| Catalog rows | 1 |
| Dropped | 0 |
| Receipt SHA-256 | `8c0c0e5ac974e627a86629d05a4806634d9a9040b0dcd88077521ba440d034c5` |
| Gather docs seal | `c614a477439624cc1ecf30e65e7865afc857340410eac42088cbe95317b04cb1` |

## Federation Registry

| Field | Value |
| --- | --- |
| Verified | true |
| Source rows | 12 |
| Federation seal | `40ca80b551e56b52005aac1e090c712b95a7f0e1f2ba3e9d30453a46693d60d7` |

## Source Rows

| ID | System | Domain | Adapter | Scope | Access | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| `reddit-old` | old Reddit | `old.reddit.com` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `high` |
| `reddit-new` | Reddit | `reddit.com` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `medium` |
| `youtube` | YouTube | `youtube.com` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `medium` |
| `hacker-news` | Hacker News | `news.ycombinator.com` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `high` |
| `devto` | dev.to | `dev.to` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `medium` |
| `linkedin` | LinkedIn | `linkedin.com` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `high` |
| `x` | X | `x.com` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `high` |
| `bluesky` | Bluesky | `bsky.app` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `high` |
| `mastodon` | Mastodon | `mastodon.social` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `high` |
| `substack` | Substack | `substack.com` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `medium` |
| `medium` | Medium | `medium.com` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `high` |
| `hashnode` | Hashnode | `hashnode.com` | `browser-chrome` | `outreach-auth-inventory` | `account_required` | `low` |

## Schema Corrections

The first two registry attempts failed because rows were missing Gather-required fields and used underscore IDs. The final validated shape requires stable lowercase hyphenated IDs plus `system`, `family`, `domain`, `adapter`, and a string `scope`.
