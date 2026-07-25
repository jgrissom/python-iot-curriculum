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
5. **Make it yours** — three variations, easiest first; run after each. Try each one before opening its triangle.

**The bouncing dot** — one lit pixel per note instead of a bar.

<details>
<summary>Answer — the bouncing dot</summary>

Only `painter()` changes — the height math already tells you *where* the dot goes:

```python
async def painter():
    """~50 fps: one dot, bouncing to the pitch."""
    while True:
        if state["freq"]:
            pos = bar_height(state["freq"]) - 1     # 0-based pixel index
            for i in range(NUM_PIXELS):
                np[i] = (0, 40, 25) if i == pos else (0, 0, 0)
        else:
            for i in range(NUM_PIXELS):
                np[i] = (0, 0, 0)
        np.write()
        await asyncio.sleep(0.02)
```

Notice `conductor()` didn't change at all — the whole point of meeting only at `state["freq"]`.

</details>

**Color by pitch** — the bar keeps its height, but *wears the note's color*: low notes green, high notes red.

<details>
<summary>Answer — color by pitch</summary>

Add a pitch-to-color mapping (same three-octave span as `bar_height`), then paint the whole bar with it — this *replaces* the per-pixel `bar_color(i)` gradient:

```python
def pitch_color(freq):
    """Low notes green, high notes red -- the bar's color IS the pitch."""
    octaves_up = math.log(freq / 131, 2)
    frac = max(0.0, min(1.0, octaves_up / 3))
    return (round(60 * frac), round(60 * (1 - frac)), 0)


async def painter():
    """~50 fps: bar height AND color both follow the note."""
    while True:
        if state["freq"]:
            height = bar_height(state["freq"])
            color = pitch_color(state["freq"])
        else:
            height, color = 0, (0, 0, 0)
        for i in range(NUM_PIXELS):
            np[i] = color if i < height else (0, 0, 0)
        np.write()
        await asyncio.sleep(0.02)
```

Height and color now encode the same information two ways — redundant on purpose, like the green GO LED next to the green DotStar.

</details>

**The light-organ jukebox** — steal Part B's buttons: A skips songs, B stops, and the painter never misses a frame.

<details>
<summary>Answer — the light-organ jukebox</summary>

Replace the setlist `main()` with a DJ loop. `conductor()` is already safe to cancel — its `finally` silences the piezo *and* zeroes `state["freq"]`, which is what makes the strip go dark instead of freezing mid-bar:

```python
async def dj():
    btnA = Pin(18, Pin.IN, Pin.PULL_UP)        # blue cap: next song
    btnB = Pin(5, Pin.IN, Pin.PULL_UP)         # yellow cap: silence!
    song_task = None
    idx = 0
    print("Light-organ jukebox: A = next song, B = stop")
    while True:
        if btnA.value() == 0:
            if song_task:
                song_task.cancel()
            song = songs.ALL[idx % len(songs.ALL)]
            idx += 1
            song_task = asyncio.create_task(conductor(song))
            await asyncio.sleep(0.3)           # debounce
        if btnB.value() == 0:
            if song_task:
                song_task.cancel()
            await asyncio.sleep(0.3)
        await asyncio.sleep(0.02)


async def main():
    asyncio.create_task(painter())
    await dj()
```

Press A mid-song and watch closely: the sound stops, the bar collapses, the next song's bar starts — and the painter task never restarted, it just kept reading `state["freq"]` at 50 fps while the world changed around it.

</details>

> [!NOTE]
> Notice what made this a ten-line trick instead of a rewrite: `parse()` never knew about pixels, `painter()` never knew about RTTTL — they meet only at `state["freq"]`. Two tasks *communicating through shared state* was Session 3's trickiest idea; tonight it's just how you build a light organ. And `await conductor(...)` in the setlist loop is a deliberate `await` of a slow thing — the rare case where "block this coroutine on the show" is exactly right, because a setlist *is* sequential. (The painter, on its own task, dances on regardless.)

---

[← Part C](05-part-c-neopixels.md) · [Session home](../README.md) · **Next:** [Assignment →](../assignment/README.md)
