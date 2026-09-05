// Tests for tools/uia.ps1 itself, as distinct from the Node wrapper around it
// in native-control.test.mjs.
//
// CI runs on ubuntu-latest, where PowerShell is absent, so the behaviour tests
// are gated on win32 and would report green by skipping. What survives that gate
// is the script's own text: the header comment, the verb table, and the switch
// have to agree with each other, and drift between them is what shipped a header
// listing five verbs over a file implementing eight. Those three lists are read
// out of the source and compared here, on every platform.

import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";

import { uiaArgs, uiaScriptPath } from "./native-control/app.mjs";

const source = readFileSync(uiaScriptPath(), "utf8");

// $VERBS = @("windows", "tree", ...) -> the strings, in order.
function declaredVerbs(text) {
  const line = /^\$VERBS = @\((.+)\)$/m.exec(text);
  assert.ok(line, "uia.ps1 must declare $VERBS as a single-line array");
  return [...line[1].matchAll(/"([^"]+)"/g)].map((m) => m[1]);
}

// The header block after the "Verbs:" line: one indented comment line per verb,
// ending at the first comment line that is not one. Returns the whole line so a
// caller can read the annotations on it, not only the verb.
function headerVerbLines(text) {
  const after = text.split(/^# .*Verbs:$/m)[1];
  assert.ok(after, "uia.ps1 header must introduce its verb list with 'Verbs:'");
  const out = [];
  for (const line of after.split("\n")) {
    const m = /^#\s{2,}(\S+)/.exec(line);
    if (!m) {
      // split() leaves the remainder of the "Verbs:" line itself in front of
      // the block, so a non-match before the first verb is not the end of it.
      if (out.length === 0) continue;
      break;
    }
    out.push({ verb: m[1], line });
  }
  return out;
}

function headerVerbs(text) {
  return headerVerbLines(text).map((entry) => entry.verb);
}

// $ARITY = @{ windows = 1; ... } -> the key names.
function arityKeys(text) {
  const line = /^\$ARITY = @\{(.+)\}$/m.exec(text);
  assert.ok(line, "uia.ps1 must declare $ARITY as a single-line hashtable");
  return [...line[1].matchAll(/(\w+)\s*=\s*\d+/g)].map((m) => m[1]);
}

function switchLabels(text) {
  return [...text.matchAll(/^ {2}"(\w+)" \{$/gm)].map((m) => m[1]);
}

test("uia.ps1 header comment lists exactly the verbs it implements", () => {
  assert.deepEqual(headerVerbs(source), declaredVerbs(source));
});

test("uia.ps1 switch handles exactly the declared verbs", () => {
  assert.deepEqual(switchLabels(source).sort(), [...declaredVerbs(source)].sort());
});

test("uia.ps1 declares an arity for every verb", () => {
  assert.deepEqual(arityKeys(source).sort(), [...declaredVerbs(source)].sort());
});

// The unknown-verb answer has to read $VERBS rather than repeat it. A second
// hand-typed copy is exactly how the header went stale, and a test comparing
// two copies that are both wrong would still pass.
test("uia.ps1 answers an unknown verb from $VERBS, not a second copy", () => {
  const dflt = /^ {2}default \{\n([\s\S]*?)^ {2}\}$/m.exec(source);
  assert.ok(dflt, "uia.ps1 switch must carry a default branch");
  assert.match(dflt[1], /verbs = \$VERBS/);
  const literals = [...source.matchAll(/@\("windows"/g)];
  assert.equal(literals.length, 1, "the verb list is declared once");
});

// 'input' and 'type' synthesise keystrokes into whatever window holds focus,
// which no other verb does. A caller that cannot tell them apart from the
// UIA-pattern verbs will steal the operator's keyboard without meaning to, so
// the marking is part of the contract rather than a courtesy.
test("uia.ps1 marks the two foreground verbs and only those", () => {
  const marked = headerVerbLines(source)
    .filter((entry) => entry.line.includes("FOREGROUND"))
    .map((entry) => entry.verb);
  assert.deepEqual(marked, ["input", "type"]);
});

test("uia.ps1 reports whether a tree listing was truncated", () => {
  assert.match(source, /truncated = \$truncated/);
  assert.match(source, /descendants = \$all\.Count/);
});

// ---- gated: the script's own selftest, which needs PowerShell ----

// Select-Candidate is where an ambiguous match either gets refused or gets
// answered with whichever element the tree walk reached first. The selftest
// drives it over synthetic records, so it runs without any particular window
// open, and it fails if the substring rung is loosened back to picking one.
test(
  "uia.ps1 selftest passes",
  { skip: process.platform === "win32" ? false : "windows-only" },
  () => {
    const run = spawnSync("powershell.exe", uiaArgs(uiaScriptPath(), "selftest"), {
      encoding: "utf8",
      timeout: 60000,
    });
    assert.equal(run.status, 0, run.stderr);
    const res = JSON.parse(run.stdout.trim().split("\n").pop());
    assert.equal(res.failed, 0, JSON.stringify(res.results));
    assert.equal(res.ok, true);
    assert.ok(res.cases >= 7, `expected at least 7 cases, got ${res.cases}`);
  },
);

// A missing argument used to reach $args[1] as $null, and .ToLower() on it threw
// a PowerShell stack trace onto a stream the contract says carries JSON.
test(
  "uia.ps1 answers a missing argument in JSON, not a stack trace",
  { skip: process.platform === "win32" ? false : "windows-only" },
  () => {
    const run = spawnSync("powershell.exe", uiaArgs(uiaScriptPath(), "invoke", ["Notepad"]), {
      encoding: "utf8",
      timeout: 60000,
    });
    assert.equal(run.status, 0, run.stderr);
    const res = JSON.parse(run.stdout.trim());
    assert.equal(res.ok, false);
    assert.match(res.error, /invoke needs 2 argument\(s\), got 1/);
  },
);
