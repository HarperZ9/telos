# crucible report: Project Telos Second-Wave Source-Checkout Tooling Claims

## Summary

- thesis_id: `ab5d74554f865ec4`
- thesis_seal: `ab5d74554f865ec494770d31ddca83adeafb2b393d49e7fe7466d77cf0953fc1`
- assessment_seal: `0d62b195545bb82b7a9d760106c375f3c7935e782fa60b8995f5534634defb25`
- counts: MATCH 5 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The current MCP-exposed flagship status surfaces report all five Project Telos flagships as ready with a 70-tool Telos room surface. | MATCH | fenced | 1 | mcp-status-review | deviation 0 within tolerance 0.5 |
| The Learn source checkout supports a receipt-backed research-training loop: status reports version 1.5.0, doctor reports MATCH, the targeted tutor/prooflesson/reverify test slice passes, and a temp study receipt verifies from evidence. | MATCH | fenced | 1 | source-checkout-command-review | deviation 0 within tolerance 0.5 |
| The BuildLang/buildc source checkout supports a receipt-backed compiler demo from an isolated Cargo target: doctor completes for buildc 1.0.6, the C backend is ready, hello.bld check emits a passed receipt, and corpus verify reports 8 C executions passed. | MATCH | fenced | 1 | source-checkout-command-review | deviation 0 within tolerance 0.5 |
| The Emet source checkout supports a narrow external-witness demo: selftest emits the current self hash and conformance passes 35 of 35 vectors, while the PATH wrapper remains out of scope because it still depends on a missing warden_shell module. | MATCH | fenced | 1 | source-checkout-command-review | deviation 0 within tolerance 0.5 |
| The second-wave outreach documents preserve the source-checkout boundary and add demo packages for Learn, BuildLang/buildc, Emet, and megatool composition. | MATCH | fenced | 1 | document-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The current MCP-exposed flagship status surfaces report all five Project Telos flagships as ready with a 70-tool Telos room surface. | mcp-status-review | telos_room: ready 5 / total 5, checks_passed 20 / checks_total 20, tools 70; gather_status: tool_version 1.5.0, status MATCH; index_status: tool_version 2.8.0, status MATCH; forum_status: tool_version 1.12.0, status MATCH; crucible_status: tool_version 1.1.0, status MATCH |
| The Learn source checkout supports a receipt-backed research-training loop: status reports version 1.5.0, doctor reports MATCH, the targeted tutor/prooflesson/reverify test slice passes, and a temp study receipt verifies from evidence. | source-checkout-command-review | C:\dev\public\learn\package.json: version 1.5.0; node src/cli.mjs doctor: learn doctor MATCH with 9 MATCH checks; temp CLI demo: tutor study-receipt research-proof reported verified true; node --test tests\tutor.test.mjs tests\learn-study-cli.test.mjs tests\tutor-reverify.test.mjs tests\tutor-prooflesson.test.mjs: 53 pass, 0 fail |
| The BuildLang/buildc source checkout supports a receipt-backed compiler demo from an isolated Cargo target: doctor completes for buildc 1.0.6, the C backend is ready, hello.bld check emits a passed receipt, and corpus verify reports 8 C executions passed. | source-checkout-command-review | C:\dev\public\pubscan\quantalang\compiler\Cargo.toml: package buildlang version 1.0.6; isolated-target buildc doctor: buildc 1.0.6 (windows), C backend ready via MSVC Build Tools; buildc check examples\quickstart\hello.bld --receipt -: schema buildlang-check-receipt/v1, status passed, source digest 0e542c60fbd874a38a2a3a87eaf61be04532a0df23e3ea25512d03301883dfae; buildc corpus verify: manifest 8 programs, c execution 8 passed |
| The Emet source checkout supports a narrow external-witness demo: selftest emits the current self hash and conformance passes 35 of 35 vectors, while the PATH wrapper remains out of scope because it still depends on a missing warden_shell module. | source-checkout-command-review | python membrane.py selftest: emet_self_sha256 b75ae75283ae774d4d8fc68452de34636fc5e47fd544d1d2d1c9783f1f282f1a; python conformance\run.py membrane.py: CONFORMANCE 35/35 vectors pass; docs/outreach/SECOND-WAVE-DEMO-PACKAGES-2026-07-02.md records the PATH wrapper boundary |
| The second-wave outreach documents preserve the source-checkout boundary and add demo packages for Learn, BuildLang/buildc, Emet, and megatool composition. | document-review | docs/outreach/SECOND-WAVE-DEMO-PACKAGES-2026-07-02.md exists and labels current claims as source-checkout claims; docs/outreach/SECOND-WAVE-CONTENT-QUEUE-2026-07-02.md exists and repeats the re-run-before-posting rule; docs/outreach/PARALLEL-CODEX-HANDOFF-2026-07-02.md references the second-wave package; docs/TOOLING-SHAPE-ASSESSMENT-2026-07-02.md distinguishes source-checkout evidence from PATH availability |
