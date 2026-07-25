# ============================================================
# New-Parts Test  --  Session 5 warm-up
# Python IoT on the TinyPICO : Sound & Light
#
# Run this ONCE after adding tonight's parts. It exercises both
# and tells you what to watch/listen for:
#
#   1. Passive piezo, driven the OLD way (on/off):
#        three soft CLICKS -- not beeps. Clicks are correct!
#        (Real beeps mean the active buzzer is still wired in.)
#   2. Passive piezo, driven with PWM:
#        a smooth rising tone
#   3. NeoPixel COUNTING step: the strip fills with a dim dot
#        at a time while numbers print -- it tells you exactly
#        what to set NUM_PIXELS to
#   4. NeoPixels: every pixel marches through red, green, blue,
#        then everything goes dark
#
# If a step fails, fix that part before moving on --
# see TROUBLESHOOTING.md in the repo.
#
# (The Session 3 breadboard -- LEDs, buttons, DotStar -- is
# unchanged tonight and already proven by Session 3's test.)
# ============================================================

from machine import Pin, PWM
import neopixel
import time

# Your stick's pixel count. Not sure? Leave it -- step 3 below
# counts it for you; then set it here and re-run. Every program
# tonight starts with this same constant.
NUM_PIXELS = 18

# The counting step drives this many pixels -- more than any
# course stick. Data for pixels that don't exist is harmless.
PROBE = 30

# --- 1. Piezo, plain on/off: this SHOULD only click -------------
print("[TEST] Piezo, plain on/off -- listen closely: three soft CLICKS")
print("       (If you hear real BEEPS, the old active buzzer is")
print("        still in the breadboard -- swap it out.)")
p = Pin(25, Pin.OUT)
for _ in range(3):
    p.on()
    time.sleep(0.3)
    p.off()
    time.sleep(0.3)

# --- 2. Piezo, PWM: the tone you couldn't make above ------------
print("[TEST] Piezo, PWM -- now a rising tone (tiny spaceship, taking off)")
buzz = PWM(Pin(25), freq=220, duty_u16=32768)
for f in range(220, 1760, 15):
    buzz.freq(f)
    time.sleep(0.01)
buzz.duty_u16(0)
buzz.deinit()

# --- 3. Count your pixels --------------------------------------
# Fills the strip one dim pixel at a time, printing each number.
# When the strip STOPS GROWING, the number just printed is your
# last pixel -- so NUM_PIXELS = that number + 1.
print("[TEST] NeoPixels -- counting. Watch the strip fill, one pixel")
print("       at a time, and note the number printed when it STOPS")
print("       growing. NUM_PIXELS = that number + 1.")
probe = neopixel.NeoPixel(Pin(4), PROBE)
for i in range(PROBE):
    probe[i] = (0, 25, 25)
    probe.write()
    print("  lighting pixel", i)
    time.sleep(0.2)
for i in range(PROBE):
    probe[i] = (0, 0, 0)
probe.write()
print("       Strip stopped growing at pixel N?  ->  NUM_PIXELS = N + 1.")
print("       If that isn't", NUM_PIXELS, "-- edit NUM_PIXELS at the top")
print("       of this file, re-run, and use YOUR number all night.")

# --- 4. NeoPixels, using NUM_PIXELS ----------------------------
# Colors kept dim ON PURPOSE (power budget -- see the setup page).
print("[TEST] NeoPixels -- the whole stick: red, then green, then blue")
np = neopixel.NeoPixel(Pin(4), NUM_PIXELS)
for color in ((40, 0, 0), (0, 40, 0), (0, 0, 40)):
    for i in range(NUM_PIXELS):
        np[i] = color
        np.write()
        time.sleep(0.04)

for i in range(NUM_PIXELS):
    np[i] = (0, 0, 0)
np.write()

print()
print("Clicks, then a tone, a correct pixel count, and three color")
print("sweeps to the very end of the stick? Your new parts are ready.")
print("Anything else -> TROUBLESHOOTING.md")
