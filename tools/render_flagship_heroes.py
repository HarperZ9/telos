from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import random
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path


SIZE = (1600, 640)
SCALE = 2
BG = (13, 15, 20)
INK = (248, 249, 246)
MUTED = (174, 181, 188)
GRID = (66, 72, 84)

DEFAULT_CONFIG = Path(__file__).with_name("flagship_brand_config.json")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        head = f.read(24)
    if not head.startswith(b"\x89PNG\r\n\x1a\n") or head[12:16] != b"IHDR":
        raise ValueError(f"{path} is not a PNG with an IHDR header")
    return struct.unpack(">II", head[16:24])


def font_receipt(path: Path, role: str) -> dict:
    receipt = {"role": role, "path": str(path), "exists": path.exists(), "committed": False}
    if path.exists():
        receipt["sha256"] = sha256_file(path)
        receipt["bytes"] = path.stat().st_size
    return receipt


def env_path(name: str, fallback: Path) -> Path:
    value = os.environ.get(name)
    return Path(value) if value else fallback


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf8"))
    for _name, cfg in data.items():
        for key in ("accent", "accent2", "accent3"):
            cfg[key] = tuple(cfg[key])
    return data


def paths(public_root: Path, tool: str) -> tuple[Path, Path]:
    root = public_root / tool
    return root / "docs" / "brand" / f"{tool}-hero.png", root / "docs" / "brand" / "README.md"


def inspect_outputs(public_root: Path, config: dict) -> list[dict]:
    outputs = []
    for name, cfg in config.items():
        image, readme = paths(public_root, name)
        width, height = png_size(image)
        text = readme.read_text(encoding="utf8")
        missing = [
            phrase
            for phrase in ("Typography:", "Accessibility floor:", "Provenance boundary:")
            if phrase not in text
        ]
        if missing:
            raise ValueError(f"{readme} missing brand receipt fields: {', '.join(missing)}")
        outputs.append(
            {
                "tool": name,
                "image": str(image),
                "readme": str(readme),
                "width": width,
                "height": height,
                "sha256": sha256_file(image),
                "motif": cfg["motif"],
            }
        )
    return outputs


def receipt(args: argparse.Namespace, mode: str, outputs: list[dict]) -> dict:
    return {
        "schema": "project-telos.brand-render/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "source_contract": "telos.rendering.research",
        "public_root": str(args.public_root),
        "dimensions": {"width": SIZE[0], "height": SIZE[1]},
        "font_inputs": [
            font_receipt(args.kilon_zip, "display"),
            font_receipt(args.conso_zip, "body-and-mono"),
        ],
        "outputs": outputs,
        "design_gates": [
            "static PNG fallback for GitHub and low-capability hosts",
            "high-contrast foreground text",
            "non-color-only status labels",
            "tool-specific motif with shared flagship presentation grammar",
        ],
        "provenance_boundary": "The repositories carry exported artwork and receipts only; purchased font files remain local operator inputs.",
    }


def font_from_zip(zip_path: Path, member_suffix: str, size: int, ImageFont):
    with zipfile.ZipFile(zip_path) as zf:
        member = next(name for name in zf.namelist() if name.endswith(member_suffix))
        return ImageFont.truetype(io.BytesIO(zf.read(member)), size=size)


