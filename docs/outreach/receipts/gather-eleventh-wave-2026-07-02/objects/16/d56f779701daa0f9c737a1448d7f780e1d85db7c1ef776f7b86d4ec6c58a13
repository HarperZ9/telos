# Pass 0029 Adversarial Steelman

Date: 2026-07-01

## Strongest Objection

The pass is still too easy because it validates source-positioning claims from
a README, not the correctness of the mathematical results. A buyer will not pay
for a packet that only says "the source says this"; a research lab needs
evidence that the claim is true, reproducible, and reviewable.

## Response

Accepted. The pass intentionally does not claim proof correctness. It proves a
smaller but necessary substrate law for research tooling:

```text
source-positioning claims must not be promoted into correctness claims without
additional verification artifacts.
```

The usefulness is not the depth of the `pipeline-math` review. The usefulness is
the rejection gate that prevents an agent from turning public source intake into
unsupported proof or market conclusions.

## Failure Modes Preserved

| Failure mode | Expected handling |
| --- | --- |
| Source text changes after 2026-07-01 | Future replay must fetch and compare a new digest. |
| README process claim is inaccurate | This pass cannot detect it; it only records source positioning. |
| Paper proof is incorrect | Remains `UNVERIFIABLE` until independent proof review or formal replay. |
| Lean formalization is unavailable or partial | Remains a source claim, not a replayed formal proof. |
| Network or console browser capture is missing | Remains `UNVERIFIABLE` from pass 0028. |
| Telos uniqueness is asserted | Must stay a hypothesis unless comparison rows prove it. |
| "All fields of science" is asserted | Must stay blocked until field-specific packets reproduce results. |

## Required Next Evidence

To move beyond source-positioning:

1. Fetch a specific paper and formal artifact from `pipeline-math`.
2. Build a claim graph from theorem statement to proof dependency.
3. Re-run available Lean formalizations in a pinned environment.
4. Store compile logs, theorem names, dependency hashes, and failure modes.
5. Bind model/tool actions through action receipts.
6. Run Crucible over theorem-level measurements.

## Product Implication

The immediate market wedge is not "Telos solves open problems." The immediate
wedge is:

```text
Telos can make every research automation claim carry a receipt trail that says
what is verified, what is only source-backed, and what is blocked.
```

That is the layer research labs, agent-ops teams, and scientific-compute teams
need before letting autonomous research loops influence funding, publication,
runtime configuration, or downstream experiments.

Current promoted natural laws: none.
