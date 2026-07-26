# Part A — The Vibration Rig: Your First Motor

⏱️ **35 min**

[← Opening Review](01-review.md) · [Session home](../README.md) · **Next:** [Part B — Ship It →](03-part-b-ship-it.md)

---

Your phone taps you on the wrist with a motor the size of a shirt button — a **coin vibration motor**: a tiny DC motor spinning an off-center weight. Tonight your game gets one. But a motor is not an LED: it drinks ~80 mA, and a GPIO pin can only *supply* ~12 mA. Ask the pin to drive it directly and you'd brown the pin out (or cook it). So this part builds the course's first **driver circuit** — four parts that let a small signal command a big current — and pays a debt outstanding since Session 3: the **flyback diode**.

New parts for this build:

| Part | What it is |
|---|---|
| Coin vibration motor (10×3 mm, 3 V) | The muscle — phone-style ERM haptics |
| — on a pre-soldered header pigtail | Leads soldered to a 2-pin header, joints heat-shrinked, every unit bench-tested before class — it plugs in like a jumper |
| A poker chip (the "haptic puck") | What the motor sticks to — light enough to actually shake; you feel the game through it |
| 2N2222A transistor (TO-92) | The switch: a trickle at the base gates a flood through the collector |
| 1 kΩ resistor | Sets the trickle; protects the GPIO |
| 1N914 diode | The flyback diode — does nothing until the exact microsecond it saves your transistor |

## A1 — mount the motor (the easy bit first)

**Wire with USB unplugged**, as always. Your motor arrives prepped: leads soldered to a 2-pin header, joints sleeved in heat shrink, and every unit tested before class — treat the wires gently and it'll outlive the course.

1. **Stick the motor to your puck** — the poker chip in tonight's kit. Peel the adhesive ring, press it on. Why a chip and not the breadboard? Mass. A coin motor is built to shake a phone's worth of grams; stuck to a big board (or a bench plate), it's trying to shake the desk and you'll feel nothing. A few grams of free-floating chip under your fingertip is its natural habitat — this is also why your phone buzzes *in your hand* but barely on a table.
2. **Tether the leads.** Run a short piece of tape over the wires, pinning them to the breadboard near the header. The #1 way these motors die is the leads tearing at the motor body — the tape makes the *taped span* flex instead of the motor's solder points, and it keeps the puck from wandering farther than its leash.
3. **Plug the header into two free breadboard rows** and note which row got the **red** wire's pin — that's the motor's 3V3 side in the next step. (Electrically the motor has no polarity; red-to-3V3 is a class convention so every bench matches the diagram.)

## A2 — build the driver

The circuit — a **low-side switch**: the transistor sits between the motor and ground, and the GPIO merely asks it to connect the two.

```
3V3 ──┬────────[ motor ]────────┬──── C (collector)
      │                         │
      └────|<|── 1N914 diode ───┘         2N2222A
           (band toward 3V3!)             B (base) ──[ 1 kΩ ]── GPIO 14
                                          E (emitter) ── GND
```

