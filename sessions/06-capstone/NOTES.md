# Design-Decision Log — Session 6 (Capstone)

Companion to Sessions [3](../03-sync-async/NOTES.md), [4](../04-wifi-iot/NOTES.md),
and [5](../05-sound-and-light/NOTES.md); same purpose, safe for the public repo.

## The core bet

**The finale is a studio session, not a lecture session** (Jeff's design,
2026-07-26). Light teaching up front (~50 min), then the longest build
block in the course: students *finish the game* — restore Session 4's
networking to their Session 5 Game-Show Edition, integrate the new haptic
channel, pick extra-credit features from a menu, and ship the result as a
battery-powered appliance demoed on the class leaderboard.

An alternative finale was seriously considered and rejected: a new
autonomous-device build ("the Sentinel") around an LDR light sensor —
ADC, averaging, hysteresis. Strong concepts, but a capstone session
shouldn't carry new concepts *and* a new artifact: the game trilogy was
90% finished, and abandoning it at the finale to start something fresh
would trade an ending for a fourth beginning. The LDR/ADC material is a
ready-made seed for a future run or a session 7 (note for then: LDR must
sit on GPIO 32/33 — ADC1 — because ADC2 pins die when Wi-Fi is up).

**The stretch goals from Sessions 4 and 5 migrated here** as the
capstone's extra-credit menu (removed from those assignment pages
2026-07-26). Rationale: 45-minute assignment windows never had room for
them; a 105-minute studio does, and a menu keeps 13 benches of different
speeds all busy and all gradeable.

## The vibration rig (Part A)

- **This is the parked motors material, right-sized.** Session 3's NOTES
  deferred "flyback diodes / motors" to a future session; a full motor
  session (drivers, gearboxes, chassis, separate supplies) is
  hardware-deep but Python-shallow. A 10×3 mm coin ERM vibration motor
  delivers the two deferred concepts — **transistor as switch** (the
  course's first amplification) and the **flyback diode** — with ~75 mA
  draw off the 3V3 rail, no external moving parts, and real product
  relevance (phone haptics).
- **Parts are deliberately cheap and deep-spared:** the transistor is
  the **2N2222A** (Jeff's stock, confirmed 2026-07-26) with the textbook
  **1 kΩ** base resistor — ~2.6 mA of base drive against the 2222A's
  600 mA rating and healthy gain at 80 mA means effortless hard
  saturation. Substitution note: a 2N3904 also works but its gain sags
  at this current — drop the base resistor to ≤470 Ω with a 3904;
  anything 470 Ω–1 kΩ is fine with the 2222A. **Pinout landmine, named
  in the lesson:** TO-92 "2N2222" parts ship in two pinouts —
  **PN2222A is E-B-C** (flat face toward you) but ON Semi's
  **P2N2222A is reversed, C-B-E**. Check the print on the package;
  a reversed part doesn't burn, it just silently does nothing (and
  weakly rumbles via the base-collector path in some cases). The
  bench test settles it in ten seconds. 1N914 ≡ 1N4148 (same die,
  older designation) as the flyback. Optional `104` ceramic across the
  motor terminals (already in kits from S3 Part D) for brush noise.
- **Screw terminals instead of solder** (2-pin, 2.54 mm breadboard
  pitch): kills 26 prep solder joints and makes dead-motor swaps a
  30-second fix. The motor's 32 AWG leads demand the ritual taught in
  Part A — twist, fold double, snug, **tug-test** — and the honest
  caveat that a vibration motor is the pathological case for screws
  walking loose ("motor got quieter → check the screws" is in
  TROUBLESHOOTING). Leads still tear at the motor body: adhesive-mount
  the motor and tape the leads down so flexing happens mid-span.
- **Motor pin is GPIO 14** — free, no boot role, and deliberately an
  ADC2 pin: the ADC2/Wi-Fi conflict only bites *inputs*, so spending an
  ADC2 pin on an output preserves 32/33 (ADC1) for future sensing.
- **`on()` full-rumbles the motor — the piezo contrast is taught.** A
  motor is a DC device: steady current = steady motion, so unlike the
  piezo it doesn't *need* PWM — PWM buys **intensity** control. This
  completes the duty-cycle triptych: duty = brightness (LED), ≈ volume
  (piezo), = strength (motor); frequency matters to the piezo alone.
  Full-intensity duty is capped ~90% (`duty_u16` ≈ 58000) — a 3 V motor
  on a 3.3 V rail, governed by duty: the average lands on spec.

## Ship it (Part B)

- Kept small on purpose (15 min): save the game as **`main.py` on the
  board**, reboot without Thonny, run from a USB power bank. It
  ceremonially breaks the course's own standing rule (TROUBLESHOOTING
  has warned against `main.py` since Session 3) — the "bug" was
  autonomy all along. The un-brick ritual (Ctrl+C storm on connect,
  delete `main.py` via Files) is taught *before* anyone needs it.
- Power bank over LiPo: students likely own one, zero charging
  logistics, and the classic gotcha (banks auto-off under light load)
  is survivable here — an ESP32 with Wi-Fi up draws enough to keep
  most banks awake; if one sleeps, it's the bank, not the board.
- The deeper point, stated in the lesson: once headless, `print()`
  reaches no one — a shipped device's only outputs are its lights,
  sounds, and network reports. Session 4's fail-soft habit becomes
  *load-bearing* on battery: there is no shell to read a traceback in.

## Capstone structure

- **Core requirements first, menu second.** Core (graded for everyone):
  network restored onto the Game-Show Edition (the S4 grafts re-applied
  — deliberately practicing *merging features into changed code*, which
  is different from following grafts into a pristine base), haptics
  integrated non-blockingly through the existing show machinery, S5
  polish intact, and a headless battery demo. Menu (choose two):
  the migrated S4/S5 stretch goals.
- **Checkpoints are printed in the assignment** (":45 — your game posts
  to the leaderboard again; flag the instructor if not") because a
  105-minute unstructured block is where studio sessions die. The
  checkpoint times are pacing advice, not grades.
- **The demo ceremony ends with one last server-kill.** The instructor
  stops the scoreboard during the final tournament — every game on
  every bench must shrug, in unison, on battery. The course's three
  villains (sleep, network, shows) take a bow together.

## Repo & solutions policy

Unchanged: `reaction_game_capstone_SOLUTION.py` (core requirements
implemented; menu items sketched in the answer key) lives only in the
instructor bundle. Session 4's Part C graft pages remain the student
path for the network restore — nothing new is published.
