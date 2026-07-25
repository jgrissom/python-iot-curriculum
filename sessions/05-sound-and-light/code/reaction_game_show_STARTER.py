# ============================================================
# Reaction Game -- GAME-SHOW EDITION (starter)
# Python IoT on the TinyPICO : Session 5 (Sound & Light)
#
# Session 3's reaction game gets stage presence: a breathing
# wait beacon (PWM), a victory fanfare (RTTTL), and NeoPixel
# stage lighting. The game logic is already done (it's the
# known-good Session 3 solution) -- tonight is show business.
# Fill in the three TODOs.
#
# THE GOLDEN RULE: THE SHOW MUST NOT STOP THE GAME.
# A fanfare runs for seconds. Await it and the buttons go deaf
# -- the same freeze as Session 4's blocking network call.
# Shows are fire-and-forget (start_show), and a new round
# cancels whatever show is still running.
#
# This file RUNS AS-IS (placeholder blink + placeholder beeps).
# Each TODO upgrades one piece; run after every one.
#
# Wiring (Session 3 build + tonight's additions):
#   LED 1 (red)   -> GPIO 26 (+ 330 ohm resistor to GND)
#   LED 2 (green) -> GPIO 27 (+ 330 ohm resistor to GND)
#   Passive piezo -> GPIO 25 (swapped in for the active buzzer)
#   Button A (blue cap)   -> GPIO 18  (other leg to GND)
#   Button B (yellow cap) -> GPIO 5   (other leg to GND)
#   NeoPixel stick -> DIN GPIO 4, VCC 3V3, GND GND
#     (set NUM_PIXELS below to YOUR stick's count -- the warm-up
#      test counted it for you)
#   DotStar -> onboard (no wiring)
#
# The board also needs rtttl.py and songs.py uploaded (like
# libraries), plus the usual micropython_dotstar.py.
# ============================================================

from machine import Pin, PWM, SoftSPI
import uasyncio as asyncio
import tinypico as TinyPICO
from micropython_dotstar import DotStar
import neopixel
import random
import rtttl
import songs

# --- Hardware setup ---
beacon = PWM(Pin(26), freq=1000, duty_u16=0)   # red LED, now dimmable
led2 = Pin(27, Pin.OUT)                        # green LED = GO indicator
piezo = PWM(Pin(25), freq=440, duty_u16=0)     # passive piezo, silent
btnA = Pin(18, Pin.IN, Pin.PULL_UP)
btnB = Pin(5, Pin.IN, Pin.PULL_UP)

NUM_PIXELS = 18   # <- YOUR stick's count (from new_parts_test.py)
np = neopixel.NeoPixel(Pin(4), NUM_PIXELS)

spi = SoftSPI(sck=Pin(TinyPICO.DOTSTAR_CLK),
              mosi=Pin(TinyPICO.DOTSTAR_DATA),
              miso=Pin(TinyPICO.SPI_MISO))
ds = DotStar(spi, 1, brightness=0.3)
TinyPICO.set_dotstar_power(True)

# --- Shared game state ---
state = {"go": False, "over": False, "winner": None, "false_start": False}

# --- Stage lighting (from Part C -- power budget already respected) ---

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
    strip_fill((0, 0, 0))


async def beep(freq=880, dur=0.2):
    """One PWM beep -- the passive-piezo version of Session 3's buzz()."""
    piezo.freq(freq)
    piezo.duty_u16(32768)
    try:
        await asyncio.sleep(dur)
    finally:
        piezo.duty_u16(0)

# --- Show machinery (provided -- read the comment, it's the subtle bit) ---

show_tasks = []


def start_show(*coros):
    """Fire-and-forget every piece of a show at once:
        start_show(rtttl.play(piezo, songs.X), strip_comet(color))
    Each piece becomes its own task, and every task is remembered --
    because cancelling a task does NOT cancel tasks it started, the
    next round can only clear the stage if it can reach EVERY piece."""
    for coro in coros:
        show_tasks.append(asyncio.create_task(coro))


def cancel_show():
    """Pull every performer off the stage (no-op if the show is over)."""
    while show_tasks:
        show_tasks.pop().cancel()

# --- The game ---

