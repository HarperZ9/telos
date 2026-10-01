// Contact primitives for the autonomous engine. Email send via the operator's
// authenticated Gmail session (no credentials handled -- the carried session is
// the auth). Uses Gmail's compose URL (view=cm) which prefills to/subject/body,
// then clicks Send. B2B outreach only: personalized, one-per-target, CAN-SPAM
// (real address + unsubscribe already in the body the caller provides).

import * as browser from "./browser.mjs";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Send an email from the operator's Gmail. Body should already include the
// signature/address/unsubscribe line for CAN-SPAM compliance.
export async function gmailSend(session, { to, subject, body }) {
  const params = new URLSearchParams({ view: "cm", fs: "1", to, su: subject, body });
  const url = `https://mail.google.com/mail/?${params.toString()}`;
  await browser.navigate(session, url);
  await sleep(4500); // compose window + prefill
  // Gmail's Send button: find it and click. The compose view=cm opens a popup.
  const click = `(()=>{
    const btns=Array.from(document.querySelectorAll('div[role=button],button,[role=button]'));
    const send=btns.find(b=>/^send$/i.test(((b.innerText||b.getAttribute('aria-label')||'')+'').trim()));
    if(send){send.click();return {sent:true,label:send.getAttribute('aria-label')||send.innerText};}
    return {sent:false,n:btns.length};
  })()`;
  const r = await session.send("Runtime.evaluate", { expression: click, returnByValue: true });
  await sleep(2500);
  // confirm: a "Sending..." / "Sent" toast, or the compose gone
  const confirm = await session.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `(()=>{const t=((document.body&&document.body.innerText)||'').toLowerCase();return {sending:/sending/.test(t),sent:/message sent|your message has been sent|sent/.test(t),stillCompose:/recipients/.test(t)};})()`,
  });
  return { to, subject, send: r.result?.value, confirm: confirm.result?.value };
}
