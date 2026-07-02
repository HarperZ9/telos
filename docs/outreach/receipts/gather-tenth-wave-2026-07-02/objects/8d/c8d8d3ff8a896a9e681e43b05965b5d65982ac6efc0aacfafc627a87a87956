# Proof-Carrying Source Federation for Biology, Medicine, and Robotics

Author: Project Telos

Date: 2026-07-02

Version: 0.1 official-copy working draft

Status: working paper draft

Evidence boundary: source federation only. This draft does not claim clinical truth, paper truth, exhaustive coverage, latest coverage, archive submission, acceptance, or promoted laws.

## Abstract

Biology, medicine, and robotics research increasingly combines source retrieval, foundation models, autonomous-science agents, workflow tools, and physical or clinical boundary conditions. The first publication problem for such systems is not how to make a larger autonomous researcher. It is how to prevent source capture from becoming a truth claim.

This paper proposes proof-carrying source federation: every source, model claim, action, measurement, and publication step carries an explicit evidence state. The ninth-wave Project Telos intake demonstrates the need for that discipline by preserving four arXiv source-lead stores, visible query-noise rows, duplicate rows, and missing-evidence boundaries. The result is a source-led working paper, not a biomedical finding, clinical recommendation, protein-design result, robotics-safety result, or official archive submission.

## Evidence-State Glossary

| Term | Meaning in this paper |
| --- | --- |
| `SOURCE_LEAD` | A captured source row, paper page, PDF link, or metadata record worth examining. It is not evidence that the source claim is true. |
| `HYPOTHESIS` | A plausible research or product direction with named missing evidence or falsifiers. |
| `PROBE_MATCH` | A bounded local inspection matched an expected local criterion, such as catalog row counts or visible query-noise classification. |
| `CRUCIBLE_MATCH` | A claim has been compared with a measurement packet by Crucible and returned a matching verdict. In this draft, this is scoped only to package-boundary claims, not biomedical, clinical, protein-design, robotics-safety, paper-truth, or grand-challenge claims. |
| `UNVERIFIABLE` | The current packet lacks enough evidence to establish the claim as scoped. |

## Claims Table

| Claim | Scope | Evidence state | Evidence reference | Missing evidence | Falsifier or demotion trigger |
| --- | --- | --- | --- | --- | --- |
| Telos captured four ninth-wave arXiv source-lead stores for bio, medicine, robotics, protein/systems biology, and AI-scientist-adjacent work. | Metadata/source receipt existence only. | `SOURCE_LEAD` | `docs/outreach/NINTH-WAVE-BIO-MED-ROBOTICS-SOURCE-FEDERATION-2026-07-02.md`; four `catalog.jsonl` files under `docs/outreach/receipts/ninth-wave/`. | Source-body reading, full-text claim extraction, independent relevance review. | Missing catalog files, failed store verification, or digest mismatch. |
| The retained catalogs contain 30 rows across the four stores. | Local JSONL row count. | `PROBE_MATCH` | Local catalog parse: biomed 8, robotics 7, protein 8, AI-scientist-biomed 7. | Any recheck count differs from the recorded counts. |
| The 30 retained rows collapse to 25 unique arXiv IDs because some rows appear in multiple lanes. | Local ID deduplication over the four catalogs. | `PROBE_MATCH` | Duplicate IDs observed: `1607.06358v2`, `2512.03307v1`, `2607.01063v1`, `2604.17070v2`. | A reparse finds a different duplicate set or unique count. |
| The source tranche contains both high-signal source leads and query-noise rows. | Manual title/category classification from the ninth-wave document and catalog metadata. | `PROBE_MATCH` | Query-noise section below. | Independent reviewer or automated classifier shows the listed noise rows are in-scope for the specific paper packet. |
| The source-lead demotion gate classified all 30 retained rows as 15 domain leads, 9 adjacent leads, and 6 query-noise rows. | Local demotion-gate receipt and coverage check only. | `PROBE_MATCH` | `docs/outreach/receipts/ninth-wave/source-lead-demotion-gate.json` | Missing row coverage, duplicate coverage, changed class counts, or absent coverage status. |
| Proof-carrying source federation is a useful publication discipline for high-stakes scientific domains. | Research-program thesis, not a measured market or domain-truth claim. | `HYPOTHESIS` | Prior proof-carrying research-loop draft plus ninth-wave source/noise split. | A stronger workflow shows source capture can safely promote claims without explicit evidence states. |
| Any biomedical, clinical, protein-design, or robotics-safety claim from these rows is established by this packet. | Domain truth. | `UNVERIFIABLE` | Only metadata/source-lead capture is present. | Requires source-body review, domain-specific evaluation, independent review, and, where relevant, clinical, wet-lab, simulation, or physical-world evidence. |
| Ninth-wave package-boundary claims reached `CRUCIBLE_MATCH` in Crucible v2. | Package-boundary claims only: store counts, demotion gate coverage, source/noise boundary, hard-problem boundary, and PubMed/Europe PMC adapter gap. | `CRUCIBLE_MATCH` | `docs/outreach/receipts/ninth-wave-tooling-run-v2-2026-07-02.json`; assessment seal `28f654ff9ab35789896f4f72de5b5e7cb1e48824772e74a66111db2e101cb5f2`. | Missing verdict file, non-`MATCH` status, seal mismatch, or use of the verdict to promote substantive domain truth. |
| This working paper is ready for official archive submission. | Publication readiness. | `UNVERIFIABLE` | The requested inputs identify missing claims table, methods, negative controls, recheck commands, and target archive package as needed work. This draft addresses format, not submission. | Archive package, review checklist, final source-body citations, and approval record are absent. |

