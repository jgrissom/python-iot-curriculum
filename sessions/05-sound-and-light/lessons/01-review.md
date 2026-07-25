# Opening Review — What the Connected Game Taught Us

⏱️ **15 min** · instructor-led

[← Overview](00-overview.md) · [Session home](../README.md) · **Next:** [Warm-up: Two New Parts →](02-setup.md)

---

One bench demos a finished Session 4 game on the projector — including the moment the instructor stops the scoreboard and the game *doesn't care*. Then three questions, because two ideas from that game are tonight's load-bearing walls.

**Q1. In the connected game, why was `report_result()` fired with `create_task()`, but `fetch_standings()` awaited?**

<details>
<summary>Answer</summary>

The game never needs the POST's answer — waiting for it would park the round's feedback on the network's mood, so it's fire-and-forget. The standings *are* the point of the fetch — the print must appear before the next round arms, so the referee awaits it in the pause. The rule: **await when you need the answer now; `create_task()` when you only need it done.** Tonight's fanfares and light shows sit firmly in the second category.

</details>

**Q2. A victory fanfare takes six seconds to play. What happens to the reaction game if the player coroutine does `await play_fanfare()` — and where have you seen this before?**

<details>
<summary>Answer</summary>

That player coroutine is parked for six seconds — it isn't watching its button, so presses vanish; if the referee waits on the round, the whole game hangs in showbiz limbo. It's Session 4's blocking `requests.get()` freeze — and Session 3's `time.sleep()` before that — with a melody instead of a network round-trip. Slow *outputs* block exactly like slow *inputs*. Tonight's golden rule: **the show must not stop the game.**

</details>

**Q3. Fire-and-forget has a new wrinkle tonight: what should happen to a victory show that's still running when the next round starts?**

<details>
<summary>Answer</summary>

It must be *stopped*, not awaited and not ignored — leftover confetti during a fresh wait phase lies to the players (and a leftover fanfare note lies to everyone's ears). Session 4 never needed this: a stray POST just finishes harmlessly. A stray light show doesn't. The new tool is `task.cancel()`, and Part B's jukebox introduces it before the assignment leans on it.

</details>

> [!NOTE]
> Scoreboard epilogue: the class leaderboard stays up — tonight's stretch goal reconnects your game if you want your Game-Show Edition reporting wins mid-fanfare. But the graded path needs no network at all.

---

[← Overview](00-overview.md) · [Session home](../README.md) · **Next:** [Warm-up: Two New Parts →](02-setup.md)
