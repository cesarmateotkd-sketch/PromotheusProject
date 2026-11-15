# Study: Dead Cells — 3D models rendered to pixel art

- **source**: community dump of the game's packed sprite atlases (player + an enemy atlas) · studied: 2026-11-15
- **true size**: atlas 1024² and a 1024² crop of a 2048x4096 atlas · **colors**: ~12 per character frame; 127 across the sampled set
- **subject**: thousands of animation frames produced by rendering 3D models to low resolution (the same pipeline as our tools/sprites renderer)

## Measurements (approximate — packed atlas frames touch, so some measured "sprites" are merged neighbours)
- outline: almost no black (2%); edge brightness ≈ interior (0.31 vs 0.28) — silhouettes read by value contrast, not line
- inner lines: 7% (lowest of all studies); 1px runs 28% (large flat bands); dithering 0.4%
- saturation 0.49; accents are hot magenta/pink and cyan on dark slate bodies

## Observations
- frames are flat 3–4 value bands per material, exactly what a 3D render quantised per material looks like
- huge frame counts per move: smoothness comes from many frames, not from detail per frame

## Rules to apply
- Our 3D→pixel pipeline is a proven commercial technique; keep per-material colour ramps and hard bands
- When rendering from 3D, rely on value contrast and a single accent colour for readability instead of heavy outlines
- Spend effort on frame count for important motions (attacks), not per-frame detail

## Do NOT copy
- Merged-atlas numbers literally; the dark low-contrast palette is tuned for a PC screen, too dark for small phone sprites
