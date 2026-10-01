// Tripwire for the rule that no Telos surface ships CAPTCHA solving, bot-check
// token harvesting, fingerprint spoofing or automation hiding. PR #52 removed
// that code; this file fails if it comes back under its old names.
//
// Static reads only. It never imports a driver module or starts a browser. It
// checks names: module files, import specifiers, dependencies, tool and verb
// names, exported functions, and environment variables. A capability renamed
// to something innocuous passes this file, so code review still owns the rule.
// Prose is not scanned, so a policy line or a detect-and-stop gate can still
// say the word CAPTCHA.
import test from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { tools as mcpTools } from "./telos-mcp.mjs";

const self = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(self), "..");

const SKIP_DIRS = new Set([".git", "node_modules", ".release", "release-check"]);
const BINARY = /\.(png|jpe?g|gif|webp|ico|woff2?|ttf|otf|pdf|zip|tgz|gz|7z|mp4|mp3|wav)$/i;
const CODE = /\.(mjs|cjs|js|py|ps1)$/i;

const FORBIDDEN_MODULE = /captcha|stealth|undetected|puppeteer-extra|playwright-extra|ghost-cursor|fingerprint-(injector|generator|suite)|capsolver|anticaptcha|nopecha|anti-?bot|bot-?bypass/i;
const FORBIDDEN_NAME = /captcha|stealth|spoof|evasion|antibot|anti_bot|botbypass/i;
const FORBIDDEN_EXACT_NAME = new Set(["warmup", "humanmove", "recaptchatoken"]);
// Input helpers named for imitating a person (humanClick, humanType, ...). 0.5.0
// shipped these with randomized keystroke timing; 0.6.0 replaced them with
// fixed-pace pointerClick/typeText/typeKeys.
const FORBIDDEN_HUMAN_INPUT = /^human_?(?:click|type|typekeys|keys|move|mouse|scroll|delay|pause|jitter|like)/i;
// Bare verbs that were only CAPTCHA entry points on the native-control surface.
const FORBIDDEN_NATIVE_VERB = new Set(["token", "solve"]);
// Upper snake case containing an underscore, so prose "CAPTCHA" is not an env var.
const FORBIDDEN_ENV = /\b(?=[A-Z0-9_]*_)[A-Z0-9_]*(?:CAPTCHA|STEALTH|ANTIBOT)[A-Z0-9_]*\b/g;

function walk(dir, out = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) walk(full, out);
    } else if (entry.isFile() && full !== self) {
      out.push(full);
    }
  }
  return out;
}

const files = walk(root);
const rel = (file) => path.relative(root, file).replaceAll("\\", "/");
const text = (file) => readFileSync(file, "utf8");
const textFiles = files.filter((file) => !BINARY.test(file));
const codeFiles = files.filter((file) => CODE.test(file));

function matchAll(source, pattern, group = 1) {
  return [...source.matchAll(pattern)].map((m) => m[group] ?? m[group + 1]).filter(Boolean);
}

