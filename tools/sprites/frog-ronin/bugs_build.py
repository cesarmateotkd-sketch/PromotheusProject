"""Blender: the bug clan (beetle, mosquito, spitter, mantis, hornet), each with idle, attack, hurt.
Run: blender -b --factory-startup --python bugs_build.py -- OUTDIR [bug,bug]
Writes OUTDIR/<bug>_<anim>_<i>_lit.png / _alb.png at 1x and OUTDIR/<bug>_meta.json (ground row)."""
import os, json
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "common.py")).read())
import math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
args = sys.argv[sys.argv.index("--") + 1:]
BUGS = args[1].split(",") if len(args) > 1 else ["beetle", "mosquito", "spitter", "mantis", "hornet"]

def cone(n, r1, r2, depth, mat, loc, rot=(0, 0, 0), scale=(1, 1, 1), v=20):
    """Cone standing on its base (radius r1 at z=0 local, r2 at the top)."""
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=v, radius1=r1, radius2=r2, depth=depth)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, depth / 2))
    me = bpy.data.meshes.new(n); bm.to_mesh(me); bm.free()
    return place(bpy.data.objects.new(n, me), mat, loc, rot, scale, 0)
def box(n, size, mat, loc, rot=(0, 0, 0)):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    me = bpy.data.meshes.new(n); bm.to_mesh(me); bm.free()
    return place(bpy.data.objects.new(n, me), mat, loc, rot, (1, 1, 1), 0)
def V(*a): return Vector(a)
def rotY(v, a, piv=V(0, 0, 0)):
    d = v - piv; return piv + V(d.x * math.cos(a) + d.z * math.sin(a), d.y, -d.x * math.sin(a) + d.z * math.cos(a))

# ---------------- BEETLE: ashigaru with jingasa hat and clan banner (faces -X) -------------
def beetle(P):
    S = 0.82
    def b(n, r, m, l, sc=(1, 1, 1), rot=(0, 0, 0), sub=1): return ball(n, r * S, m, tuple(V(*l) * S), sc, rot, sub)
    def g(n, a, c, r1, r2, m, sub=0, v=8): return seg(n, V(*a) * S, V(*c) * S, r1 * S, r2 * S, m, sub, v)
    b("shellL", 0.58, "shell", (0.18, -0.035, 0.62), (1.3, 0.95, 0.82)); b("shellR", 0.58, "shellb", (0.18, 0.035, 0.62), (1.3, 0.95, 0.82))
    b("under", 0.5, "shelld", (0.15, 0, 0.42), (1.25, 0.9, 0.5)); b("pron", 0.36, "shelld", (-0.5, 0, 0.62), (0.9, 1.0, 0.8))
    hz = 0.5 + P["head"]
    b("bhead", 0.24, "bhead", (-0.85, 0, hz))
    g("horn1", (-0.98, 0, hz + 0.1), (-1.22, 0, hz + 0.38), 0.08, 0.045, "horn", sub=1); g("horn2", (-1.22, 0, hz + 0.38), (-1.24, 0, hz + 0.58), 0.045, 0.008, "horn", sub=1)
    for s in (-1, 1):
        b(f"beye{s}", 0.06, "redeye" if P["angry"] else "beye", (-1.0, 0.14 * s, hz + 0.07))
        g(f"brow{s}", (-0.96, 0.2 * s, hz + 0.18), (-1.05, 0.06 * s, hz + 0.12), 0.03, 0.025, "lacq")
        g(f"mand{s}", (-1.02, 0.09 * s, hz - 0.1), (-1.2, 0.03 * s, hz - 0.18), 0.035, 0.01, "bleg")
        for i, lx in enumerate((-0.45, 0.0, 0.45)):
            ph = P["step"] + i * 2.1 + (0 if s > 0 else math.pi)
            hip = V(lx, 0.4 * s, 0.38); knee = hip + V(lx * 0.3 - 0.05 + 0.06 * math.sin(ph), 0.28 * s, 0.12 + 0.04 * max(0, math.cos(ph)))
            foot = V(knee.x + lx * 0.25 + 0.08 * math.sin(ph), knee.y + 0.12 * s, 0.02 / S)
            g(f"bl{s}{i}a", hip, knee, 0.05, 0.04, "bleg"); g(f"bl{s}{i}b", knee, foot, 0.04, 0.018, "bleg")
    # jingasa: shallow lacquered cone hat with the clan's gold mon
    cone("hat", 0.46 * S, 0.03 * S, 0.18 * S, "lacq", tuple(V(-0.84, 0, hz + 0.16) * S), rot=(0, -0.2, 0))
    b("mon", 0.07, "gold", (-1.13, 0, hz + 0.24), (0.4, 1, 1))
    # sashimono banner on the back, fluttering
    g("pole", (0.35, 0, 0.95), (0.42, 0, 2.05), 0.025, 0.02, "lacq", v=6)
    fl = P["flag"]
    for k in range(4):  # banner as 4 vertical strips so it can wave
        x0 = 0.42 + k * 0.13; wv = 0.06 * math.sin(fl + k * 0.9) * k / 3
        box(f"flag{k}", (0.13 * S, 0.02 * S, 0.5 * S), "clan", tuple(V(x0 + 0.065, wv, 1.75 - k * 0.02) * S))
    box("flagmon", (0.13 * S, 0.03 * S, 0.13 * S), "gold", tuple(V(0.61, -0.025, 1.74) * S), rot=(0, 0.785, 0))
    box("flagtrim", (0.54 * S, 0.025 * S, 0.04 * S), "gold", tuple(V(0.68, -0.02, 1.98) * S))

