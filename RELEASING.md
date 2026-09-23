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
3. Tag and push the tag. The tag comes from `package.json`, so it cannot name a
   different version:
   ```bash
   VERSION="v$(node -p "require('./package.json').version")"
   git tag "$VERSION"
   git push origin "$VERSION"
   ```
4. Create the GitHub release for the tag. Publishing the release triggers
   `release.yml`, which re-runs the test suite, builds the `npm pack` tarball
   and a zip with the exact same files under `telos/`, and attaches both plus
   `SHA256SUMS.txt`. It checks out the requested tag for testing and packaging.
   Alternatively, dispatch the workflow manually with the tag as input.
   Nothing attached is overwritten. The builds are reproducible, so a re-run
   after fixing credentials needs no cleanup. It passes when the attached files
   are exactly the files it just built and each one verifies against the new
   `SHA256SUMS.txt`. Any other attached set is refused.
5. npm publish runs from `release.yml` and stays skipped unless the repository
   variable `NPM_PUBLISH_ENABLED` is `true`. Before uploading it runs these
   checks in order:
   - The tag matches the declared version.
   - `repository.url` names the repository the workflow runs in.
     `--provenance` refuses a mismatch with E422.
   - The credentials are usable.
   - The packed tarball installs into a clean project and serves MCP through
     its bin shim.
   - `npx -y file:<tarball>` starts the server through npm's own bin selection.

   It then publishes that same tarball with `--provenance`.

   npm cannot configure trusted publishing for a package name that does not
   exist yet. So the first publish of a name needs `NODE_AUTH_TOKEN` from the
   `NPM_TOKEN` secret, and that token must be allowed to create a package. On
   npmjs.com that is a granular access token with read and write permission on
   **all packages**, with two-factor bypass enabled for automation. A token
   limited to named packages authenticates and lets provenance sign. Then the
   upload fails with `E404 Not Found - PUT`. npm answers 404 here, not 403, so
   the response does not reveal whether a name exists.

   After the first version is on the registry, configure a trusted publisher
   for the package on npmjs.com (repository `HarperZ9/telos`, workflow
   `release.yml`, environment `npm`), delete the `NPM_TOKEN` secret, and revoke
   the token. The same job then publishes over OIDC with no stored credential.

## What stays operator-only

- Creating or pushing tags.
- Creating or publishing GitHub releases.
- Any `npm publish`. The workflow can run one, and it stays skipped until the
  operator sets `NPM_PUBLISH_ENABLED`.
- Rotating or configuring tokens. No publish token is stored in this repo; the
  workflow reads it from a repository secret the operator controls.

## Verifying the package locally

```bash
VERSION="$(node -p "require('./package.json').version")"
npm pack --dry-run          # inspect the shipped file list
npm pack                    # build the tarball
python tools/release_artifacts.py --tarball "project-telos-mcp-$VERSION.tgz" --tag "v$VERSION" --output-dir release-check
npm install -g "./project-telos-mcp-$VERSION.tgz"
telos catalog --summary
telos-mcp                   # stdio MCP server; send {"jsonrpc":"2.0","id":1,"method":"tools/list"}
```

The archive validator rejects a missing standalone verifier, entrypoints or
native helpers, version/tag mismatches, links, traversal paths, hidden files,
and files outside the reviewed
package layout. These package controls do not establish live device control or
provider conformance. The five sibling source-launch gate remains a separate
check; sibling servers are not bundled in the npm package or zip.
