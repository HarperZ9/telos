// Generic form filler for ANY website or auth flow. Driven by the HTML standard
// `autocomplete` tokens (given-name, email, tel, address-line1, postal-code,
// country-name, ...) that virtually every modern form -- job applications, login
// pages, sign-up flows, checkout -- emits, with type and label/name heuristics as
// fallback. React/Vue-aware via the native value setter + input/change dispatch.
//
//   forms fill <profile-json>   -> detect + fill every field on the page from the
//                                  profile; click radios/selects that match; check
//                                  consent checkboxes; return a per-field report.
//                                  Detects a LOGIN form (password field) and fills
//                                  email+password from profile.credentials when
//                                  present, else reports login-required honestly.

import { readFileSync } from "node:fs";
import { homedir } from "node:os";

// Read the operator's candidate profile and map it to the generic form shape.
// `answers` is keyed by substrings likely to appear in a question's text so the
// generic radio matcher works across any ATS (Ashby, Greenhouse, Workday, ...).
export function defaultProfile(profilePath) {
  const path = profilePath || `${homedir()}/career-campaign/candidate-profile.json`;
  let raw = {};
  try { raw = JSON.parse(readFileSync(path, "utf-8")); } catch { /* caller passes a profile */ }
  const [first, ...rest] = (raw.name || "").split(" ");
  const last = rest.length ? rest[rest.length - 1] : "";
  const middle = rest.length > 1 ? rest.slice(0, -1).join(" ") : "";
  return {
    firstName: first, middleName: middle, lastName: last,
    email: raw.email, phone: raw.phone,
    location: raw.location, city: "Seattle", region: "WA",
    country: "United States", countryCode: "US", postal: null,
    linkedin: (raw.links && raw.links.linkedin) || null,
    github: (raw.links && raw.links.github) || null,
    url: "https://harperz9.github.io",
    answers: {
      authorized: "Yes",
      sponsorship: "No",
      gender: "Male",
      race: "White",
      veteran: "I am not a protected veteran",
      disability: "Yes, I have a disability",
      relocate: "No",
      "san francisco": "No",
    },
    consent: true,
  };
}

