# Pass 0105 Ledger: Reaction Mass-Conservation Receipt

Date: 2026-07-01

Status: `REACTION_MASS_CONSERVATION_RECEIPT_MATCH`

## Purpose

Advance the AI4Science lane from schema mapping into a bounded equation proof.
This pass proves and numerically probes the invariant for a closed first-order
reaction `A -> B` with mass-action rate `kA`.

The result is a scoped `LAW_CANDIDATE`, not a promoted natural law.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_reaction_mass_conservation_receipt.py` | Builds source anchors, symbolic proof, numerical probe, negative fixture, and Forum/Index/Telos receipts. |
| `tools/test_reaction_mass_conservation_receipt.py` | Focused TDD test for symbolic proof, numerical drift, negative fixture, and law boundary. |
| `tools/probe_reaction_mass_conservation_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0105_reaction_mass_conservation.py` | Independent validator for seal, proof, probes, negative fixture, and boundaries. |
| `schemas/reaction-mass-conservation-receipt-pass-0105.json` | `ReactionMassConservationReceipt/v1` artifact. |
| `schemas/pass-0105-reaction-mass-conservation-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0105.json` | Compact compose, test, Forum, Index, Telos, and law-candidate receipts. |
| `packets/115-reaction-mass-conservation-receipt.md` | Human-readable reaction mass-conservation packet. |
| `briefs/115-reaction-mass-conservation-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0105-reaction-mass-conservation-steelman.md` | Local pass 0105 steelman. |
| `crucible/pass-0105-thesis.json` | Falsifiable claims. |
| `crucible/pass-0105-measurements.json` | Measurements/evidence. |
| `crucible/pass-0105-report.md` | Crucible report. |
| `crucible/pass-0105-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| AI4Science source pass | 0104 |
| Reaction | `A -> B` |
| Rate law | `dA/dt=-kA; dB/dt=kA` |
| Stoichiometry | `A:-1, B:+1` |
| Invariant | `A+B` |
| Symbolic derivative | `0` |
| Grid points | 97 |
| Exact invariant drift | 0.0 |
| Euler invariant drift | `4.440892098500626e-16` |
| Negative fixture | `open_system_degradation` |
| Negative fixture drift | `0.2959392161530001` |
| Law candidate | `closed_first_order_reaction_total_mass_invariant` |
| Law status | `LAW_CANDIDATE` |
| Unsupported claim count | 0 |
| Promoted natural laws | 0 |
| Artifact file SHA256 | `0d2e36ea03ec3c1685fbaf31c3139cdb709a23c7bbf4167407c637c93d85573a` |
| Artifact seal | `44d61ff374c7ac528a4c837c31e8470e5ba539c19164bb098918c436f86ca26d` |

## Source Anchors

| Source | URL | Evidence Role |
| --- | --- | --- |
| Chemical Kinetics and Mass Action in Coexisting Phases | `https://pmc.ncbi.nlm.nih.gov/articles/PMC9620980/` | Mass-action kinetics source anchor. |
| Modeling with ODE | `https://people.tamu.edu/~phoward/m647/modode.pdf` | Conservation-of-mass ODE source anchor. |
| Modeling and Analysis of Mass-Action Kinetics | `https://haddad.gatech.edu/journal/Mass_Action.pdf` | Mass-action ODE-system source anchor. |
| Law of Mass Action | `https://math.libretexts.org/Bookshelves/Applied_Mathematics/Mathematical_Biology_%28Chasnov%29/06%3A_Biochemical_Reactions/6.01%3A_The_Law_of_Mass_Action` | Textbook law-of-mass-action source anchor. |

## Product Finding

Conserved-quantity proofs are a useful first AI4Science proof class because
they are small enough to verify symbolically and numerically while exercising
the same receipt fields needed for larger scientific models: source claim,
protocol, measurement, negative fixture, review boundary, and promotion verdict.

The next architectural step is a stoichiometric-matrix invariant checker that
can discover or verify conservation laws for larger reaction networks.

## Tool Findings

- Forum route receipt: `MATCH`.
- Index context envelope: `MATCH`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `2cf9822ab75f7e574d96d60f2fffe5fee48c142efab0f97213a95b20ef965ce3`,
  digest seal `029b5eb2aaff36dafb1cfc0e90d982abaf9397dedfa64db691379733ea4784e5`.
- Gather brief receipt: SHA256
  `b816f77d92418c8acbc5d322556b419c5792a2fa7ff404d38ba25ccc0be1bcb8`,
  digest seal `aa30e73ae400ed75662f0c1b4e2fcaf0ec37219276d901e610b752848b89f2b2`.
- Crucible result: 9 claims, 9 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `483ccbf50e02b9fe`.
- Crucible assessment seal:
  `fd386bf90524d14491f6c0ddf67e1f799a9d9190732e608a0af5a523b76320e8`.
- Crucible registry stats after this pass: 94 theses, 786 claims, 786 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not prove a new natural law, biological discovery, enzyme
mechanism, or experimental result. It proves a bounded invariant for a closed
toy reaction model.

## Verification

```powershell
python docs\research\dogfood\tools\test_reaction_mass_conservation_receipt.py
python -m py_compile docs\research\dogfood\tools\compose_reaction_mass_conservation_receipt.py docs\research\dogfood\tools\test_reaction_mass_conservation_receipt.py docs\research\dogfood\tools\validate_pass_0105_reaction_mass_conservation.py docs\research\dogfood\tools\probe_reaction_mass_conservation_receipt.py
python docs\research\dogfood\tools\probe_reaction_mass_conservation_receipt.py
python docs\research\dogfood\tools\validate_pass_0105_reaction_mass_conservation.py
crucible run docs\research\dogfood\crucible\pass-0105-thesis.json --measurements docs\research\dogfood\crucible\pass-0105-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0105-report.md --out docs\research\dogfood\crucible\pass-0105-run.json --json
gather docs docs\research\dogfood\packets\115-reaction-mass-conservation-receipt.md --json
gather docs docs\research\dogfood\briefs\115-reaction-mass-conservation-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Generalize from `A -> B` to a stoichiometric-matrix invariant checker that can
derive conservation vectors for larger reaction networks and reject open-system
or leaky networks as `DRIFT`.