# ---------------- MOSQUITO: ninja, hovering ---------------------------------------------------
def mosquito(P):
    z0 = 1.0 + P["hover"]
    ball("thorax", 0.17, "mosq", (0, 0, z0), (1.1, 0.95, 1.0))
    seg("abd", (0.12, 0, z0 - 0.02), (0.62, 0, z0 + 0.18 + P["abd"]), 0.15, 0.05, "mosqd", sub=1)
    for k in range(3): torus(f"ring{k}", 0.12 - k * 0.03, 0.012, "mosq", (0.25 + k * 0.13, 0, z0 + 0.03 + k * 0.05 + P["abd"] * k / 3), rot=(0, 1.2, 0))
    hx = -0.2
    ball("head", 0.14, "hood", (hx, 0, z0 + 0.06))
    ball("mask", 0.145, "mosq", (hx - 0.04, 0, z0 + 0.02), (0.9, 1.0, 0.45))     # bare face band between hood and veil
    for s in (-1, 1):
        ball(f"eye{s}", 0.075, "redeye", (hx - 0.08, 0.075 * s, z0 + 0.07), (0.8, 1, 0.7))
        ball(f"ehi{s}", 0.022, "hilite", (hx - 0.14, 0.075 * s - 0.02, z0 + 0.1), sub=0)
    seg("hoodtail", (hx + 0.1, 0, z0 + 0.12), (hx + 0.38, 0.02, z0 + 0.22 + 0.04 * math.sin(P["wing"])), 0.05, 0.015, "hood")
    a = math.radians(P["needle"]); tip = V(hx - 0.1, 0, z0 - 0.02) + V(-math.cos(a), 0, -math.sin(a)) * (0.55 + P["reach"])
    seg("needle", (hx - 0.1, 0, z0 - 0.02), tip, 0.025, 0.006, "needle", sub=0, v=6)
    for s in (-1, 1):
        for i, lx in enumerate((-0.08, 0.02, 0.12)):
            spread = (-0.22, 0.0, 0.26)[i]
            k = V(lx + spread * 0.6, 0.2 * s, z0 - 0.2); f = V(lx + spread * 1.6, 0.3 * s, z0 - 0.55 + 0.04 * math.sin(P["wing"] + i))
            seg(f"l{s}{i}a", (lx, 0.08 * s, z0 - 0.08), k, 0.018, 0.014, "mosqd", sub=0, v=6); seg(f"l{s}{i}b", k, f, 0.014, 0.006, "mosqd", sub=0, v=6)
        w = P["wing"]; ang = 0.5 + 0.55 * math.sin(w)
        ball(f"wing{s}", 0.3, "wing", (0.18, 0.2 * s + 0.12 * s * math.cos(ang), z0 + 0.2 + 0.18 * math.sin(ang)), (1.1, 0.05, 0.42), rot=(ang * s * 1.2, 0.35, 0))

