import { assertPositiveInteger, isPowerOfTwo, stableReceiptHash, validatePixels } from "./creative-kernel-utils.mjs";

export function bayerMatrix(size) {
  if (!isPowerOfTwo(size)) throw new Error("bayer: size_must_be_power_of_two");
  if (size === 1) return [[0]];
  if (size === 2) return [[0, 2], [3, 1]];
  const half = bayerMatrix(size / 2);
  const matrix = Array.from({ length: size }, () => Array.from({ length: size }, () => 0));
  for (let y = 0; y < size / 2; y += 1) {
    for (let x = 0; x < size / 2; x += 1) {
      const value = half[y][x] * 4;
      matrix[y][x] = value;
      matrix[y][x + size / 2] = value + 2;
      matrix[y + size / 2][x] = value + 3;
      matrix[y + size / 2][x + size / 2] = value + 1;
    }
  }
  return matrix;
}

export function orderedDither({ pixels, width, height, matrixSize = 4, levels = 4 }) {
  const values = validatePixels({ pixels, width, height });
  if (!isPowerOfTwo(matrixSize)) throw new Error("dither: matrix_size_must_be_power_of_two");
  assertPositiveInteger(levels, "dither.levels");
  if (levels < 2 || levels > 256) throw new Error("dither: levels_out_of_range");
  const matrix = bayerMatrix(matrixSize);
  const denominator = matrixSize * matrixSize;
  const step = 255 / (levels - 1);
  const output = new Uint8Array(values.length);

  for (let index = 0; index < values.length; index += 1) {
    const x = index % width;
    const y = Math.floor(index / width);
    const threshold = ((matrix[y % matrixSize][x % matrixSize] + 0.5) / denominator) - 0.5;
    const adjusted = Math.max(0, Math.min(255, values[index] + threshold * step));
    output[index] = Math.round(Math.round(adjusted / step) * step);
  }

  const measurement = {
    layer_id: "visual.dither-spectrum-meter",
    width,
    height,
    matrix_size: matrixSize,
    levels,
    unique_levels: new Set(output).size,
    algorithm_candidates: ["ordered-bayer", "blue-noise", "void-and-cluster"],
    measurement_hash: stableReceiptHash({
      kernel: "orderedDither",
      width,
      height,
      matrixSize,
      levels,
      output: Array.from(output)
    })
  };
  return {
    kernel: "raster.ordered-dither",
    width,
    height,
    levels,
    output,
    measurement,
    receipt_hash: stableReceiptHash({ measurement, output: Array.from(output) })
  };
}

export function pixelSortRows({ pixels, width, height, threshold = 128 }) {
  const values = validatePixels({ pixels, width, height });
  const output = Uint8Array.from(values);
  const runs = [];

  for (let row = 0; row < height; row += 1) {
    const offset = row * width;
    let cursor = 0;
    let rowRunCount = 0;
    while (cursor < width) {
      while (cursor < width && output[offset + cursor] < threshold) cursor += 1;
      const start = cursor;
      while (cursor < width && output[offset + cursor] >= threshold) cursor += 1;
      if (cursor - start >= 2) {
        const sorted = Array.from(output.slice(offset + start, offset + cursor)).sort((a, b) => a - b);
        output.set(sorted, offset + start);
        runs.push({ row, start, end: cursor - 1, mode: "threshold-run" });
        rowRunCount += 1;
      }
    }

    if (rowRunCount === 0) {
      const sorted = Array.from(output.slice(offset, offset + width)).sort((a, b) => a - b);
      output.set(sorted, offset);
      runs.push({ row, start: 0, end: width - 1, mode: "row-fallback" });
    }
  }

  const measurement = {
    layer_id: "visual.pixel-sort-meter",
    width,
    height,
    threshold,
    run_count: runs.length,
    measurement_hash: stableReceiptHash({ kernel: "pixelSortRows", width, height, threshold, runs })
  };
  return {
    kernel: "raster.pixel-sort-rows",
    output,
    runs,
    measurement,
    receipt_hash: stableReceiptHash({ measurement, output: Array.from(output) })
  };
}
