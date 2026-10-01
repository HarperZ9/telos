// Release-path boundary for native control, added in 0.6.0 after an audit of
// the 0.5.0 package. 0.5.0 shipped, inside `demo/native-control/`:
//   - a search scraper that sent a browser-impersonating User-Agent and routed
//     requests through a signed-in session to get past bot blocks,
//   - input helpers with randomized keystroke timing,
//   - unattended Gmail send, LinkedIn post and Gumroad Google sign-in verbs,
//   - a default form profile carrying one person's name source, location,
//     demographic and eligibility answers, with consent ticked by default,
//   - request capture that copied Authorization headers, request bodies and
//     URLs with tokens in their query or fragment.
// Each test below fails if one of those returns. Static reads plus pure
// functions only: nothing launches a browser or touches the network.
import test from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync, existsSync, writeFileSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
// Driver modules load inside each test, so a static check still runs and
// reports on its own when a module is missing or changed shape.
const load = (name) => import(`./native-control/${name}.mjs`);

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");

function walk(dir, out = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (/\.(mjs|cjs|js|ps1)$/.test(entry.name) && !entry.name.endsWith(".test.mjs")) out.push(full);
  }
  return out;
}

const driverFiles = [
  path.join(root, "demo/native-control.mjs"),
  ...walk(path.join(root, "demo/native-control")),
  path.join(root, "tools/uia.ps1"),
];
const rel = (file) => path.relative(root, file).replaceAll("\\", "/");
const read = (file) => readFileSync(file, "utf8");

test("the scan covers the shipped driver files", () => {
  const names = driverFiles.map(rel);
  for (const must of ["demo/native-control.mjs", "demo/native-control/runner.mjs", "demo/native-control/input.mjs", "tools/uia.ps1"]) {
    assert.ok(names.includes(must), `scan missed ${must}`);
  }
});

