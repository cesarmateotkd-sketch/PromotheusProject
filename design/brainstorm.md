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
| D5 | 2026-11-15 | Colour strategy: saturation hierarchy + learned rarity ladder (see Research R1) | Evidence-based; see R1 | Active (approved by user) |
| D6 | 2026-11-15 | Theme direction: **quirky mascot idle RPG** | Idle RPG is where revenue is growing; mascot charm sells (Capybara Go, Legend of Mushroom) — see R2 | Active |
| D7 | 2026-11-15 | Player fantasy: **getting stronger** (power fantasy — numbers explode, bosses fall) | User choice | Active |
| D8 | 2026-11-15 | Session style: **active + idle** — real play sessions with decisions, progress builds while away | Fills the "idle with real decisions" gap (R2) | Active |
| D9 | 2026-11-15 | Social: **light social** at launch — leaderboards, friend visits, gifting; no live servers needed | Social idle is a gap (R2) without big server cost | Active |
| D10 | 2026-11-15 | Mascot: **Frog Ronin** — a small frog with a twig sword who becomes a pond legend; eats defeated bugs to power up; visual upgrade ladder (lily-pad armour → reed spear → dragon-scale samurai) | Chosen from 4 original pitches (Pebble, Toast Knight, Frog Ronin, Cactus Gladiator) | Active |
| D11 | 2026-11-15 | Tone: **cute but epic** — adorable lead, battles and growth feel genuinely heroic | User choice | Active |
| D12 | 2026-11-15 | Active play: **roguelite build choices** each run (pick upgrades/skills), progress keeps building while away | Matches Capybara Go-style hits; gives real decisions (D8) | Active |
| D13 | 2026-11-15 | Core loop **draft** (see R4 "Draft loop"): auto-fight + pick 1-of-3 techniques that combine into combos; ~5-min runs ending in a boss; meta between runs; capped idle "meditation" chest; daily dojo + friend visits; ponds as chapters | Fixes the main critique of the hits (runs without real decisions) while keeping their proven structure | Active (refined by D14–D17) |
| D14 | 2026-11-15 | Run length: **about 3–5 minutes** | Fits a phone break; several runs per session | Active |
| D15 | 2026-11-15 | Control: **auto-fight + technique picks** (one-handed play) | Simplest to play; keeps idle feel | Active |
| D16 | 2026-11-15 | Run limit: **free runs, capped rewards** — full rewards only for the first few runs a day; no energy paywall | Avoids energy-as-paywall feeling; still paces the economy | Active |
| D17 | 2026-11-15 | Gear: **crafting from bug materials + occasional big rare drops** | Player control plus real "big win" moments (fixes Legend of Mushroom's weak spot, R4) | Active |

## Open questions (brainstorm order)
1. ~~Colour psychology for best results~~ → done (R1)
2. ~~Theme / setting~~ → Frog Ronin, cute but epic (D10–D11)
3. ~~Core gameplay loop~~ → D13–D17
4. Progression and upgrade structure — *next* (ties to the Terraria tier ladder and Stardew growth stages in the style guide)
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

### R2 — Which idle-game themes are working, from the most successful studios (2026-11-15)
| Studio / game | Theme | Why it worked |
|---|---|---|
| Kolibri Games — Idle Miner Tycoon (~125M downloads) | Mining tycoon | Twist on a familiar theme (dig *down* instead of building up); friendly art, "only positive emotions"; simple satisfying loop, depth unlocked later; 75% day-1 retention vs ~40% typical; weekly LiveOps |
| Nexon — MapleStory: Idle RPG | Idle RPG on known IP | Biggest idle game of 2026: $47M peak month, $350M+ in under a year |
| Habby — Capybara Go! / Joy Net — Legend of Mushroom | Quirky mascot idle RPG | Revenue held while downloads fell — retained players carry the business |
| AppQuantum — Gold and Goblins | Mining + cute goblins | $113M+ IAP |
| Grow a Garden (Roblox) / Rusty's Retirement (PC) | Cozy growing / farming | 35B+ visits; "renaissance" of desktop idlers |

**Patterns:** (1) twist a familiar theme rather than invent one; (2) plain tycoon reskins are saturated — "only if differentiated";
(3) idle RPG is where revenue is growing (Korea: downloads -30%, revenue +57% over 12 months);
(4) open gaps: social / trading / co-op idle, idle with real decisions, cozy growing; (5) a lovable, slightly odd mascot is a theme in itself.

Sources:
- https://www.gameanalytics.com/blog/making-a-hit-idle-game-eight-lessons-from-kolibri-games
- https://www.eu-startups.com/2020/10/get-your-game-out-and-on-the-market-as-fast-as-possible-interview-with-kolibri-games-co-founder-janosch-sadowski/
- https://www.kolibrigames.com/blog/lets-dig-in/
- https://www.gamigion.com/top-10-midcore-games-by-iap-revenue-in-q1-2026/
- https://www.pocketgamer.biz/h1-2026-genre-analysis-strategy-stumbles-rpgs-fall-and-puzzle-revenue-ramps-up/
- https://sensortower.com/blog/2025-q3-ios-top-5-idle%20rpg-units-us-6040bbc2241bc16eb883a0cb
- https://appmagic.rocks/research/idle-steam-games-2026
- https://rolearn.dev/trend-reports/genre-shift-2026-predictions/
- https://www.gamemeca.com/en/view.php?gid=1782789

### R3 — Competitor check: frog / samurai idle and roguelite games (2026-11-15)
No frog-samurai / frog-ronin game found. Nearby titles to stay distinct from:
- Legend of Frog: Idle RPG (Azur) — frog necromancer + undead tank, 100K+ installs — https://play.google.com/store/apps/details?id=com.metime.movingtower&hl=en_US
- Frog Idle – Lazy Kaeru (TDCGames, 10K+) — check its style if we ever lean heavily Japanese
- Froguelike (Steam bullet-heaven, frog eats bugs) — https://store.steampowered.com/app/2315020/Froguelike/ — overlaps our "eats bugs" idea; keep bug-eating as flavour, not the core hook
- Ronin: The Last Samurai (Krafton) — samurai roguelike, no frog — https://www.krafton.com/en/games/ronin-the-last-samurai/
**Takeaway:** frog + ronin + idle roguelite is open; our hook should be the samurai growth fantasy (twig sword → legend), not bug-eating alone.

### R4 — Core loops of the hits (2026-11-15)
| Game | Core loop | Where retention / revenue lives | Main critique |
|---|---|---|---|
| Capybara Go! (Habby) | Tap to advance a "day"; auto events and fights; pick 1-of-3 skills | Meta screen between runs (gear, pets, talents) — "where the real game begins" | Few meaningful decisions per run; skills barely combine; modes are stat checks |
| Legend of Mushroom | Defeat enemies → near-free gear pulls → equip/sell | Many progression verticals (mounts, relics, skills), each monetised | No "big win" feeling (shard gacha); weak social |
| Archero (Habby) | Roguelite run: clear rooms, pick skills, die/finish | Hyper-casual core for retention + light RPG meta for monetisation; ~80% D1 at launch | Grind walls; a few dominant skills |
| AFK Arena / MapleStory Idle | Earn while away into a capped chest (8–24 h) | The full chest is the "appointment"; active progress raises idle rate and idle rewards fund active play | Hard walls that push wait-or-pay |
| Kongregate idle talks | Prestige = reset with a bonus | Among the best retention on Kongregate | — |

**Key insight:** Habby simplified cores and deepened metas over time; critics everywhere complain runs lack real decisions.
Our opening: a simple core whose build choices *genuinely combine*, plus a satisfying meta.

**Draft loop (D13, proposed):**
- 30 s: auto-fight bugs along the pond path; every few fights pick 1 of 3 techniques; techniques combine into named combos
- Run (~5 min): stage chain ending in a boss; win or fall → gear, coins, bug materials
- Between runs: gear upgrade ladder (lily-pad armour → reed spear → dragon-scale), permanent techniques, collection
- Away: capped "meditation" chest; better active progress → faster idle rate (two-way loop)
- Daily: dojo challenge, boss of the day, friends' frogs visit, gift flies (light social)
- Long term: ponds as chapters, rank titles (Tadpole → … → Legend), possible prestige reset

Sources:
- https://medium.com/@shenshenlove/the-habby-formula-gamification-of-growing-and-existing-872072b15acd
- https://www.gamigion.com/capybara-go-global-launch-ua-case-study/
- https://minireview.io/adventure/capybara-go
- https://www.deconstructoroffun.com/blog/2024/4/15/the-magic-of-legend-of-mushroom
- https://www.deconstructoroffun.com/blog/2019/8/9/why-archero-banked-25m-but-leaves-25m-hanging-hlx9n
- https://naavik.co/deep-dives/survivorio-archeros-footsteps/
- https://www.deconstructoroffun.com/blog/2019/6/6/afk-arena-puts-lilith-into-the-billionaire-club
- https://alexandremacmillan.com/2019/06/13/idle-mechanics-and-monetizing-progession-in-afk-arena/
- https://archive.org/details/GDC2015Pecorella
- https://media.gdcvault.com/gdceurope2016/presentations/Pecorella_Anthony_Quest%20for%20Progress.pdf
