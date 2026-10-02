"""Float64 OKLab of sRGB byte colours, the reference for check (a) of the v2 measurement contract.

The two functions are the srgb_to_linear and linear_to_oklab rules of the resolution experiments'
colour.py (Ottosson 2020 matrices, numpy float64, np.cbrt), copied so this check runs inside the repo.

CLI: python float_oklab.py <colours.json>   colours.json = [[r, g, b], ...]; prints [[L, a, b], ...]
"""
import json
import sys

import numpy as np

M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
               [0.2119034982, 0.6806995451, 0.1073969566],
               [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
               [1.9779984951, -2.4285922050, 0.4505937099],
               [0.0259040371, 0.7827717662, -0.8086757660]])


def srgb_to_linear(u8):
    c = np.asarray(u8, dtype=np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_oklab(lin):
    return np.cbrt(lin @ M1.T) @ M2.T


if __name__ == "__main__":
    cols = np.array(json.load(open(sys.argv[1])), dtype=np.float64)
    print(json.dumps(linear_to_oklab(srgb_to_linear(cols)).tolist()))
