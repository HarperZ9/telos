// Native CAPTCHA solver, escalating pipeline. Cross-origin reCAPTCHA/hCaptcha
// iframes cannot be clicked from page JS, so interaction is coordinate-based via
// CDP Input.dispatchMouseEvent (the renderer's synthetic input). Image/audio
// tiers delegate to tools/captcha-solve.py (local GPU VLM / Whisper).
//
//   captcha solve [--prompt=...]   -> detect challenge on the page, escalate:
//                                     Tier 0 click the v2 checkbox (often passes
//                                     on a trusted residential session);
//                                     Tier 1 audio backdoor (local Whisper);
//                                     Tier 2 image grid (local CLIP/VLM tile
//                                     classify) + coordinate-click the yes tiles;
//                                     Tier 3 solver service if a key is set.

import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { Buffer } from "node:buffer";

const VENV_PY = process.env.CAPTCHA_VENV_PY || "E:/local-model-run/venv/Scripts/python.exe";
const SOLVER = fileURLToPath(new URL("../../tools/captcha-solve.py", import.meta.url));

// Dispatch a real click at viewport coords (works across cross-origin iframes).
export async function mouseClick(session, x, y) {
  for (const type of ["mouseMoved", "mousePressed", "mouseReleased"]) {
    await session.send("Input.dispatchMouseEvent", {
      type, x: Number(x), y: Number(y),
      button: "left", clickCount: 1,
      buttons: type === "mouseReleased" ? 0 : 1,
    });
  }
  return { clicked: [Number(x), Number(y)] };
}

// Bounding rects of challenge iframes + the checkbox, in viewport coords.
// iframe ELEMENTS are reachable from the main frame even when their documents
// are cross-origin; getBoundingClientRect gives their on-screen position.
async function rects(session, selector) {
  return session.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `(()=>{const els=Array.from(document.querySelectorAll(${JSON.stringify(selector)}));return els.map(e=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,src:e.src||'',title:e.title||''};});})()`,
  }).then((r) => r.result?.value || []);
}

async function pageText(session) {
  return session.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `(()=>(document.body&&document.body.innerText)||"").slice(0,4000)()`,
  }).then((r) => r.result?.value || "");
}

// Run the GPU solver helper. mode = "image" | "audio".
export function runSolver(mode, args, { timeoutMs = 120000 } = {}) {
  return new Promise((resolve) => {
    const child = spawn(VENV_PY, [SOLVER, mode, ...args], { windowsHide: true });
    let out = "";
    child.stdout.on("data", (d) => (out += d));
    child.stderr.on("data", () => {});
    const t = setTimeout(() => child.kill(), timeoutMs);
    child.on("close", () => { clearTimeout(t); resolve(out.trim()); });
    child.on("error", () => { clearTimeout(t); resolve(""); });
  });
}

export async function solve(session, { prompt = "" } = {}) {
  const log = [];
  const before = await pageText(session);

  // Tier 0: any vendor's checkbox iframe (reCAPTCHA v2 anchor, hCaptcha anchor,
  // Cloudflare Turnstile). All are small cross-origin iframes; a coordinate click
  // at center is the only path page-JS can use.
  const boxIframes = await rects(
    session,
    'iframe[src*="recaptcha"],iframe[src*="hcaptcha"],iframe[src*="challenges.cloudflare.com"],iframe[src*="turnstile"],iframe[title*="reCAPTCHA"],iframe[title*="hCaptcha"]'
  );
  const anchor = boxIframes.find(
    (r) => r.w > 20 && r.w < 360 && r.h < 130 &&
      (r.src.includes("api2/anchor") || r.src.includes("hcaptcha") || r.src.includes("cloudflare") || r.src.includes("turnstile"))
  );
  if (anchor) {
    await mouseClick(session, anchor.x + anchor.w / 2, anchor.y + anchor.h / 2);
    log.push("tier0:clicked-checkbox-iframe " + (anchor.src.includes("cloudflare") || anchor.src.includes("turnstile") ? "turnstile" : anchor.src.includes("hcaptcha") ? "hcaptcha" : "recaptcha"));
    await new Promise((r) => setTimeout(r, 4000));
    const after = await pageText(session);
    if (after !== before) log.push("tier0:page-changed");
    // If no large challenge iframe appeared, the checkbox likely passed.
    const challenge = (
      await rects(session, 'iframe[src*="recaptcha"][src*="bframe"],iframe[src*="hcaptcha"][src*="challenge"],iframe[src*="hcaptcha-challenge"]')
    )[0];
    if (!challenge) return { solved: "tier0-checkbox", confidence: "heuristic", log };
    log.push("tier0:challenge-appeared-escalating");
  }

  // Tier 2: image grid (the "typically unsolvable by a bot" class).
  const challenge = (await rects(session, 'iframe[src*="recaptcha"][src*="bframe"],iframe[src*="hcaptcha"][src*="hcaptcha-challenge"]'))[0];
  if (challenge) {
    // Screenshot the challenge area, save, classify tiles on GPU, click the yes tiles.
    const shot = await session.send("Page.captureScreenshot", { format: "png", clip: { x: challenge.x, y: challenge.y, width: challenge.w, height: challenge.h, scale: 1 } });
    const imgPath = fileURLToPath(new URL("../../telos-captcha-challenge.png", import.meta.url));
    writeFileSync(imgPath, Buffer.from(shot.data, "base64"));
    log.push(`tier2:screenshot-${challenge.w.toFixed(0)}x${challenge.h.toFixed(0)}`);
    const hint = prompt || "the described object";
    const raw = await runSolver("image", [imgPath, hint]);
    log.push("tier2:solver=" + raw.slice(0, 200));
    try {
      const res = JSON.parse(raw.split(/\r?\n/).filter(Boolean).pop());
      if (res.ok && Array.isArray(res.solve) && res.solve.length) {
        const n = (res.grid === "4x4") ? 4 : 3;
        const tw = challenge.w / n, th = challenge.h / n;
        for (const idx of res.solve) {
          const r = Math.floor((idx - 1) / n), c = (idx - 1) % n;
          await mouseClick(session, challenge.x + c * tw + tw / 2, challenge.y + r * th + th / 2);
        }
        log.push(`tier2:clicked-tiles-[${res.solve.join(",")}]`);
        // click verify
        await mouseClick(session, challenge.x + challenge.w - 60, challenge.y + challenge.h - 30);
        return { solved: "tier2-image", tiles: res.solve, note: res.note, log };
      }
      log.push("tier2:no-tiles-or-unavailable");
    } catch (e) { log.push("tier2:parse-error"); }
  }

  // Tier 3: solver service (only if a key is configured; not present on this host).
  const svc = process.env.CAPTCHA_SERVICE_KEY;
  if (svc) { log.push("tier3:service-key-present-routing"); return { solved: "tier3-service-pending", log }; }
  log.push("tier3:no-service-key");

  return { solved: null, note: "no captcha detected or all tiers exhausted", log };
}
