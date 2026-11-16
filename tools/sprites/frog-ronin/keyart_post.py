"""Frog Ronin v2 key art: toon-finish the Blender passes two ways and composite both
over one HD-2D pond backdrop. Output: keyart_pixel.png, keyart_smooth.png, compare.png"""
import sys, re, colorsys, math, random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
OUT = sys.argv[1]; R = "out"
src = open("build.py").read()
BASE = {k: tuple(map(int, v.split(","))) for k, v in re.findall(r'"(\w+)": \((\d+, \d+, \d+)\)', src.split("mats = {}")[0])}
NAMES = list(BASE); PAL = np.array([BASE[n] for n in NAMES], float)
INK = np.array([26, 20, 40], float)  # near-black, violet-biased (style guide outline)

def ramp(c):
    """4 tones per base colour: deep shadow, shadow, mid, highlight (hue-shifted)."""
    h, s, v = colorsys.rgb_to_hsv(*(np.array(c) / 255))
    def shift(h, to, amt):
        d = ((to - h + 0.5) % 1) - 0.5; return (h + d * amt) % 1
    tones = [(shift(h, 0.68, 0.16), min(1, s * 1.15 + 0.05), v * 0.48),
             (shift(h, 0.68, 0.08), min(1, s * 1.08), v * 0.72), (h, s, v),
             (shift(h, 0.14, 0.08), s * 0.8, min(1, v * 1.12 + 0.04))]
    if NAMES[[tuple(p) for p in PAL.tolist()].index(tuple(map(float, c)))] in ("eyew", "hilite"):
        tones = [(0.68, 0.18, 0.72), (0.66, 0.08, 0.86), (h, s, v), (h, s, 1.0)]
    return np.array([colorsys.hsv_to_rgb(*t) for t in tones]) * 255
RAMPS = np.array([ramp(c) for c in PAL.astype(int)])  # (n,4,3)

def load(tag):
    lit = np.asarray(Image.open(f"{R}/lit_{tag}.png").convert("RGBA"), float) / 255
    alb = np.asarray(Image.open(f"{R}/alb_{tag}.png").convert("RGBA"), float)
    a = alb[..., 3] > 127
    d = ((alb[..., None, :3] - PAL[None, None]) ** 2).sum(-1); idx = d.argmin(-1)
    L = lit[..., :3].mean(-1)
    return L, idx, a, lit[..., 3]

def toon(tag, smooth):
    L, idx, a, la = load(tag)
    th = [0.2, 0.42, 0.78]
    if smooth:  # soft-edged bands (cel with a little anti-aliasing)
        w = 0.035; t = sum(np.clip((L - x) / w + 0.5, 0, 1) for x in th)
        lo = np.floor(np.clip(t, 0, 2.999)).astype(int); f = (t - lo)[..., None]
        c0 = RAMPS[idx, lo]; c1 = RAMPS[idx, np.minimum(lo + 1, 3)]; col = c0 * (1 - f) + c1 * f
    else:
        band = sum((L > x).astype(int) for x in th); col = RAMPS[idx, band]
    H, W = idx.shape
    # ink: material boundaries (darker side) and silhouette
    diff = np.zeros((H, W), bool)
    for dy, dx in ((0, 1), (1, 0)):
        n = np.roll(idx, (-dy, -dx), (0, 1)); na = np.roll(a, (-dy, -dx), (0, 1))
        e = (n != idx) & a & na
        lum = PAL[idx].sum(-1); nl = PAL[n].sum(-1)
        diff |= e & (lum <= nl)
        diff |= np.roll(e & (nl < lum), (dy, dx), (0, 1))
    if smooth:
        dimg = Image.fromarray((diff * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
        diff = np.asarray(dimg) > 127
        inner = np.clip(RAMPS[idx, 0] * 0.55, 0, 255)
        col = np.where(diff[..., None], inner, col)
        al = Image.fromarray((a * 255).astype(np.uint8))
        out_line = np.asarray(al.filter(ImageFilter.MaxFilter(9))) > 127
        rgba = np.zeros((H, W, 4)); rgba[..., :3] = np.where(a[..., None], col, INK); rgba[..., 3] = (a | out_line) * 255
        im = Image.fromarray(rgba.astype(np.uint8), "RGBA")
        return im.resize((W // 2, H // 2), Image.LANCZOS)
    inner = RAMPS[idx, 0] * 0.7
    col = np.where(diff[..., None], inner, col)
    out_line = np.zeros_like(a)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        out_line |= np.roll(a, (dy, dx), (0, 1))
    out_line &= ~a
    rgba = np.zeros((H, W, 4)); rgba[..., :3] = np.where(a[..., None], col, INK); rgba[..., 3] = (a | out_line) * 255
    im = Image.fromarray(rgba.astype(np.uint8), "RGBA")
    return im.resize((W * 2, H * 2), Image.NEAREST)

# ---------------- HD-2D backdrop, golden hour, 720x1280 (2x the phone frame) ----
W, H = 720, 1280; GROUND = 830
rng = random.Random(7)
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))
def glow(img, xy, r, color, alpha):
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    d.ellipse([xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r], fill=(*color, alpha))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * 0.6)))
def layer(fn, blur):
    l = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(l)); return l.filter(ImageFilter.GaussianBlur(blur)) if blur else l
