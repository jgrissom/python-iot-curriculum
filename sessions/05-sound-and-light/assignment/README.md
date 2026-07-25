# Assignment — Reaction Game: Game-Show Edition

⏱️ **45 min** · 🎯 **Graded — 100 points**

[← Part D](../lessons/06-part-d-light-organ.md) · [Session home](../README.md)

---

Your reaction game has been running on a bare stage for two sessions. Tonight it gets the full production: mood lighting, a live orchestra, and pyrotechnics (small ones). The game logic is **already done** — the starter is Session 3's known-good solution with the stage rigged. Your job is the three TODOs, and one golden rule hangs over all of them:

> **The show must not stop the game.** A fanfare runs for seconds. `await` it in a player coroutine and the buttons go deaf until the last note — the exact freeze Session 4's blocking network call caused. Shows are fire-and-forget, and a new round clears the stage.

## What the finished game does

1. **Wait phase:** the red LED *breathes* — a smooth PWM swell and fade, not a blink — while the strip glows with dim red house lights and the DotStar holds red. (This was literally Session 3's stretch goal. Tonight it's the graded path.)
2. **GO:** green LED on, DotStar green, the strip floods green — and the breath dies *mid-breath*, instantly.
3. **A win:** DotStar shows the winner's cap color, and the victory show erupts — the `VICTORY` fanfare **and** a comet in the winner's cap color, running *at the same time*, while the game stays fully awake underneath.
4. **A false start:** DotStar red, sad trombone, red flashes on the strip. Shame, but responsive shame.
5. **Next round:** whatever's left of any show is cancelled — silence, dark strip, breathing beacon — like it never happened.

## Requirements (grading rubric)

| #   | Requirement                                                                                                                                          |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Wait beacon **breathes** via PWM (smooth up and down, gamma-corrected) with red house lights on the strip — an on/off blink scores zero here          |
| 2   | GO kills the breath **instantly** (mid-breath, not after the exhale) and floods the strip green                                                       |
| 3   | Victory show: fanfare + comet in the **winner's cap color**, launched fire-and-forget, sound and light genuinely concurrent                           |
| 4   | False-start show: sad trombone + red strip flashes, same fire-and-forget rule                                                                        |
| 5   | **The show never stops the game:** buttons and referee stay live during any show, and a new round cancels a still-running show cleanly (silence + dark stage) |
| 6   | Hygiene: no `time.sleep()` anywhere in the async program; the `finally` block leaves both PWMs silent and deinitialized and the strip dark            |

> [!NOTE]
> Row 5 is the session's thesis, and it gets Session 4's treatment: during your demo the instructor **will** mash a button in the middle of your victory fanfare — the game must respond on the spot, and the fresh round must start on a clean stage. Rows 3–5 die together if a show is `await`ed: the freeze *is* the bug.

## Where to work

Start from [`code/reaction_game_show_STARTER.py`](../code/reaction_game_show_STARTER.py) — or rig your own Session 3 game the same way if it plays flawlessly; grading is identical. The starter **runs as-is** (placeholder blink and beeps) and keeps running after each TODO — upgrade one, run it, move on. Board needs [`rtttl.py`](../code/rtttl.py) and [`songs.py`](../code/songs.py) uploaded, plus the usual `micropython_dotstar.py`.

Everything you need is already on the bench: the breath is Part A's coroutine plus a bail-out check, the shows are Part B's `create_task` move through the provided `start_show()` (read its comment — it exists because cancelling a task does *not* cancel tasks it started), and the lighting helpers are Part C's, shipped in the starter.

## Stretch goals (extra credit)

- **Pitch-coded reaction time:** measure the win's reaction time with `time.ticks_diff()` (Session 3 stretch) and beep a note whose pitch rises as the time drops — a fast win should *sound* fast. (One octave per 100 ms saved is dramatic; `rtttl.note_freq()` is sitting right there.)
- **Match point:** first player to 3 wins gets the full production — `CHARGE` fanfare plus a long-tailed comet in their color, and the score resets.
- **Light-organ fanfare:** merge Part D — during the victory show, the strip dances to the fanfare's actual notes instead of running a canned comet.
- **Back online:** graft Session 4's scoreboard reporting back in (`create_task` the POST, fail-soft) — your win hits the class leaderboard *while* the fanfare plays. Two sessions, one event loop, zero freezes.

---

[← Part D](../lessons/06-part-d-light-organ.md) · [Session home](../README.md)
