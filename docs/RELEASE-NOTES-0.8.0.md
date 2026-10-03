# Telos 0.8.0

Telos 0.8.0 measures your own image. Hand `telos.measurement.layers` raw 8-bit
RGBA and it returns four measurement layers, each with a SHA-256 receipt, so a
model or a script can read compact colour and tone facts about a frame and
anyone can re-derive the same numbers later. Called with no arguments, the tool
still returns the demo meters it returned in 0.7.0.

## Try it

This builds a 64 x 64 test image and asks for three layers over stdio:

```
node -e 'const px=Buffer.alloc(64*64*4).map((_,i)=>[200,80,40,255][i%4]);console.log(JSON.stringify({jsonrpc:"2.0",id:1,method:"tools/call",params:{name:"telos.measurement.layers",arguments:{image:{rgba:px.toString("base64"),width:64,height:64},layers:["L0","L1","L2"]}}}))' | npx -y project-telos-mcp@0.8.0
```

To read files from disk, list the folders Telos may open in
`TELOS_MEASUREMENT_ROOTS` and pass `image.path` with `width` and `height` in
place of `image.rgba`.

## What you get

| Layer | Carries | Drops |
|---|---|---|
| L0 | global tone range and colour cast | every spatial fact |
| L1 | a coarse 8 x 8 colour layout | fine structure and texture |
| L2 | the perceptual field in OKLab cells, with an 8-bit lightness branch for greyscale frames | detail below the cell size |
| L3 | your overlays, reported as pixel boxes | nothing inside the overlay |

You can also pass a region of interest and ask for an exact-area resample in
linear light before measuring.

- The same pixels give the same layer text and the same receipt on any engine,
  because every number comes from integer arithmetic.
- Values from your pixels are marked `computed` and carry the input receipt.
  The packet verdict stays `UNVERIFIABLE` until you name a criterion, since a
  measurement alone judges nothing.
- No layer carries more than one cell per 16 input pixels. A final scan refuses
  any response that would carry a long run of encoded data, so the tool cannot
  hand your image back to a caller in disguise.
- Paths resolve through every symlink and junction before the root check.
  UNC, device and relative paths are refused.

## Measured

Release checks, run before this release on one Windows machine with Node 25:

- An independent Python implementation re-derives 100 of 100 receipts byte for
  byte.
- 201 of 201 constant colours land in one histogram bin, and the exact OKLab
  mean is within 5e-10 of a float64 reference.
- A one-pixel edit changes the input and response receipts on 20 of 20 images.
  All 20 edited responses fail verification.
- The payload scan flagged 0 of 101 ordinary images and refused both injected
  runs.
- A mutation run breaks the code behind each of the 7 equality checks in the
  new suite, and all 11 mutations are caught.

Research measurements on three public biomedical benchmark sets (PBC blood
cells, Kather colorectal histology tiles and BBBC010 worm assays) used a linear
probe inside each source:

- L1 measured at most 142 tokens (Qwen3.5 tokenizer) over 2,536 images.
- On Kather tiles, the L2 field beats the earlier colorGrid16 encoding by 8.5
  points [4.3, 11.7] while using 59% of its tokens. On PBC the two are level.
- On PBC, L0 and L2 each add accuracy with a lower bound above zero. On Kather,
  L0 and L1 do, and adding L2 lowers accuracy by about 2 points.

## Limits

- L1 fails a structure check on texture tiles. Rebuilding an image from L1
  improves colour error on every source, yet SSIM gets worse by more than 0.05
  on 50 of 1,000 Kather tiles. An 8 x 8 grid cannot hold the structure of a
  fine texture, so read structure from L2.
- The BBBC010 results are inconclusive. The controls for both BBBC010 tasks
  fail by their own pre-registered rules, so no value is claimed there.
- L2 shifts more than its invariance bound on artwork when the image moves by
  one pixel or is halved in size. The biomedical sets pass these checks.
- The probe results hold inside each source only. The Kather intervals rest on
  10 patients. Nothing here shows how a held-out source behaves.
- None of these checks shows that a model can read the layers. The release
  checks cover bytes, paths and receipts on one machine and one Node version.
- The benchmark images are research data. Telos makes no medical claim.
