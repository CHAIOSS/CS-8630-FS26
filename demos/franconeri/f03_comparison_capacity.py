"""FRANCONERI CLAIM 3 — Humans compare 2-4 things at a time.
Interactive: the same question asked of 2, 4, then 8 series; time each
consensus. The timing curve IS the capacity limit.
Run: python f03_comparison_capacity.py [--save DIR]"""
from _franconeri import *

rng = np.random.default_rng(3)
cats = ["Q1", "Q2", "Q3", "Q4"]

def grouped(n_series, ax):
    w = 0.8 / n_series
    data = rng.uniform(40, 90, (n_series, 4))
    for i in range(n_series):
        ax.bar(np.arange(4) + i * w, data[i], width=w)
    ax.set_xticks(np.arange(4) + 0.4, cats)
    return data

if "--save" in sys.argv:
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.5))
    for ax, n in zip(axes, [2, 4, 8]):
        grouped(n, ax); ax.set_title(f"{n} series", fontsize=10)
    fig.suptitle("Same question, growing cast: 'which series rose most Q2→Q3?' (claim 3)", fontsize=12)
    fig.tight_layout(); finish(fig, "f03_capacity.png")
else:
    times = []
    for n in [2, 4, 8]:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        grouped(n, ax); ax.set_title(f"{n} series — which rose most from Q2 to Q3?")
        plt.show(block=False); plt.pause(0.1)
        times.append(timed_enter(f"  {n} series: Enter when the room agrees: "))
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([2, 4, 8], times, "o-", color=ACCENT, lw=2, ms=9)
    ax.set_xlabel("series on screen"); ax.set_ylabel("seconds to consensus")
    ax.set_title("This room's comparison capacity, measured")
    plt.show()

claim("Claim 3 — the comparison budget", [
  "2-4 items compare; beyond that, readers skim and confabulate.",
  "The fix is not fewer data: grey the context, foreground ONE comparison.",
])
