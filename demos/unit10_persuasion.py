"""CS 8630 Unit 10 demo — the title does the work.
IDENTICAL chart rendered twice; only the title changes. Then the class
votes on what the chart 'showed.' Run: python unit10_persuasion.py [--save DIR]"""
from _style import *

rng = np.random.default_rng(10)
months = np.arange(24)
reviews = 14 + 0.12 * months + np.sin(months / 2.4) * 1.8 + rng.normal(0, 0.9, 24)

def panel(ax, title, color):
    ax.plot(months, reviews, "o-", color=color, lw=2, ms=4)
    ax.set_ylim(0, 22)
    ax.set_xlabel("month"); ax.set_ylabel("median review latency (hrs)")
    ax.set_title(title, fontsize=11, loc="left", fontweight="bold")
    ax.annotate("policy change", xy=(12, reviews[12]), xytext=(13.5, 5),
        fontsize=9, color=MUTED, arrowprops=dict(arrowstyle="->", color=MUTED))

fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
panel(axes[0], "Review latency creeps upward despite policy change", INK)
panel(axes[1], "Review latency stable: policy change holds the line", TEAL)
fig.suptitle("Same marks, same data — the title tells the reader what they saw (Franconeri)", fontsize=12)
fig.tight_layout()
finish(fig, "unit10_titles.png")
