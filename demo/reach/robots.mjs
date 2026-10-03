// robots.txt parsing and matching per RFC 9309, written here with no
// dependency. Groups are chosen by the most specific matching product token;
// within a group the longest matching rule wins and Allow wins a tie.
// Crawl-delay and Sitemap are read too, since sites still publish them.

function cleanLine(raw) {
  const hash = raw.indexOf("#");
  return (hash >= 0 ? raw.slice(0, hash) : raw).trim();
}

/** Parse robots.txt text into { groups, sitemaps }. */
export function parseRobots(text) {
  const groups = [];
  const sitemaps = [];
  let current = null;
  let lastWasAgent = false;
  for (const raw of String(text ?? "").split(/\r?\n/)) {
    const line = cleanLine(raw);
    const colon = line.indexOf(":");
    if (colon < 1) continue;
    const key = line.slice(0, colon).trim().toLowerCase();
    const value = line.slice(colon + 1).trim();
    if (key === "sitemap") {
      if (value) sitemaps.push(value);
      continue;
    }
    if (key === "user-agent") {
      if (!lastWasAgent || !current) {
        current = { agents: [], rules: [], crawlDelay: null };
        groups.push(current);
      }
      current.agents.push(value.toLowerCase());
      lastWasAgent = true;
      continue;
    }
    lastWasAgent = false;
    if (!current) continue;
    if (key === "allow" || key === "disallow") current.rules.push({ allow: key === "allow", path: value });
    else if (key === "crawl-delay") {
      const delay = Number(value);
      if (Number.isFinite(delay) && delay >= 0) current.crawlDelay = delay;
    }
  }
  return { groups, sitemaps };
}

/** Pick the group for a product token: exact token first, then `*`. */
export function selectGroup(parsed, token) {
  const name = token.toLowerCase();
  const exact = parsed.groups.filter((g) => g.agents.includes(name));
  const chosen = exact.length ? exact : parsed.groups.filter((g) => g.agents.includes("*"));
  if (!chosen.length) return null;
  return {
    rules: chosen.flatMap((g) => g.rules),
    crawlDelay: chosen.map((g) => g.crawlDelay).find((d) => d !== null) ?? null,
  };
}

function escapeRegex(text) {
  return text.replace(/[.+?^${}()|[\]\\]/g, "\\$&");
}

/** Compile a robots path pattern with `*` and a trailing `$` to a RegExp. */
export function patternToRegex(pattern) {
  const anchored = pattern.endsWith("$");
  const body = anchored ? pattern.slice(0, -1) : pattern;
  const source = body.split("*").map(escapeRegex).join(".*");
  return new RegExp(`^${source}${anchored ? "$" : ""}`);
}

function normalizePath(target) {
  try {
    const decoded = decodeURIComponent(target);
    return decoded.startsWith("/") ? decoded : `/${decoded}`;
  } catch {
    return target.startsWith("/") ? target : `/${target}`;
  }
}

/**
 * Decide one path. Returns { allowed, rule, crawlDelay }. An empty Disallow
 * allows everything; /robots.txt itself is always allowed (RFC 9309 2.2.2).
 */
export function decide(parsed, token, target) {
  const group = selectGroup(parsed, token);
  const pathOnly = normalizePath(target);
  if (!group || pathOnly === "/robots.txt") return { allowed: true, rule: null, crawlDelay: group?.crawlDelay ?? null };
  let best = null;
  for (const rule of group.rules) {
    if (!rule.path) continue;
    if (!patternToRegex(normalizePath(rule.path)).test(pathOnly)) continue;
    const longer = !best || rule.path.length > best.path.length;
    const tieAllow = best && rule.path.length === best.path.length && rule.allow && !best.allow;
    if (longer || tieAllow) best = rule;
  }
  return {
    allowed: best ? best.allow : true,
    rule: best ? `${best.allow ? "Allow" : "Disallow"}: ${best.path}` : null,
    crawlDelay: group.crawlDelay,
  };
}

/**
 * Policy for a robots.txt fetch outcome (RFC 9309 2.3.1): 2xx parses the body,
 * 4xx means no restrictions, 5xx or an unreachable host means disallow all.
 */
export function robotsFromStatus(status, body) {
  if (status >= 200 && status < 300) return { parsed: parseRobots(body), basis: "robots.txt" };
  if (status >= 400 && status < 500) return { parsed: parseRobots(""), basis: `robots.txt ${status}: no restrictions` };
  return { parsed: parseRobots("User-agent: *\nDisallow: /"), basis: `robots.txt ${status || "unreachable"}: disallow all` };
}
