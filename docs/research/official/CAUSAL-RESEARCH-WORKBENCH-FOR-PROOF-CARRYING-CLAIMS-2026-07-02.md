# Causal Research Workbench for Proof-Carrying Claims

Official local copy for publication packaging.
Author: Zain Dana Harper
Date: 2026-07-02
Status: working draft, not archive-submitted

## Official Status

`CAUSAL_DAG_FIXTURE_MATCH` applies to the deterministic local toy DAG fixture.

`SOURCE_LEAD` applies to the arXiv metadata rows in the source ledger.

`HYPOTHESIS` applies to the larger causal-research workbench, biomedical,
AI4Science, and LLM benchmark product opportunity.

`NOT_REPLAYED` applies to real causal discovery, real medical claims,
BuildLang/buildc-native execution, and all external benchmark results.

## Publishable Claim

Project Telos now has a replayable causal-claim preflight that binds:

- source-ledger receipts,
- explicit graph assumptions,
- treatment and outcome declarations,
- minimal adjustment-set checks,
- negative controls,
- bounded non-claims,
- Crucible measurement receipts, and
- Learn prooflesson export.

The fixture proves only the local contract. It is not a domain result.

## Verified Artifacts

- Source ledger:
  `demo/research/causal-workbench-source-receipts.json`
- Fixture CLI:
  `demo/causal-workbench-proof-packet.mjs`
- Fixture test:
  `demo/causal-workbench-proof-packet.test.mjs`
- Fixture output:
  `docs/outreach/receipts/twenty-eighth-wave/causal-workbench-proof-packet-2026-07-02.json`
- Outreach note:
  `docs/outreach/TWENTY-EIGHTH-WAVE-CAUSAL-WORKBENCH-PREFLIGHT-2026-07-02.md`
- Working paper:
  `docs/research/whitepapers/CAUSAL-RESEARCH-WORKBENCH-FOR-PROOF-CARRYING-CLAIMS-2026-07-02.md`
- Crucible run:
  `docs/outreach/receipts/twenty-eighth-wave-causal-workbench-run-2026-07-02.json`
- Crucible run SHA-256:
  `1880e9f0c2c4f2589d4cde2f2c95e008631fd4eea0e0a921b39f19b961eef26e`
- Crucible report:
  `docs/outreach/receipts/twenty-eighth-wave-causal-workbench-report-2026-07-02.md`
- Crucible report SHA-256:
  `cc1d3ec1cd45d68e3600da5cc98b5c72ecc9f562f404273fa389afc021bff577`
- Learn packet:
  `docs/outreach/receipts/twenty-eighth-wave/causal-workbench.learn-packet.json`
- Learn packet SHA-256:
  `2788762b9328777d508d94296ec9b704d4168ef96e2d48d182f8342ca0d50e2a`
- Learn prooflesson receipt:
  `docs/outreach/receipts/twenty-eighth-wave/learn-causal-workbench/tutor/twenty-eighth-wave-causal-workbench.prooflesson.json`
- Learn prooflesson SHA-256:
  `2a93f5140737eddf9f1ac3d861e96b160a59241032165b3c2171822193ba0aa8`
- Learn reverify witness SHA-256:
  `6e358d9ea652f8e5efee0882ca7046705dc1f1c23421763d9607dd3274b6ad35`

## Fixture Result

The fixture graph declares:

- Treatment: `exercise`
- Outcome: `health_outcome`
- Confounders: `age`, `baseline_health`
- Instrument-like driver in the fixture: `encouragement`
- Descendant/collider danger variable: `biomarker`

The replayed result is:

`minimal_adjustment_sets = [["age", "baseline_health"]]`

The following adjustment attempts are rejected:

- no adjustment,
- `age` alone,
- `baseline_health` alone,
- `encouragement` alone,
- `biomarker`, because it is a descendant of the treatment.

## Publication Boundary

The publication can say:

> Project Telos turned a causal-inference source-intake lane into a replayable
> causal-claim preflight. The preflight demonstrates how a proof packet can
> carry graph assumptions, adjustment checks, negative controls, and verification
> receipts before a causal claim is promoted.

The publication must also say:

> This is a toy DAG fixture. It does not solve causal discovery, validate LLM
> causal reasoning, issue a medical recommendation, or prove BuildLang/buildc
> causal-runtime execution.

## Promotion Checklist

- [x] Source ledger is metadata-only.
- [x] Fixture graph declares treatment, outcome, observed variables, and edges.
- [x] Fixture computes treatment descendants.
- [x] Fixture identifies backdoor paths.
- [x] Fixture identifies the exact minimal adjustment set.
- [x] Fixture rejects negative controls.
- [x] Local test replays the fixture.
- [x] Public copy labels source rows as leads rather than domain proof.
- [x] Crucible run and report hashes patched after final run.
- [x] Learn packet and prooflesson hashes patched after final run.
- [ ] BuildLang/buildc version exists.
- [ ] Synthetic SCM estimator fixture exists.
- [ ] Time-series causal fixture exists.
- [ ] External benchmark-card parser exists.

## Next Submission Gate

Do not submit this as an empirical causal-inference result. The stronger next
paper should be a methods paper: proof-carrying causal claims for AI-assisted
research, with a synthetic SCM, benchmark-card parser, and BuildLang/buildc
typed DAG runtime.
