# Session Overview & Timing

[← Back to session home](../README.md) · **Next:** [Opening Review →](01-review.md)

---

The last session is mostly yours. Two short taught parts — a motor-driver rig (the transistor and flyback diode your kit has been waiting three sessions for) and the five-minute ritual that turns a bench experiment into an appliance — then the longest build block of the course: **finish the game.** Networking restored, rumble integrated, extras chosen from a menu, and a demo ceremony where thirteen battery-powered arcade machines fight for the leaderboard with no laptops in sight.

## Time budget (3.5 hours / 210 minutes)

| Block | Activity | Time |
|---|---|---|
| Review | Session 5 assignment — the show so far, and what's missing | 15 min |
| Part A | The vibration rig — transistor, flyback diode, PWM rumble | 35 min |
| Break | Stretch / troubleshoot | 10 min |
| Part B | Ship it — `main.py`, headless boot, power bank | 15 min |
| **Capstone** | **Finish the game** — studio time with checkpoints | ~105 min |
| Break | Stretch (whenever suits your build) | 5 min |
| Demo ceremony | Tournament on the leaderboard — battery power only | 20 min |
| Wrap-up | The course, in three villains | 5 min |

> [!TIP]
> Tonight needs the network again — same setup as Session 4 (`secrets.py`, cloud scoreboard, hotspot fallback). Everything was proven then; tonight it just has to keep working while the fanfare plays and the motor rumbles.

## Learning objectives

By the end of the session, students will be able to:

- Explain why a GPIO can't drive a motor directly, and what the transistor, base resistor, and flyback diode each contribute.
- Control haptic intensity with PWM duty — and name all three meanings duty has had in this course.
- Merge previously-written features (the Session 4 grafts) into a codebase that has changed since — without breaking either.
- Deploy a MicroPython program as `main.py`, run it headless on battery power, and recover a board that auto-runs.
- Finish: scope a build against a rubric, a menu, and a clock.

---

[← Back to session home](../README.md) · **Next:** [Opening Review →](01-review.md)
