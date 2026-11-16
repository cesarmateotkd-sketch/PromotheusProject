"""Blender: frog ronin vs beetle, 3/4 side view. Renders two passes per resolution:
lit_*.png (white diffuse, key light upper-left + cool rim) and alb_*.png (flat base colour).
Run: blender -b --factory-startup --python build.py -- OUTDIR"""
import bpy, bmesh, math, sys
from mathutils import Vector
OUT = sys.argv[sys.argv.index("--") + 1]
scn = bpy.context.scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o)

def srgb2lin(c):
    return tuple(((x / 255) / 12.92) if x / 255 <= 0.04045 else (((x / 255) + 0.055) / 1.055) ** 2.4 for x in c)
BASE = {  # base colours (sRGB 0-255); post-processing builds the ramps
    "skin": (92, 196, 72), "belly": (238, 226, 160), "eyew": (250, 250, 240), "pupil": (20, 18, 28),
    "band": (220, 40, 44), "vest": (52, 64, 132), "obi": (214, 168, 64), "twig": (128, 86, 48),
    "leaf": (120, 200, 70), "trim": (240, 236, 224), "armor": (176, 44, 52), "mouth": (70, 24, 36), "brow": (46, 120, 48), "wrap": (220, 40, 44), "foot": (70, 160, 60),
    "shell": (60, 110, 200), "shellb": (64, 116, 206), "shelld": (36, 62, 130), "bhead": (30, 44, 92), "bleg": (24, 30, 60),
    "horn": (70, 120, 210), "beye": (250, 220, 120), "hilite": (255, 255, 255),
}
mats = {}
for m, c in BASE.items():
    mat = bpy.data.materials.new(m); mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    d = nt.nodes.new("ShaderNodeBsdfDiffuse"); d.inputs["Color"].default_value = (0.8, 0.8, 0.8, 1)
    if m in ("pupil", "beye", "horn", "shell", "shellb"):
        d = nt.nodes.new("ShaderNodeBsdfPrincipled"); d.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
        d.inputs["Roughness"].default_value = 0.35
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = (*srgb2lin(c), 1)
    mat["lit"], mat["alb"] = d.name, e.name; mats[m] = mat

def set_pass(kind):
    for mat in mats.values():
        nt = mat.node_tree; out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
        for l in list(out.inputs[0].links): nt.links.remove(l)
        nt.links.new(nt.nodes[mat[kind]].outputs[0], out.inputs[0])

def place(o, mat, loc, rot, scale, sub):
    scn.collection.objects.link(o); o.data.materials.append(mats[mat])
    o.location, o.rotation_euler, o.scale = loc, rot, scale
    for p in o.data.polygons: p.use_smooth = True
    if sub: m = o.modifiers.new("s", "SUBSURF"); m.levels = m.render_levels = sub
    return o

def ball(n, r, mat, loc, scale=(1, 1, 1), rot=(0, 0, 0), sub=1):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=r)
    me = bpy.data.meshes.new(n); bm.to_mesh(me); bm.free()
    return place(bpy.data.objects.new(n, me), mat, loc, rot, scale, sub)

def seg(n, a, b, r1, r2, mat, sub=1, v=12):
    """Tapered limb from point a (radius r1) to point b (radius r2)."""
    a, b = Vector(a), Vector(b); d = b - a
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=v, radius1=r1, radius2=r2, depth=d.length)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, d.length / 2))
    me = bpy.data.meshes.new(n); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(n, me)
    o.rotation_mode = "QUATERNION"
    place(o, mat, a, (0, 0, 0), (1, 1, 1), sub)
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return o

def torus(n, R, r, mat, loc, scale=(1, 1, 1), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=32, minor_segments=10)
    o = bpy.context.active_object; bpy.context.collection.objects.unlink(o)
    return place(o, mat, loc, rot, scale, 1)

# ---------------- FROG (faces +X; feet at z=0; heroic chibi ~3 heads) ----------
_f0 = set(o.name for o in scn.objects)
BZ = -0.06  # lower, wider stance
ball("body", 0.33, "skin", (0, 0, 0.58 + BZ), (0.92, 0.88, 1.08))
ball("belly", 0.27, "belly", (0.13, 0, 0.55 + BZ), (0.62, 0.76, 0.96))
# haori: open-front jacket over the shoulders, white collar trim down the front edges
bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=28, v_segments=16, radius=0.4)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.x > 0.17 or v.co.z < -0.34 or v.co.z > 0.3], context="VERTS")
me = bpy.data.meshes.new("haori"); bm.to_mesh(me); bm.free()
v = place(bpy.data.objects.new("haori", me), "vest", (-0.02, 0, 0.62 + BZ), (0, 0, 0), (0.95, 0.98, 1.05), 1)
sol = v.modifiers.new("t", "SOLIDIFY"); sol.thickness = 0.035
for s in (-1, 1):
    seg(f"collar{s}", (0.12, 0.27 * s, 0.9 + BZ), (0.2, 0.13 * s, 0.4 + BZ), 0.04, 0.035, "trim")
