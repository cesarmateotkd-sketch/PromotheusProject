"""Blender: the frog's animation frames, built from pose keys (12 fps).
Run: blender -b --factory-startup --python anim_build.py -- OUTDIR [anim,anim]
Writes OUTDIR/<anim>_<i>_lit.png and _alb.png at 1x (256x224 cell, ground fixed)."""
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "common.py")).read())
import math
from mathutils import Vector
ANIMS = sys.argv[sys.argv.index("--") + 2].split(",") if len(sys.argv) > sys.argv.index("--") + 2 else ["idle", "walk", "strike"]
for name, col in {"trim": (240, 236, 224), "armor": (176, 44, 52), "mouth": (70, 24, 36), "brow": (46, 120, 48)}.items():
    if name not in mats: raise SystemExit("common.py is missing material " + name)

BASEPOSE = dict(lean=0.12, bob=0.0, head=-0.1, hipz=0.36, ff=(0.5, 0.0), bf=(-0.46, 0.0),
                grip=(0.44, 0.58), sword=55, tails=0.0, grin=1.0, sq=1.0, eye=0.0)

def build_frog(P):
    made = set(o.name for o in scn.objects)
    up = bpy.data.objects.new("up", None); scn.collection.objects.link(up)   # upper body pivot at the hips
    hd = bpy.data.objects.new("hd", None); scn.collection.objects.link(hd)   # head pivot at the neck
    upper, head = [], []
    def U(o): upper.append(o); return o
    def Hh(o): head.append(o); return o
    BZ = P["hipz"] - 0.42 + P["bob"]
    sq = P["sq"]
    U(ball("body", 0.33, "skin", (0, 0, 0.58 + BZ), (0.92 / sq ** 0.5, 0.88, 1.08 * sq)))
    U(ball("belly", 0.27, "belly", (0.13, 0, 0.55 + BZ), (0.62, 0.76, 0.96 * sq)))
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=28, v_segments=16, radius=0.4)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.x > 0.17 or v.co.z < -0.34 or v.co.z > 0.3], context="VERTS")
    me = bpy.data.meshes.new("haori"); bm.to_mesh(me); bm.free()
    v = U(place(bpy.data.objects.new("haori", me), "vest", (-0.02, 0, 0.62 + BZ), (0, 0, 0), (0.95, 0.98, 1.05 * sq), 1))
    m = v.modifiers.new("t", "SOLIDIFY"); m.thickness = 0.035
    for s in (-1, 1): U(seg(f"collar{s}", (0.12, 0.27 * s, 0.9 + BZ), (0.2, 0.13 * s, 0.4 + BZ), 0.04, 0.035, "trim"))
    U(torus("obi", 0.3, 0.05, "obi", (0.0, 0, 0.42 + BZ), (0.98, 0.92, 1.1)))
    U(ball("knot", 0.09, "obi", (-0.33, 0, 0.44 + BZ), (0.7, 1.3, 0.8)))
    U(seg("knot1", (-0.36, 0.04, 0.42 + BZ), (-0.5, 0.1, 0.2 + BZ), 0.05, 0.03, "obi"))
    U(seg("knot2", (-0.36, -0.04, 0.42 + BZ), (-0.47, -0.12, 0.24 + BZ), 0.05, 0.03, "obi"))
    U(ball("sode", 0.15, "armor", (-0.03, -0.35, 0.84 + BZ), (1.0, 0.36, 0.85), rot=(0.4, 0, 0)))
    U(ball("sodeg", 0.15, "obi", (-0.03, -0.36, 0.79 + BZ), (1.02, 0.3, 0.5), rot=(0.4, 0, 0)))
    # head: bigger eyes and a wide grin (review 2)
    HZ = 1.06 + BZ
    Hh(ball("head", 0.43, "skin", (0.05, 0, HZ), (1.1, 1.04, 0.88)))
    Hh(ball("jaw", 0.36, "belly", (0.17, 0, HZ - 0.12), (1.12, 0.92, 0.56)))
    g = P["grin"]
    Hh(ball("mouth", 0.24, "mouth", (0.49, 0, HZ - 0.07), (0.32, 1.25 * min(1.15, g), 0.1 * g), rot=(0, 0.3, 0)))
    for s in (-1, 1):
        y = 0.21 * s
        Hh(ball(f"bulb{s}", 0.215, "skin", (0.09, y, HZ + 0.29)))
        Hh(ball(f"eyew{s}", 0.19, "eyew", (0.17, y * 1.05, HZ + 0.33)))
        Hh(ball(f"pupil{s}", 0.12, "pupil", (0.31, y * 1.05 + 0.01, HZ + 0.32 + P["eye"]), (0.55, 1, 1.2)))
        Hh(ball(f"hi{s}", 0.045, "hilite", (0.375, y * 1.05 - 0.04, HZ + 0.39 + P["eye"]), sub=0))
        Hh(seg(f"brow{s}", (0.2, y * 1.05 + 0.11 * s, HZ + 0.54), (0.33, y * 0.7, HZ + 0.46), 0.038, 0.03, "brow"))
    Hh(torus("band", 0.39, 0.045, "band", (0.06, 0, HZ + 0.14), (1.1, 1.0, 1), rot=(0, -0.12, 0)))
    t = P["tails"]
    for k, (yy, zz, ln) in enumerate(((0.04, 0.0, 1.0), (-0.03, -0.1, 0.9))):
        w1 = 0.1 * math.sin(t + k * 1.3); w2 = 0.14 * math.sin(t + k * 1.3 + 1.1)
        a = Vector((-0.4, yy, HZ + 0.13 + zz * 0.2)); b = a + Vector((-0.46 * ln, 0.08 * (1 - 2 * k), -0.1 + w1))
        c = b + Vector((-0.26 * ln, 0.07 * (1 - 2 * k), 0.08 + w2))
        Hh(seg(f"tail{k}", a, b, 0.055, 0.04, "band")); Hh(seg(f"tailb{k}", b, c, 0.04, 0.012, "band"))
    # arms in haori sleeves, two-handed grip; twig at angle P["sword"] in the x-z plane
    grip = Vector((P["grip"][0], -0.04, P["grip"][1] + BZ + 0.04))
    for s in (-1, 1):
        sh = Vector((0.02, 0.29 * s, 0.84 + BZ)); el = sh + (grip - sh) * 0.5 + Vector((0.0, -0.03 * s, -0.12))
        U(seg(f"sleeve{s}", sh, el + Vector((0.02, 0.02 * s, -0.04)), 0.12, 0.155, "vest"))
        U(seg(f"farm{s}", el, grip + Vector((0, 0.05 * s, 0)), 0.065, 0.06, "skin"))
        U(ball(f"hand{s}", 0.08, "skin", grip + Vector((0.02 * s, 0.05 * s, 0.02 * s))))
    a = math.radians(P["sword"]); d = Vector((math.cos(a), 0, math.sin(a)))
    U(seg("hilt", grip - d * 0.15, grip + d * 0.15, 0.042, 0.042, "wrap"))
    U(seg("twig", grip, grip + d * 1.25, 0.038, 0.014, "twig", sub=0, v=8))
    U(seg("knotw", grip + d * 0.5, grip + d * 0.5 + Vector((0.08, 0.05, 0.1)), 0.02, 0.006, "twig", sub=0, v=6))
    U(ball("leaf", 0.065, "leaf", grip + d * 0.62 + Vector((0.03, -0.06, 0.05)), (1.9, 0.25, 0.7), rot=(0.3, -a + 0.2, 0)))
    # legs stay in world space so planted feet do not slide
    for s, (fx, fz) in ((-1, P["ff"]), (1, P["bf"])):
        y = 0.23 * s
        hip = Vector((fx * 0.25, y, P["hipz"] + P["bob"] * 0.6)); foot = Vector((fx, y * 1.25, 0.06 + fz))
        dv = foot - hip; L = 0.27; dist = min(dv.length, 2 * L - 1e-3)
        perp = Vector((-dv.z, 0, dv.x)).normalized()
        if perp.x < 0: perp = -perp
        knee = hip + dv.normalized() * dist / 2 + perp * math.sqrt(max(0, L * L - (dist / 2) ** 2))
        seg(f"thigh{s}", hip, knee, 0.18, 0.13, "skin"); seg(f"shin{s}", knee, foot, 0.11, 0.08, "skin")
        ball(f"thighb{s}", 0.17, "skin", hip + (knee - hip) * 0.45, (1.25, 0.9, 0.9))
        ball(f"foot{s}", 0.11, "foot", (fx + 0.07, y * 1.3, 0.035 + fz), (1.7, 1.15, 0.38))
        for tt in (-1, 0, 1): ball(f"toe{s}{tt}", 0.042, "foot", (fx + 0.24, y * 1.3 + tt * 0.08, 0.03 + fz), (1.2, 1, 0.8), sub=0)
    bpy.context.view_layer.update()
    for o in head: mw = o.matrix_world.copy(); o.parent = hd; o.matrix_world = mw
    hd.location = (0.05, 0, 0.85 + BZ)
    for o in upper + [hd]:
        mw = o.matrix_world.copy(); o.parent = up; o.matrix_world = mw
    bpy.context.view_layer.update()
    up.location = (0, 0, P["hipz"] + P["bob"]); 
    for o in upper + [hd]: o.location = o.location - Vector((0, 0, P["hipz"] + P["bob"]))
    up.rotation_euler = (0, P["lean"], 0); hd.rotation_euler = (0, P["head"], 0)
    return [o for o in scn.objects if o.name not in made]

