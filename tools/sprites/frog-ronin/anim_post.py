"""Pixel-finish the frog's animation frames: sheets (1x), and GIF previews at 3x on the pond.
Run: python3 anim_post.py FRAMES OUTDIR KEYART_BG"""
import sys, re, colorsys, os
import numpy as np
from PIL import Image
FR, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
PREFIX = os.environ.get("SHEET_PREFIX", "frog_")
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "common.py")).read()
BASE = {k: tuple(map(int, v.split(","))) for k, v in re.findall(r'"(\w+)": \((\d+, \d+, \d+)\)', src.split("mats = {}")[0])}
NAMES = list(BASE); PAL = np.array([BASE[n] for n in NAMES], float); INK = np.array([26, 20, 40], float)
def ramp(name, c):
    h, s, v = colorsys.rgb_to_hsv(*(np.array(c) / 255))
    def sh(h, to, a): d = ((to - h + 0.5) % 1) - 0.5; return (h + d * a) % 1
    t = [(sh(h, 0.68, 0.16), min(1, s * 1.15 + 0.05), v * 0.48), (sh(h, 0.68, 0.08), min(1, s * 1.08), v * 0.72), (h, s, v), (sh(h, 0.14, 0.08), s * 0.8, min(1, v * 1.12 + 0.04))]
    if name in ("eyew", "hilite"): t = [(0.68, 0.18, 0.72), (0.66, 0.08, 0.86), (h, s, v), (h, s, 1.0)]
    return np.array([colorsys.hsv_to_rgb(*x) for x in t]) * 255
RAMPS = np.array([ramp(n, BASE[n]) for n in NAMES])
def toon(lit_p, alb_p):
    lit = np.asarray(Image.open(lit_p).convert("RGBA"), float) / 255; alb = np.asarray(Image.open(alb_p).convert("RGBA"), float)
    lit = np.pad(lit, ((2, 2), (2, 2), (0, 0))); alb = np.pad(alb, ((2, 2), (2, 2), (0, 0)))  # no wrap-around at the cell edge
    a = alb[..., 3] > 127; idx = ((alb[..., None, :3] - PAL[None, None]) ** 2).sum(-1).argmin(-1)
    L = lit[..., :3].mean(-1); band = sum((L > x).astype(int) for x in (0.2, 0.42, 0.78)); col = RAMPS[idx, band]
    diff = np.zeros(a.shape, bool); lum = PAL[idx].sum(-1)
    for dy, dx in ((0, 1), (1, 0)):
        n = np.roll(idx, (-dy, -dx), (0, 1)); na = np.roll(a, (-dy, -dx), (0, 1)); e = (n != idx) & a & na; nl = PAL[n].sum(-1)
        diff |= e & (lum <= nl); diff |= np.roll(e & (nl < lum), (dy, dx), (0, 1))
    col = np.where(diff[..., None], RAMPS[idx, 0] * 0.7, col)
    ol = np.zeros_like(a)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)): ol |= np.roll(a, (dy, dx), (0, 1))
    ol &= ~a
    rgba = np.zeros(a.shape + (4,)); rgba[..., :3] = np.where(a[..., None], col, INK); rgba[..., 3] = (a | ol) * 255
    im = Image.fromarray(rgba[2:-2, 2:-2].astype(np.uint8), "RGBA")
    return im.transpose(Image.FLIP_LEFT_RIGHT) if os.environ.get("FLIP") else im
anims = {}
for f in sorted(os.listdir(FR)):
    m = re.match(r"(\w+?)_(\d+)_lit\.png", f)
    if m: anims.setdefault(m[1], []).append(int(m[2]))
def stage(w, h):
    """Simple golden-hour pond strip so the previews read in context (ground at the feet line)."""
    from PIL import ImageDraw
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im); g = int(h * 0.86)
    for y in range(h):
        t = y / g; c = (int(150 + 105 * t), int(196 + 18 * t), int(226 - 66 * t)) if y < g * 0.62 else (64, 168, 176)
        d.line([(0, y), (w, y)], fill=(*c, 255))
    d.rectangle([0, g - 10, w, g + 2], fill=(118, 170, 72, 255)); d.rectangle([0, g, w, h], fill=(196, 160, 110, 255))
    return im
