# Public Workspace Documentation Catalog

Date: 2026-07-02
Status: first cross-repo documentation scan

This catalog is a path-and-count scan over top-level Git repositories under
`C:/dev/public`. It is a maintenance control artifact, not a claim that every
document is current, safe to publish, or correct.

Machine-readable catalog:
`docs/registry/public-workspace-doc-catalog-2026-07-02.json`

## Scan Boundary

The scan used `rg --files` over top-level Git repositories and counted
Markdown/RST documentation files while excluding `.git`, `node_modules`,
virtual environments, `dist`, `build`, and caches.

The broader raw workspace contains additional files, nested mirrors, JSON
receipts, TXT payloads, and non-Git folders. Those are intentionally outside
this first public-doc catalog. They need separate source-payload and receipt
registries so raw transcripts, outreach receipts, private scratch, and
high-risk technical material do not blur into public documentation.

## Totals

| Metric | Count |
| --- | ---: |
| Top-level Git repos scanned | 54 |
| Markdown/RST docs counted | 909 |
| Research-like docs by path | 29 |
| Status/roadmap/current-state-like docs by path | 34 |
| Internal/scratch-like docs by path | 7 |
| Large doc surfaces, 40+ docs | 3 |
| Repos needing research review | 5 |

## Lane Summary

| Lane | Repos | Docs | Research-like docs | First action |
| --- | ---: | ---: | ---: | --- |
| Research and philosophy corpus | 2 | 185 | 6 | Split into dedicated subregistry before publication cleanup. |
| Five-flagship spine | 6 | 157 | 17 | Keep status and research docs synchronized with live receipts. |
| Supporting tooling | 13 | 122 | 0 | Keep indexed; refresh when product surface changes. |
| Agent-accountability organs | 11 | 119 | 0 | Consolidate into proof-packet and agent-action lanes. |
| Build ecosystem | 10 | 115 | 0 | Refresh Build naming, maturity ledgers, and receipt boundaries. |
| Proof and witnessing | 5 | 112 | 5 | Promote reusable proof-surface contracts into Telos docs. |
| Creative/rendering engine | 7 | 99 | 1 | Join rendering, calibration, measurement, and visual proof demos. |

## Largest Doc Surfaces

| Repo | Lane | Docs | Research-like | Status-like | Recommended action |
| --- | --- | ---: | ---: | ---: | --- |
| `senses-and-sensibility` | research-and-philosophy-corpus | 172 | 3 | 3 | Keep Senses subregistry current before publication cleanup. |
| `telos` | five-flagship-spine | 89 | 17 | 4 | Keep Telos repo subregistry current before publication, outreach, proof-demo, or site claims. |
| `emet` | proof-and-witnessing | 55 | 0 | 0 | Keep indexed; refresh only when product surface changes. |
| `proof-surface` | proof-and-witnessing | 26 | 0 | 0 | Keep indexed; promote reusable contract wedges into Telos registry. |
| `portfolio-site` | creative-rendering-engine | 25 | 1 | 1 | Review research-like docs for whitepaper, proof-demo, or internal-source status. |
| `index` | five-flagship-spine | 24 | 0 | 2 | Refresh status and roadmap docs against current receipts. |
| `raw` | creative-rendering-engine | 24 | 0 | 4 | Refresh status and roadmap docs against current receipts. |
| `build-universe` | build-ecosystem | 21 | 0 | 5 | Refresh status and roadmap docs against current receipts. |
| `accountable-surface` | agent-accountability-organs | 20 | 0 | 0 | Keep indexed; map into agent-action packet line. |
| `telos-oss-showcase` | supporting-tooling | 18 | 0 | 1 | Refresh status docs against current receipts. |
| `engine-revival` | creative-rendering-engine | 16 | 0 | 0 | Keep indexed; connect revival records to Telos engine docs. |
| `studio-engine` | creative-rendering-engine | 16 | 0 | 0 | Keep indexed; connect to rendering and creative-engine lanes. |

