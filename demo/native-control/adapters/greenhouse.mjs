// Greenhouse job-board application adapter. Encodes Greenhouse's widget
// contracts so the runner fills + submits a Greenhouse form reliably:
//
//   - intl-tel-input (iti) phone: the country is a separate widget; the phone
//     NUMBER must be set on the underlying tel input WITH iti's events.
//   - Greenhouse custom Yes/No + single-select questions: div-based dropdowns
//     whose backing value registers only when the option's click fires the
//     widget's own select handler -- opened, option found, clicked.
//
// Methods: fill(ctx, step), submit(ctx, step), check(ctx, step).

import * as forms from "../forms.mjs";
import * as behave from "../behave.mjs";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Set the phone number into the iti input with the events iti listens to.
async function setPhone(session, phone) {
  const expr = `(()=>{
    const el=document.querySelector('#phone,input[type=tel]');
    if(!el)return false;
    const p=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value');
    p.set.call(el,${JSON.stringify(phone)});
    ['input','change','keyup','blur'].forEach(t=>el.dispatchEvent(new Event(t,{bubbles:true})));
    return true;
  })()`;
  await session.send("Runtime.evaluate", { expression: expr, returnByValue: true });
}

// Greenhouse custom-question dropdown: open the question by its label, click the
// matching option. `qLabel` is a substring of the question text; `want` is the
// option text to pick.
async function pickQuestion(session, qLabel, want) {
  const open = `(()=>{
    const lbls=Array.from(document.querySelectorAll('label,p,div,span'));
    const q=lbls.find(e=>{const t=((e.innerText||'')+'').toLowerCase();return t.includes(${JSON.stringify(qLabel.toLowerCase())})&&t.length<200;});
    if(!q)return null;
    const box=q.closest('div,li,fieldset')||q.parentElement;
    const trig=box.querySelector('[class*=select],[class*=Select],[role=combobox],[role=button],button')||box;
    trig.click();trig.dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));
    return true;
  })()`;
  await session.send("Runtime.evaluate", { expression: open, returnByValue: true });
  await sleep(450);
  const pick = `(()=>{
    const want=${JSON.stringify((want+'').toLowerCase())};
    const opts=Array.from(document.querySelectorAll('[role=option],[role=listbox] *,.option,li[class*=option],div[class*=option],[class*=Option]'));
    const m=opts.find(o=>((o.innerText||o.textContent||'')+'').trim().toLowerCase().includes(want));
    if(m){m.click();m.dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));return ((m.innerText||'')+'').trim();}
    return null;
  })()`;
  const r = await session.send("Runtime.evaluate", { expression: pick, returnByValue: true });
  return r.result?.value;
}

export default {
  name: "greenhouse",

  async fill(ctx) {
    const profile = ctx.profile;
    // 1. standard text fields via the generic engine filler (autocomplete-driven)
    await forms.fill(ctx.session, profile);
    // 2. phone into the iti widget with proper events
    await setPhone(ctx.session, profile.phone);
    // 3. Greenhouse custom Yes/No questions
    await pickQuestion(ctx.session, "require sponsorship", "No");
    await pickQuestion(ctx.session, "authorized to work", "Yes");
    await pickQuestion(ctx.session, "how did you hear", "LinkedIn"); // common; harmless if absent
    return { adapter: "greenhouse", filled: "standard+phone+custom-questions" };
  },

  async submit(ctx) {
    const r = await ctx.session.send("Runtime.evaluate", {
      returnByValue: true,
      expression: `(()=>{const b=Array.from(document.querySelectorAll('button,input[type=submit]')).find(b=>/submit/i.test((b.innerText||b.value||'')));if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return{x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)};})()`,
    });
    const coords = r.result?.value;
    if (coords) await behave.humanClick(ctx.session, coords.x, coords.y);
    return { adapter: "greenhouse", clicked: coords };
  },

  async check(ctx) {
    const r = await ctx.session.send("Runtime.evaluate", {
      returnByValue: true,
      expression: `(()=>{const t=((document.body&&document.body.innerText)||'').toLowerCase();
        const errs=Array.from(document.querySelectorAll('[class*=error],[role=alert]')).map(e=>((e.innerText||'')+'').trim()).filter(x=>x).slice(0,8);
        const succ=/thank you|application received|we received|successfully submitted/.test(t);
        return { success: succ, errors: errs, title: document.title };})()`,
    });
    return r.result?.value;
  },
};
