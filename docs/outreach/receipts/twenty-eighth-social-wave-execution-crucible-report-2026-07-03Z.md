# crucible report: Twenty-eighth social wave execution receipts

## Summary

- thesis_id: `eab81af9d28cba6e`
- thesis_seal: `eab81af9d28cba6ed2e8851169a20c3603ed59ca04742dd3fdf9627189a43db8`
- assessment_seal: `e226b05b2cd9d72722b0de7543f86ef8a265eba3e52cb59fa65c5c4935b7a78c`
- counts: MATCH 5 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The executed outreach wave posted 14 public items: 5 Reddit comments, 8 YouTube comments, and 1 LinkedIn owned-channel update. | MATCH | publishable | 1 | execution-receipt-count-scan | deviation 0 within tolerance 0.1 |
| The executed Reddit outreach posted R97, R93, R95, R101, and R103, and skipped R99 because the target appeared locked or not writable. | MATCH | publishable | 1 | reddit-receipt-scan | deviation 0 within tolerance 0.1 |
| The executed YouTube outreach posted all eight YouTube drafts as the authenticated @Unorthodoxis account and included no external links in those comments. | MATCH | publishable | 1 | youtube-receipt-scan | deviation 0 within tolerance 0.1 |
| The executed owned-channel outreach posted LI01 on LinkedIn as Zain Harper with a public View post URL. | MATCH | publishable | 1 | linkedin-receipt-scan | deviation 0 within tolerance 0.1 |
| Unauthenticated or non-writable platforms were not forced; HN, dev.to, X, Medium, Bluesky, Mastodon, and Substack were recorded as handoff or skipped states. | MATCH | publishable | 1 | auth-matrix-and-handoff-scan | deviation 0 within tolerance 0.1 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The executed outreach wave posted 14 public items: 5 Reddit comments, 8 YouTube comments, and 1 LinkedIn owned-channel update. | execution-receipt-count-scan | docs/outreach/receipts/twenty-eighth-social-wave-execution-receipts-2026-07-03Z.md |
| The executed Reddit outreach posted R97, R93, R95, R101, and R103, and skipped R99 because the target appeared locked or not writable. | reddit-receipt-scan | old Reddit public permalinks in execution receipt; docs/outreach/receipts/twenty-eighth-social-wave-execution-receipts-2026-07-03Z.md |
| The executed YouTube outreach posted all eight YouTube drafts as the authenticated @Unorthodoxis account and included no external links in those comments. | youtube-receipt-scan | YouTube page verification snippets from Chrome execution; docs/outreach/receipts/twenty-eighth-social-wave-execution-receipts-2026-07-03Z.md |
| The executed owned-channel outreach posted LI01 on LinkedIn as Zain Harper with a public View post URL. | linkedin-receipt-scan | LinkedIn Post successful state and View post URL; docs/outreach/receipts/twenty-eighth-social-wave-execution-receipts-2026-07-03Z.md |
| Unauthenticated or non-writable platforms were not forced; HN, dev.to, X, Medium, Bluesky, Mastodon, and Substack were recorded as handoff or skipped states. | auth-matrix-and-handoff-scan | Chrome auth matrix; docs/outreach/receipts/twenty-eighth-social-wave-execution-receipts-2026-07-03Z.md |