## Methods

### Source Inputs Read For This Draft

The draft uses only the requested local inputs:

- `docs/outreach/NINTH-WAVE-BIO-MED-ROBOTICS-SOURCE-FEDERATION-2026-07-02.md`
- `docs/research/whitepapers/PROOF-CARRYING-RESEARCH-LOOPS-2026-07-02.md`
- `docs/research/whitepapers/OFFICIAL-PAPER-REVISION-QUEUE-2026-07-02.md`
- `docs/outreach/receipts/ninth-wave/arxiv-biomed-foundation/catalog.jsonl`
- `docs/outreach/receipts/ninth-wave/arxiv-robotics-lab/catalog.jsonl`
- `docs/outreach/receipts/ninth-wave/arxiv-protein-design/catalog.jsonl`
- `docs/outreach/receipts/ninth-wave/arxiv-ai-scientist-biomed/catalog.jsonl`

### Gather Intake Evidence

The intake used Gather's arXiv lane, and the catalogs record `method: arxiv-api-search`. The historical commands for this pass were:

```powershell
gather arxiv "biomedical foundation models medicine clinical biology 2026" --max-results 8 --scope "biomedical,medicine,clinical,biology,foundation,model,AI" --json --store docs\outreach\receipts\ninth-wave\arxiv-biomed-foundation
gather arxiv "robotics foundation models embodied AI laboratory automation 2026" --max-results 8 --scope "robotics,embodied,laboratory,automation,foundation,model,AI" --json --store docs\outreach\receipts\ninth-wave\arxiv-robotics-lab
gather arxiv "protein design generative model biology medicine 2026" --max-results 8 --scope "protein,design,generative,biology,medicine,model" --json --store docs\outreach\receipts\ninth-wave\arxiv-protein-design
gather arxiv "AI scientist biology medical research automation 2026" --max-results 8 --scope "AI,scientist,biology,medical,research,automation" --json --store docs\outreach\receipts\ninth-wave\arxiv-ai-scientist-biomed
```

Recorded catalog method:

```text
arxiv-api-search
```

### Source-Lead Demotion Gate

The demotion gate records every retained source row exactly once and classifies it as `domain_lead`, `adjacent_lead`, or `query_noise`. It is a manual metadata triage receipt, not an automated domain classifier and not a source-body review.

```powershell
Get-Content docs/outreach/receipts/ninth-wave/source-lead-demotion-gate.json | ConvertFrom-Json
```

Store verification commands to run after intake:

```powershell
gather corpus verify docs/outreach/receipts/ninth-wave/arxiv-biomed-foundation --json
gather corpus verify docs/outreach/receipts/ninth-wave/arxiv-robotics-lab --json
gather corpus verify docs/outreach/receipts/ninth-wave/arxiv-protein-design --json
gather corpus verify docs/outreach/receipts/ninth-wave/arxiv-ai-scientist-biomed --json
```

The recorded class counts are 15 `domain_lead`, 9 `adjacent_lead`, and 6 `query_noise`. Any future paper revision that promotes a row from this tranche must cite source-body review, not only the demotion class.

