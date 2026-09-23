# Releasing Project Telos

Releases are prepared in the repo and cut by the operator. Nothing publishes
automatically: pushing a branch never tags, releases, or uploads anything.
The release workflow (`.github/workflows/release.yml`) only runs on manual
dispatch or when the operator publishes a GitHub release.

## Gates

Every release candidate must pass the same gates CI runs:

```bash
# Every test. `npm test` globs demo/**/*.test.mjs, so a new test file runs
# without being added to a list anywhere.
npm test

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

Bump `package.json`. Everything that reads a version at runtime reads it from
there through `demo/version.mjs`: the MCP `serverInfo`, and the `toolVersion` in
the status, doctor, room and flagship-workflow envelopes.

Three places cannot be reached from a constant and still need a hand:

- `demo/integrations/mcp-server-manifest.json`, the telos `expected_version` and
  the leading version in `expected_current_status`
- the README version badge
- `CHANGELOG.md`

`demo/version-alignment.test.mjs` asserts all three against `package.json`, so a
missed one fails rather than shipping. It was eight hand-maintained sites before
0.4.0, and only one of them was guarded.

## Cutting a release (operator-only)

1. Confirm the gates above are green on `main`.
2. Update `CHANGELOG.md` and the release notes under `docs/`.
3. Tag and push the tag:
   ```bash
   git tag v0.4.0
   git push origin v0.4.0
   ```
4. Create the GitHub release for the tag. Publishing the release triggers
   `release.yml`, which re-runs the test suite, builds the `npm pack` tarball
   and a zip with the exact same files under `telos/`, and attaches both plus
   `SHA256SUMS.txt`. It checks out the requested tag for testing and packaging.
   Alternatively, dispatch the workflow manually with the tag as input.
   Existing output and release asset names are refused rather than overwritten.
5. npm publish runs from `release.yml` and stays skipped unless the repository
   variable `NPM_PUBLISH_ENABLED` is `true`. Before uploading it checks the tag
   against the declared version, records the tarball digest, installs the packed
   tarball into a clean project, and drives the real stdio server out of that
   install. It publishes with `--provenance`.

   npm cannot configure trusted publishing for a package name that does not
   exist yet, so the first publish of a name needs `NODE_AUTH_TOKEN` from the
   `NPM_TOKEN` secret. Once the package exists and a trusted publisher is
   configured on npmjs.com, the secret can be removed and OIDC alone is
   enough.

## What stays operator-only

- Creating or pushing tags.
- Creating or publishing GitHub releases.
- Any `npm publish`. The workflow can run one, and it stays skipped until the
  operator sets `NPM_PUBLISH_ENABLED`.
- Rotating or configuring tokens. No publish token is stored in this repo; the
  workflow reads it from a repository secret the operator controls.

## Verifying the package locally

```bash
npm pack --dry-run          # inspect the shipped file list
npm pack                    # build the tarball
python tools/release_artifacts.py --tarball project-telos-mcp-0.4.0.tgz --tag v0.4.0 --output-dir release-check
npm install -g ./project-telos-mcp-0.4.0.tgz
telos catalog --summary
telos-mcp                   # stdio MCP server; send {"jsonrpc":"2.0","id":1,"method":"tools/list"}
```

The archive validator rejects a missing standalone verifier, entrypoints or
native helpers, version/tag mismatches, links, traversal paths, hidden files,
and files outside the reviewed
package layout. These package controls do not establish live device control or
provider conformance. The five sibling source-launch gate remains a separate
check; sibling servers are not bundled in the npm package or zip.
