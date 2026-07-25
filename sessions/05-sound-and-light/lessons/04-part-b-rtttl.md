# Part B — RTTTL: Your Board Plays Ringtones

⏱️ **40 min**

[← Part A](03-part-a-pwm.md) · [Session home](../README.md) · **Next:** [Part C — NeoPixels →](05-part-c-neopixels.md)

---

In the late 1990s, Nokia needed to squeeze entire ringtones through text messages, and **RTTTL** (Ring Tone Text Transfer Language) was the result: a whole melody in one compact string. The internet still holds thousands of them, and by the end of this part your board plays any of them — because you'll have written the parser. This is the session's Python workout: string surgery in, `(frequency, duration)` pairs out, and PWM does the rest.

## B1 — anatomy of a ringtone

An RTTTL string has three sections separated by colons — **name : defaults : notes**:

```
scale:d=8,o=5,b=125:c,d,e,f,g,a,b,c6
```

- **`d=8`** — default **d**uration: an eighth note (the number is the fraction: 4 = quarter, 16 = sixteenth…).
- **`o=5`** — default **o**ctave.
- **`b=125`** — tempo in **b**eats (quarter notes) per minute.
- Then the notes, comma-separated. Each is `[duration] pitch [#] [.] [octave]`, and *everything except the pitch letter is optional* — missing pieces fall back to the defaults. So in the string above, `c` means "eighth note, C, octave 5", while `c6` overrides just the octave. `p` is a rest, `#` is a sharp, and a dot stretches the note by half, just like sheet music.

> [!TIP]
> **Do this:** dissect one at the REPL — no board hardware needed, this is pure Python:
> ```python
> song = "scale:d=8,o=5,b=125:c,d,e,f,g,a,b,c6"
> name, defaults, notes = song.split(":")
> name                      # 'scale'
> defaults.split(",")       # ['d=8', 'o=5', 'b=125']
> notes.split(",")          # ['c', 'd', 'e', ... 'c6']
> ```
> Three lines of string methods and the format is already lying open. That's the whole art of parsing: split on the big separators first, then deal with the pieces.

## B2 — the pitch formula

Part A found that +1 octave = ×2 frequency. Western music slices each octave into **12 semitones**, all equal *ratios* — so one semitone is a factor of 2^(1/12) ≈ 1.0595. Anchor the whole system to one agreed note — **a4 = 440 Hz** — and every note is:

```
freq = 440 × 2^(semitones away from a4 ÷ 12)
```

