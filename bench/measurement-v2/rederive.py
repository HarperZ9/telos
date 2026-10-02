"""Re-derive the receipt hashes of telos.measurement.layers v2 responses without any JavaScript.

Uses canonical_receipt.py (a standard-library twin of the canonical-bytes rules,
project-telos.canonical-bytes/v1). For each response it recomputes input_receipt.sha256 over the input
receipt without that field, and receipt_sha256 over the response without that field.

CLI: python rederive.py <responses.json> <out.json>
"""
import json
import sys

from canonical_receipt import receipt_sha256


def rederive(response):
    inp = dict(response["input_receipt"])
    inp.pop("sha256")
    body = dict(response)
    body.pop("receipt_sha256")
    return {"input_sha256": receipt_sha256(inp), "receipt_sha256": receipt_sha256(body)}


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    json.dump([rederive(r) for r in data], open(sys.argv[2], "w", encoding="utf-8"))
