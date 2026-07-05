// Share primitive for the autonomous engine: publish the operator's own content
// to their authenticated channels. LinkedIn feed post (authed) + Gumroad product
// listing (via Google SSO through the authed Gmail when the Gumroad session
// isn't carried). These are the operator's own accounts posting their own work.

import * as browser from "./browser.mjs";
import * as behave from "./behave.mjs";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Post text to the LinkedIn feed from the authed session.
export async function linkedinPost(session, { text }) {
  await browser.navigate(session, "https://www.linkedin.com/feed/");
  await sleep(4500);
  // click "Start a post"
  const open = `(()=>{const b=Array.from(document.querySelectorAll('button,div[role=button]')).find(e=>/start a post/i.test((e.innerText||'')+''));if(b){b.click();return true;}return false;})()`;
  await session.send("Runtime.evaluate", { expression: open, returnByValue: true });
  await sleep(2500);
  // focus + click the composer (contenteditable) and type with real key events
  // (LinkedIn DraftJS ignores insertText and keeps Post disabled).
  const focus = `(()=>{const ed=document.querySelector('div[role=textbox][contenteditable=true],div.share-box-controls__contenteditable,div.ql-editor');if(ed){ed.scrollIntoView({block:'center'});ed.focus();ed.click();return true;}return false;})()`;
  await session.send("Runtime.evaluate", { expression: focus, returnByValue: true });
  await sleep(600);
  await behave.humanTypeKeys(session, text);
  await sleep(1800);
  // click "Post"
  const post = `(()=>{const b=Array.from(document.querySelectorAll('button')).find(e=>/^post$/i.test((e.innerText||'')+'')&&!e.disabled);if(b){b.click();return {posted:true};}return {posted:false,disabled:true};})()`;
  const r = await session.send("Runtime.evaluate", { expression: post, returnByValue: true });
  await sleep(4000);
  return { text: text.slice(0, 80) + "...", result: r.result?.value };
}

// Log into Gumroad via Google SSO (credential-free, through the authed Gmail),
// then create a product. step fields: name, subtitle, description, price, file.
export async function gumroadLoginGoogle(session) {
  await browser.navigate(session, "https://gumroad.com/login");
  await sleep(3500);
  const clickGoogle = `(()=>{const b=Array.from(document.querySelectorAll('a,button')).find(e=>/google/i.test((e.innerText||'')+''));if(b){b.click();return true;}return false;})()`;
  await session.send("Runtime.evaluate", { expression: clickGoogle, returnByValue: true });
  await sleep(5000); // Google SSO consent / account pick
  // after SSO, Gumroad should be authed; verify
  const r = await session.send("Runtime.evaluate", { returnByValue: true, expression: `(()=>{const t=((document.body&&document.body.innerText)||'').toLowerCase();return {login:/log in|sign up/.test(t), products: /products|dashboard|new product/.test(t)};})()` });
  return { sso: true, state: r.result?.value };
}

// Create a Gumroad product (assumes authed). Best-effort against Gumroad's flow;
// returns what it could set + the page state for verification.
export async function gumroadList(session, { name, description, price, file } = {}) {
  await browser.navigate(session, "https://app.gumroad.com/products");
  await sleep(4000);
  const state = await session.send("Runtime.evaluate", { returnByValue: true, expression: `(()=>{const t=((document.body&&document.body.innerText)||'').toLowerCase();return {login:/log in|sign up/.test(t), hasNew:/new product|create/.test(t)};})()` });
  if (state.result?.value?.login) return { authed: false, note: "not authed; run gumroadLoginGoogle first", state: state.result.value };
  // click New product
  const open = `(()=>{const b=Array.from(document.querySelectorAll('a,button')).find(e=>/new product/i.test((e.innerText||'')+''));if(b){b.click();return true;}return false;})()`;
  await session.send("Runtime.evaluate", { expression: open, returnByValue: true });
  await sleep(3500);
  // fill name (the first prominent text input) + description + price; upload file
  const fill = `(()=>{
    const set=(el,v)=>{const p=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value')||Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value');if(p&&p.set)p.set.call(el,v);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));};
    const ins=Array.from(document.querySelectorAll('input[type=text],textarea,input:not([type])'));
    const named=ins.find(e=>/name|title/i.test(e.name+' '+e.id+' '+e.getAttribute('aria-label')+' '+(e.placeholder||'')));
    if(named&&arguments[0])set(named,arguments[0]);
    const desc=ins.find(e=>/description|desc/i.test(e.name+' '+e.id+' '+(e.placeholder||'')));
    if(desc&&arguments[1])set(desc,arguments[1]);
    const price=document.querySelector('input[name*=price],input[aria-label*=price],input[name*=amount]');
    if(price&&arguments[2])set(price,arguments[2]);
    return {setName:!!named,setDesc:!!desc,setPrice:!!price,inputs:ins.length};
  })(${JSON.stringify(name||'')},${JSON.stringify(description||'')},${JSON.stringify(price||'')})`;
  const f = await session.send("Runtime.evaluate", { expression: fill, returnByValue: true });
  if (file) { try { await browser.uploadFile(session, 'input[type=file]', file); } catch (e) {}
  }
  return { authed: true, fields: f.result?.value, file: file || null, note: "verify + Publish in the Gumroad UI" };
}
