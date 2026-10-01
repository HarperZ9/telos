// Base adapter contract. A per-site/ATS adapter encodes that platform's widget
// contracts so the runner can drive it without per-verb special-casing. Methods
// are async (ctx, step) => result, resolved via "act":"adapter.<method>".
//
// ctx = { session, profile, adapter }
// Recommended methods: fill, submit, check. Adapters may add any others.

export default {
  name: "base",
  async fill(ctx) {
    // default: standard autofill + spatial fallback
    await import("../forms.mjs").then((f) => f.fill(ctx.session, ctx.profile));
    return { note: "base.fill: standard autofill; override per-site" };
  },
  async submit(ctx) {
    const browser = await import("../browser.mjs");
    const r = await ctx.session.send("Runtime.evaluate", {
      returnByValue: true,
      expression: `(()=>{const b=Array.from(document.querySelectorAll('button,input[type=submit]')).find(b=>/submit/i.test((b.innerText||b.value||'')));if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return{x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)};})()`,
    });
    return r.result?.value;
  },
};
