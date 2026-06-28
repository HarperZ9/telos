import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const ledger = JSON.parse(
  readFileSync(new URL("./research/youtube-bgoertzel-receipts.json", import.meta.url), "utf8")
);

assert.equal(ledger.schema, "project-telos.research-intake/youtube-video-receipts-v1");
assert.equal(ledger.tool, "gather.video");
assert.equal(ledger.inputs.length, 8);
assert.equal(ledger.results.length, ledger.inputs.length);
assert.ok(ledger.inputs.includes("https://www.youtube.com/watch?v=SbafEATbfXQ&t=53s"));

for (const result of ledger.results) {
  assert.equal(result.returncode, 0, `${result.url} gathered successfully`);
  assert.ok(Array.isArray(result.catalog), `${result.url} has catalog rows`);
  const kinds = new Set(result.catalog.map((item) => item.kind));
  assert.ok(kinds.has("metadata"), `${result.url} has metadata`);
  assert.ok(kinds.has("transcript"), `${result.url} has transcript receipt`);
  for (const item of result.catalog) {
    assert.match(item.sha256, /^[0-9a-f]{64}$/);
    assert.equal(typeof item.title, "string");
    assert.equal(typeof item.method, "string");
    assert.ok(!("text" in item), "receipt ledger does not store raw transcript text");
  }
  assert.match(result.digest.seal, /^[0-9a-f]{64}$/);
}