const FILL_JS = (profileJson) => `
(() => {
  const P = ${profileJson};
  const log = { filled: [], skipped: [], radio: [], select: [], checkbox: [], login: false, unresolved: [] };
  const lc = (s) => (s == null ? "" : String(s)).toLowerCase();

  // --- autocomplete-token -> profile value (the primary, standard signal) ---
  const AUTO = {
    "given-name": P.firstName, "given_name": P.firstName, "fname": P.firstName, "first-name": P.firstName,
    "family-name": P.lastName, "family_name": P.lastName, "lname": P.lastName, "last-name": P.lastName,
    "additional-name": P.middleName, "name": (P.firstName && P.lastName ? P.firstName + " " + P.lastName : null),
    "email": P.email, "username": P.email,
    "tel": P.phone, "tel-national": P.phone, "phone": P.phone,
    "street-address": P.address, "address-line1": P.address, "address_line1": P.address,
    "address-level2": P.city, "locality": P.city, "city": P.city,
    "address-level1": P.region, "region": P.region, "state": P.region, "province": P.region,
    "postal-code": P.postal, "postal_code": P.postal, "zip": P.postal, "zip-code": P.postal,
    "country-name": P.country, "country": P.country, "country-code": P.countryCode,
    "organization": P.company, "organization-name": P.company, "company": P.company, "company-name": P.company,
    "url": P.url, "website": P.url, "linkedin": P.linkedin,
  };
  const byLabel = {
    first: P.firstName, given: P.firstName, "first name": P.firstName,
    last: P.lastName, surname: P.lastName, family: P.lastName,
    email: P.email, "e-mail": P.email,
    phone: P.phone, telephone: P.phone, mobile: P.phone, "cell": P.phone,
    linkedin: P.linkedin, "github": P.github, website: P.url, portfolio: P.url,
    location: P.location, city: P.city, state: P.region, "zip": P.postal, postal: P.postal,
    country: P.country, address: P.address,
  };

  const setVal = (el, val) => {
    if (val == null || val === "") return false;
    const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const d = Object.getOwnPropertyDescriptor(proto, "value");
    if (d && d.set && (el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement)) d.set.call(el, String(val));
    else { el.focus(); el.textContent = String(val); }
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
    el.dispatchEvent(new Event("blur", { bubbles: true }));
    return true;
  };
  const resolve = (el) => {
    const ac = lc(el.getAttribute("autocomplete"));
    if (ac && AUTO[ac] != null) return { val: AUTO[ac], why: "auto:" + ac };
    // multi-token autocomplete (e.g. "section-cc given-name")
    for (const tok of ac.split(/\s+/)) if (AUTO[tok] != null) return { val: AUTO[tok], why: "auto:" + tok };
    const t = lc(el.getAttribute("type"));
    if (t === "email" && P.email) return { val: P.email, why: "type:email" };
    if ((t === "tel") && P.phone) return { val: P.phone, why: "type:tel" };
    if ((t === "url") && (P.url || P.linkedin)) return { val: P.url || P.linkedin, why: "type:url" };
    const hints = [el.name, el.id, el.getAttribute("placeholder"), el.getAttribute("aria-label"), (el.closest("label")||{}).innerText, (el.previousElementSibling||{}).innerText];
    const blob = lc(hints.join(" "));
    for (const k in byLabel) if (blob.includes(k) && byLabel[k] != null) return { val: byLabel[k], why: "label:" + k };
    return null;
  };

  // --- text inputs / textareas ---
  let hasPassword = false;
  for (const el of document.querySelectorAll("input:not([type=radio]):not([type=checkbox]):not([type=file]):not([type=hidden]):not([type=submit]):not([type=button]):not([type=image]), textarea")) {
    try {
      const t = lc(el.getAttribute("type"));
      if (t === "password") { hasPassword = true; if (P.credentials && P.credentials.password) { setVal(el, P.credentials.password); log.filled.push("password"); } else log.unresolved.push("password"); continue; }
      const r = resolve(el);
      if (r) { if (setVal(el, r.val)) log.filled.push(r.why + "=[" + el.name + "|" + el.id + "]"); }
      else log.skipped.push((el.name || el.id || el.placeholder || "?").slice(0, 40));
    } catch (e) { log.unresolved.push("err:" + (el.name || "?")); }
  }
  log.login = hasPassword;

  // --- radios: group by name, click the option whose label matches profile.answers[question hint] ---
  const radioGroups = {};
  for (const el of document.querySelectorAll("input[type=radio]")) { (radioGroups[el.name] = radioGroups[el.name] || []).push(el); }
  for (const name in radioGroups) {
    try {
      // question hint = the group's surrounding label text
      const first = radioGroups[name][0];
      const container = first.closest("fieldset,div,section") || document.body;
      const q = lc(container.innerText || "").slice(0, 120);
      // find a desired answer: scan profile.answers keys for one mentioned in q
      let want = null, why = "";
      if (P.answers) for (const key in P.answers) if (q.includes(lc(key))) { want = P.answers[key]; why = "answers:" + key; break; }
      let clicked = false;
      for (const el of radioGroups[name]) {
        const lbl = lc((el.closest("label")||{}).innerText || el.value || "");
        if (want && (lbl === lc(want) || (lbl.length < 40 && lbl.includes(lc(want))))) { el.closest("label") ? el.closest("label").click() : el.click(); log.radio.push(why + "=" + want + " ["+name+"]"); clicked = true; break; }
      }
      if (!clicked) log.skipped.push("radio-group:" + name + (want ? " (want:"+want+" not found)" : " (no answer mapped)"));
    } catch (e) {}
  }

  // --- selects: choose the option matching a profile value ---
  for (const el of document.querySelectorAll("select")) {
    try {
      const r = resolve(el); let done = false;
      if (r) for (const opt of el.options) { if (lc(opt.text) === lc(r.val) || lc(opt.value) === lc(r.val)) { el.value = opt.value; el.dispatchEvent(new Event("change",{bubbles:true})); log.select.push(r.why); done = true; break; } }
      if (!done) log.skipped.push("select:" + (el.name || el.id || "?").slice(0, 30));
    } catch (e) {}
  }

  // --- consent / acknowledgement checkboxes (arbitration, terms, eeo consent) ---
  for (const el of document.querySelectorAll("input[type=checkbox]")) {
    try {
      const blob = lc([el.name, el.id, el.getAttribute("aria-label"), (el.closest("label")||{}).innerText].join(" "));
      if (P.consent !== false && (blob.includes("consent") || blob.includes("acknowledge") || blob.includes("certify") || blob.includes("i confirm") || blob.includes("i agree") || blob.includes("arbitration") || blob.includes("terms"))) {
        if (!el.checked) { (el.closest("label")||el).click(); log.checkbox.push("consent:" + (el.name||el.id||"?").slice(0,24)); }
      }
    } catch (e) {}
  }
  return log;
})()`;

export function fillExpression(profile) {
  return FILL_JS(JSON.stringify(profile));
}

