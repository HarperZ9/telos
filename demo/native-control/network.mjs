// Network-domain layer. In-page fetch with the session's own cookies and
// Origin, plus request capture for endpoint discovery.
//
//   apiFetch(session, {url, method, body, headers}) -> in-page fetch result
//   capture(session, {durationMs, urlFilter}) -> observed requests in a window

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
