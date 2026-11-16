"""Pack the rendered frames into the one-shot's assets: one PNG strip per character and anim,
the backdrop layers, and assets/sprites.js (cells, ground rows, frame counts).
Run: python3 make_game_assets.py FROG_FRAMES BUG_FRAMES BG_DIR GAME_DIR"""
import sys, os, json, subprocess, shutil, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
FROG, BUGS, BGD, GAME = sys.argv[1:5]
A = os.path.join(GAME, "assets"); TMP = os.path.join(HERE, "_pack"); os.makedirs(TMP, exist_ok=True)
env = dict(os.environ, SHEET_PREFIX="frog_"); env.pop("FLIP", None)
subprocess.run([sys.executable, os.path.join(HERE, "anim_post.py"), FROG, TMP], env=env, check=True, stdout=subprocess.DEVNULL)
env = dict(os.environ, SHEET_PREFIX="", FLIP="1")
subprocess.run([sys.executable, os.path.join(HERE, "anim_post.py"), BUGS, TMP], env=env, check=True, stdout=subprocess.DEVNULL)
man = {}
def add(ch, cell, ground_row, origin_col):
    anims = {}
    for p in sorted(glob.glob(f"{TMP}/{ch}_*_sheet.png")):
        an = os.path.basename(p)[len(ch) + 1:-len("_sheet.png")]
        im = Image.open(p); anims[an] = im.width // cell[0]
        im.save(f"{A}/{ch}_{an}.png", optimize=True)
    idle = np.asarray(Image.open(f"{A}/{ch}_idle.png"))[..., 3] > 0
    rows = np.nonzero(idle[:, :cell[0]].any(1))[0]
    man[ch] = {"cell": cell, "ground_row": ground_row, "origin_col": origin_col, "height": int(ground_row - rows.min()), "anims": anims, "fps": 12}
k = 0.67
fw, fh = Image.open(f"{FROG}/idle_0_lit.png").size
add("frog", [fw, fh], round(251 * k), round(118 * k))
for b in ("beetle", "mosquito", "spitter", "mantis", "hornet"):
    m = json.load(open(f"{BUGS}/{b}_meta.json")); w, h = Image.open(f"{BUGS}/{b}_idle_0_lit.png").size
    add(b, [w, h], m["ground_row"], m["origin_col"])
for f in ("sky", "far", "water", "ground"): shutil.copy(f"{BGD}/bg_{f}.png", f"{A}/bg_{f}.png")
with open(f"{A}/sprites.js", "w") as fh_:
    fh_.write("// PROTOTYPE - NOT FOR PRODUCTION\n// Rendered sprite strips in assets/, made by tools/sprites/frog-ronin (Blender + Python).\n")
    fh_.write("// Per character: cell size, the ground row and origin column inside a cell, the idle height, frames per anim.\n")
    fh_.write("window.SPRITES = " + json.dumps(man, indent=1) + ";\n")
    # the strips again as data URIs: a page opened from disk can draw them without tainting the canvas
    import base64
    imgs = {os.path.basename(p)[:-4]: "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()
            for p in sorted(glob.glob(f"{A}/*.png"))}
    fh_.write("window.SPRITE_IMAGES = " + json.dumps(imgs) + ";\n")
print(json.dumps({k_: (v["cell"], v["height"], v["anims"]) for k_, v in man.items()}))
