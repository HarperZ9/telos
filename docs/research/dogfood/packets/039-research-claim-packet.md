# Packet 039: Executable Research Claim Packet

Date: 2026-07-01

Status: `PROBE_MATCH`

This pass turns the previous source/browser evidence binding into a small,
market-facing research claim packet. The target is not to prove
`pipeline-math`; the target is to show the product shape Telos needs for
AI4Science and research-lab buyers:

```text
public source -> extracted claim -> source receipt digest -> action receipt proposal -> verifier measurement -> unsupported-promotion rejection
```

## Source Anchor

Public source:

```text
https://raw.githubusercontent.com/Pengbinghui/pipeline-math/main/README.md
```

Observed through web source intake on 2026-07-01.

Source receipt:

```text
path = fixtures/pipeline-math-source-receipt-pass-0029.json
schema = PublicSourceReceipt/v1
sha256 = fcc8d3d9dea488bfd4dee9bbc9898cde12472df26ecbcc3665aaaae9d045bf62
seal = 280633352b3f7c285f167f846d816b5b7de2efdfbc79ce13c418efaa6bc2a76b
verification_status = verified
confidence = high
raw_page_material_required_for_replay = false
```

The source receipt records three source-backed claims:

1. The README positions the repository as collecting resolutions of open
   problems from COLT, commutative ring theory, an Erdos problem, and a FOCS
   2023 open question.
2. The README says proof discovery used a simple prover-verifier pipeline,
   with papers assembled in Claude Code and then polished and verified by the
   authors.
3. The README says commutative-ring-theory solutions are formalized in Lean
   using an agentic Lean formalization pipeline, with open source release
   pending.

## Prior Telos Evidence Binding

Pass 0029 binds to the pass 0028 source/browser evidence receipt so the
research-claim packet is not isolated from the action/evidence layer.

```text
path = schemas/source-evidence-binding-pass-0028.json
schema = SourceEvidenceBindingSet/v1
sha256 = 75aeda5b9afa02eb1da746aa319d2908a7895f26aefe5d1949d1d949ff3c0f32
seal = 879c147a7c755ca357eaf07802a893cb6a3a92752af0664a3ea2e1ec9565337e
network_summary_verdict = UNVERIFIABLE
console_summary_verdict = UNVERIFIABLE
```

Those `UNVERIFIABLE` states must remain `UNVERIFIABLE`. They cannot be
converted into a successful live-browser or production-capture claim.

## Research Claims

The packet contains five claims:

| Claim id | Status | Boundary |
| --- | --- | --- |
| `rc_pipeline_math_scope` | `verified` | Source-positioning claim only. |
| `rc_pipeline_math_prover_verifier` | `verified` | README process claim only. |
| `rc_pipeline_math_lean_formalization` | `verified` | README formalization-positioning claim only. |
| `rc_pipeline_math_proof_correctness` | `UNVERIFIABLE` | Requires independent proof review or formal replay. |
| `rc_pipeline_math_future_currentness` | `UNVERIFIABLE` | Requires future fetch and digest comparison. |

The three verified claims are useful for market mapping. They are not proof of
the mathematical results. They are not proof that the approach generalizes to
all scientific fields.

## Research Claim Packet

Primary packet:

```text
path = schemas/research-claim-packet-pass-0029.json
schema = ResearchClaimPacket/v1
status = RESEARCH_CLAIM_PACKET_MATCH
claim_count = 5
verified_claim_count = 3
unverifiable_claim_count = 2
negative_fixture_count = 10
seal = 272b3afd43cd60688f06fabd11d66934796f448ba1f07a02d62a3798443a62f4
```

Validator result:

```text
path = schemas/pass-0029-research-claim-packet-validator-result.json
status = MATCH
match = 1
drift = 0
unsupported_claim_promotion_rejected = true
network_summary_verdict = UNVERIFIABLE
console_summary_verdict = UNVERIFIABLE
```

## Action Receipt Proposal

The pass defines an `ActionReceiptResearchClaimProposal/v1` event:

```text
action_id = act_dogfood_0029_research_claim_extract
event_id = evt_dogfood_0029_research_claim_packet
event_type = research_claim_packet_created
authority_class = read_only_research_packet
raw_source_material_required = false
raw_browser_payload_required = false
model_reasoning_required_for_replay = false
verification_verdict = MATCH
```

Inputs:

```text
artifact:fixtures/pipeline-math-source-receipt-pass-0029.json
artifact:schemas/source-evidence-binding-pass-0028.json
```

Input digests:

```text
sha256:fcc8d3d9dea488bfd4dee9bbc9898cde12472df26ecbcc3665aaaae9d045bf62
sha256:75aeda5b9afa02eb1da746aa319d2908a7895f26aefe5d1949d1d949ff3c0f32
```

## Negative Fixtures

All ten negative fixtures expect validator status `REJECT`:

```text
negative-proof-correctness-promoted
negative-future-currentness-promoted
negative-broad-science-generalization
negative-source-url-missing
negative-source-receipt-sha-drift
negative-pass-0028-binding-drift
negative-unverifiable-network-promoted
negative-unverifiable-console-promoted
negative-action-receipt-proposal-missing
negative-verifier-measurement-missing
```

## Market Reading

The market wedge is a hypothesis, not a uniqueness fact:

```text
Research proof packets can package public source intake, claim extraction,
action provenance, verifier measurements, and unsupported-promotion fences in
one portable object.
```

This matters because `pipeline-math` shows a visible market pull for
prover-verifier research loops. Telos can aim one layer lower: not only
"generate a proof attempt", but "bind every claim, source, model action,
verifier result, reproducibility gap, and rejection condition into a portable
packet".

That packet shape should feed:

- AI4Science lab due diligence;
- math/proof-result replay;
- BuildLang/buildc scientific runtime receipts;
- browser/source evidence packets;
- action-receipt ledgers;
- Crucible verification reports;
- Forum routing and adversarial review.

## Non-Promotion Boundary

This pass does not prove the mathematical correctness of `pipeline-math`
papers, broad scientific generalization, buyer adoption, Telos uniqueness
against all competitors, live browser capture, production DLP, or any natural
law.

Current promoted natural laws: none.
