# Capstone — Finish the Game

⏱️ **~105 min studio + demo ceremony** · 🎯 **Graded — 100 points**

[← Part B](../lessons/03-part-b-ship-it.md) · [Session home](../README.md)

---

Four sessions, one game. Tonight it gets finished: the network comes back, the rumble goes in, you pick two features from the menu, and it ships — battery-powered, laptop-free, fighting for the class leaderboard in the closing tournament. This is studio time: the room is yours, the checkpoints below keep you honest, and the instructor is on call.

## What "finished" means

1. **Everything Session 5 built still works:** breathing beacon, green flood, victory and false-start shows, clean cancellation between rounds.
2. **The network is back** — the [Session 4 grafts](../../04-wifi-iot/lessons/05-part-c-connected-game.md), re-applied to your Game-Show Edition: results POSTed fire-and-forget, standings fetched in the pause, leader flourish, fail-soft everywhere. Fair warning: the grafts were written for the *old* game, and your file has changed — the beacon is PWM now, `buzz()` became `beep()`, the referee's reset cancels shows. Tonight you're not following a recipe, you're **merging** — figuring out where each graft's *idea* lands in the code you have now. Budget real time for it; that's the skill.
3. **The game has a sense of touch.** Rumble on at least **two distinct game moments** with **distinct feels** — say, a brief tap at GO and a long buzz on a false start, or heartbeats through the victory show. (Part A taught you the trick: near the stall floor these motors quit outright, so dependable "soft" is made from *short* full-strength pulses, not whisper-level duty.) Cued through `start_show()` like every other performer, so round-reset silences it too.
4. **Two menu items** from below, working.
5. **It ships:** saved as `main.py`, demoed on the power bank. No laptop on the demo table.

## The rumble channel (copyable)

Wire-in block for your game — same shape as `beep()`, cancellation-safe, capped at the motor's 3 V spec:

```python
# --- Hardware: the rumble motor (Part A's rig) ---
rumble = PWM(Pin(14), freq=200, duty_u16=0)

RUMBLE_FULL = 58000          # ~90% duty: 3 V motor, 3.3 V rail, on spec


async def rumble_pulse(strength=RUMBLE_FULL, dur=0.15):
    """One haptic pulse. Cue it through start_show() like everything else."""
    rumble.duty_u16(strength)
    try:
        await asyncio.sleep(dur)
    finally:
        rumble.duty_u16(0)   # survives cancellation -- no stuck motors
```

And two one-liners elsewhere: `rumble.duty_u16(0)` joins the referee's reset (a cancelled show must not leave the motor humming), and `rumble.duty_u16(0); rumble.deinit()` joins the `finally` cleanup.

## Requirements (grading rubric)

| #   | Requirement                                                                                                                              | Pts |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------- | --- |
| 1   | Network restored onto the Game-Show Edition: results POSTed fire-and-forget, standings awaited in the pause, leader flourish — all correct on the live leaderboard | 20 |
| 2   | **Fail-soft, on battery:** scoreboard stopped mid-demo → the game plays on, shows and all, no crash, no stall                              | 15 |
| 3   | Haptics: ≥2 distinct moments with distinct feels (strength × duration), cued via the show machinery, never blocking, silent between rounds  | 20 |
| 4   | Session 5 polish intact: beacon breathes, GO kills it mid-breath, shows cancel to a clean stage                                            | 10 |
| 5   | Ships: boots from `main.py` on the power bank into a fully playable game                                                                   | 15 |
| 6   | Two menu items, demonstrated working                                                                                                       | 20 |

## The menu (choose two)

- **Reaction-time telemetry** — measure each win with `time.ticks_diff()` and add `"ms"` to the POST payload. (The server ignores unknown fields — shipping telemetry before the backend supports it is a real-world move.)
- **Pitch-coded wins** — the win beep's pitch rises as reaction time drops; `rtttl.note_freq()` is sitting right there. A fast win should *sound* fast.
- **Match point** — when a team reaches 5 wins on the *class* standings, the full production: `CHARGE`, a long-tailed comet, maximum rumble.
- **Light-organ fanfare** — merge Session 5's Part D: during the victory show, the strip dances to the fanfare's actual notes.
- **Startup health check** — on boot, GET `/scores` once: two beeps + a green flash if the scoreboard is reachable, one low beep + amber if not. (Notice this is *required thinking* for a headless device — `print()` can't tell you anymore.)
- **Quiet mode** — hold a button during boot to halve every duty ceiling (piezo, rumble, strip). Ship a device your housemates can live with.
- **Compose your own victory jingle** — an original RTTTL string in the songbook's style, played as *your* game's signature fanfare.

## Checkpoints (pacing, not grades)

- **:20 — rumble is in.** The copyable block wired, one show rumbling, game still plays. *(Behind? Flag the instructor — it's a five-minute fix worth not being stuck on.)*
- **:45 — you're on the leaderboard again.** Grafts merged, a test win visible on the projector. This is the hard checkpoint; the room stops and celebrates the first bench there.
- **:75 — menu items working.**
- **:95 — shipped.** `main.py` saved, power-bank boot tested, laptop closed. Demo-ready.

## The demo ceremony

Leaderboard wiped; each bench gets ~90 seconds on battery: one real round of each kind, rumble felt by a volunteer's hand on the breadboard, menu items shown. Then the closing tournament — every bench playing at once, standings live on the projector — during which the instructor **will stop the scoreboard one last time**. Thirteen games, on batteries, shrugging in unison: that's the course. Three villains — sleep, the network, the show — all taught the same lesson, all bowing together.

---

[← Part B](../lessons/03-part-b-ship-it.md) · [Session home](../README.md)
