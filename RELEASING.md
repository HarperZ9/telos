# Releasing Project Telos

Releases are prepared in the repo and cut by the operator. Nothing publishes
automatically: pushing a branch never tags, releases, or uploads anything.
The release workflow (`.github/workflows/release.yml`) only runs on manual
dispatch or when the operator publishes a GitHub release.

## Gates

Every release candidate must pass the same gates CI runs:

```bash
# Contract tests (the list in .github/workflows/ci.yml)
node demo/action-receipt.test.mjs
# ... every demo/*.test.mjs named in ci.yml ...

# MCP surface and source-checkout launch gate
npm run test:mcp
python tools/test_release_artifacts.py

# Room and workflow smoke
node demo/catalog.mjs --summary
node demo/server-manifest.mjs --summary
node demo/room.mjs --json
node demo/flagship-workflow.mjs
```

`npm run test:mcp` and `demo/flagship-workflow.mjs` need the sibling flagship
checkouts (`gather`, `crucible`, `index`, `forum`) next to the `telos`
directory, and the checkout directory must be named `telos`.

## Version pins

The version is declared in more than one place and the freshness system
verifies they agree. When bumping, change all of them together:

- `package.json` `version`
- `demo/telos-mcp.mjs` `serverInfo.version` (test-enforced against package.json)
- `demo/status.mjs` `toolVersion` and the leading version in `current_status`
- `demo/integrations/mcp-server-manifest.json` telos `expected_version` and
  `expected_current_status` (must equal the status.mjs string exactly)
- `demo/doctor.mjs`, `demo/room.mjs`, `demo/flagship-workflow.mjs` `toolVersion`
- README version badge and the Current status Release line

## Cutting a release (operator-only)

1. Confirm the gates above are green on `main`.
2. Update `CHANGELOG.md` and the release notes under `docs/`.
3. Tag and push the tag:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```
4. Create the GitHub release for the tag. Publishing the release triggers
   `release.yml`, which re-runs the test suite, builds the `npm pack` tarball
   and a zip with the exact same files under `telos/`, and attaches both plus
   `SHA256SUMS.txt`. It checks out the requested tag for testing and packaging.
   Alternatively, dispatch the workflow manually with the tag as input.
   Existing output and release asset names are refused rather than overwritten.
5. npm publish, if and when wanted, is a separate manual operator step. There
   is no automated npm publish anywhere in this repo.

## What stays operator-only

- Creating or pushing tags.
- Creating or publishing GitHub releases.
- Any `npm publish`.
- Rotating or configuring tokens. No publish tokens are stored in this repo.

## Verifying the package locally

```bash
npm pack --dry-run          # inspect the shipped file list
npm pack                    # build the tarball
python tools/release_artifacts.py --tarball project-telos-mcp-0.2.0.tgz --tag v0.2.0 --output-dir release-check
npm install -g ./project-telos-mcp-0.2.0.tgz
telos catalog --summary
telos-mcp                   # stdio MCP server; send {"jsonrpc":"2.0","id":1,"method":"tools/list"}
```

The archive validator rejects missing entrypoints or native helpers, version/tag
mismatches, links, traversal paths, hidden files, and files outside the reviewed
package layout. These package controls do not establish live device control or
provider conformance. The five sibling source-launch gate remains a separate
check; sibling servers are not bundled in the npm package or zip.
