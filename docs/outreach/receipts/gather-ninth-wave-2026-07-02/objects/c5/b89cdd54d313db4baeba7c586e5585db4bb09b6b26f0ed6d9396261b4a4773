# Project Telos Demo Packages

Date: 2026-07-02

This file is the demo backlog for the parallel Codex posting session. Each package is written so a public-facing session can pick one, run the commands, capture screenshots or terminal output, and post without inventing claims.

Second-wave update: Learn, BuildLang/buildc, and Emet are now source-checkout demo-ready. Use `docs/outreach/SECOND-WAVE-DEMO-PACKAGES-2026-07-02.md` for the newest exact commands and boundaries. The sections below remain the first-wave backlog.

## Demo 1: 70-Tool MCP Freshness And Compatibility

Core message: Telos does not ask a host to trust that its MCP servers are fresh. It checks the loaded surface against declared versions, tools, and probes.

Evidence commands:

```powershell
npm.cmd run catalog
npm.cmd run manifest
node demo/compatibility-doctor.mjs --summary
node demo/operator-doctor.mjs --summary
node --test demo/telos-mcp.test.mjs demo/mcp-server-launch.test.mjs
```

Expected current result:

- Catalog: 70 total, 70 available.
- Manifest: 70 expected.
- Compatibility doctor: 14/14, `MATCH`.
- Operator doctor: 14/14, `MATCH`.
- MCP launch parity test: pass.

Audience: AI infrastructure teams, MCP users, agent-tooling builders.

Post angle: "MCP drift is a real failure mode. Telos treats the tool list itself as evidence."

## Demo 2: Source Federation Research Proof Packet

Core message: frontier research intake needs source admission, warning policy, and falsifiable packets before synthesis.

Evidence files:

- `docs/research/dogfood/packets/161-frontier-problem-source-federation.md`
- `docs/research/dogfood/briefs/161-frontier-problem-source-federation-brief.md`
- `docs/research/dogfood/pass-0151-ledger.md`
- `docs/research/dogfood/crucible/pass-0151-run.json`

Evidence commands:

```powershell
python -m pytest docs\research\dogfood\tools\test_frontier_problem_source_federation.py -q
python docs\research\dogfood\tools\validate_pass_0151_frontier_problem_source_federation.py
gather corpus verify docs\research\dogfood\gather\pass-0151-frontier-problem-source-federation --json
```

Expected current result:

- 83 candidate sources.
- 15 source families.
- 40 domains.
- 24 Gather-verified captures.
- 12 problem lanes.
- 8 admission gates.
- Crucible verification with no promoted theorem or natural-law claim.

Audience: AI4Science, research labs, academic tool builders.

Post angle: "The hard part is not summarizing papers. It is knowing which sources were admitted, which warnings were preserved, and which claims were not promoted."

## Demo 3: Agent Action Proof Packet

Core message: agent work should leave a packet that shows context, proposed action, admission, execution, and verification.

Evidence commands:

```powershell
node demo/context-pack.mjs
node demo/action-receipt.mjs
node demo/loop-ledger.mjs
node demo/browser-evidence.mjs
```

Expected current result:

- JSON contracts for context pack, action receipt, loop ledger, and browser evidence.
- No external writes.
- No raw private paths in public packet.

Audience: regulated agent workflows, AI infra buyers, internal platform teams.

Post angle: "Tracing tells you what happened. A proof packet tells you what was allowed, what changed, and what can be re-checked."

## Demo 4: Learn Prooflesson Loop

Core message: learning tools should help the learner produce evidence, not let a model do graded work.

Evidence source:

- `C:\dev\public\learn\README.md`

Current source-checkout commands:

```powershell
node C:\dev\public\learn\src\cli.mjs status
node C:\dev\public\learn\src\cli.mjs doctor
node C:\dev\public\learn\src\cli.mjs tutor plan mysession --topic "derivatives" --objectives "power-rule,chain-rule"
node C:\dev\public\learn\src\cli.mjs tutor record mysession --objective power-rule --prompt "d/dx x^3" --answer "3x^2" --correct true
node C:\dev\public\learn\src\cli.mjs tutor study mysession --now 2026-07-02T00:00:00Z
node C:\dev\public\learn\src\cli.mjs tutor study-receipt mysession --now 2026-07-02T00:00:00Z
node C:\dev\public\learn\src\cli.mjs tutor reverify mysession
```

Packaging work needed:

- Run from a temp directory to avoid writing demo tutor state into the repo.
- Add a Telos proof-packet lesson bridge as a follow-up.

Audience: educators, self-learners, credential platforms, research training programs.

Post angle: "The tutor should create pressure to retrieve and prove, not bypass the learner."

## Demo 5: BuildLang Effect Receipt And Build Color Measurement

Core message: BuildLang/buildc can become the accountable scientific runtime lane, while Build Color gives a visual measurement domain that people can inspect.

Evidence sources:

- `C:\dev\public\pubscan\quantalang\README.md`
- `C:\dev\public\build-color\README.md`
- `docs/research/dogfood/packets/020-buildlang-scientific-runtime-receipts.md`
- `docs/research/dogfood/packets/021-color-calibration-proof-kit.md`

Current source-checkout commands:

```powershell
cargo run --target-dir C:\Users\Zain\AppData\Local\Temp\buildlang-codex-target-20260702 --manifest-path compiler\Cargo.toml --bin buildc -- doctor
& C:\Users\Zain\AppData\Local\Temp\buildlang-codex-target-20260702\debug\buildc.exe check examples\quickstart\hello.bld --receipt -
& C:\Users\Zain\AppData\Local\Temp\buildlang-codex-target-20260702\debug\buildc.exe corpus verify
```

Packaging work needed:

- `buildc` is not on PATH in this shell.
- Use isolated Cargo target until the default Windows target lock is cleared.
- Add policy receipt verify and pair one `.bld` receipt with a Telos/Crucible measurement packet.

Audience: compiler people, scientific computing, visual computing, finance/security runtime buyers.

Post angle: "A language for scientific work should make effects and receipts visible, not just run fast."

## Demo 6: Emet External Witness

Core message: Emet is the small external witness: same bytes, same verdict, no in-band trust claims.

Evidence source:

- `C:\dev\public\pubscan\emet\README.md`

Candidate commands from README:

```powershell
python membrane.py selftest
python conformance/run.py membrane.py
python test_forward_delivery_contract.py
python test_membrane.py
```

Current boundary:

- `emet` is on PATH but fails in this shell with `ModuleNotFoundError: No module named 'warden_shell'`.
- Checkout commands pass selftest and 35/35 conformance vectors; use checkout commands until the wrapper is fixed.

Audience: security-minded AI users, reviewers, release engineers.

Post angle: "The witness has three answers: `MATCH`, `DRIFT`, `UNVERIFIABLE`. Not trusted. Not approved. Just re-derived."

## Demo Packaging Order

1. MCP freshness and 70-tool compatibility.
2. Source federation proof packet.
3. Agent action proof packet.
4. Learn prooflesson.
5. BuildLang effect receipt plus Build Color measurement.
6. Emet witness.
