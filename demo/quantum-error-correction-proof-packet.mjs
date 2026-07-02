import { writeFileSync } from "node:fs";

const code = {
  name: "three_qubit_bit_flip_repetition_code",
  logical_zero: [0, 0, 0],
  logical_one: [1, 1, 1],
  stabilizers: ["Z0Z1", "Z1Z2"],
  syndrome_bits: ["q0_xor_q1", "q1_xor_q2"],
  correction_map: {
    "0,0": null,
    "1,0": 0,
    "1,1": 1,
    "0,1": 2
  },
  supported_error_model: "single Pauli-X bit flip on at most one physical qubit",
  unsupported_error_models: [
    "phase errors",
    "arbitrary rotations",
    "amplitude damping",
    "measurement noise",
    "surface-code decoding",
    "hardware threshold claims"
  ]
};

function encode(logical) {
  if (logical === 0) return [...code.logical_zero];
  if (logical === 1) return [...code.logical_one];
  throw new Error(`invalid logical bit: ${logical}`);
}

function xor(a, b) {
  return Number(a !== b);
}

function syndrome(bits) {
  return [xor(bits[0], bits[1]), xor(bits[1], bits[2])];
}

function flip(bits, index) {
  const output = [...bits];
  output[index] = output[index] === 0 ? 1 : 0;
  return output;
}

function applyError(bits, error) {
  if (error === "none") return [...bits];
  if (/^X[0-2]$/.test(error)) return flip(bits, Number(error.slice(1)));
  return [...bits];
}

function correctionFor(syndromeBits, correctionMap = code.correction_map) {
  return correctionMap[syndromeBits.join(",")];
}

function correct(bits, correctionIndex) {
  if (correctionIndex === null || correctionIndex === undefined) return [...bits];
  return flip(bits, correctionIndex);
}

function decode(bits) {
  if (bits.every((bit) => bit === 0)) return 0;
  if (bits.every((bit) => bit === 1)) return 1;
  return null;
}

function hammingWeight(bits) {
  return bits.reduce((sum, bit) => sum + bit, 0);
}

function evaluate(logical, error, correctionMap = code.correction_map) {
  const encoded = encode(logical);
  const after_error = applyError(encoded, error);
  const measured_syndrome = syndrome(after_error);
  const correction_index = correctionFor(measured_syndrome, correctionMap);
  const after_correction = correct(after_error, correction_index);
  const decoded = decode(after_correction);
  return {
    logical,
    error,
    encoded,
    after_error,
    syndrome: measured_syndrome,
    correction_index,
    after_correction,
    decoded,
    logical_match: decoded === logical
  };
}

function singleErrorTable() {
  const rows = [];
  for (const logical of [0, 1]) {
    for (const error of ["none", "X0", "X1", "X2"]) rows.push(evaluate(logical, error));
  }
  return rows;
}

function invalidCodeword(bits) {
  return decode(bits) === null && bits.length === 3 && bits.every((bit) => bit === 0 || bit === 1);
}

function negativeControls() {
  const doubleError = (() => {
    const logical = 0;
    const encoded = encode(logical);
    const after_error = flip(flip(encoded, 0), 1);
    const measured_syndrome = syndrome(after_error);
    const correction_index = correctionFor(measured_syndrome);
    const after_correction = correct(after_error, correction_index);
    return {
      id: "double_bit_flip_aliases_to_logical_error",
      verdict: decode(after_correction) === logical ? "MATCH" : "DRIFT",
      logical,
      after_error,
      syndrome: measured_syndrome,
      correction_index,
      after_correction,
      decoded: decode(after_correction),
      failed_reason: "two X errors are outside the fixture code distance"
    };
  })();

  const phaseError = {
    id: "phase_error_out_of_scope",
    verdict: "UNVERIFIABLE",
    requested_error: "Z1",
    measured_syndrome: syndrome(encode(0)),
    failed_reason: "the bit-flip repetition fixture does not measure phase syndromes"
  };

  const wrongMap = (() => {
    const badMap = { ...code.correction_map, "1,1": 2 };
    const row = evaluate(0, "X1", badMap);
    return {
      id: "wrong_syndrome_map_for_middle_qubit",
      verdict: row.logical_match ? "MATCH" : "DRIFT",
      expected_correction_index: 1,
      observed_correction_index: row.correction_index,
      after_correction: row.after_correction,
      decoded: row.decoded,
      failed_reason: "syndrome [1,1] must correct the middle physical qubit"
    };
  })();

  const missingStabilizer = {
    id: "missing_stabilizer_measurement",
    verdict: "UNVERIFIABLE",
    available_syndrome_bits: ["q0_xor_q1"],
    failed_reason: "one stabilizer bit cannot identify all three single-qubit X errors"
  };

  const nonCodeword = {
    id: "non_codeword_input",
    verdict: invalidCodeword([1, 0, 1]) ? "DRIFT" : "MATCH",
    input_bits: [1, 0, 1],
    hamming_weight: hammingWeight([1, 0, 1]),
    failed_reason: "fixture accepts only encoded logical 000 or 111 before an allowed error"
  };

  return [doubleError, phaseError, wrongMap, missingStabilizer, nonCodeword];
}

