# Pass 0115 Ledger: Solver-Branch Replay Adapter

Date: 2026-07-01

## Objective

Turn the pass 0114 multi-domain constrained optimization suite into a solver
branch replay adapter. The pass replays the four toy optimization witnesses
through deterministic local branches, runs the available SciPy HiGHS branch for
the quant case, fences unavailable OR-Tools and PuLP branches, and binds four
new YouTube links as Gather-verified source leads.

This pass is still a proof-packet exercise, not a claim of industrial solver
deployment or scientific discovery.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_solver_branch_replay_adapter.py` | Solver replay composer plus Forum, Index, Telos, and YouTube source-lead bindings. |
| `tools/solver_youtube_leads.py` | Gather-backed YouTube source-lead parser for pass 0115. |
| `tools/test_solver_branch_replay_adapter.py` | Focused TDD test for solver branches, availability fences, and YouTube lead receipts. |
| `tools/probe_solver_branch_replay_adapter.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0115_solver_branch_replay_adapter.py` | Independent validator for solver branches, receipt boundaries, and source-lead fields. |
| `schemas/solver-branch-replay-adapter-pass-0115.json` | `SolverBranchReplayAdapterReceipt/v1` artifact. |
| `schemas/pass-0115-solver-branch-replay-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0115.json` | Compact solver, YouTube, roadmap, Forum, Index, Telos, compose, and test receipts. |
| `packets/125-solver-branch-replay-adapter.md` | Human-readable solver-branch replay packet. |
| `briefs/125-solver-branch-replay-adapter-brief.md` | Buyer-facing solver replay brief. |
| `adversarial/pass-0115-solver-branch-replay-adapter-steelman.md` | Local pass 0115 steelman. |
| `crucible/pass-0115-thesis.json` | Falsifiable claims. |
| `crucible/pass-0115-measurements.json` | Measurements/evidence. |
| `crucible/pass-0115-report.md` | Crucible report. |
| `crucible/pass-0115-run.json` | Crucible run record. |
| `gather/pass-0115-youtube-leads/` | Gather video receipts and stored source objects for the four new links. |

## Result

| Measurement | Value |
| --- | --- |
| Artifact status | `SOLVER_BRANCH_REPLAY_ADAPTER_MATCH` |
| Artifact sha256 | `54934757886e58ce3a78edc6322cb49f02943137aef01a51941a545c51ac6d21` |
| Artifact seal | `b4930f6e1901aadc52ea67f2a958e3cd9220893e2be1ebbf15c2b2c24afc8a65` |
| Suite pass binding | `0114` |
| YouTube roadmap pass | `0102` |
| YouTube source pass | `0085` |
| New YouTube lead count | `4` |
| Gather-verified leads | `4` |
| New transcript receipts | `4` |
| Raw transcripts included | `false` |
| Solver branches | `4` |
| Drift total | `0` |
| Unavailable branch count | `2` |
| Unsupported claims | `0` |
| Current promoted natural laws | `0` |

## Solver Branch Matrix

| Branch | Status | Evidence |
| --- | --- | --- |
| `builtin_exhaustive_replay` | `MATCH` | Replayed all four pass 0114 toy cases against expected objectives and assignments. |
| `scipy_highs_quant_replay` | `MATCH` | `quant_risk_budget` objective `9/2`, weights `asset_a=1/2`, `asset_b=1/4`, `asset_c=1/4`, solver status `0`. |
| `ortools_cp_sat` | `UNAVAILABLE_FENCED` | Python module `ortools` missing in this environment. |
| `pulp_cbc` | `UNAVAILABLE_FENCED` | Python module `pulp` missing in this environment. |

## New YouTube Source Leads

| Video | Title | Source status | Claim status | Transcript sha256 |
| --- | --- | --- | --- | --- |
| `HbKzqvey5PA` | The Born rule is Entropy | `GATHER_VERIFIED_RECEIPT` | `SOURCE_LEAD_ONLY` | `26fcba7763c4467d1b3aa5d327ce4100a160b6f8c3e349b1a992cbbda52c5f70` |
| `4MQbd5wTlI8` | Emily Riehl - Higher Category Theory, Homotopy & AI in Math | `GATHER_VERIFIED_RECEIPT` | `SOURCE_LEAD_ONLY` | `4ed1cf2ac702f78e9b8d2e052015a72e38d321906651745c2d8a0f485911542d` |
| `EdVG5qNm2rY` | 21 Yr Old Disproves 4 Decades Old Belief in Computing | `GATHER_VERIFIED_RECEIPT` | `SOURCE_LEAD_ONLY` | `304feec6cab459937db1d38aa87abcbda3979a176799cbf6c3724e55a2fb29cf` |
| `nYwid6Q5HXk` | LLM that loops instead of Doing Chain-of-Thought | `GATHER_VERIFIED_RECEIPT` | `SOURCE_LEAD_ONLY` | `671d1d47e04306c223ff504d0503bc7895f3e364ab0f58f2c6a8b42ba9e2a5eb` |

## Roadmap Pressure

| Pressure | Source | Status |
| --- | --- | --- |
| Formal math proof packets need category theory and homotopy receipts. | `4MQbd5wTlI8` | `hypothesis` |
| Physics packets need quantum foundation claim boundaries before law promotion. | `HbKzqvey5PA` | `hypothesis` |
| Research packets need counterexample and belief-revision workflows. | `EdVG5qNm2rY` | `hypothesis` |
| Agent packets need loop replay receipts without chain-of-thought exposure. | `nYwid6Q5HXk` | `hypothesis` |

## Gather

| Document | sha256 | seal |
| --- | --- | --- |
| `packets/125-solver-branch-replay-adapter.md` | `4ba5e0f793e7af9ef055e4254000531170c9ba2744ede595a908b96a7ea9d081` | `12a202b8c768e25089a63ee3146a8e1ec3977753cfb3af9ba040b38f7cdc2fcb` |
| `briefs/125-solver-branch-replay-adapter-brief.md` | `13da264d214e0c59a5e6fbe93d47758a6710af425f4862763724a2351680f3f0` | `f6fe9cd8cf1d6858a9ab676e0bdad09e0d48b9003f87871df654048bf3ed7c0b` |

## Crucible

| Measurement | Value |
| --- | --- |
| Thesis id | `84e0d4569dd25dbe` |
| Claims | `13` |
| MATCH | `13` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `a7a45353ff9a5e01364924601ce2ecc7667a3755609b93685acd032cfea8c984` |
| Measurement seal | `e053021df0f9e77a5cfb61cce79f5d910690259db92f6a47853a63ce0a5f6564` |
| Assessment seal | `daed11220fe834bb6340ae4a668c309f687aa0d26db28ad5a6925e0d027144c9` |

Registry after pass 0115:

- theses: `105`;
- claims: `913`;
- verdicts: `913 MATCH`, `0 DRIFT`, `0 UNVERIFIABLE`.

## File Hashes

| File | sha256 |
| --- | --- |
| `schemas/pass-0115-solver-branch-replay-validator-result.json` | `e45400a833e4abb9cff2d4eba5cf7dddeafbf21cb8d4f1b012f033e3c0ea7a16` |
| `schemas/tool-receipts-pass-0115.json` | `b24517623975f1dd806b5a0cd2f21b58d89ada2ceb48e520c67e7d6ce943830a` |
| `adversarial/pass-0115-solver-branch-replay-adapter-steelman.md` | `0461a0f0d772f515f075cc591553f31b9103679cb3af7fb0cb026e5e42bc640e` |
| `crucible/pass-0115-thesis.json` | `dc475574d6ab3ecc64b27d981f92006ad11dee10f797b35c631d1892af4abdd4` |
| `crucible/pass-0115-measurements.json` | `9c8a8439bc1a28f3f2b551382e0fefbc18a6f7b33b9132844df50c8d7a94dba5` |
| `crucible/pass-0115-report.md` | `f4f987ed1a3b08fc11b49245a3eaabf0dd64f82e2ab0c525bc90ca8b993db5b8` |
| `crucible/pass-0115-run.json` | `d4e32636884b855d143c9f5a4e0af37edaef01b2dd91e3ef7c0ae0f4546fd751` |
| `tools/compose_solver_branch_replay_adapter.py` | `2f818018af58e94b6e183978f4142a84b3786ccba06412f48b12d4abf2f395f1` |
| `tools/solver_youtube_leads.py` | `040e090404eec8e5c6683e57ff85c1c424e592ce874f1d2549dc31d6b5db1364` |
| `tools/test_solver_branch_replay_adapter.py` | `f5fc74d38eededd12f936a4409454e20f18f5d01b6f248b93d45b3a137034d8b` |
| `tools/validate_pass_0115_solver_branch_replay_adapter.py` | `2bb7bbb9f5ac1c9eb88afb22fbc4479a30e4f8c72a9128a4737e2851c72b905f` |
| `tools/probe_solver_branch_replay_adapter.py` | `45352b6ab9fb004b0f2fa7c5f275a9b74e55dcef2ed25aee241975d44f5e8829` |

## Verification Commands

```powershell
gather video --json --store docs\research\dogfood\gather\pass-0115-youtube-leads https://www.youtube.com/watch?v=HbKzqvey5PA
gather video --json --store docs\research\dogfood\gather\pass-0115-youtube-leads https://www.youtube.com/watch?v=4MQbd5wTlI8
gather video --json --store docs\research\dogfood\gather\pass-0115-youtube-leads https://www.youtube.com/watch?v=EdVG5qNm2rY&t=337s
gather video --json --store docs\research\dogfood\gather\pass-0115-youtube-leads https://www.youtube.com/watch?v=nYwid6Q5HXk
python docs\research\dogfood\tools\probe_solver_branch_replay_adapter.py
python docs\research\dogfood\tools\test_solver_branch_replay_adapter.py
python docs\research\dogfood\tools\validate_pass_0115_solver_branch_replay_adapter.py
python -m py_compile docs\research\dogfood\tools\compose_solver_branch_replay_adapter.py docs\research\dogfood\tools\solver_youtube_leads.py docs\research\dogfood\tools\test_solver_branch_replay_adapter.py docs\research\dogfood\tools\validate_pass_0115_solver_branch_replay_adapter.py docs\research\dogfood\tools\probe_solver_branch_replay_adapter.py
gather docs docs\research\dogfood\packets\125-solver-branch-replay-adapter.md --json
gather docs docs\research\dogfood\briefs\125-solver-branch-replay-adapter-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0115-thesis.json --measurements docs\research\dogfood\crucible\pass-0115-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0115-report.md --out docs\research\dogfood\crucible\pass-0115-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

The next useful pass is a formal-math and physics source-lead bridge: turn the
four new videos into bounded proof-packet requirements for category-theory
notation, counterexample discovery, quantum-foundation claim boundaries, and
loop-replay agent receipts. Keep the videos as source leads until independent
papers, code, or formal artifacts are gathered.