### Catalog Inspection

The local catalog probe used the four JSONL files as source receipts. Each row was treated as a `SOURCE_LEAD`; row counts, duplicate IDs, and visible lane fit were treated as bounded `PROBE_MATCH` checks. No catalog row was treated as proof of the underlying paper's claims.

## Source Intake Receipts

| Lane | Store | Retained rows | Dropped rows reported by summary | Digest seal | State |
| --- | --- | ---: | ---: | --- | --- |
| Biomedical foundation models | `docs/outreach/receipts/ninth-wave/arxiv-biomed-foundation` | 8 | 0 | `d3fe14ba9368def788557a3268fde724a605cf87a5df060af87f79c42362fbe6` | `SOURCE_LEAD` |
| Robotics and lab automation | `docs/outreach/receipts/ninth-wave/arxiv-robotics-lab` | 7 | 1 | `e5ae3b8acd8cae740d9b678e148794dd94841742a5096cd480d37355adbc4516` | `SOURCE_LEAD` |
| Protein design and systems biology | `docs/outreach/receipts/ninth-wave/arxiv-protein-design` | 8 | 0 | `c1ab2439eef86c3db3e55600bf744bbd1f084fd0c9020eb6dd474dd20a2bd91c` | `SOURCE_LEAD` |
| AI-scientist automation, biomedical-adjacent | `docs/outreach/receipts/ninth-wave/arxiv-ai-scientist-biomed` | 7 | 1 | `eadd0ca7b25db20edf82d2827d03e090c9416279ad032656b8033f3870b0d829` | `SOURCE_LEAD` |

## Source Lead Table

These rows are source leads for future packets. Their titles and categories suggest relevance, but their paper bodies have not been read in this draft.

| Row | Lane | Why it is a source lead | Proposed packet | State |
| --- | --- | --- | --- | --- |
| `2504.21336v3` UniBiomed | Biomedical foundation | Grounded biomedical image interpretation needs provenance, model output boundary, measurement, and review separation. | Biomedical image interpretation proof packet. | `SOURCE_LEAD` |
| `2403.00868v3` SoftTiger | Biomedical foundation | Clinical workflow models need source provenance, action provenance, tool authority, and clinical-claim boundaries. | Clinical workflow action-receipt proof packet. | `SOURCE_LEAD` |
| `2605.10877v1` Neural at ArchEHR-QA 2026 | Biomedical foundation | EHR QA is a natural fit for retrieval provenance, answer-boundary labeling, and evidence-state promotion. | EHR QA evidence-state packet. | `SOURCE_LEAD` |
| `2203.13906v1` Biolink Model | Biomedical foundation | A biomedical knowledge-graph schema may support source graph joins and adapter design. | Biomed knowledge-graph source-ref adapter. | `SOURCE_LEAD` |
| `2602.02370v2` Uncertainty-Aware Image Classification | Biomedical foundation | Biomedical image uncertainty is relevant to measurement and confidence-boundary receipts. | Biomedical imaging uncertainty packet. | `SOURCE_LEAD` |
| `2505.20503v2` Embodied AI with Foundation Models | Robotics | Embodied foundation-model robotics needs environment receipts, action receipts, and simulator/physical-world separation. | Embodied AI action-receipt packet. | `SOURCE_LEAD` |
| `2511.23143v1` Automated Generation of MDPs | Robotics | LLM-to-MDP generation can be checked against formal model constraints and rollout evidence. | LLM-to-MDP verification packet. | `SOURCE_LEAD` |
| `2309.06611v3` Automated Containerization for Robotic Applications | Robotics | Deployment substrate claims can be separated from robot-performance claims. | Robotics deployment provenance packet. | `SOURCE_LEAD` |
| `2605.10653v1` Embodied AI in Action | Robotics | Safety, trust, and real-world deployment language needs strict evidence boundaries. | Robotics deployment boundary packet. | `SOURCE_LEAD` |
| `2504.06806v1` Mass Balance Approximation of Unfolding | Protein/systems biology | Protein stability prediction can be decomposed into source, model, physical invariant, benchmark, and uncertainty receipts. | Protein-stability invariant packet. | `SOURCE_LEAD` |
| `1607.06358v2` Bayesian uncertainty analysis for systems biology models | Protein/systems biology and biomedical lanes | Systems-biology uncertainty modeling is relevant to proof-carrying scientific workflows. | Systems-biology uncertainty packet. | `SOURCE_LEAD` |
| `2511.04583v4` Jr. AI Scientist and Its Risk Report | AI-scientist-adjacent | Autonomous scientific exploration is directly relevant to proof-carrying research loops and risk gating. | AI-scientist risk-boundary packet. | `SOURCE_LEAD` |

