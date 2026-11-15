# Study: Stardew Valley items and crops — icon families and growth stages

- **source**: Spriters Resource "Crops" (256x832) and "Harvested Crops, Seed Packets, Minerals, Food, Equipment & Misc" (512x624), native-size page screenshots · studied: 2026-11-15
- **true size**: 16x16 icons; crops in 16x32 stage strips · **colors**: ~6 per item
- **subject**: hundreds of item icons and crop growth stages

## Measurements (items sheet is dense; touching icons partly merged)
- outline: dark coloured (black only 8%), edge lum 0.21 vs 0.40
- inner lines 13%; 1px runs 76%; dithering 3.4% (texture on minerals/food)
- saturation 0.71 (very vivid); light from upper-left

## Observations
- every icon fits a 16x16 cell with a consistent ~1px margin and a consistent 3/4 top-left light
- crops show progress in 4–6 stages: seed → sprout → leafy → flowering → ripe; size and colour saturation increase stage by stage, the ripe stage introduces the product colour
- bars/ores progress copper → iron → gold → iridium by hue, keeping the same shape

## Rules to apply
- Icons: fixed cell (16 or 32px), fixed margin, same light, ~6 colours, vivid
- Show progress by growth stages that increase size + saturation, with the final stage revealing the reward colour
- Material tiers: keep the shape, change the hue (copper/iron/gold/iridium ramps)

## Do NOT copy
- Stardew's exact icons; its dither texture on everything (keep dither for minerals/food surfaces only)
