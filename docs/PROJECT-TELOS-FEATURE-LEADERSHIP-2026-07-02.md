# Project Telos Feature-Leadership Addendum

Date: 2026-07-02
Status: strategic addendum
Follows: `docs/PROJECT-TELOS-LARGE-SCALE-ROADMAP-2026-07-02.md`
Scope: public-safe Project Telos flagships (gather, index, forum, crucible,
telos/Studio, learn, buildlang, emet), read against the roadmap's frontier
R&D posture

## 0. Why This Addendum Exists

The large-scale roadmap defines the proof spine:

```text
source -> context -> route -> action -> measurement -> verdict -> receipt -> paper/product
```

It scopes the megatool families, the proof lanes, and the frontier-domain map
(cybernetics, biochem, nuclear, AI/ML, quant, defense-adjacent, robotics,
medicine, advanced computing). Read it first. This document does not replace
any of that.

This addendum adds one correction of emphasis. The headline directive
(2026-07-02) states it plainly:

> Receipt and re-verification cannot be the only thing that makes our tools a
> better choice than another. Each really should offer the biggest and best of
> all user features.

The roadmap is heavily weighted toward the proof layer, because the proof layer
is the differentiator nobody else has. That weighting is correct for defens-
ibility and wrong for adoption. A tool that only wins on receipts is a tool a
frontier R&D user admires and does not switch to. This document rebalances the
plan so every flagship is planned as a best-in-class tool in its own category
on raw user features first, and carries the proof layer on top of those
features rather than instead of them.

## 1. Principle: Accountability Is The Floor

Three claims, in order.

1. **Accountability is the floor, not the differentiator.** Receipts,
   `MATCH`/`DRIFT`/`UNVERIFIABLE`, proof packets, hash-chained ledgers, and
   re-derivation are the price of entry for high-stakes work. They are
   necessary. They are not, on their own, a reason to switch tools. A researcher
   picks Elicit for extraction tables, a platform engineer picks LangGraph for
   human-in-the-loop, a graphics tinkerer picks Shadertoy for the live loop. The
   receipt does not enter their decision until after the tool already does the
   job.

2. **Each flagship must be best-in-class on raw user features in its own
   category.** Not "accountable but feature-thin." The target is: a researcher
   would pick gather for coverage and extraction even with the receipts turned
   off; a maintainer would pick index for symbol navigation and codebase Q&A
   even with the certificates hidden; a platform engineer would pick forum for
   HITL and the dashboard even before hearing the word ledger.

3. **The moat is features and proof compounding, not either alone.** The two do
   not sit side by side, they multiply. A feature generates evidence; the
   evidence makes the receipt real; the receipt makes the feature trustworthy
   enough to route frontier work through. A competitor can copy any single
   feature in a sprint. The property they cannot cheaply copy is that every
   feature's output is a re-derivable artifact, because copying that means
   rebuilding their product on a receipt substrate and giving up the model
   opacity their speed depends on. Reach times receipts is the compounding line.

Where the roadmap says "the differentiator is a proof-centered substrate," this
addendum says: the proof-centered substrate is the moat, and best-in-class user
features are the reason a user ever gets close enough to the moat to fall in.

### Honesty posture (carried from the roadmap's Market Gate)

Every market-position and competitor claim in this document is a **hypothesis**
until backed by a comparison matrix (roadmap Publication Gate 6). Competitor
feature descriptions are dated 2026 and cited in the per-flagship analyses that
back this addendum; treat them as moderate-to-high confidence secondary
evidence, not settled fact. No flagship is called "best" here without a stated
comparison basis, and where a flagship is behind, this document says so in
plain words. The frontier-domain scope from the roadmap applies throughout: the
standout features below are meant to serve frontier R&D users (physics, quant,
QEC, robotics, nuclear-adjacent modeling, AI/ML eval) as directly as they serve
the general user, and none of them may turn high-risk source material into
operational instructions.

## 2. Per-Flagship Feature Leadership

Each section states the category and user, the competitors that win users
today, the flagship's honest current features, the standout features it must
ship (each marked buildable-now or later), the compounding moat, and the honest
gaps. All eight flagships follow the same shape so they can be compared as
peers, consistent with the roadmap's "flagships interoperate as peers" stance.

---

### 2.1 gather (PyPI gather-engine 1.5.0; repo c:/dev/public/gather)

**Category and user.** Research intake and source ingestion: the front door
that turns scattered, gated, and awkward-to-reach material (papers, video
captions, JS-walled pages, scanned PDFs, audio, authenticated APIs, feeds,
local docs) into a durable, queryable, provenance-carrying corpus. The user is
a researcher, analyst, systematic reviewer, or an autonomous agent that must
later prove where every fact came from. In the constellation, gather is the one
organ allowed network, credentials, and third-party tools, isolated behind
source adapters, feeding index/forum/crucible/telos.

**Competitors and what wins them users.**

- **Elicit** wins systematic reviewers on structured extraction tables (define
  columns, auto-populate across thousands of papers) plus a reproducible
  PRISMA-2020 screening pipeline at up to 40,000-paper scale.
- **Undermind** wins on agentic multi-hop recall: reads hundreds of full-text
  papers per query and follows citation trails.
- **Consensus** wins on the Consensus Meter: a visual yes/no/possibly synthesis
  across roughly 200M papers.
- **SciSpace** wins on breadth (280M+ papers, more free extraction columns).
- **LlamaParse / Docling** win on high-fidelity document parsing (table
  boundaries, multi-column, OCR to clean Markdown/JSON).
- **OpenAlex / Semantic Scholar** win as free, keyless scholarly graphs (250M+
  and 200M+ works with citation edges).

**Honest current features.** 15+ source adapters behind one isolated `Source`
shape (video captions, static web, RSS/Atom, local docs, arXiv by id or query,
local PDFs via pdftotext, authenticated JSON APIs with env-isolated credentials
never witnessed, JS-rendered pages via a real headless browser stamped
`browser-extract`, scanned images via OCR, audio via transcription). A durable
content-addressed corpus with hash-dedup of bodies and a streamed catalog;
recall/query by scope terms and source/kind/method filters; a witnessed
gather-run; a deterministic scope filter that records how many items it dropped;
a source-federation registry with offline capture-planning, a retry/backoff
policy compiler, and an entity-resolution receipt keyed on named identifier
paths (ror, openalex-id) that refuses fuzzy-name promotions; availability
re-verification with typed outcomes. Zero third-party runtime deps in core,
Python 3.11+, native MCP tools.

**Standout features to ship.**

1. **Scholarly-graph federation adapter** (OpenAlex + Semantic Scholar +
   Crossref) with citation-edge capture. *Buildable now.* Turns gather from a
   per-URL fetcher into a coverage tool, lands on the ror/openalex-id identifier
   paths the entity-resolution receipt already speaks, and gives Undermind-class
   reach with a provenance receipt on every retrieved work.
