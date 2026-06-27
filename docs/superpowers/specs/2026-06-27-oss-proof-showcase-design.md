# Project Telos OSS Proof Showcase - Design Spec

Date: 2026-06-27
Status: draft for operator review
Home: `C:\dev\public\telos`
Scope: Telos-hosted showcase lane for `gather`, `crucible`, `index`, `forum`, and `telos`

## Objective

Build a public proof lane that demonstrates the five Project Telos flagships on real open-source work: find high-star repositories with open, current, fixable issues; capture the issue and repository evidence; map the codebase; route the work; verify the patch thesis; and emit a reviewable PR-readiness record.

This lane is a showcase, not an auto-PR bot. It should make high-quality external contributions easier and more repeatable, while keeping public communication and PR submission operator-gated.

## Current Evidence

These facts were checked from the local workspace and live GitHub data on 2026-06-27.

- Telos local room reports all five flagships ready: 5 ready of 5, 18 checks passed of 18, and 22 available protocol tools in `project-telos.mcp-tool-catalog/v1`. Confidence: high.
- The current five pushed commits are clean locally: Gather `b718500`, Crucible `cbae956` on `release/1.1.0`, Index `b282d26`, Forum `33a62db`, and Telos `c32c7ba`. Confidence: high.
- The Telos integration catalog already names CLI, MCP, OpenAI, Anthropic, Codex plugin, IDE, TUI, and app host surfaces under `demo/integrations`. Confidence: high.
- A live GitHub scan found large current repositories with active issue surfaces, including `pandas-dev/pandas`, `microsoft/vscode`, `huggingface/transformers`, `microsoft/playwright`, and `vercel/next.js`. Confidence: high.
- Sample candidate `pandas-dev/pandas#66050` is fresh and has a minimal reproduction for `pd.array()` dropping NumPy masked-array missing values. Confidence: high.
- Sample candidate `microsoft/vscode#323066` is fresh and has a concrete Node debug-console reproduction for `%j` formatting. Confidence: high.
- Sample candidate `huggingface/transformers#46897` includes code pointers and a related prior fix pattern for Florence2 training-loss double shifting. Confidence: high.
- Sample candidate `microsoft/playwright#41462` includes a reproduction for retained detached DOM nodes and a maintainer comment inviting investigation. Confidence: high.

## Design Principles

- The lane proves the tools by doing useful work against real upstream code, not by showing synthetic demos only.
- Each step must leave a receipt that can be read without hidden session state.
- Candidate discovery may be automated; public posting, PR creation, or maintainer communication stays operator-gated.
- The first implementation should be small enough to verify locally, then extensible to more repositories and languages.
- The workflow should be IO protocol agnostic: CLI JSON first, MCP callable where available, file receipts as the durable interchange format.
- The lane must not clone or publish private workspace data. External candidates live in isolated checkout folders outside the five flagship repos.

## Approaches Considered

### Approach A: Telos-hosted general lane, with one proving target first

Telos owns the candidate schema, scoring, run records, and showcase output. The first run uses one concrete target family, likely pandas, then the same workflow can scan TypeScript, JavaScript, Python, AI-model, and tooling repos.

This is the recommended approach. It gives the project one durable public-proof workflow without baking pandas-specific logic into the product surface.

### Approach B: One-off upstream patch first

Clone one repo, fix one issue, and document the result afterward.

This is fast, but it underuses the five-tool system and leaves no reusable showcase lane. It is useful once the lane exists, not as the architecture.

### Approach C: Full multi-repo automation first

Build broad discovery, ranking, cloning, patching, and reporting across many ecosystems before attempting a patch.

This looks ambitious but has too much blast radius. It risks optimizing for search breadth before proving that a single candidate can move cleanly from issue to local patch evidence.

## Product Shape

The OSS Proof Showcase is a Telos lane with four operator-facing commands or command-equivalent surfaces:

1. `showcase scout`: query current public issue surfaces and write candidate receipts.
2. `showcase brief`: gather one candidate into a compact evidence brief.
3. `showcase assess`: score patchability and risk using gathered evidence, repository structure, and a falsifiable patch thesis.
4. `showcase record`: write the final PR-readiness packet after local reproduction, patch, and tests exist.

The implementation may expose these as Node demo commands first, then add MCP tools after the file contract is stable.

