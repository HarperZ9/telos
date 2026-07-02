# Documentation Consolidation Registry

Date: 2026-07-02
Status: first control-plane registry

This registry starts the maintenance pass for Project Telos documentation. It
does not claim the whole corpus is clean. It establishes the labels and first
routing decisions so follow-up passes can update, publish, quarantine, or
internalize documents consistently.

The machine-readable companion is
`docs/registry/documentation-registry.json`. The publication-control companion
is `docs/research/PUBLICATION-QUEUE-2026-07-02.md`. The cross-repo
documentation catalog is
`docs/registry/PUBLIC-WORKSPACE-DOC-CATALOG-2026-07-02.md`, with machine data
at `docs/registry/public-workspace-doc-catalog-2026-07-02.json`. The Senses
and Sensibility subregistry is
`docs/registry/SENSES-AND-SENSIBILITY-SUBREGISTRY-2026-07-02.md`, with machine
data at `docs/registry/senses-and-sensibility-subregistry-2026-07-02.json`. The Build
ecosystem subregistry is
`docs/registry/BUILD-ECOSYSTEM-SUBREGISTRY-2026-07-02.md`, with machine data at
`docs/registry/build-ecosystem-subregistry-2026-07-02.json`. The
proof/witnessing subregistry is
`docs/registry/PROOF-WITNESSING-SUBREGISTRY-2026-07-02.md`, with machine data
at `docs/registry/proof-witnessing-subregistry-2026-07-02.json`. The Telos
repo subregistry is
`docs/registry/TELOS-REPO-SUBREGISTRY-2026-07-02.md`, with machine data at
`docs/registry/telos-repo-subregistry-2026-07-02.json`.

## Registry Rules

- Public docs need stable claims, source refs, commands, and non-claims.
- Internal docs may hold raw payloads, transcripts, runbooks, private scans, and
  high-risk technical detail, but public docs should reference them only by
  hash, receipt id, or sanitized summary.
- A whitepaper is not automatically publication-ready. It becomes a paper
  candidate only after citation, method, artifact, and risk review.
- Nested repo docs are not secondary. BuildLang, Build Universe, Proof Surface,
  Learn, Emet, Reconcile, Studio Engine, and the Build packages contain
  first-class Telos evidence.
- A stale name such as QuantaLang can remain for lineage, but current product
  docs should prefer BuildLang, `buildc`, Build Universe, and Build ecosystem
  when the repo has already moved.

## Current Workspace Evidence

| Item | Current evidence | Confidence |
| --- | --- | --- |
| Public workspace map | 68 repos, 62 public-class, 6 local-class, 7 dirty. | high |
| Telos dirty state | Telos has working-tree docs and proof artifacts, including QEC files and unrelated outreach files. | high |
| Site dirty state | Portfolio site has a QEC page update in working tree. | high |
| BuildLang evidence | BuildLang README documents `buildc`, C backend, typed effects, receipts, and scientific runtime receipts. | high |
| Build Universe evidence | Build Universe README says BuildLang compiler is Rust, C backend is working, self-hosting is a goal, and BuildOS is a separate hobby kernel. | high |
| TI Morse field intake | Captured as source receipts, not promoted domain truth. | high |
| Telos repo subregistry | Telos repo classified into front-door, control-plane, registry, research, proof-demo, outreach, receipt, integration, risk, verification, support, and cache surfaces. | high |

## Public Index Docs

| Document | Label | Current action |
| --- | --- | --- |
| `README.md` | `public-index` | Keep as product front door; add roadmap links and avoid overloading with full strategy. |
| `CHANGELOG.md` | `public-index` | Keep factual release ledger; do not use as strategy document. |
| `docs/CURRENT-STATE.md` | `public-index` | Update every serious pass after Index/Forum/Gather/Crucible checks. |
| `docs/PROJECT-CONNECTION-MAP.md` | `public-index` | Keep as constellation map; refresh Build naming and new domain lanes in follow-up. |
| `docs/FORWARD-FACING-REPOSITORY-INVENTORY.md` | `public-index` | Needs refresh from 2026-06-29 counts to 2026-07-02 Index map. |
| `docs/ARCHITECTURE.md` | `public-index` | Keep as system architecture; cross-link to megatool roadmap. |
| `docs/WHO-USES-IT.md` | `public-index` | Needs buyer/persona update after market research pass. |

