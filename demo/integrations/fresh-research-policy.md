# Fresh Research Policy

Project Telos tools must not rely on remembered facts for living tool, API, model, medical, scientific, regulatory, academic, or market claims.

## Rule

Before a tool or operator-facing report states a current claim about an external scientific, medical, academic, AI-tool, archive, API, model, licensing, or regulatory surface, it must attach current source evidence or mark the claim `UNVERIFIABLE`.

## Evidence Priority

1. Primary official documentation or API docs.
2. Peer-reviewed publications, preprints, registries, or model cards with clear provenance.
3. Reputable reporting only for announcements or critique when no primary technical evidence exists.

## Tool Behavior

- `gather` refreshes current sources and records receipts.
- `index` maps which sources and domains are in play.
- `forum` routes the request to the right research or verification lane.
- `crucible` turns repeated claims into falsifiable checks.
- `telos` reconciles the chain into a witnessed action record.

## Medical And Scientific Boundaries

- Medical, diagnostic, clinical, therapeutic, biomedical, and wet-lab claims require current evidence and should be phrased as evidence status, not advice.
- Emerging systems such as Midjourney Medical are monitored as claims and evidence until clinical, regulatory, and API support is proven.
- Model outputs such as AlphaFold predictions are artifacts with inputs, version, confidence, license, and provenance, not experimental truth by themselves.

## Full-Text Access Boundary

- Lawful open-access resolution is part of the research stack: Unpaywall, PubMed Central, Europe PMC, DOAJ, CORE, publisher OA links, institutional repositories, preprints, and official dataset/model repositories.
- Sci-Hub, shadow libraries, leaked PDFs, and other illicit full-text sources are not valid provenance sources for Project Telos tooling.
- User-provided Sci-Hub, shadow-library, leaked-PDF, or paywalled-copy references may be recorded only as non-evidentiary source leads. Hash the lead reference, extract bibliographic identifiers, and cross-reference DOI, title, authors, PMID/PMCID, arXiv id, publisher metadata, repository metadata, and open-access resolvers to find the lawful source.
- If lawful full text is unavailable, record metadata, abstracts, citations, license/access attempts, and mark full-text evidence `UNVERIFIABLE` instead of bypassing access controls.