## Roles By Flagship

`gather` captures issue evidence.

- Inputs: GitHub issue URL, issue body, labels, comments, repository metadata, maintainer signals, linked issues or PRs.
- Outputs: source receipts with fetched-at timestamps, URLs, issue numbers, labels, and content digests.
- Failure mode: if GitHub data cannot be fetched, the candidate is `UNVERIFIABLE`, not silently skipped.

`index` maps the target repository.

- Inputs: isolated clone path, target issue keywords, likely language and test framework hints.
- Outputs: repo map, context pack, likely modules, likely tests, package commands, and dependency surface.
- Failure mode: if the repository is too large or unsupported, emit a bounded map with explicit omissions.

`forum` routes the candidate.

- Inputs: candidate brief, issue labels, language, repository shape, and requested action.
- Outputs: lane decision such as `python-dataframe`, `typescript-debugger`, `model-library`, `browser-automation`, `docs-only`, or `needs-human-triage`.
- Failure mode: low confidence becomes a first-class route result with next actions.

`crucible` verifies the patch thesis.

- Inputs: reproduction claim, proposed fix claim, local test commands, observed before and after results.
- Outputs: `MATCH`, `DRIFT`, or `UNVERIFIABLE` assessment with exact evidence references.
- Failure mode: unverifiable reproduction blocks PR-readiness, but still produces a useful research record.

`telos` reconciles the showcase.

- Inputs: all prior receipts plus local git diff metadata and test summaries.
- Outputs: PR-readiness packet with candidate score, evidence, patch thesis, tests, risks, and operator next actions.
- Failure mode: if any upstream, local, or test evidence is missing, record the missing piece instead of producing a public-ready packet.

## Candidate Schema

Every candidate record should be JSON and file-backed.

```json
{
  "schema": "project-telos.oss-candidate/v1",
  "captured_at": "2026-06-27T00:00:00Z",
  "repository": {
    "full_name": "pandas-dev/pandas",
    "url": "https://github.com/pandas-dev/pandas",
    "stars": 0,
    "language": "Python",
    "open_issues": 0
  },
  "issue": {
    "number": 66050,
    "url": "https://github.com/pandas-dev/pandas/issues/66050",
    "title": "BUG: pd.array() silently drops missing values when converting NumPy masked arrays",
    "labels": ["Bug", "Needs Triage"],
    "comments_count": 0,
    "updated_at": "2026-06-27T06:58:11Z"
  },
  "signals": {
    "has_reproduction": true,
    "has_expected_behavior": true,
    "maintainer_invited_pr": false,
    "likely_docs_only": false
  },
  "score": {
    "patchability": 0,
    "showcase_value": 0,
    "risk": 0,
    "priority": 0
  },
  "next_actions": []
}
```

The implementation should fill numeric fields from current data. The schema uses `0` in the example to show type, not as a default claim.

## Scoring Model

The score is deterministic and explainable. It is not a model confidence score.

- Patchability increases with minimal reproduction, clear expected behavior, recent update, small likely surface, testable local command, and maintainer acceptance signals.
- Showcase value increases with repository visibility, AI/tooling relevance, research relevance, provenance richness, and ability to demonstrate more than one flagship.
- Risk increases with security sensitivity, unclear ownership, huge build requirements, GPU-only reproduction, flaky integration surfaces, or ambiguous expected behavior.
- Priority is computed from patchability plus showcase value minus risk, with a hard block if reproduction is absent and no maintainer signal exists.

Initial weight guidance:

- `has_reproduction`: +30 patchability
- `has_expected_behavior`: +20 patchability
- `updated_within_14_days`: +10 patchability
- `maintainer_invited_pr`: +25 showcase value
- `stars_over_100k`: +10 showcase value
- `requires_gpu_or_large_model`: +35 risk
- `security_sensitive`: +40 risk
- `ambiguous_expected_behavior`: +25 risk

The score output must include a `reasons` array so an operator can disagree with the ranking without reverse engineering it.

## Data Flow

1. Scout queries GitHub through `gh` or the GitHub API, with explicit query text and captured timestamps.
2. Gather writes candidate receipts under a Telos showcase output directory.
3. Index maps only the selected target clone, not the whole workstation.
4. Forum routes the candidate to a capability lane and notes low-confidence decisions.
5. The operator or an agent attempts local reproduction in an isolated checkout.
6. Crucible assesses the reproduction and patch thesis against observed command output.
7. Telos writes the final packet and links every receipt.

