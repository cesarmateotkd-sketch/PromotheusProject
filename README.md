# PromotheusProject
Just a little side thing :)

## Game-dev toolchain

This repo is set up for building a mobile game with Claude Code, using Godot.

**New cloud session:** run `tools/setup-gamedev.sh` to install Godot 4.7.2 and Blender 5.3. It checks both downloads against their official checksums.
**3D modeling:** run `tools/start-blender.sh` to start Blender on a virtual display with the Blender MCP add-on on localhost:9876.

| Tool | Source | Where it's configured |
|---|---|---|
| Studio agents, skills and hooks | Donchitos/Claude-Code-Game-Studios (MIT, v1.3.0) | `.claude/`, `CLAUDE.md`, `design/`, `production/` |
| Game-dev skills: router, godot, disciplines, genres, workflows | gamedev-skills/awesome-gamedev-agent-skills (Apache-2.0) | `.claude/settings.json` → `enabledPlugins` |
| Superpowers workflow | obra/superpowers (MIT) | `.claude/settings.json` |
| MCP for Blender | ahujasid/mcp-for-blender (MIT) | plugin, plus the add-on in `tools/blender/` |
| Godot MCP | @coding-solo/godot-mcp@0.1.1 (MIT) | `.mcp.json` |

Telemetry is turned off through `env` in `.claude/settings.json`.
