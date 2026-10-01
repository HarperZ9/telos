// CDP input primitives for coordinate-based click, text entry, scroll, and
// custom-dropdown selection. These wrap Input.dispatch* and Runtime.evaluate for
// form workflows where CSS selectors cannot reach the target (cross-origin
// iframes, rich editors, custom select widgets).
//
// Pacing is fixed and deterministic. A short constant pause between keystrokes
// lets rich editors settle their state; it is not randomized and does not
// imitate human timing. Telos does not ship input "humanization", CAPTCHA
// handling, or any other bot-check bypass (demo/bypass-capability-guard.test.mjs).

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Default pause between keystrokes for editors that rebuild state per key.
export const KEY_PAUSE_MS = 20;
// Default pause for a custom dropdown to open or filter.
export const MENU_PAUSE_MS = 400;

function pause(value, fallback) {
  const ms = value == null ? fallback : Number(value);
  if (!Number.isFinite(ms) || ms < 0) throw new Error(`invalid pause: ${value}`);
  return ms;
}

export async function pointerClick(session, x, y) {
  for (const type of ["mousePressed", "mouseReleased"]) {
    await session.send("Input.dispatchMouseEvent", {
      type, x: Number(x), y: Number(y),
      button: "left", clickCount: 1,
      buttons: type === "mouseReleased" ? 0 : 1,
    });
  }
  return { clicked: [x, y] };
}

export async function typeText(session, text, { pauseMs } = {}) {
  const wait = pause(pauseMs, KEY_PAUSE_MS);
  let n = 0;
  for (const ch of String(text)) {
    await session.send("Input.insertText", { text: ch });
    if (wait) await sleep(wait);
    n++;
  }
  return { typed: n, pauseMs: wait };
}

// Type via key events (keyDown/char/keyUp) for rich editors that ignore
// Input.insertText and only update their state from real key events.
export async function typeKeys(session, text, { pauseMs } = {}) {
  const wait = pause(pauseMs, KEY_PAUSE_MS);
  let n = 0;
  for (const ch of String(text)) {
    await session.send("Input.dispatchKeyEvent", { type: "rawKeyDown", text: ch, key: ch, unmodifiedText: ch });
    await session.send("Input.dispatchKeyEvent", { type: "char", text: ch, key: ch, unmodifiedText: ch });
    await session.send("Input.dispatchKeyEvent", { type: "keyUp", text: ch, key: ch, unmodifiedText: ch });
    if (wait) await sleep(wait);
    n++;
  }
  return { typed: n, pauseMs: wait };
}

export async function scroll(session, dy) {
  const amount = dy || 200;
  await session.send("Runtime.evaluate", {
    expression: `window.scrollBy(0,${Math.round(amount)})`,
  });
}

// Generic custom-dropdown selector: click the field to open its popup, then click
// the option whose text matches `want`. Handles custom select widgets, country
// pickers, and combobox search dropdowns that text-entry filling cannot actuate.
export async function selectOption(session, fieldSelector, want, { searchFallback = true, pauseMs } = {}) {
  const wait = pause(pauseMs, MENU_PAUSE_MS);
  const open = `(()=>{const el=document.querySelector(${JSON.stringify(fieldSelector)});if(!el)return false;el.scrollIntoView({block:'center'});el.focus();el.click();el.dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));return true;})()`;
  await session.send("Runtime.evaluate", { expression: open, returnByValue: true });
  await sleep(wait);
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
    await sleep(wait);
    const pick2 = pick.replace("return 'typed-search';", "return null;");
    const r2 = await session.send("Runtime.evaluate", { expression: pick2, returnByValue: true });
    return { picked: r2.result?.value || "search-typed" };
  }
  return { picked: r.result?.value };
}
