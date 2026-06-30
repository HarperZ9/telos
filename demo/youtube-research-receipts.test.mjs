import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const hash64 = /^[0-9a-f]{64}$/;

const bgoertzelLedger = JSON.parse(
  readFileSync(new URL("./research/youtube-bgoertzel-receipts.json", import.meta.url), "utf8")
);
const learningForgeLedger = JSON.parse(
  readFileSync(new URL("./research/youtube-learning-forge-receipts.json", import.meta.url), "utf8")
);

function assertVideoResult(result) {
  assert.equal(result.returncode, 0, `${result.url} gathered successfully`);
  assert.ok(Array.isArray(result.catalog), `${result.url} has catalog rows`);
  const kinds = new Set(result.catalog.map((item) => item.kind));
  assert.ok(kinds.has("metadata"), `${result.url} has metadata`);
  assert.ok(kinds.has("transcript"), `${result.url} has transcript receipt`);
  for (const item of result.catalog) {
    assert.match(item.sha256, hash64);
    assert.equal(typeof item.title, "string");
    assert.equal(typeof item.method, "string");
    assert.ok(!("text" in item), "receipt ledger does not store raw transcript text");
  }
  assert.match(result.digest.seal, hash64);
}

assert.equal(bgoertzelLedger.schema, "project-telos.research-intake/youtube-video-receipts-v1");
assert.equal(bgoertzelLedger.tool, "gather.video");
assert.equal(bgoertzelLedger.inputs.length, 7);
assert.equal(bgoertzelLedger.results.length, bgoertzelLedger.inputs.length);
for (const result of bgoertzelLedger.results) {
  assertVideoResult(result);
}

assert.equal(learningForgeLedger.schema, "project-telos.learning-forge/youtube-research-seed/v1");
assert.match(learningForgeLedger.source_request.sha256, hash64);
assert.ok(!("attachment" in learningForgeLedger.source_request), "ledger does not expose local attachment paths");
assert.equal(learningForgeLedger.inputs.videos.length, 8);
assert.equal(learningForgeLedger.video_results.length, learningForgeLedger.inputs.videos.length);
assert.equal(learningForgeLedger.inputs.channels.length, 2);
assert.equal(learningForgeLedger.channel_results.length, learningForgeLedger.inputs.channels.length);
assert.match(learningForgeLedger.claim_state.research_claims, /UNVERIFIABLE/);

for (const result of learningForgeLedger.video_results) {
  assertVideoResult(result);
}

for (const channel of learningForgeLedger.channel_results) {
  assert.equal(channel.returncode, 0, `${channel.url} channel list captured`);
  assert.equal(channel.source_type, "youtube_channel");
  assert.equal(channel.video_list_state, "match");
  assert.equal(channel.method, "yt-dlp-flat-playlist");
  assert.match(channel.metadata_sha256, hash64);
  assert.ok(channel.captured_entries > 0, `${channel.url} has captured entries`);
  for (const entry of channel.entries) {
    assert.equal(typeof entry.id, "string");
    assert.equal(typeof entry.title, "string");
    assert.equal(typeof entry.url, "string");
  }
}