## Research Docs

| Document family | Label | Current action |
| --- | --- | --- |
| `docs/research/official/*.md` | `public-official` | Keep short, source-backed, non-claim heavy. |
| `docs/research/whitepapers/*.md` | `public-whitepaper` | Treat as paper candidates only after citation and artifact review. |
| `docs/research/proof-packets/**` | `proof-demo` | Keep runnable/formal artifacts; add registry rows per packet. |
| `docs/research/mycology-network-intelligence.md` | `paper-candidate` | Reframe as hyphal context protocol / learning systems paper, not biology truth. |
| `docs/research/rl-scaling-receipt-spine.md` | `paper-candidate` | Route into Model Foundry and objective monitor paper queue. |
| `docs/research/dogfood/**/.cache` | `quarantine-and-adapt` | Cache artifacts should not be public research evidence; review ignore policy. |

## Current Paper Candidates

| Candidate | Existing artifacts | Next edit |
| --- | --- | --- |
| BuildLang Scientific Runtime Receipts | BuildLang README and `docs/SCIENTIFIC-RECEIPT.md`; `buildc receipt export` bridge. | Draft methods paper: accountable scientific compute receipts and Crucible export. |
| Causal Research Workbench | Official/whitepaper, proof packet, Learn/Crucible receipts. | Add synthetic SCM and BuildLang typed DAG plan. |
| QEC Proof Packets | Working-tree official/whitepaper/outreach docs and fixture. | Commit/publish after rebasing; then plan Clifford/surface-code follow-on. |
| Embodied Sim-to-Real | Official/whitepaper/outreach docs and site page. | Add typed-unit BuildLang version and controller-stability packet. |
| TI Morse Field Integration | Source receipt ledger, official/whitepaper/outreach docs. | Capture primary sources before any field claim promotion. |
| Hyphal Context Protocol | Biology network and hyphal context benchmark docs. | Expand benchmark over more corpora and record false-claim rates. |
| Formal PDE Replay | Lean proof-packet material and whitepaper. | Add BuildLang numerical receipt and formal boundary table. |
| Browser Evidence Kernel | Design/plan docs and smoke receipt. | Convert to agent action proof packet paper. |

## Machine-Readable Registry Snapshot

`docs/registry/documentation-registry.json` currently records:

| Class | Row count | Notes |
| --- | ---: | --- |
| Evidence records | 13 | Gather, Index, Forum, Crucible, Telos manifest, Index map, Git dirty state, Ti Morse federation seal, public-workspace doc catalog, Build ecosystem subregistry, proof/witnessing subregistry, Senses subregistry, and Telos repo subregistry. |
| Documentation rows | 14 | Front-door docs, current-state docs, roadmap, posture, connection map, inventory, buyer/persona docs, cross-repo doc catalog, Build ecosystem subregistry, proof/witnessing subregistry, Senses subregistry, and Telos repo subregistry. |
| Research packet rows | 8 | BuildLang runtime, causal, embodied, biology, hyphal, formal replay, QEC, and Ti Morse field integration. |
| Build ecosystem rows | 6 | Build subregistry, BuildLang/buildc, Build Universe, Build Color, Calibrate Pro, and Build Engine. |
| Proof/witnessing rows | 6 | Proof/witnessing subregistry, EMET, Proof Surface, Repo Proof Index, Proof Surface Report, and Witnessing Spine. |
| Senses and Sensibility rows | 9 | Senses subregistry, front door, integrated thesis, dissertation apparatus, paper track, bibliography policy, source substrate, engineering/security bridge, and referenced-missing curation artifacts. |
| Telos repo rows | 12 | Front door, control-plane docs, registry control plane, research official/whitepapers, proof demos, outreach copy, outreach/proof receipts, demo/integration surface, frontier risk, specs/verification, funding/brand/support, and caches/local payloads. |
| Megatool nodes | 5 | Research workbench, Build runtime, industrial science packets, agent action packets, and color/rendering measurement. |
| Internal fence rows | 3 | Raw transcripts/source payloads, credentials/session state, and high-risk operational detail. |