def clear(objs):
    for o in objs:
        me = o.data if o.type == "MESH" else None
        bpy.data.objects.remove(o)
        if me and me.users == 0: bpy.data.meshes.remove(me)

def P(**kw):
    p = dict(BASEPOSE); p.update(kw); return p
def mix(a, b, t):
    o = {}
    for k in a:
        if isinstance(a[k], tuple): o[k] = tuple(x + (y - x) * t for x, y in zip(a[k], b[k]))
        else: o[k] = a[k] + (b[k] - a[k]) * t
    return o
TAU = 2 * math.pi
def idle(i, n=6):
    ph = TAU * i / n
    return P(bob=-0.02 * (1 - math.cos(ph)) / 2, sword=55 + 3 * math.sin(ph), tails=ph, grin=1.0, head=-0.1 + 0.02 * math.sin(ph))
def walk(i, n=8):
    ph = TAU * i / n; c, s_ = math.cos(ph), math.sin(ph)
    ff = (0.18 + 0.3 * c, max(0, 0.12 * s_)); bf = (-0.12 - 0.3 * c, max(0, -0.12 * s_))
    return P(ff=ff, bf=bf, hipz=0.4, bob=0.03 * abs(math.sin(ph)), lean=0.08, sword=62, grip=(0.4, 0.62), tails=ph * 1.5, head=-0.05)
