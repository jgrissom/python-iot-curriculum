# Part B — Ship It: `main.py` and the Battery

⏱️ **15 min**

[← Part A](02-part-a-vibration.md) · [Session home](../README.md) · **Next:** [Capstone →](../assignment/README.md)

---

Since Session 3, the [troubleshooting guide](../../../TROUBLESHOOTING.md) has carried a warning: *never save your program as `main.py` on the board — MicroPython auto-runs it at boot and you'll fight to get a prompt back.* Tonight we break that rule on purpose, because the "bug" was **autonomy** all along. A program that starts itself the moment power arrives, on any power, forever — that's not a board misbehaving; that's an appliance.

We'll practice on something already working — Session 5's game — so the ritual is familiar before your capstone needs it.

## B1 — learn the escape hatch *first*

Before deploying anything, know how to undo it. A board auto-running `main.py` fights you for the REPL, and the fight is winnable:

1. **Reconnect Thonny** (Stop/Restart button) and **hammer Ctrl+C** during/right after the connect — you're racing the boot, and interrupting the program wins you a `>>>`.
2. From there: *View → Files*, right-click `main.py` on the device, **Delete**. Ctrl+F2. The board is a lab bench again.
3. If the timing race is stubborn (a program that boots *fast*): Stop → unplug → hold Ctrl+C down in the shell as you replug.

That's the whole ritual. Nothing tonight can brick a board — worst case is thirty seconds of Ctrl+C.

## B2 — deploy

1. **Open your working Game-Show Edition** in Thonny (the file you finished last session).
2. ***File → Save As…* → choose *MicroPython device* → name it exactly `main.py`.** (Your computer copy stays where it was — you just put a copy on the board with the magic name.)
3. **Prove the autonomy:** press the board's **reset button** (or unplug/replug USB). Don't touch Thonny. Within a few seconds: the beacon breathes. Nobody pressed Run. The laptop is now just a power supply.
4. **Get the bench back:** Stop/Restart in Thonny + Ctrl+C (the B1 ritual, first live use) — you'll be editing this game all night, so you need the REPL back. Leave `main.py` on the board; you'll re-save over it before the demo.

## B3 — cut the cable

1. **Plug the board into a USB power bank** instead of the laptop. The game boots and plays — no computer involved. Walk it around. Hand it to a classmate. It's a *device*.
2. **Two truths about headless life**, worth thirty seconds of reflection before the capstone:
   - **Every `print()` now prints to nobody.** Standings, fail-soft notes, debug lines — composed and discarded. A shipped device speaks only through what's *on* it: lights, sound, rumble, and its network reports. If information matters, it needs one of those channels.
   - **Fail-soft is now survival, not courtesy.** On the bench, a crash shows a traceback; on battery, a crash is indistinguishable from death. Session 4's `try/except OSError` habit is what separates "device" from "brick with LEDs."
3. **Power-bank gotcha, named in advance:** some banks switch off when the load looks too small. An ESP32 with Wi-Fi up generally draws enough to stay awake, but if your bank powers off after a few seconds — it's the bank being clever, not the board being broken. Try another bank (or a wall USB adapter).

> [!NOTE]
> **Why did the course ban `main.py` for five sessions, then teach it in fifteen minutes?** Because the danger was never `main.py` — it was *not knowing the escape hatch*. Deployment is trivial; recovery is the skill. That's true of most "dangerous" operations in computing: learn the undo first, and the do becomes boring. (You did B1 before B2. That ordering was the lesson.)

---

[← Part A](02-part-a-vibration.md) · [Session home](../README.md) · **Next:** [Capstone →](../assignment/README.md)
