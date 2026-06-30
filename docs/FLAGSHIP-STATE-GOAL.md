# Project Telos Flagship-State Goal

Generated: 2026-06-30

This is the active goal ledger for bringing the flagship and private-line tools
to flagship state. It is intentionally evidence-first: a tool is not flagship
because the README says so; it is flagship when the public/developer surface,
protocol surface, tests, receipts, and operational boundaries all verify.

## Current Receipts

Fresh dogfood pass, 2026-06-30:

- Telos compatibility doctor: `MATCH`, 14/14 checks, 63 tools, 5 servers.
- Telos MCP freshness contract: `MATCH`; stale server, tool-surface drift,
  version drift, behavior drift, unresolved launcher, and unavailable freshness
  probes are typed failure codes.
- Gather status: `MATCH`, version `1.5.0`, host surfaces include CLI JSON, MCP
  stdio, plugins, IDEs, TUIs, and apps.
- Gather source launcher fix: commit `ab959c7`; GitHub Actions run
  `28459724472` passed on Python 3.11 and 3.12 after fixing
  `python -m gather.cli` from source checkout.
- Index public map: `C:\dev\public`, generated `2026-06-30T09:26:32-07:00`,
  repo_count `52`, dirty_count `2`, root prefix `92ef331e0850ccf6`.
- Index private-line map: `C:\dev\opsec`, generated
  `2026-06-30T09:26:42-07:00`, repo_count `5`, dirty_count `0`, root prefix
  `d3bb8c6b0e33f765`.
- Index state map: `C:\dev\state`, generated `2026-06-30T09:26:41-07:00`,
  repo_count `4`, dirty_count `0`, root prefix `f66313befd67089d`.
- Forum route for the active goal: decided `project-telos`, confidence
  `0.6818181818181818`, no escalation.
- Aleph private-line doctor with local Codex MCP config: aggregate `MATCH`;
  `aleph`, `gather`, `crucible`, `index`, `forum`, and `telos` launchers all
  `MATCH`.

## Flagship-State Gates

Every first-level flagship must meet these gates:

- Product surface: README, changelog, status, brand graphic, quick start, and
  developer/operator narrative are current and plain enough for a public user.
- Protocol surface: CLI JSON, MCP stdio, IDE/TUI/plugin/app embedding, and
  source-checkout launchers work without hidden local assumptions.
- Receipt surface: actions emit typed schemas, hashes or redacted refs, verdicts
  of `MATCH`, `DRIFT`, or `UNVERIFIABLE`, and clear next actions.
- Host freshness: loaded MCP servers can be compared against manifest versions,
  tool hashes, status payloads, and behavior probes before output is trusted.
- CI health: current branch is pushed, GitHub Actions pass, and runtime/action
  major drift is visible through Telos CI receipts.
- Security boundary: no `.env`, keys, tokens, raw private evidence, private
  runbooks, or high-risk payloads cross into public repos or public docs.
- Accessibility and performance: any site or app surface has static receipts
  for landmarks, labels, reduced motion, focus handling, byte/script budgets,
  asset policy, and embedding posture.
- Large-context operation: Index context envelopes, Gather digests, Forum
  route/ledger decisions, Crucible verdicts, and Telos loop/action receipts are
  available for handoff without dumping raw workspaces into model context.

Private-line tools use the same gates plus an extra publication boundary:

- Public docs may describe role, interface, receipt shape, and sanitized
  capability class.
- Sensitive runtime behavior, credentials, target material, private runbooks,
  payloads, and proprietary sources stay inside local/private repos and local
  adapters.

## Active Tool Set

First-level flagships:

- `gather`
- `crucible`
- `index`
- `forum`
- `telos`

Private-line flagships:

- `aleph` / `opsec`
- `seed`
- `kun`
- `sofer`
- `orca`
- `behavior-transform.io`

Second-level and revival candidates are promoted only after a lane record has a
source receipt, risk boundary, host flagship, interop shape, native check, and
Crucible-verifiable claim.

## Immediate Queue

1. Keep Aleph/opsec as the private-line receipt server and cross-tool doctor.
2. Fix source-checkout and MCP parity bugs as they are found, starting with the
   highest-blast-radius flagship surfaces.
3. Convert current map receipts into repo-specific issue lists: docs, CI,
   protocol, presentation, accessibility, performance, and safe publication.
4. Continue small pushed increments with CI evidence instead of large
   unverified sweeps.
5. Promote older tools through shared contracts rather than copy/paste import:
   source, transform, criterion, measurement, verdict, replay reference.

## Non-Negotiable Stop Conditions

- Do not publish secrets, `.env` files, credentials, private evidence, or
  sensitive local-only payloads.
- Do not claim a tool is flagship-state without current receipts.
- Do not trust a live MCP handle after source changes until freshness probes or
  a host restart confirm the loaded server state.
