// The published manifest has to launch what the README says it launches.
//
// Every other gate starts the server with `node demo/telos-mcp.mjs`. A user
// starts it through a bin, usually `npx -y project-telos-mcp`, and 0.4.0
// shipped with no bin npx could select. These assertions read package.json the
// way npm reads it, so the documented command is checked instead of assumed.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { normalizeBinTarget, npxBin } from "../tools/npx-bin.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const manifest = JSON.parse(readFileSync(path.join(root, "package.json"), "utf8"));
const SERVER = "demo/telos-mcp.mjs";

// `npx -y project-telos-mcp` runs the MCP server.
const selected = npxBin(manifest);
assert.ok(selected, "npx cannot determine which bin to run for this manifest");
assert.equal(selected.target, SERVER, `npx would run ${selected.target}, not the MCP server`);

// The rule itself, against the manifest 0.4.0 shipped. If this stops failing,
// the copied rule has drifted from npm's and the assertion above proves nothing.
assert.equal(
  npxBin({
    name: "project-telos-mcp",
    bin: { telos: "./demo/telos.mjs", "telos-mcp": "./demo/telos-mcp.mjs" }
  }),
  null
);

// npm publish rewrites any bin target that is not already canonical, so the
// manifest on the registry would differ from the one in the tag.
for (const [name, target] of Object.entries(manifest.bin)) {
  assert.equal(normalizeBinTarget(target), target, `bin ${name} is not canonical: ${target}`);
}

// Each bin target ships in the tarball and starts with a node shebang. npm
// packs bin targets even when `files` excludes them, so the failure this
// catches is a bin naming a file that does not exist, which installs a
// dangling shim.
// npm is a .cmd shim on Windows and needs a shell there; the command is fixed
// text, so it goes through as one string rather than as unescaped arguments.
const packCommand = "npm pack --dry-run --json --ignore-scripts";
const pack = process.platform === "win32"
  ? spawnSync(packCommand, { cwd: root, encoding: "utf8", shell: true })
  : spawnSync("npm", packCommand.split(" ").slice(1), { cwd: root, encoding: "utf8" });
assert.equal(pack.status, 0, `npm pack --dry-run failed: ${pack.stderr}`);
const shipped = new Set(JSON.parse(pack.stdout)[0].files.map((file) => file.path));
for (const [name, target] of Object.entries(manifest.bin)) {
  assert.ok(shipped.has(target), `bin ${name} points at ${target}, which is not in the tarball`);
  const firstLine = readFileSync(path.join(root, target), "utf8").split("\n", 1)[0];
  assert.equal(firstLine.trim(), "#!/usr/bin/env node", `bin ${name} has no node shebang`);
}

// --provenance rejects the upload with E422 unless repository.url names the
// repository the workflow ran in.
const repo = String(manifest.repository?.url ?? "")
  .replace(/^git\+/, "")
  .replace(/\.git$/, "");
assert.equal(repo, "https://github.com/HarperZ9/telos");

// Every documented npx command resolves to the server through npm's rule: each
// `npx` line inside a shell code fence, and each host-config `"args"` array
// given beside `"command": "npx"`. Prose that happens to start with "npx" is
// not a command and is not read.
function documentedInvocations(text) {
  const found = [];
  let fence = null;
  for (const raw of text.split("\n")) {
    const line = raw.trimEnd();
    const marker = line.match(/^\s*```\s*([\w-]*)\s*$/);
    if (marker) {
      fence = fence === null ? marker[1].toLowerCase() : null;
      continue;
    }
    if (["bash", "sh", "shell", ""].includes(fence) && /^\s*npx\s/.test(line)) {
      found.push({ line, words: line.trim().split(/\s+/).slice(1) });
    }
  }
  for (const match of text.matchAll(/"command":\s*"npx"[\s\S]{0,40}?"args":\s*(\[[^\]]*\])/g)) {
    found.push({ line: match[0], words: JSON.parse(match[1]) });
  }
  return found;
}

const docs = ["README.md", "USAGE.md", ...readdirSync(path.join(root, "docs"))
  .filter((file) => /^RELEASE-NOTES-.*\.md$/.test(file))
  .map((file) => `docs/${file}`)];
let checked = 0;
for (const doc of docs) {
  const text = readFileSync(path.join(root, doc), "utf8");
  for (const { line, words } of documentedInvocations(text)) {
    const positional = [];
    let packageFlag = null;
    for (let i = 0; i < words.length; i += 1) {
      if (words[i] === "-p" || words[i] === "--package") packageFlag = words[++i];
      else if (words[i].startsWith("--package=")) packageFlag = words[i].slice(10);
      else if (!words[i].startsWith("-")) positional.push(words[i]);
    }
    if (packageFlag) {
      assert.equal(packageFlag, manifest.name, `${doc}: ${line}`);
      assert.equal(normalizeBinTarget(manifest.bin[positional[0]] ?? ""), SERVER, `${doc}: ${line}`);
    } else {
      assert.deepEqual(positional, [manifest.name], `${doc}: npx runs one bin; drop the extra word in: ${line}`);
    }
    checked += 1;
  }
}
assert.ok(checked > 0, "no npx command found in the docs; the check above ran on nothing");
