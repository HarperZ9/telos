# Project Telos 0.2.0

Release notes for the operator-authorized 0.2.0 release. This file summarizes
the source changes since `v0.1.0` (2026-06-29); package availability and
source-checkout verification are separate from live control measurements.

## Summary

0.1.0 shipped the five-flagship operator room: catalog, server manifest,
MCP freshness, and the certificate-loop demo. Since then, `main` added a
doctor suite, a CI triage lane, browser evidence packets, a Learning Forge
research lane, the OSS Proof Showcase scout, a render seam for the learn
flagship, and the packaging needed to install the workbench as commands.
The MCP surface grew from 64 to 69 tools (telos from 37 to 41).

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
  MCP tool (tool count 64 to 65). The proof lanes below then carried the
  surface to 69 tools.

## Research and delivery lanes

- Learning Forge research packet and executable labs.
- OSS Proof Showcase lane: fixture-first candidate scout and PR-readiness
  packets (`demo/showcase.mjs`).
- Second-level flagship queue exposure and workstation substrate intake.
- `telos render <specPath>` CLI subcommand (`demo/telos-cli.mjs`) for the
  learn flagship interop seam.

## Proof lanes

- Four fixture-backed proof packets over `demo/proof.mjs`, each with its own
  verifier and exporter: agent-action (`telos.proof`), research-claim
  (`telos.proof.research`), visual-truth (`telos.proof.visual`), and build
  scientific-runtime (`telos.proof.build`).
- These four read-only MCP tools moved the five-flagship catalog from 65 to
  69 tools and grew the telos surface from 37 to 41 tools.

## Presentation and brand

- Forward-facing repository presentation inventory and render configs.
- Flagship card repo banner; emet, buildlang, and learn added to the
  cross-repo nav.

## Fixes

- Manifest: gather/forum `source_checkout` launch aligned with the
  trampoline contract.
- Manifest: `index.select` declared as Index auxiliary compatibility surface
  so the launch gate matches the current Index tool surface.
- Release preflight also declares Gather context/pilot and five Index router-job
  tools, bringing the auxiliary surface to 36 tools. These names were checked
  with `tools/list`; that check does not establish each tool's live behavior.
- Brand gate: hero dimension check matches the shipped flagship card canon
  (2400x1260).
- Native-control packaging includes the Windows UIA and device helpers beside
  their drivers. Explicit browser matches reject missing or ambiguous targets
  before a CDP connection; focus receipts preserve unknown background behavior.
  These are contract and packaging checks, not proof of live computer control
  or background-only operation.

## Packaging (this release)

- `bin` entries: `telos-mcp` (stdio MCP server) and `telos` (router over the
  demo command surface).
- An npm tarball and runnable zip share one reviewed file set, including the
  native helper scripts and their contract documentation. The zip contains a
  `telos/` directory. `SHA256SUMS.txt` records both archive digests.
  Render receipts with local font-input metadata are excluded from the assets.
- Release workflow checks out the requested tag, runs the CI and source-launch
  gates, validates archive entries, and attaches new assets. Existing assets
  are never overwritten. npm registry publication is a separate action and is
  not part of this release.

## Install and run

```bash
node demo/telos-mcp.mjs            # from a checkout or the extracted telos/ zip
node demo/telos.mjs catalog --summary
npm install -g ./project-telos-mcp-0.2.0.tgz  # downloaded release asset
telos catalog --summary
```

Node 20 or newer is required; CI uses Node 24. The five-server source-checkout
launch gate additionally requires sibling `gather`, `crucible`, `index`, and
`forum` checkouts. The tarball does not bundle those servers. Research fixtures
and proof receipts retain their stated scope; this release makes no MHS
conformance, live actuation, model-quality, or comparative-superiority claim.

Validation limit: the existing hyphal context benchmark remains advisory in CI
because of its stale-commit dependency. Its failure is retained and is not
counted as passing release evidence.
