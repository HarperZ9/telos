// Network-domain layer. The architectural unlock for score-based anti-bot:
// harvest the page's OWN reCAPTCHA token via grecaptcha.execute (the page
// generated it for this exact session + action) and submit the application at
// the API layer with fetch() from the page context -- which carries the session
// cookies, the correct Origin, and the page's legitimate token. This sidesteps
// DOM widget filling entirely and reframes "invisible reCAPTCHA" from a wall
// into a token the page hands you. Also exposes request capture for endpoint
// discovery.
//
//   recaptchaToken(session, {action, siteKey}) -> page's own token
//   apiFetch(session, {url, method, body, headers}) -> in-page fetch result
//   capture(session, {durationMs, urlFilter}) -> observed requests in a window

// Pull a fresh reCAPTCHA / Enterprise token the way the page itself does.
// Site key auto-detected from the recaptcha iframe (k=) or [data-sitekey].
export async function recaptchaToken(session, { action = "submit", siteKey } = {}) {
  const detect = `(()=>{
    if(!siteKey){
      const f=document.querySelector('iframe[src*="recaptcha"]');
      if(f){const m=/[?&]k=([^&]+)/.exec(f.src);if(m)siteKey=m[1];}
    }
    if(!siteKey){const d=document.querySelector('[data-sitekey]');if(d)siteKey=d.getAttribute('data-sitekey');}
    return siteKey;
  })()`;
  const r = await session.send("Runtime.evaluate", { expression: detect, returnByValue: true });
  const key = siteKey || r.result?.value;
  if (!key) return { ok: false, note: "no site key detected (set siteKey explicitly)" };
  // Prefer Enterprise (Greenhouse/Workday use recaptcha enterprise); fall back to v3.
  const exec = `
    (async()=>{
      const g=window.grecaptcha;
      if(!g)return {ok:false,note:'grecaptcha not loaded yet'};
      const ready=()=>new Promise(r=>g.ready?g.ready(r):r());
      await ready();
      try{
        if(g.enterprise&&g.enterprise.execute){
          const t=await g.enterprise.execute(${JSON.stringify(key)},{action:${JSON.stringify(action)}});
          return {ok:true,kind:'enterprise',token:t,action:${JSON.stringify(action)}};
        }
        if(g.execute){
          const t=await g.execute(${JSON.stringify(key)},{action:${JSON.stringify(action)}});
          return {ok:true,kind:'v3',token:t,action:${JSON.stringify(action)}};
        }
        return {ok:false,note:'no execute() on grecaptcha'};
      }catch(e){return {ok:false,note:String(e&&e.message||e)};}
    })()`;
  const res = await session.send("Runtime.evaluate", { expression: exec, awaitPromise: true, returnByValue: true });
  return res.result?.value;
}

// POST/GET at the API layer from the page's own context: uses the page's session
// cookies + Origin + any CSRF the page holds. Body is JSON-serializable or a
// string; contentType defaults to application/json.
export async function apiFetch(session, { url, method = "POST", body, headers = {}, contentType = "application/json" }) {
  const expr = `
    (async()=>{
      const opts={method:${JSON.stringify(method)},headers:Object.assign({'Content-Type':${JSON.stringify(contentType)}}, ${JSON.stringify(headers||{})}),credentials:'include'};
      const b=${body == null ? "null" : (typeof body === "string" ? JSON.stringify(body) : JSON.stringify(JSON.stringify(body)))};
      if(b!=null)opts.body=b;
      try{
        const r=await fetch(${JSON.stringify(url)},opts);
        const text=await r.text();
        let json=null;try{json=JSON.parse(text);}catch(e){}
        return {ok:r.ok,status:r.status,text:text.slice(0,1200),json:json};
      }catch(e){return {ok:false,error:String(e&&e.message||e)};}
    })()`;
  const res = await session.send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
  return res.result?.value;
}

// Observe requests in a window for endpoint discovery. Captures method/url/
// postData/headers for requests matching urlFilter (substring). Requires a CDP
// session that stays open for durationMs.
export async function capture(session, { durationMs = 3000, urlFilter = "" } = {}) {
  await session.send("Network.enable");
  const seen = [];
  const onRequest = (p) => {
    const u = p.request.url || "";
    if (urlFilter && !u.includes(urlFilter)) return;
    seen.push({
      requestId: p.requestId,
      method: p.request.method,
      url: u,
      postData: (p.request.postData || "").slice(0, 600),
      headers: p.request.headers,
      type: p.type,
    });
  };
  const onResponse = (p) => {
    const row = seen.find((s) => s.requestId === p.requestId);
    if (row) row.status = p.response?.status;
  };
  session.on("Network.requestWillBeSent", onRequest);
  session.on("Network.responseReceived", onResponse);
  await new Promise((r) => setTimeout(r, durationMs));
  await session.send("Network.disable").catch(() => {});
  return { captured: seen.length, requests: seen };
}
