# Study: Pokémon Black/White battle sprites — long, grounded idle loops

- **source**: pokemondb.net animated battle GIFs (charizard, emboar, lucario, pikachu, serperior, zoroark), downloaded directly · studied: 2026-11-15
- **true size**: ~80x70px, native · **colors**: 13 per sprite, ~75 across six creatures
- **subject**: always-on idle animations of creatures on a small (DS) screen

## Measurements
- outline: 48% of edge pixels near-black, the rest dark coloured (selout on lit edges)
- inner lines 12%; 1px runs 56%; dithering 1%
- light from upper-left; saturation 0.64 (vivid)
- animation: 112–179 frames per loop at 50ms (≈6–9 s cycle); body bob 3–10px; **feet never move** (foot shift 0–2px)

## Observations
- loops are layered motion (breathing body, flicking tail/flame, blinking) at different rates, so they never feel repetitive
- 2 hue families per creature with clear hue shift (+4° median, highlights warm)

## Rules to apply
- Idle-game idle loops: long (5–9 s), subtle (bob ≤ 10% of height), feet/base locked, secondary parts (tails, flames, cloth) on their own timing
- Vivid saturation on the focal creature/character; 13-ish colours per sprite

## Do NOT copy
- The 150-frame budget everywhere; use it for the hero/featured unit, cheaper loops for the rest