2. **High-fidelity layout-aware document parsing** (tables, multi-column,
   figures) as an upgraded PDF/browser path. *Buildable now.* Preserves table
   cells and reading order and records the extractor and its fidelity in the
   receipt, so the parse is both trustworthy and re-verifiable.
3. **Structured extraction-to-table over a corpus** (define columns, populate
   across N sources, each cell provenance-linked). *Buildable now.* This is
   Elicit's killer feature, but every cell is a re-checkable pointer to the
   exact source item and hash, so a review is reproducible.
4. **Cross-source dedup and entity resolution** across the whole corpus (same
   paper via DOI/arXiv/OpenAlex, same person/org). *Buildable now.* Promotes the
   existing identifier-path receipt into an active corpus-wide resolver,
   exact-id joins only, fuzzy refused, every merge sealed.
5. **Incremental corpus indexing and watch mode** (capture only deltas).
   *Buildable now.* Corpus index is gather's own listed future work; a watch
   mode re-probes federated sources and captures only new/changed items, each
   delta a receipt.
6. **Evidence-synthesis digest with per-claim provenance** (a Consensus-Meter-
   style answer where every supporting/contradicting item is a receipt).
   *Buildable now.* Reuses the existing witnessed-digest and derive seam.

**Compounding moat.** gather is the only place in the category where reach,
coverage, extraction, and synthesis are each born re-verifiable. Competitors
bolt provenance on after the fact (a citation link you must trust); gather makes
the receipt the substrate every feature is built from. Federation gives
OpenAlex-class coverage with an auditable hash on every work; parsing gives
Docling-class extraction with the extractor recorded; extraction-to-table
matches Elicit with reproducible cells; dedup stays exact-id-only and sealed;
synthesis matches the Consensus Meter with every item openable. Copying the
whole stack means rebuilding on a receipt substrate.

**Honest gaps.** gather is currently intake plumbing with excellent provenance,
not yet a best-in-class research tool on raw features. Coverage is thin (arXiv
only, no scholarly graph, no citation edges). Parsing fidelity is weak
(pdftotext, no table structure). No extraction UX. Dedup is exact-hash only.
No synthesis quality beyond verbatim compile. Recall reads every body and does
not scale; corpus indexing is unshipped. The browser adapter's host guard
covers only the first navigation, so its gated/JS reach is real but not safe to
point at untrusted URLs. None of these are overclaimed in the README, which is
to the project's credit.

---

### 2.2 index (PyPI index-graph 2.8.0; repo c:/dev/public/index)

**Category and user.** Workspace and codebase intelligence: dependency mapping,
code navigation, auto-generated repo docs, and context packs for agents. The
user is anyone handed a codebase or multi-repo workspace they did not write (new
maintainers, reviewers, onboarding leads, diligence teams) and the AI agents
that route work over that code and need trustworthy structural context.

**Competitors and what wins them users.**

- **Sourcegraph** wins on SCIP-based precise code navigation: symbol-granularity
  go-to-definition, find-references, find-implementations across repos.
- **DeepWiki** wins on zero-effort conversational repo understanding (replace
  github.com with deepwiki.com, get architecture diagrams and grounded chat).
- **Cody** wins on whole-codebase-aware AI answers and edits on large monorepos.
- **repomix** wins on one-command AI-friendly repo packs with token counts and
  a Tree-sitter `--compress` mode.
- **context7** wins on up-to-date, version-specific library docs injected via
  MCP, killing hallucinated APIs.
- **SCIP / ctags** are the symbol-index substrate everything above builds on.

**Honest current features.** index atlas (a two-layer interactive HTML map of
code and knowledge on one pannable canvas). A 9-ecosystem dependency graph
(Python exact from the AST; 8 others best-effort) where every edge carries a
file:line witness and a confidence grade. index wiki (multi-page self-contained
single-repo wiki, no prose, no model calls). index serve (loopback, consent-
clean on-demand wiki server). index internals (intra-repo module graph with
cycles and fan-in/out). context envelopes and context packs (budgeted, source-
ref-hashed). index select (typed path selection). architecture certificates (CI
gate), drift, freshness, typed invalidation. Token-economics bench. MCP-native
server. Offline, deterministic, zero runtime dependencies, private-by-default.

**Standout features to ship.**

1. **Symbol-graph navigation** (go-to-definition, find-references, find-
   implementations at symbol granularity, cross-file and cross-repo, each hop
   carrying file:line evidence). *Buildable now.* The single feature Sourcegraph
   wins on; index resolves module and repo edges but not symbol edges. Adding it
   keeps the evidence-and-recheck discipline no code-nav tool offers.
2. **Grounded, extractive codebase Q&A** (answer natural-language questions
   purely from the graph, returning file:line spans with a MATCH/DRIFT recheck,
   never generated prose). *Buildable now.* Same interface as DeepWiki/Cody with
   the opposite (non-fabricating) failure mode.
3. **Token-budgeted source pack with structural compression** (a repomix-class
   bundle ordered and trimmed BY the dependency graph, with a signed manifest).
   *Buildable now.* index already computes fan-in/out and the token bench, so it
   packs the right files and proves what it dropped.
4. **Live external-dependency docs and version pinning** (resolve imports to
   installed/locked versions, surface local package docs inline, flag manifest-
   vs-installed drift). *Buildable now.* context7's anti-hallucination benefit
   with zero network and a freshness verdict.
5. **Persistent, shareable, self-updating workspace surface** (a hosted-optional
   multi-repo atlas/wiki that regenerates deterministically on each push with a
   visible freshness/drift badge and a diff view). *Buildable now.* The
   shareability DeepWiki/Sourcegraph have plus the freshness proof they lack.
6. **Change-impact and blast-radius view** (given a changed file or PR diff, show
   which modules, repos, docs, certificates, and context packs are affected
   downstream, ranked by dependency distance). *Buildable now.* Reuses typed
   invalidation and the cross-repo edge graph; turns the map into a decision
   tool.

**Compounding moat.** Every feature derives from one offline, deterministic,
file:line-witnessed graph, and every output carries the same
MATCH/DRIFT/UNVERIFIABLE recheck. Symbol navigation cites evidence Sourcegraph
shows but cannot let you re-verify; the Q&A has the opposite failure mode from
DeepWiki with a verdict attached; the pack is graph-ranked with a signed
manifest; freshness and blast-radius are only possible because the map is a
re-checkable certificate. A competitor can bolt receipts onto an LLM wiki but
cannot make an LLM stop hallucinating; index started from the graph, so
accountability is native. All zero-dependency, offline, private-by-default,
which network-bound leaders cannot match for regulated or air-gapped teams.

**Honest gaps.** No symbol-level navigation today. No natural-language Q&A at
all. No cross-repo semantic or symbol code search. Best-effort parsing outside
Python for the other 8 ecosystems, below SCIP-grade. One-shot HTML artifacts, no
persistent hosted surface (index serve is loopback-only by design). No token-
budgeted source pack competing with repomix's `--compress`. No live external-
library docs surface. On scale: DeepWiki cites 50k+ repos and 4B+ lines indexed;
index has no comparable public traction, and its verified-wiki wedge, while
architecturally differentiated, is unproven against real large repos at volume.

