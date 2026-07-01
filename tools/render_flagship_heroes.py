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


SIZE = (2400, 1260)
SCALE = 2
BG = (13, 15, 20)
INK = (248, 249, 246)
MUTED = (198, 205, 210)
DEFAULT_CONFIG = Path(__file__).with_name("flagship_brand_config.json")
BAYER_4 = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))


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
        receipt.update({"sha256": sha256_file(path), "bytes": path.stat().st_size})
    return receipt


def env_path(name: str, fallback: Path) -> Path:
    return Path(os.environ[name]) if os.environ.get(name) else fallback


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf8"))
    for cfg in data.values():
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
        missing = [phrase for phrase in ("Typography:", "Accessibility floor:", "Provenance boundary:") if phrase not in text]
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
        "schema": "project-telos.brand-render/v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "source_contract": "telos.rendering.research",
        "public_root": str(args.public_root),
        "dimensions": {"width": SIZE[0], "height": SIZE[1]},
        "font_inputs": [font_receipt(args.kilon_zip, "display"), font_receipt(args.conso_zip, "body-and-mono")],
        "outputs": outputs,
        "design_gates": [
            "three-second headline and product-role read",
            "solid text field with no high-frequency texture under copy",
            "contained engine viewport for procedural rendering material",
            "static PNG fallback for GitHub and low-capability hosts",
            "non-color-only status labels",
        ],
        "provenance_boundary": "Repositories carry exported artwork and receipts only; purchased font files remain local operator inputs.",
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

    fonts = {
        "display": font_from_zip(args.kilon_zip, "Fonts/Kilon.ttf", 116 * SCALE, ImageFont),
        "display_sm": font_from_zip(args.kilon_zip, "Fonts/Kilon.ttf", 44 * SCALE, ImageFont),
        "mono": font_from_zip(args.conso_zip, "Fonts/Conso-Regular.ttf", 28 * SCALE, ImageFont),
        "bold": font_from_zip(args.conso_zip, "Fonts/Conso-Bold.ttf", 27 * SCALE, ImageFont),
        "small": font_from_zip(args.conso_zip, "Fonts/Conso-SemiBold.ttf", 18 * SCALE, ImageFont),
    }

    def rgba(color, alpha):
        return (*color, alpha)

    def blend(a, b, t):
        return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))

    def text_y(draw, text, font, y, height):
        box = draw.textbbox((0, 0), text, font=font)
        return y + (height - (box[3] - box[1])) // 2 - box[1]

    def background(size, cfg, alpha=255):
        image = Image.new("RGBA", size, (*BG, alpha))
        px = image.load()
        accent, accent2, accent3 = cfg["accent"], cfg["accent2"], cfg["accent3"]
        for y in range(size[1]):
            v = y / max(1, size[1] - 1)
            for x in range(size[0]):
                u = x / max(1, size[0] - 1)
                wave = math.sin(u * 7.0 + v * 4.4 + cfg["seed"] * 0.01) * 0.5 + 0.5
                base = blend(BG, blend(accent, accent2, 0.35), 0.12 + wave * 0.08)
                px[x, y] = (*blend(base, accent3, 0.04 * math.sin((u + v) * math.tau) ** 2), alpha)
        return image

    def finish(image, output):
        image = image.resize(SIZE, Image.Resampling.LANCZOS)
        image = image.filter(ImageFilter.UnsharpMask(radius=1.0, percent=105, threshold=4))
        output.parent.mkdir(parents=True, exist_ok=True)
        image.convert("RGB").save(output, optimize=True, quality=94)

    def grid(draw, w, h, step, alpha):
        for x in range(0, w, step):
            draw.line((x, 0, x, h), fill=(255, 255, 255, alpha))
        for y in range(0, h, step):
            draw.line((0, y, w, y), fill=(255, 255, 255, alpha))

    def traces(draw, w, h, cfg):
        rng = random.Random(cfg["seed"])
        for _ in range(46):
            y = rng.randrange(40, h - 40)
            x = rng.randrange(0, max(1, w - 260))
            color = rng.choice([cfg["accent"], cfg["accent2"], cfg["accent3"], INK])
            draw.rounded_rectangle((x, y, x + rng.randrange(42, 260), y + 2 * SCALE), 1 * SCALE, fill=rgba(color, rng.randrange(22, 62)))

    def dither(draw, w, h, alpha):
        for y in range(0, h, 3 * SCALE):
            draw.line((0, y, w, y), fill=(0, 0, 0, alpha))
        for y in range(0, h, 4 * SCALE):
            for x in range(0, w, 4 * SCALE):
                if BAYER_4[(y // (4 * SCALE)) % 4][(x // (4 * SCALE)) % 4] < 4:
                    draw.point((x, y), fill=(255, 255, 255, alpha))

    def motif(draw, w, h, cfg):
        cx, cy = int(w * 0.52), int(h * 0.50)
        colors = [cfg["accent"], cfg["accent2"], cfg["accent3"]]
        if cfg["motif"] == "verdict":
            labels = ["MATCH", "DRIFT", "UNVERIFIABLE"]
            for i, label in enumerate(labels):
                y = int(h * 0.24) + i * int(0.17 * h)
                draw.rounded_rectangle((int(w * 0.42), y, int(w * 0.92), y + 54 * SCALE), 10 * SCALE, fill=(9, 12, 16, 218), outline=rgba(colors[i % 3], 190), width=2 * SCALE)
                draw.text((int(w * 0.47), text_y(draw, label, fonts["bold"], y, 54 * SCALE)), label, font=fonts["bold"], fill=INK)
            draw.arc((cx - 190 * SCALE, cy - 150 * SCALE, cx + 190 * SCALE, cy + 150 * SCALE), 200, 510, fill=rgba(cfg["accent"], 190), width=5 * SCALE)
            return
        rng = random.Random(cfg["seed"])
        nodes = [(rng.randrange(int(w * 0.22), int(w * 0.86)), rng.randrange(int(h * 0.22), int(h * 0.80))) for _ in range(10)]
        for i, a in enumerate(nodes):
            for j, b in enumerate(nodes[i + 1 :], i + 1):
                if (i * 5 + j * 3 + cfg["seed"]) % 7 < 3:
                    draw.line((*a, *b), fill=rgba(colors[i % 3], 82), width=2 * SCALE)
        for i, (x, y) in enumerate(nodes):
            color = colors[i % 3]
            r = (8 + i % 3 * 2) * SCALE
            draw.ellipse((x - r, y - r, x + r, y + r), fill=rgba(color, 225), outline=rgba(INK, 100), width=SCALE)
        if cfg["motif"] == "intake":
            label = "PACKET"
        elif cfg["motif"] == "ledger":
            label = "HANDOFF"
        elif cfg["motif"] == "graph":
            label = "MAP"
        elif cfg["motif"] == "gamut":
            label = "COLOR"
        elif cfg["motif"] == "verdict":
            label = "RESULT"
        else:
            label = "WORKBENCH"
        draw.rounded_rectangle((int(w * 0.57), int(h * 0.72), int(w * 0.91), int(h * 0.85)), 12 * SCALE, fill=(9, 12, 16, 222), outline=rgba(cfg["accent"], 155), width=2 * SCALE)
        draw.text((int(w * 0.61), text_y(draw, label, fonts["bold"], int(h * 0.72), int(h * 0.13))), label, font=fonts["bold"], fill=INK)

    def viewport(cfg, w=576 * SCALE, h=420 * SCALE):
        image = background((w, h), cfg)
        draw = ImageDraw.Draw(image, "RGBA")
        grid(draw, w, h, 40 * SCALE, 14)
        traces(draw, w, h, cfg)
        motif(draw, w, h, cfg)
        dither(draw, w, h, 4)
        draw.rounded_rectangle((36 * SCALE, 32 * SCALE, 244 * SCALE, 80 * SCALE), 9 * SCALE, fill=(9, 12, 16, 210), outline=rgba(cfg["accent"], 125), width=SCALE)
        header = {
            "intake": "SOURCES",
            "verdict": "CHECK",
            "graph": "MAP",
            "ledger": "ROUTE",
            "gamut": "COLOR",
            "membrane": "WORKSPACE",
        }.get(cfg["motif"], cfg["motif"].upper())
        draw.text((54 * SCALE, text_y(draw, header, fonts["small"], 32 * SCALE, 48 * SCALE)), header, font=fonts["small"], fill=INK)
        return image.filter(ImageFilter.UnsharpMask(radius=0.8, percent=110, threshold=3))

    def paste_rounded(base, layer, xy, radius):
        mask = Image.new("L", layer.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, layer.size[0] - 1, layer.size[1] - 1), radius=radius, fill=255)
        clipped = layer.copy()
        clipped.putalpha(mask)
        base.alpha_composite(clipped, dest=xy)

    def draw_text_panel(draw, cfg):
        x, y = 84 * SCALE, 78 * SCALE
        draw.rounded_rectangle((x, y, 902 * SCALE, 562 * SCALE), 12 * SCALE, fill=(6, 9, 13, 246), outline=(248, 249, 246, 58), width=SCALE)
        draw.text((112 * SCALE, 108 * SCALE), cfg["title"], font=fonts["display"], fill=INK)
        draw.rounded_rectangle((116 * SCALE, 244 * SCALE, 852 * SCALE, 252 * SCALE), 2 * SCALE, fill=cfg["accent"])
        draw.rounded_rectangle((388 * SCALE, 244 * SCALE, 852 * SCALE, 252 * SCALE), 2 * SCALE, fill=cfg["accent2"])
        draw.rounded_rectangle((612 * SCALE, 244 * SCALE, 852 * SCALE, 252 * SCALE), 2 * SCALE, fill=cfg["accent3"])
        draw.text((116 * SCALE, 298 * SCALE), cfg["subtitle"].upper(), font=fonts["bold"], fill=cfg["accent"])
        draw.text((116 * SCALE, 354 * SCALE), cfg["tagline"], font=fonts["mono"], fill=MUTED)
        bx = 116 * SCALE
        for badge in cfg["badges"]:
            width = max(86 * SCALE, int(draw.textlength(badge, font=fonts["small"])) + 30 * SCALE)
            box = (bx, 462 * SCALE, bx + width, 502 * SCALE)
            draw.rounded_rectangle(box, 8 * SCALE, fill=(22, 27, 35, 236), outline=rgba(cfg["accent"], 155), width=SCALE)
            draw.text((bx + 15 * SCALE, text_y(draw, badge, fonts["small"], 462 * SCALE, 40 * SCALE)), badge, font=fonts["small"], fill=INK)
            bx += width + 14 * SCALE
        draw.text((116 * SCALE, 526 * SCALE), cfg.get("footer", "PROJECT TELOS FLAGSHIP / CLI + MCP + RECEIPTS"), font=fonts["small"], fill=(210, 216, 220, 190))

    for name, cfg in config.items():
        base = background((SIZE[0] * SCALE, SIZE[1] * SCALE), cfg)
        draw = ImageDraw.Draw(base, "RGBA")
        grid(draw, base.size[0], base.size[1], 56 * SCALE, 3)
        vp = viewport(cfg)
        paste_rounded(base, vp, (972 * SCALE, 94 * SCALE), 18 * SCALE)
        draw.rounded_rectangle((972 * SCALE, 94 * SCALE, 1548 * SCALE, 514 * SCALE), 18 * SCALE, outline=(248, 249, 246, 70), width=SCALE)
        draw_text_panel(draw, cfg)
        finish(base, paths(args.public_root, name)[0])
    return inspect_outputs(args.public_root, config)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render or verify Project Telos flagship README hero images.")
    parser.add_argument("--public-root", type=Path, default=Path("C:/dev/public"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--kilon-zip", type=Path, default=env_path("TELOS_KILON_FONT_ZIP", Path.home() / "Downloads" / "Kilon-Bold-Display-Font.zip"))
    parser.add_argument("--conso-zip", type=Path, default=env_path("TELOS_CONSO_FONT_ZIP", Path.home() / "Downloads" / "Conso-Font-Family.zip"))
    parser.add_argument("--render", action="store_true", help="render PNGs using local font ZIPs and Pillow")
    parser.add_argument("--check-existing", action="store_true", help="verify existing PNGs and brand receipts without Pillow")
    parser.add_argument("--json", action="store_true", help="emit receipt JSON to stdout")
    parser.add_argument("--receipt", type=Path, help="optional path to write receipt JSON")
    args = parser.parse_args()
    if not args.render and not args.check_existing:
        args.check_existing = True
    config = load_config(args.config)
    outputs = render_all(args, config) if args.render else inspect_outputs(args.public_root, config)
    mode = "render" if args.render else "check-existing"
    payload = json.dumps(receipt(args, mode, outputs), indent=2)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(payload + "\n", encoding="utf8")
    print(payload if args.json else f"{mode}: {len(outputs)} hero images verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