test("the removed outreach, scraping and consumer sign-in modules stay removed", () => {
  for (const name of ["scrape.mjs", "contact.mjs", "share.mjs", "behave.mjs"]) {
    assert.equal(existsSync(path.join(root, "demo/native-control", name)), false, `${name} is back`);
  }
  const verbs = new Set();
  for (const file of driverFiles) {
    for (const m of read(file).matchAll(/\bcase\s+["'`]([^"'`]+)["'`]\s*:|\bR\.set\(\s*["'`]([^"'`]+)["'`]/g)) verbs.add(m[1] ?? m[2]);
  }
  for (const gone of ["send", "targets", "linkedin", "gumroadlogin", "gumroadlist", "contact.send"]) {
    assert.equal(verbs.has(gone), false, `verb ${gone} is back`);
  }
});

test("no driver impersonates a browser or hides automation", () => {
  const forbidden = [
    [/Mozilla\/5\.0|AppleWebKit\/|Chrome\/\d+\.\d/, "browser User-Agent string"],
    [/setUserAgentOverride|--user-agent=/i, "User-Agent override"],
    [/navigator\.webdriver/, "webdriver flag access"],
    [/AutomationControlled/, "automation-hiding Chrome flag"],
    [/["'`]User-Agent["'`]\s*:/i, "hand-set User-Agent header"],
  ];
  const hits = [];
  for (const file of driverFiles) {
    const source = read(file);
    for (const [pattern, label] of forbidden) if (pattern.test(source)) hits.push(`${rel(file)}: ${label}`);
  }
  assert.deepEqual(hits, []);
});

test("driver pacing is fixed, never randomized", () => {
  // ledger.mjs draws a random suffix for a run identifier, not for timing.
  const hits = driverFiles
    .filter((file) => rel(file) !== "demo/native-control/ledger.mjs")
    .filter((file) => /Math\.random|crypto\.randomInt|Get-Random/.test(read(file)))
    .map(rel);
  assert.deepEqual(hits, []);
});

test("input helpers use the fixed default pause and reject invalid ones", async () => {
  const input = await load("input");
  const sent = [];
  const session = { send: async (method, params) => { sent.push([method, params]); return {}; } };
  const r = await input.typeText(session, "ab", { pauseMs: 0 });
  assert.deepEqual(r, { typed: 2, pauseMs: 0 });
  assert.deepEqual(sent.map(([m]) => m), ["Input.insertText", "Input.insertText"]);
  assert.equal(input.KEY_PAUSE_MS, 20);
  await assert.rejects(input.typeKeys(session, "a", { pauseMs: -1 }), /invalid pause/);
});

test("the default form profile carries no personal data and no consent", async () => {
  const { defaultProfile, emptyProfile } = await load("forms");
  const empty = defaultProfile(undefined, {});
  assert.deepEqual(empty, emptyProfile());
  assert.deepEqual(empty.answers, {});
  assert.equal(empty.consent, false);
  for (const [key, value] of Object.entries(empty)) {
    if (key === "answers" || key === "consent") continue;
    assert.equal(value, null, `${key} has a built-in default`);
  }
  const forms = read(path.join(root, "demo/native-control/forms.mjs"));
  assert.doesNotMatch(forms, /candidate-profile|career-campaign|harperz9|Seattle|have a disability|protected veteran|\b(gender|race|veteran|disability|sponsorship|authorized)\s*:\s*"/i);
  const greenhouse = read(path.join(root, "demo/native-control/adapters/greenhouse.mjs"));
  assert.doesNotMatch(greenhouse, /pickQuestion\([^)]*,\s*["'`](Yes|No|LinkedIn)["'`]\)/);
});

test("a named profile file is read, and consent needs an explicit true", async () => {
  const { defaultProfile, profileFromRecord } = await load("forms");
  const dir = mkdtempSync(path.join(tmpdir(), "telos-profile-"));
  try {
    const file = path.join(dir, "profile.json");
    writeFileSync(file, JSON.stringify({ name: "Ada B Lovelace", email: "ada@example.test", consent: "yes" }));
    const p = defaultProfile(undefined, { TELOS_FORM_PROFILE: file });
    assert.equal(p.firstName, "Ada");
    assert.equal(p.middleName, "B");
    assert.equal(p.lastName, "Lovelace");
    assert.equal(p.email, "ada@example.test");
    assert.equal(p.consent, false);
    assert.equal(profileFromRecord({ consent: true }).consent, true);
    assert.throws(() => defaultProfile(path.join(dir, "missing.json"), {}), /ENOENT/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
  const forms = read(path.join(root, "demo/native-control/forms.mjs"));
  assert.doesNotMatch(forms, /consent\s*!==\s*false/);
});

test("request capture redacts credential headers and request bodies", async () => {
  const { redactHeaders, describeBody, capture } = await load("network");
  assert.deepEqual(redactHeaders({
    Authorization: "Bearer abc", Cookie: "sid=1", "X-CSRF-Token": "t", "X-Api-Key": "k",
    ":authority": "example.test", Accept: "application/json",
  }), {
    Authorization: "[redacted]", Cookie: "[redacted]", "X-CSRF-Token": "[redacted]", "X-Api-Key": "[redacted]",
    ":authority": "example.test", Accept: "application/json",
  });
  assert.deepEqual(describeBody('{"password":"pw"}'), { bytes: 17, content: "[redacted]" });
  assert.deepEqual(describeBody(undefined), { bytes: 0, content: null });

  const handlers = {};
  const session = {
    send: async () => ({}),
    on: (method, fn) => { handlers[method] = fn; },
  };
  const pending = capture(session, { durationMs: 20, urlFilter: "/api" });
  await new Promise((r) => setTimeout(r, 0));
  handlers["Network.requestWillBeSent"]({
    requestId: "1", type: "Fetch",
    request: { method: "POST", url: "https://example.test/api/login", postData: "user=a&password=b", headers: { Authorization: "Bearer secret" } },
  });
  handlers["Network.responseReceived"]({ requestId: "1", response: { status: 200 } });
  const out = await pending;
  assert.equal(out.redacted, true);
  assert.equal(JSON.stringify(out).includes("secret"), false);
  assert.equal(JSON.stringify(out).includes("password=b"), false);
  assert.equal(out.requests[0].status, 200);
  assert.equal(out.requests[0].body.bytes, 17);
});

test("request capture redacts credentials carried in the URL", async () => {
  const { redactUrl, capture } = await load("network");
  assert.equal(
    redactUrl("https://u:pw@example.test/cb?code=abc&state=s1&page=2#access_token=t0k&token_type=bearer"),
    "https://[redacted]@example.test/cb?code=[redacted]&state=s1&page=2#access_token=[redacted]&token_type=[redacted]",
  );
  assert.equal(
    redactUrl("https://bucket.example.test/o?X-Amz-Signature=f00&X-Amz-Credential=c&api_key=k&q=telos"),
    "https://bucket.example.test/o?X-Amz-Signature=[redacted]&X-Amz-Credential=[redacted]&api_key=[redacted]&q=telos",
  );
  assert.equal(redactUrl("https://example.test/docs#section-2"), "https://example.test/docs#section-2");

  const handlers = {};
  const session = { send: async () => ({}), on: (method, fn) => { handlers[method] = fn; } };
  const pending = capture(session, { durationMs: 20, urlFilter: "/api" });
  await new Promise((r) => setTimeout(r, 0));
  handlers["Network.requestWillBeSent"]({
    requestId: "2", type: "XHR",
    request: { method: "GET", url: "https://example.test/api/me?access_token=secret123&fields=id", headers: {} },
  });
  const out = await pending;
  assert.equal(out.requests[0].url, "https://example.test/api/me?access_token=[redacted]&fields=id");
  assert.equal(JSON.stringify(out).includes("secret123"), false);
});
