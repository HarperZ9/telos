# Frontier R&D Operating Posture

Date: 2026-07-02
Status: active scope update

## Scope Statement

Project Telos includes frontier R&D across advanced computation, AI/ML,
mathematics, physics, biology, medicine, robotics, cybernetics, quant, finance,
color/rendering/scientific compute, nuclear and energy systems, defense-adjacent
technology, and other high-stakes technical domains when the work is framed as
research, measurement, safety, assurance, simulation, verification, education,
or accountable tooling.

This supersedes any narrower roadmap posture that treated military-adjacent or
defense-adjacent work as out of scope by default. The active rule is not "avoid
the domain." The active rule is "route the domain through evidence, safety,
publication, and receipt boundaries."

## Boundary

Allowed public work:

- Source-led research packets.
- Market and tooling comparisons.
- Scientific or engineering measurement methods.
- Reproducible toy fixtures.
- Safety, assurance, verification, and red-team-resilient publication framing.
- BuildLang/buildc receipts for bounded compute kernels.
- Crucible gates that label claims `MATCH`, `DRIFT`, or `UNVERIFIABLE`.
- Learning Forge objects that teach concepts without turning high-risk details
  into operational instructions.

Fenced or internal by default:

- Raw high-risk implementation payloads.
- Operational instructions that enable harm.
- Credential, exploit, evasion, or target-specific offensive material.
- Unreviewed lab protocols, biochem procedures, or nuclear engineering details
  beyond public-source, non-operational, measurement-safe summaries.
- Private transcripts, customer data, private runbooks, or unpublished third
  party IP.

## Publication Rule

Public docs can name high-stakes domains. They must also name:

1. The source basis.
2. The measured claim.
3. The non-claims.
4. The negative controls or failure condition.
5. The reason the artifact is safe to publish.
6. The internal boundary for anything not safe to publish.

If those six items are missing, the artifact is not ready for public release.

## Domain-Specific First Packets

| Domain | First public-safe packet | Internal/fenced boundary |
| --- | --- | --- |
| Nuclear and energy | Source-to-simulation packet with public sources, units, uncertainty, regulatory-state references, and non-claims. | Operational design, enrichment, plant safety conclusions, or sensitive implementation details. |
| Biochem and medicine | Literature/causal/instrument measurement packet with no clinical action recommendation. | Lab protocols, wet-lab execution, diagnosis, treatment, or synthesis instructions. |
| Defense-adjacent systems | Assurance, simulation, logistics, safety, reliability, verification, or materials measurement packet. | Operational targeting, weapons-use instructions, evasion, or misuse-enabling details. |
| Cybernetics and robotics | Controller stability, safety envelope, trace replay, and simulation packet. | Deployment instructions for unsafe autonomous action or real-world safety claims without review. |
| AI/ML | Dataset/eval/model-foundry receipt with contamination checks and budget ledger. | Proprietary data, unsafe model capability deployment, or unsupported benchmark superiority. |
| Quant and finance | Backtest receipt with data version, split, costs, baseline, and paper/live boundary. | Investment advice, live capital instructions, or return guarantees. |
| Quantum computing | Stabilizer, Clifford, decoder, or resource-estimation packet with explicit error model. | Hardware, cryptographic, advantage, or fault-tolerance claims without primary evidence. |
| Security | Defensive scan, patch, release, redaction, provenance, or audit packet. | Unauthorized exploitation, credential acquisition, stealth, persistence, or evasion instructions. |

## Tooling Implication

The broader mission increases the importance of the proof substrate. It does
not reduce it.

- Gather must classify source sensitivity and provenance.
- Index must preserve public/internal boundaries in context envelopes.
- Forum must route high-risk lanes to the right review path.
- Crucible must keep unsupported claims `UNVERIFIABLE`.
- Telos must bind actions to receipts and publication decisions.
- BuildLang/buildc must make compute kernels re-runnable and receipt-bearing.
- Learn must convert research into safe functional learning objects.

## Review Standard

For each new frontier packet, answer these before publication:

- What exact claim is being made?
- What exact evidence supports it?
- What exact experiment or replay would falsify it?
- What details were deliberately withheld, summarized, or internalized?
- What market or scientific need does this packet answer?
- Which tool in the Telos/Build ecosystem becomes stronger because this packet
  exists?