# ---------------- SPITTER: teppo gunner with straw kasa and bamboo tube -----------------------
def spitter(P):
    sq = P["sq"]; pf = P["puff"]
    ball("body", 0.42, "spit", (0.12, 0, 0.5 * sq), (1.15, 1.0, 0.95 * sq))
    ball("belly", 0.36, "spitb", (0.02, 0, 0.42 * sq), (1.0, 0.95, 0.75 * sq))
    hz = 0.62 * sq
    ball("head", 0.24, "spit", (-0.32, 0, hz))
    for s in (-1, 1):
        ball(f"cheek{s}", 0.13 * (1 + pf), "spitb", (-0.4, 0.15 * s, hz - 0.08))
        ball(f"eye{s}", 0.07, "eyew", (-0.48, 0.1 * s, hz + 0.1))
        ball(f"pup{s}", 0.04, "pupil", (-0.53, 0.1 * s, hz + 0.1))
        g = (-1, 1)
        for i, lx in enumerate((-0.1, 0.15, 0.4)):
            seg(f"l{s}{i}", (lx, 0.3 * s, 0.3 * sq), (lx - 0.06, 0.42 * s, 0.02), 0.045, 0.03, "spitb", sub=0, v=6)
    tb = V(-0.5, 0, hz - 0.06); a = math.radians(P["aim"])
    seg("tube", tb, tb + V(-math.cos(a), 0, math.sin(a)) * 0.42, 0.06, 0.06, "bamboo", sub=0, v=10)
    for k in (0.12, 0.3): torus(f"node{k}", 0.065, 0.015, "leaf", tuple(tb + V(-math.cos(a), 0, math.sin(a)) * k), rot=(0, 1.5708 - a, 0))
    cone("kasa", 0.42, 0.02, 0.2, "straw", (-0.3, 0, hz + 0.16), rot=(0, -0.2, 0))
    torus("kasaband", 0.17, 0.02, "clan", (-0.31, 0, hz + 0.2), rot=(0, -0.2, 0))

# ---------------- MANTIS: orchid-pink ronin mini-boss -----------------------------------------
def mantis(P):
    ball("abd", 0.4, "mant", (0.45, 0, 0.62), (1.45, 0.9, 0.8), rot=(0, -0.3, 0))
    for k in range(3): ball(f"petal{k}", 0.16, "mantl", (0.2 + k * 0.22, 0, 0.5 - k * 0.03), (1.0, 1.3, 0.25))
    tz = 0.62; top = V(-0.12, 0, 1.0 + P["rise"])
    seg("thorax", (0.1, 0, tz + 0.1), top, 0.17, 0.12, "mant", sub=1)
    hc = top + V(-0.08, 0, 0.16)
    ball("head", 0.26, "mant", tuple(hc), (0.9, 1.25, 0.82))
    for s in (-1, 1):
        ball(f"eye{s}", 0.14, "mantl", tuple(hc + V(-0.05, 0.25 * s, 0.06)))
        ball(f"pup{s}", 0.07, "pupil", tuple(hc + V(-0.16, 0.25 * s, 0.06)))
        seg(f"ant{s}", hc + V(-0.05, 0.06 * s, 0.12), hc + V(-0.35, 0.2 * s, 0.5), 0.012, 0.004, "mantd", sub=0, v=5)
    cone("kasa", 0.44, 0.02, 0.18, "straw", tuple(hc + V(0.02, 0, 0.13)), rot=(0, 0.2, 0))
    for k in range(5):  # torn brim
        a = k * 1.25; ball(f"tear{k}", 0.06, "straw", tuple(hc + V(0.02 + 0.41 * math.cos(a), 0.41 * math.sin(a), 0.11)), (1, 1, 0.3), sub=0)
    # raptorial arms: shoulder -> elbow -> blade, angles per pose
    for s, (ua, ba) in ((-1, P["armN"]), (1, P["armF"])):
        sh = top + V(0.02, 0.12 * s, -0.12)
        el = sh + V(-math.cos(math.radians(ua)), 0.06 * s, math.sin(math.radians(ua))) * 0.42
        bt = el + V(-math.cos(math.radians(ba)), 0.02 * s, math.sin(math.radians(ba))) * 0.62
        seg(f"uarm{s}", sh, el, 0.075, 0.065, "mant", sub=0); ball(f"elb{s}", 0.06, "mant", tuple(el), sub=0)
        seg(f"blade{s}", el, bt, 0.055, 0.008, "blade", sub=0, v=4)
        ball(f"guard{s}", 0.05, "gold", tuple(el), (1, 1.4, 0.5), sub=0)
    for s in (-1, 1):
        for i, lx in enumerate((0.15, 0.45)):
            k = V(lx - 0.05, 0.3 * s, 0.6); f = V(lx - 0.1 + i * 0.25, 0.4 * s, 0.02)
            seg(f"l{s}{i}a", (lx, 0.08 * s, 0.6), k, 0.035, 0.03, "mantd", sub=0, v=6); seg(f"l{s}{i}b", k, f, 0.03, 0.012, "mantd", sub=0, v=6)

