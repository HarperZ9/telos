# Project Telos 0.2.0 (draft)

Draft release notes. The tag and the GitHub release are cut by the operator;
this file summarizes what actually landed on `main` between `v0.1.0`
(2026-06-29) and this release candidate, derived from the git history.

## Summary

0.1.0 shipped the five-flagship operator room: catalog, server manifest,
MCP freshness, and the certificate-loop demo. Since then, `main` added a
doctor suite, a CI triage lane, browser evidence packets, a Learning Forge
research lane, the OSS Proof Showcase scout, a render seam for the learn
flagship, and the packaging needed to install the workbench as commands.
The MCP surface grew from 64 to 65 tools.

## Doctor suite

- CI doctor (`demo/ci-doctor.mjs`, `telos.ci.doctor`): GitHub Actions
  runtime and action-major drift receipts for the five flagships, including
  local workflow scanning with `--scan-root`.
- CI triage (`demo/ci-triage.mjs`, `telos.ci.triage`): separates fatal
  test/format/step failures from Node runtime migration warnings, with live
  read-only intake via `--gh-run owner/repo#run_id`.
- Presentation doctor: README, changelog, and brand parity across flagships,
  with a configurable nav roster and umbrella-aware conformance.
- Accessibility doctor, performance doctor, compatibility doctor, and
  operator doctor complete the lane.

## Browser evidence

- `project-telos.browser-evidence/v1` packet contract,
  `demo/browser-evidence.mjs` native verbs, and the `telos.browser.evidence`
  MCP tool (tool count 64 to 65).

## Research and delivery lanes

- Learning Forge research packet and executable labs.
- OSS Proof Showcase lane: fixture-first candidate scout and PR-readiness
  packets (`demo/showcase.mjs`).
- Second-level flagship queue exposure and workstation substrate intake.
- `telos render <specPath>` CLI subcommand (`demo/telos-cli.mjs`) for the
  learn flagship interop seam.

## Presentation and brand

- Forward-facing repository presentation inventory and render configs.
- Flagship card repo banner; emet, buildlang, and learn added to the
  cross-repo nav.

## Fixes

- Manifest: gather/forum `source_checkout` launch aligned with the
  trampoline contract.
- Manifest: `index.select` declared as Index auxiliary compatibility surface
  so the launch gate matches the current Index tool surface.
- Brand gate: hero dimension check matches the shipped flagship card canon
  (2400x1260).

## Packaging (this release)

- `bin` entries: `telos-mcp` (stdio MCP server) and `telos` (router over the
  demo command surface).
- `files` allowlist so `npm pack` ships the runnable demo, the current-state
  doc, and brand assets only.
- Release workflow that builds the npm tarball and a runnable demo zip on
  manual dispatch or a published release. No automated publishing.

## Install and run

```bash
node demo/telos-mcp.mjs            # from a checkout
node demo/telos.mjs catalog --summary
# once published: npx --package project-telos-mcp telos-mcp
```