Turn it into code (this goes in a new file — it's the first piece of `rtttl.py`):

```python
# Semitone offsets within one octave (c = 0 ... b = 11)
SEMITONES = {"c": 0, "c#": 1, "d": 2, "d#": 3, "e": 4, "f": 5,
             "f#": 6, "g": 7, "g#": 8, "a": 9, "a#": 10, "b": 11}


def note_freq(pitch, octave):
    """Frequency in Hz for a pitch name ('c'..'b', sharps allowed) and octave.
    Anchored at a4 = 440 Hz; every semitone is a factor of 2**(1/12)."""
    steps = SEMITONES[pitch] + (octave - 4) * 12 - 9   # semitones from a4
    return round(440 * 2 ** (steps / 12))
```

The `- 9` is because `a` sits 9 semitones above `c` in our table, and we're anchoring on `a`, not `c`.

> [!TIP]
> **Do this:** press **Run** on your file. The shell stays quiet — running it only *defines* the function (and no `import` is needed: Run executes the file straight into the shell's namespace, as if you'd typed it all at the `>>>`). Now interrogate it at the prompt, one line at a time — the REPL echoes each result, and these are the numbers you should see:
> ```
> >>> note_freq("a", 4)
> 440
> >>> note_freq("a", 5)
> 880
> >>> note_freq("c", 5)
> 523
> >>> note_freq("c#", 5)
> 554
> ```
> The anchor by construction; one octave = exactly double; soprano C; and one semitone above it, ×1.0595. (Later, once the finished file is uploaded to the board as a library, other programs will reach the same function as `rtttl.note_freq(...)` — `import` is for libraries; Run is for the file you're building.)
>
> Twelve dictionary entries and one line of math generate the entire piano. When a formula replaces a table of 88 magic numbers, you've found the structure underneath.

## B3 — the parser

Durations are the last piece. At `b` beats per minute, one quarter note lasts `60000 / b` ms, so a whole note is four times that — and every note's length is `whole / duration` (×1.5 if dotted). Now walk each token character by character: optional digits, then the pitch letter, then optional `#`, `.`, octave.

Here's the full parser — a **generator** that yields one `(freq_hz, duration_ms)` pair per note, with `0` Hz meaning rest:

```python
def parse(song):
    """Yield (freq_hz, duration_ms) for every note. freq 0 = rest."""
    _, defaults, notes = song.split(":")

    d = {"d": 4, "o": 5, "b": 63}                # the spec's defaults
    for part in defaults.split(","):
        key, _, val = part.strip().partition("=")
        d[key] = int(val)

    whole_ms = 4 * 60000 // d["b"]               # b = quarter-note beats/min

    for token in notes.split(","):
        token = token.strip().lower()

        i = 0                                    # 1. leading duration digits
        while i < len(token) and token[i].isdigit():
            i += 1
        duration = int(token[:i]) if i else d["d"]

        pitch = token[i]                         # 2. pitch letter (+ sharp)
        i += 1
        if i < len(token) and token[i] == "#":
            pitch += "#"
            i += 1

        dotted = False                           # 3. dot and/or octave,
        octave = d["o"]                          #    in either order
        while i < len(token):
            if token[i] == ".":
                dotted = True
            elif token[i].isdigit():
                octave = int(token[i])
            i += 1

        ms = whole_ms // duration
        if dotted:
            ms += ms // 2

        yield (0 if pitch == "p" else note_freq(pitch, octave), ms)
```

> [!TIP]
> **Do this:** feed it the scale and read the output like a musician:
> ```python
> for freq, ms in parse("scale:d=8,o=5,b=125:c,d,e,f,g,a,b,c6"):
>     print(freq, "Hz for", ms, "ms")
> ```
> Eight rising frequencies, 240 ms each (an eighth note at 125 bpm — check the math). No sound yet, and that's the point: **parsing and playing are separate jobs.** A generator of `(freq, ms)` pairs can feed a piezo, a light show (Part D does exactly that), or a test print — the parser doesn't care.

> [!NOTE]
> Why `yield` instead of building a list? A generator hands over one note at a time, as asked — no 60-note list sitting in RAM, and playback can be cancelled mid-song without having done the work of parsing the rest. On a microcontroller, "compute it when asked" is a habit worth building.

The finished library — `note_freq`, `parse`, a `title()` helper, and the `play()` you're about to meet — is [`code/rtttl.py`](../code/rtttl.py). **Upload it to the board like a library** (Thonny → View → Files → right-click → *Upload to /*), same dance as `async_http.py` last session. Also upload [`code/songs.py`](../code/songs.py) — a starter songbook so nobody has to type Beethoven.

## B4 — play it (wrongly, then rightly)

The obvious player is a loop with `time.sleep()`. You already know what that costs — so let's *measure* it. Predict first: with a breathing LED task running, what does the red LED do during a 20-second song?

```python
from machine import Pin, PWM
import uasyncio as asyncio
import time
import rtttl, songs

led1 = PWM(Pin(26), freq=1000, duty_u16=0)
piezo = PWM(Pin(25), freq=440, duty_u16=0)


async def breathe(led, step_s=0.02):
    while True:
        for level in range(0, 256, 5):
            led.duty_u16(level * level)
            await asyncio.sleep(step_s)
        for level in range(255, -1, -5):
            led.duty_u16(level * level)
            await asyncio.sleep(step_s)


async def play_blocking(song):                 # it's 'async' -- but it's a lie
    for freq, ms in rtttl.parse(song):
        piezo.duty_u16(32768 if freq else 0)
        if freq:
            piezo.freq(freq)
        time.sleep(ms / 1000)                  # <-- the crime
        piezo.duty_u16(0)
        time.sleep(0.025)


async def main():
    asyncio.create_task(breathe(led1))
    await asyncio.sleep(3)                     # three good breaths...
    print("song starts -- watch the red LED!")
    await play_blocking(songs.ODE_TO_JOY)
    print("song over -- the LED lives again")
    while True:
        await asyncio.sleep(1)

try:
    asyncio.run(main())
finally:
    led1.duty_u16(0); led1.deinit()
    piezo.duty_u16(0); piezo.deinit()
```

> [!TIP]
> **Do this:** run it. The LED breathes… the song starts… and the LED **freezes mid-breath, for the entire melody** — nearly twenty seconds of paralysis. Every `time.sleep()` between notes is stolen from every other task. In your game this would be buttons dead through the whole victory fanfare. You predicted it; now you've seen it.

The fix is the same as it's been all course — sleep asynchronously. This is `rtttl.py`'s real `play()`:

```python
async def play(pwm, song, gap_ms=25):
    """Play one RTTTL song on a PWM pin without blocking the event loop."""
    try:
        for freq, ms in parse(song):
            if freq:
                pwm.freq(freq)
                pwm.duty_u16(32768)
            else:
                pwm.duty_u16(0)                  # rest
            await asyncio.sleep_ms(max(ms - gap_ms, 10))
            pwm.duty_u16(0)                      # a hair of silence between
            await asyncio.sleep_ms(gap_ms)       # notes, so repeats don't merge
    finally:
        pwm.duty_u16(0)                          # never leave a note stuck on
```

Three details, each earning its place:

- **`asyncio.sleep_ms(...)`** — new tool, uasyncio-only: sleep in integer milliseconds, music's native unit. Same yielding behavior as `asyncio.sleep()`.
- **The `gap_ms` of silence** — without it, `e,e,e` plays as one long *eeee*. Articulation, a musician would say.
- **The `try/finally`** — in a moment you'll *cancel* this coroutine mid-note. Cancellation stops a task wherever it's awaiting; without the `finally`, a cancelled song leaves its last note droning forever. Cleanup that must survive cancellation goes in `finally` — remember this one.

In `main()`, replace `await play_blocking(...)` with `await rtttl.play(piezo, songs.ODE_TO_JOY)` and run again: **the LED breathes straight through the song.** Two tasks, one CPU, zero rudeness.

### The jukebox

Finale: music on demand, from the buttons — and your first `task.cancel()`:

```python
async def jukebox():
    btnA = Pin(18, Pin.IN, Pin.PULL_UP)        # blue cap: next song
    btnB = Pin(5, Pin.IN, Pin.PULL_UP)         # yellow cap: silence!
    song_task = None
    idx = 0
    print("Jukebox ready: A = next song, B = stop")
    while True:
        if btnA.value() == 0:
            if song_task:
                song_task.cancel()             # stop the current one first
            song = songs.ALL[idx % len(songs.ALL)]
            idx += 1
            print("Now playing:", rtttl.title(song))
            song_task = asyncio.create_task(rtttl.play(piezo, song))
            await asyncio.sleep(0.3)           # debounce
        if btnB.value() == 0:
            if song_task:
                song_task.cancel()
                print("...silence.")
            await asyncio.sleep(0.3)
        await asyncio.sleep(0.02)
```

Add `asyncio.create_task(jukebox())` to `main()` (keep the breather running) and DJ for a while.

> [!TIP]
> **Do this:** press A mid-song — the old song stops *instantly*, the new one starts, the LED never misses a breath. That's the whole show-business API: `create_task()` starts a performance without waiting for it, `cancel()` pulls the performer off stage, and `finally` makes sure they don't leave a note stuck on behind them. The assignment is exactly these three moves wearing a game costume.

## Discussion (5 min)

**Q1. Your game's victory fanfare: `await rtttl.play(...)` or `asyncio.create_task(rtttl.play(...))`? And when would the `await` version be the right call?**

<details>
<summary>Answer</summary>

In the game, `create_task()` — the fanfare is decoration, and awaiting it deafens the buttons for seconds (Session 4's rubric penalized awaiting the POST for the same reason). `await` is right when the program genuinely must not proceed until the sound finishes: a countdown beep sequence before GO, an alarm that must complete before a retry. Same rule as ever: await when you need it *done before you continue*, task when you just need it *done*.

</details>

**Q2. Cancel a song while a note is sounding. Walk the chain: what exactly stops the sound?**

<details>
<summary>Answer</summary>

`cancel()` doesn't stop the PWM — hardware doesn't know tasks exist; the note keeps sounding. What cancellation does is make the task's current `await` raise `CancelledError` inside the coroutine. The `try/finally` catches the unwinding and runs `pwm.duty_u16(0)` — *that* line silences the chip. Delete the `finally` and a cancelled song drones its last note forever: hardware keeps doing the last thing software told it, so cancellable code must clean up in `finally`.

</details>

---

[← Part A](03-part-a-pwm.md) · [Session home](../README.md) · **Next:** [Part C — NeoPixels →](05-part-c-neopixels.md)
