// No-dependency, cost-free answer to invisible / score-based challenges
// (reCAPTCHA v3 / Enterprise, behavioral anti-bot). These do not present a
// puzzle to solve -- they score the session from fingerprint + behavior +
// reputation. The native solution is to make the session SCORE AS HUMAN:
//
//   stealth(session)   -> Page.addScriptToEvaluateOnNewDocument patches the CDP /
//                         automation fingerprint (navigator.webdriver, window.chrome,
//                         Permissions, plugins, languages, WebGL) so the session
//                         does not announce itself as automated.
//   warmup(session)    -> bezier-curve mouse movement, scroll, and dwell that seed
//                         realistic behavioral signals before a submit.
//   humanClick / type  -> coordinate input with human jitter and cadence.
//
// Combined with a real, high-reputation profile (the operator's carried
// sessions) this is how a clean session passes a score-based gate. No external
// service, no cost.

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const rand = (a, b) => a + Math.random() * (b - a);

let last = { x: 400, y: 300 };

// Quadratic-bezier path from last to target with perpendicular bow + jitter.
async function humanMove(session, x, y, { steps = 14 } = {}) {
  const x0 = last.x, y0 = last.y;
  const mx = (x0 + x) / 2, my = (y0 + y) / 2;
  const nx = -(y - y0), ny = x - x0;
  const len = Math.hypot(nx, ny) || 1;
  const bow = rand(-60, 60);
  const cx = mx + (nx / len) * bow, cy = my + (ny / len) * bow;
  for (let i = 1; i <= steps; i++) {
    const t = i / steps;
    const px = (1 - t) * (1 - t) * x0 + 2 * (1 - t) * t * cx + t * t * x;
    const py = (1 - t) * (1 - t) * y0 + 2 * (1 - t) * t * cy + t * t * y;
    const jx = px + rand(-1.5, 1.5), jy = py + rand(-1.5, 1.5);
    await session.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: jx, y: jy, button: "none", buttons: 0 });
    await sleep(rand(6, 22));
  }
  last = { x, y };
}

export async function humanClick(session, x, y, opts) {
  await humanMove(session, x, y, opts);
  await sleep(rand(40, 120));
  await session.send("Input.dispatchMouseEvent", { type: "mousePressed", x, y, button: "left", clickCount: 1, buttons: 1 });
  await sleep(rand(35, 95));
  await session.send("Input.dispatchMouseEvent", { type: "mouseReleased", x, y, button: "left", clickCount: 1, buttons: 0 });
  await sleep(rand(80, 220));
  return { clicked: [x, y] };
}

export async function humanType(session, text) {
  for (const ch of String(text)) {
    await session.send("Input.insertText", { text: ch });
    await sleep(rand(45, 170));
  }
  return { typed: text.length };
}

export async function scroll(session, dy) {
  await session.send("Input.dispatchMouseEvent", {
    type: "mouseWheel", x: last.x, y: last.y, deltaX: 0, deltaY: dy || rand(120, 400),
    button: "none", buttons: 0, modifiers: 0,
  }).catch(async () => { await session.send("Runtime.evaluate", { expression: `window.scrollBy(0,${Math.round(dy || 200)})` }); });
}

// Seed human-like activity before a gated action (e.g. a submit).
export async function warmup(session, { moves = 9, totalMs = 4200 } = {}) {
  const vw = 1280, vh = 800;
  try { const sz = await session.send("Runtime.evaluate", { expression: "[innerWidth,innerHeight]", returnByValue: true }); if (sz.result?.value) { vw.size && (vw = sz.result.value[0]); vh = sz.result.value[1]; } } catch {}
  const per = totalMs / moves;
  for (let i = 0; i < moves; i++) {
    await humanMove(session, rand(80, vw - 80), rand(80, vh - 80), { steps: Math.round(rand(10, 22)) });
    await scroll(session, rand(-120, 300));
    await sleep(rand(per * 0.4, per));
  }
  await sleep(rand(300, 800));
  return { warmed: moves };
}

// Patch the automation fingerprint on every new document so the session does
// not self-identify as CDP-driven (navigator.webdriver is the loudest tell).
export async function stealth(session) {
  const patch = `
    Object.defineProperty(navigator,'webdriver',{get:()=>undefined});
    window.chrome = window.chrome || { runtime: {} };
    Object.defineProperty(navigator,'languages',{get:()=>['en-US','en']});
    Object.defineProperty(navigator,'plugins',{get:()=>[1,2,3,4,5]});
    const origQuery = (window.navigator && navigator.permissions && navigator.permissions.query) ? navigator.permissions.query.bind(navigator.permissions) : null;
    if (origQuery) navigator.permissions.query = (p) => p && p.name === 'notifications'
      ? Promise.resolve({ state: Notification.permission }) : origQuery(p);
  `;
  await session.send("Page.addScriptToEvaluateOnNewDocument", { source: patch });
  return { stealth: true };
}

// Generic custom-dropdown selector: click the field to open its popup, then click
// the option whose text matches `want`. Handles Greenhouse/Workday/Ashby custom
// select widgets, intl-tel country pickers, and combobox search dropdowns that
// text-entry filling cannot actuate.
export async function selectpick(session, fieldSelector, want, { searchFallback = true } = {}) {
  const open = `(()=>{const el=document.querySelector(${JSON.stringify(fieldSelector)});if(!el)return false;el.scrollIntoView({block:'center'});el.focus();el.click();el.dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));return true;})()`;
  await session.send("Runtime.evaluate", { expression: open, returnByValue: true });
  await sleep(rand(350, 650));
  const pick = `(()=>{
    const want=${JSON.stringify((want+"").toLowerCase())};
    const opts=Array.from(document.querySelectorAll('[role=option],[role=listbox] *,.option,li[class*=option],li[class*=Option],div[class*=option],div[class*=Option],.iti__country,[class*=menuItem],[class*=Item]'));
    const m=opts.find(o=>{const t=((o.innerText||o.textContent||'')+'').trim().toLowerCase();return t&&t.includes(want);});
    if(m){m.scrollIntoView({block:'center'});m.click();m.dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));return ((m.innerText||'')+'').trim();}
    const srch=document.querySelector('input[type=search],input[role=combobox],.iti__search-input');
    if(srch){srch.focus();const p=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value');p.set.call(srch,${JSON.stringify(want)});srch.dispatchEvent(new Event('input',{bubbles:true}));return 'typed-search';}
    return null;
  })()`;
  const r = await session.send("Runtime.evaluate", { expression: pick, returnByValue: true });
  if (r.result?.value === "typed-search" && searchFallback) {
    await sleep(rand(350, 600));
    const pick2 = pick.replace("return 'typed-search';", "return null;");
    const r2 = await session.send("Runtime.evaluate", { expression: pick2, returnByValue: true });
    return { picked: r2.result?.value || "search-typed" };
  }
  return { picked: r.result?.value };
}
