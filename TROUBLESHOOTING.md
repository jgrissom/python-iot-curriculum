# Troubleshooting — Thonny + TinyPICO

[← Back to home](README.md)

Symptom-first. Find your problem, apply the fix, get back to the lesson. When in doubt, the universal reset is: **click Stop in Thonny, then press Ctrl+F2** (soft-reboots the board and gives you a fresh `>>>` prompt).

---

## Connecting

### Thonny says "Couldn't find the device" or shows no `>>>` prompt

1. **Check the cable.** Charge-only USB cables are the #1 cause — swap for a known data cable.
2. **Check the port.** Tools → Options → Interpreter: interpreter must be *MicroPython (ESP32)* and the port the TinyPICO's serial port (on macOS it looks like `/dev/cu.usbserial-XXXX` or `/dev/cu.SLAB_USBtoUART`; on Windows, a `COM` number that appears when you plug the board in and disappears when you unplug it).
3. Click the **Stop/Restart** button (red stop sign) — Thonny often just needs a nudge to re-open the port.

### "Device is busy" / "Port is in use" / connection drops immediately

Something else is holding the serial port. Close any other serial monitor (Arduino IDE, a second Thonny window, `screen` in a terminal), unplug/replug the board, then Stop/Restart in Thonny.

### The `>>>` prompt appears but the board ignores everything

A program is still running and hogging the CPU (very common with a `while True` loop that never yields). Press **Ctrl+C** to interrupt it; if that doesn't land, **Ctrl+F2**.

---

## Running code

### My async program crashed and now nothing runs right (or `asyncio` behaves strangely on the next run)

After an async program crashes or is interrupted with Ctrl+C, the old event loop and its tasks can be left half-alive — the next `asyncio.run()` may error or inherit zombie tasks (symptoms: `RuntimeError`, tasks from the *previous* run still blinking LEDs).

**Fix: Ctrl+F2 (soft reset) before re-running.** Make this a reflex in Parts B–D: *Stop → Ctrl+F2 → Run*. It takes one second and eliminates a whole class of "my code is broken" that isn't.

### `OSError: 28` when saving or uploading a file

Error 28 = the board's flash filesystem is **full**. The TinyPICO has ~4 MB and old experiments add up.

1. View → Files, look at the *MicroPython device* pane (bottom).
2. Delete files you don't need (right-click → Delete). Keep `micropython_dotstar.py` (and `tinypico.py` if you uploaded it)!
3. Empty a file's contents and re-saving does **not** reclaim space reliably — delete the file itself.

### `ImportError: no module named 'micropython_dotstar'` (or `'tinypico'`)

The helper library isn't on the board. Follow the upload steps in [Part C](sessions/03-sync-async/lessons/04-part-c-dotstar.md) — download from [tinypico/tinypico-micropython](https://github.com/tinypico/tinypico-micropython), then Thonny → View → Files → right-click the file → *Upload to /*. Do **not** rename `micropython_dotstar.py`; the import matches the real filename.

### The board runs an old program every time it powers on, and I can't get a prompt

You (or a previous student) saved a program as **`main.py` on the device** — MicroPython auto-runs it at boot. Connect, press Ctrl+C repeatedly during/after plugging in until you get `>>>`, then delete or rename `main.py` via View → Files. In Sessions 3–5, save work under any other name (e.g. `reaction_game_yourname.py`) and use the Run button instead. **Session 6 breaks this rule on purpose** — deploying as `main.py` is how the capstone ships — and its [Part B](sessions/06-capstone/lessons/03-part-b-ship-it.md) teaches exactly this recovery ritual *before* the deploy.

### Thonny says "Backend not responding"

Stop/Restart button. If it persists: unplug the board, close Thonny, plug in, reopen.

---

## Hardware

### An LED never lights

- **Polarity:** long leg (anode) goes to the GPIO side; short leg (cathode) to the resistor, then GND — see the [wiring diagram](sessions/03-sync-async/diagrams/wiring.svg). (Resistor on the anode side works too — it just has to be *somewhere* in the series loop.)
- The 330 Ω resistor must be **in series** (in the same current path), not on a random row.
- Jumper actually in the GPIO's breadboard column? Off-by-one rows are the classic.
- Test the pin from the REPL: `from machine import Pin; Pin(26, Pin.OUT).on()` — if the LED lights now, the problem was the program, not the wiring.

### A button reads pressed (0) all the time — or never reads pressed

- Constant `0`: the GPIO leg and GND leg are probably on the **same** side of the switch (momentary switches have two pairs of legs; opposite corners are safest), or the pin is shorted to GND.
- Never `0`: missing `Pin.PULL_UP` in code (the pin floats), or the button isn't actually bridging to GND. Test at the REPL: `from machine import Pin; b = Pin(18, Pin.IN, Pin.PULL_UP); b.value()` — should print `1` released, `0` held.

