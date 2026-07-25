# Part D — The Light Organ *(optional)*

⏱️ **~20 min** · for benches that finish early — nothing in the assignment depends on this

[← Part C](05-part-c-neopixels.md) · [Session home](../README.md) · **Next:** [Assignment →](../assignment/README.md)

---

In the 1970s you could buy a "light organ" — a box that made lamps dance to music. Yours will be better: since *your program* decides every note, no microphone is needed — the code that plays the song can simply *tell* the code that paints the lights what note is sounding. Two tasks, one shared dict. This is Session 3's `flashing` flag all grown up.

It's also why Part B insisted that parsing and playing are separate jobs: `rtttl.parse()` is about to feed two consumers at once.

## The design

```
conductor task ──> plays each note on the piezo
      │
      └──> state["freq"] = the note now sounding (0 = silence)
                    │
painter task <──────┘  reads it ~50x/s, paints the strip to match
```

The mapping: pitch → bar height, using the fact you proved in Part A — octaves are *doublings*. `math.log(f / 131, 2)` counts how many octaves the note sits above C3 (131 Hz); the strip covers three octaves, so multiply by `NUM_PIXELS / 3` pixels per octave — the code below is length-agnostic, and a longer stick simply gets finer pitch resolution.

## Build it

1. **Check the board copies are in place** (they are if you finished B3): at the `>>>`, `import rtttl, songs` should succeed silently.
2. **Create the file:** *File → New*, save as `light_organ.py` → **This computer**.
3. **Type this in:**

   ```python
   from machine import Pin, PWM
   import uasyncio as asyncio
   import neopixel
   import math
   import rtttl, songs

   NUM_PIXELS = 18          # <- YOUR stick's count, from the warm-up test
   np = neopixel.NeoPixel(Pin(4), NUM_PIXELS)
   piezo = PWM(Pin(25), freq=440, duty_u16=0)

   state = {"freq": 0}                      # the one note currently sounding


   async def conductor(song):
       """rtttl.play(), but narrating every note into shared state."""
       print("Now playing:", rtttl.title(song))
       try:
           for freq, ms in rtttl.parse(song):
               state["freq"] = freq
               if freq:
                   piezo.freq(freq)
                   piezo.duty_u16(32768)
               else:
                   piezo.duty_u16(0)
               await asyncio.sleep_ms(max(ms - 25, 10))
               piezo.duty_u16(0)
               state["freq"] = 0            # the articulation gap goes dark too
               await asyncio.sleep_ms(25)
       finally:
           piezo.duty_u16(0)
           state["freq"] = 0


   def bar_height(freq):
       """Map a frequency to 1..NUM_PIXELS: C3 (131 Hz) -> 1 pixel,
       three octaves above it -> the full stick."""
       octaves_up = math.log(freq / 131, 2)
       return max(1, min(NUM_PIXELS, 1 + round(octaves_up * NUM_PIXELS / 3)))


   def bar_color(i):
       """Green at the bottom of the stick shading to red at the top --
       proportional, so it works for any NUM_PIXELS."""
       frac = i / (NUM_PIXELS - 1)
       return (round(60 * frac), round(60 * (1 - frac)), 0)


   async def painter():
       """~50 fps: light a bar as tall as the current note is high."""
       while True:
           height = bar_height(state["freq"]) if state["freq"] else 0
           for i in range(NUM_PIXELS):
               np[i] = bar_color(i) if i < height else (0, 0, 0)
           np.write()
           await asyncio.sleep(0.02)


   async def main():
       asyncio.create_task(painter())
       for song in songs.ALL:
           await conductor(song)                    # await on purpose: a setlist
           await asyncio.sleep(1)                   # is sequential by nature

   try:
       asyncio.run(main())
   finally:
       piezo.duty_u16(0); piezo.deinit()
       for i in range(NUM_PIXELS):
           np[i] = (0, 0, 0)
       np.write()
   ```

4. **Run it and watch a song or two.** Melodies have *shape*, and the bar makes it visible: scales climb the strip, octave jumps leap it, rests snap it dark. The shell prints each title as the setlist advances; Ctrl+C when you've had enough — the `finally` blocks leave the bench silent and dark.
5. **Make it yours** (run after each experiment):
   - Swap `bar_height` for a **position** mapping (one lit pixel per note, a bouncing dot).
   - Color by pitch instead of height.
   - Steal the jukebox's buttons so A skips songs while the painter never stops.

> [!NOTE]
> Notice what made this a ten-line trick instead of a rewrite: `parse()` never knew about pixels, `painter()` never knew about RTTTL — they meet only at `state["freq"]`. Two tasks *communicating through shared state* was Session 3's trickiest idea; tonight it's just how you build a light organ. And `await conductor(...)` in the setlist loop is a deliberate `await` of a slow thing — the rare case where "block this coroutine on the show" is exactly right, because a setlist *is* sequential. (The painter, on its own task, dances on regardless.)

---

[← Part C](05-part-c-neopixels.md) · [Session home](../README.md) · **Next:** [Assignment →](../assignment/README.md)
