# ============================================================
# rtttl.py  --  tiny RTTTL ringtone parser + async player
# Python IoT on the TinyPICO : Session 5 (Sound & Light)
#
# Built step by step in Part B of the lesson. Upload to the
# board like a library (same dance as Session 4's async_http):
#   Thonny -> View -> Files -> right-click -> Upload to /
#
# Usage:
#     from machine import Pin, PWM
#     import uasyncio as asyncio
#     import rtttl, songs
#
#     piezo = PWM(Pin(25), freq=440, duty_u16=0)
#     asyncio.run(rtttl.play(piezo, songs.ODE_TO_JOY))
#
# In a running program, fire-and-forget instead:
#     task = asyncio.create_task(rtttl.play(piezo, songs.VICTORY))
#     ...
#     task.cancel()   # play() cleans up after itself (see finally)
# ============================================================

import uasyncio as asyncio

# Semitone offsets within one octave (c = 0 ... b = 11)
SEMITONES = {"c": 0, "c#": 1, "d": 2, "d#": 3, "e": 4, "f": 5,
             "f#": 6, "g": 7, "g#": 8, "a": 9, "a#": 10, "b": 11}


def note_freq(pitch, octave):
    """Frequency in Hz for a pitch name ('c'..'b', sharps allowed)
    and octave. Anchored at a4 = 440 Hz; every semitone is a factor
    of 2**(1/12)."""
    steps = SEMITONES[pitch] + (octave - 4) * 12 - 9   # semitones from a4
    return round(440 * 2 ** (steps / 12))


def title(song):
    """The song's name -- the part before the first colon."""
    return song.split(":")[0]


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


async def play(pwm, song, gap_ms=25):
    """Play one RTTTL song on a PWM pin without blocking the event
    loop. Await it if you need the song finished before continuing;
    asyncio.create_task() it for fire-and-forget."""
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
        # (finally, not just end-of-loop: a cancelled task unwinds
        #  through here too -- without this, cancelling a song would
        #  leave its last note droning forever)
