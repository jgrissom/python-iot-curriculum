# Opening Review — The Show So Far

⏱️ **15 min** · instructor-led

[← Overview](00-overview.md) · [Session home](../README.md) · **Next:** [Part A — The Vibration Rig →](02-part-a-vibration.md)

---

One bench demos their Game-Show Edition — breathing beacon, green flood, a fanfare interrupted mid-note by the instructor mashing a button. Then three questions that set up tonight's build.

**Q1. In the Game-Show Edition, `start_show()` insisted on tracking *every* piece of a show as its own task. A new output — say, a rumble motor — joins the victory show tonight. What does that machinery buy you, and what would break without it?**

<details>
<summary>Answer</summary>

Cancelling a task does **not** cancel tasks it started — so the round-reset can only clear the stage if it can reach every performer directly. Add a rumble coroutine through `start_show(fanfare, comet, rumble)` and the next round silences all three for free. Sneak it in with a bare `create_task()` inside another show and reset can't reach it: the motor buzzes into the next round's wait phase, lying to the players. Tonight's new channel plugs into three-session-old machinery *because* that machinery was built honestly.

</details>

**Q2. Your Session 5 game has no networking, but your Session 4 game did. Tonight you put the Session 4 grafts into the Session 5 file. What's different about grafting into a file that's changed since the grafts were written?**

<details>
<summary>Answer</summary>

The anchors moved. Session 4's grafts assumed `buzz()`, plain `led1`, a bare referee reset; the Game-Show Edition renamed, rewired, or replaced several of those (PWM beacon, `beep()`, show cancellation in the reset). So tonight is not "follow the recipe again" — it's **merging**: find where each graft's idea belongs *now*, not where its lines used to go. That's the everyday professional skill hiding in the capstone, and it's why the graded work budget is generous.

</details>

**Q3. Tonight your game runs from a battery with no Thonny attached. Every `print()` in your code — the standings, the fail-soft notes — goes where, exactly? And what does that change?**

<details>
<summary>Answer</summary>

Nowhere. No shell is listening; the text is composed and discarded. A shipped device's only outputs are the ones on the device — lights, sounds, rumble — and its network reports. That's why fail-soft stops being a rubric row and becomes survival: on battery there is no traceback to read, so a crash just looks like *death*. It's also tonight's design nudge: any information you care about had better be expressed in light or sound, not print.

</details>

---

[← Overview](00-overview.md) · [Session home](../README.md) · **Next:** [Part A — The Vibration Rig →](02-part-a-vibration.md)
