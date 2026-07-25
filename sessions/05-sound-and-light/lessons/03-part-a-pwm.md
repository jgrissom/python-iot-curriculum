# Part A — PWM: One Trick, Two Senses

⏱️ **35 min**

[← Warm-up](02-setup.md) · [Session home](../README.md) · **Next:** [Part B — RTTTL →](04-part-b-rtttl.md)

---

A GPIO pin knows two words: on and off. **PWM — pulse-width modulation** — is the hardware trick of saying them *very fast, on a schedule*, and it has exactly two knobs:

- **Frequency** — how many on/off cycles per second (Hz).
- **Duty cycle** — what fraction of each cycle is spent on. In MicroPython it's `duty_u16`, from 0 (always off) to 65535 (always on); 32768 ≈ 50%.

The punchline of this part: your LED cares only about one knob, your piezo only about the other. Same signal, two different senses.

## A1 — the dimmer (duty cycle)

**Nothing to create — this whole step happens at the `>>>` prompt.** The ESP32 has dedicated PWM hardware: you configure it and it toggles the pin forever, no CPU involved.

1. **Start a PWM on the red LED:**

   ```
   >>> from machine import Pin, PWM
   >>> led = PWM(Pin(26), freq=1000, duty_u16=32768)
   ```

   The LED is lit — at 1000 Hz, 50% duty. But is it *half* bright? Hold that thought.

2. **Play dimmer switch** — type each line, watch the LED between them:

   ```
   >>> led.duty_u16(65535)    # 100% -- full brightness
   >>> led.duty_u16(32768)    # 50%
   >>> led.duty_u16(5000)     # ~8%
   >>> led.duty_u16(800)      # ~1% -- still clearly visible!
   >>> led.duty_u16(0)        # off
   ```

   At 1000 Hz the LED genuinely turns fully on and fully off a thousand times a second. Your eye can't follow anything faster than ~60 flickers a second, so it reports the *average* — duty cycle **is** brightness. And notice: 50% looked *way* more than half as bright, and 1% is far from invisible — your eye's brightness sense is logarithmic, not linear. That fact matters in A2.

3. **Now abuse the other knob** — set the duty back to 50%, then lower the frequency until the trick collapses:

   ```
   >>> led.duty_u16(32768)
   >>> led.freq(200)          # still smooth
   >>> led.freq(60)           # ...borderline...
   >>> led.freq(20)           # visible flicker!
   ```

   Frequency only needs to be "fast enough to fool the eye" — beyond that, the LED doesn't care about it. Remember which knob mattered here; the piezo will invert it.

4. **Release the pin:**

   ```
   >>> led.deinit()
   ```

   **Always `deinit()` before using the pin as a plain `Pin` again** — a pin can't serve two masters, and "my LED ignores `.on()`" almost always means a PWM still owns it.

## A2 — the breathing LED

Blinking is binary. *Breathing* — the smooth swell and fade of a sleeping laptop's light — is just duty cycle swept smoothly over time. And because your eye is logarithmic, we square the level instead of using it raw (conveniently, `255 * 255 = 65025` — a squared 8-bit level is almost exactly the `u16` range).

1. **Create the file:** *File → New*, save as `breathe.py` → **This computer**.
2. **Type this in:**

   ```python
   from machine import Pin, PWM
   import uasyncio as asyncio

   led1 = PWM(Pin(26), freq=1000, duty_u16=0)   # red
   led2 = PWM(Pin(27), freq=1000, duty_u16=0)   # green


   async def breathe(led, step_s):
       """Sweep brightness up and down forever, one small step at a time."""
       while True:
           for level in range(0, 256, 5):          # inhale: 0 -> 255
               led.duty_u16(level * level)         # squared = perceptually smooth
               await asyncio.sleep(step_s)
           for level in range(255, -1, -5):        # exhale: 255 -> 0
               led.duty_u16(level * level)
               await asyncio.sleep(step_s)


   async def main():
       asyncio.create_task(breathe(led1, 0.02))    # slow, calm red
       asyncio.create_task(breathe(led2, 0.008))   # quick, eager green
       while True:
           await asyncio.sleep(1)

   try:
       asyncio.run(main())
   finally:
       led1.duty_u16(0); led1.deinit()
       led2.duty_u16(0); led2.deinit()
   ```

