"""FRANCONERI CLAIM 6 — Titles steer what readers take away and remember.
Interactive: the chart shows for 6 seconds with title A; the class writes
one sentence. Repeat with title B. Read sentences aloud; they diverge.
Run: python f06_titles_framing.py [--save DIR]"""
from _franconeri import *

rng = np.random.default_rng(6)
t = np.arange(24)
v = 14 + 0.12 * t + np.sin(t / 2.4) * 1.8 + rng.normal(0, 0.9, 24)
TITLES = ["Review latency creeps upward despite policy change",
          "Review latency stable: policy change holds the line"]

def chart(title, col):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(t, v, "o-", color=col, lw=2, ms=4)
    ax.set_ylim(0, 22); ax.set_xlabel("month"); ax.set_ylabel("median review latency (hrs)")
    ax.axvline(12, color=MUTED, ls="--", lw=1.2)
    ax.set_title(title, loc="left", fontweight="bold", fontsize=12)
    return fig

if "--save" in sys.argv:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
    for ax, ti, col in zip(axes, TITLES, [INK, TEAL]):
        ax.plot(t, v, "o-", color=col, lw=2, ms=4); ax.set_ylim(0, 22)
        ax.axvline(12, color=MUTED, ls="--", lw=1.2)
        ax.set_title(ti, loc="left", fontweight="bold", fontsize=10)
    fig.suptitle("Identical marks. The title decides what readers remember the chart said (claim 6)", fontsize=12)
    fig.tight_layout(); finish(fig, "f06_titles.png")
else:
    for i, (ti, col) in enumerate(zip(TITLES, [INK, TEAL]), 1):
        fig = chart(ti, col)
        plt.show(block=False); plt.pause(6); plt.close(fig)
        input(f"  round {i}: everyone writes ONE sentence — what did the chart show? Enter when done: ")
    print("\n  Read a few sentences from each round aloud. Same marks; two memories.")

claim("Claim 6 — titles do the work", [
  "The title often determines recalled content more than the marks do.",
  "A claiming title is legitimate exactly when the encoding can cash it (Unit 10).",
])
