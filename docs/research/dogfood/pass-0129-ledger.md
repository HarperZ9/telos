# Pass 0129 Ledger: Brandom Functional Learning Digest

Date: 2026-07-01

## Objective

Catalog and digest the supplied Robert Brandom sources into functional-learning
tool hypotheses while keeping evidence boundaries explicit. This pass treats
Brandom's work as a source substrate for learning-tool design: claims become
moves in a reason-governed practice, not isolated notes.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_brandom_functional_learning_digest.py` | Composer for source receipts, topic signals, derivation map, scorekeeping fixture, tool hypotheses, and negative controls. |
| `tools/test_brandom_functional_learning_digest.py` | Focused TDD test for pass 0129. |
| `tools/validate_pass_0129_brandom_functional_learning_digest.py` | Validator for seal, source receipts, transcript boundary, topic signals, scorekeeping, and flagships. |
| `tools/probe_brandom_functional_learning_digest.py` | Packet, brief, steelman, thesis, measurement, and tool-receipt generator. |
| `schemas/brandom-functional-learning-digest-pass-0129.json` | `BrandomFunctionalLearningDigestReceipt/v1` artifact. |
| `schemas/pass-0129-brandom-functional-learning-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0129.json` | Compact source, digest, Forum, Index, Telos, catalog, compose, test, and validator receipts. |
| `packets/139-brandom-functional-learning-digest.md` | Human-readable pass 0129 digest packet. |
| `briefs/139-brandom-functional-learning-brief.md` | Buyer-facing pass 0129 brief. |
| `adversarial/pass-0129-brandom-functional-learning-steelman.md` | Local pass 0129 steelman. |
| `crucible/pass-0129-thesis.json` | Falsifiable claims. |
| `crucible/pass-0129-measurements.json` | Measurements/evidence. |
| `crucible/pass-0129-report.md` | Crucible report. |
| `crucible/pass-0129-run.json` | Crucible run record. |
| `gather/pass-0129-brandom-functional-learning/` | Gather source store for supplied Brandom pages and video receipts. |

## Result

| Measurement | Value |
| --- | --- |
| Artifact status | `BRANDOM_FUNCTIONAL_LEARNING_DIGEST_MATCH` |
| Artifact sha256 | `f59fc22c4a1f7f44dfd0aaa74047e16764fe2d36130a2e57badd0b15b6a465d8` |
| Artifact seal | `3c1fbb62dfdf5b3696e847b2020488b5a73093e7b4991228071ae3d218e7e31a` |
| Gather source receipts | `7` |
| Inaccessible supplied sources | `2` |
| Tool hypotheses | `5` |
| Scorekeeping fixture | `MATCH` |
| Negative fixtures rejected | `5` |
| Current promoted natural laws | `0` |

## Source Receipts

| Source | Kind | sha256 | status |
| --- | --- | --- | --- |
| `https://sites.pitt.edu/~rbrandom/` | webpage | `e18b789804ea94229451a6db56f30608ab25023f954120ad26f667fe9bf65aff` | `GATHER_VERIFIED` |
| `https://sites.pitt.edu/~rbrandom/Texts%20Mark%201%20p.html` | webpage | `bc801e10d78960b928caec6973ce5361a456f6b4a55f18112b6f2ae95fc2b3a1` | `GATHER_VERIFIED` |
| `https://sites.pitt.edu/~rbrandom/Courses%201%20c.html` | webpage | `df90a0fc81d07eee9039738d4fac36977246879fc1cac070cdc3b8abb6f26cd1` | `GATHER_VERIFIED` |
| `https://www.philosophy.pitt.edu/people/rbrandom` | webpage | `36491130518b409d05c8ac709ee04b6d78422aa9ae74a43d1def3bbdc59fd2a3` | `GATHER_VERIFIED` |
| `https://www.youtube.com/@BobBrandomPitt/videos` | webpage | `d61a7a5790bfd9f4027fb5e0ee11800aaef50b03b200fafd7867f7dfcadf5fc7` | `GATHER_VERIFIED_SHORT` |
| `JOvZWTk8KFU` | metadata | `7589efc0ab4b2d469c6ce43b85b67789242b0e3ae7987db73e80c7ab3c0f9eb7` | `GATHER_VERIFIED` |
| `JOvZWTk8KFU` | transcript | `1e0538cdc0aae8dca484cced9f0a9b52b57be9433eb2dba862f939e9602a1772` | `GATHER_VERIFIED_HASHED` |