3. **Run it.** You should see both LEDs breathing — red slow and calm, green quick and eager — each its own coroutine, ~50 gentle updates a second. And the CPU is nearly idle, because the PWM hardware does the thousand-times-a-second part. Software picks the brightness; hardware holds it.
4. **Stop it** (Ctrl+C, then Ctrl+F2 for a clean slate — the `finally` block leaves the pins released either way).

This coroutine is almost exactly the assignment's breathing wait beacon — remember where you left it.

## A3 — the other knob (frequency)

Now the piezo. It converts voltage swings into air pressure swings — so it doesn't care what fraction of the time the pin is high, it cares **how many times per second the signal repeats**. That's pitch.

1. **Create the file:** *File → New*, save as `siren.py` → **This computer**.
2. **Type this in:**

   ```python
   from machine import Pin, PWM
   import time

   buzz = PWM(Pin(25), freq=440, duty_u16=32768)   # concert A -- orchestras tune to this
   time.sleep(1)

   buzz.freq(262); time.sleep(1)     # middle C
   buzz.freq(524); time.sleep(1)     # C one octave up: exactly double
   buzz.freq(1048); time.sleep(1)    # and double again

   for f in range(200, 2000, 10):    # a rising siren sweep
       buzz.freq(f)
       time.sleep(0.005)

   buzz.duty_u16(0)                  # silence: duty 0 (PWM stays configured)
   buzz.deinit()
   ```

3. **Run it and listen:** one second of concert A, then three C's — and **each doubling of the frequency raises the pitch exactly one octave**: 262 → 524 → 1048 all sound like "the same note, higher." Pitch, like brightness, is perceived logarithmically — Part B turns that into a formula that generates every note on a piano. Then the siren sweeps up and the script silences itself.
4. **Improvise at the `>>>`** — the script released the pin, so make a fresh one:

   ```
   >>> from machine import Pin, PWM
   >>> buzz = PWM(Pin(25), freq=440, duty_u16=32768)
   >>> buzz.freq(100)
   >>> buzz.freq(1000)
   >>> buzz.freq(5000)
   ```

   Anything from 100 to 5000 Hz — find where your piezo is loudest (usually 2–4 kHz, its resonance).
5. **Now try the *wrong* knob, mid-tone:**

   ```
   >>> buzz.freq(880)
   >>> buzz.duty_u16(10000)
   >>> buzz.duty_u16(50000)
   >>> buzz.duty_u16(32768)
   ```

   The *pitch* doesn't budge; the timbre/loudness shifts a little. The piezo reads the frequency knob and mostly shrugs at the duty knob — the exact mirror of the LED. (Duty 0 is the exception: no swings at all is how we make silence between notes.)
6. **Quiet the bench:**

   ```
   >>> buzz.duty_u16(0)
   >>> buzz.deinit()
   ```

> [!NOTE]
> `time.sleep()` in `siren.py` — has the course gone soft? No: this is a plain synchronous script with one job, Session 3's "blocking is a choice, sometimes the right one." The moment a melody has to share the board with a running game, that choice is wrong — which is Part B's whole story.

## Discussion (5 min)

**Q1. One PWM signal, two knobs, two devices that each obey a different knob. What's the underlying reason the LED tracks duty while the piezo tracks frequency?**

<details>
<summary>Answer</summary>

Each device is a filter that averages the signal differently. Your eye averages over ~1/60 s — at 1000 Hz it can't see individual cycles, so all that survives is the on-time fraction: duty = brightness, frequency invisible (until you drop below the eye's rate and it flickers). Your ear does the opposite: it's a *change* detector that hears repetition rates from ~20 Hz to ~20 kHz, so the cycle rate itself is the signal: frequency = pitch. Same square wave; the receiver decides what it means.

</details>

**Q2. Why did the passive piezo click — once — under plain `on()`, and why couldn't any amount of `on()` make a tone?**

<details>
<summary>Answer</summary>

`on()` is a single edge: the disc jumps to its flexed position and stays — one pressure pulse, one click, then silence, because constant position means constant pressure means no sound. A tone requires the disc to move back and forth continuously at an audible rate. You could hand-write a toggle loop (Session 3's A2 dead-end, reborn), but the PWM peripheral is that loop as hardware: set `freq`, and it toggles forever while your code does something better.

</details>

---

[← Warm-up](02-setup.md) · [Session home](../README.md) · **Next:** [Part B — RTTTL →](04-part-b-rtttl.md)
