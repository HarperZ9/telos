# Brief 146 - SAIR As A Math Research Infrastructure Signal

Pass 0136 adds SAIR to the research substrate map. The strongest signal is not generic AI-for-science branding; it is the move from talks and challenge pages into public judges, Lean harnesses, exact reasoning tasks, and large theorem/counterexample graphs.

Primary wedge: `Competition Proof Packet`.

Why it matters:

- SAIR-style challenges provide bounded tasks that can be turned into reproducible proof packets.
- The Stage 1 and Stage 2 repositories expose the shape of the missing product: source refs, task definitions, model/tool attempts, judge commands, proof certificates, counterexamples, and replayable verdicts.
- The Terence Tao video is useful as an infrastructure thesis lead: proof generation and verification are not enough if institutions cannot digest the volume of AI-era results.
- This intersects directly with Telos, Crucible, Index, Gather, Model Foundry, and BuildLang/buildc.

30-day push:

1. Build a local Stage 1 judge fixture adapter from public repo material.
2. Emit a `CompetitionProofPacket/v1` with task hash, prompt hash, model/run placeholder, verdict parser output, failure cases, and no external API dependency.
3. Add a `LeanProofReceipt/v1` skeleton for Stage 2.
4. Add a BuildLang/buildc exact modular arithmetic microbenchmark as a separate receipt branch.
5. Use Crucible to reject every packet missing source refs, judge command, expected output, negative control, or verifier status.

Market hypothesis:

Research organizations will need infrastructure for proof/result intake before they need another unbounded math chatbot. SAIR-style competitions are a public, concrete substrate for dogfooding that infrastructure.
