# Fifth-Wave OSS Proof Showcase Demo

Date: 2026-07-02

Purpose: turn the current Telos proof-packet discipline toward public growth. The demo shows a fixture-first OSS lane that can rank a public bug candidate, produce a PR-readiness packet when evidence is complete, and block the packet when evidence is missing. This is a package-shape demo, not a claim that Project Telos fixed pandas.

## Verified Results

| Segment | Evidence | Boundary |
| --- | --- | --- |
| Fixture scout | `node demo\showcase.mjs scout --fixture --json --now 2026-07-02T00:00:00Z --out docs\outreach\receipts\fifth-wave\oss-showcase-scout` wrote `scout.json` with schema `project-telos.oss-scout/v1`, candidate `pandas-dev/pandas#66050`, and priority `70`. | Offline deterministic fixture. Does not prove current GitHub state or current pandas issue metadata. |
| Ready fixture packet | `node demo\showcase.mjs record --candidate demo\showcase\fixtures\pandas-66050.json --evidence docs\outreach\receipts\fifth-wave\oss-showcase-fixture-ready-evidence.json --now 2026-07-02T00:00:00Z --json` wrote `oss-showcase-fixture-ready-packet.json` with schema `project-telos.oss-pr-readiness/v1`, `pr_ready: true`, `operator_next_action: open-pr`, and verdict `MATCH`. | Synthetic fixture evidence only. Do not post this as an actual upstream patch or maintainer-ready PR. |
| Blocked fixture packet | The same record command with `oss-showcase-fixture-blocked-evidence.json` wrote `oss-showcase-fixture-blocked-packet.json` with `pr_ready: false`, `operator_next_action: revise`, verdict `UNVERIFIABLE`, and blockers `missing passing test evidence`, `crucible verdict is not MATCH`, and `missing patch summary`. | Negative fixture. It proves the readiness packet can block incomplete evidence; it does not prove every bad OSS packet is caught. |
| Unit coverage | `node --test demo\showcase.test.mjs` passed. | Unit scope only. It covers fixture scout, live-scout failure handling, scoring, path hygiene, and record packet readiness logic. |

## Artifact Map

| Artifact | Role |
| --- | --- |
| `docs/outreach/receipts/fifth-wave/oss-showcase-scout/scout.json` | Generated fixture scout output. |
| `docs/outreach/receipts/fifth-wave/oss-showcase-fixture-ready-evidence.json` | Fixture-only evidence with reproduction, patch summary, passing test, `MATCH` verdict, and not-verified scope. |
| `docs/outreach/receipts/fifth-wave/oss-showcase-fixture-ready-packet.json` | Generated PR-readiness packet from the ready fixture. |
| `docs/outreach/receipts/fifth-wave/oss-showcase-fixture-blocked-evidence.json` | Negative fixture with missing patch/test/MATCH evidence. |
| `docs/outreach/receipts/fifth-wave/oss-showcase-fixture-blocked-packet.json` | Generated blocked PR-readiness packet from the negative fixture. |
| `docs/outreach/receipts/fifth-wave-tooling-thesis-2026-07-02.json` | Crucible thesis for this pass. |
| `docs/outreach/receipts/fifth-wave-tooling-measurements-2026-07-02.json` | Measurement rows for the thesis. |

## Re-run Commands

From `C:\dev\public\telos`:

```powershell
node demo\showcase.mjs scout --fixture --json --now 2026-07-02T00:00:00Z --out docs\outreach\receipts\fifth-wave\oss-showcase-scout

node demo\showcase.mjs record --candidate demo\showcase\fixtures\pandas-66050.json --evidence docs\outreach\receipts\fifth-wave\oss-showcase-fixture-ready-evidence.json --now 2026-07-02T00:00:00Z --json

node demo\showcase.mjs record --candidate demo\showcase\fixtures\pandas-66050.json --evidence docs\outreach\receipts\fifth-wave\oss-showcase-fixture-blocked-evidence.json --now 2026-07-02T00:00:00Z --json

node --test demo\showcase.test.mjs
```

Crucible package check:

```powershell
crucible run docs\outreach\receipts\fifth-wave-tooling-thesis-2026-07-02.json --measurements docs\outreach\receipts\fifth-wave-tooling-measurements-2026-07-02.json --out docs\outreach\receipts\fifth-wave-tooling-run-2026-07-02.json --report docs\outreach\receipts\fifth-wave-tooling-report-2026-07-02.md --json
```

## Public Post Angle

> A useful proof system should not only verify private demos. It should help find small public work, rank it, package the evidence, and block the handoff when a patch lacks reproduction, tests, or a verifier verdict. This fifth-wave Telos fixture shows that shape without pretending a fixture is an upstream PR.

## Do Not Post

- Do not claim Project Telos fixed `pandas-dev/pandas#66050`.
- Do not claim the fixture reflects current GitHub issue state.
- Do not claim live GitHub scouting ran unless a fresh live-scout receipt exists.
- Do not claim a packet is PR-ready unless reproduction, patch summary, passing tests, and a `MATCH` verifier verdict are all present.