The Ti Morse federation row is source-intake only. It validates the source
registry shape and seal for five videos plus one channel catalog; it does not
promote nuclear, AI, biology, manufacturing, or economics claims.

## Cross-Repo Catalog Snapshot

`docs/registry/PUBLIC-WORKSPACE-DOC-CATALOG-2026-07-02.md` currently records:

| Metric | Count |
| --- | ---: |
| Top-level Git repos scanned | 54 |
| Markdown/RST docs counted | 909 |
| Research-like docs by path | 29 |
| Status/roadmap/current-state-like docs by path | 34 |
| Internal/scratch-like docs by path | 7 |

The largest doc surfaces are `senses-and-sensibility`, `telos`, `emet`,
`proof-surface`, `portfolio-site`, `index`, `raw`, and `build-universe`.
The Senses, proof/witnessing, Build ecosystem, and Telos repo subregistries now
exist. The remaining deeper work is per-site-page, receipt-store, and
internal-source subregistry expansion.

## Telos Repo Snapshot

`docs/registry/TELOS-REPO-SUBREGISTRY-2026-07-02.md` currently records:

| Metric | Count |
| --- | ---: |
| Repo Markdown/RST docs | 94 |
| Docs Markdown/JSON/RST files | 150 |
| Demo MJS/JSON/MD files | 198 |
| Official research docs | 7 |
| Whitepaper research docs | 7 |
| Outreach docs | 12 |
| Outreach receipt JSON files | 61 |
| Research receipt JSON files | 13 |

The Telos split is now explicit: front-door docs are navigation and stable demo
claims; control-plane docs describe strategy with claim-state labels; research
docs stay behind publication gates; demos prove bounded fixtures only;
outreach copy is not evidence; receipt stores are cited by digest and typed
packet; caches and raw payloads remain internal or quarantined. The repo is
currently on `main`, behind `origin/main` by 17 commits, with tracked edits and
untracked registry, QEC, outreach, and receipt artifacts, so working-tree
boundaries must stay visible.

## Senses And Sensibility Snapshot

`docs/registry/SENSES-AND-SENSIBILITY-SUBREGISTRY-2026-07-02.md` currently
records:

| Metric | Count |
| --- | ---: |
| Markdown/RST docs | 172 |
| Preserved `.txt` source files | 1 |
| Root Markdown docs | 12 |
| Dissertation docs | 125 |
| Submission docs | 4 |
| Paper docs | 3 |
| Thesis docs | 18 |

The Senses split is now explicit: it is a research and philosophy corpus, not a
tooling repo. It can inform Telos vocabulary around accountability,
authorship, human gates, provenance, authentication/authorization separation,
and proof-before-trust. It cannot be treated as philosophical proof, journal
readiness, authorship attestation, citation verification, or shipped Telos
capability. The current checkout is clean but one commit behind `origin/main`,
and several curation artifacts referenced by the corpus index are absent from
the local checkout.

## Build Ecosystem Snapshot

`docs/registry/BUILD-ECOSYSTEM-SUBREGISTRY-2026-07-02.md` currently records:

| Metric | Count |
| --- | ---: |
| Top-level Build-adjacent repos | 10 |
| Top-level Build Markdown/RST docs | 115 |
| BuildLang lineage docs under `pubscan/quantalang` | 131 |
| Subregistry planning rows | 11 |

The Build split is now explicit: BuildLang/buildc is the accountable compute
and receipt layer; Build Universe is the alpha domain-module ledger; Build
Color and Calibrate Pro are color/rendering measurement lanes; Build Finance,
Build Oracle, and Build Engine are quant/forecasting lanes; Build UI and editor
packages are support surfaces only.

## Proof And Witnessing Snapshot

`docs/registry/PROOF-WITNESSING-SUBREGISTRY-2026-07-02.md` currently records:

| Metric | Count |
| --- | ---: |
| Proof/witnessing repos | 5 |
| Proof/witnessing Markdown/RST docs | 112 |
| Subregistry layer rows | 5 |

The layer split is now explicit: EMET is the witness layer; Proof Surface is
the validator-contract and domain-wedge layer; Repo Proof Index is the proof
artifact index; Proof Surface Report is the reviewer-facing handoff renderer;
Witnessing Spine is the theory and publication-context corpus. The first Telos
bridges are agent-action proof packets, research-claim packets, visual
measurement packets, and AI4Science packets. These rows do not grant release,
trust, compliance, safety, authority, or product-capability status.