STRIKE = [  # key poses: wind-up, raise, hold, CUT, follow-through, settle
    P(lean=0.0, sword=95, grip=(0.3, 0.8), head=-0.05, grin=0.9),
    P(lean=-0.12, sword=128, grip=(0.12, 0.94), head=0.0, bob=0.02, grin=0.8, ff=(0.42, 0.0), tails=1.0),
    P(lean=-0.16, sword=140, grip=(0.06, 0.96), head=0.02, bob=0.03, grin=0.8, ff=(0.42, 0.0), tails=1.6),
    P(lean=0.42, sword=30, grip=(0.64, 0.8), head=-0.2, hipz=0.3, ff=(0.72, 0.0), bf=(-0.58, 0.0), grin=1.5, sq=0.92, tails=3.0),
    P(lean=0.36, sword=20, grip=(0.64, 0.74), head=-0.18, hipz=0.3, ff=(0.72, 0.0), bf=(-0.58, 0.0), grin=1.4, sq=0.95, tails=3.8),
    P(lean=0.26, sword=32, grip=(0.55, 0.7), head=-0.14, hipz=0.33, ff=(0.64, 0.0), bf=(-0.52, 0.0), grin=1.2, tails=4.6),
    mix(P(lean=0.26, sword=32, grip=(0.55, 0.7), head=-0.14, hipz=0.33, ff=(0.64, 0.0), bf=(-0.52, 0.0), grin=1.2, tails=5.2), P(tails=5.2), 0.5),
    P(tails=6.0),
]
POSES = {"idle": [idle(i) for i in range(6)], "walk": [walk(i) for i in range(8)], "strike": STRIKE}

# ---------------- camera, lights, render ------------------------------------
tgt = Vector((0.12, 0.0, 0.9)); az, el = math.radians(30), math.radians(9)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); scn.collection.objects.link(cam)
cam.data.type = "ORTHO"; cam.data.ortho_scale = 256 / 91.0
cam.location = tgt + 20 * Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler(); scn.camera = cam
def sun(n, to_src, col, s):
    l = bpy.data.objects.new(n, bpy.data.lights.new(n, "SUN")); scn.collection.objects.link(l)
    l.data.energy, l.data.color, l.data.angle = s, col, math.radians(6)
    l.rotation_euler = Vector(to_src).normalized().to_track_quat("Z", "Y").to_euler()
sun("key", (-1.0, -1.1, 1.0), (1, 0.85, 0.65), 3.6); sun("rim", (1.3, 1.2, 0.5), (1.0, 0.75, 0.5), 2.0)
w = bpy.data.worlds.new("w"); scn.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.25, 0.27, 0.35, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.35
r = scn.render; r.engine = "CYCLES"; scn.cycles.device = "CPU"; r.film_transparent = True
scn.view_settings.view_transform = "Standard"; r.resolution_x, r.resolution_y, r.resolution_percentage = 256, 224, 100
os.makedirs(OUT, exist_ok=True)
for anim in ANIMS:
    for i, pose in enumerate(POSES[anim]):
        objs = build_frog(pose)
        for kind in ("lit", "alb"):
            set_pass(kind); scn.cycles.samples = 24 if kind == "lit" else 1
            scn.cycles.filter_width = 1.5 if kind == "lit" else 0.01
            r.filepath = f"{OUT}/{anim}_{i}_{kind}.png"; bpy.ops.render.render(write_still=True)
        clear(objs)
