(() => {
  const canvas = document.getElementById("effect-canvas");
  const receipt = document.getElementById("effect-receipt");
  if (!canvas || !receipt) return;

  const TelosEffects = {
    version: "project-telos.effects-engine/v1",
    seed: 5505,
    layers: [
      { id: "retro", name: "Retro CGI", family: "cgi", claim: "Wireframes, horizon grids, shaded primitives, and measurement-friendly depth." },
      { id: "glitch", name: "Glitch", family: "corruption", claim: "Scanline offsets, channel splits, and deliberate corruption with readable state." },
      { id: "generative", name: "Generative", family: "procedural", claim: "Seeded particle fields and graph traces for repeatable variation." },
      { id: "plotter", name: "Plotter", family: "vector", claim: "Pen-plotter paths, hatch lines, and vector-like trace discipline." },
      { id: "pixelsort", name: "Pixel sort", family: "raster", claim: "Luminance-ranked row fragments that expose algorithmic image transforms." },
      { id: "poster", name: "Poster", family: "print", claim: "Typographic blocks and print-system composition for flagship presentation." },
      { id: "fractal", name: "Fractal", family: "recursive", claim: "Branching recursion and orbital geometry for sensitivity-map demos." },
      { id: "splat", name: "Gaussian splat", family: "radiance", claim: "Transparent ellipses that stand in for web-native splat fields." },
      { id: "clustered", name: "Clustered lights", family: "lighting", claim: "Forward-style screen clusters showing light bins and overlay visibility." },
      { id: "crt", name: "CRT scanlines", family: "display", claim: "Phosphor scanlines, vignette, and refresh artifacts with reduced-motion fallback." },
      { id: "chromatic", name: "Chromatic split", family: "optics", claim: "Channel-separated offsets for lens and signal stress tests." },
      { id: "dither", name: "Dither", family: "raster", claim: "Ordered threshold texture for low-bit export previews." },
      { id: "contour", name: "Contour map", family: "measurement", claim: "Iso-line fields for scientific overlays and scalar maps." },
      { id: "voronoi", name: "Voronoi cells", family: "partition", claim: "Nearest-seed regions for segmentation and route-field sketches." },
      { id: "ascii", name: "ASCII raster", family: "terminal", claim: "Glyph-based rasterization for TUI and log-friendly previews." },
      { id: "vector", name: "Vector field", family: "flow", claim: "Directional arrows for flow, gradient, and sensitivity overlays." },
      { id: "feedback", name: "Feedback trails", family: "temporal", claim: "Frame-to-frame echo paths for history and action-loop memory." }
    ]
  };
  window.TelosEffects = TelosEffects;

  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const buttons = [...document.querySelectorAll("[data-effect]")];
  const intensityInput = document.getElementById("effect-intensity");
  const densityInput = document.getElementById("effect-density");
  const freezeButton = document.getElementById("effect-freeze");
  const stepButton = document.getElementById("effect-step");
  const rerollButton = document.getElementById("effect-reroll");
  const labels = Object.fromEntries(TelosEffects.layers.map((layer) => [layer.id, layer.name]));
  labels.all = "All layers";

  let mode = "all";
  let lastFrame = 0;
  let frame = 0;
  let seed = TelosEffects.seed;
  let frozen = false;
  let intensity = Number(intensityInput?.value ?? 82) / 100;
  let density = Number(densityInput?.value ?? 64) / 100;

  function makeRng(value) {
    let state = value >>> 0;
    return () => {
      state = (state * 1664525 + 1013904223) >>> 0;
      return state / 4294967296;
    };
  }

  function clear() {
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, "#07080b");
    gradient.addColorStop(0.55, "#111525");
    gradient.addColorStop(1, "#050608");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  function line(x1, y1, x2, y2, color, width = 1) {
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  function drawArrow(x, y, angle, length, color) {
    const x2 = x + Math.cos(angle) * length;
    const y2 = y + Math.sin(angle) * length;
    line(x, y, x2, y2, color, 1.2);
    line(x2, y2, x2 - Math.cos(angle - 0.52) * 7, y2 - Math.sin(angle - 0.52) * 7, color, 1.2);
    line(x2, y2, x2 - Math.cos(angle + 0.52) * 7, y2 - Math.sin(angle + 0.52) * 7, color, 1.2);
  }

  function drawRetroCgi(time) {
    const horizon = 324;
    for (let i = 0; i < 18; i++) {
      const y = horizon + i * i * 1.55;
      line(0, y, canvas.width, y, `rgba(70,224,178,${0.18 * intensity})`);
    }
    for (let i = -16; i <= 16; i++) {
      line(canvas.width / 2, horizon, canvas.width / 2 + i * 58, canvas.height, `rgba(82,103,255,${0.22 * intensity})`);
    }
    const cx = 250 + Math.sin(time * 0.001) * 28 * intensity;
    const cy = 180;
    ctx.strokeStyle = "rgba(248,249,246,.72)";
    ctx.lineWidth = 2;
    for (let i = 0; i < 5; i++) ctx.strokeRect(cx + i * 12, cy + i * 10, 160 - i * 18, 116 - i * 12);
    const sphere = ctx.createRadialGradient(720, 150, 8, 720, 150, 108);
    sphere.addColorStop(0, "rgba(255,255,255,.96)");
    sphere.addColorStop(0.45, "rgba(255,96,160,.78)");
    sphere.addColorStop(1, "rgba(82,103,255,.08)");
    ctx.fillStyle = sphere;
    ctx.beginPath();
    ctx.arc(720, 150, 98, 0, Math.PI * 2);
    ctx.fill();
  }

  function drawGenerative(time) {
    const rng = makeRng(seed + Math.floor(time / 300));
    const count = Math.round(24 + density * 42);
    const points = [];
    for (let i = 0; i < count; i++) points.push([80 + rng() * 800, 54 + rng() * 410]);
    for (let i = 0; i < points.length; i++) {
      for (let j = i + 1; j < points.length; j++) {
        const dx = points[i][0] - points[j][0];
        const dy = points[i][1] - points[j][1];
        const d = Math.hypot(dx, dy);
        if (d < 84 + density * 54) line(points[i][0], points[i][1], points[j][0], points[j][1], "rgba(255,194,92,.16)");
      }
    }
    for (const [x, y] of points) {
      ctx.fillStyle = "rgba(70,224,178,.65)";
      ctx.fillRect(x - 2, y - 2, 4, 4);
    }
  }

  function drawPlotter(time) {
    ctx.strokeStyle = "rgba(248,249,246,.72)";
    ctx.lineWidth = 1.15;
    ctx.beginPath();
    for (let i = 0; i < 720; i++) {
      const t = i / 720 * Math.PI * 2;
      const r = 92 + 48 * Math.sin(5 * t + time * 0.001);
      const x = 500 + Math.cos(t * 3) * r + Math.cos(t) * 82;
      const y = 272 + Math.sin(t * 2) * r * 0.72;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    for (let y = 398; y < 520; y += Math.max(5, 12 - density * 8)) line(70, y, 890, y + Math.sin(y * 0.05) * 18, "rgba(255,194,92,.28)");
  }

  function drawFractal(x, y, length, angle, depth) {
    if (depth <= 0) return;
    const x2 = x + Math.cos(angle) * length;
    const y2 = y + Math.sin(angle) * length;
    line(x, y, x2, y2, `rgba(70,224,178,${0.16 + depth * 0.07})`, Math.max(1, depth * 0.55));
    drawFractal(x2, y2, length * 0.72, angle - 0.48, depth - 1);
    drawFractal(x2, y2, length * 0.67, angle + 0.42, depth - 1);
  }

  function drawSplat() {
    const rng = makeRng(seed + 88);
    const count = Math.round(88 + density * 170);
    for (let i = 0; i < count; i++) {
      const x = 600 + (rng() - 0.5) * 560;
      const y = 260 + (rng() - 0.5) * 320;
      const rx = 4 + rng() * 22;
      const ry = 2 + rng() * 16;
      ctx.fillStyle = [`rgba(82,103,255,.20)`, `rgba(70,224,178,.22)`, `rgba(255,96,160,.18)`, `rgba(255,194,92,.16)`][i % 4];
      ctx.beginPath();
      ctx.ellipse(x, y, rx, ry, rng() * Math.PI, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function drawClustered() {
    const cols = 12;
    const rows = 7;
    const w = canvas.width / cols;
    const h = canvas.height / rows;
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        const active = (x * 7 + y * 5 + seed) % 9;
        ctx.fillStyle = active < 3 ? `rgba(82,103,255,${0.12 * intensity})` : "rgba(248,249,246,.025)";
        ctx.fillRect(x * w, y * h, w - 1, h - 1);
        if (active === 0) {
          ctx.fillStyle = "rgba(255,194,92,.76)";
          ctx.beginPath();
          ctx.arc(x * w + w * 0.58, y * h + h * 0.42, 4, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }
  }

  function drawPoster() {
    ctx.fillStyle = "rgba(248,249,246,.90)";
    ctx.font = "700 78px Arial Black, sans-serif";
    ctx.fillText("TELOS", 54, 118);
    ctx.font = "700 28px ui-monospace, Consolas, monospace";
    ctx.fillStyle = "rgba(255,194,92,.90)";
    ctx.fillText("MATCH / DRIFT / UNVERIFIABLE", 58, 158);
    ctx.fillStyle = "rgba(70,224,178,.82)";
    ctx.fillRect(58, 178, 250, 12);
    ctx.fillStyle = "rgba(255,96,160,.68)";
    ctx.fillRect(58, 198, 372, 12);
  }

  function drawCrt() {
    ctx.fillStyle = `rgba(0,0,0,${0.12 * intensity})`;
    for (let y = 0; y < canvas.height; y += 4) ctx.fillRect(0, y, canvas.width, 1);
    const glow = ctx.createRadialGradient(canvas.width / 2, canvas.height / 2, 120, canvas.width / 2, canvas.height / 2, 560);
    glow.addColorStop(0, "rgba(255,255,255,0)");
    glow.addColorStop(1, "rgba(0,0,0,.52)");
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  function drawDither() {
    const matrix = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
    const step = 8;
    for (let y = 0; y < canvas.height; y += step) {
      for (let x = 0; x < canvas.width; x += step) {
        const threshold = matrix[((y / step) % 4) * 4 + ((x / step) % 4)] / 16;
        if (threshold < density * 0.55) {
          ctx.fillStyle = `rgba(248,249,246,${0.04 + threshold * 0.08})`;
          ctx.fillRect(x, y, 2, 2);
        }
      }
    }
  }

  function drawContour(time) {
    ctx.strokeStyle = "rgba(70,224,178,.30)";
    ctx.lineWidth = 1;
    for (let r = 26; r < 250; r += 18) {
      ctx.beginPath();
      for (let a = 0; a <= Math.PI * 2 + 0.08; a += 0.08) {
        const wave = Math.sin(a * 5 + time * 0.001) * 10 + Math.cos(a * 3) * 7;
        const x = 700 + Math.cos(a) * (r + wave);
        const y = 308 + Math.sin(a) * (r * 0.54 + wave);
        if (a === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
  }

  function drawVoronoi() {
    const rng = makeRng(seed + 211);
    const sites = Array.from({ length: 13 }, () => [rng() * canvas.width, rng() * canvas.height, rng()]);
    const cell = 26;
    for (let y = 0; y < canvas.height; y += cell) {
      for (let x = 0; x < canvas.width; x += cell) {
        let best = sites[0];
        let bd = Infinity;
        for (const site of sites) {
          const d = (x - site[0]) ** 2 + (y - site[1]) ** 2;
          if (d < bd) { bd = d; best = site; }
        }
        ctx.fillStyle = `rgba(${80 + best[2] * 120},${115 + best[2] * 90},255,${0.035 * intensity})`;
        ctx.fillRect(x, y, cell - 1, cell - 1);
      }
    }
    for (const [x, y] of sites) {
      ctx.fillStyle = "rgba(255,194,92,.85)";
      ctx.fillRect(x - 2, y - 2, 4, 4);
    }
  }

  function drawAscii() {
    const glyphs = ".:+*#@";
    ctx.font = "10px ui-monospace, Consolas, monospace";
    for (let y = 22; y < canvas.height; y += 22) {
      for (let x = 24; x < canvas.width; x += 24) {
        const n = Math.abs(Math.sin(x * 0.024 + y * 0.031 + seed));
        if (n > 1 - density * 0.65) {
          ctx.fillStyle = "rgba(248,249,246,.22)";
          ctx.fillText(glyphs[Math.floor(n * glyphs.length) % glyphs.length], x, y);
        }
      }
    }
  }

  function drawVectorField(time) {
    for (let y = 54; y < canvas.height - 20; y += 42) {
      for (let x = 44; x < canvas.width - 20; x += 54) {
        const angle = Math.sin(x * 0.012 + time * 0.0007) + Math.cos(y * 0.018);
        drawArrow(x, y, angle, 13 + density * 12, "rgba(70,224,178,.36)");
      }
    }
  }

  function drawFeedback(time) {
    const cx = canvas.width * 0.5;
    const cy = canvas.height * 0.5;
    for (let i = 0; i < 18; i++) {
      const t = time * 0.001 + i * 0.44;
      const x = cx + Math.cos(t * 1.7) * (80 + i * 14);
      const y = cy + Math.sin(t * 1.3) * (40 + i * 8);
      ctx.strokeStyle = `rgba(255,96,160,${0.18 - i * 0.007})`;
      ctx.strokeRect(x - 18 - i, y - 12 - i * 0.6, 36 + i * 2, 24 + i * 1.2);
    }
  }

  function applyGlitch(time) {
    const slices = 12;
    for (let i = 0; i < slices; i++) {
      const y = Math.floor((i / slices) * canvas.height);
      const h = 8 + (i % 4) * 3;
      const dx = Math.round(Math.sin(time * 0.006 + i) * 12 * intensity);
      ctx.drawImage(canvas, 0, y, canvas.width, h, dx, y, canvas.width, h);
    }
    ctx.globalCompositeOperation = "screen";
    ctx.fillStyle = "rgba(255,96,160,.08)";
    ctx.fillRect(6, 0, canvas.width, canvas.height);
    ctx.globalCompositeOperation = "source-over";
  }

  function applyChromaticSplit(time) {
    const dx = Math.round(Math.sin(time * 0.002) * 5 * intensity + 5);
    ctx.globalCompositeOperation = "screen";
    ctx.fillStyle = "rgba(255,0,96,.08)";
    ctx.fillRect(dx, 0, canvas.width, canvas.height);
    ctx.fillStyle = "rgba(0,220,255,.07)";
    ctx.fillRect(-dx, 0, canvas.width, canvas.height);
    ctx.globalCompositeOperation = "source-over";
  }

  function applyPixelSort() {
    const image = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = image.data;
    for (let y = 24; y < canvas.height; y += Math.max(7, Math.round(14 - density * 8))) {
      const row = [];
      for (let x = 0; x < canvas.width; x += 3) {
        const i = (y * canvas.width + x) * 4;
        row.push([data[i] + data[i + 1] + data[i + 2], data[i], data[i + 1], data[i + 2], data[i + 3]]);
      }
      row.sort((a, b) => a[0] - b[0]);
      for (let x = 0; x < row.length; x++) {
        const i = (y * canvas.width + x * 3) * 4;
        const px = row[x];
        data[i] = px[1]; data[i + 1] = px[2]; data[i + 2] = px[3]; data[i + 3] = px[4];
      }
    }
    ctx.putImageData(image, 0, 0);
  }

  function activeLayers() {
    return mode === "all" ? TelosEffects.layers.map((layer) => layer.id) : [mode];
  }

  function render(time = 0) {
    clear();
    const layers = activeLayers();
    if (layers.includes("clustered")) drawClustered();
    if (layers.includes("voronoi")) drawVoronoi();
    if (layers.includes("splat")) drawSplat();
    if (layers.includes("retro")) drawRetroCgi(time);
    if (layers.includes("generative")) drawGenerative(time);
    if (layers.includes("contour")) drawContour(time);
    if (layers.includes("vector")) drawVectorField(time);
    if (layers.includes("feedback")) drawFeedback(time);
    if (layers.includes("plotter")) drawPlotter(time);
    if (layers.includes("fractal")) drawFractal(820, 510, 72, -Math.PI / 2, 8);
    if (layers.includes("poster")) drawPoster();
    if (layers.includes("ascii")) drawAscii();
    if (layers.includes("dither")) drawDither();
    if (layers.includes("pixelsort")) applyPixelSort();
    if (layers.includes("chromatic")) applyChromaticSplit(time);
    if (layers.includes("glitch")) applyGlitch(time);
    if (layers.includes("crt")) drawCrt();
    receipt.value = `Scene receipt: mode=${labels[mode]}; seed=${seed}; layers=${layers.map((layer) => labels[layer]).join(" + ")}; intensity=${Math.round(intensity * 100)}; density=${Math.round(density * 100)}; frame=${frame}; status=MATCH; fallback=canvas+text; reduced_motion=${reducedMotion.matches}`;
  }

  function tick(time) {
    if (!frozen && !reducedMotion.matches && time - lastFrame > 80) {
      frame += 1;
      render(time);
      lastFrame = time;
    }
    requestAnimationFrame(tick);
  }

  function setMode(nextMode) {
    mode = nextMode;
    for (const item of buttons) item.setAttribute("aria-pressed", String(item.dataset.effect === nextMode));
    render(performance.now());
  }

  for (const button of buttons) button.addEventListener("click", () => setMode(button.dataset.effect));
  intensityInput?.addEventListener("input", () => { intensity = Number(intensityInput.value) / 100; render(performance.now()); });
  densityInput?.addEventListener("input", () => { density = Number(densityInput.value) / 100; render(performance.now()); });
  freezeButton?.addEventListener("click", () => {
    frozen = !frozen;
    freezeButton.setAttribute("aria-pressed", String(frozen));
    freezeButton.textContent = frozen ? "Resume" : "Freeze";
    render(performance.now());
  });
  stepButton?.addEventListener("click", () => { frame += 1; render(frame * 120); });
  rerollButton?.addEventListener("click", () => { seed += 97; frame = 0; render(performance.now()); });
  reducedMotion.addEventListener("change", () => render(performance.now()));

  render(0);
  requestAnimationFrame(tick);
})();