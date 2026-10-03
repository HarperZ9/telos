// Crawler behaviour against a fake site: robots first, disallowed paths never
// fetched, redirects re-checked, feeds and sitemaps preferred, budgets held.
import test from "node:test";
import assert from "node:assert/strict";
import { Crawler, normalizeUrl } from "./reach/crawler.mjs";
import { fakeHttp } from "./reach/fake-net.mjs";
import { isFeed, parseFeed, parseHtml, parseSitemap } from "./reach/parse.mjs";

const O = "https://site.test";
const html = (body, head = "") => ({ body: `<html><head><title>T</title>${head}</head><body>${body}</body></html>`, headers: { "content-type": "text/html" } });

function site(extra = {}) {
  return {
    [`${O}/robots.txt`]: { body: "User-agent: *\nDisallow: /private\nCrawl-delay: 3\nSitemap: https://site.test/sitemap.xml\n" },
    [`${O}/sitemap.xml`]: { body: `<urlset><url><loc>${O}/a</loc></url><url><loc>${O}/private/x</loc></url></urlset>` },
    [`${O}/`]: html(`<a href="/a">a</a><a href="/b">b</a><a href="/private/y">p</a><a href="https://other.test/">o</a><a rel="nofollow" href="/nf">nf</a>`, `<link rel="alternate" type="application/rss+xml" href="/feed.xml">`),
    [`${O}/feed.xml`]: { body: `<rss><channel><title>F</title><item><title>One</title><link>${O}/c</link></item></channel></rss>` },
    [`${O}/a`]: html("A page"),
    [`${O}/b`]: html("B page"),
    [`${O}/c`]: html("C page"),
    ...extra,
  };
}

test("a disallowed URL is refused and its page is never requested", async () => {
  const { http, calls } = fakeHttp(site({ [`${O}/private/x`]: html("secret") }));
  const crawler = new Crawler({ http });
  const got = await crawler.fetchPage(`${O}/private/x`);
  assert.equal(got.page, null);
  assert.match(got.refused, /robots\.txt disallowed \(Disallow: \/private\)/);
  assert.ok(!calls.some((c) => c.url === `${O}/private/x`));
  // Paired: an allowed URL on the same site is fetched.
  const ok = await crawler.fetchPage(`${O}/a`);
  assert.equal(ok.page.kind, "html");
  assert.match(ok.page.text, /A page/);
});

test("robots.txt is read once per origin and its Crawl-delay paces the host", async () => {
  const { http, calls, sleeps } = fakeHttp(site());
  const crawler = new Crawler({ http });
  await crawler.fetchPage(`${O}/a`);
  await crawler.fetchPage(`${O}/b`);
  assert.equal(calls.filter((c) => c.url.endsWith("/robots.txt")).length, 1);
  assert.ok(sleeps.includes(3000), "Crawl-delay 3 must space requests by 3 s");
});

test("a redirect into a disallowed path is refused at the hop", async () => {
  const { http, calls } = fakeHttp(site({ [`${O}/go`]: { status: 301, headers: { location: "/private/z" } }, [`${O}/private/z`]: html("no") }));
  const got = await new Crawler({ http }).fetchPage(`${O}/go`);
  assert.equal(got.status, 0);
  assert.ok(!calls.some((c) => c.url === `${O}/private/z`));
});

test("an unreachable robots.txt means disallow all", async () => {
  const { http, calls } = fakeHttp({ [`${O}/robots.txt`]: { status: 500 }, [`${O}/a`]: html("A") });
  const got = await new Crawler({ http }).fetchPage(`${O}/a`);
  assert.equal(got.page, null);
  assert.ok(!calls.some((c) => c.url === `${O}/a`));
});

