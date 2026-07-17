// Scrape primitive for the autonomous engine: discover public targets (businesses,
// postings, leads) for outreach/application. Fetches a search-results page and
// extracts {title, url, snippet} per result. For B2B outreach this returns the
// target companies + their public sites; per-site email/contact-form discovery is
// a follow-up pass (enrich). No credentials -- public web only.
//
//   scrape targets <query> [limit]  -> [{title, url, snippet}]

import * as browser from "./browser.mjs";

// DuckDuckGo's HTML endpoint is fetchable and parseable without an API key.
async function ddgHtml(query, fetchImpl = fetch) {
  const url = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`;
  const res = await fetchImpl(url, { headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" } });
  if (!res.ok) throw new Error(`search HTTP ${res.status}`);
  return res.text();
}

function parseResults(html, limit) {
  const out = [];
  const re = /<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([\s\S]*?)<\/a>[\s\S]*?<a[^>]+class="result__snippet"[^>]*>([\s\S]*?)<\/a>/g;
  let m;
  while ((m = re.exec(html)) && out.length < limit) {
    let href = m[1];
    // DDG wraps URLs in a redirect; unwrap the real uddg target.
    const u = /uddg=([^&]+)/.exec(href);
    if (u) href = decodeURIComponent(u[1]);
    const title = m[2].replace(/<[^>]+>/g, "").trim();
    const snippet = m[3].replace(/<[^>]+>/g, "").trim();
    if (title && href && !/duckduckgo\.com/.test(href)) out.push({ title, url: href, snippet: snippet.slice(0, 180) });
  }
  return out;
}

// In-engine scrape via the authed browser (more robust against bot-blocks than a
// raw fetch, and shares the carried session's reputation).
export async function targets(session, { query, limit = 12 } = {}) {
  const url = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`;
  await browser.navigate(session, url);
  await new Promise((r) => setTimeout(r, 2500));
  const r = await session.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `(()=>{
      const out=[];
      document.querySelectorAll('a.result__a').forEach((a,i)=>{
        if(i>=${limit})return;
        let href=a.href; const m=/uddg=([^&]+)/.exec(href); if(m)href=decodeURIComponent(m[1]);
        const sn=a.closest('.result')&&a.closest('.result').querySelector('.result__snippet');
        out.push({title:a.innerText.trim(),url:href,snippet:(sn?sn.innerText.trim():'').slice(0,180)});
      });
      return out;
    })()`,
  });
  const list = r.result?.value || [];
  // fallback to raw fetch if the in-browser parse returned nothing
  if (!list.length) {
    try { const html = await ddgHtml(query); return { query, count: 0, results: parseResults(html, limit), via: "fetch-fallback" }; }
    catch (e) { return { query, count: 0, results: [], error: String(e.message || e) }; }
  }
  return { query, count: list.length, results: list, via: "browser" };
}

// Enrich a target: from the CURRENT page (navigate to url first if given), find
// the public ways to reach them -- mailto addresses and contact/careers/apply
// links. Public web only; this reads what a visitor sees, it does not bypass any
// gate. Feed results into the review queue, not a blast.
export async function enrich(session, { url } = {}) {
  if (url) { await browser.navigate(session, url); await new Promise((r) => setTimeout(r, 1500)); }
  const r = await session.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `(() => {
      const abs = (h) => { try { return new URL(h, location.href).href; } catch { return null; } };
      const emails = new Set(), links = new Set();
      document.querySelectorAll('a[href]').forEach((a) => {
        const h = a.getAttribute('href') || '';
        if (/^mailto:/i.test(h)) emails.add(h.replace(/^mailto:/i, '').split('?')[0]);
        else if (/contact|careers?|jobs?|apply|about/i.test(h + ' ' + (a.innerText || ''))) { const u = abs(h); if (u) links.add(u); }
      });
      (((document.body && document.body.innerText) || '').match(/[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}/gi) || []).forEach((e) => emails.add(e));
      return { host: location.host, emails: [...emails].slice(0, 10), links: [...links].slice(0, 15) };
    })()`,
  });
  return r.result?.value || { emails: [], links: [] };
}