### The DotStar stays dark

- Did you call `TinyPICO.set_dotstar_power(True)`? The DotStar's power rail is switched — without this line it shows nothing, with no error.
- The SoftSPI setup must use `TinyPICO.DOTSTAR_CLK` / `TinyPICO.DOTSTAR_DATA` (and a `miso` pin, even though it's unused).
- Setting a color must come *after* both of the above.

### The buzzer clicks weakly instead of beeping

Passive piezo buzzers need a tone (PWM), not a steady on. In Sessions 3–4 the bench buzzer is **active** (steady `on()` beeps) — if yours only clicks there, flag the instructor; you likely have a passive one from a different kit. **In Session 5 this flips:** the passive piezo is swapped in deliberately, clicking under plain `on()` is expected, and beeping under plain `on()` means the *active* buzzer is still in the breadboard.

### The DotStar rainbow stutters (Part C)

That's not a fault — that's the lesson. Something in your code is blocking. Hunt for any `time.sleep()` in a coroutine, or a loop that never `await`s.

---

## Wi-Fi & network (Session 4+)

### The board won't join the Wi-Fi

- **2.4 GHz only.** The ESP32 cannot see 5 GHz-only networks. Confirm the SSID broadcasts on 2.4 GHz.
- **SSID/password typo in `secrets.py`** — case matters.
- **MAC not registered** (school guest network): run `print_mac.py`, check the address against the registered list.
- **Captive portal:** if joining this network on a laptop pops a login page, the board can't use it — boards can't click "Accept." Use the registered/hotspot network instead.

### `ImportError: no module named 'secrets'` (or `wifi_connect`, `async_http`)

The file isn't on the board. These upload like libraries: Thonny → View → Files → right-click → *Upload to /*. Remember `secrets.py` is one you *create* from `secrets_TEMPLATE.py` — the template alone isn't enough.

### Requests fail with `OSError: -202` (or `getaddrinfo` errors)

DNS lookup failed — the board is on Wi-Fi but can't resolve names. The cloud scoreboard is reached by hostname, so it needs DNS: usually this means the network has no actual internet, or Wi-Fi dropped — reconnect with `wifi_connect.connect()`. (If class is running in fallback mode against a local scoreboard, that's a raw IP and DNS isn't involved — this error then points at a different name, likely a public API's.)

### Requests to the scoreboard time out, but the leaderboard loads in a browser

First check the browser and board are testing the same thing: on a phone **on the class network**, open `http://<SCOREBOARD_HOST>/scores` (note *http*). If the phone can't load it either, the network is blocking plain outbound HTTP — flag the instructor; that's a network problem with a planned fallback, not your code. If the phone loads it but your board times out, recheck `SCOREBOARD_HOST`/`SCOREBOARD_PORT` in `secrets.py` (port must be `80` for the cloud scoreboard) and confirm Wi-Fi is still up.

*Fallback mode only (local scoreboard on a laptop):* timeouts there are almost always **client isolation** — the network blocks device-to-device traffic. That's exactly why class normally runs against the cloud.

### `OSError: [Errno 104] ECONNRESET` / occasional failed requests

Networks drop connections; it's their hobby. This is exactly why the lesson wraps every network call in `try/except OSError` — confirm yours does, and let the next attempt succeed.

### Requests start failing after several successes

Socket leak — something isn't calling `r.close()` (blocking library) or is bypassing `async_http` (which closes for you). Ctrl+F2 resets the sockets; then fix the leak.

### `ntptime.settime()` times out

The network has no internet (or blocks NTP's port). Skip it — nothing in the session depends on the clock.

---

## Sound & light (Session 5)

### `TypeError` mentioning `duty_u16` (or `PWM` has no such method)

The board's MicroPython firmware predates the modern PWM API. Flag the instructor — the fix is a firmware update (the pre-class checklist verifies this, so it should be rare). Don't fall back to the legacy `duty(0..1023)` API; mixed duty scales in class create exactly the confusion the lesson avoids.

### The piezo is silent under PWM

- Is duty non-zero? `duty_u16(0)` **is** the "off switch" — a fresh `PWM(Pin(25), freq=440, duty_u16=0)` is configured but silent until you raise the duty (`32768` is the standard tone setting).
- Did an earlier program leave the pin claimed? Ctrl+F2, then re-create the PWM.
- Wiring: + leg → GPIO 25, – leg → GND — same holes the old buzzer used.
- Still nothing at, say, `freq=1000`? Swap in a neighbor's piezo to split part-vs-code in one move.

### The piezo plays, but it's *quiet*

That's piezo life — no amplifier, and loudness varies a lot with frequency (they're loudest near resonance, typically 2–4 kHz; low notes are naturally faint). It is *not* a defect, and there's no volume knob — though dropping `duty_u16` well below 50% quiets it somewhat, which is the trick to know for polite testing in a room with 12 other benches.