The durable output root should be under a generated directory such as `demo/showcase/runs/<run-id>/`. Generated run output should stay uncommitted unless intentionally curated as a synthetic or redacted example.

## PR-Readiness Packet

The final packet is a local artifact, not a public submission.

Required fields:

- candidate record path
- issue URL and repository URL
- clone path or commit SHA used for analysis
- reproduction command and result
- patch summary
- tests run and result
- Crucible verdict
- files changed
- risk notes
- public PR draft text, clearly marked as draft
- operator next action: `open-pr`, `revise`, `abandon`, or `monitor`

The packet may include a patch file or git diff path, but it must not include secrets, local private paths beyond the isolated checkout root, or unrelated workstation metadata.

## Error Handling

- GitHub API failure: emit `UNVERIFIABLE` candidate capture with command, exit status, and stderr excerpt.
- Rate limit: stop the scout and record the reset time if available.
- Clone failure: keep the candidate brief and mark repository analysis missing.
- Test failure before patch: preserve the reproduction failure as evidence.
- Test failure after patch: mark the patch thesis `DRIFT` unless the failure is unrelated and independently evidenced.
- Missing reproduction: keep the issue as `needs-human-triage`, not PR-ready.
- Large repository timeout: emit partial index evidence with elapsed time and omitted paths.

## Testing Strategy

The first implementation should not require live GitHub for unit tests.

- Use a static fixture for a candidate modeled after the pandas masked-array issue.
- Test candidate scoring deterministically.
- Test that a missing reproduction cannot become PR-ready.
- Test that a record with reproduction, patch summary, test evidence, and `MATCH` verdict can become PR-ready.
- Test that generated packets do not include `.env`, token-like fields, or unredacted home-directory paths.
- Add one live smoke command only if it is explicitly separated from default tests.

## Accessibility And UX

The CLI output should be useful for repeated operator work.

- Human output should show a compact ranked table, not raw JSON.
- JSON output should be complete, stable, and schema-versioned.
- Every generated path should be printed once.
- Every blocked candidate should name the missing evidence.
- The visual Telos demo can later render the showcase as a pipeline, but the first implementation should work without a browser.

## Compatibility

The lane should work through:

- local CLI JSON commands
- MCP tools after command behavior is stable
- GitHub CLI or GitHub API fetchers
- isolated local clones
- generated file receipts
- future Codex, Claude, OpenAI Agents, IDE, TUI, or full app hosts that consume the same JSON contracts

No provider-specific adapter should own the workflow logic.

## Initial Target Recommendation

Use `pandas-dev/pandas#66050` as the first proving target.

Reasons:

- Fresh issue from 2026-06-27. Confidence: high.
- Minimal reproduction is included in the issue body. Confidence: high.
- Expected behavior is explicit. Confidence: high.
- The likely fix and test surface are local Python, not GPU, browser, or IDE integration. Confidence: moderate until repository mapping confirms exact files.
- It demonstrates high-value data correctness, which fits Gather receipts, Index mapping, Forum routing, Crucible verification, and Telos PR-readiness output cleanly.

## Out Of Scope For First Implementation

- Automatically opening PRs.
- Posting comments on upstream issues.
- Running GPU-only reproductions.
- Broad multi-repo patch automation.
- Persisting private workstation scans as showcase evidence.
- Claiming a candidate is fixed without before and after local evidence.

## Acceptance Criteria

The first implementation plan should be considered ready when the spec supports these outcomes:

1. A candidate can be represented as `project-telos.oss-candidate/v1`.
2. A scout can rank at least one fixture candidate without network access.
3. A PR-readiness packet can be generated from local evidence.
4. Missing reproduction or missing test evidence blocks PR-readiness.
5. The lane composes with the existing Telos catalog and action-envelope model.
6. Public PR submission remains operator-gated.

## Review Gate

After this design is approved as a written spec, the next step is a task-by-task implementation plan. The implementation plan should start with a fixture-only scout and record writer in Telos, then add one live GitHub scout smoke path, then use the first pandas candidate as the proving target.