![Wiring diagram for the vibration rig: schematic on the left — motor and 1N914 flyback diode (band toward 3V3) between the 3V3 rail and the 2N2222A's collector, emitter to GND, GPIO 14 through a 1 kΩ resistor to the base; on the right, a breadboard row map — motor header in rows 1–2 (blue wire row 1, red wire row 2), red row jumpered to 3V3, diode spanning rows 1–2 with its band on the red row's side, row 3 left empty for elbow room, a gray jumper from the blue row down to the transistor's collector in row 4, transistor legs C/B/E in rows 4/5/6, resistor from row 5 to row 7, jumpers to GND and GPIO 14 — plus a TO-92 pinout inset](../diagrams/vibration_rig.svg)

*Printable. The row map on the right matches the steps below — the row numbers are just names; any five free rows work.*

1. **Plant the transistor** across three adjacent free rows. With the **flat face toward you, legs down**, the legs are **E – B – C, left to right** — *for the parts in tonight's kit*. (Say it out loud, check it twice — swapped legs is tonight's classic mistake, and it doesn't damage anything, it just mysteriously does nothing.)

> [!WARNING]
> **If you ever buy your own "2N2222":** TO-92 versions of this transistor ship in **two different pinouts** — the PN2222A is E-B-C as above, but the P2N2222A (same function, different manufacturer) is **reversed: C-B-E**. Check the exact part number printed on the package against its datasheet. Tonight's kit parts are verified; your future parts drawer is on its own.
2. **Emitter row → GND rail.**
3. **The red-wire pin's row → 3V3 rail.**
4. **The blue-wire pin's row → the collector row.**
5. **The flyback diode goes *across the motor*:** one end into motor row 1 (the 3V3 side), the other into motor row 2. **The black band faces the 3V3 side.** This is the only polarized part in the build, and backwards it conducts whenever the motor is on — a short that cooks the diode. Band toward 3V3, always.
6. **GPIO 14 → 1 kΩ → the base row.**

That's the whole rig. Plug the USB back in.

## A3 — first rumble (and a surprise)

**Nothing to create — this step happens at the `>>>` prompt.** Before you type: the piezo only *clicked* under plain `on()`. Predict what the motor does.

1. **Ask for everything:**

   ```
   >>> from machine import Pin, PWM
   >>> m = Pin(14, Pin.OUT)
   >>> m.on()
   ```

   **Full rumble.** Not a click — the real thing. A motor is a DC device: steady current means steady spinning, so unlike the piezo it doesn't need a waveform to work. So what's PWM *for* here?

2. **Turn it off, switch to PWM, and find out.** For all of these, **rest the puck on your upturned fingers** — sitting on your fingertips it's freest to shake; pressing down on it squashes the very vibration you're trying to feel:

   ```
   >>> m.off()
   >>> rumble = PWM(Pin(14), freq=200, duty_u16=0)
   >>> rumble.duty_u16(58000)     # ~90% -- full strength
   >>> rumble.duty_u16(30000)     # medium buzz
   >>> rumble.duty_u16(15000)     # a whisper -- barely there
   >>> rumble.duty_u16(0)         # off
   ```

   Duty is **intensity**. The motor's inertia smooths 200 pulses a second into one continuous strength level — the same averaging your eye did for the LED, done by a spinning weight. That completes the course's duty-cycle triptych: **duty = brightness on the LED, ≈ volume on the piezo, = strength on the motor.** Frequency, meanwhile, mattered only to the piezo — try `rumble.freq(500)` mid-buzz and the motor shrugs.

3. **Now find the floor.** The whisper is nearly the bottom — step down from it, `13000`, `12000`, `11000`, until the motor stops. Not "gets quiet": *stops*. Unlike the LED (visible at 1% duty), a motor must overcome its own friction and the flywheel effect of its off-center weight before it can run at all, so somewhere around a fifth of full power it stalls outright (the exact floor varies motor to motor). Two consequences worth keeping:
   - **A dependable "soft" haptic is a *short full-strength pulse*** — 40 ms at 58000 reads as a gentle tap on every motor; a whisper-level duty sits so close to the floor that unit-to-unit variation can silence it. Strength and *duration* are your two real knobs.
   - Dedicated haptic-driver chips (your phone has one) handle this with a **kick**: full power for a few tens of ms to break friction, then drop to a low hum. Now you know why that chip exists.

4. **Why 58000 and not 65535?** The motor is rated 3 V; the rail is 3.3 V. Capping duty at ~90% makes the *average* land on spec — duty as a governor, not just a knob. Use 58000 as your ceiling tonight.
5. **Release it:**

   ```
   >>> rumble.duty_u16(0)
   >>> rumble.deinit()
   ```

## A4 — the rig test

1. **Run [`code/rumble_test.py`](../code/rumble_test.py)** (download, open in Thonny, Run — nothing to upload). Expected show, in order: two plain on/off buzzes, a smooth ramp from whisper to full and back, then four **heartbeats** — lub-DUB, lub-DUB — soft thump, hard thump.
2. **While it runs, rest the puck on your fingers** — haptics are meant to be *felt*. If the heartbeat pattern reads clearly, your game's new sense works.

## Discussion (5 min)

**Q1. The GPIO never touches the motor's current. Trace the actual path of the 80 mA — and then the path of the ~2.6 mA. What exactly is the transistor doing?**

<details>
<summary>Answer</summary>

The 80 mA flows 3V3 → motor → collector → emitter → GND — a loop powered entirely by the 3.3 V rail. The ~2.6 mA (that's (3.3 V − 0.7 V) ÷ 1 kΩ) flows GPIO → 1 kΩ → base → emitter → GND — a separate, tiny loop. The transistor is a *current-operated switch*: the small base current makes the collector-emitter path conduct. The GPIO signs the permission slip; the rail does the lifting. This is amplification — the first time in the course a signal has commanded more power than it carries — and it's the same trick, scaled up, that drives every relay, motor controller, and power stage you'll ever meet.

</details>

**Q2. The flyback diode does absolutely nothing while the motor runs. When does it act, what would happen without it — and why does PWM make it matter 200 times more per second?**

<details>
<summary>Answer</summary>

A motor winding is a coil, and current through a coil refuses to stop instantly. The moment the transistor switches off, the collapsing magnetic field drives the motor's collector-side terminal to whatever voltage it takes to keep the current flowing — a spike of tens of volts aimed at the transistor. The diode — reverse-biased and invisible in normal operation — becomes a short little loop where that current can circulate and die harmlessly. Without it, every turn-off sandblasts the transistor's ratings; it might survive minutes or die on the first click. And PWM at 200 Hz *is* 200 turn-offs per second — the diode isn't insurance for a rare event, it's catching kickback continuously. (This is the exact lesson Session 3's NOTES deferred "to a future motor session." Welcome to it.)

</details>

---

[← Opening Review](01-review.md) · [Session home](../README.md) · **Next:** [Part B — Ship It →](03-part-b-ship-it.md)
