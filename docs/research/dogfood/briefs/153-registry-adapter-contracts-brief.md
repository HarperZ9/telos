# Pass 0143 Brief - Registry Adapter Contracts

Primary push: implement the adapter contract layer before attempting larger source crawling or theorem solving.

Shape: 6 repository-directory fixtures, 8 scholarly-graph fixtures, 15 join keys, and 10 negative fixtures.

Why it matters: large-scale research tools fail when source discovery, identifier joins, license state, version state, and verification verdicts are separated. These contracts make each join replayable before downstream AI, BuildLang/buildc kernels, or proof assistants consume it.

Next pass: instantiate one live, bounded institution graph from ROR plus repository-directory plus scholarly-graph adapters, while preserving all non-promotion boundaries.
