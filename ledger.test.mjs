// Ledger hash-chain unit test (pure, no browser). Validates canonical-JSON
// stability, chain derivation, export/verify on an intact ledger, and that a
// tampered step or reordering breaks verification.
import { Ledger, canonicalJson, chainValue } from "./demo/native-control/ledger.mjs";

let pass = 0, fail = 0;
const ok = (name, cond) => { if (cond) { pass++; } else { fail++; console.log("FAIL", name); } };

ok("canonicalJson sorts keys", canonicalJson({ b: 1, a: 2 }) === '{"a": 2, "b": 1}');
ok("canonicalJson stable across orderings", canonicalJson({ x: { z: 1, y: 2 }, a: 0 }) === canonicalJson({ a: 0, x: { y: 2, z: 1 } }));
ok("chainValue deterministic", chainValue("0".repeat(64), "s1", { ok: true }) === chainValue("0".repeat(64), "s1", { ok: true }));

const L = new Ledger({ name: "unit" });
L.append("s1", { action: "navigate", target: "https://x", ok: true, result: { url: "https://x" } });
L.append("s2", { action: "fill", target: "#email", ok: true, result: { set: "#email" } });
const exported = L.export();
ok("export has 2 entries", exported.count === 2);
ok("export integrity INTACT", exported.integrity === "INTACT");

const v = Ledger.verify(exported);
ok("verify intact ledger", v.ok === true && v.count === 2);

// tamper a result -> chain should break on re-verify
const tampered = JSON.parse(JSON.stringify(exported));
tampered.entries[0].result.url = "https://EVIL";
const vt = Ledger.verify(tampered);
ok("verify rejects tampered result", vt.ok === false);

// reorder -> break
const reordered = JSON.parse(JSON.stringify(exported));
reordered.entries = [reordered.entries[1], reordered.entries[0]];
const vr = Ledger.verify(reordered);
ok("verify rejects reordering", vr.ok === false);

console.log(`\npass ${pass} / fail ${fail}`);
process.exit(fail ? 1 : 0);
