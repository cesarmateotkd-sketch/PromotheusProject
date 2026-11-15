# Game Brief: Frog Ronin

## In your words
mobile portrait, cute-but-epic idle RPG. A small frog samurai auto-fights bugs along a pond path; every few fights the player picks 1 of 3 techniques; techniques combine into named combos (real build decisions); a run lasts about 3-5 minutes and ends in a boss; win or fall you bring home coins and bug materials; between runs a simple upgrade screen (crafting gear from bug materials). One-handed tap only. Placeholder pixel art is fine. Question to answer: is the run loop (auto-fight + 1-of-3 picks + combos + boss) fun and does it make you want another run?

1. Fights: few tough bugs · 2. Combos: shown · 3. View: side view · 4. Difficulty: fall, then win

**Pitch:** A tiny frog with a twig sword fights his way along the pond, mixing techniques into combos, to become the pond's legend.

**Genre:** idle RPG with roguelite runs (survivors-like build picks, no steering)

**Controls:** tap only, one-handed — tap a technique card to pick; tap buttons on the upgrade screen

**Question:** Is the run loop (auto-fight + pick 1-of-3 + combos + boss) fun, and does it make you want another run?

**Hooks:** techniques that visibly combine into named combos; a twig-sword frog growing into a samurai legend

**Intent:** staged failure (from your answer: fall, then win)

## Look and references
- Look: side-view pixel art following `design/art/sprite-style-guide.md`: muted pond-bank backdrop (dusky greens, teal water), a vivid green frog with a red headband and twig sword, each bug one colour family, gold coins and white hit sparks as the most saturated things on screen, 1px near-black outlines on all characters. Signature detail: combos flash their name in a banner and change the frog's look. Every figure drawn, no emoji, no plain circles.
- References: Capybara Go (auto-advance + 1-of-3 picks), Legend of Mushroom (watching duels), Vampire Survivors (evolve recipes shown on cards).
- View: 2D · Camera: static side view; the path scrolls past.

## First minute
The frog hops onto the pond path and duels a beetle on his own (tap anything to speed up). After two fights the first "choose 1 of 3" pauses the game: Tongue Lash, Lily Leap, Rain Stance, each card saying what it does. The next pick offers a technique whose card shows "+ Tongue Lash = Storm Tongue"; taking it fires the first combo banner and his attacks visibly change: the hook pays off.

## Challenge
First real trouble: a Mantis mini-boss around minute 2. The Hornet Shogun boss around minute 4 usually beats a first run. A fall keeps coins and bug materials; crafting one upgrade (e.g. lily-pad armour) makes run 2 winnable. Fights get tougher stop by stop.

## Core loop
- The frog auto-walks and duels 1–3 bugs per stop; you watch and tap to speed up
- Every few fights, pick 1 of 3 techniques; matching pairs form named combos
- Beat the Hornet Shogun or fall → bring home coins and bug materials
- Between runs, craft gear from bug materials → start the next run stronger

## Goal & fail state
- Goal: beat the Hornet Shogun at the end of the pond. Fail: the frog's health hits zero → run ends, coins and materials kept.

## Features
- [x] Auto-walking side-view run (~4 min) with health, run timer and stop counter
- [x] 4 bug kinds, each attacking differently: Beetle (tough, slow), Mosquito (fast, weak), Spitter Bug (ranged), Mantis mini-boss; plus the Hornet Shogun boss
- [x] Pick-1-of-3 technique cards (about 8 techniques), held ones level up
- [x] 4–5 named combos, shown as recipes on the cards, with a banner and a visible change when formed
- [x] Coins + bug materials earned in the run, kept on a fall
- [x] Between-runs crafting screen: 3 gear pieces (lily-pad armour, reed spear, beetle-shell guard) that carry over, saved in the browser
- [x] Tap to speed up fights

## Your systems
- Auto-fight run · in the slice
- Technique picks and combos · in the slice
- Boss fight · in the slice
- Crafting gear from bug materials · thin stand-in
- Idle meditation chest · later
- Light social (friends, gifting) · later

## Keep
- The run loop's gameplay: auto-fight, 1-of-3 picks, combos, boss (first play: "the game play works")
- A combo firing: the banner and the frog changing how he fights (first play: best moment)

## Avoid
- energy or stamina limits on runs (D16)
- deceptive reward patterns — no fake wins (Goals guardrail)

## Out of scope
- Idle meditation chest: grow it
- Many ponds (chapters) and rank titles: grow it
- Daily dojo / boss of the day: change it after play
- Friends, gifting, leaderboards: needs a server: not built yet
- Ads and paid items: not built yet
- A phone app build: a browser game sized for a phone is built instead; Godot after you've played it

## Build order
1. The slice: one complete run with picks, combos, mini-boss and boss, plus the crafting screen and a second run
2. Balance the run so run 1 falls and run 2 can win
3. Polish combo banners and hit feedback

---
**Kill condition:** if after two tuning rounds the picks still feel like they don't matter (combos change nothing you can see). *(guessed)*

**Who it's for / what they feel:** mobile players on short breaks who want to feel a tiny hero get strong through their own choices. *(inferred (strong), from D7)*

**Games you love / don't:** Capybara Go and Legend of Mushroom as references. *(guessed)*
