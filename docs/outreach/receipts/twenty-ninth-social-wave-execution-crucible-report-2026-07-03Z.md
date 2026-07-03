# crucible report: Twenty-ninth social wave execution receipts

## Summary

- thesis_id: `bd67c2812415d6d8`
- thesis_seal: `bd67c2812415d6d8db9e7dfa93290752ba7fbd74d9e76fe47813e2232eac0f82`
- assessment_seal: `0d40bb8cc580cff544502f0b14b5fc8f30a6f5ad066258f5771618844f9007d2`
- counts: MATCH 5 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The executed outreach continuation attempted 9 non-GitHub public targets and posted 6 public items. | MATCH | publishable | 1 | execution-receipt-count-scan | deviation 0 within tolerance 0.1 |
| The executed dev.to outreach posted B63, B65, B67, and B69 as the authenticated @harperz9 account, with no external links included in those comments. | MATCH | publishable | 1 | devto-receipt-scan | deviation 0 within tolerance 0.1 |
| The owned-channel outreach posted OWN01-X on X and OWN01-MASTODON on Mastodon, each with the Project Telos repository link included. | MATCH | publishable | 1 | owned-channel-receipt-scan | deviation 0 within tolerance 0.1 |
| The execution recorded Hacker News B59 and B61 as authenticated but not writable, without forcing a comment onto closed item pages. | MATCH | publishable | 1 | hn-auth-gate-receipt-scan | deviation 0 within tolerance 0.1 |
| The execution recorded Bluesky as authenticated but composer-gated, and did not claim a Bluesky post without a writable editor. | MATCH | publishable | 1 | bluesky-gate-receipt-scan | deviation 0 within tolerance 0.1 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The executed outreach continuation attempted 9 non-GitHub public targets and posted 6 public items. | execution-receipt-count-scan | docs/outreach/receipts/twenty-ninth-social-wave-execution-receipts-2026-07-03Z.md |
| The executed dev.to outreach posted B63, B65, B67, and B69 as the authenticated @harperz9 account, with no external links included in those comments. | devto-receipt-scan | dev.to page verification snippets from Chrome execution; docs/outreach/receipts/twenty-ninth-social-wave-execution-receipts-2026-07-03Z.md |
| The owned-channel outreach posted OWN01-X on X and OWN01-MASTODON on Mastodon, each with the Project Telos repository link included. | owned-channel-receipt-scan | X profile verification snippet from Chrome execution; Mastodon profile verification snippet from Chrome execution; docs/outreach/receipts/twenty-ninth-social-wave-execution-receipts-2026-07-03Z.md |
| The execution recorded Hacker News B59 and B61 as authenticated but not writable, without forcing a comment onto closed item pages. | hn-auth-gate-receipt-scan | Hacker News item-page form checks from Chrome execution; docs/outreach/receipts/twenty-ninth-social-wave-execution-receipts-2026-07-03Z.md |
| The execution recorded Bluesky as authenticated but composer-gated, and did not claim a Bluesky post without a writable editor. | bluesky-gate-receipt-scan | Bluesky composer checks from Chrome execution; docs/outreach/receipts/twenty-ninth-social-wave-execution-receipts-2026-07-03Z.md |
