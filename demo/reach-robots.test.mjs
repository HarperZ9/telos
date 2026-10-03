// robots.txt behaviour, each rule paired with the case that would pass if the
// rule were broken.
import test from "node:test";
import assert from "node:assert/strict";
import { decide, parseRobots, patternToRegex, robotsFromStatus, selectGroup } from "./reach/robots.mjs";

const SAMPLE = `
# comment
User-agent: Googlebot
Disallow: /

User-agent: *
Disallow: /private
Allow: /private/open
Disallow: /*.pdf$
Crawl-delay: 4

User-agent: telos
User-agent: other
Disallow: /telos-only
Crawl-delay: 2
Sitemap: https://example.test/sitemap.xml
`;

test("the specific product token wins over the wildcard group", () => {
  const parsed = parseRobots(SAMPLE);
  assert.equal(decide(parsed, "telos", "/telos-only/x").allowed, false);
  // Paired: the wildcard's /private rule does not apply to telos, which has its own group.
  assert.equal(decide(parsed, "telos", "/private").allowed, true);
  assert.equal(decide(parsed, "somebot", "/private").allowed, false);
  assert.equal(selectGroup(parsed, "telos").crawlDelay, 2);
  assert.equal(selectGroup(parsed, "somebot").crawlDelay, 4);
});

test("the longest match wins and Allow wins a tie", () => {
  const parsed = parseRobots("User-agent: *\nDisallow: /a\nAllow: /a/b\nDisallow: /a/b/c\nDisallow: /t\nAllow: /t\n");
  assert.equal(decide(parsed, "telos", "/a/x").allowed, false);
  assert.equal(decide(parsed, "telos", "/a/b/x").allowed, true);
  assert.equal(decide(parsed, "telos", "/a/b/c/d").allowed, false);
  assert.equal(decide(parsed, "telos", "/t").allowed, true, "Allow must win an equal-length tie");
  assert.equal(decide(parsed, "telos", "/a/b/x").rule, "Allow: /a/b");
});

test("wildcards and end anchors match as RFC 9309 describes", () => {
  assert.ok(patternToRegex("/*.pdf$").test("/files/a.pdf"));
  assert.ok(!patternToRegex("/*.pdf$").test("/files/a.pdf?x=1"));
  assert.ok(patternToRegex("/fish*").test("/fish.html"));
  assert.ok(!patternToRegex("/fish").test("/Fish"), "matching is case-sensitive");
  const parsed = parseRobots(SAMPLE);
  assert.equal(decide(parsed, "somebot", "/doc.pdf").allowed, false);
  assert.equal(decide(parsed, "somebot", "/doc.pdf.html").allowed, true);
});

test("an empty Disallow allows everything and robots.txt is always readable", () => {
  const open = parseRobots("User-agent: *\nDisallow:\n");
  assert.equal(decide(open, "telos", "/anything").allowed, true);
  const closed = parseRobots("User-agent: *\nDisallow: /\n");
  assert.equal(decide(closed, "telos", "/anything").allowed, false);
  assert.equal(decide(closed, "telos", "/robots.txt").allowed, true);
});

test("sitemaps are collected from anywhere in the file", () => {
  assert.deepEqual(parseRobots(SAMPLE).sitemaps, ["https://example.test/sitemap.xml"]);
});

test("fetch status maps to policy: 4xx open, 5xx and unreachable closed", () => {
  assert.equal(decide(robotsFromStatus(404, "").parsed, "telos", "/x").allowed, true);
  assert.equal(decide(robotsFromStatus(500, "").parsed, "telos", "/x").allowed, false);
  assert.equal(decide(robotsFromStatus(0, "").parsed, "telos", "/x").allowed, false);
  assert.equal(decide(robotsFromStatus(200, "User-agent: *\nDisallow: /x").parsed, "telos", "/x").allowed, false);
  assert.match(robotsFromStatus(503, "").basis, /disallow all/);
});
