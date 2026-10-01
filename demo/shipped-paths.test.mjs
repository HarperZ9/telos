// Gate: no absolute workstation path ships in the npm package or the client
// plugin. A directory listing reviewer reads shipped files, and a path such as
// a drive-letter source root or a home directory tells them where the files
// came from and nothing about what the tool does. Fixtures name sources as
// {repo, commit, path, sha256} instead, so re-derivation still works from a
// clone.
//
// Negative control: run this file against the 0.6.0 tree (git show
// v0.6.0:<file>), where it fails on the revival registry, the second-level
// queue, the display-calibration contract, the four proof-packet conventions,
// learn.mjs, dft.mjs and subject.mjs.
import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

export const PATTERNS = [
  { name: "drive-letter path", re: /(?<![A-Za-z0-9])[A-Za-z]:[\\/]/g },
  { name: "home directory", re: /(?<![\w.])\/(home|Users)\/[^/\s"']+\//g },
  { name: "protected tree", re: /protected\//g },
  { name: "legacy tree", re: /legacy-repos/g }
];

// Exact substrings that match a pattern and are not workstation paths. Each
// entry names its file, so the same text elsewhere still fails.
export const ALLOWED = [
  // Chrome's default install locations, used only when the env vars are unset.
  { file: "demo/native-control/browser.mjs", text: "C:/Program Files" },
  // A detector that rejects Windows user paths in showcase packets.
  { file: "demo/showcase/schema.mjs", text: "C:\\\\\\\\Users" },
  // A captured GitHub-hosted runner log, not this workstation.
  { file: "demo/integrations/ci-triage-fixtures.json", text: "/home/runner/" }
];

export function findLocalPaths(file, text) {
  let scrubbed = text;
  for (const entry of ALLOWED) {
    if (entry.file === file) scrubbed = scrubbed.split(entry.text).join(" ".repeat(entry.text.length));
  }
  const hits = [];
  for (const { name, re } of PATTERNS) {
    for (const match of scrubbed.matchAll(re)) {
      const window = text.slice(Math.max(0, match.index - 2), match.index + 24);
      hits.push(`${file}: ${name} at ${match.index}: ${JSON.stringify(window)}`);
    }
  }
  return hits;
}

function npmFiles() {
  const r = spawnSync("npm", ["pack", "--dry-run", "--json", "--ignore-scripts"], {
    cwd: root, encoding: "utf8", shell: process.platform === "win32", maxBuffer: 1 << 26
  });
  assert.equal(r.status, 0, r.stderr);
  const start = r.stdout.indexOf("[");
  return JSON.parse(r.stdout.slice(start))[0].files.map((f) => f.path.replace(/\\/g, "/"));
}

function pluginFiles() {
  const code = [
    "import json, sys",
    "sys.path.insert(0, 'scripts')",
    "import build_client_plugin as b",
    "cfg = json.loads(b.read(b.ROOT, 'client-plugin/config.json'))",
    "data = b.payload(b.ROOT, cfg, b.version(b.ROOT, cfg))",
    "print(json.dumps({k: v.decode('utf-8', 'replace') for k, v in data.items()}))"
  ].join("\n");
  for (const py of ["python", "python3"]) {
    const r = spawnSync(py, ["-c", code], { cwd: root, encoding: "utf8", maxBuffer: 1 << 28 });
    if (r.status === 0) return JSON.parse(r.stdout);
  }
  return null;
}

function isText(buffer) {
  return !buffer.subarray(0, 8000).includes(0);
}

test("the matcher catches each kind of local path and spares URLs", () => {
  const sample = ["C:/dev/public/x", "c:\\dev\\x", "/home/alice/repo/", "/Users/bob/x/",
    "protected/legacy-repos/y"].join("\n");
  assert.equal(findLocalPaths("demo/x.mjs", sample).length, 6);
  assert.deepEqual(findLocalPaths("demo/x.mjs", "https://example.test/home/develop/api/ and https://a.b/"), []);
  assert.deepEqual(findLocalPaths("demo/native-control/browser.mjs", "`C:/Program Files/Google`"), []);
  assert.equal(findLocalPaths("demo/other.mjs", "`C:/Program Files/Google`").length, 1);
});

test("no shipped npm file names an absolute workstation path", () => {
  const hits = [];
  for (const file of npmFiles()) {
    const buffer = readFileSync(path.join(root, file));
    if (isText(buffer)) hits.push(...findLocalPaths(file, buffer.toString("utf8")));
  }
  assert.deepEqual(hits, []);
});

test("no client plugin payload file names an absolute workstation path", (t) => {
  const payload = pluginFiles();
  if (!payload) return t.skip("python unavailable to stage the plugin payload");
  const hits = [];
  for (const [name, text] of Object.entries(payload)) {
    const file = name.replace(/^server\//, "");
    if (!text.includes("\u0000")) hits.push(...findLocalPaths(file, text));
  }
  assert.deepEqual(hits, []);
});
