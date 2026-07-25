# Warm-up — Two New Parts on the Bench

⏱️ **25 min**

[← Opening Review](01-review.md) · [Session home](../README.md) · **Next:** [Part A — PWM →](03-part-a-pwm.md)

---

Your Session 3 breadboard stays exactly as built — LEDs, buttons, and all. Tonight adds two parts:

| Part | What it is | Where it goes |
|---|---|---|
| **Passive piezo buzzer** | A speaker with no brain — it only makes the sound *you* wave at it | Swaps into the old buzzer's spot (GPIO 25) |
| **NeoPixel stick (WS2812)** | A row of individually addressable RGB LEDs on one data wire | DIN → GPIO 4, VCC → 3V3, GND → GND |

How many pixels? Doesn't matter yet — the test below **counts them for you**, and every program tonight starts with the same `NUM_PIXELS = ...` constant. Set it once to your stick's number and the whole session follows.

> [!IMPORTANT]
> **Wire with USB unplugged.** Same rule as Session 3, both steps below.

## 1 — Swap the buzzer

The buzzer you've used since Session 3 is an **active** buzzer: it has a tiny oscillator inside, so a steady `on()` makes a steady beep. Pull it out and put it in the kit bag — it's retired for the night.

The **passive piezo** from tonight's kit goes in the same holes: **+ leg → GPIO 25, – leg → GND** (a drop-in swap; the wiring diagram doesn't change). It has no oscillator. What it can do that the old one never could — play any pitch you ask for — is the whole first half of tonight.

## 2 — Wire the NeoPixel stick

Three wires:

| Stick pin | Goes to |
|---|---|
| **DIN** (data in) | GPIO 4 |
| **VCC** (may be marked 5V/VDD) | **3V3** |
| **GND** | GND rail |

- **Direction matters.** The stick has DIN on one end and DOUT on the other (look for the arrows printed on the board — they point *away* from DIN). Data goes in the DIN end; wired backwards, the stick stays politely dark.
- **Yes, 3V3 — even if the pin says 5V.** WS2812 pixels count a signal as "high" only above 70% of their supply voltage. Powered at 5 V, they'd want 3.5 V data — more than the TinyPICO's 3.3 V pins can give, which works on some sticks and flickers on others. Powered at 3.3 V, the math is comfortably on your side. Slightly dimmer, completely reliable. (Real installations use a 5 V supply plus a *level shifter* chip for the data line — now you know why that part exists.)

> [!WARNING]
> **The brightness budget is a hard rule.** Every pixel at full white draws ~60 mA — an 18-pixel stick would pull **~1 A**, several times what the board's 3.3 V regulator can give, and it brown-outs the TinyPICO (symptom: the board mysteriously resets). All of tonight's code keeps color values **≤ 60 out of 255** — that puts even a fully lit 18-pixel stick around 250 mA, inside the budget, and it's plenty bright. Never write `(255, 255, 255)` to the strip; sticks longer than ~20 pixels need their own power supply and don't belong on the 3V3 rail at all.

## 3 — Test the new parts

Download [`code/new_parts_test.py`](../code/new_parts_test.py), open it in Thonny, plug the board back in, and press **Run**. (Nothing to upload — this one just runs from the editor.) Expected show, in order:

1. **Piezo, driven the old way** (`on()`/`off()`) — three soft **clicks**. Not beeps. *Clicks.* If you hear real beeps, the active buzzer is still in the breadboard.
2. **Piezo, driven with PWM** — a smooth rising tone, like a tiny spaceship taking off.
3. **The pixel count** — the strip fills with dim teal, one pixel at a time, while numbers print in the shell. When the strip *stops growing*, the number just printed is your last pixel: **`NUM_PIXELS` = that number + 1.** If it differs from the value at the top of the file, edit it and re-run — and use *your* number in every program tonight.
4. **Full-stick sweep** — every pixel marches through red, green, blue, then everything goes dark. The sweep must reach the very end of the stick; falling short means `NUM_PIXELS` is still set too low.

It ends with a printed all-clear. Anything else → [Troubleshooting](../../../TROUBLESHOOTING.md).

> [!NOTE]
> **About those clicks — that's not a broken buzzer, that's the lesson.** `on()` slams the piezo disc to one position: one click, then silence, because a speaker only makes sound while it's *moving*. Sound **is** vibration — to get a tone you must switch the pin on and off hundreds of times per second, at the frequency you want to hear. Nobody wants to write that loop by hand… and nobody has to. The hardware trick that does it for free is Part A.

---

[← Opening Review](01-review.md) · [Session home](../README.md) · **Next:** [Part A — PWM →](03-part-a-pwm.md)
