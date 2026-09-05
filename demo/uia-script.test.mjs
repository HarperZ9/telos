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

// Line endings are normalised because every check below is a multi-line regex
// over PowerShell source, and a checkout with core.autocrlf leaves a \r in front
// of each \n. A pattern like `default {\n` then matches nothing and the test
// reports the file has no default branch, which is a lie about the source rather
// than a finding. This is not hypothetical: a fresh worktree on this machine
// checks the file out with CRLF and the file in place has LF.
function readScript(path) {
  return readFileSync(path, "utf8").replace(/\r\n/g, "\n");
}

const source = readScript(uiaScriptPath());

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

// $ARITY = @{ windows = 1; ... } -> { windows: 1, ... }. The count includes the
// verb itself, so a caller supplies one fewer than this.
function arityTable(text) {
  const line = /^\$ARITY = @\{(.+)\}$/m.exec(text);
  assert.ok(line, "uia.ps1 must declare $ARITY as a single-line hashtable");
  return Object.fromEntries(
    [...line[1].matchAll(/(\w+)\s*=\s*(\d+)/g)].map((m) => [m[1], Number(m[2])]));
}

function arityKeys(text) {
  return Object.keys(arityTable(text));
}

// Read the labels out of the $verb switch specifically. Anchoring on the switch
// rather than on an indent keeps this pointed at the dispatch after the whole
// block moved inside the guard, and keeps it off the switch inside Deny-Body.
function switchLabels(text) {
  const block = text.split(/^\s*switch \(\$verb\) \{$/m)[1];
  assert.ok(block, "uia.ps1 must dispatch on $verb with a switch");
  return [...block.matchAll(/^ {4}"(\w+)" \{$/gm)].map((m) => m[1]);
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
  const dflt = /^ {4}default \{\n([\s\S]*?)^ {4}\}$/m.exec(source);
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

// Truncation is the loud way a listing fails to settle absence. The quiet way is
// a walk that completed behind a provider boundary and saw nothing named, which
// reads identically to a window holding nothing. A caller deciding "the control
// is not there" needs both collapsed into one field, and it has to come from the
// function the selftest drives rather than being worked out again at the call
// site, because a second copy of a rule is a second place for it to go wrong.
test("uia.ps1 answers whether a tree listing settles absence", () => {
  assert.match(source, /settlesAbsence = \(Test-SettlesAbsence \$count \$truncated\)/);
  assert.match(source, /opaque = \(\$count -eq 0\)/);
  const derivations = [...source.matchAll(/settlesAbsence = /g)];
  assert.equal(derivations.length, 1, "settlesAbsence is derived in one place");
});

// The element rungs have no behavioural gate here: two controls sharing a name
// inside one window is a property of whatever is running on the machine, not
// something a test can arrange. What can be held is the shape. FindFirst returns
// one arbitrary hit and reports nothing about the others, so a rung built on it
// cannot refuse a duplicate however carefully the caller reads the answer, and
// swapping FindAll for it is the plausible optimisation that would silently
// restore the defect. This is a structural check standing in for a behavioural
// one, which is weaker, and the substitution is the point.
test("uia.ps1 resolves an element by a search that can see duplicates", () => {
  const fn = /function Find-Element[\s\S]*?\n\}/m.exec(source);
  assert.ok(fn, "uia.ps1 must define Find-Element");
  assert.doesNotMatch(fn[0], /FindFirst/);
  assert.match(fn[0], /\$hits\.Count -gt 1.*\n?.*New-Ambiguity/);
});

// Every verb reaches into a live UIA provider in another process, and
// $ErrorActionPreference = "Stop" turns anything one of them throws into a
// terminating error. Unhandled that empties stdout and exits 1, which is the one
// outcome the header promises never happens.
// The catch is matched through the switch it belongs to, not on its own. The
// file opens with two other guards at the same indentation, and a pattern that
// finds any `} catch {` reads the first one: the Add-Type handler, which does
// call Out-Json and would report this gate green over a dispatch guard that had
// been changed to write something else entirely.
test("uia.ps1 dispatches inside a guard that answers in JSON", () => {
  const guard =
    /^try \{\n {2}switch \(\$verb\) \{[\s\S]*?^\} catch \{\n([\s\S]*?)^\}$/m.exec(source);
  assert.ok(guard, "the $verb switch must sit inside a try with a catch");
  assert.match(guard[1], /Out-Json/);
  assert.match(guard[1], /ok = \$false/);
});

// A test that ran 'input' or 'type' on a developer's machine would synthesise
// keystrokes into whatever window happened to hold focus, which is the operator's
// desktop and not a fixture. The two verbs are read out of the header rather than
// named here, so a third foreground verb is covered the day it is marked.
test("this suite never spawns a verb that types into the focused window", () => {
  const own = readScript(new URL(import.meta.url));
  const foreground = headerVerbLines(source)
    .filter((entry) => entry.line.includes("FOREGROUND"))
    .map((entry) => entry.verb);
  assert.ok(foreground.length > 0, "the header must mark its foreground verbs");
  const spawned = [...own.matchAll(/uiaArgs\(uiaScriptPath\(\), "(\w+)"/g)].map((m) => m[1]);
  assert.deepEqual(spawned.filter((verb) => foreground.includes(verb)), []);
  // The windowed sweep below spawns a verb it computed rather than one written
  // here, so the check above cannot see it. What keeps it clear of the keyboard
  // is that a foreground verb takes no window, and that is asserted, not assumed.
  const bothWays = headerVerbLines(source)
    .filter((entry) => entry.line.includes("FOREGROUND") && entry.line.includes("<windowMatch>"));
  assert.deepEqual(bothWays, []);
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

const WIN32 = { skip: process.platform === "win32" ? false : "windows-only" };

function runUia(verb, params) {
  const run = spawnSync("powershell.exe", uiaArgs(uiaScriptPath(), verb, params), {
    encoding: "utf8",
    timeout: 60000,
  });
  assert.equal(run.status, 0, run.stderr);
  assert.equal(run.stderr, "", "the contract puts nothing on stderr");
  return JSON.parse(run.stdout.trim());
}

// A window match nothing on the machine can satisfy, so a test asserts the same
// thing whatever happens to be open.
const ABSENT_WINDOW = "no-such-window-b2f4c1a9";

// The arity table catches a maxElements that is missing. One that is present and
// unusable reached the [int] cast instead, which throws under
// $ErrorActionPreference = "Stop" and left the caller parsing an empty stdout
// beside a stack trace on the wrong stream. Passing a window that cannot resolve
// pins the order too: the argument has to be read before the walk is set up, or
// a caller who mistyped a ceiling is told its window is missing instead.
test("uia.ps1 refuses a maxElements it cannot read, in JSON", WIN32, () => {
  const res = runUia("tree", [ABSENT_WINDOW, "abc"]);
  assert.equal(res.ok, false);
  assert.match(res.error, /maxElements must be a positive integer: abc/);
});

// A negative ceiling was the worse half of the same defect: no cast to throw, so
// the walk collected nothing and the answer was ok with an empty listing. A
// caller reading that as "the window holds no controls" is wrong in the one
// direction this file exists to prevent.
test("uia.ps1 refuses a maxElements below one rather than answering empty", WIN32, () => {
  const res = runUia("tree", [ABSENT_WINDOW, "-5"]);
  assert.equal(res.ok, false);
  assert.match(res.error, /maxElements must be a positive integer: -5/);
  assert.equal(res.count, undefined, "a refusal carries no listing");
});

// Every verb that takes a window resolves it before touching anything, so a
// window match nothing can satisfy is the one live-machine path that exercises
// each verb without acting on a real control. The verbs come from the header's
// own <windowMatch> annotations, so a new one is covered when it is documented.
test("uia.ps1 denies in JSON for a window that cannot resolve", WIN32, () => {
  const arity = arityTable(source);
  const windowed = headerVerbLines(source)
    .filter((entry) => entry.line.includes("<windowMatch>"))
    .map((entry) => entry.verb);
  assert.ok(windowed.length >= 5, `expected the windowed verbs, got ${windowed}`);
  for (const verb of windowed) {
    const params = ["Element", "text"].slice(0, arity[verb] - 2);
    const res = runUia(verb, [ABSENT_WINDOW, ...params]);
    assert.equal(res.ok, false, `${verb} answered ok for a window that is not there`);
    assert.equal(res.error, `window not found: ${ABSENT_WINDOW}`, verb);
  }
});
