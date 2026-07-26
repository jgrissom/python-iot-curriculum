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
- **Motors are prepped as soldered header pigtails** (decided
  2026-07-26 after a screw-terminal detour): each motor's hair-thin
  leads soldered to a 2-pin header, joints heat-shrinked, leads
  twisted as a pair. **17 units built and 100% QC'd** (rail-buzz at
  3V3 — test at operating voltage, not 5 V — plus a wiggle-while-
  buzzing test to catch cold joints; passed units sharpie-dotted).
  Rationale: screw terminals were the planned no-solder path, but
  solder beat them on the one axis that matters for this part —
  **vibration walks screws loose; solder doesn't** — and pre-built
  pigtails (and later, the pre-assembled puck) reduce the student
  step to "plug it in."
  For a future run without prep time: 2-pin 2.54 mm screw terminal
  blocks do work — the ritual is twist the strands, fold the bare end
  double, snug, then tug-test *and* twirl-test (a wire that rotates
  freely is clamped on insulation) — with re-snugging expected over an
  evening of vibration. Leads still tear at the motor body under
  either scheme: adhesive-mount the motor and tape the leads down so
  flexing happens mid-span.
- **Motor pin is GPIO 14** — free, no boot role, and deliberately an
  ADC2 pin: the ADC2/Wi-Fi conflict only bites *inputs*, so spending an
  ADC2 pin on an output preserves 32/33 (ADC1) for future sensing.
- **The motor mounts on a poker-chip "haptic puck," not the breadboard**
  (bench-found 2026-07-26): stuck to a breadboard on an acrylic base
  plate, the vibration is underwhelming — a coin ERM is designed to
  shake ~phone-mass, and a plate coupled to a desk swallows it.
  A light, rigid, free chip under a fingertip is the design-intent
  environment (why phones buzz in hands, not on tables). **Pucks are
  fully assembled at prep** (Jeff, final call 2026-07-26): one
  pea-sized dab of hot glue on the chip, motor pressed in, leads
  swept into the dab's tail before it cools — anchor and strain
  relief in one squeeze. **Motor sits edge-biased, not centered**
  (built that way 2026-07-26): the offset torques the chip so the far
  edge swings harder (rocking amplification — more feel per mA),
  fingers get bare chip to rest on, leads exit over the near edge,
  and the rocking rattles louder on the bench. Keep the motor fully
  on the chip — an overhang shrinks the glue contact right where
  stress is highest. The decision trail, for the record: tape was
  considered (electrical tape flags and gums; Kapton is the tape-
  world answer), then inspection showed these motors ship with a
  **factory glue blob potting the lead solder joints**, briefly
  making extra protection look redundant — glue was chosen anyway:
  it's also the *mount*, rigid glue couples vibration to the chip
  better than the foam adhesive ring, and the embedded span removes
  the free-flapping wire that fatigues at the factory blob's edge.
  Hot glue peels off a poker chip with a thumbnail if a motor needs
  swapping. Students receive a finished component and just plug it
  in; the one handling rule is taught in A1: by the chip, never by
  the wires. Don't "simplify" the puck away; the mass
  argument is in Part A's step 1.
- **Coin ERMs have a start/stall floor around a fifth of full duty**
  (bench-found 2026-07-26 on the puck: 15000 = faint whisper, 12000 =
  dead silence — the motor never spins; static friction + the eccentric
  mass's inertia). A3 step 2 includes the 15000 whisper deliberately;
  step 3 has students walk down from it and find their own floor.
  Consequence taught with it: *dependable soft = short full-strength
  pulse* (whisper-duty sits so close to the floor that unit variation
  can silence it) — and haptic driver chips exist partly to "kick"
  past this (overdrive then drop). Game cues use strength × duration
  above the floor; the answer key warns graders about claimed-soft
  cues below it. Feeling technique also matters and is taught: **rest
  the puck ON upturned fingers** — pressing down on it damps the
  vibration.
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
