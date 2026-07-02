# Packet 005: Materials and Chemistry Discovery

Status: `SOURCE_LEAD` plus `HYPOTHESIS`

## Question

Can Telos package materials discovery claims across model prediction, DFT validation, synthesis attempt, and lab evidence?

## Source Anchors

- GNoME Nature paper: https://www.nature.com/articles/s41586-023-06735-9
- DeepMind GNoME blog: https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/
- Materials Project docs: https://docs.materialsproject.org/
- A-Lab context: https://ceder.berkeley.edu/news/a-lab-paper-published-in-nature-featured-in-news-story/

## Working Thesis

Materials discovery is a strong Telos domain because candidate generation, physics-based validation, database provenance, and synthesis attempts naturally form a claim ladder.

Confidence: moderate. Needs actual data integration before any material claim.

## Claim Ladder

1. Candidate generated.
2. Candidate canonicalized.
3. Existing database checked.
4. DFT or surrogate validation run.
5. Stability/energy claim recorded.
6. Synthesis plan proposed.
7. Lab or literature synthesis evidence attached.
8. Claim promoted, rejected, or marked `UNVERIFIABLE`.

## Adversarial Steelman

Objection: GNoME and Materials Project already operate at a scale Telos cannot match.

Response: Telos should not compete on model scale. It should compete on evidence object portability, reviewability, and failure preservation.

## Next Proof Attempt

Use a tiny public Materials Project query or static fixture. Build a packet for one candidate with database ref, predicted property, validation status, and explicit uncertainty.

