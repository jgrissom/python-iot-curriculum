# Session 6 — Capstone: Finish the Game

*Part of the [Python IoT on the TinyPICO curriculum](../../README.md).*

Three sessions ago you built a reaction game. Then it went online. Then it got a stage show. Tonight it gets **finished**: the network comes back, the game gains a sense of *touch* (a phone-style vibration motor — and the transistor and flyback diode that driving a motor demands), and the whole thing ships as a self-contained device that runs from a battery with no laptop attached. Most of tonight is **studio time** — you, your game, and a menu of features — ending in a demo ceremony on the class leaderboard.

| | |
|---|---|
| **Duration** | 3.5 hours (210 min) |
| **Level** | Intermediate Python (Sessions 3–5 required) |
| **Environment** | [Thonny](https://thonny.org/) + MicroPython — until the end, when your board won't need it anymore |
| **Board** | TinyPICO ESP32 — Session 5 bench wiring **+ the vibration rig** |

---

## Lesson navigation

1. [Session Overview & Timing](lessons/00-overview.md)
2. [Opening Review — The Show So Far](lessons/01-review.md) — *15 min*
3. [Part A — The Vibration Rig: Your First Motor](lessons/02-part-a-vibration.md) — *35 min*
4. [Part B — Ship It: `main.py` and the Battery](lessons/03-part-b-ship-it.md) — *15 min*
5. [Capstone — Finish the Game](assignment/README.md) — *~105 min studio + demo ceremony, graded*

Something not working? → **[Troubleshooting & FAQ](../../TROUBLESHOOTING.md)** — now with motor-rig entries.

## Code files

| File | What it is |
|---|---|
| [`code/rumble_test.py`](code/rumble_test.py) | Run once after building the vibration rig — clicks, an intensity ramp, and a heartbeat |
| [Session 4, Part C](../04-wifi-iot/lessons/05-part-c-connected-game.md) | The network grafts you'll re-apply — same copyable blocks as before |
| [Session 5's libraries](../05-sound-and-light/README.md) | `rtttl.py` + `songs.py` stay on the board from last session |

## New parts on the bench

| Part | Purpose |
|---|---|
| 10×3 mm coin vibration motor (3 V ERM) | The game's new sense: haptics |
| 2-pin screw terminal block (2.54 mm pitch) | Clamps the motor's hair-thin leads — no soldering |
| NPN transistor (2N2222A) + 1 kΩ resistor | The switch that lets a 12 mA GPIO command an 80 mA motor |
| 1N914 diode | The flyback diode — Session 3's long-promised lesson, finally paid |
| USB power bank | Cuts the last cable: your game runs alone |

## What students will be able to do

- Drive a motor from a GPIO safely: transistor as a switch, base resistor, flyback diode — and explain what each part is *for*
- Use PWM duty as haptic intensity — the third meaning of the same knob (brightness, pitch-volume, rumble)
- Integrate a new output into an existing async architecture without blocking it
- Re-apply the Session 4 network grafts to a changed codebase — the everyday skill of merging features
- Deploy MicroPython as an appliance: `main.py`, headless boot, battery power, and the recovery ritual
- Scope and finish a project against a rubric and a clock — the capstone skill
