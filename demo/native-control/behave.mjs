// Input-actuation primitives: move, click, type, scroll, and custom-dropdown
// selection, driven as CDP synthetic events so the operator's physical cursor
// stays free. The smooth motion and typing cadence here exist to reliably
// actuate real controls (rich editors, custom select widgets, drag targets),
// not to defeat a detector.
//
//   humanMove / humanClick   -> move + click a viewport coordinate
//   humanType / humanTypeKeys -> insert text / dispatch real keystrokes
//   scroll                    -> wheel/scroll the page
//   selectpick                -> open a custom dropdown and pick a matching option
//
// The personhood-forging layer that used to live here (stealth fingerprint
// patching + pre-submit behavioral seeding) has moved to redteam/evade.mjs,
// which is walled off the outreach path. See BOUNDARY.md.

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const rand = (a, b) => a + Math.random() * (b - a);

let last = { x: 400, y: 300 };

// Quadratic-bezier path from last to target with perpendicular bow + jitter.
export async function humanMove(session, x, y, { steps = 14 } = {}) {
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

// Type via key events (keyDown/char) for rich editors (LinkedIn DraftJS, Gmail
// compose, Slack) that ignore Input.insertText and need real keystrokes to
// update their React/editor state (and enable Submit/Post buttons).
export async function humanTypeKeys(session, text) {
  let n = 0;
  for (const ch of String(text)) {
    await session.send("Input.dispatchKeyEvent", { type: "rawKeyDown", text: ch, key: ch, unmodifiedText: ch });
    await session.send("Input.dispatchKeyEvent", { type: "char", text: ch, key: ch, unmodifiedText: ch });
    await session.send("Input.dispatchKeyEvent", { type: "keyUp", text: ch, key: ch, unmodifiedText: ch });
    await sleep(rand(30, 95));
    n++;
  }
  return { typed: n };
}

export async function scroll(session, dy) {
  await session.send("Input.dispatchMouseEvent", {
    type: "mouseWheel", x: last.x, y: last.y, deltaX: 0, deltaY: dy || rand(120, 400),
    button: "none", buttons: 0, modifiers: 0,
  }).catch(async () => { await session.send("Runtime.evaluate", { expression: `window.scrollBy(0,${Math.round(dy || 200)})` }); });
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
