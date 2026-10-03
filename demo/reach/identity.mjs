// Who the reach layer says it is. Every request names Telos, its version and a
// contact URL, so a site operator can see what fetched a page and ask it to stop.
// The value is fixed: no option rotates it, randomizes it or copies a browser.
import { TELOS_VERSION } from "../version.mjs";

export const PROJECT_URL = "https://github.com/HarperZ9/telos";

/** The robots.txt product token Telos matches against `User-agent:` lines. */
export const ROBOTS_TOKEN = "telos";

/**
 * The honest User-Agent. TELOS_REACH_CONTACT may add the user's own contact
 * (an email or URL), which site operators prefer; it cannot replace the name.
 */
export function userAgent(env = process.env) {
  const contact = typeof env.TELOS_REACH_CONTACT === "string" ? env.TELOS_REACH_CONTACT.trim() : "";
  const safe = contact.replace(/[^\w@.:/+\-~]/g, "").slice(0, 120);
  const suffix = safe ? `; contact ${safe}` : "";
  return `Telos/${TELOS_VERSION} (+${PROJECT_URL}; reach crawler${suffix})`;
}

/** Methods the reach layer refuses to ship, stated once for receipts and docs. */
export const BOUNDARY = Object.freeze([
  "reads robots.txt and obeys Disallow and Crawl-delay",
  "one honest User-Agent naming Telos; no browser imitation",
  "no identity, proxy or account rotation",
  "no cookie or credential extraction from browsers",
  "no CAPTCHA handling; a bot check stops the read",
  "official APIs only for Reddit and X, with the user's own credentials",
]);
