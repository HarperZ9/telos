# Pass 0133 Ledger: YouTube Source-Lead Intake

Date: 2026-07-01

## Objective

Ingest the latest supplied YouTube links and the Kane B channel page into the
dogfood research lane as source leads. The pass binds metadata, transcript, and
channel-page receipts without treating video titles, auto-captions, or speaker
claims as verified facts.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_youtube_source_lead_intake.py` | Composer for video receipts, route heuristics, product hypotheses, boundary policy, flagship receipts, and negative controls. |
| `tools/test_youtube_source_lead_intake.py` | Focused TDD test for pass 0133. |
| `tools/probe_youtube_source_lead_intake.py` | Packet, brief, steelman, thesis, measurement, and tool-receipt generator. |
| `tools/validate_pass_0133_youtube_source_lead_intake.py` | Validator for source counts, video route boundaries, negative controls, and artifact seal. |
| `schemas/youtube-source-lead-intake-pass-0133.json` | `YouTubeSourceLeadIntakeReceipt/v1` artifact. |
| `schemas/pass-0133-youtube-source-lead-intake-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0133.json` | Compact source, route, Forum, Index, Telos, catalog, compose, test, and validator receipts. |
| `packets/143-youtube-source-lead-intake.md` | Human-readable pass 0133 source-lead intake packet. |
| `briefs/143-youtube-source-lead-intake-brief.md` | Buyer-facing pass 0133 source-lead intake brief. |
| `adversarial/pass-0133-youtube-source-lead-intake-steelman.md` | Local pass 0133 steelman. |
| `crucible/pass-0133-thesis.json` | Falsifiable claims. |
| `crucible/pass-0133-measurements.json` | Measurements/evidence. |
| `crucible/pass-0133-report.md` | Crucible report. |
| `crucible/pass-0133-run.json` | Crucible run record. |
| `gather/pass-0133-youtube-source-lead-intake/` | Gather source store for supplied YouTube metadata, transcripts, and channel page. |

## Result

| Measurement | Value |
| --- | --- |
| Artifact status | `YOUTUBE_SOURCE_LEAD_INTAKE_MATCH` |
| Artifact sha256 | `d63895cc9432c230c4802ee294fcc7d50bc133951608845cf9453359db22af89` |
| Artifact seal | `3e489c7334fbcdb2acd5d3ee9bb52c6bdf7bc9d5730942fbefc58e53e6d5e5ce` |
| Gather source receipts | `19` |
| Video leads | `9 SOURCE_LEAD_ONLY` |
| Routes | `4` |
| Product hypotheses | `4` |
| Negative fixtures rejected | `6` |
| Unsupported claim count | `0` |
| Current promoted natural laws | `0` |
| `yt-dlp` version | `2026.06.09` |

Boundary: pass 0133 records YouTube metadata, transcript, and channel-page
receipts as lead evidence only. It does not verify the underlying philosophical,
biological, computing, market, or scientific claims in the videos.

## Source Receipts

| Source | Kind | Method | sha256 | status |
| --- | --- | --- | --- | --- |
| `https://www.youtube.com/watch?v=PxucUNi3UZo` | metadata | `yt-dlp` | `086bc4d181c57c9b9f563386b48e044f884057562817bb6ce33ad0f673d6f7d9` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=PxucUNi3UZo` | transcript | `auto-caption` | `a16e0ce2c7c44140a94af14e5cef746792b063be06c762ce92c9e7a989da59ea` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=c9BFn4Kqj0E&t=136s` | metadata | `yt-dlp` | `38a9b0424b5fcc51eb48ba755e0b94c5852baf0795673f3b132103c321bbda9c` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=c9BFn4Kqj0E&t=136s` | transcript | `auto-caption` | `be5ecb121f0419baf2e754342c5ed670dfb993863dc5087db9bf7476ee917d94` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=jOqymknUa_k` | metadata | `yt-dlp` | `e15ecf773a16844420711a0fc3d6d62e25c04a49b336db9d6d6c05f6c8507b24` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=jOqymknUa_k` | transcript | `auto-caption` | `b87e8309f1ee9a8f0bbc0145b2b6bd482eb5e6cfec8104050bdb8416ff8cb6af` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=1luMT2KUAOo` | metadata | `yt-dlp` | `7b26e9f66d89bec2963ab9446ea627828f6add5521654ab4094af0341d9ce4cb` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=1luMT2KUAOo` | transcript | `auto-caption` | `537b0364c19d4b7a334bcf3c7b2011de494404f155af824694017178c3e10805` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=WN0sl_jQ3Mg` | metadata | `yt-dlp` | `c9d95c9f088e358d96f869362b6a08a2a059c9ad2f25030c167c1e6ef955756d` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=WN0sl_jQ3Mg` | transcript | `auto-caption` | `c1d03c7b2b215a6e0d36fa5e76db9b21e9cd4f3a03cd52b280be7d995a562afc` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=6Jd1syHnjAQ` | metadata | `yt-dlp` | `014fbd6dbb8ffa439b92b512ffbbb1248fe7f2feb4f6da9cb4e4ede2d3c186d8` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=6Jd1syHnjAQ` | transcript | `auto-caption` | `426cf0ee6ae1208455bfeeed100a1da8e77558a610eb0ce7f2d85348f1720f00` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=XcnCnNQlNnE` | metadata | `yt-dlp` | `758df042a93ce47722a28d3315852cc6b07cc14902e815710a37dc0eb8750516` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=XcnCnNQlNnE` | transcript | `auto-caption` | `f4652a7d29ea8ae087bd1c1f3fb4bdcfc58d91bb74b25457c4d2ca981467c2ae` | `GATHER_VERIFIED` |
| `https://www.youtube.com/@KaneB/videos` | webpage | `http-get` | `d61a7a5790bfd9f4027fb5e0ee11800aaef50b03b200fafd7867f7dfcadf5fc7` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=3_XRPv1OcPg` | metadata | `yt-dlp` | `0bf37000f378994a7df8cd0665233ba8338fecefd417d5599bda190c51326f82` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=3_XRPv1OcPg` | transcript | `auto-caption` | `2aaced66b05cab0e98acf04dd2369f4683a88b64dcfaaf4a649f83161fa1d4be` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=EdVG5qNm2rY` | metadata | `yt-dlp` | `21487bbc4d7877efe38915567f8221ef7f560e95676dd402be0865af15303891` | `GATHER_VERIFIED` |
| `https://www.youtube.com/watch?v=EdVG5qNm2rY` | transcript | `yt-dlp` | `304feec6cab459937db1d38aa87abcbda3979a176799cbf6c3724e55a2fb29cf` | `GATHER_VERIFIED` |

