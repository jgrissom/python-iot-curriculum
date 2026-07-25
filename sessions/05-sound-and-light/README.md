# Session 5 — Sound & Light: PWM, Ringtones & NeoPixels

*Part of the [Python IoT on the TinyPICO curriculum](../../README.md).*

Your board can already blink, buzz, and talk to the internet. Tonight it learns *showmanship*: LEDs that breathe instead of blink, a piezo that plays actual melodies from Nokia-era ringtone strings, and a stick of addressable NeoPixels for stage lighting. Underneath the fun is one serious idea, and it's the same one as always — a melody takes seconds to play, an animation takes seconds to run, and **if you block on them, your program is deaf until the show ends.** Sound and light are Session 4's slow network call wearing a party hat.

| | |
|---|---|
| **Duration** | 3.5 hours (210 min) + optional bonus segment |
| **Level** | Intermediate Python (Session 3 required; Session 4 recommended) |
| **Environment** | [Thonny](https://thonny.org/) + MicroPython |
| **Board** | TinyPICO ESP32 — Session 3 bench wiring **+ two new parts** (passive piezo, NeoPixel stick) |

---

## Lesson navigation

1. [Session Overview & Timing](lessons/00-overview.md)
2. [Opening Review — What the Connected Game Taught Us](lessons/01-review.md) — *15 min*
3. [Warm-up: Two New Parts on the Bench](lessons/02-setup.md) — *25 min*
4. [Part A — PWM: One Trick, Two Senses](lessons/03-part-a-pwm.md) — *35 min*
5. [Part B — RTTTL: Your Board Plays Ringtones](lessons/04-part-b-rtttl.md) — *40 min*
6. [Part C — NeoPixels: Stage Lighting](lessons/05-part-c-neopixels.md) — *30 min*
7. [Part D — The Light Organ (optional)](lessons/06-part-d-light-organ.md) — *bonus*
8. [Assignment — Reaction Game: Game-Show Edition](assignment/README.md) — *45 min, graded*

Something not working? → **[Troubleshooting & FAQ](../../TROUBLESHOOTING.md)** — now with a sound & light section.

## Code files

| File | What it is |
|---|---|
| [`code/new_parts_test.py`](code/new_parts_test.py) | Run once after wiring tonight's parts — clicks, a rising tone, and a pixel parade that **counts your stick** (sets `NUM_PIXELS` for the whole night) |
| [`code/rtttl.py`](code/rtttl.py) | The RTTTL parser + async player you build in Part B — upload to the board like a library |
| [`code/songs.py`](code/songs.py) | A songbook of RTTTL strings (fanfares, classics, and one sad trombone) — upload like a library |
| [`code/reaction_game_show_STARTER.py`](code/reaction_game_show_STARTER.py) | The assignment scaffold — Session 3's game with the stage rigged, three TODOs to make it a show |

## What students will be able to do

- Explain PWM's two knobs — duty cycle and frequency — and which one each device cares about
- Dim and *breathe* LEDs with `machine.PWM` instead of switching them on/off
- Generate musical pitches on a passive piezo and explain the 2^(1/12) semitone rule
- Parse a compact text format (RTTTL) into data a program can act on
- Drive a WS2812 NeoPixel strip with the built-in `neopixel` module — and respect its power budget
- Run seconds-long sound and light effects *without ever blocking the program* — fire-and-forget with `asyncio.create_task()`, and cancel a show that's no longer wanted
