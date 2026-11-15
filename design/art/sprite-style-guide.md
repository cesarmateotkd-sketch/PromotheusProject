# Sprite Style Guide — lessons from 12 reference studies

Read this before making ANY sprite for this project. It is the project's memory of what makes pixel art read well,
measured from shipped games. Per-game detail lives in the study cards at
`.claude/skills/pixel-art-studio/references/learned/006`–`017` (indexed in that folder's `INDEX.md`);
raw measurements are in `design/art/studies/data/`. Reference images themselves are not stored in the repo (third-party IP);
only our measurements and rules are.

## The process (always)
1. **Study before drawing.** Pick 2–3 shipped games whose look matches the target. Get their sheets and run
   `python3 tools/sprites/study_ref.py NAME OUTDIR files...` (sheets, single sprites or animated GIFs; upscales are detected).
2. **Write a style card** (palette budget, outline rule, light, line-work share, proportions) before building.
3. **Build to the card**, then **measure the result with the same script** and compare numbers, not impressions.
4. Run the pixel-art-studio checklist (`references/validations.md`) and the asset report before calling anything done.

## Measured across the references
| study | median size | colours/sprite | black outline | inner lines | 1px runs | dither | saturation |
|---|---|---|---|---|---|---|---|
| deadcells | 88x46 | 12 | 2% | 7% | 28% | 0.4% | 0.49 |
| eastward | 54x65 | 11 | 0% | 14% | 41% | 0.3% | 0.53 |
| ff6 | 19x27 | 11 | 0% | 26% | 72% | 2.5% | 0.5 |
| idleon | 100x90 | 18 | 86% | 11% | 48% | 1.0% | 0.47 |
| idleslayer | 32x16 | 10 | 86% | 28% | 69% | 0.0% | 0.53 |
| metalslug_adv | 95x38 | 13 | 1% | 19% | 67% | 1.8% | 0.35 |
| pokemon_bw | 81x68 | 13 | 48% | 12% | 56% | 1.0% | 0.64 |
| soulknight | 40x40 | 8 | 100% | 17% | 64% | 1.3% | 0.4 |
| stardew | 14x15 | 6 | 8% | 13% | 76% | 3.4% | 0.71 |
| terraria | 23x24 | 17 | 7% | 22% | 91% | 6.6% | 0.58 |
| strider_nxc (earlier study) | ~85x80 | 25 | 0% (coloured) | 31% | 61% | 2.0% | high |
| ro_assassin (earlier study) | ~40x70 | 45 | 0% (soft coloured) | 14% | 59% | 0.8% | low |

## Laws that held across (almost) every study
1. **Light comes from the top or upper-left.** Every single reference. Never light from below or switch per sprite.
2. **Dithering is rare.** Under 3.5% everywhere; Terraria's 6.6% is sparkle on top-tier items only.
3. **Outline weight follows size.** Small phone sprites (≤ ~48px: Soul Knight, Idle Slayer, IdleOn) use a 1px **near-black** outline (86–100%).
   Larger, detailed sprites (RO, Eastward, Metal Slug, FF6, Strider) use **dark coloured** outlines (0–8% black) — contrast without black.
4. **Colour budget is small and fixed.** Icons ~6 colours, small units 8–13, detailed characters 13–25.
   Eastward animates 34 frames with **15 colours total**. Lock the palette before animating.
5. **Line work scales inversely with size.** Tiny sprites need 25%+ interior line pixels to separate parts (FF6, Idle Slayer);
   mid sprites 11–19%; soft/3D-rendered styles 7–14%.
6. **Crisp, not smooth.** 1px colour runs dominate (41–91%); no anti-aliased soft edges (semi-alpha ≈ 0 except glow).

## Defaults for a mobile idle game (use unless a study for the chosen look says otherwise)
- **Units/characters on screen at once:** 24–48px tall, 1px near-black outline, 8–13 colours, one dominant colour family per unit
  so each type is recognisable by colour alone (Idle Slayer, Soul Knight).
- **Featured hero / showcase unit:** 64–96px, dark coloured outline, 13–25 colours, more line work for form (Strider, Pokémon, RO).
- **Modular roster:** one template body + layered gear, weapons, hats and colour (IdleOn). Detail goes into upgradeable items.
- **Idle animation:** long, subtle loops (Pokémon: 5–9 s, bob ≤ 10% of height, feet locked, secondary parts on their own timing).
  Cheap background units: 2–4 frames at 150–200ms with a 1px bob (Soul Knight).
- **Upgrade tiers (Terraria ladder):** tiers 1–4 keep the shape and swap material hue (copper → iron → gold → platinum);
  then add silhouette features (guards, gems); top tiers get bigger, a signature saturated colour, more colours and 1–3 glow pixels.
  A higher tier is never smaller or duller.
- **Progress / growth (Stardew):** 4–6 stages that grow in size and saturation; the final stage reveals the reward colour.
- **Icons:** fixed 16 or 32px cell, fixed margin, same light, ~6 colours, vivid (Stardew saturation ≈ 0.7).
- **Saturation hierarchy:** effects/feedback (coins, hits, level-ups) most saturated → units vivid → backgrounds muted
  (Metal Slug, Idle Slayer). Muted characters on vivid backgrounds is the wrong way round.
- **Feedback frames:** exaggerated squash/recoil and bright separate effect sprites make taps satisfying (Metal Slug).
- **Faces:** at ≤ 32px a face is 2 dark pixels; expressiveness goes into face + hands while the body silhouette stays stable (Eastward).

## Our own pipeline (tools/sprites) — lessons from the ninja test
- 3D → pixel works commercially (Dead Cells): per-material colour ramps, hard bands, value contrast, many frames.
- Place feet first (inverse kinematics) or walks moonwalk; move units at the measured stride speed or feet slide.
- After rendering, always: majority-smooth the shade shapes, remove orphan pixels, thin lines to pixel-perfect 1px.
- Decode Blender's flat ID colours through the sRGB curve or material lookups silently fail.
