"""(materials and helpers shared with the key art)
Blender: frog ronin vs beetle, 3/4 side view. Renders two passes per resolution:
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
    "lacq": (44, 36, 58), "gold": (236, 184, 60), "clan": (200, 36, 48), "cloth": (240, 232, 214),
    "mosq": (128, 84, 176), "mosqd": (70, 46, 104), "hood": (34, 30, 46), "wing": (206, 232, 244), "redeye": (236, 64, 64),
    "needle": (190, 196, 214), "spit": (236, 150, 52), "spitb": (250, 204, 120), "straw": (222, 190, 112), "bamboo": (150, 186, 82),
    "mant": (240, 168, 204), "mantl": (252, 226, 240), "blade": (226, 232, 246), "mantd": (190, 110, 160),
    "hyel": (250, 200, 40), "hblk": (40, 32, 34), "cape": (190, 30, 44), "heye": (60, 30, 30),
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

