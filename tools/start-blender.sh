#!/usr/bin/env bash
# Starts Blender on a virtual display with the MCP for Blender add-on listening
# on localhost:9876, so Claude's Blender MCP tools can drive it in a cloud session.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
command -v blender >/dev/null || { echo "blender not installed (see tools/setup-gamedev.sh)"; exit 1; }
# Install + enable the add-on once (idempotent).
blender --background --factory-startup --python-expr "
import bpy, addon_utils
mods=[m.__name__ for m in addon_utils.modules()]
if 'mcp_for_blender_addon' not in mods:
    bpy.ops.preferences.addon_install(filepath='$DIR/blender/mcp_for_blender_addon.py', overwrite=True)
addon_utils.enable('mcp_for_blender_addon', default_set=True, persistent=True)
bpy.ops.wm.save_userpref()
" >/dev/null 2>&1
if ! pgrep -x Xvfb >/dev/null; then Xvfb :99 -screen 0 1600x900x24 >/dev/null 2>&1 & sleep 1; fi
if ! pgrep -f 'blender-5.*/blender$|/blender( |$)' | grep -qv $$; then
  DISPLAY=:99 nohup blender >/tmp/blender-mcp.log 2>&1 &
fi
for i in $(seq 1 30); do (echo >/dev/tcp/127.0.0.1/9876) 2>/dev/null && { echo "Blender MCP add-on listening on 9876"; exit 0; }; sleep 1; done
echo "Blender started but add-on not listening yet; see /tmp/blender-mcp.log"; exit 1
