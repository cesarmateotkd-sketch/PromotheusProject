# Frog Ronin sprite pipeline (Blender -> pixel art)

Original models built from primitives in script; no third-party art.

- `keyart_build.py` — builds the frog and beetle in Blender, renders a white-diffuse light pass
  (`lit_*`) and a flat base-colour pass (`alb_*`) at 1x (360x200) and 4x.
  `blender -b --factory-startup --python keyart_build.py -- OUTDIR` (writes to OUTDIR; post reads `out/`)
- `keyart_post.py` — toon finish: 4-tone hue-shifted ramps per material, material-boundary ink,
  1px violet-black outline, nearest 2x; composites over the golden-hour HD-2D pond with pixel
  hit effects. `python3 keyart_post.py OUTDIR` (run from the folder holding `out/`).

Decisions: design/brainstorm.md D19-D22. Approved look: design/art/keyart/frog-ronin-keyart-v2.png.

## Animation frames (12 fps)
- `common.py` — shared materials and mesh helpers (read by the two scripts below).
- `anim_build.py` — posable frog (stance, planted feet with 2-bone legs, grip, sword angle,
  lean, head, tail flutter, grin); renders idle (8), walk (8), strike (7), strike2 (6), strike3 (6), hurt (5), dodge (7), victory (8) at 1x in a 256x288
  cell with the ground fixed. `blender -b --factory-startup --python anim_build.py -- FRAMES [idle,walk,strike]`
- `anim_post.py` — same pixel finish as the key art; writes `frog_<anim>_sheet.png` (1x strip)
  and a 3x GIF preview. `python3 anim_post.py FRAMES OUTDIR`

## The bug clan
- `bugs_build.py` — beetle (ashigaru), mosquito (ninja), spitter (teppo gunner), mantis (ronin
  mini-boss), hornet shogun (boss); idle 6, attack 6, hurt 3 each. Built mirrored (facing +X with
  mirrored lights) so the fronts face the camera; writes `<bug>_meta.json` with cell size and
  ground row. `blender -b --factory-startup --python bugs_build.py -- FRAMES [bug,bug]`
- Finish with `FLIP=1 SHEET_PREFIX="" python3 anim_post.py FRAMES OUTDIR` (flips them to face left).

## Into the game
- `RES_PCT=67` on both build scripts renders at the game's scale (2/3 of the key art).
- `bg_layers.py OUTDIR` — golden-hour parallax backdrop layers (sky, far, water, ground) at 2x.
- `make_game_assets.py FROG_FRAMES BUG_FRAMES BG_DIR prototypes/frog-ronin` — packs the strips and
  layers into the game's assets/ and writes assets/sprites.js (metadata plus embedded copies).