# ---------------- HORNET SHOGUN: armoured warlord ---------------------------------------------
def hornet(P):
    z = P["hover"]
    # striped abdomen with stinger, behind
    for k in range(4):
        ball(f"ab{k}", 0.38 - k * 0.06, "hyel" if k % 2 == 0 else "hblk", (0.45 + k * 0.2, 0, 1.15 + z - k * 0.12), (1.0, 0.95, 0.9))
    seg("sting", (1.1, 0, 0.75 + z), (1.35, 0, 0.5 + z), 0.07, 0.005, "hblk", sub=0)
    # cape
    ball("cape", 0.55, "cape", (0.25, 0, 1.45 + z), (0.45, 1.15, 1.25), rot=(0, 0.25 + 0.05 * math.sin(P["wing"]), 0))
    # thorax in lacquered do armour with gold trim
    ball("thorax", 0.36, "hyel", (0, 0, 1.6 + z), (0.95, 1.0, 1.05))
    ball("do", 0.38, "hblk", (-0.05, 0, 1.55 + z), (0.9, 1.05, 0.9))
    for k in range(3): torus(f"lame{k}", 0.34 - k * 0.02, 0.022, "gold", (-0.05, 0, 1.36 + z + k * 0.14), (0.95, 1.08, 1))
    ball("waist", 0.2, "hblk", (0.02, 0, 1.12 + z))
    for s in (-1, 1):
        ball(f"sode{s}", 0.2, "hblk", (0.0, 0.42 * s, 1.85 + z), (0.9, 0.4, 0.9), rot=(0.3 * s, 0, 0))
        ball(f"sodeg{s}", 0.2, "gold", (0.0, 0.43 * s, 1.78 + z), (0.92, 0.3, 0.45), rot=(0.3 * s, 0, 0))
    # head + kabuto
    hc = V(-0.1, 0, 2.18 + z + P["head"])
    ball("head", 0.26, "hyel", tuple(hc), (1.0, 1.05, 0.95))
    for s in (-1, 1):
        ball(f"eye{s}", 0.15, "heye", tuple(hc + V(-0.14, 0.15 * s, 0.0)), (0.8, 0.85, 1.25))
        ball(f"ehi{s}", 0.04, "hilite", tuple(hc + V(-0.26, 0.15 * s - 0.04, 0.08)), sub=0)
        seg(f"mand{s}", hc + V(-0.18, 0.08 * s, -0.16), hc + V(-0.32, 0.02 * s, -0.24), 0.04, 0.01, "hblk", sub=0)
        seg(f"brow{s}", hc + V(-0.22, 0.24 * s, 0.2), hc + V(-0.28, 0.06 * s, 0.13), 0.035, 0.03, "hblk", sub=0)
    ball("kabuto", 0.29, "hblk", tuple(hc + V(0.03, 0, 0.12)), (1.05, 1.08, 0.75))
    cone("shikoro", 0.44, 0.28, 0.16, "hblk", tuple(hc + V(0.06, 0, -0.04)))
    torus("hachi", 0.3, 0.025, "gold", tuple(hc + V(0.03, 0, 0.1)), (1.05, 1.08, 1))
    for s in (-1, 1):  # kuwagata crest
        a = hc + V(-0.24, 0.05 * s, 0.22); b = a + V(-0.12, 0.16 * s, 0.32); c = b + V(0.08, 0.1 * s, 0.24)
        seg(f"crest{s}", a, b, 0.04, 0.03, "gold", sub=0); seg(f"crestb{s}", b, c, 0.03, 0.01, "gold", sub=0)
    ball("maedate", 0.07, "gold", tuple(hc + V(-0.28, 0, 0.24)), (0.5, 1, 1))
    # arms with twin stinger blades
    for s, (ua, ba) in ((-1, P["armN"]), (1, P["armF"])):
        sh = V(-0.05, 0.4 * s, 1.75 + z); el = sh + V(-math.cos(math.radians(ua)), 0.08 * s, math.sin(math.radians(ua))) * 0.4
        hd = el + V(-math.cos(math.radians(ua - 40)), 0, math.sin(math.radians(ua - 40))) * 0.3
        seg(f"ua{s}", sh, el, 0.07, 0.06, "hblk", sub=0); seg(f"fa{s}", el, hd, 0.06, 0.05, "hyel", sub=0)
        bt = hd + V(-math.cos(math.radians(ba)), 0.02 * s, math.sin(math.radians(ba))) * 0.95
        seg(f"hilt{s}", hd - (bt - hd).normalized() * 0.14, hd, 0.035, 0.035, "clan", sub=0)
        seg(f"blade{s}", hd, bt, 0.06, 0.006, "blade", sub=0, v=4)
        ball(f"tsuba{s}", 0.07, "gold", tuple(hd), (1, 1, 0.35), sub=0)
    # legs and wings
    for s in (-1, 1):
        k = V(0.0, 0.2 * s, 0.62 + z * 0.5); f = V(-0.08, 0.26 * s, 0.03)
        seg(f"thigh{s}", (0.02, 0.14 * s, 1.08 + z), k, 0.08, 0.06, "hblk", sub=0); seg(f"shin{s}", k, f, 0.06, 0.03, "hyel", sub=0)
        ball(f"foot{s}", 0.07, "hblk", tuple(f + V(-0.05, 0, 0)), (1.6, 0.9, 0.5), sub=0)
        w = P["wing"]
        for j in range(2):
            ang = 0.6 + 0.5 * math.sin(w + j * 0.6)
            ball(f"wing{s}{j}", 0.5 - j * 0.12, "wing", (0.45 + j * 0.12, (0.25 + 0.2 * math.cos(ang)) * s, 2.0 + z + 0.25 * math.sin(ang) - j * 0.2), (1.2, 0.04, 0.38), rot=(ang * s, 0.5, 0))

