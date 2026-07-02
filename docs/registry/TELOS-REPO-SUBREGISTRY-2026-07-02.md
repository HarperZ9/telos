# Telos Repo Subregistry

Date: 2026-07-02
Status: first Telos repo mixed-surface consolidation pass

This subregistry classifies the Telos repository itself. It does not certify a
release, prove a site page is live, prove a scientific result, prove market
traction, or prove every local change has been committed and pushed. It records
the current control-plane shape so front-door docs, research packets, proof
demos, outreach copy, receipt stores, and caches do not blur into one claim
surface.

Machine-readable companion:
`docs/registry/telos-repo-subregistry-2026-07-02.json`

## Evidence Read

| Evidence | Current result | Confidence |
| --- | --- | --- |
| Flagship status refresh | Gather `1.5.0`, Index `2.8.0`, Forum `1.12.0`, and Crucible `1.1.0` returned `MATCH`. | high |
| Telos server manifest | `telos.server.manifest` returned `MATCH` for source/package profiles, host targets, expected tools, and freshness probes. | high |
| Telos operator doctor | `telos.operator.doctor` returned `MATCH`, 14/14 checks passed, with README/current-state/catalog/manifest/status surfaces present. | high |
| Index Telos repo map | One public repo on `main`, head `1e0e1a1`, dirty count 3, untracked count 35, root SHA256 prefix `45e8256faa8bdc98`. | high |
| Forum route | Routed this subregistry and TI Morse integration request to `project-telos`, confidence `0.5`, no escalation. | high |
| Gather docs digest | Telos docs digest verified with seal `24b94d64f78e323245338463f79b6b87d97738bf1db489234826ff438a3d6270`; 38 large payloads were dropped from model context. | high |
| Git state | `main` is behind `origin/main` by 17 commits; tracked dirty files are `CHANGELOG.md`, `README.md`, and `docs/CURRENT-STATE.md`; many registry, QEC, outreach, and receipt artifacts are untracked. | high |

## Surface Counts

| Surface | Count |
| --- | ---: |
| Repo Markdown/RST docs | 94 |
| Docs Markdown/JSON/RST files | 150 |
| Demo MJS/JSON/MD files | 198 |
| Root Markdown docs | 7 |
| Root docs Markdown docs | 14 |
| Official research docs | 7 |
| Whitepaper research docs | 7 |
| Outreach docs | 12 |
| Outreach receipt Markdown files | 7 |
| Outreach receipt JSON files | 61 |
| Registry JSON files | 6 |
| Registry Markdown files | 5 |
| Root demo `.mjs` files | 106 |
| Root demo test `.mjs` files | 54 |
| Research receipt JSON files | 13 |

## Classification Rows

| Row | Role | Publication boundary |
| --- | --- | --- |
| Front door | `README.md`, `CHANGELOG.md`, `PRODUCT.md`, `USAGE.md`, `AGENTS.md`, `AUTHORS.md`, and `CONTRIBUTING.md`. | Keep concise; claim only stable public demos and current registry links. |
| Control-plane docs | Current state, roadmap, consolidation registry, frontier posture, connection map, inventory, architecture, how-it-works, and buyer docs. | State strategy and scope only when committed, working-tree, planned, inferred, and unverifiable claims are separated. |
| Registry control plane | Documentation registry, public-workspace catalog, Build, proof/witnessing, Senses, and Telos subregistries. | Classify and route; do not prove correctness, publication readiness, or release status. |
| Research official and whitepapers | `docs/research/official/*.md`, `docs/research/whitepapers/*.md`, publication queue, mycology, and RL-scaling docs. | Require source, scope, falsification, reproduction, risk, and freshness gates before promotion. |
| Proof-demo fixtures | Causal, embodied, QEC, source-receipt, and TI Morse demo receipts and tests. | Fixture `MATCH` is bounded to command, fixture, and negative controls; it is not field-result proof. |
| Outreach copy | `docs/outreach/*.md`. | Outreach copy is not evidence and must cite official packets, demo commands, and receipt ids before publication. |
| Outreach and proof receipts | `docs/outreach/receipts/**/*.json`, `.jsonl`, and `.md`. | Public docs cite digest, report, and typed packet refs instead of raw object stores. |
| Demo and integration surface | `demo/*.mjs`, `demo/*.test.mjs`, `demo/integrations/*.json`, and integration notes. | Tested demos prove only their bounded contracts, not external service integration or production readiness. |
| Frontier posture and risk | Frontier R&D posture, publication queue, and current state. | High-risk material is shaped as research, measurement, safety, simulation, assurance, education, or accountable tooling. |
| Superpowers specs and verification | `docs/superpowers/**` and `docs/verification/**`. | Specs and historical verification reports can drift; rerun relevant commands before capability claims. |
| Funding, brand, and support | Funding, brand, presentation, OSS showcase, and quality revival docs. | Budget and brand docs are context, not proof of funding, traction, or market validation. |
| Caches and local payloads | `.telos/**`, cache directories, and dogfood caches. | Public artifacts may reference digest seals, redacted refs, and claim boundaries only. |

## TI Morse Integration Boundary

The latest YouTube/source cluster is already represented as a bounded TI Morse
field intake. The current packet records five video metadata receipts, five
transcript receipts, and one channel-list snapshot. It maps source leads into
industrial science proof packets, causal research workbench, agentic benchmark
foundry, microscopy/materials/biology measurement, and compute/infrastructure
ledger lanes.

The verified local claim is the intake shape: receipts exist, raw transcript
bodies are not tracked, and the lane map is explicitly inferred. Nuclear,
energy, manufacturing, causal, AGI benchmark, biology, microscopy, materials,
AI-scale, economics, and infrastructure claims remain
`UNVERIFIABLE_UNTIL_PRIMARY_SOURCE_OR_REPLAY`.

## Publication Controls

- Label working-tree artifacts `working-tree-only` until committed or explicitly
  published.
- Keep outreach copy separate from evidence; official packets and proof demos
  come first.
- Cite receipt stores by digest, report, and typed packet reference rather than
  copying raw object stores into front-door docs.
- Keep raw transcripts, caches, private/local payloads, and run internals
  internal or quarantined.
- Require source, scope, falsification, reproduction, risk, and freshness gates
  for every research packet.
- Bound every demo claim to the exact command, fixture, and negative controls
  that were run.

## First Telos Bridges

| Priority | Bridge | First artifact |
| ---: | --- | --- |
| 1 | Commit-boundary publication gate | Block README/site claims when a referenced demo or doc is still working-tree-only. |
| 2 | Receipt-index bridge | Feed `docs/outreach/receipts` and `demo/research` receipts into Repo Proof Index or a Telos proof-index row. |
| 3 | Outreach-to-official claim gate | Require each outreach wave to cite an official packet, proof-demo command, and receipt id. |
| 4 | Cache and raw payload quarantine | Add a stale/raw payload scan for dogfood caches and local Gather payload references. |

## Hard Non-Claims

- This is not release certification.
- This is not proof that a portfolio site page is live.
- This is not scientific, market, buyer, or adoption evidence.
- This is not proof that all demos pass.
- This is not proof that local changes are committed or pushed.
- This is not a claim that the TI Morse videos prove their domain claims.

## Next Passes

1. Keep this subregistry synchronized with every documentation consolidation
   pass.
2. Create one row per public site page after the portfolio pages are committed
   and live.
3. Build the receipt-index bridge over outreach and research receipts.
4. Add the commit-boundary check before README, site, or outreach copy claims a
   working-tree artifact is shipped.
5. Review dogfood caches and ignore policy so cache artifacts cannot become
   public research evidence by accident.
