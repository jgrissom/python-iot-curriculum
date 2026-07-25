# Session Overview & Timing

[← Back to session home](../README.md) · **Next:** [Opening Review →](01-review.md)

---

Tonight the reaction game gets stage presence: a wait beacon that *breathes* instead of blinking, a victory fanfare played from a Nokia-era ringtone string, and a stick of NeoPixels for stage lighting. The engineering spine is the curriculum's oldest friend in a new costume — a fanfare takes six seconds, and a program that `await`s it is deaf for six seconds. Session 3 taught you not to block on sleep, Session 4 not to block on the network; tonight: **don't block on the show.**

## Time budget (3.5 hours / 210 minutes)

| Block | Activity | Time |
|---|---|---|
| Review | Session 4 assignment — what the connected game taught us | 15 min |
| Warm-up | Two new parts: swap in the passive piezo, wire the NeoPixel stick | 25 min |
| Part A | PWM — dim, breathe, and make pitch from the same trick | 35 min |
| Break | Stretch / troubleshoot | 10 min |
| Part B | RTTTL — parse ringtone strings, build the async player, jukebox | 40 min |
| Part C | NeoPixels — first light, frames, and a comet | 30 min |
| Break | Stretch | 5 min |
| Assignment | Reaction Game: Game-Show Edition | 45 min |
| Wrap-up | Show-off round, Q&A | 5 min |
| *Optional* | *Part D — the light organ (if time permits)* | *+20 min* |

> [!TIP]
> **No network tonight.** Everything in this session — assignment included — runs with zero Wi-Fi, so it works in any venue and at home. If your Session 4 muscle memory reaches for `secrets.py`, relax: the only thing being transmitted tonight is music.

## Learning objectives

By the end of the session, students will be able to:

- Explain PWM's two knobs — duty cycle and frequency — and predict which one a given device responds to.
- Fade and breathe LEDs with `machine.PWM` and `duty_u16`, including the perceptual (gamma) correction.
- Generate musical pitches on a passive piezo and compute any note's frequency from a4 = 440 Hz.
- Parse the RTTTL ringtone format into `(frequency, duration)` pairs with a generator.
- Drive a WS2812 NeoPixel strip with the built-in `neopixel` module, within its power budget.
- Run long sound/light effects with `asyncio.create_task()` so the program never goes deaf — and stop them with `task.cancel()`.

---

[← Back to session home](../README.md) · **Next:** [Opening Review →](01-review.md)
