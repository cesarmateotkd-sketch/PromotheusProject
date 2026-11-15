// PROTOTYPE - NOT FOR PRODUCTION
// Question: Is the run loop (auto-fight + pick 1-of-3 + combos + boss) fun, and does it make you want another run?
// Date: 2026-11-15
// Every tuning value lives here, each with value, min, max and step. The game reads them live
// through tune.<name> (index.html); the tweak panel, an add-on, writes them back here.
window.CONFIG = {
  seed: 1, // every gameplay random call reads rng(), seeded from this (or ?seed= in the address)
  volume: { value: 0.5, min: 0, max: 1, step: 0.05 },

  // ---- the run ----
  stops: { value: 12, min: 6, max: 20, step: 1 },              // stops on the pond path; the last is the boss
  pick_every: { value: 2, min: 1, max: 4, step: 1 },          // a technique pick after every N cleared stops
  walk_time: { value: 4, min: 0.5, max: 6, step: 0.1 },      // seconds walking between stops
  speedup: { value: 3, min: 1, max: 6, step: 0.5 },            // game speed while the screen is held
  heal_between: { value: 0.25, min: 0, max: 0.5, step: 0.01 }, // fraction of max HP healed after each stop
  enemy_scale: { value: 0.07, min: 0, max: 0.4, step: 0.01 },  // enemy HP/attack growth per stop

  // ---- the frog ----
  frog_hp: { value: 100, min: 20, max: 400, step: 5 },
  frog_atk: { value: 12, min: 1, max: 60, step: 1 },           // damage per sword strike
  frog_atk_interval: { value: 0.8, min: 0.2, max: 2, step: 0.05 }, // seconds between strikes

  // ---- bugs: hp, attack damage, seconds between attacks ----
  beetle_hp: { value: 80, min: 5, max: 200, step: 1 },
  beetle_atk: { value: 3, min: 1, max: 40, step: 1 },
  beetle_int: { value: 1.8, min: 0.3, max: 4, step: 0.05 },
  beetle_armor: { value: 2, min: 0, max: 10, step: 1 },        // damage removed from each frog strike
  mosq_hp: { value: 28, min: 3, max: 100, step: 1 },
  mosq_atk: { value: 1, min: 1, max: 30, step: 1 },
  mosq_int: { value: 0.7, min: 0.2, max: 3, step: 0.05 },
  mosq_dodge: { value: 0.2, min: 0, max: 0.8, step: 0.05 },    // chance a frog strike misses a mosquito
  spit_hp: { value: 44, min: 3, max: 120, step: 1 },
  spit_atk: { value: 3, min: 1, max: 40, step: 1 },
  spit_int: { value: 2, min: 0.4, max: 5, step: 0.05 },
  spit_travel: { value: 0.5, min: 0.1, max: 2, step: 0.05 },   // seconds a goo ball flies before hitting
  mantis_hp: { value: 300, min: 20, max: 800, step: 5 },       // mini-boss, stop 6
  mantis_atk: { value: 7, min: 1, max: 60, step: 1 },
  mantis_int: { value: 1.2, min: 0.3, max: 4, step: 0.05 },
  hornet_hp: { value: 820, min: 50, max: 3000, step: 10 },     // boss, last stop
  hornet_atk: { value: 11, min: 1, max: 80, step: 1 },
  hornet_int: { value: 1.1, min: 0.3, max: 4, step: 0.05 },
  hornet_rage: { value: 1.6, min: 1, max: 3, step: 0.1 },      // attack-speed multiplier below half HP

  // ---- techniques (per level) ----
  lash_dmg: { value: 12, min: 1, max: 80, step: 1 },           // Tongue Lash damage
  lash_cd: { value: 3, min: 0.5, max: 10, step: 0.1 },         // seconds between lashes
  leap_dodge: { value: 0.12, min: 0, max: 0.4, step: 0.01 },   // Lily Leap dodge chance per level
  rain_regen: { value: 2, min: 0, max: 15, step: 0.5 },        // Rain Stance HP per second in fights
  fury_speed: { value: 0.25, min: 0, max: 1, step: 0.05 },     // Twig Fury attack speed per level
  shell_block: { value: 2, min: 0, max: 10, step: 1 },         // Shell Guard damage blocked per hit
  croak_cd: { value: 7, min: 2, max: 20, step: 0.5 },          // Croak Shout cooldown at level 1
  croak_stun: { value: 1.2, min: 0.2, max: 4, step: 0.1 },     // seconds enemies are stunned
  spark_burn: { value: 3, min: 0, max: 20, step: 0.5 },        // Firefly Spark burn damage per second per level
  bubble_shield: { value: 20, min: 0, max: 100, step: 5 },     // Bubble Shield absorbed at each fight start

  // ---- combos ----
  storm_heal: { value: 3, min: 0, max: 15, step: 1 },          // Storm Tongue: HP healed per lash hit
  moon_hits: { value: 3, min: 2, max: 6, step: 1 },            // Moon Leap: strikes after a dodge
  thunder_dmg: { value: 25, min: 0, max: 150, step: 5 },       // Thunder Croak: shout damage
  fortress_reflect: { value: 0.3, min: 0, max: 1, step: 0.05 },// Fortress Shell: share of blocked damage reflected
  mist_heal: { value: 6, min: 0, max: 30, step: 1 },           // Mist Ronin: heal on each dodge

  // ---- loot and crafting ----
  coin_beetle: { value: 4, min: 0, max: 50, step: 1 },
  coin_mosq: { value: 2, min: 0, max: 50, step: 1 },
  coin_spit: { value: 3, min: 0, max: 50, step: 1 },
  coin_mantis: { value: 25, min: 0, max: 200, step: 5 },
  coin_hornet: { value: 60, min: 0, max: 500, step: 5 },
  armour_hp: { value: 60, min: 0, max: 200, step: 5 },         // Lily-Pad Armour: max HP per level
  spear_atk: { value: 8, min: 0, max: 40, step: 1 },           // Reed Spear: strike damage per level
  guard_block: { value: 3, min: 0, max: 20, step: 1 },         // Beetle-Shell Guard: damage blocked per hit per level
  cost_growth: { value: 1.7, min: 1, max: 4, step: 0.1 },      // each gear level costs this much more
};
