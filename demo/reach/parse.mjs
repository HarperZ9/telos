// Small parsers written here with no dependency: RSS 2.0, Atom, sitemaps, and
// enough HTML to get a title, readable text, links and feed links. They are
// tolerant readers for agent use, not validators.

const ENTITIES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " " };

export function decodeEntities(text) {
  return String(text ?? "").replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (whole, code) => {
    if (code[0] === "#") {
      const n = code[1].toLowerCase() === "x" ? parseInt(code.slice(2), 16) : parseInt(code.slice(1), 10);
      return Number.isFinite(n) && n > 0 && n < 0x110000 ? String.fromCodePoint(n) : whole;
    }
    return ENTITIES[code.toLowerCase()] ?? whole;
  });
}

function stripCdata(text) {
  return String(text ?? "").replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1");
}

/** Inner text of the first <tag> in xml, decoded, or null. */
export function tagText(xml, tag) {
  const match = xml.match(new RegExp(`<${tag}(?:\\s[^>]*)?>([\\s\\S]*?)</${tag}>`, "i"));
  return match ? decodeEntities(stripCdata(match[1])).trim() : null;
}

function blocks(xml, tag) {
  return [...xml.matchAll(new RegExp(`<${tag}(?:\\s[^>]*)?>([\\s\\S]*?)</${tag}>`, "gi"))].map((m) => m[1]);
}

function atomLink(entry) {
  const links = [...entry.matchAll(/<link\b([^>]*)\/?>/gi)].map((m) => m[1]);
  const pick = links.find((attrs) => !/rel=["'](?!alternate)/i.test(attrs)) ?? links[0];
  const href = pick?.match(/href=["']([^"']+)["']/i);
  return href ? decodeEntities(href[1]) : null;
}

/** True when the text looks like an RSS or Atom document. */
export function isFeed(text) {
  return /<rss[\s>]|<feed[\s>][\s\S]*xmlns=["']http:\/\/www\.w3\.org\/2005\/Atom/i.test(String(text).slice(0, 4000));
}

/** Parse RSS or Atom into { kind, title, items: [{ title, link, date, summary }] }. */
export function parseFeed(xml) {
  const text = String(xml ?? "");
  if (/<rss[\s>]/i.test(text)) {
    const channel = blocks(text, "channel")[0] ?? text;
    const items = blocks(text, "item").map((item) => ({
      title: tagText(item, "title"),
      link: tagText(item, "link"),
      date: tagText(item, "pubDate") ?? tagText(item, "dc:date"),
      summary: htmlToText(tagText(item, "description") ?? "").slice(0, 500),
    }));
    return { kind: "rss", title: tagText(channel.split(/<item[\s>]/i)[0], "title"), items };
  }
  const items = blocks(text, "entry").map((entry) => ({
    title: tagText(entry, "title"),
    link: atomLink(entry),
    date: tagText(entry, "updated") ?? tagText(entry, "published"),
    summary: htmlToText(tagText(entry, "summary") ?? tagText(entry, "content") ?? "").slice(0, 500),
  }));
  return { kind: "atom", title: tagText(text.split(/<entry[\s>]/i)[0], "title"), items };
}

/** Parse a sitemap or sitemap index into { kind, urls }. */
export function parseSitemap(xml) {
  const text = String(xml ?? "");
  const kind = /<sitemapindex[\s>]/i.test(text) ? "index" : "urlset";
  const urls = blocks(text, "loc").map((loc) => decodeEntities(stripCdata(loc)).trim()).filter(Boolean);
  return { kind, urls };
}

/** Readable text from HTML: drops script, style and tags, collapses space. */
export function htmlToText(html) {
  return decodeEntities(
    String(html ?? "")
      .replace(/<(script|style|noscript|template|svg)\b[\s\S]*?<\/\1>/gi, " ")
      .replace(/<!--[\s\S]*?-->/g, " ")
      .replace(/<\/(p|div|li|h[1-6]|tr|section|article|br)\s*>|<br\s*\/?>/gi, "\n")
      .replace(/<[^>]+>/g, " ")
  )
    .replace(/[ \t\f\v\r]+/g, " ")
    .replace(/\s*\n\s*/g, "\n")
    .trim();
}

function resolveHref(href, base) {
  try {
    const url = new URL(decodeEntities(href), base);
    if (url.protocol !== "http:" && url.protocol !== "https:") return null;
    url.hash = "";
    return url.toString();
  } catch {
    return null;
  }
}

/** Title, text, links and feed links of an HTML page. Honors rel=nofollow. */
export function parseHtml(html, base) {
  const source = String(html ?? "");
  const robotsMeta = source.match(/<meta[^>]+name=["']robots["'][^>]*content=["']([^"']+)["']/i)?.[1]?.toLowerCase() ?? "";
  const anchors = [...source.matchAll(/<a\b([^>]*)>/gi)].map((m) => m[1]);
  const links = robotsMeta.includes("nofollow")
    ? []
    : anchors.filter((a) => !/rel=["'][^"']*nofollow/i.test(a)).map((a) => a.match(/href=["']([^"']+)["']/i)?.[1]).filter(Boolean).map((h) => resolveHref(h, base)).filter(Boolean);
  const feeds = [...source.matchAll(/<link\b([^>]*)>/gi)]
    .map((m) => m[1])
    .filter((a) => /rel=["']alternate["']/i.test(a) && /type=["']application\/(rss|atom)\+xml["']/i.test(a))
    .map((a) => resolveHref(a.match(/href=["']([^"']+)["']/i)?.[1] ?? "", base))
    .filter(Boolean);
  return {
    title: tagText(source, "title"),
    text: htmlToText(source.replace(/<head\b[\s\S]*?<\/head>/i, " ")),
    links: [...new Set(links)],
    feeds: [...new Set(feeds)],
    noindex: robotsMeta.includes("noindex"),
  };
}