torus("obi", 0.3, 0.05, "obi", (0.0, 0, 0.42 + BZ), (0.98, 0.92, 1.1))
ball("knot", 0.09, "obi", (-0.33, 0, 0.44 + BZ), (0.7, 1.3, 0.8))
seg("knot1", (-0.36, 0.04, 0.42 + BZ), (-0.5, 0.1, 0.2 + BZ), 0.05, 0.03, "obi")
seg("knot2", (-0.36, -0.04, 0.42 + BZ), (-0.47, -0.12, 0.24 + BZ), 0.05, 0.03, "obi")
# shoulder armour (sode) on the near shoulder, gold-edged
ball("sode", 0.15, "armor", (-0.03, -0.35, 0.84 + BZ), (1.0, 0.36, 0.85), rot=(0.4, 0, 0))
ball("sodeg", 0.15, "obi", (-0.03, -0.36, 0.79 + BZ), (1.02, 0.3, 0.5), rot=(0.4, 0, 0))
# head: rounder, less cheek; a grin line and determined brows
_h0 = set(o.name for o in scn.objects)
HZ = 1.06 + BZ
ball("head", 0.43, "skin", (0.05, 0, HZ), (1.1, 1.04, 0.88))
ball("jaw", 0.36, "belly", (0.15, 0, HZ - 0.11), (1.1, 0.9, 0.55))
ball("mouth", 0.22, "mouth", (0.47, 0, HZ - 0.06), (0.3, 1.15, 0.1), rot=(0, 0.3, 0))
for s in (-1, 1):
    y = 0.2 * s
    ball(f"bulb{s}", 0.2, "skin", (0.09, y, HZ + 0.27))
    ball(f"eyew{s}", 0.17, "eyew", (0.17, y * 1.05, HZ + 0.31))
    ball(f"pupil{s}", 0.105, "pupil", (0.3, y * 1.05 + 0.01, HZ + 0.3), (0.55, 1, 1.2))
    ball(f"hi{s}", 0.038, "hilite", (0.355, y * 1.05 - 0.035, HZ + 0.36), sub=0)
    seg(f"brow{s}", (0.2, y * 1.05 + 0.1 * s, HZ + 0.5), (0.31, y * 0.7, HZ + 0.43), 0.035, 0.028, "brow")
torus("band", 0.39, 0.045, "band", (0.06, 0, HZ + 0.14), (1.1, 1.0, 1), rot=(0, -0.12, 0))
seg("tail1", (-0.4, 0.04, HZ + 0.13), (-0.88, 0.14, HZ + 0.02), 0.055, 0.04, "band")
seg("tail1b", (-0.88, 0.14, HZ + 0.02), (-1.15, 0.22, HZ + 0.14), 0.04, 0.012, "band")
seg("tail2", (-0.4, -0.02, HZ + 0.1), (-0.84, -0.1, HZ - 0.12), 0.05, 0.035, "band")
seg("tail2b", (-0.84, -0.1, HZ - 0.12), (-1.06, -0.18, HZ - 0.06), 0.035, 0.01, "band")
HEAD = set(o.name for o in scn.objects) - _h0
# legs: deep wide stance
for s, fx in ((-1, 0.58), (1, -0.52)):
    y = 0.23 * s
    ball(f"thigh{s}", 0.18, "skin", (fx * 0.4, y, 0.25), (1.35, 0.85, 0.85))
    seg(f"shin{s}", (fx * 0.62, y * 1.15, 0.2), (fx, y * 1.25, 0.06), 0.095, 0.07, "skin")
    ball(f"foot{s}", 0.11, "foot", (fx + 0.07, y * 1.3, 0.035), (1.7, 1.15, 0.38))
    for t in (-1, 0, 1):
        ball(f"toe{s}{t}", 0.042, "foot", (fx + 0.24, y * 1.3 + t * 0.08, 0.03), (1.2, 1, 0.8), sub=0)
# arms in wide haori sleeves, two-handed grip raised high toward the beetle
grip = Vector((0.44, -0.04, 0.62 + BZ))
for s in (-1, 1):
    sh = Vector((0.02, 0.29 * s, 0.84 + BZ)); el = Vector((0.22, 0.26 * s, 0.62 + BZ))
    seg(f"sleeve{s}", sh, el + Vector((0.02, 0.02 * s, -0.04)), 0.12, 0.155, "vest")
    seg(f"farm{s}", el, grip + Vector((0, 0.05 * s, 0)), 0.065, 0.06, "skin")
    ball(f"hand{s}", 0.08, "skin", grip + Vector((0.02 * s, 0.05 * s, 0.02 * s)))