### A note gets "stuck on" (droning forever)

Something stopped the program between `duty_u16(32768)` and the silence that was supposed to follow — a crash, Ctrl+C, or a cancelled task without a `finally`. Immediate silence: `PWM(Pin(25)).duty_u16(0)` at the REPL, or Ctrl+F2. The real fix is the lesson's pattern: tone cleanup lives in `try/finally`, so even a cancelled song shuts up on its way out.

### The NeoPixel strip stays completely dark

- **Direction:** data must enter at **DIN** — the arrows printed on the stick point *away* from it. Wired into DOUT, the strip ignores you silently. This is the #1 cause.
- Did you call `np.write()`? Assignments to `np[i]` only edit a buffer in RAM — nothing shows until `write()`.
- Wiring check: DIN → GPIO 4, VCC → 3V3, GND → the GND rail; and the pin number in `NeoPixel(Pin(4), NUM_PIXELS)` must actually be 4.
- Colors dim-but-technically-lit can *look* dark under room lights — try `(60, 0, 0)` on all pixels before declaring death.

### Animations stop partway down the strip (the far pixels never light)

`NUM_PIXELS` is smaller than your actual stick — the far pixels are never sent data. Re-run the counting step in [`new_parts_test.py`](sessions/05-sound-and-light/code/new_parts_test.py) and set `NUM_PIXELS` to what it tells you, in *every* program you run tonight. (Too *big* is harmless — data for pixels that don't exist falls off the end — which is why the counting step can probe with 30.)

### The strip shows the wrong colors (red and green swapped, or a white-ish 4th channel)

Classic sign of an RGBW stick (four channels) driven as RGB, or a stick with a different channel order. Try `neopixel.NeoPixel(Pin(4), NUM_PIXELS, bpp=4)` and 4-tuples `(r, g, b, w)`; if it's channel order, flag the instructor — course kits are plain GRB WS2812 and the driver handles that order automatically, so a mismatch means a stray part.

### The board resets/disconnects when the strip lights up

Brownout: the strip pulled more current than the 3.3 V regulator could give. Almost always a brightness-cap violation — hunt for channel values above ~60 (the classic is a `(255, 255, 255)` "just to test"). Dim the code, Ctrl+F2, carry on. The [setup page](sessions/05-sound-and-light/lessons/02-setup.md) has the power math.

### The first pixel flickers or glitches while the rest behave

The stick is powered from 5 V somewhere (so 3.3 V data is marginal — pixel 1 takes the brunt, cleans up the signal, and the rest behave). Power the stick from **3V3** as the setup page wires it and the problem disappears.

---

## The vibration rig (Session 6)

### The motor does nothing at all

Work backwards along the current's path:

- **Transistor legs.** Flat face toward you, legs down: **E–B–C** left to right for the course's 2N2222A parts. Swapped legs don't damage anything — they just silently do nothing. Re-seat it deliberately. (Using your own transistor? Some TO-92 "2N2222" variants — notably the P2N2222A — are **reversed, C-B-E**; check the printed part number against its datasheet.)
- **Tug-test the screw terminal.** Hair-thin motor leads slip out of clamps that *look* closed. Gentle pull on each wire; if it moves, re-strip, twist, fold the end double, re-clamp.
- **Base resistor actually reaching the base row?** No base current, no switch.
- Test the driver without the code: at the REPL, `Pin(14, Pin.OUT).on()` — buzz means the rig is fine and the problem is the program; silence means wiring.

### The motor got quieter over the evening (or cuts in and out)

A vibration motor in a screw terminal is the textbook case of screws shaking loose. Re-snug both, tug-test again. Chronic loosener: a dab of hot glue over the clamped wires after tightening.

### The motor runs but never turns off (or the transistor gets hot)

- Never off: the flyback diode is probably in **backwards** — band must face the 3V3 side. Installed reversed it conducts whenever the motor runs (and it may now be cooked — replace it, they're pennies).
- Hot transistor with weak rumble: base resistor far too large (1 kΩ is right for the course's 2N2222A; if you've substituted a 2N3904, its gain sags at this current — use ≤470 Ω), or the transistor is being asked to drive something bigger than a coin motor.

### The motor buzzes the desk but you can't feel it in the board

It's not stuck down. The adhesive ring must bond the motor to the breadboard (or bench) — a loose coin motor just dances. Stick it, tape the leads, retest.

### One lead tore off the motor body

The #1 coin-motor death. It's not repairable without soldering — swap in a spare from the kit bag, and this time tape the leads to the breadboard so the taped span takes the flexing.

---

Still stuck? Ask — but be ready to say what you observed, what you expected, and what you already tried. That sentence is half of debugging.

[← Back to home](README.md)