bg = Image.new("RGB", (W, H)); px = ImageDraw.Draw(bg)
SKY = [(0, (96, 150, 214)), (380, (150, 196, 226)), (600, (255, 214, 160)), (705, (255, 176, 120))]
for y in range(H):
    for (y0, c0), (y1, c1) in zip(SKY, SKY[1:]):
        if y0 <= y <= y1: c = lerp(c0, c1, (y - y0) / (y1 - y0)); break
    else: c = SKY[-1][1]
    px.line([(0, y), (W, y)], fill=c)
bg = bg.convert("RGBA")
glow(bg, (520, 640), 230, (255, 236, 180), 150); glow(bg, (520, 640), 70, (255, 250, 220), 230)  # low sun
def clouds(d):
    for cx, cy, w in ((120, 300, 200), (470, 220, 260), (640, 420, 180), (260, 470, 150)):
        for k in range(6):
            r = w * (0.18 + 0.08 * (k % 3)); x = cx - w / 2 + k * w / 5
            d.ellipse([x - r, cy - r * 0.55, x + r, cy + r * 0.45], fill=(255, 238, 226, 200))
bg.alpha_composite(layer(clouds, 4))
def pines(col, base, hmin, hmax, step):
    def f(d):
        x = -30
        while x < W + 40:
            h = rng.randint(hmin, hmax); w = h * 0.42
            d.rectangle([x - 3, base - h * 0.25, x + 3, base], fill=col)
            for k in range(4):
                ty = base - h + k * h * 0.2; bw = w * (0.35 + k * 0.2)
                d.polygon([(x, ty), (x - bw / 2, ty + h * 0.3), (x + bw / 2, ty + h * 0.3)], fill=col)
            x += rng.randint(step, step * 2)
    return f
bg.alpha_composite(layer(pines((150, 170, 160, 255), 705, 150, 240, 28), 6))   # hazy far pines
bg.alpha_composite(layer(pines((92, 132, 104, 255), 712, 90, 170, 40), 3))     # nearer pines
def torii(d):
    x0, y0 = 120, 600; red = (212, 70, 60, 255)
    d.rectangle([x0, y0, x0 + 9, y0 + 105], fill=red); d.rectangle([x0 + 70, y0, x0 + 79, y0 + 105], fill=red)
    d.polygon([(x0 - 22, y0 - 8), (x0 + 101, y0 - 8), (x0 + 108, y0 - 20), (x0 - 29, y0 - 20)], fill=(226, 80, 66, 255))
    d.rectangle([x0 - 8, y0 + 12, x0 + 87, y0 + 19], fill=red)
    for i in range(-60, W + 60, 6): d.rectangle([i, 696 + int(6 * math.sin(i / 40)), i + 6, 720], fill=(84, 126, 92, 255))