---

### 2.3 forum (PyPI forum-engine 1.12.0; repo c:/dev/public/forum)

**Category and user.** Multi-agent orchestration and durable agentic workflow
engine. The user is a developer or platform/ML engineer running a fleet of LLM
agents for real work (clinical intake, newsroom fact-check, due-diligence,
research pipelines, token-budget-bound loops) who needs the route the agents
took to be an inspectable, resumable, provable artifact. Secondary: compliance-
sensitive enterprises where a verifiable record is a hard requirement, and self-
hosters who want to orchestrate their own subscriptions and local models.

**Competitors and what wins them users.**

- **LangGraph** wins on durable checkpointing with time-travel plus native
  human-in-the-loop pause/resume (Klarna, Uber, LinkedIn in production).
- **n8n** wins on a visual drag-and-drop builder with 500+ integrations and 70+
  AI nodes, usable by non-engineers.
- **OpenAI Agents SDK** wins on a built-in tracing dashboard plus first-class
  handoffs, guardrails, and sessions.
- **Temporal** wins on durable execution: crash-replay of event history to
  resume exactly where it left off.
- **Inngest** wins on durability/observability as library primitives with
  retry-from-failure.
- **CrewAI** wins on role-based crews with parallel delegation.
- **AutoGen / Microsoft Agent Framework** wins on conversational multi-agent
  patterns (GroupChat), now in maintenance mode folded into the broader
  framework.

**Honest current features.** Model-agnostic execution behind one seam (any
command/CLI, any OpenAI-compatible server, or the Anthropic API). Tiered
execution by roster tier. A DAG planner compiling a task graph into parallel
waves with bounded concurrency, cycle/missing-dep detection, and typed data
edges. RunBudget and ContextBudget cost/safety caps. Wave checkpoints and resume
from the ledger. Three surfaces from one core (CLI, HTTP daemon, MCP). Context
capsules and `context preflight`. Deterministic delivery floor plus expert
delivery profiles. Run rooms. Witnessed model-tier escalation. A deterministic
route-frame contract. Zero third-party runtime deps, self-hosted, all on a
hash-chained, content-addressed, replayable causal ledger with deep tamper
detection.

**Standout features to ship.**

1. **First-class human-in-the-loop: durable pause / approve / edit / resume
   gates.** *Buildable now.* LangGraph's headline production feature; forum
   already has wave checkpoints and resume, so this exposes them as an approval
   gate where the approval itself becomes a hash-chained, replayable ledger
   entry, strictly stronger than a trusted audit log.
2. **A visual ledger-replay and run-room dashboard.** *Buildable now.* Extends
   the existing static demo HTML into a live read-only surface rendering the DAG,
   wave progress, per-task cost/tokens, verdicts, and a scrub-to-any-state replay
   that mutable-log trace viewers structurally cannot reproduce.
3. **An integrations / connector catalog with a witnessed tool-call seam.**
   *Buildable now.* Start with HTTP/DB/filesystem/shell-sandboxed/MCP-client
   connectors (zero-dep constraint, not 500 branded ones); every tool invocation
   and result becomes a first-class witnessed ledger entry with a side-effect
   class, making the exact failure class competitors' APM cannot see into a
   replayable record.
4. **A built-in eval and regression harness.** *Buildable now.* Extends
   `forum bench` with a suite runner scored by the existing intent-judge and
   delivery floors plus optional LLM-as-judge; every eval run witnessed, so an
   improvement is proven from the record.
5. **OpenTelemetry / OTLP trace export from the ledger.** *Buildable now.* Emit
   GenAI-semantic-convention spans derived deterministically from the ledger, so
   forum drops into an existing LangSmith/Langfuse/Arize/Datadog stack as a
   provably-faithful source of truth.
6. **Named agent handoffs with a witnessed transfer contract.** *Buildable now.*
   The core pattern in the OpenAI Agents SDK, CrewAI, and AutoGen; a witnessed
   handoff makes forum the only engine where a delegation is a scope-checked,
   replayable record the lane gate can refuse to over-route.

**Compounding moat.** The differentiator is a hash-chained, content-addressed,
replayable causal ledger with deep tamper detection (verify(deep=True) catches a
swapped result; Merkle checkpoint avoids CVE-2012-2459). Every competitor treats
the record as a side effect you trust; forum treats the record as the work you
check. Each feature inherits proof for free: a HITL approval is provable, a tool
call is a witnessed side effect, an eval result is proven from the record, a
handoff is scope-checked, an OTel export is provably faithful, the dashboard
visualizes a scrub-to-any-past-state replay. To match the pair a competitor
would re-architect their engine so the record is the primitive, which
LangGraph/CrewAI/Temporal/n8n did not build for.

**Honest gaps.** No HITL approval gate ships today. No visual UI beyond a static
demo page. No integrations/connector catalog and no witnessed tool-call seam
(n8n ships 500+; forum ships zero). No eval/regression harness beyond
`forum bench` A/B. No OpenTelemetry export. No named-agent handoff primitive.
Maturity and adoption: a single-author fair-source project at 1.12.0 with no
cited production deployments, versus LangGraph's Klarna/Uber/LinkedIn footprint
and Temporal's enterprise base. The roadmap-vs-shipped line in the README must
stay honest: the dashboard, platform execution rooms, and code-readability
contract are not shipped.

---

### 2.4 crucible (PyPI crucible-bench 1.1.0; repo c:/dev/public/crucible)

**Category and user.** LLM and AI-agent evaluation and claim-checking. The user
is an AI engineer, ML/eval lead, agent developer, or research scientist who
needs to decide whether a claim, a model output, or an eval result actually
holds before shipping or publishing. Adjacent: safety/red-team teams, agent-ops
running regression gates in CI, and researchers who need a verdict that survives
peer review. crucible sits in the eval and judgment layer of the roadmap spine.

**Competitors and what wins them users.**

- **LangSmith** wins on end-to-end eval UX fused with tracing (versioned
  datasets, offline+online evaluators, side-by-side comparison dashboards).
- **Braintrust** wins on a browser Playground plus CI/CD regression tracking (a
  GitHub Action posts which cases improved or regressed on every PR).
- **Langfuse** wins on best-in-class open-source self-hostable tracing with
  accurate token/cost tracking and annotation queues.
- **Arize Phoenix / AX** wins on OpenTelemetry-native tracing plus drift and
  hallucination monitoring at production scale.
- **promptfoo** (OpenAI, Mar 2026) wins on declarative YAML evals plus automated
  red-teaming across 50+ vulnerability types.
- **Ragas** wins as the sharpest RAG-specific metric set (faithfulness, answer
  relevance, context precision/recall).

