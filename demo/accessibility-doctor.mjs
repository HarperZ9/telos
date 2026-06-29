import { createHash } from "node:crypto";
import { existsSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultHtml = path.join(here, "index.html");

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

function hasLabelForEachInput(text) {
  const inputs = [...text.matchAll(/<input\b[^>]*>/gi)];
  if (inputs.length === 0) {
    return true;
  }
  return inputs.every((match) => {
    const input = match[0];
    if (/\baria-label\s*=|\baria-labelledby\s*=/i.test(input)) {
      return true;
    }
    const id = input.match(/\bid\s*=\s*["']([^"']+)["']/i)?.[1];
    return Boolean(id && new RegExp(`<label\\b[^>]*\\bfor\\s*=\\s*["']${escapeRegExp(id)}["']`, "i").test(text));
  });
}

function hasCanvasFallbackText(text) {
  return [...text.matchAll(/<canvas\b[^>]*>([\s\S]*?)<\/canvas>/gi)]
    .every((match) => match[1].trim().length > 0);
}

function hasCanvasName(text) {
  return [...text.matchAll(/<canvas\b[^>]*>/gi)]
    .every((match) => /\baria-label\s*=|\baria-labelledby\s*=|\btitle\s*=/i.test(match[0]));
}

function allButtonsHaveType(text) {
  return [...text.matchAll(/<button\b[^>]*>/gi)]
    .every((match) => /\btype\s*=/i.test(match[0]));
}

function hasInteractiveState(text) {
  const hasPressed = /\baria-pressed\s*=/i.test(text);
  const hasSelected = /\baria-selected\s*=/i.test(text);
  const hasExpanded = /\baria-expanded\s*=/i.test(text);
  return hasPressed || hasSelected || hasExpanded;
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function signalsFor(text) {
  return {
    html_lang: /<html\b[^>]*\blang\s*=/i.test(text),
    viewport_meta: /<meta\b[^>]*\bname\s*=\s*["']viewport["'][^>]*>/i.test(text),
    skip_link: /href\s*=\s*["']#main["'][^>]*>\s*Skip to content/i.test(text),
    main_landmark: /<main\b/i.test(text),
    navigation_label: /<(header|nav)\b[^>]*\baria-label\s*=/i.test(text),
    focus_visible_style: /:focus-visible/i.test(text),
    reduced_motion_media: /prefers-reduced-motion\s*:\s*reduce/i.test(text),
    responsive_media: /@media\s*\(\s*max-width\s*:/i.test(text),
    canvas_accessible_name: hasCanvasName(text),
    canvas_fallback_text: hasCanvasFallbackText(text),
    button_type: allButtonsHaveType(text),
    interactive_state: hasInteractiveState(text),
    form_controls_labeled: hasLabelForEachInput(text),
    live_region: /\baria-live\s*=/i.test(text)
  };
}

function signalFailures(signals) {
  const mapping = {
    html_lang: "html_lang_missing",
    viewport_meta: "viewport_meta_missing",
    skip_link: "skip_link_missing",
    main_landmark: "main_landmark_missing",
    navigation_label: "navigation_label_missing",
    focus_visible_style: "focus_visible_missing",
    reduced_motion_media: "reduced_motion_missing",
    responsive_media: "responsive_media_missing",
    canvas_accessible_name: "canvas_accessible_name_missing",
    canvas_fallback_text: "canvas_fallback_missing",
    button_type: "button_type_missing",
    interactive_state: "interactive_state_missing",
    form_controls_labeled: "form_label_missing",
    live_region: "live_region_missing"
  };
  return Object.entries(mapping)
    .filter(([key]) => !signals[key])
    .map(([, code]) => code);
}

export function scanAccessibilitySurface(htmlPath = defaultHtml, options = {}) {
  const resolved = path.resolve(htmlPath);
  if (!existsSync(resolved) || !statSync(resolved).isFile()) {
    return {
      schema: "project-telos.accessibility-doctor/v1",
      tool: "telos.accessibility.doctor",
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
      signals: {},
      requirements: requirements()
    };
  }

  const text = readFileSync(resolved, "utf8");
  const signals = signalsFor(text);
  const failures = unique(signalFailures(signals));
  return {
    schema: "project-telos.accessibility-doctor/v1",
    tool: "telos.accessibility.doctor",
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
    "HTML document has language, viewport, title, skip link, main landmark, and labeled navigation",
    "Interactive controls expose keyboard focus, button types, state attributes, form labels, and live-region updates",
    "Motion and layout respect reduced-motion and responsive media queries",
    "Canvas surfaces have accessible names and text fallbacks"
  ];
}

export function summary(value = scanAccessibilitySurface()) {
  const lines = [
    "Telos Accessibility Doctor",
    `schema       ${value.schema}`,
    `tool         ${value.tool}`,
    `surface      ${value.surface.path_ref}`,
    `checks       ${value.aggregate.check_count}`,
    `passed       ${value.aggregate.passed_count}`,
    `verdict      ${value.aggregate.verdict}`,
    "next         node demo/accessibility-doctor.mjs"
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
  const packet = scanAccessibilitySurface(htmlPath);
  if (args.includes("--summary")) {
    process.stdout.write(summary(packet));
  } else {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