## Route Summary

| Route | Videos | Status |
| --- | ---: | --- |
| `biology_evolution_geometry` | `1` | `SOURCE_LEAD_ONLY` |
| `epistemology_ethics_learning` | `5` | `SOURCE_LEAD_ONLY` |
| `philosophy_learning` | `2` | `SOURCE_LEAD_ONLY` |
| `theoretical_computing_breakthrough` | `1` | `SOURCE_LEAD_ONLY` |

## Video Leads

| Video | Title | Route | Status |
| --- | --- | --- | --- |
| `1luMT2KUAOo` | `The Veridicalist Response to Skepticism` | `epistemology_ethics_learning` | `SOURCE_LEAD_ONLY` |
| `3_XRPv1OcPg` | `"Geometric Framework for Biological Evolution" by Vitaly Vanchurin` | `biology_evolution_geometry` | `SOURCE_LEAD_ONLY` |
| `6Jd1syHnjAQ` | `Can we eliminate the harm of death?` | `philosophy_learning` | `SOURCE_LEAD_ONLY` |
| `EdVG5qNm2rY` | `21 Yr Old Disproves 4 Decades Old Belief in Computing` | `theoretical_computing_breakthrough` | `SOURCE_LEAD_ONLY` |
| `PxucUNi3UZo` | `Is Skepticism Immoral?` | `epistemology_ethics_learning` | `SOURCE_LEAD_ONLY` |
| `WN0sl_jQ3Mg` | `Who is the Best Philosopher Ever?` | `philosophy_learning` | `SOURCE_LEAD_ONLY` |
| `XcnCnNQlNnE` | `Skepticism Isn't About What You Don't Know` | `epistemology_ethics_learning` | `SOURCE_LEAD_ONLY` |
| `c9BFn4Kqj0E` | `Nonpropositional Truth` | `epistemology_ethics_learning` | `SOURCE_LEAD_ONLY` |
| `jOqymknUa_k` | `Threshold Deontology` | `epistemology_ethics_learning` | `SOURCE_LEAD_ONLY` |

