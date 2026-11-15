# Game Brainstorm — Living Memory

This is the project's running memory for the game's design: goals, research, and every decision, in order.
**Read it at the start of every session before proposing design work.** Add to it as decisions are made and
commit after each brainstorm step. Newest entries go at the bottom of each section; never silently delete —
mark superseded items instead.

## Goals
- **Platform:** mobile (Android first; iOS later needs a Mac or a paid cloud build).
- **Genre:** idle / incremental game.
- **Primary aim:** highly engaging — players want to come back and keep playing.
- **Guardrail (agreed approach):** compelling through satisfying feedback and strong reward signals, *not* deceptive
  patterns (no "losses disguised as wins", no fake celebrations, no manipulative pressure timers). These hurt trust and
  retention and attract app-store / loot-box regulatory risk.

## Decisions log
| # | Date | Decision | Why | Status |
|---|---|---|---|---|
| D1 | 2026-11-15 | Engine: **Godot 4.7** | Free, runs fully in the cloud workspace, exports Android | Active |
| D2 | 2026-11-15 | Art: **pixel art**, built to `design/art/sprite-style-guide.md` | 12 reference studies done; rules measured from shipped games | Active |
| D3 | 2026-11-15 | Always **study references before making a new visual style**, then measure results against the style card | Biggest quality jumps came right after studies | Active |
| D4 | 2026-11-15 | The ninja character was a **test of the pipeline only** — the game is not ninja-themed | User clarified | Active |
| D5 | 2026-11-15 | Colour strategy: saturation hierarchy + learned rarity ladder (see Research R1) | Evidence-based; see R1 | Proposed — confirm with user |

## Open questions (brainstorm order)
1. ~~Colour psychology for best results~~ → done (R1)
2. Theme / setting of the idle game — *next*
3. Core gameplay loop (what the player does in the first 30 seconds, 5 minutes, 1 day)
4. Progression and upgrade structure (ties to the Terraria tier ladder and Stardew growth stages in the style guide)
5. Monetisation (ethical: no deceptive patterns — see Goals)
6. Camera / view (side, top-down, isometric) and sprite sizes
7. The original market-gap research from the earlier chat was **not recovered** — redo if needed

---

## Research

### R1 — Colour psychology for an engaging idle game (2026-11-15)
**Framing:** colour does not create compulsion by itself; it controls *arousal, attention and reward signalling*, which
amplify the gameplay loop. Use colour to make rewards feel big and the screen readable for long sessions.

**Evidence (strongest first):**
1. **Saturation drives arousal more than hue.** Valdez & Mehrabian (1994): arousal mainly from saturation, pleasantness
   mainly from brightness. Wilms & Oberfeld (2018) confirm saturated/bright colours raise arousal; hue matters a little
   (blue → green → red rising).
   - https://www.semanticscholar.org/paper/Effects-of-color-on-emotions.-Valdez-Mehrabian/d15bdf485f3a64abb59e4d0d1d1b18a9fc652bf9
   - https://www.semanticscholar.org/paper/Color-and-emotion:-effects-of-hue,-saturation,-and-Wilms-Oberfeld/0d2b186b038257aea1fd7a156cbaf2211b4aa3f4
2. **Attention goes to local contrast, but players habituate.** A local change in colour *and* luminance captures attention;
   several salient items compete and slow players; repeated accents get tuned out; motion/sudden onset beats colour alone.
   - https://pmc.ncbi.nlm.nih.gov/articles/PMC5013140
3. **Rarity colours are learned conventions.** Grey → green → blue → purple → orange/gold (Diablo/WoW lineage) is the genre
   standard; players feel value before reading numbers. (Practitioner source.)
   - https://click2.app/blog/item-rarity-tiers-explained-drop-rates/
4. **Sensory reward cues sustain gambling-style loops.** Schüll, *Addiction by Design*: colour, light, animation and sound
   are tuned as one system; wins come with lights/music/graphics. Also documents "losses disguised as wins" — which we
   will NOT do.
   - https://muse.jhu.edu/book/61897
5. **Pop colour-psychology mostly fails to replicate.** The "red impairs performance" effect shrank to ~nothing in a 2020
   meta-analysis. Don't choose colours by symbolism ("red = hunger", "blue = trust").
   - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7704521/
6. **~8% of men have colour-vision deficiency** (mostly red-green). Never carry information by colour alone; pair with
   shape/frame/brightness; blue vs orange is the safest pair.
   - https://www.smashingmagazine.com/2024/02/designing-for-colorblindness/

**Resulting palette strategy (proposed, D5):**
| Layer | Saturation | Purpose |
|---|---|---|
| Background / world | Low, muted | Comfortable for long sessions; makes everything else pop |
| Units / characters | Medium-high, one colour family each | Readable at a glance |
| Reward feedback (coins, gems, level-ups) | Highest; gold/yellow reserved for currency | Arousal spike; always paired with motion + sound |
| Rarity / tiers | Grey → green → blue → purple → gold, plus a frame or shape per tier | Learned value signal; colour-blind safe |
| Alerts | One reserved accent, used rarely | Stays effective (no habituation) |

**Caveat:** game-specific sources were mostly practitioner blogs; used only where they agree with the peer-reviewed work.
