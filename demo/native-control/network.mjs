// Network-domain layer. In-page fetch with the session's own cookies and
// Origin, plus request capture for endpoint discovery.
//
//   apiFetch(session, {url, method, body, headers}) -> in-page fetch result
//   capture(session, {durationMs, urlFilter}) -> observed requests in a window,
//     with credential headers and request bodies redacted

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

// Header names whose values carry credentials or session state. Capture keeps
// the name and replaces the value, so endpoint discovery never copies a token,
// cookie or key into a receipt, ledger or model context.
const SECRET_HEADER = /^(authorization|proxy-authorization|cookie|set-cookie)$|token|secret|session|api-?key|auth(?!ority)|csrf|xsrf|signature|credential|password/i;

export function redactHeaders(headers = {}) {
  const out = {};
  for (const [name, value] of Object.entries(headers || {})) {
    out[name] = SECRET_HEADER.test(name) ? "[redacted]" : value;
  }
  return out;
}

// Request bodies can hold passwords, tokens and personal data, so capture
// records only their size, never their content.
export function describeBody(postData) {
  const text = postData == null ? "" : String(postData);
  return { bytes: Buffer.byteLength(text, "utf8"), content: text ? "[redacted]" : null };
}

// Observe requests in a window for endpoint discovery. Captures method, URL,
// status, redacted headers and body size for requests matching urlFilter
// (substring). Requires a CDP session that stays open for durationMs.
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
      body: describeBody(p.request.postData),
      headers: redactHeaders(p.request.headers),
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
  return { captured: seen.length, redacted: true, requests: seen };
}
