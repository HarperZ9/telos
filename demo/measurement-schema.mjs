// measurement-schema.mjs: the MCP input schema of telos.measurement.layers v2.
// telos.measurement.layers v2 request (project-telos.measurement-request/v2); every field is optional,
// and no arguments returns the v1 demo packet.
const b64 = { type: "string", contentEncoding: "base64" };
export const measurementInputSchema = {
  type: "object",
  properties: {
    image: {
      type: "object",
      description: "Raw 8-bit RGBA: rgba (base64) or path (a file under TELOS_MEASUREMENT_ROOTS), with width and height.",
      properties: { rgba: b64, path: { type: "string" }, width: { type: "integer", minimum: 1 }, height: { type: "integer", minimum: 1 } },
      required: ["width", "height"],
      additionalProperties: false
    },
    declared: {
      type: "object",
      properties: {
        colour_space: { enum: ["srgb", "display-p3", "rec2020", "unknown"] },
        alpha: { enum: ["none", "straight", "premultiplied"] },
        bit_depth: { const: 8 }
      },
      additionalProperties: false
    },
    layers: { type: "array", items: { enum: ["L0", "L1", "L2", "L3"] } },
    n: { type: "integer", minimum: 1, maximum: 64 },
    roi: {
      type: "object",
      properties: { x: { type: "integer" }, y: { type: "integer" }, w: { type: "integer" }, h: { type: "integer" } },
      required: ["x", "y", "w", "h"],
      additionalProperties: false
    },
    resample: {
      type: "object",
      properties: { long_edge: { type: "integer", minimum: 1, maximum: 4096 }, filter: { const: "area-linear" } },
      required: ["long_edge", "filter"],
      additionalProperties: false
    },
    overlays: {
      type: "array",
      items: { type: "object", properties: { id: { type: "string" }, mask: b64 }, required: ["id", "mask"], additionalProperties: false }
    },
    overlays_drawn: { type: "boolean" },
    run_id: { type: "string" },
    frame_id: { type: "string" }
  },
  additionalProperties: false
};
