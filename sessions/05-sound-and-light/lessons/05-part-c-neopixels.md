# Part C — NeoPixels: Stage Lighting

⏱️ **30 min**

[← Part B](04-part-b-rtttl.md) · [Session home](../README.md) · **Next:** [Part D — The Light Organ (optional) →](06-part-d-light-organ.md)

---

The DotStar taught you addressable color on one pixel. The NeoPixel stick is a whole row of them on **one data wire** — each WS2812 pixel reads its 3 bytes from the incoming stream and forwards the rest down the line. Chain 8 or 300, still one wire. This is the LED that lights stadium signs, and MicroPython supports it **out of the box** — no library upload, no power-enable call, no SPI setup. Remember the Session 3 DotStar ritual — download the driver, upload it to the board, exact filename, `set_dotstar_power(True)`? The `neopixel` driver is *frozen into the firmware*: it ships inside MicroPython itself. That's what "batteries included" means at the firmware level. (Fairness note: the DotStar earns its keep elsewhere — it's the price of being *onboard*.)

## C1 — first light

**Nothing to create yet — this whole step happens at the `>>>` prompt.**

1. **Set up the strip** (use *your* pixel count from the warm-up test):

   ```
   >>> from machine import Pin
   >>> import neopixel
   >>> NUM_PIXELS = 18                # <- YOUR stick's count
   >>> np = neopixel.NeoPixel(Pin(4), NUM_PIXELS)
   ```

2. **Assign some colors** — and watch the strip while you do:

   ```
   >>> np[0] = (60, 0, 0)             # pixel 0: red
   >>> np[3] = (0, 60, 0)             # pixel 3: green
   >>> np[7] = (0, 0, 60)             # pixel 7: blue
   ```

   *Nothing happens.* That's correct — keep going.

3. **Now send the frame:**

   ```
   >>> np.write()
   ```

   All three pixels light **at once**. Unlike the DotStar (whose library quietly pushed every change), NeoPixels are explicitly **frame-based**: `np[i] = ...` edits a buffer in RAM; `write()` streams the whole buffer down the wire in one precisely-timed burst. Compose the frame, then show the frame. Every display you've ever used works this way — now you're doing it by hand.

4. **Clear the stage** (paste the whole loop; the prompt handles it):

   ```python
   for i in range(NUM_PIXELS):
       np[i] = (0, 0, 0)
   np.write()
   ```

> [!WARNING]
> Values are capped at **≤ 60 per channel** in every example tonight — that's the [power budget from setup](02-setup.md), not politeness. A full-white strip can brown-out the board.

## C2 — frames over time = animation

An animation is just frames with awaits between them. Build the showpiece — a comet with a fading tail. Each frame: clear the buffer, paint the head bright, then paint each trailing pixel dimmer. The dimming is a bit-shift — `>> t` halves each channel per tail step, which is cheap *and* respects the power budget by construction.

1. **Create the file:** *File → New*, save as `strip_show.py` → **This computer**.
2. **Type this in** — the two helpers at the top reappear verbatim in the assignment starter, so this is not throwaway typing:

   ```python
   from machine import Pin
   import uasyncio as asyncio
   import neopixel

   NUM_PIXELS = 18          # <- YOUR stick's count
   np = neopixel.NeoPixel(Pin(4), NUM_PIXELS)


   def strip_fill(color):
       """Every pixel the same color, in one frame."""
       for i in range(NUM_PIXELS):
           np[i] = color
       np.write()


   async def strip_flash(color, times=3):
       """Flash the whole strip on and off."""
       for _ in range(times):
           strip_fill(color)
           await asyncio.sleep(0.15)
           strip_fill((0, 0, 0))
           await asyncio.sleep(0.15)


   async def strip_comet(color, laps=3, tail=3):
       """A bright head sweeps the strip, dragging a fading tail."""
       for step in range(laps * NUM_PIXELS):
           head = step % NUM_PIXELS
           for i in range(NUM_PIXELS):
               np[i] = (0, 0, 0)
           for t in range(tail + 1):                  # t=0 is the head itself
               i = head - t
               if i >= 0:
                   np[i] = (color[0] >> t, color[1] >> t, color[2] >> t)
           np.write()
           await asyncio.sleep(0.06)
       strip_fill((0, 0, 0))                          # leave the stage dark


   async def main():
       await strip_comet((0, 0, 60))                  # a blue comet, three laps
       await strip_flash((60, 40, 0), times=2)        # two amber flashes
       await strip_comet((60, 0, 0), laps=2, tail=5)  # long-tailed red one

   asyncio.run(main())
   ```