Inaccessible supplied sources:

- `https://www.researchgate.net/profile/Bob-Brandom`: `INACCESSIBLE_HTTP_403`
- `https://pitt.academia.edu/RobertBrandom`: `INACCESSIBLE_HTTP_403`

## Digest

Top observed topic signals:

| Term | Documents | Hits |
| --- | --- | --- |
| `logic` | `4` | `58` |
| `Kant` | `3` | `52` |
| `reason` | `4` | `39` |
| `language` | `4` | `32` |
| `representation` | `3` | `28` |
| `pragmatism` | `4` | `19` |
| `Hegel` | `2` | `18` |
| `Sellars` | `5` | `16` |
| `expressivism` | `3` | `9` |
| `inferentialism` | `2` | `5` |

Derived learning-tool hypotheses:

| Tool | Status | Need |
| --- | --- | --- |
| `Inferential Graph Tutor` | `HYPOTHESIS` | Turn readings and lectures into claim, reason, consequence, and objection graphs. |
| `Scorekeeping Lab` | `HYPOTHESIS` | Let learners practice commitments, entitlements, challenges, and repairs with action receipts. |
| `Expressive Vocabulary Ladder` | `HYPOTHESIS` | Show which vocabulary makes an implicit practice explicit. |
| `Seminar-to-Proof Packet` | `HYPOTHESIS` | Convert lecture source leads into exercises, tests, and Crucible-checked learning packets. |
| `Tradition Derivation Atlas` | `HYPOTHESIS` | Map Kant, Hegel, Sellars, Rorty, and Brandom dependencies across courses and texts. |

## Scorekeeping Fixture

The bounded learning fixture models a claim as a commitment and a source-backed
claim as an entitlement. The loop asserts `p`, attaches a source receipt,
adds `p -> q`, and only then infers `q`. Final entitlements are
`p,p_implies_q,q`.

## Negative Controls

| Fixture | Status | Failure reason |
| --- | --- | --- |
| `raw_transcript_as_textbook_rejected` | `REJECTED` | `copyright_boundary,requires_digest_not_dump` |
| `blocked_profiles_as_evidence_rejected` | `REJECTED` | `researchgate_403,academia_403` |
| `profile_as_complete_bibliography_rejected` | `REJECTED` | `profile_is_partial,requires_texts_and_courses_catalog` |
| `philosophy_to_product_without_tasks_rejected` | `REJECTED` | `needs_learning_fixture,needs_measurable_outcome` |
| `brandom_corpus_as_natural_law_rejected` | `REJECTED` | `humanities_digest,not_scientific_law` |

## Gather

| Document | sha256 | seal |
| --- | --- | --- |
| `packets/139-brandom-functional-learning-digest.md` | `76118b140b5cdd4481e9cee5989be9963289d2ba39093ba5bb99fe986383194f` | `d03298e9c0033b59006a8ed44d70bbf33d185735fdec73214bf1193831437955` |
| `briefs/139-brandom-functional-learning-brief.md` | `5bcad7705a7c64cab5dc37ad857b53053052706a825c970fca2872216b9d5f13` | `bbb782b26f4f362398b5dd4d2bdbdb335234a24db949703efa8694b644463d64` |

## Crucible

| Measurement | Value |
| --- | --- |
| Thesis id | `0c10d22df7ccdcc3` |
| Thesis seal | `0c10d22df7ccdcc327dd733bcc368c8c5739caa2cf3eecd87b8ec6a76c46f78b` |
| Claims | `12` |
| MATCH | `12` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `2103b0aa393d5e76bde3d66023bf58e6bd18b23d4db1df1483fa8d2191a81c49` |
| Measurement seal | `2900b845203e9db512840e1ea265fe604d59399f45f579f0c988b92709ef3741` |
| Assessment seal | `cc4bbfeaeb891994cf693d8743b662b116b1c5726775327da57101ed60e46818` |

