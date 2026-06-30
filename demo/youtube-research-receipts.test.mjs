import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const hash64 = /^[0-9a-f]{64}$/;

const ledger = JSON.parse(
  readFileSync(new URL("./research/youtube-bgoertzel-receipts.json", import.meta.url), "utf8")
);
const mathEducatorLedger = JSON.parse(
  readFileSync(new URL("./research/youtube-math-educator-receipts.json", import.meta.url), "utf8")
);
const learningForgeReceiptLedger = JSON.parse(
  readFileSync(new URL("./research/youtube-learning-forge-receipts.json", import.meta.url), "utf8")
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
    assert.match(item.sha256, hash64);
    assert.equal(typeof item.title, "string");
    assert.equal(typeof item.method, "string");
    assert.ok(!("text" in item), "receipt ledger does not store raw transcript text");
  }
  assert.match(result.digest.seal, hash64);
}

assert.equal(mathEducatorLedger.schema, "project-telos.research-intake/youtube-source-leads-v1");
assert.equal(mathEducatorLedger.tool, "gather.video");
assert.equal(mathEducatorLedger.freshness.raw_transcripts_stored, false);
assert.equal(mathEducatorLedger.freshness.raw_video_stored, false);
assert.ok(mathEducatorLedger.inputs.includes("https://www.youtube.com/@InigoQuilez"));
assert.ok(mathEducatorLedger.inputs.includes("https://www.youtube.com/watch?v=5pieVHmlbyk&t=29s"));
assert.ok(mathEducatorLedger.mission.normalized_concepts.includes("painting-with-maths"));
assert.ok(mathEducatorLedger.mission.telos_implications.some((item) => /Educator surfaces/.test(item)));
assert.equal(mathEducatorLedger.results.length, 8);

const sourceLeadIds = new Set(mathEducatorLedger.results.map((item) => item.id));
for (const id of [
  "DAMiS2PGTEE",
  "tv17bmE2FNY",
  "TUzgnbhdo2Y",
  "21ZB0yhILZo",
  "eFgknPFK-g0",
  "XyUFPHRQtyw",
  "rf1FKWaSpEY",
  "5pieVHmlbyk"
]) {
  assert.ok(sourceLeadIds.has(id), `missing source lead ${id}`);
}

for (const lead of mathEducatorLedger.results) {
  assert.match(lead.metadata_sha256, hash64);
  assert.equal(typeof lead.title, "string");
  assert.ok(Array.isArray(lead.lead_topics) && lead.lead_topics.length > 0);
  assert.equal("transcript_text" in lead, false);
  assert.equal("raw_transcript" in lead, false);
}

assert.equal(learningForgeReceiptLedger.schema, "project-telos.learning-forge/youtube-research-seed/v1");
assert.match(learningForgeReceiptLedger.source_request.sha256, hash64);
assert.equal("attachment" in learningForgeReceiptLedger.source_request, false);
assert.equal(learningForgeReceiptLedger.inputs.videos.length, 8);
assert.equal(learningForgeReceiptLedger.video_results.length, learningForgeReceiptLedger.inputs.videos.length);
assert.equal(learningForgeReceiptLedger.inputs.channels.length, 2);
assert.equal(learningForgeReceiptLedger.channel_results.length, learningForgeReceiptLedger.inputs.channels.length);
assert.match(learningForgeReceiptLedger.claim_state.research_claims, /UNVERIFIABLE/);

for (const result of learningForgeReceiptLedger.video_results) {
  assert.equal(result.returncode, 0, `${result.url} gathered successfully`);
  const kinds = new Set(result.catalog.map((item) => item.kind));
  assert.ok(kinds.has("metadata"), `${result.url} has metadata`);
  assert.ok(kinds.has("transcript"), `${result.url} has transcript receipt`);
  for (const item of result.catalog) {
    assert.match(item.sha256, hash64);
    assert.equal("text" in item, false);
  }
  assert.match(result.digest.seal, hash64);
}

for (const channel of learningForgeReceiptLedger.channel_results) {
  assert.equal(channel.returncode, 0, `${channel.url} channel list captured`);
  assert.equal(channel.source_type, "youtube_channel");
  assert.equal(channel.video_list_state, "match");
  assert.equal(channel.method, "yt-dlp-flat-playlist");
  assert.match(channel.metadata_sha256, hash64);
  assert.ok(channel.captured_entries > 0);
  assert.equal("description" in channel, false);
}
