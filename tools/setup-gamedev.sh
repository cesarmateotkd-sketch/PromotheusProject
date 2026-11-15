#!/usr/bin/env bash
# Reinstalls the game-dev toolchain in a fresh cloud session (idempotent).
# Downloads are checked against the official checksums before use.
set -euo pipefail
GODOT_V=4.7.2-stable
BLENDER_V=5.3.0
mkdir -p /opt/gamedev && cd /opt/gamedev
if ! command -v godot >/dev/null; then
  Z="Godot_v${GODOT_V}_linux.x86_64.zip"
  curl -fsSL -o "$Z" "https://github.com/godotengine/godot/releases/download/$GODOT_V/$Z"
  curl -fsSL "https://github.com/godotengine/godot/releases/download/$GODOT_V/SHA512-SUMS.txt" | grep " $Z\$" | sha512sum -c
  unzip -qo "$Z" && rm "$Z"
  ln -sf "/opt/gamedev/Godot_v${GODOT_V}_linux.x86_64" /usr/local/bin/godot
fi
if ! command -v blender >/dev/null; then
  T="blender-${BLENDER_V}-linux-x64.tar.xz"; M="${BLENDER_V%.*}"
  curl -fsSL -o "$T" "https://download.blender.org/release/Blender$M/$T"
  curl -fsSL "https://download.blender.org/release/Blender$M/blender-${BLENDER_V}.sha256" | grep " $T\$" | sha256sum -c
  tar -xJf "$T" && rm "$T"
  ln -sf "/opt/gamedev/blender-${BLENDER_V}-linux-x64/blender" /usr/local/bin/blender
fi
command -v Xvfb >/dev/null || { apt-get update -qq && apt-get install -y -qq xvfb; }
godot --headless --version
blender --background --version | head -1
