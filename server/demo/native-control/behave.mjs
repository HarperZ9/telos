// CDP input primitives for coordinate-based click, type, scroll, and custom-
// dropdown selection. These wrap Input.dispatch* and Runtime.evaluate for
// form-filling workflows where CSS selectors cannot reach the target (cross-
// origin iframes, obfuscated React widgets, rich editors).

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const rand = (a, b) => a + Math.random() * (b - a);

export async function humanClick(session, x, y) {
  for (const type of ["mousePressed", "mouseReleased"]) {
    await session.send("Input.dispatchMouseEvent", {
      type, x: Number(x), y: Number(y),
      button: "left", clickCount: 1,
      buttons: type === "mouseReleased" ? 0 : 1,
    });
  }
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
  const amount = dy || 200;
  await session.send("Runtime.evaluate", {
    expression: `window.scrollBy(0,${Math.round(amount)})`,
  });
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
