# Telos 0.5.0 candidate

Telos now builds scoped client packages alongside the main distribution. Windows
x64 ZIP and Claude Desktop MCPB artifacts include a pinned Node runtime and its
license. Advanced source ZIP packages retain an explicit Node prerequisite.

The plugin contains the Telos workbench skill and MCP entrypoint. It does not
install sibling tools, configure client accounts or add a model. Native control,
network and write permissions retain their existing boundaries.

Release packaging requires matching source and plugin versions, a clean exact-tag
checkout, runtime and payload checksums, real local stdio validation and exact-byte
rerun comparison. Client installation and marketplace review remain separate gates.

The integration manifest targets Gather 2.1.0, Crucible 1.4.0, Index 2.15.0 and
Forum 1.16.0. Their candidate source processes pass launch, tool-list, version and
status checks. Required tools must be present; optional tools may be absent when
their permissions are not granted. Unknown tools still cause a freshness failure.

The Index selection/freshness compatibility probe uses one temporary synthetic
repository named index, a 4,000-token budget and bounded output. It requires MATCH,
no failure codes and no omissions. A source mutation must fail the freshness
recheck. This establishes the bounded protocol contract for that fixture.
The source command `node --test demo/sibling-behavior.test.mjs` creates and removes
the fixture, resolving the manifest's PROJECT_TELOS_COMPAT_FIXTURE placeholder.
It requires the declared sibling source checkouts next to the telos directory.
The real candidate workspace at 700 tokens still overflows and remains
UNVERIFIABLE; the test rejects that response as positive acceptance. It does not
show that a full repository fits the compatibility fixture's budget.

Publication remains held until the sibling tags exist and the accepted source
and rebuilt native packages pass the release workflow.