## High-Priority Subregistries

### `senses-and-sensibility`

This is the largest doc surface and should not be folded blindly into product
docs. It is a research and philosophy corpus with publication-shaped material.

First subregistry:
`docs/registry/SENSES-AND-SENSIBILITY-SUBREGISTRY-2026-07-02.md`

First subregistry fields:

- corpus section
- manuscript or chapter path
- maturity label
- citation target
- overlap with Telos engineering claims
- public-safe excerpt boundary
- publication target: dissertation, paper, whitepaper, site page, or internal
  research note

### `telos`

Telos is the active control-plane repo and has the densest mix of roadmap,
proof-demo, outreach, receipt, and research material. It needs the strictest
classification because it is where research claims can accidentally become
product claims.

First subregistry:
`docs/registry/TELOS-REPO-SUBREGISTRY-2026-07-02.md`

First subregistry fields:

- `public-index`
- `public-official`
- `public-whitepaper`
- `proof-demo`
- `paper-candidate`
- `internal-source`
- `quarantine-and-adapt`
- `working-tree-only`

### `emet` and `proof-surface`

These repos are reusable proof/witnessing foundations. Their docs should feed
the Telos megatool map, but their validators and contracts should remain
separate products.

First subregistry:
`docs/registry/PROOF-WITNESSING-SUBREGISTRY-2026-07-02.md`

First subregistry fields:

- contract name
- validator or command
- verdict lattice
- authority boundary
- Telos consumer
- market-facing wedge
- conformance test

### Build Ecosystem

The Build ecosystem has enough docs to warrant its own registry because the
scope is broader than BuildLang/buildc alone: compiler, modules, color,
calibration, finance, UI, oracle, engine, VS Code tooling, and universe docs.

First subregistry:
`docs/registry/BUILD-ECOSYSTEM-SUBREGISTRY-2026-07-02.md`

First subregistry fields:

- current name
- lineage name
- maturity label
- receipt capability
- backend/runtime status
- Telos integration point
- market lane: math, physics, rendering, color, quant, finance, security, or
  tooling

## Publication Control Decisions

- `senses-and-sensibility` should be treated as a publication corpus, not a
  tooling README source.
- `telos/docs/research/**` should stay in the publication queue until each
  paper candidate passes source, scope, falsification, reproduction, risk, and
  freshness gates.
- `proof-surface` and `emet` docs should be cited as proof/witnessing
  infrastructure, not copied into Telos wholesale.
- Build ecosystem docs should be used as evidence of current runtime direction
  only after status and maturity ledgers are checked.
- Creative/rendering docs should be routed into the color/rendering measurement
  proof kit, with device, render, profile, and artifact receipts separated.
- Outreach docs and raw receipts are not product docs. They can support a claim
  only after the claim is restated in an official, source-backed packet.

## Next Maintenance Passes

1. Keep `docs/registry/senses-and-sensibility-subregistry-2026-07-02.json`
   current as human-gate, citation-locator, paper-track, and missing-artifact
   repairs land.
2. Keep `docs/registry/build-ecosystem-subregistry-2026-07-02.json` current as
   Build receipt imports and proof-kit schemas land.
3. Keep `docs/registry/proof-witnessing-subregistry-2026-07-02.json` current as
   proof-surface bridge fixtures, proof-index runs, and report renderers land.
4. Keep `docs/registry/telos-repo-subregistry-2026-07-02.json` current as
   proof demos, outreach receipts, official packets, publication gates, and
   cache quarantine checks land.
5. Refresh `docs/PROJECT-CONNECTION-MAP.md` from the catalog lanes.
6. Add a stale-doc check that flags old names, unsupported maturity claims,
   missing non-claims, and receipt/date drift.
7. Move raw source-payload and outreach-receipt indexing into a separate
   internal-source catalog so it cannot pollute public publication docs.