# ---------------- poses -----------------------------------------------------------------------
TAU = 2 * math.pi
def C(**kw): return kw
POSES = {
 "beetle": dict(base=C(head=0.0, angry=0, step=0.0, flag=0.0, dx=0.0, dz=0.0, lean=0.0, sq=1.0, flash=0),
   idle=[C(step=0.0, flag=TAU * i / 6, sq=1.0 - 0.025 * (1 - math.cos(TAU * i / 6)) / 2) for i in range(6)],
   attack=[C(lean=0.12, dx=0.12, sq=0.92, angry=1, flag=0.5), C(lean=0.18, dx=0.2, sq=0.88, angry=1, head=-0.05, flag=1.0),
           C(lean=-0.22, dx=-0.42, sq=1.05, angry=1, head=-0.08, step=1.5, flag=1.8), C(lean=-0.28, dx=-0.55, sq=1.08, angry=1, head=-0.1, step=2.4, flag=2.6),
           C(lean=-0.08, dx=-0.3, sq=1.0, angry=1, step=3.2, flag=3.4), C(lean=0.0, dx=-0.05, angry=0, step=4.0, flag=4.2)],
   hurt=[C(lean=0.22, dx=0.15, sq=0.9, head=0.08, flag=1.0), C(lean=0.15, dx=0.2, sq=0.95, head=0.05, flag=2.0), C(lean=0.04, dx=0.08, flag=3.0)]),
 "mosquito": dict(base=C(hover=0.0, wing=0.0, abd=0.0, needle=20, reach=0.0, dx=0.0, dz=0.0, lean=0.0, sq=1.0),
   idle=[C(hover=0.05 * math.sin(TAU * i / 6), wing=TAU * i / 3, abd=0.04 * math.sin(TAU * i / 6)) for i in range(6)],
   attack=[C(wing=0.0, needle=5, dx=0.15, dz=0.08, lean=0.15), C(wing=2.1, needle=0, dx=0.25, dz=0.1, lean=0.2, abd=0.08),
           C(wing=4.2, needle=10, dx=-0.5, dz=-0.05, lean=-0.15, reach=0.2), C(wing=6.3, needle=12, dx=-0.6, dz=-0.08, lean=-0.18, reach=0.25),
           C(wing=8.4, needle=18, dx=-0.3, lean=-0.05, reach=0.1), C(wing=10.5, needle=20, dx=-0.05)],
   hurt=[C(wing=0.0, dx=0.2, dz=0.12, lean=0.35, needle=40), C(wing=1.5, dx=0.24, dz=0.05, lean=0.25, needle=35), C(wing=3.0, dx=0.1, lean=0.08, needle=25)]),
 "spitter": dict(base=C(sq=1.0, puff=0.0, aim=12, dx=0.0, dz=0.0, lean=0.0),
   idle=[C(sq=1.0 - 0.04 * (1 - math.cos(TAU * i / 6)) / 2, aim=12 + 3 * math.sin(TAU * i / 6)) for i in range(6)],
   attack=[C(puff=0.2, sq=0.95, aim=16), C(puff=0.45, sq=0.9, aim=20, lean=0.08), C(puff=0.6, sq=0.88, aim=22, lean=0.1),
           C(puff=-0.1, sq=1.08, aim=28, dx=0.18, lean=-0.12), C(puff=0.0, sq=1.02, aim=18, dx=0.1, lean=-0.05), C(puff=0.0, aim=12, dx=0.02)],
   hurt=[C(sq=0.86, dx=0.16, lean=0.2, aim=40, puff=-0.1), C(sq=0.94, dx=0.18, lean=0.12, aim=30), C(sq=1.0, dx=0.06, lean=0.04, aim=18)]),
 "mantis": dict(base=C(lean=0.0, rise=0.0, armN=(70, -60), armF=(75, -55), dx=0.0, dz=0.0, sq=1.0),
   idle=[C(rise=0.03 * math.sin(TAU * i / 6), armN=(70 + 4 * math.sin(TAU * i / 6), -60), armF=(75 - 4 * math.sin(TAU * i / 6), -55)) for i in range(6)],
   attack=[C(rise=0.08, lean=0.15, armN=(110, 150), armF=(115, 160)), C(rise=0.12, lean=0.25, armN=(120, 170), armF=(125, 175)),
           C(rise=-0.05, lean=-0.3, dx=-0.25, armN=(20, -30), armF=(60, 110)), C(rise=-0.08, lean=-0.35, dx=-0.32, armN=(0, -50), armF=(10, -40)),
           C(rise=-0.04, lean=-0.15, dx=-0.18, armN=(30, -60), armF=(25, -55)), C(rise=0.0, dx=-0.04)],
   hurt=[C(lean=0.3, dx=0.14, rise=-0.05, armN=(100, 30), armF=(110, 40)), C(lean=0.22, dx=0.18, armN=(90, 0), armF=(95, 10)), C(lean=0.06, dx=0.06)]),
 "hornet": dict(base=C(hover=0.0, wing=0.0, head=0.0, armN=(-35, -10), armF=(-15, 40), dx=0.0, dz=0.0, lean=0.0, sq=1.0),
   idle=[C(hover=0.06 * math.sin(TAU * i / 6), wing=TAU * i / 2, armN=(-35 + 5 * math.sin(TAU * i / 6), -10), head=0.02 * math.sin(TAU * i / 6)) for i in range(6)],
   attack=[C(wing=0.0, armN=(100, 150), armF=(110, 165), lean=0.12, hover=0.05), C(wing=3.1, armN=(120, 170), armF=(125, 180), lean=0.18, hover=0.1),
           C(wing=6.3, armN=(10, -20), armF=(70, 120), lean=-0.25, dx=-0.3, hover=-0.02), C(wing=9.4, armN=(-10, -45), armF=(0, -30), lean=-0.3, dx=-0.38),
           C(wing=12.6, armN=(20, -10), armF=(30, 10), lean=-0.12, dx=-0.2), C(wing=15.7, dx=-0.03)],
   hurt=[C(wing=0.0, lean=0.25, dx=0.15, head=0.05, armN=(80, 90), armF=(90, 100)), C(wing=3.1, lean=0.18, dx=0.2, armN=(60, 60), armF=(70, 80)), C(wing=6.3, lean=0.05, dx=0.06)]),
}
BUILD = {"beetle": beetle, "mosquito": mosquito, "spitter": spitter, "mantis": mantis, "hornet": hornet}
CELL = {"beetle": (288, 288, 0.95), "mosquito": (256, 256, 0.95), "spitter": (256, 224, 0.62), "mantis": (320, 288, 1.0), "hornet": (416, 480, 1.95)}