**Honest current features.** One-command operator runs (`crucible run` ties
steelman -> measure -> assess -> recheck into one session and writes a self-
contained review packet). Batch manifests. A content-addressed registry with
stats/search/prune and recall. Drift tracking across rounds (held/moved/improved/
regressed). Deterministic Markdown assessment reports. A refine loop with
harmonic-mean cohesion. Missing-evidence explanations (every UNVERIFIABLE claim
gets a typed row naming the missing evidence class). Pre-assessment measurement
validation with `--strict`. Pluggable measure/steelman seams including
subprocess oracle adapters and interop measures for Telos/Gather/index. A
creative measurement-gate returning allow/require_review/block. A native MCP
bridge. Publication-gated export.

**Standout features to ship.**

1. **A hosted or local-server eval dashboard with side-by-side experiment
   comparison** (a verdict matrix, a MATCH<->DRIFT<->UNVERIFIABLE diff view,
   margin trend lines, a filterable registry browser, every cell linking to its
   re-derivable packet). *Buildable now.* Comparison dashboards are the most-
   cited reason users choose LangSmith and Braintrust; crucible already computes
   the data and has no eyes.
2. **A versioned dataset / test-suite store with a fixture-pack format** (register
   a reusable suite of theses/claims/falsification-conditions/expected-
   measurements, run it repeatedly, pin a baseline; ship starter packs). *Buildable
   now.* Table stakes across every leader; the registry is already content-
   addressed so datasets get seals for free.
3. **A native CI regression gate that posts a PR comment** (`crucible ci` runs a
   dataset against a baseline and emits a diff comment with a fail-closed exit
   code and a ready GitHub Action). *Buildable now.* Braintrust's headline
   adoption driver; the gate is a pure function of recorded measurements, so a
   green check is re-derivable.
4. **A calibrated LLM-as-judge scorer demoted to proposer, never decider, with an
   inter-run agreement report.** *Buildable now.* 2026 research shows judges flip
   the same rubric roughly 30 percent of the time at temperature 1; crucible
   gives the familiar judge UX while quantifying and fencing the unreliability,
   surfacing disagreement as UNVERIFIABLE rather than a silent average.
5. **A human review and annotation queue that calibrates the oracle, not
   overrides it** (a reviewer supplies a measurement or a falsification
   observation, not a raw verdict, which feeds the pure verdict function and
   re-seals the assessment). *Buildable now.* Keeps the integrity guarantee
   intact while matching LangSmith/Langfuse annotation queues.
6. **A RAG and agent-trace evaluation adapter** (ingest a RAG answer with its
   retrieved context or an agent tool-call trace and auto-register claims with
   measurable falsification conditions, bound to deterministic measures where
   possible). *Buildable now.* Meets the two highest-volume eval workloads where
   the data already is.

**Compounding moat.** crucible is the only tool where the verdict is a pure
function of a recorded measurement, with no model in the verdict step, so it
re-derives from the stored record and UNVERIFIABLE is fail-closed. Layer the six
features on top and it becomes structural: the dashboard shows re-derivable
diffs; the CI gate's green check re-runs identically where a non-deterministic
judge cannot; datasets carry content-address seals; the judge is demoted and its
unreliability measured; human review feeds evidence into the pure verdict
function. Retrofitting a model-free, re-derivable verdict step would invalidate
the LLM-as-judge score history competitors' platforms are built on.

**Honest gaps.** No UI beyond a static example HTML file. No versioned dataset
store or curated packs (users hand-author each thesis). No CI-native PR-comment
flow. No LLM-as-judge scorer library, so out of the box crucible measures nothing
(UNVERIFIABLE) unless the user brings a substrate. No RAG-specific or agent-trace
ingestion. No human annotation queue. No production/online drift over live
traffic. A dogfood caveat (from operator memory, 2026-07-01, moderate confidence,
not re-verified this session): in the current registry 872/875 deviations are
author-supplied 0.0 and refutations never execute, so the shipped 100 percent
MATCH rate is partly theatrical. The verdict function is honest, but the tool
cannot yet make a measurement FAIL on its own, which must be fixed before the CI
gate and RAG adapter are trustworthy as real measurement.

---

### 2.5 telos / Studio (repo c:/dev/public/telos + studio-engine + site studio.html)

**Category and user.** AI-native creative-verification workspace: a live,
browser-first surface where a person and a model look at the same artifact (a
shader field, an orbit sim, a sound graph, a render), generate and steer it
together, then verify it against an external criterion. The user is a builder-
who-must-show-their-work: shader/graphics artists, notebook-driven researchers
and physicists, ML/agent engineers prototyping model-in-the-loop pipelines, and
technical educators. They currently split across Shadertoy, ComfyUI,
Observable/Jupyter, HF Spaces, and Canvas/Artifacts.

**Competitors and what wins them users.**

- **Cursor / Windsurf** win on model-in-the-loop as the core interaction (per-
  task model switching, Windsurf Arena Mode, background agents).
- **ComfyUI** wins on visual node-graph authoring plus frictionless workflow
  portability (JSON/PNG-embedded recipes, 60,000+ community nodes, App Mode).
- **Shadertoy / three.js** win on zero-install browser live-coding with instant
  feedback and a fork-and-remix community.
- **Hugging Face Spaces** win on one-push deploy of an interactive demo to a
  public, cloneable URL.
- **ChatGPT Canvas / Claude Artifacts** win on a live preview pane beside the
  chat with targeted inline edits.
- **Observable / Jupyter** win on reactive literate computing where the working
  surface is the shareable document.

