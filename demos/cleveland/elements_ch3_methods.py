"""ELEMENTS OF GRAPHING DATA — Ch. 3, Graphical Methods
Key methods demonstrated: the dot plot (Cleveland's invention) vs bars;
loess on a scatter; the Tukey mean-difference plot; superposed vs
juxtaposed curves. Run: python elements_ch3_methods.py [--save DIR]"""
from _cleveland import *

rng = np.random.default_rng(3)

# Fig A: dot plot vs bar chart
labs = ["augur", "frontend", "docs", "infra", "ml-pipeline", "website", "cli", "sdk"]
vals = np.sort(rng.uniform(58, 96, len(labs)))[::-1]
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
axes[0].barh(labs[::-1], vals[::-1], color=INK)
axes[0].set_xlim(0, 100); axes[0].set_title("Bar chart: length encoding —\nzero baseline is mandatory, resolution suffers", fontsize=10)
axes[1].plot(vals[::-1], labs[::-1], "o", color=ACCENT, ms=7)
axes[1].set_xlim(55, 100)
axes[1].grid(axis="y", color="#E3E8EB", lw=1)
axes[1].set_title("Cleveland dot plot: position encoding —\nnon-zero scale is legitimate, resolution returns", fontsize=10)
fig.suptitle("The dot plot: position along a common scale, freed from the zero-baseline tax (Elements Ch.3)", fontsize=12)
fig.tight_layout()
finish(fig, "e3_dotplot.png")

# Fig B: loess on scatter, span comparison
x = rng.uniform(0, 10, 120)
y = np.sin(x) + x/4 + rng.normal(0, .35, 120)
fig, ax = plt.subplots(figsize=(9, 4))
ax.scatter(x, y, s=18, color=MUTED, alpha=.7)
for frac, col, lab in [(0.15, ACCENT, "span 0.15: chases noise"), (0.4, INK, "span 0.40: the structure"),
                       (0.9, TEAL, "span 0.90: erases the structure")]:
    xs, ys = loess(x, y, frac=frac)
    ax.plot(xs, ys, color=col, lw=2.4, label=lab)
ax.legend(fontsize=9)
ax.set_title("Loess — Cleveland's own smoother; the span is an authored parameter (Elements Ch.3)")
fig.tight_layout()
finish(fig, "e3_loess.png")

# Fig C: Tukey mean-difference plot
before = rng.normal(70, 9, 40)
after = before + rng.normal(2.5, 3.5, 40)
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.9))
axes[0].scatter(before, after, s=22, color=INK)
lims = [45, 100]
axes[0].plot(lims, lims, color=MUTED, ls="--"); axes[0].set_xlim(lims); axes[0].set_ylim(lims)
axes[0].set_xlabel("before"); axes[0].set_ylabel("after")
axes[0].set_title("Paired scatter: is 'after' higher?\nJudging distance-to-diagonal is hard", fontsize=10)
m, d = (before+after)/2, after-before
axes[1].scatter(m, d, s=22, color=ACCENT)
axes[1].axhline(0, color=MUTED, ls="--")
axes[1].axhline(d.mean(), color=INK, lw=2)
axes[1].set_xlabel("mean of pair"); axes[1].set_ylabel("difference (after − before)")
axes[1].set_title("Mean–difference plot: the question\nbecomes distance-to-horizontal — easy", fontsize=10)
fig.suptitle("Re-express so the judgment is the easy one: the m–d plot (Elements Ch.3)", fontsize=12)
fig.tight_layout()
finish(fig, "e3_meandiff.png")

keypoints("Elements Ch.3 — Graphical Methods", [
  "Dot plots: position judgments without the zero-baseline tax bars must pay.",
  "Loess makes trend visible in noise; its span is a choice you must disclose.",
  "The mean-difference plot converts a hard visual judgment into an easy one — Cleveland's design move in miniature.",
  "Method choice is perception engineering, not chart shopping.",
])
