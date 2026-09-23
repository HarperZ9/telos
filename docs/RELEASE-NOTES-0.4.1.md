# Project Telos 0.4.1

The first version on the npm registry. 0.4.0 was tagged and released on GitHub
but never uploaded, and it could not have worked from npm: the command its notes
gave to start the server fails before running anything.

```bash
npx -y project-telos-mcp
```

In an MCP host config that is `"command": "npx"` with
`"args": ["-y", "project-telos-mcp"]`. Installing globally still gives two
commands, `telos-mcp` for the server and `telos` for the demo command surface:

```bash
npm install -g project-telos-mcp
```

## Fixed: npx had no bin to run

npx picks the bin to run from the manifest with one rule. If every bin points at
the same file, it runs that file. Otherwise it runs the bin named after the
package, and failing that it stops with `could not determine executable to run`.
0.4.0 declared `telos` and `telos-mcp`, pointing at different files, and nothing
named `project-telos-mcp`, so `npx -y project-telos-mcp telos-mcp` stopped there.
The trailing `telos-mcp` never mattered: npx passes it to the program as an
argument and does not use it to choose one.

0.4.1 adds a `project-telos-mcp` bin that points at the server. Running the
0.4.0 command against the 0.4.0 tarball reproduces the error, and the 0.4.1
command against the 0.4.1 tarball serves `telos 0.4.1`.

Every gate before this one started the server with `node demo/telos-mcp.mjs`,
which never goes through a bin, so none of them could see it. Two checks now do:

- `demo/package-manifest.test.mjs` applies npm's rule to `package.json` and
  requires it to select the server. It also checks every `npx` line in the
  README, USAGE and release notes, that every bin target ships in the tarball
  with a node shebang, and that bin paths are already in the form npm publishes.
- The release probe launches the installed server through its bin shim, then
  runs `npx -y file:<tarball>` through npm's own bin selection.

## Fixed: provenance would have refused the upload

`--provenance` signs a statement naming the repository the workflow ran in, and
the registry refuses the upload with E422 unless `package.json` names the same
repository. 0.4.0 declared none. 0.4.1 declares `repository`, `homepage`, `bugs`
and `keywords`, and the publish job checks the repository before anything is
signed.

## Changed: the publish job uploads the bytes it tested

The job used to digest and probe one tarball, then run `npm publish` on the
checkout, which packs a second time. It now publishes the tarball it probed. A
new step checks the publish credentials first: with a token, `npm whoami` has to
succeed; with none, npm has to be 11.5.1 or newer for trusted publishing.

## Also

`npm publish` no longer rewrites the bin map. Paths written as `./demo/x.mjs`
were rewritten to `demo/x.mjs` on upload, which npm reports as "script name ...
was invalid and removed". That message describes a rename. It does not mean a
deletion. The manifest now uses the published form, so the registry serves the
same manifest the tag holds.
