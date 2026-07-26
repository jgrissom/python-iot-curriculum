# ============================================================
# Rumble-Rig Test  --  Session 6, Part A
# Python IoT on the TinyPICO : Capstone
#
# Run this ONCE after building the vibration rig. Expected, in
# order (rest the puck ON your fingers -- haptics are FELT):
#
#   1. Plain on/off: two half-second full-strength buzzes
#   2. PWM ramp: silence at first (below its stall floor -- roughly
#      a fifth of full duty -- the motor can't overcome its own
#      friction; physics, not a fault), then it kicks in and swells
#      to full and back down to a stall
#   3. Heartbeat: lub-DUB, lub-DUB (short thump, long thump) x4
#      -- both at full strength, so it carries even with the puck
#      resting on the bench (in the game, your fingers are busy)
#
# Silence at step 1 -> check the transistor legs (E-B-C, flat
# face toward you) and that the motor's header is seated in the
# rows your jumpers think it is.
# See TROUBLESHOOTING.md for the full symptom list.
#
# Rig: motor 3V3<->collector, 1N914 band toward 3V3 across the
# motor, emitter->GND, GPIO 14 -> 1 kohm -> base.
# ============================================================

from machine import Pin, PWM
import time

MOTOR_PIN = 14
FULL = 58000    # ~90% duty: a 3 V motor on a 3.3 V rail, on spec

print("[TEST] Plain on/off -- two half-second buzzes, full strength")
m = Pin(MOTOR_PIN, Pin.OUT)
for _ in range(2):
    m.on()
    time.sleep(0.5)
    m.off()
    time.sleep(0.4)

print("[TEST] PWM ramp -- silent at first (stall zone), then swells")
rumble = PWM(Pin(MOTOR_PIN), freq=200, duty_u16=0)
for level in list(range(0, 256, 4)) + list(range(255, -1, -4)):
    rumble.duty_u16(level * 227)      # 255 * 227 = 57885, just under FULL
    time.sleep(0.02)
rumble.duty_u16(0)
time.sleep(0.5)

print("[TEST] Heartbeat -- lub-DUB, lub-DUB (feel it in the rail)")


def thump(strength, dur):
    rumble.duty_u16(strength)
    time.sleep(dur)
    rumble.duty_u16(0)


for _ in range(4):
    thump(FULL, 0.07)      # lub  (short)
    time.sleep(0.10)
    thump(FULL, 0.22)      # DUB  (long)
    time.sleep(0.60)

rumble.duty_u16(0)
rumble.deinit()

print()
print("Two buzzes, a smooth ramp, four heartbeats? Your driver works,")
print("and your game just grew a sense of touch. -> Part B")