// Spatial-label filler: for obfuscated React ATS (Ashby «rN» fields with no
// autocomplete/name), associate each input to its visible label by on-screen
// rect proximity, then keyword-map the label text. Works on any layout.
export const SPATIAL_FILL_JS = (profileJson) => `
(() => {
  const P = ${profileJson};
  const log = { filled: [], unresolved: [], radio: [], select: [], checkbox: [], spatial: true };
  const kw = {
    "first": P.firstName, "given": P.firstName, "legal name": P.firstName, "first name": P.firstName,
    "last": P.lastName, "surname": P.lastName, "family": P.lastName, "last name": P.lastName,
    "email": P.email, "e-mail": P.email,
    "phone": P.phone, "telephone": P.phone, "mobile": P.phone, "number": P.phone,
    "linkedin": P.linkedin, "github": P.github, "website": P.url, "portfolio": P.url, "url": P.url,
    "located": P.location, "where": P.location, "location": P.location, "city": P.city,
    "address": P.address, "state": P.region, "zip": P.postal, "postal": P.postal, "country": P.country,
  };
  const setVal = (el, val) => {
    if (val == null || val === "") return false;
    const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const d = Object.getOwnPropertyDescriptor(proto, "value");
    if (d && d.set) d.set.call(el, String(val)); else { el.focus(); el.textContent = String(val); }
    el.dispatchEvent(new Event("input", { bubbles: true })); el.dispatchEvent(new Event("change", { bubbles: true }));
    return true;
  };
  // candidate labels: short visible text elements with a rect
  const labels = Array.from(document.querySelectorAll("label,p,span,div,legend,h1,h2,h3,h4"))
    .map(e => ({ e, t: ((e.innerText||"")+"").trim(), r: e.getBoundingClientRect() }))
    .filter(o => o.t && o.t.length < 50 && o.r.width > 0 && o.r.height > 0);
  const nearest = (ir) => {
    let best = null, bd = 1e9;
    for (const l of labels) {
      // a label is "for" an input if it sits just above it (label bottom near input top) and overlaps horizontally
      const dy = ir.top - l.r.bottom;
      const overlap = Math.min(ir.right, l.r.right) - Math.max(ir.left, l.r.left);
      if (dy >= -8 && dy < 90 && overlap > 0) { const d = dy + Math.max(0, 40 - overlap); if (d < bd) { bd = d; best = l; } }
    }
    return best ? best.t : "";
  };
  for (const el of document.querySelectorAll("input:not([type=radio]):not([type=checkbox]):not([type=file]):not([type=hidden]):not([type=submit]):not([type=button]):not([type=image]), textarea")) {
    try {
      const ir = el.getBoundingClientRect(); if (ir.width === 0) continue;
      const ac = (el.getAttribute("autocomplete")||"").toLowerCase();
      let val = null, why = "";
      for (const tok of ac.split(/\\s+/)) if (kw[tok] != null) { val = kw[tok]; why = "auto:"+tok; break; }
      if (val == null) {
        const blob = ((el.name||"")+" "+(el.id||"")+" "+(el.placeholder||"")+" "+(el.getAttribute("aria-label")||"")).toLowerCase();
        const lbl = (nearest(ir) + " " + blob).toLowerCase();
        for (const k in kw) if (lbl.includes(k) && kw[k] != null) { val = kw[k]; why = "spatial:"+k; break; }
      }
      if (val != null) { if (setVal(el, val)) log.filled.push(why + "=" + String(val).slice(0,30)); }
      else log.unresolved.push((el.placeholder || el.name || el.id || "?").slice(0, 30));
    } catch (e) {}
  }
  // radios + checkboxes: associate by nearest label (question text), then click option matching profile.answers
  const groups = {};
  for (const el of document.querySelectorAll("input[type=radio]")) (groups[el.name] = groups[el.name] || []).push(el);
  for (const name in groups) {
    try {
      const ir = groups[name][0].getBoundingClientRect();
      const q = nearest(ir).toLowerCase();
      let want = null;
      if (P.answers) for (const k in P.answers) if (q.includes(k.toLowerCase())) { want = P.answers[k]; break; }
      let clicked = false;
      if (want) for (const el of groups[name]) {
        const ol = el.getBoundingClientRect();
        const otext = (nearest(ol) + " " + (el.value||"")).toLowerCase();
        if (otext.includes(want.toLowerCase()) || want.toLowerCase().includes(otext.replace(/[^a-z ]/g,"").trim()) && otext.trim()) {
          (el.closest("label")||el).click(); log.radio.push(q.slice(0,20)+"="+want); clicked = true; break;
        }
      }
      if (!clicked) log.unresolved.push("radio:" + (q||name).slice(0,24) + (want ? " want:"+want : ""));
    } catch (e) {}
  }
  for (const el of document.querySelectorAll("input[type=checkbox]")) {
    try { const t = nearest(el.getBoundingClientRect()).toLowerCase();
      if (P.consent !== false && /consent|acknowledge|certify|confirm|agree|arbitration|terms/.test(t)) {
        if (!el.checked) { (el.closest("label")||el).click(); log.checkbox.push("consent:"+t.slice(0,20)); } } } catch (e) {}
  }
  return log;
})()`;

export async function spatialFill(session, profile) {
  const res = await session.send("Runtime.evaluate", { expression: SPATIAL_FILL_JS(JSON.stringify(profile)), returnByValue: true });
  if (res.exceptionDetails) throw new Error(`spatial fill failed: ${res.exceptionDetails.text}`);
  return res.result?.value;
}

export async function fill(session, profile) {
  const res = await session.send("Runtime.evaluate", {
    expression: fillExpression(profile),
    returnByValue: true,
    awaitPromise: false,
  });
  if (res.exceptionDetails) throw new Error(`forms fill failed: ${res.exceptionDetails.text}`);
  return res.result?.value;
}