bg.alpha_composite(layer(torii, 2))
def water(d):
    d.rectangle([0, 715, W, GROUND - 10], fill=(64, 168, 176, 255))
    for i in range(70):
        y = rng.randint(720, GROUND - 20); x = rng.randint(-40, W); l = rng.randint(20, 90)
        d.line([(x, y), (x + l, y)], fill=(150, 220, 214, rng.randint(80, 160)), width=2)
    for y in range(722, GROUND - 14, 5):
        w = rng.randint(8, 34); d.line([(520 - w, y), (520 + w, y)], fill=(255, 226, 150, 170), width=2)  # sun road
    for lx, ly in ((90, 760), (250, 790), (440, 750), (630, 785)):
        d.ellipse([lx - 34, ly - 9, lx + 34, ly + 9], fill=(86, 170, 74, 255)); d.pieslice([lx - 34, ly - 9, lx + 34, ly + 9], 300, 330, fill=(64, 168, 176, 255))
        if lx in (250, 630): d.ellipse([lx - 6, ly - 12, lx + 6, ly - 2], fill=(255, 170, 200, 255))  # lotus
bg.alpha_composite(layer(water, 1.2))
def bank(d):
    d.polygon([(0, GROUND - 30), (W, GROUND - 22), (W, H), (0, H)], fill=(118, 170, 72, 255))
    d.rectangle([0, GROUND - 8, W, H], fill=(196, 160, 110, 255))
    for i in range(140):
        x = rng.randint(0, W); y = rng.randint(GROUND, H - 300); r = rng.randint(2, 7)
        d.ellipse([x - r, y - r // 2, x + r, y + r // 2], fill=(222, 192, 142, 255) if i % 3 else (160, 126, 86, 255))
    for i in range(60):
        x = rng.randint(0, W); y = GROUND - 22 + rng.randint(-6, 10)
        for k in range(3): d.line([(x, y), (x + rng.randint(-6, 6), y - rng.randint(8, 18))], fill=(132, 196, 80, 255), width=2)
    for i in range(14):
        x = rng.randint(0, W); y = GROUND - 26 + rng.randint(-4, 6)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 230, 120, 255) if i % 2 else (255, 255, 255, 255))  # wildflowers
bg.alpha_composite(layer(bank, 0))
BG = bg

def foreground(img):
    def reeds(d):
        for i in range(9):
            x = rng.choice([rng.randint(-30, 120), rng.randint(600, 760)]); top = rng.randint(820, 920)
            d.line([(x, H - 300), (x + rng.randint(-30, 30), top)], fill=(70, 120, 60, 255), width=rng.randint(10, 16))
            d.ellipse([x - 8, top - 30, x + 8, top + 10], fill=(150, 100, 60, 255))
    img.alpha_composite(layer(reeds, 9))
    for i in range(18):  # floating pollen in the sun
        x, y = rng.randint(20, W - 20), rng.randint(450, 900); glow(img, (x, y), 7, (255, 240, 170), 140)
        ImageDraw.Draw(img).rectangle([x - 2, y - 2, x + 1, y + 1], fill=(255, 252, 230))

