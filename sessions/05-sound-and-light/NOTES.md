# Design-Decision Log — Session 5 (Sound & Light)

Companion to Sessions [3](../03-sync-async/NOTES.md) and
[4](../04-wifi-iot/NOTES.md); same purpose, safe for the public repo.

## The core bet

The session's thesis is that **slow outputs are the third face of blocking**:
Session 3's villain was `time.sleep()`, Session 4's was the network, and
tonight's is a six-second fanfare. A melody or an animation is a
seconds-long operation exactly like a slow HTTP request, and the same two
rules apply — never block the event loop on it, and choose deliberately
between `await` (wait for it) and `create_task()` (fire and forget). Every
segment feeds that thesis; the assignment grades it (the instructor presses
buttons *during* the victory fanfare, the exact analogue of Session 4's
kill-the-server demo). New tool introduced on the same theme:
`task.cancel()` — a show that's no longer wanted (a new round started) must
be stoppable, and Part B's jukebox teaches cancellation before the
assignment needs it.

**Session 5 deliberately needs no network.** Sound and light are
self-contained; a second failure domain (venue Wi-Fi) would buy nothing and
cost setup time. The whole session — assignment included — runs anywhere,
including at home. (The Game-Show Edition grafts onto the *offline*
Session 3 game, not Session 4's connected version, for the same reason;
a stretch goal reconnects it for those who want both.)

## Hardware decisions (load-bearing)

- **The active buzzer is swapped for a passive piezo, same spot, GPIO 25.**
  Sessions 3–4 used an active buzzer (internal oscillator — plain `on()`
  beeps). Passive piezos have no oscillator: `on()` produces one weak
  *click*, and *you* must supply the tone as a waveform. That click is the
  session's opening hook (the warm-up test plays it on purpose, then plays
  a PWM sweep on the same part) — show-then-fix, the curriculum's standard
  move. Swapping in place keeps the Session 3 reference wiring otherwise
  untouched and needs no new pin. GPIO 25 was reserved for exactly this in
  Session 3's NOTES ("DAC-capable, leaving the door open for tone/PWM
  work"). The DAC itself stays parked — PWM covers everything the session
  needs, and true DAC audio (samples, amplifiers) is a different course.
  The retired active buzzer goes back in the kit bag; Session 3's files
  are not updated (they document the bench as it was).
  *Bench-verified 2026-07-25:* the **active** buzzer also plays RTTTL
  passably under PWM — switching the whole unit (oscillator included) at
  audio rate makes the switching frequency the dominant pitch, just with
  a buzzier timbre. So the retired buzzer in the kit bag doubles as an
  **emergency spare** for a dead piezo: same holes, same code, degraded
  tone. It does *not* replace the swap — the click-vs-beep opening and
  the clean-tone physics both need the passive part.
- **NeoPixel stick: WS2812, data on GPIO 4, powered from 3V3 — length
  variable by design.** The course sticks are believed to be ~18 pixels
  but weren't confirmable before class day (revised 2026-07-25; the
  session was first drafted around an 8-pixel stick), so nothing anywhere
  hardcodes a length: every program starts with one `NUM_PIXELS`
  constant (default 18), the warm-up test *counts the stick* (fills a
  30-pixel probe one dim pixel at a time with indices printed — data for
  pixels that don't exist is harmless, which is itself a teachable
  property of the protocol), and all effects scale (the light organ's
  gradient and bar mapping are proportional, not per-pixel constants).
  **~20 pixels is the documented ceiling on 3V3**: at the ≤60 cap a
  fully-lit 18-pixel stick draws ~250 mA — inside the regulator's budget
  but near its edge — while full white at 18 px is ~1 A, a guaranteed
  (harmless) brownout reset. Longer strips need their own 5 V supply +
  level shifter and are out of scope; the setup page says so.
  - *Why GPIO 4:* free general-purpose output on the same header side as
    the LEDs and piezo, no boot-time role. Same avoid-list as Session 3:
    34–39 (input-only), 0/2/12/15 (strapping/DotStar). GPIO 5 stays
    input-only per Session 3's caveat.
  - *Why 3V3, not 5V:* WS2812 logic-high threshold is 0.7 × VDD. At
    VDD = 5 V that's 3.5 V — *above* the ESP32's 3.3 V data line, which
    works on many sticks and flickers on others (the classic "first pixel
    glitches" symptom). At VDD = 3.3 V the threshold is ~2.3 V and the
    logic margin is solid. Slightly dimmer, completely classroom-stable.
    The "real product" answer (5 V supply + level shifter) is named in the
    lesson so students leave knowing the honest trade-off.
  - *The brightness cap is a hard rule, not a style choice.* Full white is
    ~60 mA/pixel — at any course stick length that exceeds the 3V3
    regulator's comfortable budget on top of the board itself (brownout =
    mystery resets), and at 18 pixels it's ~1 A. All lesson/starter code
    keeps channel values ≤ 60 and the comet helper dims by bit-shifting.
    TROUBLESHOOTING documents the brownout symptom. Don't "brighten up"
    example code.
- **Buttons, LEDs, DotStar: unchanged from Session 3.** LED 1 (GPIO 26)
  is driven by `PWM` this session — code must `deinit()` PWM before
  anything re-uses the pin as a plain `Pin`, and cleanup blocks do.

## Library / API decisions

- **`machine.PWM` with `duty_u16` (0–65535), not the legacy `duty`
  (0–1023).** `duty_u16` is the documented modern API; mixed use is a
  classic confusion source. If a board's firmware lacks `duty_u16`, the
  firmware is old enough to update (pre-class checklist verifies). 50%
  duty (`32768`) is the standard tone setting; silence between notes is
  `duty_u16(0)` — cheaper and cleaner than `deinit()`/reconstruct per note.