## Query-Noise And Demotion

The ninth-wave tranche intentionally preserves query noise. The demotion gate is part of the result: source federation should keep noisy rows visible while preventing them from becoming domain claims.

| Row | Noise or adjacency reason | Proper handling | State |
| --- | --- | --- | --- |
| `2607.01063v1` AutoRestTest at the SBFT 2026 Tool Competition | Software-testing row, not biology, medicine, protein design, or robotics from title/category alone. | Keep only as agent-tooling source lead unless a separate software-testing packet is opened. | `PROBE_MATCH` |
| `2604.17070v2` NTIRE 2026 Rip Current Detection and Segmentation | Vision challenge row, not biomedical or protein design from title/category alone. | Keep only if a visual-measurement benchmark packet needs it. | `PROBE_MATCH` |
| `2606.03948v1` IWSLT 2026 speech translation | Speech-translation row, not protein design from title/category alone. | Demote from protein lane. | `PROBE_MATCH` |
| `2603.22728v1` Interspeech 2026 Audio Encoder Capability Challenge | Audio benchmark row, not protein design from title/category alone. | Demote from protein lane. | `PROBE_MATCH` |
| `2604.11487v1` Robust AI-Generated Image Detection | AI safety / vision row, not biomedical from title/category alone. | Keep for provenance or safety lane only. | `PROBE_MATCH` |
| `2601.16513v1` Competing Visions of Ethical AI | Governance row, not biomedical or robotics source evidence. | Keep for policy lane only. | `PROBE_MATCH` |
| `2602.21012v1` International AI Safety Report 2026 | Safety-governance row, not biomedical domain evidence. | Keep for governance and risk-boundary packet only. | `PROBE_MATCH` |
| `2512.03307v1` Robust Tabular Foundation Models | General tabular-model row appearing in both biomed and robotics stores; relevance is not established by metadata alone. | Mark as adjacent until source-body review justifies a domain packet. | `SOURCE_LEAD` |
| `2606.29981v1` Hephaestus | Cybersecurity AI-scientist row, relevant to autonomous-research tooling but not biomedical truth. | Keep only in AI-scientist / tool-risk lane. | `SOURCE_LEAD` |

## Negative Controls

1. Query-noise rows are retained as negative controls for the promotion gate. A row can be captured, hashed, and visible without becoming a domain claim.
2. Duplicate IDs across stores are retained as a deduplication control. The same source may be relevant to multiple lanes, but counting rows is not the same as counting unique papers.
3. Metadata-only rows are retained as a source-body control. Title, category, DOI, PDF link, and SHA-256 metadata do not establish paper claims.
4. PubMed and Europe PMC are absent in this packet. The ninth-wave note says `gather api` currently requires `GATHER_API_TOKEN` in this environment, so arXiv should not be treated as adequate coverage for medicine.
5. No clinical, wet-lab, physical-robot, or simulator experiment is attached. Domain safety and efficacy remain `UNVERIFIABLE`.
6. Crucible v2 attaches only package-boundary claims. No substantive biomedical, clinical, protein-design, robotics-safety, paper-truth, or grand-challenge claim is `CRUCIBLE_MATCH`.

## Missing Evidence

- Source-body reading for each promoted row.
- Abstract/full-text claim extraction.
- Independent relevance classification.
- Automated domain/noise classifier with threshold and failure cases.
- PubMed, Europe PMC, clinical-guideline, standards, and dataset intake where appropriate.
- Biomedical expert review before any clinical-facing language.
- Protein-design benchmark or wet-lab evidence before any protein-design result.
- Robotics simulator or physical-world run receipts before any robotics-safety result.
- Domain-specific Crucible measurement packets and verdicts for any substantive claim proposed for `CRUCIBLE_MATCH`.
- Website-copy summary link and archive package review.
- Explicit revision log for official-paper release tracking.

## Recheck Commands

Run from `C:\dev\public\telos`.