## Build Ecosystem Docs

| Repo/doc | Label | Current action |
| --- | --- | --- |
| `pubscan/quantalang/README.md` | `public-index` / `paper-source` | Treat as current BuildLang evidence, but prefer canonical source repo in future scans. |
| `pubscan/quantalang/docs/SCIENTIFIC-RECEIPT.md` | `paper-source` | Promote into Telos paper queue and measurement bridge docs. |
| `build-universe/README.md` | `public-index` | Use for Build family reality: mixed-language, alpha, C backend working, self-hosting goal. |
| `build-color/README.md` | `proof-demo` / `market-source` | Use for color/calibration proof kit. |
| `calibrate-pro/README.md` | `proof-demo` / `market-source` | Pair with Build Color and display calibration contract. |
| `build-engine/README.md` | `proof-demo` / `market-source` | Keep finance claims paper-first and not investment advice. |
| `build-finance`, `build-oracle`, `build-ui`, `build-ecosystem` | `public-index` | Refresh into Build mega-lane map. |

## Internal Or Fenced Material

These classes should not be copied into public docs without sanitization:

- Raw YouTube transcripts and raw video payloads under `.telos/gather/**`.
- Raw private viability notes for local-only tools.
- Credentials, `.env`, tokens, signing material, browser session state, cookies,
  and private external account data.
- Client/customer data, proprietary third-party source, unpublished private
  papers, private runbooks, and operational command logs.
- High-risk technical details in nuclear, biochem, cyber, defense, robotics, or
  security domains when they would become actionable instructions rather than
  research methodology, measurement, safety, or assurance evidence.
- Any doc whose only evidence is a model-generated summary with no source refs,
  test, or receipt.

## Quarantine Criteria

Mark a doc `quarantine-and-adapt` when any condition is true:

- It claims a maturity level not backed by current tests or receipts.
- It uses old project names as current names after a rename.
- It promotes source leads as verified scientific, market, or technical facts.
- It lacks non-claims for high-stakes domains.
- It includes raw transcripts or raw private payloads.
- It describes deployment, credentials, or external writes without action
  receipt boundaries.
- It has no timestamp and no evidence pointer.

## Maintenance Loop

Every consolidation pass should run:

```text
Index map -> Forum route -> Gather source refresh -> Crucible gate -> Telos state update
```

Then update:

1. `docs/CURRENT-STATE.md` for the live state.
2. This registry for doc classification.
3. `docs/PROJECT-TELOS-LARGE-SCALE-ROADMAP-2026-07-02.md` when priorities change.
4. `README.md` only for stable front-door changes.
5. Website pages only after the corresponding artifact is committed and verified.

## Next Registry Work

- Expand `docs/registry/documentation-registry.json` with one row per public site page.
- Expand `docs/registry/public-workspace-doc-catalog-2026-07-02.json` into
  per-repo subregistries for the largest and riskiest documentation surfaces.
- Keep `docs/registry/senses-and-sensibility-subregistry-2026-07-02.json`
  synchronized as human-gate, citation-locator, paper-track, and missing-artifact
  repairs land.
- Keep `docs/registry/build-ecosystem-subregistry-2026-07-02.json` synchronized
  as BuildLang receipt imports, Build Universe module rows, and color/quant
  proof-kit schemas land.
- Keep `docs/registry/proof-witnessing-subregistry-2026-07-02.json`
  synchronized as EMET, Proof Surface, Repo Proof Index, Proof Surface Report,
  and Witnessing Spine bridge fixtures land.
- Keep `docs/registry/telos-repo-subregistry-2026-07-02.json` synchronized as
  Telos proof demos, official packets, outreach receipts, publication gates,
  and cache quarantine checks land.
- Add the commit-boundary publication gate and receipt-index bridge identified
  by the Telos repo subregistry.
- Add stale-name rows for Quanta -> Build transitions beyond the first BuildLang lineage row.
- Add a public/internal boundary row for each local-only revival candidate.
- Add market-research `MarketRow` and `WedgeScore` sections once the next
  competitor pass has source-backed entries.