- **`neopixel` is used precisely because it's frozen into MicroPython** —
  zero-install, deliberately contrasted with Session 3's
  upload-the-DotStar-library dance (the lesson names the contrast; it
  teaches what "batteries included" means in firmware). The explicit
  `np.write()` (vs DotStar's auto-write) is likewise teaching material:
  compose the frame, then send it — one timing-critical burst down one
  wire.
- **`rtttl.py` is published in the public repo like `async_http.py` was**:
  built stage-by-stage in Part B, then uploaded as a library so the
  assignment imports it instead of re-pasting it. Its `play()` wraps the
  note loop in `try/finally: duty_u16(0)` **on purpose** — a cancelled
  task would otherwise leave a note stuck on forever; this is the
  session's cancellation-safety example. Don't simplify the `finally`
  away.
- **RTTTL over ad-hoc `(freq, ms)` lists** because parsing a real-world
  compact text format is the session's Python meat (string methods,
  defaults, generators) and because the format is culturally fun (Nokia
  ringtones) with a big internet supply of songs students can paste in.
  Parser follows the spec defaults (`d=4, o=5, b=63`), anchors a4 = 440 Hz,
  and accepts dot-before-or-after-octave (real-world strings disagree).
- **`asyncio.sleep_ms()` appears for the first time** (music timing is
  ms-native); the lesson introduces it explicitly as uasyncio-only.
  Elsewhere float-seconds `asyncio.sleep()` stays the house style.
- **`songs.py` contains only public-domain melodies** (Beethoven, Tárrega
  is *not* included — the Nokia tune's *arrangement* status is murky;
  Ode to Joy, Für Elise, The Entertainer, Twinkle, Happy Birthday) plus
  original two-bar jingles (victory, charge, sad trombone) composed for
  the course. Keep it that way — the repo is public.

## Pedagogy notes

- **Part A teaches PWM as one mechanism with two knobs** — duty cycle
  (energy → brightness) and frequency (repetition rate → pitch) — across
  two senses on parts already on the bench. The LED ignores frequency
  (above flicker fusion) and obeys duty; the piezo obeys frequency and
  mostly shrugs at duty. Same signal, two transducers — that's the aha.
  The `level * level` gamma trick is kept (perceived brightness is
  nonlinear; squaring an 8-bit level conveniently maxes at 65025 ≈ u16)
  — but it is *asserted, not demonstrated*: a side-by-side
  linear-vs-squared A/B experiment (briefly A2.1) was cut on 2026-07-25,
  Jeff's call — the extra parameter and second code block would confuse
  more than the comparison teaches. Don't reintroduce it; the one-line
  explanation in A2's intro is the intended depth.
- **Part B's blocking demo re-runs the curriculum's signature beat**: a
  `time.sleep()` player visibly freezes the breathing LED for a whole
  song before the async player un-freezes it. By Session 5 students
  should *predict* the freeze — the lesson asks them to, before running.
- **The jukebox (B4) exists to teach `cancel()`** with a physical remote
  (Button A = next song, Button B = stop). It's the assignment's
  round-reset show-cancellation, met one hour earlier in a toy.
- **Part C is 30 minutes on purpose** — the `neopixel` API is small, and
  animation depth lives in Part D and the assignment instead. Helpers
  (`strip_fill`, comet) reappear verbatim in the starter so assignment
  time goes to the TODOs, not to re-deriving a comet.
- **Part D (light organ) is optional** for the standard reasons: the core
  210 minutes are full, it needs no new parts, and it's the best
  early-finisher magnet in the curriculum so far (parse() reuse + shared
  state between a conductor task and a painter task — C2C's flag move,
  scaled up).
- **Assignment scaffolding follows Session 3's shape** (starter file,
  architecture given, exactly three TODOs: breathing beacon, victory
  show, false-start show) rather than Session 4's graft pages — the game
  logic already exists, so students decorate a known-good file; a starter
  .py is the natural home again. The starter runs correctly *before* any
  TODO is touched (placeholder beeps in the show slots) — runnable at
  every stage, per the Session 4 ladder lesson.
- **Show-cancellation is provided, not a TODO**: the referee cancels
  `show_task` at round reset. It's the subtlest concurrency line in the
  file; the rubric tests it (mash a button during a show → next round
  must start clean) but students get the line for free and the comment
  explains it. Three TODOs stays three.
- **Color semantics extend, unchanged**: red = wait/lose (dim-red house
  lights during the wait, red flashes on false start), green = GO (green
  flood), winner feedback = the winner's *cap* color (comet). Same
  reserved-color rule as Session 3 — don't cast red or green for anything
  else.

## Repo & solutions policy

Unchanged from Sessions 3–4: solution and answer key live only in the
private instructor bundle (`05-sound-and-light/` there mirrors this
folder); the public `.gitignore` patterns are a backstop, not the rule.
Discussion questions keep collapsible `<details>` answers in public pages.

## Standing to-dos / open items

- Kit procurement: 13× passive piezo + 13× WS2812 stick (~18 px; any
  length to ~20 works unmodified) (+ spares).
  Sticks usually ship with unsoldered header pins — **solder before class**;
  13 sticks × 3 joints is not a classroom activity.
- Classroom sound management: 13 boards playing ringtones is chaos.
  The pre-class checklist proposes "sound check" etiquette (headphone-less
  hardware has no volume knob; duty cycle down = somewhat quieter, and the
  lesson names that trick).
- Session 6 remains undesigned; flyback diodes / motors still parked.
  The light organ's freq→bar mapping could seed a future
  sensors/ADC session (microphone input) if Session 6 wants it.