3. **Run it.** A blue comet laps the strip three times, two amber flashes, then a long-tailed red comet — and the stage goes dark. ~16 frames a second, and it costs the scheduler almost nothing: these are *polite* animations, `await`ing between every frame.
4. **Make it yours** — change colors, `laps`, `tail`, the frame delay; run after each change.
5. **The connoisseur's test:** add a breathing-LED task to `main()` (you have the coroutine from Part A) and confirm comet and breath run together without a hiccup.

<details>
<summary>Answer</summary>

Three additions: the PWM import and LED setup, Part A's coroutine pasted in unchanged, and one `create_task()` line in `main()`:

```python
from machine import Pin, PWM                     # PWM is new here

led1 = PWM(Pin(26), freq=1000, duty_u16=0)       # red LED, Part A style


async def breathe(led, step_s=0.02):             # straight from Part A
    while True:
        for level in range(0, 256, 5):
            led.duty_u16(level * level)
            await asyncio.sleep(step_s)
        for level in range(255, -1, -5):
            led.duty_u16(level * level)
            await asyncio.sleep(step_s)


async def main():
    asyncio.create_task(breathe(led1))           # runs underneath everything
    await strip_comet((0, 0, 60))
    await strip_flash((60, 40, 0), times=2)
    await strip_comet((60, 0, 0), laps=2, tail=5)

asyncio.run(main())
led1.duty_u16(0)                                 # leave the pin clean
led1.deinit()
```

Note the shape: the breath is `create_task()` (it should run *underneath* the whole show), while the strip effects are `await`ed in sequence (a playlist is sequential on purpose). Choosing per-effect between those two is the exact skill the assignment grades.

</details>

One style note before you invent your own effects: animation code grows index arithmetic and conditionals *fast*. The comet stays readable because each frame is computed in named steps — `head` first, then a plain `if i >= 0` guard for the tail. When an effect of yours turns into line-noise, simplify the motion, not the syntax.

## Discussion (5 min)

**Q1. Why do NeoPixels make you call `write()` instead of updating on every `np[i] = ...` like the DotStar library did?**

<details>
<summary>Answer</summary>

One wire, no clock: WS2812 data is a single precisely-timed burst, and every pixel *before* the one you changed has to be re-sent anyway — the stream passes through them. Auto-writing on each assignment would re-transmit the strip per pixel touched (our comet edits up to 12 pixels per frame — 12 bursts instead of 1). Buffer-then-write batches the work *and* gives you atomic frames: viewers never see a half-painted strip. The DotStar could afford auto-write because it has a clock wire, no strict timing, and we drove exactly one pixel.

</details>

**Q2. Your comet at `(60, 0, 0)`: roughly what current does it draw, worst frame? And your whole stick at `(255, 255, 255)`? (Rule of thumb: ~60 mA per pixel at full white, ~20 mA per channel at 255.)**

<details>
<summary>Answer</summary>

Comet: head 60/255 on one channel ≈ 5 mA, tail pixels half that and half again — the worst frame is maybe 10 mA total, *regardless of stick length* (a comet lights the same handful of pixels on any strip). Full white is the opposite — it scales with every pixel you own: an 18-pixel stick is 18 × 60 mA ≈ **1.1 A**, before the ESP32's own draw, through a 3.3 V regulator good for a fraction of that — hence brownout resets. The scary part: brightness *feels* linear but current *is* linear, while your logarithmic eye barely distinguishes 60 from 255. You give up almost nothing by staying dim — one of the friendliest asymmetries in embedded work.

</details>

---

[← Part B](04-part-b-rtttl.md) · [Session home](../README.md) · **Next:** [Part D — The Light Organ (optional) →](06-part-d-light-organ.md)
