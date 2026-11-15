"""Measure the pixel-art style of a reference set.

python3 study_ref.py NAME OUTDIR file [file ...]

Each file may be a sheet (sprites are cut out automatically), a single sprite, or an
animated GIF (frames are analysed and timing/motion is reported). Upscaled images are
reduced to their true pixel size first. Writes OUTDIR/NAME.json and OUTDIR/NAME_zoom.png.
"""
import sys, json, os, colorsys
from collections import Counter, deque
import numpy as np
from PIL import Image, ImageSequence

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills", "pixel-art-studio", "scripts"))
from pixelstudio import detect_scale  # noqa: E402

name, outdir, files = sys.argv[1], sys.argv[2], sys.argv[3:]
os.makedirs(outdir, exist_ok=True)


def to_rgba(im):
    im = im.convert("RGBA")
    a = np.asarray(im).copy()
    if (a[:, :, 3] < 255).sum() < 0.01 * a[:, :, 3].size:      # no real alpha: key out the border colour
        border = np.concatenate([a[0, :, :3], a[-1, :, :3], a[:, 0, :3], a[:, -1, :3]])
        bg = Counter(map(tuple, border)).most_common(1)[0][0]
        a[(a[:, :, :3] == bg).all(-1), 3] = 0
    return a


def true_pixels(a):
    s = detect_scale(Image.fromarray(a, "RGBA"))
    s = s[0] if isinstance(s, tuple) else s
    if s and s > 1:
        a = a[::s, ::s]
    return a, (s or 1)


def components(al, min_side=8, gap=2):
    H, W = al.shape
    dil = al.copy()
    for dy in range(-gap, gap + 1):
        for dx in range(-gap, gap + 1):
            dil |= np.roll(np.roll(al, dy, 0), dx, 1)
    lab = np.zeros((H, W), int); n = 0; out = []
    for y in range(H):
        for x in range(W):
            if dil[y, x] and not lab[y, x]:
                n += 1; q = deque([(y, x)]); lab[y, x] = n; ys = [y]; xs = [x]
                while q:
                    cy, cx = q.popleft()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            yy, xx = cy + dy, cx + dx
                            if 0 <= yy < H and 0 <= xx < W and dil[yy, xx] and not lab[yy, xx]:
                                lab[yy, xx] = n; q.append((yy, xx)); ys.append(yy); xs.append(xx)
                y0, y1, x0, x1 = min(ys), max(ys), min(xs), max(xs)
                if y1 - y0 + 1 >= min_side and x1 - x0 + 1 >= min_side:
                    out.append((y0, x0, y1, x1))
    return out