## Product Hypotheses

| Tool | Status | Wedge |
| --- | --- | --- |
| `Argument-to-Proof Packet Router` | `HYPOTHESIS` | Turn philosophy videos into source leads, claim graphs, objections, and proof gates. |
| `Bio-Evolution Geometry Queue` | `HYPOTHESIS` | Route biology/evolution geometry talks into executable model and falsifier packets. |
| `TCS Breakthrough Replication Queue` | `HYPOTHESIS` | Turn computing-breakthrough videos into paper/source retrieval and independent proof replay tasks. |
| `Transcript Boundary Auditor` | `HYPOTHESIS` | Separate metadata, transcript, speaker claims, and independently verified claims. |

## Negative Controls

| Fixture | Status | Failure reason |
| --- | --- | --- |
| `video_title_as_fact_rejected` | `REJECTED` | `title_is_source_lead,requires_primary_source` |
| `auto_caption_as_ground_truth_rejected` | `REJECTED` | `auto_caption_noise,requires_verification` |
| `channel_page_as_complete_catalog_rejected` | `REJECTED` | `dynamic_page,partial_http_capture` |
| `raw_transcript_export_rejected` | `REJECTED` | `copyright_boundary,digest_only` |
| `video_only_market_claim_rejected` | `REJECTED` | `no_buyer_evidence,no_competitor_matrix` |
| `source_lead_as_law_rejected` | `REJECTED` | `requires_independent_proof,requires_reproduction` |

## Gather

| Document | sha256 | seal |
| --- | --- | --- |
| `packets/143-youtube-source-lead-intake.md` | `472ed8b4bb4bc0c68b4cf47f2cde551877a8efb0bea1d44cff49e64c6168a233` | `b54771ac5731e7f41e4a7b4b3454b42a5de6b335e488ab163e63b73eb26cd5f1` |
| `briefs/143-youtube-source-lead-intake-brief.md` | `dfe96bf86545e09e29fbf1899091c8acacb36d2e03fe5f22e66d86d9748f051c` | `c6a22286eed4a080d9fb2daedb374ffbad37adf0e800ec09d62d6f0f43822e51` |

## Crucible

| Measurement | Value |
| --- | --- |
| Thesis id | `0854c2272c84e7d4` |
| Thesis seal | `0854c2272c84e7d442d7413aa62e024899ae19a962f08d31748698df2b5f13e9` |
| Claims | `11` |
| MATCH | `11` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `6e6a8abddb0ae1e26bb0b95426d0ca748af296bb9f7aa1f3db49005cca5efca8` |
| Measurement seal | `7bb62941f376999d91839db66cca9e48e931824134be528b495f691608ed5696` |
| Assessment seal | `7f898951e699a50dac8cf1316dd8a3fd8ce895a68e93b38c5192308e28d4423b` |

Registry after pass 0133:

- theses: `126`;
- claims: `1151`;
- verdicts: `1151 MATCH`, `0 DRIFT`, `0 UNVERIFIABLE`;
- invalid latest assessments: `0`.

## File Hashes

