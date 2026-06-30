import { createHash } from "node:crypto";
import { existsSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultHtml = path.join(here, "index.html");

const budgets = {
  max_html_bytes: 60000,
  max_inline_style_bytes: 20000,
  max_script_tags: 4,
  max_external_font_urls: 2,
  allowed_external_hosts: ["harperz9.github.io"]
};

function sha256(text) {
  return `sha256:${createHash("sha256").update(text).digest("hex")}`;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function relativeLabel(filePath) {
  const relative = path.relative(path.resolve(here, ".."), filePath).replace(/\\/g, "/");
  return relative.startsWith("..") ? path.basename(filePath) : relative;
}

function byteLength(text) {
  return Buffer.byteLength(text, "utf8");
}

function tagAttrs(tag) {
  const attrs = {};
  for (const match of tag.matchAll(/([a-zA-Z:-]+)\s*=\s*["']([^"']*)["']/g)) {
    attrs[match[1].toLowerCase()] = match[2];
  }
  return attrs;
}

function headText(text) {
  return text.match(/<head\b[^>]*>([\s\S]*?)<\/head>/i)?.[1] ?? "";
}

function styleBlocks(text) {
  return [...text.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)].map((match) => match[1]);
}

function tags(text, name) {
  return [...text.matchAll(new RegExp(`<${name}\\b[^>]*>`, "gi"))].map((match) => match[0]);
}

function srcUrls(text) {
  const urls = [];
  for (const match of text.matchAll(/\b(?:src|href|url)\s*(?:=|\()\s*["']?([^"')\s>]+)["']?/gi)) {
    urls.push(match[1]);
  }
  return urls;
}

function externalUrls(text) {
  return srcUrls(text).filter((url) => /^https?:\/\//i.test(url));
}

function hostFor(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return null;
  }
}

function allCanvasHaveDimensions(text) {
  return tags(text, "canvas").every((tag) => /\bwidth\s*=/i.test(tag) && /\bheight\s*=/i.test(tag));
}

function allMediaHaveDimensions(text) {
  const media = [...tags(text, "img"), ...tags(text, "video")];
  return media.every((tag) => {
    const attrs = tagAttrs(tag);
    const hasDimensions = Boolean(attrs.width && attrs.height);
    const lazyImage = !/^<img\b/i.test(tag) || attrs.loading === "lazy";
    return hasDimensions && lazyImage;
  });
}

function allFontFacesUseSwap(text) {
  const blocks = styleBlocks(text).join("\n");
  const fontFaces = [...blocks.matchAll(/@font-face\s*{([\s\S]*?)}/gi)].map((match) => match[1]);
  return fontFaces.length === 0 || fontFaces.every((block) => /font-display\s*:\s*swap/i.test(block));
}

function signalsFor(text) {
  const head = headText(text);
  const styleBytes = styleBlocks(text).reduce((sum, block) => sum + byteLength(block), 0);
  const scriptTags = tags(text, "script");
  const headScripts = tags(head, "script");
  const externalScriptTags = scriptTags.filter((tag) => /\bsrc\s*=\s*["']https?:\/\//i.test(tag));
  const stylesheetTags = tags(text, "link").filter((tag) => /\brel\s*=\s*["']stylesheet["']/i.test(tag));
  const externalStylesheets = stylesheetTags.filter((tag) => /\bhref\s*=\s*["']https?:\/\//i.test(tag));
  const externals = externalUrls(text);
  const externalHosts = unique(externals.map(hostFor));
  const externalFontUrls = externals.filter((url) => /\.(woff2?|ttf|otf)(?:$|[?#])/i.test(url));

  const metrics = {
    html_bytes: byteLength(text),
    inline_style_bytes: styleBytes,
    script_tags: scriptTags.length,
    external_script_tags: externalScriptTags.length,
    external_stylesheets: externalStylesheets.length,
    external_urls: externals.length,
    external_font_urls: externalFontUrls.length,
    external_hosts: externalHosts
  };

  const signals = {
    html_byte_budget: metrics.html_bytes <= budgets.max_html_bytes,
    inline_style_budget: metrics.inline_style_bytes <= budgets.max_inline_style_bytes,
    script_count_budget: metrics.script_tags <= budgets.max_script_tags,
    head_blocking_script_absent: headScripts.every((tag) => /\b(defer|async|type\s*=\s*["']module["'])/i.test(tag)),
    external_scripts_absent: metrics.external_script_tags === 0,
    external_stylesheets_absent: metrics.external_stylesheets === 0,
    external_hosts_allowed: externalHosts.every((host) => budgets.allowed_external_hosts.includes(host)),
    font_display_swap: allFontFacesUseSwap(text),
    external_font_budget: metrics.external_font_urls <= budgets.max_external_font_urls,
    canvas_dimensions: allCanvasHaveDimensions(text),
    media_dimensions: allMediaHaveDimensions(text),
    inline_handlers_absent: !/\son[a-z]+\s*=/i.test(text),
    reduced_motion_media: /prefers-reduced-motion\s*:\s*reduce/i.test(text),
    autoplay_absent: !/<(?:audio|video)\b[^>]*\bautoplay\b/i.test(text)
  };

  return { signals, metrics };
}

function signalFailures(signals) {
  const mapping = {
    html_byte_budget: "html_byte_budget_exceeded",
    inline_style_budget: "inline_style_budget_exceeded",
    script_count_budget: "script_count_budget_exceeded",
    head_blocking_script_absent: "head_blocking_script_present",
    external_scripts_absent: "external_script_present",
    external_stylesheets_absent: "external_stylesheet_present",
    external_hosts_allowed: "external_host_unapproved",
    font_display_swap: "font_display_swap_missing",
    external_font_budget: "external_font_budget_exceeded",
    canvas_dimensions: "canvas_dimensions_missing",
    media_dimensions: "media_dimensions_missing",
    inline_handlers_absent: "inline_event_handler_present",
    reduced_motion_media: "reduced_motion_missing",
    autoplay_absent: "autoplay_media_present"
  };
  return Object.entries(mapping)
    .filter(([key]) => !signals[key])
    .map(([, code]) => code);
}

export function scanPerformanceSurface(htmlPath = defaultHtml, options = {}) {
  const resolved = path.resolve(htmlPath);
  if (!existsSync(resolved) || !statSync(resolved).isFile()) {
    return {
      schema: "project-telos.performance-doctor/v1",
      tool: "telos.performance.doctor",
      generated_at: options.generatedAt ?? new Date().toISOString(),
      surface: {
        kind: "html",
        present: false,
        path_ref: relativeLabel(resolved)
      },
      aggregate: {
        check_count: 14,
        passed_count: 0,
        verdict: "UNVERIFIABLE",
        failure_codes: ["html_surface_unjoinable"]
      },
      privacy_boundary: privacyBoundary(),
      budgets,
      metrics: {},
      signals: {},
      requirements: requirements()
    };
  }

  const text = readFileSync(resolved, "utf8");
  const { signals, metrics } = signalsFor(text);
  const failures = unique(signalFailures(signals));
  return {
    schema: "project-telos.performance-doctor/v1",
    tool: "telos.performance.doctor",
    generated_at: options.generatedAt ?? new Date().toISOString(),
    surface: {
      kind: "html",
      present: true,
      path_ref: relativeLabel(resolved),
      hash: sha256(text)
    },
    aggregate: {
      check_count: Object.keys(signals).length,
      passed_count: Object.values(signals).filter(Boolean).length,
      verdict: failures.length === 0 ? "MATCH" : "DRIFT",
      failure_codes: failures
    },
    privacy_boundary: privacyBoundary(),
    budgets,
    metrics,
    signals,
    requirements: requirements()
  };
}

function privacyBoundary() {
  return {
    raw_html_included: false,
    absolute_paths_included: false,
    external_fetches_performed: false,
    filesystem_writes_performed: false,
    browser_automation_required: false
  };
}

function requirements() {
  return [
    "Studio HTML stays within static byte, style, script, font, and external-host budgets",
    "Head scripts are non-blocking and scripts remain local to the demo surface",
    "Canvas and media elements reserve dimensions to avoid layout shift",
    "Motion, autoplay, inline handlers, and third-party assets stay compatible with host embedding"
  ];
}

export function summary(value = scanPerformanceSurface()) {
  const lines = [
    "Telos Performance Doctor",
    `schema       ${value.schema}`,
    `tool         ${value.tool}`,
    `surface      ${value.surface.path_ref}`,
    `checks       ${value.aggregate.check_count}`,
    `passed       ${value.aggregate.passed_count}`,
    `verdict      ${value.aggregate.verdict}`,
    "next         node demo/performance-doctor.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function optionValue(args, name) {
  const index = args.indexOf(name);
  const inline = args.find((arg) => arg.startsWith(`${name}=`));
  if (inline) {
    return inline.slice(name.length + 1);
  }
  if (index !== -1) {
    return args[index + 1];
  }
  return null;
}

function main() {
  const args = process.argv.slice(2);
  const htmlPath = optionValue(args, "--html") ?? defaultHtml;
  const packet = scanPerformanceSurface(htmlPath);
  if (args.includes("--summary")) {
    process.stdout.write(summary(packet));
  } else {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
