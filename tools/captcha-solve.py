#!/usr/bin/env python
# Native CAPTCHA solver for the "typically unsolvable by a bot" image class.
#
# Run in the local-model venv (E:\local-model-run\venv) which has torch+CUDA
# (RTX 4090) + transformers. Two tiers, both fully local and free:
#
#   image <grid.png> <prompt>   -> reCAPTCHA/hCaptcha image grid: crop tiles,
#                                 ask a local VLM per tile "does this show
#                                 {prompt}?", return the yes-tile indices.
#   audio <audio.wav>            -> reCAPTCHA/hCaptcha audio challenge: run a
#                                 local Whisper STT, return the digit/word string.
#
# The VLM/Whisper load lazily and are selected by env (CAPTCHA_VLM,
# CAPTCHA_WHISPER), so this script degrades honestly when a model is absent.
#
# Output: one JSON line on stdout: {"tier":..., "ok":bool, "solve":..., "note":...}

from __future__ import annotations
import sys, os, json, io

def _torch():
    import torch
    return torch

def solve_image(path: str, prompt: str) -> dict:
    """Crop a reCAPTCHA-style NxN grid and classify each tile with a local VLM.
    Returns the 1-based indices of tiles the VLM judges as matching `prompt`."""
    from PIL import Image
    img = Image.open(path).convert("RGB")
    w, h = img.size
    # reCAPTCHA grids are 3x3 or 4x4; auto-detect the nearest square grid by
    # assuming square tiles and trying 3 then 4.
    picks = []
    note = ""
    vlm_id = os.environ.get("CAPTCHA_VLM", "Qwen/Qwen2-VL-2B-Instruct")
    try:
        # Zero-shot CLIP tile classifier: lighter and reliably importable, asks
        # per cropped tile "is this {prompt}?" and returns the yes tiles.
        from transformers import CLIPModel, CLIPProcessor
        clip_id = os.environ.get("CAPTCHA_CLIP", "openai/clip-vit-large-patch14")
        model = CLIPModel.from_pretrained(clip_id, torch_dtype="auto").eval()
        proc = CLIPProcessor.from_pretrained(clip_id)
        torch = _torch()
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        model = model.to(dev)
        # try 3x3 then 4x4; pick the grid whose top tile-class looks most decisive
        for n in (3, 4):
            tw, th = w // n, h // n
            tiles = [img.crop((c * tw, r * th, (c + 1) * tw, (r + 1) * th))
                     for r in range(n) for c in range(n)]
            yes_text = f"a photo of {prompt}"
            no_text = "a photo of something else"
            inputs = proc(text=[yes_text, no_text] * len(tiles),
                          images=[t for t in tiles for _ in (0, 1)],
                          return_tensors="pt", padding=True).to(dev)
            with torch.no_grad():
                probs = model(**inputs).logits_per_image.softmax(dim=-1)[:, 0]
            picks = [i + 1 for i, p in enumerate(probs.tolist()) if p > 0.5]
            note = f"clip {clip_id} grid {n}x{n}"
            if picks:
                return {"tier": "image-vlm", "ok": True, "solve": picks,
                        "grid": f"{n}x{n}", "note": note}
        return {"tier": "image-vlm", "ok": True, "solve": [], "note": note + " (no tiles matched)"}
    except Exception as ex:  # model not downloaded / offline
        return {"tier": "image-vlm", "ok": False, "solve": [],
                "note": f"VLM/CLIP unavailable ({type(ex).__name__}: {ex}); set CAPTCHA_VLM/CAPTCHA_CLIP and pre-download"}


def solve_audio(path: str) -> dict:
    """Transcribe a reCAPTCHA/hCaptcha audio challenge with local Whisper."""
    whisper_id = os.environ.get("CAPTCHA_WHISPER", "tiny.en")
    try:
        import whisper  # openai-whisper
        model = whisper.load_model(whisper_id)
        text = model.transcribe(path)["text"].strip()
        return {"tier": "audio-whisper", "ok": True, "solve": text, "note": f"whisper {whisper_id}"}
    except Exception as ex:
        return {"tier": "audio-whisper", "ok": False, "solve": "",
                "note": f"whisper unavailable ({type(ex).__name__}: {ex}); pip install -U openai-whisper + ffmpeg"}


def main() -> int:
    if len(sys.argv) < 3:
        print(json.dumps({"ok": False, "note": "usage: captcha-solve.py image <path> <prompt> | audio <path>"}))
        return 64
    mode = sys.argv[1]
    if mode == "image":
        out = solve_image(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
    elif mode == "audio":
        out = solve_audio(sys.argv[2])
    else:
        out = {"ok": False, "note": f"unknown mode: {mode}"}
    print(json.dumps(out))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
