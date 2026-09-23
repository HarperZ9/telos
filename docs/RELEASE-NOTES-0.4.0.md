# Project Telos 0.4.0

The first npm release. `project-telos-mcp` is on the registry, so an MCP host
can reach the stdio server without a source checkout:

```bash
npx -y project-telos-mcp telos-mcp
```

or install both commands, `telos-mcp` for the MCP server and `telos` for the
demo command surface:

```bash
npm install -g project-telos-mcp
```

Zero runtime dependencies. Node 20 or newer.

## Breaking: the MCP server reports a different name

`initialize` now returns `serverInfo.name` of `telos`. It returned
`project-telos-telos` from June 2026 through 0.3.0.

That string was introduced in a single commit and referenced by nothing except
the one assertion guarding it. No document named it. Every sibling flagship
reports its short name, so this reads as a concatenation slip rather than a
choice, and publishing to a registry would have turned it into an interface.
Anything matching on the old value needs updating.

`serverInfo.version` is unchanged in meaning and now comes from `package.json`.

## Version reporting

The version was written out in eight places. One was guarded: a test bound the
MCP `serverInfo` version to the manifest. The four action-envelope sites had no
check, so a bump could leave `telos.status`, `telos.doctor`, the room summary
and the flagship workflow all reporting the previous version while the suite
stayed green.

`demo/version.mjs` reads `package.json` once and everything reads from there.
`demo/version-alignment.test.mjs` binds the module constants, the value
`initialize` returns, the three envelope surfaces, the freshness expectation
Telos holds for itself, and the README version badge.

## Freshness expectations re-observed

`telos.mcp.freshness` compares a live server against the manifest's declared
surface. Three expectations had gone stale, so it would report DRIFT against a
server that is current and tell the operator to restart something healthy.

| server | was | now |
|---|---|---|
| gather | 1.6.1 | 1.8.2 |
| index | 2.9.0 | 2.13.0 |
| forum | 1.13.0 | 1.14.0 |
| crucible | 1.2.0 | unchanged |

Taken from the live servers. Tool surfaces were compared at the same time and
all four matched exactly, so only versions and status lines moved.

## Checks that existed but were not running

Four, all found by running them rather than reading them.

**21 of 65 test files were never named in CI.** The workflow listed files by
hand. `npm test` now globs `demo/**/*.test.mjs`, so a new test file runs without
being added anywhere.

**The sibling flagships were checked out at main** while the manifest declares
their released surfaces, so CI tested a combination Telos does not claim to
support. Each sibling is now checked out at the tag matching its
`expected_version`, read from the manifest.

**The smallharness fixture pack could not verify off Windows.** Its receipts
carry a SHA-256 over each fixture file's bytes and nothing pinned the line
ending, so the committed digests were CRLF values. `.gitattributes` pins the
pack to LF and the receipts carry the digests of the committed bytes.

**A documented release gate was never invoked.** `RELEASING.md` lists
`python tools/test_release_artifacts.py` among the required checks and neither
workflow ran it. It runs in both now, and it caught a real problem immediately.

## An honest null in the hyphal benchmark

`demo/hyphal-context-benchmark.test.mjs` replays commits recorded in a
correction packet. Those commits predate a history rewrite and survive only on
local branches that were never pushed, so a fresh clone cannot reach any of
them.

CI had absorbed this with `|| true`, which suppressed the entire file and its
roughly thirty other assertions. The replay now runs when the commits are
present and prints an `UNVERIFIABLE` line naming which are missing and why when
they are not. In CI that reads 4 of 4 unreachable.

The provenance claims in that benchmark cannot be reproduced from a public
clone. That was true before this release and is now stated on every run instead
of hidden.

## Publishing

`release.yml` gains an npm publish job, gated on the repository variable
`NPM_PUBLISH_ENABLED`. Before uploading it checks the tag against the declared
version, records the tarball digest, installs the packed tarball into a clean
project, and drives the real stdio server out of that install. It publishes with
`--provenance`.

npm cannot configure trusted publishing for a package name that does not exist,
so the first publish of a name needs a token. Later releases can run on OIDC
alone.

## Does not prove

Package controls check archive layout, entry points and version agreement. They
do not establish live device control, provider conformance, or that any receipt
is semantically true. A consistent hash chain does not establish execution
success or authorship.