function buildPacket() {
  const table = singleErrorTable();
  const negatives = negativeControls();
  const allSingleErrorsCorrect = table.every((row) => row.logical_match);
  const negativesRejected = negatives.every((control) => control.verdict !== "MATCH");
  const result = allSingleErrorsCorrect && negativesRejected
    ? "QEC_STABILIZER_FIXTURE_MATCH"
    : "QEC_STABILIZER_FIXTURE_DRIFT";

  return {
    schema: "project-telos.quantum-error-correction/proof-packet-fixture/v1",
    generated_at: "2026-07-02T00:00:00.000Z",
    result,
    code,
    checks: {
      single_error_rows: table,
      unique_syndromes: [...new Set(table.map((row) => row.syndrome.join(",")))].length === 4,
      all_single_x_errors_correct: allSingleErrorsCorrect,
      negative_controls: negatives
    },
    claim_card: {
      claim: "In the deterministic 3-qubit bit-flip code fixture, the declared stabilizer syndrome table corrects no-error and single Pauli-X errors for both logical basis states, while double-X, phase-error, missing-syndrome, wrong-map, and non-codeword controls are rejected or marked unverifiable.",
      verdict: result === "QEC_STABILIZER_FIXTURE_MATCH" ? "MATCH" : "DRIFT",
      scope: "One local stabilizer-code fixture only; not a surface-code decoder, hardware threshold, quantum advantage, cryptographic, or fault-tolerant computation claim.",
      falsification: "Any single X error fails to recover the encoded logical bit, syndromes are not unique, or any configured negative control is accepted as MATCH."
    },
    toolchain_implications: [
      "Gather owns QEC, syndrome decoder, quantum compiler, hardware, and resource-estimation source receipts.",
      "Index should package circuit specs, syndrome tables, code distance, logical operators, decoder configs, and source refs.",
      "Forum should route quantum claims through physics, formal methods, compiler, hardware, and verification lanes.",
      "BuildLang/buildc should become the typed runtime for Pauli operators, stabilizers, circuits, syndromes, and resource estimates.",
      "Crucible should reject quantum claims without supported error model, code distance, syndrome table, decoder verdicts, and negative controls.",
      "Learn should turn fixtures into exercises about stabilizers, syndromes, logical errors, unsupported error models, and overclaim boundaries."
    ],
    non_claims: [
      "This fixture does not implement a surface-code decoder.",
      "This fixture does not prove hardware-level quantum error correction.",
      "This fixture does not establish fault-tolerant quantum computing.",
      "This fixture does not validate quantum advantage or resource estimates.",
      "This fixture is not yet a BuildLang/buildc-native receipt."
    ]
  };
}

function argValue(args, name) {
  const inline = args.find((arg) => arg.startsWith(`${name}=`));
  if (inline) return inline.slice(name.length + 1);
  const index = args.indexOf(name);
  return index === -1 ? null : args[index + 1] ?? null;
}

const packet = buildPacket();
const args = process.argv.slice(2);
const outPath = argValue(args, "--out");
if (outPath) writeFileSync(outPath, `${JSON.stringify(packet, null, 2)}\n`);

if (args.includes("--summary")) {
  process.stdout.write([
    "Project Telos Quantum Error-Correction Proof Packet",
    `result      ${packet.result}`,
    `single_x    ${packet.checks.single_error_rows.length}`,
    `unique      ${packet.checks.unique_syndromes}`,
    `negative    ${packet.checks.negative_controls.length}`,
    `verdict     ${packet.claim_card.verdict}`
  ].join("\n") + "\n");
} else {
  process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
}