SMEAR = {"strike": [2], "strike2": [2], "strike3": [2]}   # cut frames get a baked swing smear
FLASH = {"hurt": [0]}                                        # hit flash
TWIG = np.array(BASE["twig"], float)
def twig_ends(alb_p):
    al = np.asarray(Image.open(alb_p).convert("RGBA"), float)
    m = (np.abs(al[..., :3] - TWIG).sum(-1) < 8) & (al[..., 3] > 127)
    ys, xs = np.nonzero(m)
    if len(xs) < 3: return None
    body = np.array([np.nonzero(al[..., 3] > 127)[1].mean(), np.nonzero(al[..., 3] > 127)[0].mean()])
    d = (xs - body[0]) ** 2 + (ys - body[1]) ** 2
    return (xs[d.argmax()], ys[d.argmax()]), (xs[d.argmin()], ys[d.argmin()])
def smear(size, prev_tip, tip, hand):
    from PIL import ImageDraw
    im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hx, hy = hand
    a0 = np.arctan2(prev_tip[1] - hy, prev_tip[0] - hx); a1 = np.arctan2(tip[1] - hy, tip[0] - hx)
    if a1 - a0 > np.pi: a1 -= 2 * np.pi
    if a0 - a1 > np.pi: a1 += 2 * np.pi
    r = np.hypot(tip[0] - hx, tip[1] - hy) + 2
    outer = [(hx + r * np.cos(a0 + (a1 - a0) * t), hy + r * np.sin(a0 + (a1 - a0) * t)) for t in np.linspace(0, 1, 18)]
    inner = [(hx + r * (0.45 + 0.4 * t) * np.cos(a0 + (a1 - a0) * t), hy + r * (0.45 + 0.4 * t) * np.sin(a0 + (a1 - a0) * t)) for t in np.linspace(0, 1, 18)]
    poly = outer + inner[::-1]
    d.polygon(poly, fill=(255, 210, 110, 255), outline=(26, 20, 40, 255))
    mid = [((o[0] * 2 + i[0]) / 3, (o[1] * 2 + i[1]) / 3) for o, i in zip(outer, inner)]
    d.polygon(outer + mid[::-1], fill=(255, 250, 225, 255)); d.line(outer, fill=(26, 20, 40, 255), width=1)
    return im
for an, idxs in anims.items():
    idxs = sorted(idxs); frames = []
    for i in idxs:
        fr = toon(f"{FR}/{an}_{i}_lit.png", f"{FR}/{an}_{i}_alb.png")
        if i in SMEAR.get(an, []) and i > 0:
            pe, ce = twig_ends(f"{FR}/{an}_{i-1}_alb.png"), twig_ends(f"{FR}/{an}_{i}_alb.png")
            if pe and ce:
                sm = smear(fr.size, pe[0], ce[0], ce[1]); sm.alpha_composite(fr); fr = sm
        if i in FLASH.get(an, []):
            arr = np.asarray(fr).astype(float); body = arr[..., 3] > 0
            inkm = (np.abs(arr[..., :3] - INK).sum(-1) < 10)
            arr[..., :3] = np.where((body & ~inkm)[..., None], arr[..., :3] * 0.35 + 255 * 0.65, arr[..., :3]); fr = Image.fromarray(arr.astype(np.uint8), "RGBA")
        frames.append(fr)
    cw, ch = frames[0].size
    sheet = Image.new("RGBA", (cw * len(frames), ch)); [sheet.paste(fr, (cw * k, 0)) for k, fr in enumerate(frames)]
    sheet.save(f"{OUT}/{PREFIX}{an}_sheet.png")
    gif = []
    for fr in frames:
        base = stage(cw * 2, ch * 2); base.alpha_composite(fr.resize((cw * 2, ch * 2), Image.NEAREST)); gif.append(base.convert("RGB"))
    hold = [83] * len(gif)
    if an in ("strike", "strike2", "strike3"): hold[-1] = 250
    gif[0].save(f"{OUT}/{PREFIX}{an}.gif", save_all=True, append_images=gif[1:], duration=hold, loop=0)
    print(an, len(frames), sheet.size)
