<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/art/hero-dark.svg">
  <img src="docs/art/hero-light.svg" alt="telos: One workbench, and packets that recompute their own claims. An eye drawn in nested fine contours, its iris a ring of short radial lines around a dark pupil with a glowing rim. Five small rings sit on the eye's edge; one is dashed and marked UNVERIFIABLE." width="100%">
</picture>

# telos

Telos is a local MCP server and command line for AI agents. It lets an agent read web pages and public APIs, triage a failed GitHub Actions run, check an HTML page for accessibility and size problems, and drive a browser or Windows app once you grant permission from your own terminal.

```bash
npx -y project-telos-mcp
```

[![version: 0.9.0](https://img.shields.io/badge/version-0.9.0-e6e1d6?style=flat-square&labelColor=1a1712)](https://www.npmjs.com/package/project-telos-mcp)
[![CI](https://github.com/HarperZ9/telos/actions/workflows/ci.yml/badge.svg)](https://github.com/HarperZ9/telos/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-FSL--1.1--MIT-e6e1d6?style=flat-square&labelColor=1a1712)](LICENSE)
![node 20+](https://img.shields.io/badge/node-20%2B-e6e1d6?style=flat-square&labelColor=1a1712)

[Project Telos](https://harperz9.github.io) | [gather](https://github.com/HarperZ9/gather) | [crucible](https://github.com/HarperZ9/crucible) | [index](https://github.com/HarperZ9/index) | [forum](https://github.com/HarperZ9/forum) | [telos](https://github.com/HarperZ9/telos) | [learn](https://github.com/HarperZ9/learn) | [emet](https://github.com/HarperZ9/emet) | [buildlang](https://github.com/HarperZ9/buildlang)

It is plain Node.js 20+ with no npm dependencies. The npm package is `project-telos-mcp`. It serves 50 tools over stdio to any MCP host, such as Claude Code, Codex or the OpenAI Agents SDK.

## What it does

- **Reads the web and public APIs.** `telos reach` and nine MCP tools read pages, feeds and sitemaps, and they follow robots.txt and Crawl-delay. They read Reddit through its official API with your own app, single X posts through X's oEmbed endpoint, and APIs such as Hacker News, GitHub, arXiv and Wikipedia. Each fetch is logged with its URL, time, status and a SHA-256 of the bytes. The crawler reads HTML as served and does not run page JavaScript, so pages behind a login or a bot check come back empty. See [the reach guide](docs/REACH.md).
- **Controls a browser or Windows app after you grant it.** The CLI drives Chrome through the DevTools Protocol and Windows apps through UI Automation. Each verb has a risk tier. Nothing runs until you issue a grant with `telos grant issue`, which needs an interactive terminal, so an agent's own shell cannot grant itself access. Consequential actions also ask for a confirmation each time. Password, OTP and card fields are always refused. App control is Windows only. The MCP tool for this lists the verbs and runs none of them. See [the tier spec](docs/spec/telos-tiers.md) and [the control contract](docs/native-control-contract.md).
- **Logs every gated action.** Gated actions and refusals append to a hash-chained log. After `telos keys init` the chain heads are signed with a local ed25519 key, and `telos receipts verify <session.jsonl>` finds edited, reordered, inserted or deleted entries.
- **Triages CI.** `ci-triage --gh-run owner/repo#run_id` reads a GitHub Actions run through the `gh` CLI and says whether it failed on a blocking step or only on warnings, such as a deprecated action runtime. It names the failing step type. It does not diagnose the test.
- **Checks HTML pages.** `accessibility-doctor --html FILE` runs 14 static checks, including language, viewport, skip link, landmarks, focus style, reduced motion and labels. `performance-doctor --html FILE` runs 14 byte-budget checks. Neither opens a browser.
- **Writes packets you can verify later.** `proof.mjs` writes a JSON packet for an agent action, a research claim, a colour measurement or a build invariant, with the inputs embedded. `proof.mjs verify` recomputes the hashes and values and prints MATCH, DRIFT (something changed) or UNVERIFIABLE (an input is missing). Packets are hash-checked and unsigned.

The repo also holds work in progress. The model foundry and learning forge are written contracts and call no model. The causal, embodied and quantum packets are small fixed demos. The creative engine is a set of deterministic image kernels behind [`demo/index.html`](demo/index.html). The presentation and operator doctors are tuned to the Project Telos repositories.

## Try it

In an MCP host config, set `"command": "npx"` with `"args": ["-y", "project-telos-mcp"]`. A `tools/list` call against 0.9.0 returns 50 tools.

For the command line, install the package globally. That puts `telos` and `telos-mcp` on your PATH. Run `telos` from the install, not through npx, because the npm name `telos` belongs to an unrelated package.

```bash
npm install -g project-telos-mcp
telos reach doctor
# reach doctor  7/12 channels ready
# web         ready               free
# reddit      needs credentials   set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
# ...

telos reach fetch https://example.com
# {"result": {"url": "https://example.com/", "status": 200, "page": {"title": "Example Domain", ...}},
#  "receipt": {"fetches": [{"url": "https://example.com/robots.txt", "robots": "robots.txt 404: no restrictions", ...

telos ci-triage --gh-run owner/repo#run_id --summary
# blocking     1
# verdict      DRIFT

telos accessibility-doctor --html page.html --summary
# checks       14
# passed       10
```

Without a grant, a control verb is refused before it runs:

```bash
telos native-control browser navigate https://example.com
# "status": "REFUSED", "tier": "T3", "executed": false, "reason": "NO_GRANT"
```

To run the demos from source:

```bash
git clone https://github.com/HarperZ9/telos.git
cd telos
node demo/run.mjs
#   RUN A (honest render)  : CERTIFIED      recheck=true
#   RUN B (broken render)  : UNVERIFIABLE   recheck=true
```

From a checkout, `npm start` (the same as `node demo/telos-mcp.mjs`) runs the stdio MCP server.

`demo/run.mjs` renders a 4-D cube, recovers its vertex and edge counts from the image, and checks them against the known shape. The second render is too small to read, so it comes back UNVERIFIABLE.

The outputs above come from `project-telos-mcp` 0.9.0 installed from npm, run on Node 25 on Windows.

## How it compares

- **Playwright MCP and Chrome DevTools MCP** cover far more browser verbs. Telos covers fewer, and adds Windows app control, a grant you issue from your own terminal, and a log of each action.
- **Firecrawl and Jina Reader** render JavaScript and run as hosted services. `telos reach` runs on your machine, reads HTML as served, and follows robots.txt.
- **Lighthouse and axe-core** load the page in a real browser and run far more rules. The Telos doctors are quick static checks on the HTML file.
- **in-toto and Sigstore** sign supply-chain attestations with managed keys and public logs. The Telos action log uses one local key, and its packets are hash-checked without a signature.

## Running all five Project Telos servers

`node demo/server-manifest.mjs` prints host config (Codex TOML, Claude JSON, OpenAI Agents) that launches Telos beside [gather](https://github.com/HarperZ9/gather), [index](https://github.com/HarperZ9/index), [forum](https://github.com/HarperZ9/forum) and [crucible](https://github.com/HarperZ9/crucible), for 78 tools in all plus 38 auxiliary compatibility tools. That setup expects all five repositories checked out side by side, with `PROJECT_TELOS_PUBLIC` set to their parent folder. The orientation commands:

```bash
node demo/catalog.mjs --summary          # 78 tools across the five servers
node demo/server-manifest.mjs --summary  # launch map with host config
```

Expected catalog summary:

```
Project Telos MCP Catalog
tools    78 total, 78 available
transport stdio, streamable-http
gather    5 tools ...
index     5 tools ...
forum     5 tools ...
crucible  13 tools ...
telos     50 tools ...
```

Health and state:

```bash
node demo/status.mjs --summary
node demo/doctor.mjs --summary
node demo/room.mjs --json
```

Each command prints JSON with a MATCH, DRIFT or UNVERIFIABLE status. The package's `telos` and `telos-mcp` commands route to the same scripts.

## See it work

The [animated explainer](https://harperz9.github.io/repo-explainers/telos.html) steps through the cube demo, a proof packet verified from its own contents, and four edits that each come back DRIFT with the failing check named. Its source is [docs/explainer/index.html](docs/explainer/index.html).

[![A passing check can still be wrong: a narrated film, 2 min 24 s](https://harperz9.github.io/media/explainers/passing-check/poster.jpg)](https://harperz9.github.io/explainers.html#passing-check-h)

**[A passing check can still be wrong](https://harperz9.github.io/explainers.html#passing-check-h)** is a 2 min 24 s narrated, captioned film about the same loop. The film page has the transcript and sources.

## Proof packets

<p align="center"><img src="docs/art/proof-lane.svg" alt="Eight stages from loose materials to a replayable packet: fixture, assemble, completeness, recompute, join, derive, witness, replay. The verdict folds out of the checks rather than being read off the packet, so a canned pass embedded in the materials can never win. A witness that reports drift lowers the derived verdict, and a witness that cannot be reached is recorded as coverage lost rather than counted as a pass. Three outcomes: match when every claim recomputed, drift when a recomputed value disagrees with its claim, and unverifiable when the evidence to check a claim is not there." width="100%"></p>

Write the demo agent-action packet, then verify it from the packet alone:

```bash
node demo/proof.mjs agent-action --demo --json > packet.json
node demo/proof.mjs verify packet.json
```

Output from a fresh clone:

```
verdict       MATCH
witness       unavailable / UNVERIFIABLE
```

Edit the packet and verify again, and the changed fields are named:

```text
$ node demo/proof.mjs verify edited.json
packet_hash_mismatch (DRIFT)
artifact_digest_mismatch (DRIFT) outputs[0].digest
embedded_verdict_not_derived (DRIFT)
```

The witness line is a second check by [emet](https://github.com/HarperZ9/emet). Telos looks for it in a sibling `../emet` checkout or at `TELOS_EMET_CLI`. With emet present the line reads `witnessed / MATCH`. The witness can lower a verdict and never raises one.

The packet holds source refs, context refs, route, admission decision, side effects and output digests. The verifier recomputes the digests from the embedded inputs, so editing any of those fields gives DRIFT, and a missing input gives UNVERIFIABLE with its path. The verdict is computed from the checks, so a `MATCH` written into the packet has no effect. The other packet types work the same way: `research` recomputes source digests, `visual` recomputes colour and luminance from embedded sRGB samples, and `build` checks a conserved quantity against a fixture that must break it. Details are in [docs/PROOF-LANES.md](docs/PROOF-LANES.md).

## Command surface

`node demo/catalog.mjs` is the authoritative map. Highlights by area:

| Area | Commands |
| --- | --- |
| Web and APIs | `reach.mjs` (doctor, menu, fetch, site, reddit, x, api) |
| Permissions and log | `grant.mjs`, `confirm.mjs`, `keys.mjs`, `receipts.mjs` |
| Orientation | `run.mjs`, `catalog.mjs`, `server-manifest.mjs`, `status.mjs`, `doctor.mjs`, `room.mjs` |
| Doctors | `ci-doctor.mjs`, `ci-triage.mjs`, `presentation-doctor.mjs`, `accessibility-doctor.mjs`, `performance-doctor.mjs`, `compatibility-doctor.mjs`, `operator-doctor.mjs`, `mcp-freshness.mjs` |
| Proof | `proof.mjs` (agent-action, research, visual, build, verify, export), `showcase.mjs` |
| Context | `context-envelope.mjs`, `context-pack.mjs`, `action-receipt.mjs`, `loop-ledger.mjs` |
| Creative | `creative-engine.mjs`, `creative-kernels.mjs`, `measurement-layers.mjs`, `rendering-capabilities.mjs`, `display-calibration.mjs` |
| Research | `causal-workbench-proof-packet.mjs`, `embodied-sim2real-proof-packet.mjs`, `quantum-error-correction-proof-packet.mjs`, `thermodynamic-ai-chip-receipt.mjs` |
| Foundry | `model-foundry.mjs`, `learning-forge.mjs`, `learning-forge-labs.mjs` |
| Workstation | `native-control.mjs`, `browser-evidence.mjs`, `workstation-substrate.mjs`, `revival-registry.mjs`, `second-level-flagship-queue.mjs` |

Most accept `--summary` for a compact terminal (TUI) view and `--json` for IDE, app, and automation hosts.

The doctors in full: `node demo/ci-doctor.mjs`, `node demo/presentation-doctor.mjs`, `node demo/accessibility-doctor.mjs`, `node demo/performance-doctor.mjs`, `node demo/compatibility-doctor.mjs`, and `node demo/operator-doctor.mjs`, plus `node demo/ci-triage.mjs` and `node demo/mcp-freshness.mjs`. Live CI intake works read-only: `node demo/ci-triage.mjs --gh-run owner/repo#run_id --summary`.

## Documentation

- [docs/INTRODUCTION.md](docs/INTRODUCTION.md): what Telos is and your first ten minutes.
- [docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md): the verifier loop, step by step, including where it stops.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/PROJECT-CONNECTION-MAP.md](docs/PROJECT-CONNECTION-MAP.md): system shape and how the five flagships connect.
- [docs/PROOF-LANES.md](docs/PROOF-LANES.md): the proof packet types and what each one recomputes.
- [docs/CURRENT-STATE.md](docs/CURRENT-STATE.md): current state of each surface.
- [USAGE.md](USAGE.md): install, run, MCP, and verify commands.

Peer repos: [gather](https://github.com/HarperZ9/gather) (research intake), [index](https://github.com/HarperZ9/index) (workspace maps and context), [forum](https://github.com/HarperZ9/forum) (agent routing with a causal ledger), [crucible](https://github.com/HarperZ9/crucible) (claim verification), [emet](https://github.com/HarperZ9/emet) (independent second check). Telos can launch gather, index, forum and crucible beside itself from one manifest; each also stands alone.

## Status

`project-telos-mcp` 0.9.0 is the current release, on [npm](https://www.npmjs.com/package/project-telos-mcp/v/0.9.0) and as [GitHub release artifacts](https://github.com/HarperZ9/telos/releases/tag/v0.9.0) that include native Windows ZIP and MCPB client packages. See [the client package guide](client-plugin/README.md). `npm test` runs every test file in `demo/`, and CI runs it on each change. Interfaces may still move between minor versions. The research packets are fixed demos: they do not do causal discovery, robot safety or hardware error correction.

### Upgrading from 0.2.0

0.3.0 writes native-control ledger hash version 2. Upgrade readers before writers, because 0.2.0 readers reject the new format. New readers still accept old receipts. Browser evidence packets are not redacted: URLs, titles, selectors, artifact references and summaries stay in them, so keep them private. See [release notes](docs/RELEASE-NOTES-0.3.0.md).

The roadmap is [`docs/PROJECT-TELOS-LARGE-SCALE-ROADMAP-2026-07-02.md`](docs/PROJECT-TELOS-LARGE-SCALE-ROADMAP-2026-07-02.md). The documentation index is [`docs/DOCUMENTATION-CONSOLIDATION-REGISTRY-2026-07-02.md`](docs/DOCUMENTATION-CONSOLIDATION-REGISTRY-2026-07-02.md), with machine-readable data under [`docs/registry/`](docs/registry/).

## Reading a record

Most commands print a JSON record. Here is one from the artwork checker, field by field. Run it with `python tools/check_repo_art.py --json`:

<p align="center"><img src="docs/art/receipt-anatomy.svg" alt="Six fields of a receipt the artwork checker emits, each with what comes back in it and how a reader would check that field for themselves. schema names the contract the record is written to. mode says whether the run rendered the files or only compared them. specs lists the diffable input the pictures are a function of. outputs carries one entry per drawing, each with a byte count and a SHA-256 read from the file on disk. checks carries one entry per gate, each naming itself and listing what it found. passed is the verdict, and it folds out of those checks rather than being written down, so a record cannot claim a pass its own checks do not support." width="100%"></p>

## License

Text: CC BY 4.0. Code: FSL-1.1-MIT.

The whitepapers and research notes in [`docs/research/`](docs/research/) are
licensed CC BY 4.0. Share and adapt them with credit to Zain Dana Harper; the
terms are in [`LICENSE-TEXT`](LICENSE-TEXT).

The code and the software documentation are FSL-1.1-MIT (fair source). The code is open to read and run, free for nearly any use except building a competing product, and each release converts to the MIT license after two years. Copyright is held by the author. See [LICENSE](LICENSE).

Version 0.9.0 and earlier releases were published under FSL-1.1-ALv2 and keep that license, so each of them still converts to Apache 2.0. FSL-1.1-MIT applies from the next release.

## For developers

Zero dependencies, so there is nothing to install. Run the MCP contract tests and smoke checks before opening a PR:

```bash
npm run test:mcp
node demo/catalog.mjs --summary
node demo/server-manifest.mjs --summary
node demo/room.mjs --json
```

CI (`.github/workflows/ci.yml`) runs `npm test` on Node 24. Run one test file with `node demo/<name>.test.mjs`. `node demo/operator-doctor.mjs --summary` checks that the README, package metadata and examples match the code.

---

Built by **[Zain Dana Harper](https://github.com/HarperZ9)** in Seattle. More tools: [Project Telos](https://harperz9.github.io), [Flywheel](https://github.com/HarperZ9/flywheel) and its [getting started guide](https://github.com/HarperZ9/flywheel/blob/main/GETTING-STARTED.md), and the [workspace canon](https://github.com/HarperZ9/workspace).