def render_all(args: argparse.Namespace, config: dict) -> list[dict]:
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
    except ImportError as exc:
        raise SystemExit("render mode requires Pillow: python -m pip install Pillow") from exc

    font_kilon = font_from_zip(args.kilon_zip, "Fonts/Kilon.ttf", 134 * SCALE, ImageFont)
    font_conso = font_from_zip(args.conso_zip, "Fonts/Conso-Regular.ttf", 29 * SCALE, ImageFont)
    font_bold = font_from_zip(args.conso_zip, "Fonts/Conso-Bold.ttf", 30 * SCALE, ImageFont)
    font_small = font_from_zip(args.conso_zip, "Fonts/Conso-SemiBold.ttf", 19 * SCALE, ImageFont)

    def rgba(color, alpha):
        return (*color, alpha)

    def blend(a, b, t):
        return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))

    def rounded(draw, box, radius, fill, outline=None, width=1):
        draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

    def draw_background(base, cfg):
        draw = ImageDraw.Draw(base, "RGBA")
        accent, accent2, accent3 = cfg["accent"], cfg["accent2"], cfg["accent3"]
        draw.rectangle((0, 0, SIZE[0] * SCALE, SIZE[1] * SCALE), fill=(*BG, 255))
        for y in range(0, SIZE[1] * SCALE, 8):
            t = y / (SIZE[1] * SCALE)
            color = blend(blend(accent, accent2, 0.35), BG, 0.78 + 0.12 * math.sin(t * math.pi))
            draw.line((0, y, SIZE[0] * SCALE, y), fill=(*color, 16), width=8)
        cell = 64 * SCALE
        for row in range(-2, 12):
            for col in range(-2, 15):
                x = 810 * SCALE + col * cell + row * 10 * SCALE
                y = 64 * SCALE + row * 44 * SCALE
                if x < 620 * SCALE or x > SIZE[0] * SCALE + cell:
                    continue
                alpha = 30 if (row + col) % 3 else 58
                draw.polygon(
                    [(x, y), (x + cell * 0.78, y + cell * 0.12), (x + cell * 0.62, y + cell * 0.58), (x - cell * 0.16, y + cell * 0.46)],
                    outline=rgba(GRID, alpha),
                )
        draw.line((0, 570 * SCALE, SIZE[0] * SCALE, 536 * SCALE), fill=rgba(accent, 90), width=2 * SCALE)
        draw.line((0, 578 * SCALE, SIZE[0] * SCALE, 602 * SCALE), fill=rgba(accent2, 70), width=SCALE)
        draw.line((0, 76 * SCALE, SIZE[0] * SCALE, 44 * SCALE), fill=rgba(accent3, 45), width=SCALE)

    def draw_splats(base, cfg):
        rng = random.Random(cfg["seed"])
        layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer, "RGBA")
        colors = [cfg["accent"], cfg["accent2"], cfg["accent3"], (245, 246, 238)]
        cx, cy = 1115 * SCALE, 305 * SCALE
        for i in range(280):
            angle = rng.uniform(-1.0, 1.2) + i * 0.018
            radius = rng.gauss(188, 74) * SCALE
            x = cx + math.cos(angle) * radius * rng.uniform(0.48, 1.34)
            y = cy + math.sin(angle * 1.35) * radius * rng.uniform(0.34, 0.92)
            rx, ry = rng.uniform(2.5, 12.0) * SCALE, rng.uniform(1.2, 8.0) * SCALE
            draw.ellipse((x - rx, y - ry, x + rx, y + ry), fill=rgba(colors[rng.randrange(len(colors))], rng.randrange(18, 82)))
        base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.6 * SCALE)))

    def draw_motif(base, cfg):
        draw = ImageDraw.Draw(base, "RGBA")
        accent, accent2, accent3 = cfg["accent"], cfg["accent2"], cfg["accent3"]
        motif = cfg["motif"]
        if motif == "intake":
            for i in range(7):
                x, y = (958 + i * 58) * SCALE, (190 + (i % 2) * 44) * SCALE
                rounded(draw, (x, y, x + 132 * SCALE, y + 34 * SCALE), 8 * SCALE, rgba((21, 25, 32), 210), rgba(accent, 120), SCALE)
                draw.line((x + 16 * SCALE, y + 17 * SCALE, 1340 * SCALE, 390 * SCALE), fill=rgba(accent2 if i % 2 else accent, 100), width=2 * SCALE)
            rounded(draw, (1268 * SCALE, 348 * SCALE, 1468 * SCALE, 432 * SCALE), 16 * SCALE, rgba((20, 24, 31), 230), rgba(accent2, 160), 2 * SCALE)
            draw.text((1288 * SCALE, 374 * SCALE), "RECEIPT", font=font_bold, fill=rgba(INK, 235))
        elif motif == "verdict":
            for i, label in enumerate(["MATCH", "DRIFT", "UNVERIFIABLE"]):
                y = (214 + i * 74) * SCALE
                color = [accent2, accent, accent3][i]
                rounded(draw, (1060 * SCALE, y, 1435 * SCALE, y + 46 * SCALE), 10 * SCALE, rgba((18, 22, 29), 232), rgba(color, 175), 2 * SCALE)
                draw.text((1092 * SCALE, y + 12 * SCALE), label, font=font_bold, fill=rgba(INK, 230))
        elif motif == "graph":
            rng = random.Random(cfg["seed"])
            nodes = [(960 * SCALE + rng.randrange(0, 510) * SCALE, 142 * SCALE + rng.randrange(0, 330) * SCALE) for _ in range(18)]
            for i, a in enumerate(nodes):
                for j, b in enumerate(nodes):
                    if i < j and (i * 7 + j * 3) % 11 < 3:
                        draw.line((*a, *b), fill=rgba(accent if i % 2 else accent2, 70), width=SCALE)
            for i, (x, y) in enumerate(nodes):
                color = [accent, accent2, accent3][i % 3]
                draw.ellipse((x - 9 * SCALE, y - 9 * SCALE, x + 9 * SCALE, y + 9 * SCALE), fill=rgba(color, 220), outline=rgba(INK, 80), width=SCALE)
        elif motif == "ledger":
            for i in range(6):
                x, y = (1010 + (i % 2) * 54) * SCALE, (156 + i * 58) * SCALE
                color = [accent, accent2, accent3][i % 3]
                rounded(draw, (x, y, x + 382 * SCALE, y + 38 * SCALE), 9 * SCALE, rgba((18, 22, 29), 225), rgba(color, 135), SCALE)
                draw.line((x + 24 * SCALE, y + 19 * SCALE, x + 330 * SCALE, y + 19 * SCALE), fill=rgba(color, 120), width=2 * SCALE)
        else:
            for r in range(5):
                box = (990 * SCALE - r * 42 * SCALE, 308 * SCALE - r * 32 * SCALE, 1340 * SCALE + r * 42 * SCALE, 330 * SCALE + r * 32 * SCALE)
                draw.arc(box, 168, 372, fill=rgba([accent, accent2, accent3][r % 3], 150 - r * 18), width=max(1, (5 - r) * SCALE))
            rounded(draw, (1128 * SCALE, 250 * SCALE, 1332 * SCALE, 382 * SCALE), 20 * SCALE, rgba((18, 22, 29), 225), rgba(accent, 170), 2 * SCALE)

    def draw_text(base, cfg):
        draw = ImageDraw.Draw(base, "RGBA")
        x, y = 104 * SCALE, 126 * SCALE
        draw.text((x, y), cfg["title"], font=font_kilon, fill=(*INK, 255))
        draw.text((x + 4 * SCALE, y + 120 * SCALE), cfg["subtitle"].upper(), font=font_bold, fill=(*cfg["accent"], 245))
        draw.text((x + 4 * SCALE, y + 172 * SCALE), cfg["tagline"], font=font_conso, fill=(*MUTED, 245))
        draw.line((x + 4 * SCALE, y + 226 * SCALE, x + 426 * SCALE, y + 226 * SCALE), fill=(*cfg["accent2"], 160), width=2 * SCALE)
        bx = x + 4 * SCALE
        for badge in cfg["badges"]:
            width = max(92 * SCALE, draw.textlength(badge, font=font_small) + 28 * SCALE)
            rounded(draw, (bx, y + 256 * SCALE, bx + width, y + 292 * SCALE), 18 * SCALE, rgba((22, 27, 35), 235), rgba(cfg["accent"], 130), SCALE)
            draw.text((bx + 14 * SCALE, y + 265 * SCALE), badge, font=font_small, fill=(*INK, 230))
            bx += width + 12 * SCALE
        draw.text((x + 4 * SCALE, 536 * SCALE), "PROJECT TELOS FLAGSHIP  /  CLI + MCP + RECEIPTS", font=font_small, fill=(200, 205, 210, 180))
        rounded(draw, (1030 * SCALE, 508 * SCALE, 1506 * SCALE, 568 * SCALE), 14 * SCALE, rgba((15, 18, 24), 220), rgba(cfg["accent"], 125), SCALE)
        draw.text((1052 * SCALE, 526 * SCALE), "VISIBLE STATE  /  FALLBACK  /  REPLAY", font=font_small, fill=(*INK, 220))

    for name, cfg in config.items():
        base = Image.new("RGBA", (SIZE[0] * SCALE, SIZE[1] * SCALE), (0, 0, 0, 0))
        draw_background(base, cfg)
        draw_splats(base, cfg)
        draw_motif(base, cfg)
        draw_text(base, cfg)
        out, _readme = paths(args.public_root, name)
        out.parent.mkdir(parents=True, exist_ok=True)
        base.resize(SIZE, Image.Resampling.LANCZOS).convert("RGB").save(out, optimize=True)
    return inspect_outputs(args.public_root, config)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render or verify the five Project Telos flagship README hero images.")
    parser.add_argument("--public-root", type=Path, default=Path("C:/dev/public"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--kilon-zip",
        type=Path,
        default=env_path("TELOS_KILON_FONT_ZIP", Path.home() / "Downloads" / "Kilon-Bold-Display-Font.zip"),
    )
    parser.add_argument(
        "--conso-zip",
        type=Path,
        default=env_path("TELOS_CONSO_FONT_ZIP", Path.home() / "Downloads" / "Conso-Font-Family.zip"),
    )
    parser.add_argument("--render", action="store_true", help="render PNGs using local font ZIPs and Pillow")
    parser.add_argument("--check-existing", action="store_true", help="verify existing PNGs and brand receipts without Pillow")
    parser.add_argument("--json", action="store_true", help="emit the receipt JSON to stdout")
    parser.add_argument("--receipt", type=Path, help="optional path to write the receipt JSON")
    args = parser.parse_args()

    if not args.render and not args.check_existing:
        args.check_existing = True
    config = load_config(args.config)
    outputs = render_all(args, config) if args.render else inspect_outputs(args.public_root, config)
    mode = "render" if args.render else "check-existing"
    doc = receipt(args, mode, outputs)
    payload = json.dumps(doc, indent=2)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(payload + "\n", encoding="utf8")
    if args.json:
        print(payload)
    else:
        print(f"{mode}: {len(outputs)} hero images verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
