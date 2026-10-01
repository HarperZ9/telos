// Canonical JSON for digests and signatures: one implementation, owned by the
// receipt verifier (demo/receipts/verify.mjs), so a grant, a hold decision, an
// action digest and a receipt seal can never hash the same value two ways.
// Sorted keys, compact separators, UTF-8, integers only; object keys whose value
// is undefined are dropped.
import { canonical, sha256Hex } from "../receipts/verify.mjs";

export { canonical, sha256Hex };

export function digestOf(value) {
  return sha256Hex(canonical(value));
}
