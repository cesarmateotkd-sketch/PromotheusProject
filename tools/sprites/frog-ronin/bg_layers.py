"""Golden-hour HD-2D pond backdrop for the game, as parallax layers at 2x (drawn at half size).
Game layout (logical px): sky 0-300, water 300-366, bank 366-460, ground line 432.
Run: python3 bg_layers.py OUTDIR"""
import sys, os, math, random
from PIL import Image, ImageDraw, ImageFilter
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
S = 2; TW = 720 * S // 2 * 2   # tile width 1440 (2 screens) for the scrolling layers
rng = random.Random(11)
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def glow(img, xy, r, color, alpha):
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r], fill=(*color, alpha))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * 0.6)))
def wrap_draw(d, fn, x, *a):  # draw a shape at x and its wrapped copies so the tile loops
    for off in (-TW, 0, TW): fn(d, x + off, *a)
# sky (static), 720 x 600
sky = Image.new("RGBA", (360 * S, 300 * S)); d = ImageDraw.Draw(sky)
STOPS = [(0, (96, 150, 214)), (220, (150, 196, 226)), (470, (255, 214, 160)), (600, (255, 178, 122))]
for y in range(300 * S):
    for (y0, c0), (y1, c1) in zip(STOPS, STOPS[1:]):
        if y0 <= y <= y1: c = lerp(c0, c1, (y - y0) / (y1 - y0)); break
    d.line([(0, y), (360 * S, y)], fill=(*c, 255))
glow(sky, (500, 560), 200, (255, 236, 180), 150); glow(sky, (500, 560), 60, (255, 250, 220), 230)
cl = Image.new("RGBA", sky.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(cl)
for cx, cy, w in ((110, 150, 200), (470, 90, 240), (640, 260, 170), (250, 330, 140)):
    for k in range(6):
        r = w * (0.18 + 0.08 * (k % 3)); x = cx - w / 2 + k * w / 5
        dc.ellipse([x - r, cy - r * 0.55, x + r, cy + r * 0.45], fill=(255, 238, 226, 200))
sky.alpha_composite(cl.filter(ImageFilter.GaussianBlur(4))); sky.save(f"{OUT}/bg_sky.png")
# far layer: hazy pines, nearer pines, shrine gate and far bank (scroll 0.2), 1440 x 600
far = Image.new("RGBA", (TW, 300 * S), (0, 0, 0, 0))
def pine(d, x, base, h, col):
    w = h * 0.42; d.rectangle([x - 3, base - h * 0.25, x + 3, base], fill=col)
    for k in range(4):
        ty = base - h + k * h * 0.2; bw = w * (0.35 + k * 0.2)
        d.polygon([(x, ty), (x - bw / 2, ty + h * 0.3), (x + bw / 2, ty + h * 0.3)], fill=col)
for col, base, hmin, hmax, step, blur in (((150, 170, 160, 255), 596, 150, 240, 28, 6), ((92, 132, 104, 255), 600, 90, 170, 40, 3)):
    l = Image.new("RGBA", far.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(l); x = 0
    while x < TW:
        h = rng.randint(hmin, hmax); wrap_draw(dl, pine, x, base, h, col); x += rng.randint(step, step * 2)
    far.alpha_composite(l.filter(ImageFilter.GaussianBlur(blur)))
l = Image.new("RGBA", far.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(l)
def torii(d, x0, y0):
    red = (212, 70, 60, 255)
    d.rectangle([x0, y0, x0 + 9, y0 + 100], fill=red); d.rectangle([x0 + 70, y0, x0 + 79, y0 + 100], fill=red)
    d.polygon([(x0 - 22, y0 - 8), (x0 + 101, y0 - 8), (x0 + 108, y0 - 20), (x0 - 29, y0 - 20)], fill=(226, 80, 66, 255))
    d.rectangle([x0 - 8, y0 + 12, x0 + 87, y0 + 19], fill=red)
wrap_draw(dl, torii, 180, 492); wrap_draw(dl, torii, 1000, 500)
for i in range(0, TW, 6): dl.rectangle([i, 588 + int(6 * math.sin(i * 2 * math.pi / TW * 9)), i + 6, 600], fill=(84, 126, 92, 255))
far.alpha_composite(l.filter(ImageFilter.GaussianBlur(1.5))); far.save(f"{OUT}/bg_far.png")
# water (scroll 0.5), 1440 x 132
wat = Image.new("RGBA", (TW, 66 * S), (64, 168, 176, 255)); dw = ImageDraw.Draw(wat)
for i in range(90):
    y = rng.randint(4, 66 * S - 6); x = rng.randint(0, TW); ln = rng.randint(20, 90)
    wrap_draw(dw, lambda d, x, y, ln, a: d.line([(x, y), (x + ln, y)], fill=(150, 220, 214, a), width=2), x, y, ln, rng.randint(80, 160))
for lx in range(60, TW, 260):
    ly = rng.randint(40, 100)
    wrap_draw(dw, lambda d, x, y: (d.ellipse([x - 34, y - 9, x + 34, y + 9], fill=(86, 170, 74, 255)), d.pieslice([x - 34, y - 9, x + 34, y + 9], 300, 330, fill=(64, 168, 176, 255))), lx, ly)
    if rng.random() < 0.5: dw.ellipse([lx - 6, ly - 12, lx + 6, ly - 2], fill=(255, 170, 200, 255))
wat = wat.filter(ImageFilter.GaussianBlur(1.0)); wat.save(f"{OUT}/bg_water.png")
# bank and path (scroll 1.0), 1440 x 188; ground line 432 -> row (432-366)*2 = 132
gnd = Image.new("RGBA", (TW, 94 * S), (196, 160, 110, 255)); dg = ImageDraw.Draw(gnd)
dg.rectangle([0, 0, TW, 26], fill=(118, 170, 72, 255))
for i in range(0, TW, 3): dg.rectangle([i, 26, i + 3, 30 + (i * 7) % 5], fill=(96, 148, 60, 255))
for i in range(200):
    x = rng.randint(0, TW); y = rng.randint(40, 94 * S - 6); r = rng.randint(2, 7)
    wrap_draw(dg, lambda d, x, y, r, c: d.ellipse([x - r, y - r // 2, x + r, y + r // 2], fill=c), x, y, r, (222, 192, 142, 255) if i % 3 else (160, 126, 86, 255))
for i in range(90):
    x = rng.randint(0, TW)
    for k in range(3):
        dx, h = rng.randint(-6, 6), rng.randint(8, 18)
        wrap_draw(dg, lambda d, x, dx, h: d.line([(x, 24), (x + dx, 24 - h)], fill=(132, 196, 80, 255), width=2), x, dx, h)
for i in range(22):
    x = rng.randint(0, TW); c = (255, 230, 120, 255) if i % 2 else (255, 255, 255, 255)
    wrap_draw(dg, lambda d, x, c: d.ellipse([x - 4, 14, x + 4, 22], fill=c), x, c)
gnd.save(f"{OUT}/bg_ground.png")
print("ok", sky.size, far.size, wat.size, gnd.size)
