// Boundary tripwires for the reach layer. It is our own code on Node
// built-ins: no runtime dependency, no client library, no scraping framework,
// no headless browser. And no code path that reads browser cookie stores,
// sends cookies, rotates identities or proxies, or calls X's private web API.
// Each detector is first shown to fire on a synthetic sample.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { userAgent } from "./reach/identity.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const reachDir = path.join(here, "reach");
const reachFiles = [path.join(here, "reach.mjs"), ...readdirSync(reachDir).filter((f) => f.endsWith(".mjs")).map((f) => path.join(reachDir, f))];
const source = (file) => readFileSync(file, "utf8");
// Comments may name a forbidden method to say it is absent; code may not.
const code = (file) => source(file).replace(/^\s*\/\/.*$/gm, "").replace(/\/\*[\s\S]*?\*\//g, "");

export function importSpecifiers(text) {
  return [...text.matchAll(/\bfrom\s*["']([^"']+)["']|\bimport\s*\(\s*["']([^"']+)["']\s*\)|\brequire\s*\(\s*["']([^"']+)["']\s*\)/g)].map((m) => m[1] ?? m[2] ?? m[3]);
}
const allowedSpecifier = (spec) => spec.startsWith("node:") || spec.startsWith("./") || spec.startsWith("../");

const FORBIDDEN_CODE = [
  { name: "browser cookie store", pattern: /[\/\\"'`]Cookies["'`]|Login Data|cookies\.sqlite|Local State|browser_cookie|chrome-cookies/ },
  { name: "sending a cookie header", pattern: /["'`]cookie["'`]\s*:/i },
  { name: "proxy or identity rotation", pattern: /rotat\w*\s*\(|proxyList|proxies\s*=|residential|socks5:/i },
  { name: "browser User-Agent string", pattern: /Mozilla\/5\.0|AppleWebKit|Chrome\/\d/ },
  { name: "X private web API", pattern: /\/i\/api\/|graphql|guest_token|x-guest-token|auth_token/i },
  { name: "headless browser or scraping framework", pattern: /puppeteer|playwright|selenium|cheerio|jsdom|crawlee|scrapy/i },
];

test("detectors fire on synthetic forbidden samples", () => {
  const samples = {
    "browser cookie store": 'open(path.join(profile, "Cookies"))',
    "sending a cookie header": 'headers: { "cookie": jar }',
    "proxy or identity rotation": "const next = rotateIdentity()",
    "browser User-Agent string": '"Mozilla/5.0 (Windows NT 10.0)"',
    "X private web API": 'fetch("https://x.com/i/api/graphql/abc")',
    "headless browser or scraping framework": 'import x from "puppeteer"',
  };
  for (const { name, pattern } of FORBIDDEN_CODE) assert.ok(pattern.test(samples[name]), name);
  assert.deepEqual(importSpecifiers('import a from "undici"; const b = require("axios");'), ["undici", "axios"]);
  assert.ok(!allowedSpecifier("undici"));
});

test("package.json has no runtime dependency of any kind", () => {
  const pkg = JSON.parse(source(path.join(root, "package.json")));
  for (const field of ["dependencies", "optionalDependencies", "peerDependencies", "bundleDependencies", "bundledDependencies"]) {
    const value = pkg[field];
    const count = Array.isArray(value) ? value.length : Object.keys(value ?? {}).length;
    assert.equal(count, 0, `package.json ${field} must stay empty; the reach layer is Node built-ins only`);
  }
});

test("reach modules import only Node built-ins and each other", () => {
  assert.ok(reachFiles.length >= 14, `found only ${reachFiles.length} reach files`);
  const hits = reachFiles.flatMap((file) => importSpecifiers(source(file)).filter((spec) => !allowedSpecifier(spec)).map((spec) => `${path.basename(file)} imports ${spec}`));
  assert.deepEqual(hits, []);
});

test("no reach code reads cookies, rotates identities, imitates a browser or calls private X endpoints", () => {
  const hits = [];
  for (const file of reachFiles) {
    if (file.endsWith("fake-net.mjs")) continue;
    for (const { name, pattern } of FORBIDDEN_CODE) if (pattern.test(code(file))) hits.push(`${path.basename(file)}: ${name}`);
  }
  assert.deepEqual(hits, []);
});

test("the User-Agent is fixed: same value every call, Telos named", () => {
  const values = new Set(Array.from({ length: 20 }, () => userAgent({})));
  assert.equal(values.size, 1);
  assert.match([...values][0], /^Telos\//);
});

test("the test double is kept out of the published package", () => {
  const pkg = JSON.parse(source(path.join(root, "package.json")));
  assert.ok(pkg.files.includes("!demo/reach/fake-net.mjs"));
});