def pixel_fx(top):
    """Hit effects drawn at 1x (360x640) and scaled 2x nearest, so they match the pixel sprites."""
    fx = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0)); d = ImageDraw.Draw(fx)
    sx, sy, ex, ey = [v / 2 for v in SLASH]
    outer, inner = [], []
    for i in range(29):  # bold crescent slash trail, thick in the middle
        t = i / 28; bul = math.sin(t * math.pi)
        bx, by = sx + (ex - sx) * t, sy + (ey - sy) * t
        outer.append((bx + 0.8 * bul * 34, by - 0.6 * bul * 34)); inner.append((bx + 0.8 * (bul * 34 - 2 - 11 * bul), by - 0.6 * (bul * 34 - 2 - 11 * bul)))
    d.polygon(outer + inner[::-1], fill=(255, 196, 64, 255))
    mid = [((o[0] + i[0]) / 2 + 1, (o[1] + i[1]) / 2 - 1) for o, i in zip(outer, inner)]
    d.polygon(outer + mid[::-1], fill=(255, 250, 220, 255)); d.line(outer, fill=(255, 255, 255, 255), width=1)
    for k in range(5):  # speed lines
        y = sy + 6 + k * 9; d.line([(sx - 40 + k * 3, y), (sx - 14 + k * 3, y)], fill=(255, 255, 255, 200), width=1)
    cx, cy = [v / 2 for v in SPARK]
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=(255, 240, 180, 255), width=2)  # impact ring
    for k in range(8):
        a = k * math.pi / 4 + 0.39; l = 22 if k % 2 == 0 else 12
        d.polygon([(cx + math.cos(a - 0.35) * 3, cy + math.sin(a - 0.35) * 3), (cx + math.cos(a) * l, cy + math.sin(a) * l), (cx + math.cos(a + 0.35) * 3, cy + math.sin(a + 0.35) * 3)], fill=(255, 255, 240, 255))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
    for k in range(7):  # shell chips
        a = rng.uniform(-0.9, 0.6); r = rng.uniform(14, 28)
        x, y = cx + math.cos(a) * r + 6, cy + math.sin(a) * r
        d.polygon([(x, y), (x + 3, y + 1), (x + 1, y + 3)], fill=(110, 170, 240, 255), outline=(26, 20, 40, 255))
    try: font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
    except Exception: font = None
    d.fontmode = "1"; nx, ny = cx + 6, cy - 46
    for ox in (-2, -1, 0, 1, 2):
        for oy in (-2, -1, 0, 1, 2): d.text((nx + ox, ny + oy), "24", font=font, fill=(26, 20, 40, 255))
    d.text((nx, ny), "24", font=font, fill=(255, 236, 90, 255)); d.text((nx, ny), "24", font=font, fill=(255, 236, 90, 255))
    return fx.resize((W, H), Image.NEAREST)

def compose(chars, label):
    img = BG.copy(); top = GROUND + 12 - FEET
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    for cx, rw in SHADOWS: d.ellipse([cx - rw, GROUND + 2, cx + rw, GROUND + 26], fill=(90, 60, 40, 130))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    img.alpha_composite(chars, (0, top))
    glow(img, SPARK, 46, (255, 240, 180), 200)
    img.alpha_composite(pixel_fx(top))
    foreground(img)
    v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-260, -200, W + 260, H + 200], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (60, 36, 40, 255)), v.filter(ImageFilter.GaussianBlur(140)))
    img = img.crop(CROP); img.convert("RGB").save(f"{OUT}/keyart_{label}.png"); return img

from PIL import ImageFont
CROP = (0, 190, 720, 976)
FEET, SHADOWS, SLASH, SPARK = 340, ((205, 110), (540, 150)), (350, 650, 405, 750), (380, 700)
v2 = compose(toon("x1", False), "v2")
v1 = Image.open(f"{OUT}/keyart_pixel.png")
CW, CH = v2.size
cmp = Image.new("RGB", (CW * 2 + 24, CH + 70), (14, 12, 24)); cmp.paste(v1, (0, 70)); cmp.paste(v2.convert("RGB"), (CW + 24, 70))
d = ImageDraw.Draw(cmp); f = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
d.text((20, 18), "Before (review 1)", fill=(239, 227, 156), font=f); d.text((CW + 44, 18), "After: v2", fill=(239, 227, 156), font=f)
cmp.save(f"{OUT}/compare_v2.png")
