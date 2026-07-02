# Packet 116: Stoichiometric Invariant Checker Receipt

Date: 2026-07-01

Status: `STOICHIOMETRIC_INVARIANT_CHECKER_RECEIPT_MATCH`

Purpose: generalize the pass 0105 `A -> B` invariant into a small
stoichiometric-matrix checker that derives conserved quantities from
`l^T S = 0`, then rejects an open leaky network.

```text
source_reaction_pass = 0105
source_ai4science_pass = 0104
youtube_pass = 0085
roadmap_pass = 0102
valid_youtube_videos = 19
transcript_receipts = 19
network = closed A->B->C->A cycle
derived_vector = [1, 1, 1]
invariant = A+B+C
residual = [0, 0, 0]
grid_points = 201
max_total_drift = 3.9968028886505635e-15
negative_candidate_residual = [0, 0, 0, -1]
negative_max_total_drift = 0.455672581497486
compose_status = MATCH
test_status = MATCH
```

## Numerical Samples

| t | A | B | C | total |
| ---: | ---: | ---: | ---: | ---: |
| 0.000 | 2.000000000 | 0.500000000 | 1.250000000 | 3.750000000 |
| 1.250 | 1.727851322 | 0.781557942 | 1.240590736 | 3.750000000 |
| 2.500 | 1.530092396 | 0.916720994 | 1.303186610 | 3.750000000 |
| 3.750 | 1.395834201 | 0.969255285 | 1.384910514 | 3.750000000 |
| 5.000 | 1.310022600 | 0.979111209 | 1.460866191 | 3.750000000 |

## Source Anchors

| Source | URL | Kind |
| --- | --- | --- |
| The Convex Basis of the Left Null Space of the Stoichiometric Matrix | https://pmc.ncbi.nlm.nih.gov/articles/PMC1303061/ | paper |
| What makes a reaction network chemical? | https://pmc.ncbi.nlm.nih.gov/articles/PMC9484159/ | paper |
| Catalyst.jl CRN Theory | https://docs.sciml.ai/Catalyst/stable/network_analysis/crn_theory/ | official_docs |
| Catalyst.jl Network Analysis API | https://docs.sciml.ai/Catalyst/stable/api/network_analysis_api/ | official_docs |
| EQTK Core Concepts | https://eqtk.github.io/user_guide/core_concepts.html | official_docs |

## Product Meaning

The YouTube corpus pulls toward AI4Science proof packets, BuildLang scientific
runtime receipts, and optimization/scientific computing workflows. This pass
turns that signal into one reusable proof primitive: conserved-quantity
derivation with a negative fixture and promotion boundary.

## Boundary

This pass implements a bounded stoichiometric invariant checker. It does not prove a new natural law, biological discovery, wet-lab result, or production scientific runtime.