tip = grip + Vector((0.72, 0.0, 1.02))
seg("hilt", grip - Vector((0.1, 0, 0.12)), grip + Vector((0.1, 0, 0.12)), 0.042, 0.042, "wrap")
seg("twig", grip, tip, 0.038, 0.014, "twig", sub=0, v=8)
seg("knotw", grip + Vector((0.34, 0, 0.31)), grip + Vector((0.42, 0.05, 0.43)), 0.02, 0.006, "twig", sub=0, v=6)
ball("leaf", 0.065, "leaf", grip + Vector((0.46, -0.06, 0.38)), (1.9, 0.25, 0.7), rot=(0.3, -0.7, 0))
# lean the whole frog into the swing
piv = bpy.data.objects.new("frogpivot", None); scn.collection.objects.link(piv)
for o in scn.objects:
    if o.name not in _f0 and o is not piv and o.name not in HEAD: o.parent = piv
hp = bpy.data.objects.new("headpivot", None); scn.collection.objects.link(hp); hp.location = (0.05, 0, 0.85 + BZ)
bpy.context.view_layer.update()
for o in scn.objects:
    if o.name in HEAD:
        mw = o.matrix_world.copy(); o.parent = hp; o.matrix_world = mw
hp.parent = piv
piv.rotation_euler = (0, 0.16, 0); piv.location = (0.05, 0, 0)
hp.rotation_euler = (0, -0.12, 0)  # keep the face up while the body leans in

# ---------------- BEETLE (faces -X; at +X) --------------------------------------
B, BS = Vector((1.95, 0.15, 0)), 0.82
def bl(v): return tuple(B + BS * Vector(v))
def bball(n, r, mat, loc, scale=(1, 1, 1), rot=(0, 0, 0), sub=1): return ball(n, r * BS, mat, bl(loc), scale, rot, sub)
def bseg(n, a, b, r1, r2, mat, sub=0, v=8): return seg(n, bl(a), bl(b), r1 * BS, r2 * BS, mat, sub, v)
# two elytra halves: the ink line between them is the wing-case split
bball("shellL", 0.58, "shell", (0.18, -0.035, 0.62), (1.3, 0.95, 0.82))
bball("shellR", 0.58, "shellb", (0.18, 0.035, 0.62), (1.3, 0.95, 0.82))
bball("under", 0.5, "shelld", (0.15, 0, 0.42), (1.25, 0.9, 0.5))
bball("pron", 0.36, "shelld", (-0.5, 0, 0.62), (0.9, 1.0, 0.8))
bball("bhead", 0.24, "bhead", (-0.85, 0, 0.5))
bseg("horn1", (-0.98, 0, 0.6), (-1.22, 0, 0.88), 0.08, 0.045, "horn", sub=1)
bseg("horn2", (-1.22, 0, 0.88), (-1.24, 0, 1.08), 0.045, 0.008, "horn", sub=1)
for s in (-1, 1):
    bball(f"beye{s}", 0.055, "beye", (-1.0, 0.14 * s, 0.57))
    bseg(f"mand{s}", (-1.02, 0.09 * s, 0.4), (-1.2, 0.03 * s, 0.32), 0.035, 0.01, "bleg")
    for i, lx in enumerate((-0.45, 0.0, 0.45)):
        hip = Vector((lx, 0.4 * s, 0.38)); knee = hip + Vector((lx * 0.3 - 0.05, 0.28 * s, 0.12)); foot = knee + Vector((lx * 0.25, 0.12 * s, -0.5))
        bseg(f"bl{s}{i}a", hip, knee, 0.05, 0.04, "bleg"); bseg(f"bl{s}{i}b", knee, foot, 0.04, 0.018, "bleg")

# ---------------- camera (3/4 side), lights, render ----------------------------
tgt = Vector((0.98, 0.05, 0.62)); az, el = math.radians(30), math.radians(9)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); scn.collection.objects.link(cam)
cam.data.type = "ORTHO"; cam.data.ortho_scale = 3.95
cam.location = tgt + 20 * Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler(); scn.camera = cam
def sun(n, to_src, col, s):
    l = bpy.data.objects.new(n, bpy.data.lights.new(n, "SUN")); scn.collection.objects.link(l)
    l.data.energy, l.data.color, l.data.angle = s, col, math.radians(6)
    l.rotation_euler = Vector(to_src).normalized().to_track_quat("Z", "Y").to_euler()
sun("key", (-1.0, -1.1, 1.0), (1, 0.85, 0.65), 3.6)   # upper-left, camera side
sun("rim", (1.3, 1.2, 0.5), (1.0, 0.75, 0.5), 2.0)    # cool rim from back-right
w = bpy.data.worlds.new("w"); scn.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.25, 0.27, 0.35, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.35
r = scn.render; r.engine = "CYCLES"; scn.cycles.device = "CPU"; r.film_transparent = True
scn.view_settings.view_transform = "Standard"
r.resolution_x, r.resolution_y = 360, 200   # logical px; aspect of the duel strip
for name, pct, samples in (("x1", 100, 24), ("x4", 400, 24)):
    r.resolution_percentage = pct
    for kind in ("lit", "alb"):
        set_pass(kind)
        scn.cycles.samples = samples if kind == "lit" else 1
        scn.cycles.filter_width = 1.5 if kind == "lit" else 0.01
        r.filepath = f"{OUT}/{kind}_{name}.png"; bpy.ops.render.render(write_still=True)