Catalog row counts and recorded methods:

```powershell
$files = @(
  'docs/outreach/receipts/ninth-wave/arxiv-biomed-foundation/catalog.jsonl',
  'docs/outreach/receipts/ninth-wave/arxiv-robotics-lab/catalog.jsonl',
  'docs/outreach/receipts/ninth-wave/arxiv-protein-design/catalog.jsonl',
  'docs/outreach/receipts/ninth-wave/arxiv-ai-scientist-biomed/catalog.jsonl'
)
foreach ($f in $files) {
  $rows = Get-Content $f | ForEach-Object { $_ | ConvertFrom-Json }
  [pscustomobject]@{
    Path = $f
    Rows = @($rows).Count
    UniqueIds = @($rows.id | Select-Object -Unique).Count
    Methods = ($rows.method | Select-Object -Unique) -join ','
  }
}
```

Duplicate-ID probe:

```powershell
$files = @(
  'docs/outreach/receipts/ninth-wave/arxiv-biomed-foundation/catalog.jsonl',
  'docs/outreach/receipts/ninth-wave/arxiv-robotics-lab/catalog.jsonl',
  'docs/outreach/receipts/ninth-wave/arxiv-protein-design/catalog.jsonl',
  'docs/outreach/receipts/ninth-wave/arxiv-ai-scientist-biomed/catalog.jsonl'
)
$rows = foreach ($f in $files) {
  Get-Content $f | ForEach-Object {
    $o = $_ | ConvertFrom-Json
    [pscustomobject]@{ Id = $o.id; Title = $o.title; Store = $f }
  }
}
$rows | Group-Object Id | Where-Object Count -gt 1 | Select-Object Name,Count
```

Store verification:

```powershell
gather corpus verify docs/outreach/receipts/ninth-wave/arxiv-biomed-foundation --json
gather corpus verify docs/outreach/receipts/ninth-wave/arxiv-robotics-lab --json
gather corpus verify docs/outreach/receipts/ninth-wave/arxiv-protein-design --json
gather corpus verify docs/outreach/receipts/ninth-wave/arxiv-ai-scientist-biomed --json
```

Source-lead demotion gate parse:

```powershell
$gate = Get-Content docs/outreach/receipts/ninth-wave/source-lead-demotion-gate.json | ConvertFrom-Json
$gate.summary
$gate.rows | Group-Object classification | Select-Object Name,Count
```

Crucible v2 boundary receipt parse:

```powershell
$crucible = Get-Content docs/outreach/receipts/ninth-wave-tooling-run-v2-2026-07-02.json | ConvertFrom-Json
$crucible.assessment | Select-Object claims,match,drift,unverifiable,seal
$crucible.verdicts | Select-Object claim_id,status,method
```

Boundary-language scan for this draft:

```powershell
rg -n "clinical truth|paper truth|exhaustive|latest|official submission|PROMOTED_LAW|promoted law" docs/research/whitepapers/BIO-MED-ROBOTICS-SOURCE-FEDERATION-2026-07-02.md
```

The boundary scan is allowed to find the explicit non-claim boundary statements in this draft. It should not find affirmative promotion language.

## Publication Boundary

This is an official-copy working draft, not an official submission. It is suitable for internal review of paper structure, evidence-state vocabulary, source-lead tables, query-noise handling, and recheck commands.

The next revision may become a publication candidate only after source-body review, domain-specific evidence gaps are either filled or explicitly preserved, public website-copy boundaries are reviewed, and any substantive measured claims are run through domain-specific Crucible packets. Until then, the paper's publication state is `UNVERIFIABLE`.

## Revision Log

| Version | Date | Change | Evidence boundary |
| --- | --- | --- | --- |
| 0.1 | 2026-07-02 | Initial official-copy working draft for proof-carrying source federation. | Source federation only. |
| 0.1.1 | 2026-07-02 | Added historical Gather commands, source-lead demotion gate, scoped Crucible v2 boundary receipt, and explicit revision-log requirements. | Package-boundary `CRUCIBLE_MATCH`; substantive domain claims remain unverified. |

## Website-Copy Summary Link

No website-copy summary has been published from this draft yet. The current companion outreach file is `docs/outreach/NINTH-WAVE-CONTENT-QUEUE-2026-07-02.md`; any public website copy should preserve the same non-claim boundary.
