// Which executable `npx <package>` runs, and whether npm rewrites the bin map.
//
// npm exec picks a bin from the published manifest with one rule, in
// libnpmexec/lib/get-bin-from-manifest.js: if every bin points at the same
// file, run the first; otherwise run the bin named after the package (scope
// stripped); otherwise fail with "could not determine executable to run".
//
// 0.4.0 declared two bins, `telos` and `telos-mcp`, pointing at different
// files, and none named `project-telos-mcp`. So the README's
// `npx -y project-telos-mcp telos-mcp` could never start anything: npx treats
// the trailing `telos-mcp` as an argument, not a bin choice, and fails before
// it gets that far. Nothing checked it, because every gate launched the server
// with `node demo/telos-mcp.mjs` and never went through a bin.
//
// The rule is copied rather than imported: libnpmexec lives inside the npm
// install, not in this package's dependencies, and this package has none.

// npm publish rewrites "./demo/x.mjs" to "demo/x.mjs" in the manifest it
// uploads and reports it as "script name ... was invalid and removed", which
// reads as a deletion but is a rename. Normalizing here matches what the
// registry serves.
export function normalizeBinTarget(target) {
  return target.replace(/\\/g, "/").replace(/^(\.\/)+/, "");
}

export function npxBin(manifest) {
  const bin = typeof manifest.bin === "string"
    ? { [manifest.name.replace(/^@[^/]+\//, "")]: manifest.bin }
    : manifest.bin ?? {};
  const targets = Object.values(bin).map(normalizeBinTarget);
  if (targets.length > 0 && new Set(targets).size === 1) {
    const name = Object.keys(bin)[0];
    return { name, target: targets[0] };
  }
  const name = manifest.name.replace(/^@[^/]+\//, "");
  if (bin[name]) return { name, target: normalizeBinTarget(bin[name]) };
  return null;
}