**Honest current features.** A real generative engine (9 domains, 11 techniques,
10-11 named generators, each a closed-form strand expression). A single
expression-algebra substrate (one frozen AST is the single source every backend
derives from; AST -> emit GLSL -> parse -> AST' matches to 1e-6). Multi-backend
emission (WebGL shaders, a portable Web-Audio synth graph, a first-class time
axis with a witnessed motion Timeline). A renderer capability contract with a
real fallback ladder (WebGPU -> WebGL2 -> Canvas2D -> static). A live browser
Studio surface with the First Integral showcase (SEED -> MOTION -> LAW ->
WITNESS, a Kepler orbit integrated live and a conserved invariant recovered on
screen, reduced-motion aware). Determinism (seed/generator/scheme fully
determine a World with a stable id and sha256). Interactive cross-examine plus a
local HTTP API and a handoff package.

**Standout features to ship.**

1. **Model-in-the-loop live generation, in the browser, with the model as a
   first-class collaborator** (type or speak an intent, the model edits the strand
   expression, canvas + sound + timeline update live; an Arena-style split where
   two proposals render side by side and WITNESS certifies the kept one).
   *Buildable now.* The single biggest reason a user would choose Studio over a
   static demo, and it closes the gap between the site copy and the shipped
   interaction.
2. **Fork-and-remix shareable Worlds via a self-contained receipt URL** (a share
   link or PNG-embedded receipt that reopens the exact live World, plus a public
   gallery). *Buildable now.* Determinism means a share link is a re-runnable,
   re-verifiable artifact, strictly stronger than a Shadertoy fork.
3. **One-click publish of a World to a live, embeddable, standalone page** (the
   reference-chamber already exists in handoff/). *Buildable now.* HF-Spaces-class
   deploy with zero server dependency and the receipt inline.
4. **App Mode / parameter-surface** (expose chosen strand-expression inputs as
   labeled sliders/toggles/text so a non-authoring viewer can drive the World and
   the invariant re-checks as they drag). *Buildable now.* ComfyUI's App Mode
   reach; the strand expressions already have named, sampleable parameters.
5. **Visual node/graph authoring over the strand substrate** (wire generator,
   field-op, palette, sonify, and criterion nodes, compiling to one strand
   expression). *Later.* The compositor and organ library exist but a visual
   graph is a larger build.
6. **Cross-examine as a conversational, forkable timeline** (every steer recorded
   as a branchable step; walk back, fork, diff two branches and their verdicts).
   *Later.* Determinism plus the existing session cross-examine make it buildable
   but not first.

**Compounding moat.** The shareable, remixable, publishable, model-driven World
is the same object as its re-runnable receipt, because both derive from one
frozen strand expression (GLSL/audio/verify all from one source, matched to
1e-6). A fork inherits a live artifact and its proof and re-verifies on the
forker's machine; model-in-the-loop generation is bounded by a criterion the
model did not author, so "AI made this" comes with "and here is the check it
passed," exactly the trust gap frontier R&D audiences cannot get from Cursor- or
Canvas-class tools; determinism turns every user-created World into a compounding
re-checkable commons asset. Competitors can copy a node graph or an Arena split
in a quarter; they cannot cheaply retrofit a witnessed expression-algebra
substrate under an engine not built on one.

**Honest gaps.** No model-in-the-loop yet, which is the flagship's own
positioning, so the site copy is currently ahead of the shipped interaction. No
public gallery, share-link, or remix loop. No visual node-graph authoring. No
App-Mode parameter surface. The live Studio is narrow (one polished First
Integral showcase, not the general create-anything surface the generator set
implies). Renderer maturity is uneven (WebGPU splat/clustered is a selection/
fallback contract with prototype and static tiers, not a shipped high-end GPU
renderer, which the README states plainly). No real-time co-editing and no
cloud/GPU path (local, single-user, which is honest and a security virtue but
behind HF Spaces on reach and team tools on collaboration). None of these are
accountability gaps; they are the raw-feature gaps the directive calls out, and
closing standout features 1 through 4 is what moves Studio from a witnessed demo
to a top-choice workspace.

---

### 2.6 learn (npm @harperz9/learn 1.5.0; repo c:/dev/public/learn)

**Category and user.** Personal learning and study tool: the spaced-repetition,
retrieval-practice, AI-tutor category. The user is a serious self-learner or
credential-seeker (student, professional certifying, self-taught) who wants to
master material and prove the mastery is theirs, not the machine's. learn is
differentiated by refusing to auto-complete graded work and by emitting a re-
verifiable receipt separating what the engine did from what the human did.

**Competitors and what wins them users.**

- **Anki** wins on the FSRS scheduler (default since 23.10, trained on 700M+
  reviews) plus a massive shared-deck ecosystem.
- **RemNote** wins on note-taking and studying fused (one keystroke turns a
  bullet into a source-linked card, AI card generation from PDFs, a knowledge
  graph).
- **Mochi** wins on clean Markdown+LaTeX authoring with FSRS, image occlusion,
  and .apkg import.
- **NotebookLM** wins on source-grounded generation (auto flashcards and quizzes
  from your own documents with click-to-explain citations).
- **Khanmigo** wins on a Socratic tutor that refuses to hand over answers, which
  is why schools trust it.
- **Duolingo Max** wins on delight and engagement (adaptive Roleplay, streaks,
  polished mobile-first).

**Honest current features** (zero external deps, 240 tests). SM-2-lite/Leitner
scheduler. `tutor due` most-overdue-first review queue. Retrieval practice via
auto cloze-blanking of claims your own draft asserts, each carrying its source.
Predict-then-observe scoring with no silent pass on pending predictions. Self-
explanation grading that buckets your claims into grounded/shaky/unverifiable via
crucible. Misconception targeting ranked by your own wrong-attempt counts. A
concept map with topological learning path and prerequisite-gated readiness. A
`tutor study` orchestrator. Proof-packet lessons whose verdict equals the
packet's. A telos math_physics render bridge. A credential-logistics engine that
halts at every graded step. CLI plus a zero-dep advisory MCP server.

**Standout features to ship.**

1. **FSRS-class scheduler with per-learner optimization.** *Buildable now.* The
   entire serious-SRS category has standardized on FSRS (20-30 percent fewer
   reviews for equal retention); learn ships a generation-behind SM-2-lite. FSRS
   composes perfectly with the receipt: the schedule becomes a re-derivable
   function of recorded attempts.
2. **Source-grounded card and quiz generation from the learner's own material.**
   *Buildable now.* Extends the honest half (retrieval blanks claims the draft
   asserts) to ingest a document and emit cloze/QA cards each bound to a source
   span, with unverifiable extractions flagged rather than presented as fact.
3. **Image occlusion and rich card types** (LaTeX via the existing math_physics
   bridge, cloze, worked-example). *Buildable now.* Table stakes for medical/
   anatomy and STEM learners; learn is text/cloze only today.
4. **A real study UI (web/desktop) driving the same witnessed core.** *Buildable
   now.* Every leader wins on a fast keyboard-driven review surface; learn is CLI
   + MCP only, the largest adoption barrier. The receipt and reverify become
   first-class UI.
5. **Cross-device sync and shared/importable decks** (.apkg import plus a portable
   witnessed export and content-addressed sync of the hash-chained ledger).
   *Buildable now.* An Anki-ecosystem on-ramp plus tamper-evident synced state no
   competitor's sync provides.
6. **A Socratic self-explanation tutor loop that never hands over the answer.**
   *Buildable now.* learn already enforces the refusal harder than anyone (assess
   steps halt; mastery is a pure function of the learner's own scored attempts);
   promoting it to an interactive ask/hint/re-ask/grade loop that structurally
   cannot emit the graded answer turns the accountability floor into Khanmigo's
   headline feature, enforced by construction rather than policy.

**Compounding moat.** Competitors treat "does not cheat" as a policy promise or
ignore it; learn makes it structural (assess steps cannot auto-complete, mastery
is a pure function of scored attempts, the session emits a hash-chained receipt
that `tutor reverify` recomputes, with CHAIN_BROKEN / VERDICT_MISMATCH typed
failures and author-controlled booleans never gating). Each feature inherits the
floor: FSRS becomes re-derivable, generated cards carry source-span provenance,
synced decks are tamper-evident, the Socratic loop is the one tutor that
structurally cannot leak the answer. A competitor can copy any feature in a
sprint but cannot bolt witness-chained, halt-on-graded accountability onto an
architecture not built for it, which is exactly what a credential or a serious
learner needs when the mastery claim must survive scrutiny.

**Honest gaps.** Scheduler is a generation behind (SM-2-lite vs FSRS), the
biggest single gap and measurable. No AI/source card generation from arbitrary
PDFs. No image occlusion, limited card types (no native LaTeX rendering, no
worked-example type). No GUI at all, the largest adoption barrier. No cross-device
sync, no shared-deck ecosystem, no .apkg import. No gamification/engagement layer.
What learn already leads on is the accountability floor and zero-dependency
portability, which no listed competitor offers.

---

### 2.7 buildlang / buildc (crate buildlang on crates.io; repo HarperZ9/buildlang; public checkout c:/dev/public/pubscan/quantalang)

**Category and user.** Accountable scientific and systems runtime: a compiled
language for numerical, physics, and systems kernels that also emits re-checkable
proof receipts. The user is a scientific-computing or systems engineer who today
reaches for Julia, Mojo, Rust, Zig, Triton, JAX, or Chapel to write a fast
kernel and additionally needs the result reproducible, auditable, and capability-
gated (regulated/frontier R&D: physics sim, quant, embodied control, QEC, energy/
nuclear modeling). Accountability is the floor this user increasingly demands;
raw compute ergonomics and speed are still what makes them pick a language.

**Competitors and what wins them users.**

- **Julia** wins on the SciML ecosystem plus multiple dispatch (numerical
  batteries already there and interoperating at near-C speed).
- **Mojo** wins on one language for CPU and GPU kernels (MLIR, lowers to PTX/
  AMDGPU/Metal, Python-superset ergonomics).
- **Rust** wins on a sound borrow checker without a GC plus cargo/crates.io.
- **Zig** wins on comptime, drop-in C interop, and zero-config cross-compilation.
- **Triton** wins as the default kernel layer for PyTorch 2.x (torch.compile
  lowers to it).
- **JAX** wins on composable function transforms (grad, jit, vmap, pmap) with XLA.
- **Chapel** wins on language-level parallelism and distributed arrays for HPC.

**Honest current features** (verified against STATUS.md/README 2026-07-02). A
working compiler core (lexer to parser to Hindley-Milner inference with typed
algebraic effects to MIR to C backend to native executable) with an 8/8 semantic-
corpus C execution receipt and a large Rust test suite. Typed capability effects
(FileSystem, Network, Process, Environment, Clock, Gpu, Console, Foreign as first-
class declared effects, tracked through higher-order calls/closures/async, effect
laundering rejected). Julia-style static multiple dispatch with specificity and
ambiguity-as-error. Native C-ABI FFI both directions. Additive math syntax
(elementwise broadcast over fixed-size arrays with compile-time length checking,
a small linalg stdlib over dynamic Vec<f64>). HLSL/GLSL shader codegen. An LSP
server plus a VS Code extension. An operator CLI. An experimental opt-in
`#[linear]` no-cloning attribute (labeled not-yet-sound). An opt-in experimental
drop-insertion pass (default baseline still leaks, stated plainly).

**Standout features to ship.**

1. **Compile-time dimensional analysis** (first-class typed physical units
   enforced by the type checker; a unit mismatch is a compile error and units
   flow into the scientific-runtime receipt's measurement block). *Buildable now.*
   Julia (Unitful.jl), Rust (uom), and C++ (Boost.Units) offer units as
   libraries; none bind units into a re-checkable receipt. This is the single
   feature that turns BuildLang into the obvious accountable-science choice, and
   it extends the existing HM type system and the receipt's `units?` field.
2. **Effect-typed determinism and reproducibility as a language guarantee**
   (promote the receipt's already-computed determinism/seed/input facts into a
   first-class deterministic effect region so a kernel can be statically certified
   reproducible and re-run bit-stably). *Buildable now.* No competitor has a
   language-level deterministic-region certificate; it requires exactly the typed-
   effect substrate BuildLang already has.
3. **A real numerical standard library and a dynamic Matrix<T> / N-D array type**
   with BLAS-class linear algebra (matmul, solve, decompositions, FFT), broadcast
   over dynamic Vec, f32/f64 parity. *Buildable now.* Table stakes the leaders
   already clear; without real arrays no scientist writes a real kernel here
   regardless of receipts. This is the price of admission.
4. **A GPU compute backend that actually executes** (promote one experimental
   SPIR-V or LLVM path to a verified end-to-end compute target: dispatch a kernel,
   read results back). *Later.* GPU is the center of gravity for Mojo/Triton/JAX;
   the executing backend has to exist before the differentiated wedge (an
   executing kernel with a receipt) is real.
5. **A working package manager with a live registry and reproducible, receipt-
   sealed builds** (turn `buildc pkg` into a registry with content-addressed,
   digest-pinned dependencies). *Later.* cargo/crates.io is a top reason users
   pick Rust; the manifest/lockfile machinery exists but no registry does.
6. **Sound resource safety** (finish the `#[linear]` affine/borrow checker to a
   stated soundness boundary and make default heap memory management correct, drop
   insertion on by default). *Later.* Rust wins on a sound checker; BuildLang's is
   a best-effort lint with known-open holes and the default build leaks. This is
   the credibility floor for the safety claims already in the README.

**Compounding moat.** Capability effects, deterministic regions, and typed units
are all type-system facts; the scientific-runtime receipt is a sealed, re-runnable
witness of those facts. The type system that makes the kernel fast/safe is the
same type system that makes the receipt trustworthy. A units-typed, determinism-
certified value flows into a receipt a third party re-runs with `buildc receipt
verify` to re-derive the verdict, with a can-it-FAIL discipline (every invariant
ships a paired negative fixture, `--self-test` tampers the verifier). Julia, Mojo,
Zig, Triton, JAX, and Chapel would each have to retrofit a capability-effect
system, a determinism certificate, units-in-the-type-checker, and a re-execution-
based receipt-verify path onto a language whose type system was not built for it.

**Honest gaps.** No real numerical ecosystem (only the C backend works end-to-
end; SPIR-V/LLVM/WASM/Rust/x86-64/ARM64 are experimental or assembly-only with no
execution test; no Matrix type, no linear algebra, no FFT, no solvers, no autodiff;
broadcasting is elementwise over fixed-size arrays only, explicitly NOT Julia-
parity). No executing GPU path (emits shaders and untested SPIR-V, cannot dispatch
a compute kernel and read results back). No package ecosystem (manifest/lockfile
code but no live registry). Memory safety is not sound and default memory
management is incorrect (`#[linear]` is a best-effort lint; the default build
inserts no Drop terminators, so a 3-String program does 9 allocations and 0
frees). The receipt does not yet carry typed units (it seals a bare numeric series
with an optional free-text `units?` field and an author-declared numerical_method,
and honestly labels every receipt NOT_A_NEW_PHYSICAL_LAW). LSP is partial and not
end-to-end VS Code-verified; async and GC runtimes are designs not linked into
compiled programs; the self-hosted 244k-line .bld compiler cannot compile. The
license is Fair-Source (source-available, not open source), which narrows
community adoption relative to the permissively-licensed competitors.

---

### 2.8 emet (PyPI emet; MPL-2.0; repo c:/dev/public/emet)

**Category and user.** Content and artifact provenance / integrity witnessing, in
a specific sub-niche: inference-time source-to-view consistency for AI oversight.
The user is an engineer, reviewer, or oversight/red-team operator who needs to
prove that the bytes actually reaching a model (or a monitor, or a generated
report) still match the source they claim to represent. Distinct from build-time
provenance (who built this) and from statistical LLM observability (is quality
drifting): emet answers "is the view I am looking at faithful to the source on
disk, right now, re-derivable by anyone." Buyers: AI oversight teams, high-stakes-
domain reviewers (roadmap scope: cybernetics, biochem, nuclear, AI/ML, quant,
defense-adjacent), and release-diligence engineers.

**Competitors and what wins them users.**

- **C2PA / Content Credentials** wins on standard gravity (6,000+ members by Jan
  2026, native signing in OpenAI/Gemini/Chrome/Galaxy/Pixel) plus an EU AI Act
  transparency tailwind. Chosen because it is THE standard, not the best re-
  derivation tool.
- **Sigstore / Cosign** wins on keyless identity-based signing with transparency-
  log inclusion (46M signatures in 13 months), frictionless in CI/CD.
- **in-toto / SLSA** wins on a policy-driven attestation model enforced as a
  machine admission gate.
- **SynthID and cross-vendor watermarking** wins on invisible durable watermarks
  at internet scale (100B+ items by May 2026), needing no strippable side-channel
  metadata; its documented weakness (bypassable, editing-sensitive, only covers
  watermarked generators) is the trust-from-authority gap emet refuses.

**Honest current features.** Zero-dependency stdlib-only reference in Python plus
three more full implementations (Rust no-crates, Node built-in-modules-only, Go
stdlib-only), so it drops into any of four runtimes with no supply-chain footprint
of its own. A frozen normative v1.0 spec with a language-agnostic conformance
suite (35 vectors, all four impls green in CI on every push). A concrete command
surface beyond hashing: `anchor` (pin raw-byte hashes), `verify` (MATCH/DRIFT/
UNVERIFIABLE), `coherence` (is a presented view faithful to its source), `refuse`
(detect and strip in-band authority claims like TRUSTED/APPROVED/SAFE),
`corroborate` (read-path-diverse agreement), `audit` (recompute a tamper-evident
log chain). A machine-readable canonical `--json` envelope with stable exit codes.
A STRIDE threat model, an in-toto attestation adapter, and a proof-surface receipt
adapter. `refuse` and the coherence check are the two features no competitor has.

**Standout features to ship.**

1. **Stripped-credential recovery / rebind** (given naked bytes and a detached
   anchor set or a C2PA/sigstore attestation, re-establish MATCH without an intact
   embedded manifest). *Buildable now.* The defining failure of the whole category
   is intermediaries stripping embedded metadata; emet's trust-from-re-derivation
   model survives stripping by construction, so this is the feature users reach for
   after the standards fail in the wild.
2. **Detached, portable witness receipts with content-addressed bundles** (one
   JSON receipt recording exactly what source and view were compared, the verdict,
   the marker corpus version, and re-derivation instructions, verifiable by a
   stranger with only the bytes). *Buildable now.* Promotes the existing proof-
   surface adapter into a first-class release-readiness and diligence artifact.
3. **Interop verifiers for C2PA manifests, sigstore/Rekor entries, and in-toto/
   SLSA attestations** (ingest a signed claim, independently re-derive the
   underlying bytes, emit MATCH/DRIFT/UNVERIFIABLE against it). *Buildable now.*
   Turns every competitor into an input and positions emet as the neutral external
   re-checker that tells you when a signed claim no longer matches disk, which none
   of them do at inference time.
4. **Watch/daemon mode with continuous re-anchoring and DRIFT alerting**
   (re-verify anchored paths and stream DRIFT events with the stable exit-code/JSON
   contract). *Buildable now.* C2PA and cosign are one-shot; the AI-oversight
   failure is continuous and runtime, so a low-overhead watch mode makes emet a
   live oversight sensor.
5. **Independent, different-author conformance certification and a public
   conformance badge** (a hosted runner any third-party implementation submits to,
   plus a verifiable passing badge). *Later.* For a tool whose entire value is
   reproduction, third-party-verified conformance IS the flagship feature, but it
   depends on an external implementation emet does not yet have.
6. **IDE / CI native integrations** (a GitHub Action that runs `verify`/`coherence`
   and posts the receipt on a PR, a pre-commit hook, a review-surface lens).
   *Buildable now.* Sigstore's adoption came from frictionless pipeline placement,
   not cryptography; emet needs the same on-ramp.

**Compounding moat.** emet roots trust in re-derivation and deliberately refuses a
TRUSTED verdict, which is why `refuse` and the coherence check exist, where C2PA,
sigstore, and in-toto all root trust in authority. Every raw feature is a re-
derivation feature: rebind survives the exact intermediary-stripping that breaks
C2PA; the interop verifiers can neutrally re-check a signed claim because emet
claims no authority of its own; the watch daemon and portable receipts are
credible because anyone can independently re-run them. A competitor that copied
rebind or continuous re-checking would have to admit their signed claim can
silently diverge from disk, undercutting the authority their business rests on.
Cross-language conformance (four independent runtimes, one frozen spec) is the
durability layer under all of it.

**Honest gaps.** The core credibility gap is emet's own, admitted in its README:
all four implementations share one author, so the spec is demonstrably
IMPLEMENTABLE in four languages but not yet independently RE-DERIVABLE; SPEC
section 12's bar (a different-author implementation passing the 35 vectors) is
unmet, and v1.0.0 explicitly does not claim re-derivability is proven. No
ecosystem or standards gravity versus C2PA's 6,000+ members and sigstore's 46M+
signatures. No interop with the actual standards yet, so today it is a fifth silo
rather than the neutral re-checker on top. One-shot and CLI-only: no watch/daemon,
no GitHub Action, no pre-commit hook, no editor surface. Scope is deliberately
narrow (it never edits, signs, blocks, or grants permission), correct as a
principle but zero enforcement value on its own, so it must be paired with a gate
to be actionable. The proof-surface receipt and in-toto adapter live outside the
core and are not yet a portable, stranger-verifiable receipt format.

## 3. Feature Leadership Backlog (Prioritized)

The single highest-leverage buildable-now standout feature per flagship, ordered
by leverage across the constellation. Leverage is judged by: how directly it
closes the largest raw-feature gap against the category leader, how much it reuses
substrate already shipped, and how much it feeds the rest of the constellation
(roadmap megatool families).

| Rank | Flagship | First feature to build | One-line why |
| --- | --- | --- | --- |
| 1 | gather | Scholarly-graph federation adapter (OpenAlex + Semantic Scholar + Crossref) with citation edges | Coverage is the thinnest gap and gather is the intake front door for every other megatool; lands on identifier paths the entity receipt already speaks. |
| 2 | index | Symbol-graph navigation (go-to-def / find-refs / find-impls with file:line evidence) | The one feature Sourcegraph wins on that index lacks, built on the graph index already computes, and it makes the atlas a tool people live in. |
| 3 | forum | First-class human-in-the-loop pause / approve / edit / resume gates | LangGraph's headline production win; forum already has checkpoints and resume, and the approval becomes a provable ledger entry no competitor can match. |
| 4 | crucible | Native CI regression gate that posts a PR comment (crucible ci + GitHub Action) | Braintrust's headline adoption driver; the `--strict` exit codes and drift classifier are most of the way there and the green check is re-derivable. |
| 5 | telos/Studio | Model-in-the-loop live generation in the browser | The flagship's own positioning and the single biggest reason to choose Studio over a static demo; closes the gap between site copy and shipped interaction. |
| 6 | learn | FSRS-class scheduler with per-learner optimization | The one axis power users judge SRS by; learn is a generation behind, and FSRS makes the schedule a re-derivable function of recorded attempts. |
| 7 | buildlang | Compile-time dimensional analysis (typed units flowing into the receipt) | The feature that makes BuildLang the obvious accountable-science choice; extends the existing HM type system and the receipt's units field, and no competitor binds units into a receipt. |
| 8 | emet | Stripped-credential rebind (re-establish MATCH from naked bytes) | The C2PA killer feature C2PA structurally cannot ship; emet's re-derivation model already survives metadata stripping, so this is the after-the-standards-fail feature users reach for. |

Ordering rationale. gather and index rank highest because they sit earliest in
the spine (source and context) and their features feed every downstream megatool.
forum and crucible follow because human-in-the-loop and CI gating are the two
features that most directly convert their engines from admired to adopted. Studio
ranks fifth because model-in-the-loop is the highest-value feature but is scoped
to one flagship's surface rather than the whole constellation. learn, buildlang,
and emet each rank by the same test: the highest-leverage buildable-now feature
that closes their single largest raw-feature gap. All eight are buildable now;
the later-tier features (Studio node graph and forkable timeline, buildlang GPU
backend, package registry, and sound resource safety, emet conformance
certification) are sequenced after these.

## 4. Integration With The Proof Lanes And Megatool Families

This addendum does not add a new spine. It changes what rides on the existing
spine from the roadmap:

```text
source -> context -> route -> action -> measurement -> verdict -> receipt -> paper/product
```

**The proof layer rides on the standout features, not instead of them.** Each
standout feature above is a raw-user-feature first and a proof-carrying feature
second, in that order. Concretely, mapping the priority backlog onto the
roadmap's megatool families:

- **Telos Research Workbench** (Gather, Index, Forum, Crucible, Telos, Learn):
  the top four backlog items (gather federation, index symbol navigation, forum
  HITL, crucible CI gate) are exactly the raw features that make this megatool
  usable by a real researcher, not just auditable. gather's federation adapter
  feeds the `ResearchClaim` registry with coverage; index's symbol navigation
  makes the workspace context legible; forum's HITL is the human gate the
  publication pipeline already assumes; crucible's CI gate is the promotion gate
  Phase 2 assigns crucible. The receipts are already planned; the features are
  what this addendum adds.

- **Build Scientific Runtime** (BuildLang/buildc, Crucible, Telos receipts):
  buildlang's typed-units feature (backlog rank 7) is the raw feature that makes
  the `buildlang-scientific-runtime-receipt/v0` export meaningful to a scientist.
  The roadmap already scopes exporting the receipt into Crucible; this addendum
  says the receipt is worth more when the value it seals is a units-typed,
  determinism-certified quantity, not a bare series.

- **Agent Action Proof Packets** (Telos action receipts, Forum, Index, Crucible,
  browser evidence): forum's witnessed tool-call seam (standout feature 3) and
  named handoffs (standout feature 6) are the raw features under the roadmap's
  "external-write action packet." The side-effect class the roadmap wants on the
  action receipt is exactly what forum's tool-call seam produces.

- **Learning Forge** (Gather, Learn, Index, Crucible, Telos): learn's FSRS
  scheduler and source-grounded card generation are the raw features that make a
  prooflesson a study tool a learner returns to, not just a verifiable object.

- **Creative and Measurement Engine** (studio-engine, reconcile, measurement
  layers): Studio's model-in-the-loop and shareable receipt-URL features are the
  raw features that make the witnessed Scene worth generating and worth sharing.

- **Corpus and Publication Control Plane** and the **proof/witnessing organs**
  (EMET, Proof Surface, Repo Proof Index): emet's interop verifiers and portable
  receipts are the raw features that let emet act as the roadmap's neutral
  external re-checker across C2PA/sigstore/in-toto, consistent with Phase 2's
  "bridged by receipts, not merged into a single authority-shaped product."

The compounding claim from Section 1 is the same claim the roadmap makes about
the proof spine, read from the other direction: the roadmap says every frontier
claim should be traceable from evidence to execution to verification; this
addendum says every flagship should first be the tool a user picks for its raw
features, and then that traceability makes the tool's output worth more than the
same output made anywhere else. Features get the flagship into the consideration
set; the proof-carrying substrate is why the artifacts it produces are worth more.
Neither half alone is the product.

## 5. Honest Posture

Carried from the roadmap's Decision Rules and Publication Gates, restated for this
document:

- **Every market claim here is a hypothesis** until backed by a comparison matrix
  (roadmap Gate 6). Competitor feature descriptions are dated 2026 secondary
  evidence at moderate-to-high confidence, not settled fact. Where this document
  says a competitor "wins users on X," read it as "the cited 2026 sources report X
  as the adoption driver," not as a measured claim about our own comparative
  standing.
- **No "best" claim appears without a stated comparison basis.** Where a flagship
  is called best-in-class-capable, it is a target the standout features are meant
  to reach, not a current-state assertion. Where a flagship is behind, Section 2
  says so in plain words in its Honest Gaps.
- **The dogfood caveats are labeled by confidence.** The crucible 100-percent-
  MATCH-is-partly-theatrical note is from operator memory (2026-07-01), moderate
  confidence, not re-verified this session, and it gates the crucible CI-gate
  feature until the verifier can make a measurement FAIL on its own.
- **The frontier-domain scope applies to features, not only to receipts.** The
  standout features are meant to serve frontier R&D users directly: gather's
  federation and parsing serve systematic reviewers and nuclear/energy source
  intake; index's symbol navigation and blast-radius serve diligence teams;
  forum's HITL and tool-call witnessing serve clinical and defense-adjacent
  agent pipelines; crucible's CI gate and RAG adapter serve AI/ML eval leads;
  buildlang's typed units serve physics, quant, and QEC kernel authors; Studio's
  model-in-the-loop serves physicists and ML engineers; emet's rebind and interop
  serve AI oversight and release diligence. None of these features may turn high-
  risk source material into operational instructions; the roadmap's Risk Gate and
  the private/internal boundary for raw or high-risk payloads stay in force.
- **Shipped versus planned stays separated.** Everything in Section 2's "honest
  current features" is shipped; everything in "standout features to ship" is not,
  and the buildable-now versus later marks are the honest sequencing. The README
  and site copy for each flagship must not describe a standout feature as shipped
  until it is.