async def wait_beacon():
    """During the wait phase: the red LED breathes, the DotStar glows
    red, and dim red 'house lights' fill the strip. Dark and
    hands-off the rest of the time."""
    while True:
        if not state["go"] and not state["over"]:
            # ---- TODO 1: make it BREATHE ------------------------
            # Replace this placeholder blink with one smooth breath
            # per loop (Part A's coroutine is your model):
            #   - set the house lights once per breath:
            #       strip_fill((8, 0, 0));  ds[0] = (255, 0, 0)
            #   - sweep level 0..255 and back in small steps:
            #       beacon.duty_u16(level * level), short await each step
            #   - re-check `not state["go"] and not state["over"]`
            #     EVERY step and bail out mid-breath: GO must kill
            #     the breath instantly, not at the end of the exhale
            beacon.duty_u16(65535)          # placeholder: plain blink
            await asyncio.sleep(0.25)
            beacon.duty_u16(0)
            await asyncio.sleep(0.25)
            # -----------------------------------------------------
        else:
            beacon.duty_u16(0)
            await asyncio.sleep(0.01)


async def referee():
    """Runs the round: reset the stage, wait, show GO, then let the
    players end it."""
    while True:
        # Reset -- clear the stage from last round's show, re-arm state
        cancel_show()
        piezo.duty_u16(0)                 # silence anything mid-note
        strip_fill((0, 0, 0))             # stage dark
        state.update(go=False, over=False, winner=None, false_start=False)
        led2.off()

        # Random wait -- players may false-start during this
        await asyncio.sleep(random.uniform(2, 5))

        # Only show GO if nobody false-started during the wait
        if not state["over"]:
            state["go"] = True
            ds[0] = (0, 255, 0)           # green = GO...
            strip_fill((0, 60, 0))        # ...and the stage floods green
            beacon.duty_u16(0)            # kill the breath instantly
            led2.on()

        # Wait for a player coroutine to end the round
        while not state["over"]:
            await asyncio.sleep(0.01)

        # The pause between rounds -- this is the show's moment
        await asyncio.sleep(3)


async def player(btn, name, color):
    """Watches one button and reacts based on game state."""
    while True:
        if btn.value() == 0:   # button pressed

            if not state["go"] and not state["over"]:
                # FALSE START
                state["over"] = True
                state["false_start"] = True
                state["winner"] = name          # the offender
                ds[0] = (255, 0, 0)             # red = loss
                print("Player", name, "FALSE START - you lose!")
                # ---- TODO 3: the walk of shame ------------------
                # Fire-and-forget (never await a show): the sad
                # trombone plus red flashes on the strip, together.
                # Ingredients: songs.SAD_TROMBONE, strip_flash,
                # start_show (it takes several coroutines at once).
                start_show(beep(220, 0.3))      # placeholder -- replace
                # -------------------------------------------------

            elif state["go"] and not state["over"]:
                # VALID WIN
                state["over"] = True
                state["winner"] = name
                ds[0] = color                   # winner's cap color
                print("Player", name, "WINS!")
                # ---- TODO 2: the victory show -------------------
                # Fire-and-forget: the fanfare plus a comet in the
                # winner's cap color -- you're holding `color`.
                # Ingredients: songs.VICTORY, strip_comet, start_show.
                # (Timing thought: one comet lap is NUM_PIXELS x 0.06 s.
                #  How many laps fit in the 3 s pause before the next
                #  round's reset cancels the show?)
                start_show(beep(880, 0.3))      # placeholder -- replace
                # -------------------------------------------------

            await asyncio.sleep(0.15)   # debounce
        await asyncio.sleep(0.01)       # yield to other tasks


async def main():
    asyncio.create_task(wait_beacon())
    asyncio.create_task(referee())
    asyncio.create_task(player(btnA, "Blue", (0, 0, 255)))       # blue cap
    asyncio.create_task(player(btnB, "Yellow", (255, 255, 0)))   # yellow cap
    while True:
        await asyncio.sleep(1)

try:
    asyncio.run(main())
finally:
    TinyPICO.set_dotstar_power(False)
    beacon.duty_u16(0)
    beacon.deinit()
    piezo.duty_u16(0)
    piezo.deinit()
    strip_fill((0, 0, 0))
    led2.off()