Registry after pass 0129:

- theses: `121`;
- claims: `1093`;
- verdicts: `1093 MATCH`, `0 DRIFT`, `0 UNVERIFIABLE`;
- invalid latest assessments: `0`.

## File Hashes

| File | sha256 |
| --- | --- |
| `schemas/brandom-functional-learning-digest-pass-0129.json` | `f59fc22c4a1f7f44dfd0aaa74047e16764fe2d36130a2e57badd0b15b6a465d8` |
| `schemas/pass-0129-brandom-functional-learning-validator-result.json` | `b1b63adc39b6e47257bec1010ed439e7252433a7371f485bc4ee887ba115ba97` |
| `schemas/tool-receipts-pass-0129.json` | `1f32daa729a9e15e30ec16d9be219d9ca4dff36d35d656c84332f71d4ebe41bb` |
| `packets/139-brandom-functional-learning-digest.md` | `76118b140b5cdd4481e9cee5989be9963289d2ba39093ba5bb99fe986383194f` |
| `briefs/139-brandom-functional-learning-brief.md` | `5bcad7705a7c64cab5dc37ad857b53053052706a825c970fca2872216b9d5f13` |
| `adversarial/pass-0129-brandom-functional-learning-steelman.md` | `c39e21d496f7ea68e2e874d4bcac5e9e81b9c2093a4597a6101c9c6899909842` |
| `crucible/pass-0129-thesis.json` | `96cc168a5175f7b48a0ace07f0e6c9870ee97fe92915bde41feb8d1d6a41585f` |
| `crucible/pass-0129-measurements.json` | `4a0ff68214a88d29b6e8db49fe7e16ef7384aa38f1c7dd9645b1dc28d579c763` |
| `crucible/pass-0129-report.md` | `185bc32aeb5c20e30525460e106065b8fa617a0a7708684d44fa5bbeaca1909a` |
| `crucible/pass-0129-run.json` | `b0b0032f41695cd66ee9682b5b241770fa093c2a476473e276714eab2ac42038` |
| `tools/compose_brandom_functional_learning_digest.py` | `fa627b8be943d45c6181eb5d98eee83b2aa9e5b9661b880674b5c883744754f5` |
| `tools/test_brandom_functional_learning_digest.py` | `7f83f72187beab8cf3de8c80ae1d9ee9b037bead48458a7ba7bbd4ce05852c70` |
| `tools/validate_pass_0129_brandom_functional_learning_digest.py` | `6ccf2157eed8f5c031ecb1322af23d81abe5dadc1183e97577cbb7d9322a25dc` |
| `tools/probe_brandom_functional_learning_digest.py` | `587ef7536957ef7a13afced947ee2b31db74f6645456cef96cd5334ddb683223` |

## Verification Commands

```powershell
python -m py_compile docs\research\dogfood\tools\compose_brandom_functional_learning_digest.py docs\research\dogfood\tools\test_brandom_functional_learning_digest.py docs\research\dogfood\tools\validate_pass_0129_brandom_functional_learning_digest.py docs\research\dogfood\tools\probe_brandom_functional_learning_digest.py
python docs\research\dogfood\tools\test_brandom_functional_learning_digest.py
python docs\research\dogfood\tools\probe_brandom_functional_learning_digest.py
python docs\research\dogfood\tools\validate_pass_0129_brandom_functional_learning_digest.py
gather docs docs\research\dogfood\packets\139-brandom-functional-learning-digest.md --json
gather docs docs\research\dogfood\briefs\139-brandom-functional-learning-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0129-thesis.json --measurements docs\research\dogfood\crucible\pass-0129-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0129-report.md --out docs\research\dogfood\crucible\pass-0129-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

The next pass should deepen the Brandom corpus map: fetch specific downloadable
texts from the Pitt texts page, extract a work-level catalog, and convert one
course into a lesson graph with claims, prerequisites, exercises, objections,
and Crucible-checked learner actions.
