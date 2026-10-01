const refs = new Map([
  ["attestation", ["in-toto"]],
  ["inventory", ["SBOM", "AIBOM"]],
  ["content-authenticity", ["C2PA"]],
  ["client-observed", ["Project Telos client_observed receipt"]]
]);

export function standardRefsFor(kind) {
  return refs.get(kind) || [];
}