function importSpecifiers(source, file) {
  if (file.endsWith(".py")) {
    return matchAll(source, /^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))/gm);
  }
  return [
    ...matchAll(source, /\bfrom\s*["'`]([^"'`]+)["'`]/g),
    ...matchAll(source, /\bimport\s*\(\s*["'`]([^"'`]+)["'`]\s*\)/g),
    ...matchAll(source, /\bimport\s+["'`]([^"'`]+)["'`]/g),
    ...matchAll(source, /\brequire\s*\(\s*["'`]([^"'`]+)["'`]\s*\)/g),
  ];
}

// Script paths named in string literals, such as a helper spawned as a child process.
function scriptLiterals(source) {
  return matchAll(source, /["'`]([^"'`\s]*\.(?:py|mjs|cjs|js|ps1))["'`]/g);
}

function definedNames(source, file) {
  if (file.endsWith(".py")) return matchAll(source, /^\s*(?:async\s+)?def\s+(\w+)/gm);
  return [
    ...matchAll(source, /\bexport\s+(?:async\s+)?function\s*\*?\s*(\w+)/g),
    ...matchAll(source, /\bexport\s+(?:const|let|var|class)\s+(\w+)/g),
    ...matchAll(source, /^\s*(?:async\s+)?function\s*\*?\s*(\w+)/gm),
    ...matchAll(source, /^\s*(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{/gm),
  ];
}

function verbNames(source) {
  return [
    ...matchAll(source, /\bcase\s+["'`]([^"'`]+)["'`]\s*:/g),
    ...matchAll(source, /\bsub\s*===\s*["'`]([^"'`]+)["'`]/g),
    ...matchAll(source, /\bR\.set\(\s*["'`]([^"'`]+)["'`]/g),
  ];
}

const isForbiddenName = (name) =>
  FORBIDDEN_NAME.test(name) || FORBIDDEN_EXACT_NAME.has(name.toLowerCase()) || FORBIDDEN_HUMAN_INPUT.test(name);

function dependencyNames(pkg) {
  const fields = ["dependencies", "devDependencies", "optionalDependencies", "peerDependencies"];
  const names = fields.flatMap((field) => Object.keys(pkg[field] ?? {}));
  const bundled = pkg.bundleDependencies ?? pkg.bundledDependencies ?? [];
  return [...names, ...(Array.isArray(bundled) ? bundled : [])];
}

test("the scan reaches the tree it guards", () => {
  const names = files.map(rel);
  assert.ok(files.length > 200, `walked only ${files.length} files`);
  for (const must of ["package.json", "demo/native-control.mjs", "demo/native-control/runner.mjs"]) {
    assert.ok(names.includes(must), `scan missed ${must}`);
  }
  assert.ok(verbNames(text(path.join(root, "demo/native-control.mjs"))).length > 20);
  assert.ok(verbNames(text(path.join(root, "demo/native-control/runner.mjs"))).length > 10);
  assert.ok(mcpTools.length > 30, "MCP tool list did not load");
});

test("detectors flag synthetic forbidden names", () => {
  assert.ok(FORBIDDEN_MODULE.test("example-captcha-solver.py"));
  assert.deepEqual(importSpecifiers('import * as c from "./captcha.mjs";', "x.mjs"), ["./captcha.mjs"]);
  assert.deepEqual(importSpecifiers("from captcha_kit import solve\n", "x.py"), ["captcha_kit"]);
  assert.deepEqual(dependencyNames({ dependencies: { "example-stealth": "1" } }), ["example-stealth"]);
  assert.ok(verbNames('case "captcha":').some(isForbiddenName));
  assert.ok(definedNames("export async function warmup(s) {}", "x.mjs").some(isForbiddenName));
  assert.ok(definedNames("export async function humanType(s, t) {}", "x.mjs").some(isForbiddenName));
  assert.ok(!isForbiddenName("forum.prose.humanize"));
  assert.deepEqual("EXAMPLE_CAPTCHA_KEY and CAPTCHA prose".match(FORBIDDEN_ENV), ["EXAMPLE_CAPTCHA_KEY"]);
});

test("no module file, import or spawned helper is named for bot-check bypass", () => {
  const hits = files.map(rel).filter((name) => FORBIDDEN_MODULE.test(path.basename(name)));
  for (const file of codeFiles) {
    const source = text(file);
    for (const spec of importSpecifiers(source, file)) {
      if (FORBIDDEN_MODULE.test(spec)) hits.push(`${rel(file)} imports ${spec}`);
    }
    for (const lit of scriptLiterals(source)) {
      if (FORBIDDEN_MODULE.test(path.basename(lit))) hits.push(`${rel(file)} names ${lit}`);
    }
  }
  assert.deepEqual(hits, []);
});

test("no dependency, install step or packaged path is a bypass package", () => {
  const hits = [];
  for (const file of files.filter((f) => path.basename(f) === "package.json")) {
    const pkg = JSON.parse(text(file));
    for (const name of dependencyNames(pkg)) if (FORBIDDEN_MODULE.test(name)) hits.push(`${rel(file)}: ${name}`);
    for (const [key, cmd] of Object.entries(pkg.scripts ?? {})) if (FORBIDDEN_MODULE.test(cmd)) hits.push(`${rel(file)} script ${key}`);
    for (const entry of pkg.files ?? []) if (FORBIDDEN_MODULE.test(entry)) hits.push(`${rel(file)} files ${entry}`);
  }
  const manifests = files.filter((f) =>
    /^(requirements.*\.txt|pyproject\.toml|Pipfile|setup\.cfg|setup\.py)$/i.test(path.basename(f))
    || /\.github\/workflows\/.*\.ya?ml$/.test(rel(f)));
  for (const file of manifests) {
    for (const line of text(file).split(/\r?\n/)) {
      const isDep = !/\.ya?ml$/.test(file) || /\binstall\b/.test(line);
      if (isDep && FORBIDDEN_MODULE.test(line)) hits.push(`${rel(file)}: ${line.trim()}`);
    }
  }
  assert.deepEqual(hits, []);
});

test("no MCP tool, CLI verb, workflow action or function carries a bypass name", () => {
  const hits = [];
  const catalog = JSON.parse(text(path.join(root, "demo/integrations/mcp-tool-catalog.json")));
  const manifest = JSON.parse(text(path.join(root, "demo/integrations/mcp-server-manifest.json")));
  const toolNames = [
    ...mcpTools.map((tool) => tool.name),
    ...catalog.tools.map((tool) => tool.name),
    ...Object.values(manifest.servers).flatMap((server) => server.expected_tools ?? []),
  ];
  for (const name of toolNames) if (isForbiddenName(name)) hits.push(`MCP tool ${name}`);
  for (const file of codeFiles) {
    const source = text(file);
    const native = /native-control/.test(rel(file));
    for (const verb of verbNames(source)) {
      if (isForbiddenName(verb) || (native && FORBIDDEN_NATIVE_VERB.has(verb))) hits.push(`${rel(file)} verb ${verb}`);
    }
    for (const name of definedNames(source, file)) {
      if (isForbiddenName(name)) hits.push(`${rel(file)} defines ${name}`);
    }
  }
  assert.deepEqual(hits, []);
});

test("no environment variable configures a bypass helper", () => {
  const hits = [];
  for (const file of textFiles) {
    for (const name of new Set(text(file).match(FORBIDDEN_ENV) ?? [])) hits.push(`${rel(file)}: ${name}`);
  }
  assert.deepEqual(hits, []);
});