sprites, anim = [], []
for f in files:
    im = Image.open(f)
    frames = [to_rgba(fr.copy()) for fr in ImageSequence.Iterator(im)] if getattr(im, "n_frames", 1) > 1 else [to_rgba(im)]
    if len(frames) > 1:
        durs = []
        for fr in ImageSequence.Iterator(im):
            durs.append(fr.info.get("duration", 0))
        fr0, s = true_pixels(frames[0])
        fx = [true_pixels(fr)[0] for fr in frames]
        boxes = []
        for a in fx:
            ys, xs = np.nonzero(a[:, :, 3] > 0)
            if len(ys): boxes.append((ys.min(), ys.max(), xs.min(), xs.max()))
        tops = [b[0] for b in boxes]; bots = [b[1] for b in boxes]
        anim.append({"file": os.path.basename(f), "frames": len(frames), "scale": s,
                     "median_ms": float(np.median(durs)) if durs else None,
                     "top_bob_px": int(max(tops) - min(tops)) if tops else 0,
                     "foot_shift_px": int(max(bots) - min(bots)) if bots else 0})
        frames = fx[:: max(1, len(fx) // 6)]          # sample a few frames for style metrics
    else:
        frames = [true_pixels(frames[0])[0]]
    for a in frames:
        al = a[:, :, 3] > 0
        boxes = components(al) if max(a.shape[:2]) > 140 else [(0, 0, a.shape[0] - 1, a.shape[1] - 1)]
        for (y0, x0, y1, x1) in boxes:
            c = a[y0:y1 + 1, x0:x1 + 1]
            if (c[:, :, 3] > 0).sum() > 30:
                sprites.append(c)

if len(sprites) > 150:
    sprites = sprites[:: len(sprites) // 150][:150]
lum_w = np.array([0.299, 0.587, 0.114]) / 255
S = dict(colors=[], gx=0.0, gy=0.0, npx=0, runs=[], dark_edge=[], edge_l=[], in_l=[], black_edge=0, edges=0,
         lines=0, interior=0, sat=[], checker=0, blocks=0, semi=0, families=[], hueshift=[])
pal = Counter(); sizes = []
for c in sprites:
    al = c[:, :, 3] > 0; rgb = c[:, :, :3].astype(float); H, W = al.shape
    sizes.append((W, H)); S["semi"] += int(((c[:, :, 3] > 0) & (c[:, :, 3] < 255)).sum())
    cols = Counter(map(tuple, c[:, :, :3][al])); S["colors"].append(len(cols)); pal.update(cols)
    lum = rgb @ lum_w
    pad = np.pad(al, 1)
    edge = al & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    inn = al & ~edge
    S["edge_l"] += list(lum[edge]); S["in_l"] += list(lum[inn])
    S["black_edge"] += int((edge & (lum < 0.09)).sum()); S["edges"] += int(edge.sum())
    # light direction from interior gradients
    hx = inn[:, 1:-1] & al[:, 2:] & al[:, :-2]; hy = inn[1:-1] & al[2:] & al[:-2]
    S["gx"] += float(np.where(hx, lum[:, 2:] - lum[:, :-2], 0).sum()); S["gy"] += float(np.where(hy, lum[2:] - lum[:-2], 0).sum())
    S["npx"] += int(inn.sum())
    # inner line art: interior pixels clearly darker than the mean of their 4 neighbours
    nb = (np.roll(lum, 1, 0) + np.roll(lum, -1, 0) + np.roll(lum, 1, 1) + np.roll(lum, -1, 1)) / 4
    S["lines"] += int((inn & (lum < nb - 0.12)).sum()); S["interior"] += int(inn.sum())
    for y in range(H):
        r = 1
        for x in range(1, W):
            if al[y, x] and al[y, x - 1] and (c[y, x, :3] == c[y, x - 1, :3]).all(): r += 1
            else:
                if al[y, x - 1]: S["runs"].append(r)
                r = 1
    # checkerboard dithering in 2x2 blocks
    for y in range(0, H - 1, 2):
        for x in range(0, W - 1, 2):
            if al[y:y + 2, x:x + 2].all():
                S["blocks"] += 1
                p = c[y:y + 2, x:x + 2, :3]
                if (p[0, 0] == p[1, 1]).all() and (p[0, 1] == p[1, 0]).all() and not (p[0, 0] == p[0, 1]).all():
                    S["checker"] += 1
    hsv = [colorsys.rgb_to_hsv(*(np.array(k) / 255)) for k in cols]
    S["sat"] += [h[1] for h in hsv for _ in range(1)]
    fam = Counter(int(h[0] * 12) % 12 for h in hsv if h[1] > 0.15)
    S["families"].append(sum(1 for v in fam.values() if v >= 3))
    # hue shift: inside each hue family, compare darkest vs lightest colours
    for b in [k for k, v in fam.items() if v >= 3]:
        mem = sorted([(h[2], h[0]) for h in hsv if h[1] > 0.15 and int(h[0] * 12) % 12 == b])
        d = (mem[-1][1] - mem[0][1] + 0.5) % 1 - 0.5          # light hue minus dark hue, in turns
        S["hueshift"].append(d * 360)

r = lambda v, n=2: round(float(v), n)
report = {
    "study": name, "files": [os.path.basename(f) for f in files], "sprites": len(sprites),
    "sprite_size_median_wh": [int(np.median([s[0] for s in sizes])), int(np.median([s[1] for s in sizes]))] if sizes else None,
    "colors_per_sprite_median": int(np.median(S["colors"])) if S["colors"] else 0,
    "palette_total": len(pal),
    "light_dir": {"x": r(S["gx"] / max(S["npx"], 1), 4), "y": r(S["gy"] / max(S["npx"], 1), 4),
                  "note": "negative x = lit from left, negative y = lit from top"},
    "edge_vs_interior_lum": [r(np.median(S["edge_l"])), r(np.median(S["in_l"]))],
    "black_outline_share": r(S["black_edge"] / max(S["edges"], 1)),
    "inner_line_share": r(S["lines"] / max(S["interior"], 1), 3),
    "one_px_run_share": r(np.mean(np.array(S["runs"]) == 1)) if S["runs"] else None,
    "dither_checker_share": r(S["checker"] / max(S["blocks"], 1), 3),
    "saturation_median": r(np.median(S["sat"])) if S["sat"] else None,
    "ramp_families_per_sprite": r(np.median(S["families"]), 1) if S["families"] else 0,
    "hue_shift_light_minus_dark_deg_median": r(np.median(S["hueshift"]), 1) if S["hueshift"] else None,
    "semi_alpha_px": S["semi"],
    "animation": anim,
    "top_colors": ["#%02x%02x%02x" % k for k, _ in pal.most_common(16)],
}
json.dump(report, open(f"{outdir}/{name}.json", "w"), indent=1)
# zoom sheet of up to 10 representative sprites
pick = sorted(sprites, key=lambda c: -(c[:, :, 3] > 0).sum())[:: max(1, len(sprites) // 10)][:10]
if pick:
    z = max(2, min(8, 420 // max(max(p.shape[:2]) for p in pick)))
    Wt = sum(p.shape[1] for p in pick) * z + 8 * len(pick); Ht = max(p.shape[0] for p in pick) * z
    sheet = Image.new("RGBA", (Wt, Ht), (64, 78, 62, 255)); x = 0
    for p in pick:
        im = Image.fromarray(p.astype(np.uint8), "RGBA").resize((p.shape[1] * z, p.shape[0] * z), Image.NEAREST)
        sheet.alpha_composite(im, (x, Ht - im.height)); x += im.width + 8
    sheet.save(f"{outdir}/{name}_zoom.png")
print(json.dumps({k: report[k] for k in report if k not in ("files", "top_colors")}))