# ---------------- camera, lights, render ------------------------------------------------------
az, el = math.radians(30), math.radians(9)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); scn.collection.objects.link(cam); scn.camera = cam
cam.data.type = "ORTHO"
def sun(n, to_src, col, s):
    l = bpy.data.objects.new(n, bpy.data.lights.new(n, "SUN")); scn.collection.objects.link(l)
    l.data.energy, l.data.color, l.data.angle = s, col, math.radians(6)
    l.rotation_euler = Vector(to_src).normalized().to_track_quat("Z", "Y").to_euler()
# mirrored rig: geometry flipped to face +X and lights reflected across the camera plane; the
# post step flips the image so the bug faces left with the key light upper-left like the frog
sun("key", (1.47, 0.32, 1.0), (1, 0.85, 0.65), 3.6); sun("rim", (-1.7, -0.53, 0.5), (1.0, 0.75, 0.5), 2.0)
w = bpy.data.worlds.new("w"); scn.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.25, 0.27, 0.35, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.35
r = scn.render; r.engine = "CYCLES"; scn.cycles.device = "CPU"; r.film_transparent = True
scn.view_settings.view_transform = "Standard"; r.resolution_percentage = int(os.environ.get("RES_PCT", "100"))
os.makedirs(OUT, exist_ok=True)
for bug in BUGS:
    cw, ch, tz = CELL[bug]; r.resolution_x, r.resolution_y = cw, ch
    cam.data.ortho_scale = max(cw, ch) / 91.0
    tgt = Vector((0.0, 0.0, tz))
    cam.location = tgt + 20 * Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    g = world_to_camera_view(scn, cam, Vector((0, 0, 0)))
    k = r.resolution_percentage / 100; json.dump({"cell": [round(cw * k), round(ch * k)], "ground_row": round((1 - g.y) * ch * k), "origin_col": round((cw - g.x * cw) * k), "fps": 12, "flipped": True}, open(f"{OUT}/{bug}_meta.json", "w"))
    spec = POSES[bug]
    for anim in ("idle", "attack", "hurt"):
        for i, kw in enumerate(spec[anim]):
            Pp = dict(spec["base"]); Pp.update(kw)
            made = set(o.name for o in scn.objects)
            BUILD[bug](Pp)
            root = bpy.data.objects.new("root", None); scn.collection.objects.link(root)
            new = [o for o in scn.objects if o.name not in made and o is not root]
            for o in new:
                if o.parent is None: o.parent = root
            root.location = (Pp.get("dx", 0), 0, Pp.get("dz", 0)); root.rotation_euler = (0, Pp.get("lean", 0), 0)
            mir = bpy.data.objects.new("mirror", None); scn.collection.objects.link(mir); mir.scale = (-1, 1, 1); root.parent = mir
            for kind in ("lit", "alb"):
                set_pass(kind); scn.cycles.samples = 24 if kind == "lit" else 1
                scn.cycles.filter_width = 1.5 if kind == "lit" else 0.01
                r.filepath = f"{OUT}/{bug}_{anim}_{i}_{kind}.png"; bpy.ops.render.render(write_still=True)
            for o in new + [root, mir]:
                me = o.data if o.type == "MESH" else None; bpy.data.objects.remove(o)
                if me and me.users == 0: bpy.data.meshes.remove(me)