| File | sha256 |
| --- | --- |
| `schemas/youtube-source-lead-intake-pass-0133.json` | `d63895cc9432c230c4802ee294fcc7d50bc133951608845cf9453359db22af89` |
| `schemas/pass-0133-youtube-source-lead-intake-validator-result.json` | `00bfae86bc9f3d46b8e8453dc5339641858ca7c3a3e72f02c91b32047e894ebd` |
| `schemas/tool-receipts-pass-0133.json` | `2694abb6238b905b18d552cb96df950c8e39eaff3ce8430925d4b90f3e908101` |
| `packets/143-youtube-source-lead-intake.md` | `472ed8b4bb4bc0c68b4cf47f2cde551877a8efb0bea1d44cff49e64c6168a233` |
| `briefs/143-youtube-source-lead-intake-brief.md` | `dfe96bf86545e09e29fbf1899091c8acacb36d2e03fe5f22e66d86d9748f051c` |
| `adversarial/pass-0133-youtube-source-lead-intake-steelman.md` | `ffd266d4df8cd228f86bb02ffbffe2f3874b199d32d93b157fb22e7f2ef2b732` |
| `crucible/pass-0133-thesis.json` | `d07d41cbade4d84f32234e71cb54fb0ec9883ff050bfbc8f3f76c52d1dac8a06` |
| `crucible/pass-0133-measurements.json` | `948aa9bf592d0bd2762e750fe086cdc8a27bb4faae65b496939b130aa4af20b7` |
| `crucible/pass-0133-report.md` | `d98e8ec9a7b76a0076be94a39fbab4ec198680d45e34341fb8632d1b68c9e719` |
| `crucible/pass-0133-run.json` | `ef5515bd3de3ada60827379bca484f5b5c94c9c27ce531fd4367058866022a16` |
| `tools/compose_youtube_source_lead_intake.py` | `b7482721c8cf187d4475e3161c1d6cd99943e30013b6288893c6d9becc2ba540` |
| `tools/test_youtube_source_lead_intake.py` | `3cc2df8cbee4a8176c1b4beacba78aacfaea7f93e88ca19b44e6d559ac5185fd` |
| `tools/validate_pass_0133_youtube_source_lead_intake.py` | `9b1e238c90fbbf828c8362e2e81106fe549e536870ff15fc85531f9079b95952` |
| `tools/probe_youtube_source_lead_intake.py` | `62081849c0060632e40420002934aa283514bbbdb46223ab7dd2d43c173d6d25` |

## Verification Commands

```powershell
python -m py_compile docs\research\dogfood\tools\compose_youtube_source_lead_intake.py docs\research\dogfood\tools\test_youtube_source_lead_intake.py docs\research\dogfood\tools\validate_pass_0133_youtube_source_lead_intake.py docs\research\dogfood\tools\probe_youtube_source_lead_intake.py
python docs\research\dogfood\tools\test_youtube_source_lead_intake.py
python docs\research\dogfood\tools\probe_youtube_source_lead_intake.py
python docs\research\dogfood\tools\validate_pass_0133_youtube_source_lead_intake.py
gather corpus verify docs\research\dogfood\gather\pass-0133-youtube-source-lead-intake --json
gather docs docs\research\dogfood\packets\143-youtube-source-lead-intake.md --json
gather docs docs\research\dogfood\briefs\143-youtube-source-lead-intake-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0133-thesis.json --measurements docs\research\dogfood\crucible\pass-0133-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0133-report.md --out docs\research\dogfood\crucible\pass-0133-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

The next pass should convert the source-lead intake into an author/reference
theory graph: source author, works, reference lineage, theory chain, proofable
claim, experiment target, negative-control fixture, and market/tool hypothesis.
Best first lanes are Brandom/Kane B for learning-theory graphs, Vitaly
Vanchurin/Michael Levin for biology/evolution geometry, and the Turing
computing-breakthrough video for primary-paper retrieval and independent proof
replay.