test("records carry URL, status, robots decision and byte hash", async () => {
  const { http } = fakeHttp(site());
  const crawler = new Crawler({ http });
  await crawler.fetchPage(`${O}/a`);
  const [robots, page] = crawler.records;
  assert.equal(robots.channel, "robots");
  assert.equal(page.url, `${O}/a`);
  assert.equal(page.status, 200);
  assert.match(page.robots, /^allowed/);
  assert.match(page.bytes_sha256, /^[a-f0-9]{64}$/);
  assert.ok(Date.parse(page.at));
});

test("site crawl reads sitemap and feed first, stays on host, skips disallowed and nofollow", async () => {
  const { http, calls } = fakeHttp(site());
  const out = await new Crawler({ http }).crawlSite(`${O}/`, { depth: 2, pageBudget: 10 });
  const order = out.pages.map((p) => p.url);
  assert.equal(order[0], `${O}/sitemap.xml`);
  assert.ok(order.indexOf(`${O}/feed.xml`) < order.indexOf(`${O}/b`), "feed before ordinary links");
  assert.ok(!calls.some((c) => c.url.startsWith("https://other.test")));
  assert.ok(!calls.some((c) => c.url === `${O}/nf`));
  assert.ok(!calls.some((c) => c.url.includes("/private/")));
  assert.equal(new Set(order).size, order.length, "no URL twice");
});

test("page budget and depth are hard caps", async () => {
  const { http } = fakeHttp(site());
  const two = await new Crawler({ http }).crawlSite(`${O}/`, { depth: 3, pageBudget: 2 });
  assert.equal(two.pages.length, 2);
  const shallow = fakeHttp(site());
  const zero = await new Crawler({ http: shallow.http }).crawlSite(`${O}/`, { depth: 0, pageBudget: 50 });
  assert.ok(!zero.pages.some((p) => p.url === `${O}/b`), "depth 0 must not follow links");
  const capped = await new Crawler({ http: fakeHttp(site()).http }).crawlSite(`${O}/`, { depth: 99, pageBudget: 999 });
  assert.equal(capped.depth, 3);
  assert.equal(capped.page_budget, 50);
});

test("only http and https are read", async () => {
  const { http } = fakeHttp({});
  await assert.rejects(new Crawler({ http }).fetchPage("file:///etc/passwd"), /only http and https/);
  assert.equal(normalizeUrl("https://Site.test:443/a#frag"), "https://site.test/a");
});

test("parsers: RSS, Atom, sitemap index, HTML links and meta robots", () => {
  const atom = '<feed xmlns="http://www.w3.org/2005/Atom"><title>A</title><entry><title>E &amp; F</title><link rel="alternate" href="https://x.test/e"/><updated>2026-01-01</updated></entry></feed>';
  assert.ok(isFeed(atom));
  assert.deepEqual(parseFeed(atom).items[0], { title: "E & F", link: "https://x.test/e", date: "2026-01-01", summary: "" });
  assert.equal(parseSitemap("<sitemapindex><sitemap><loc>https://x.test/s1.xml</loc></sitemap></sitemapindex>").kind, "index");
  const page = parseHtml('<meta name="robots" content="noindex,nofollow"><a href="/x">x</a><script>bad()</script>Hi', "https://x.test/");
  assert.deepEqual(page.links, [], "meta nofollow drops links");
  assert.equal(page.noindex, true);
  assert.doesNotMatch(page.text, /bad\(\)/);
  assert.deepEqual(parseHtml('<a href="javascript:x()">j</a><a href="/y#z">y</a>', "https://x.test/").links, ["https://x.test/y"]);
});

test("a bot-check page stops the read and says so", async () => {
  const { http, calls } = fakeHttp(site({ [`${O}/a`]: { status: 403, body: "<html>Please complete the CAPTCHA</html>" } }));
  const got = await new Crawler({ http }).fetchPage(`${O}/a`);
  assert.equal(got.page, null);
  assert.match(got.stopped, /bot check: Telos stops here/);
  assert.equal(calls.filter((c) => c.url === `${O}/a`).length, 1, "no retry against a bot check");
});
