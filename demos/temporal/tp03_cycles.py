"""CYCLES — folding time at its period, and at the WRONG period.
Run: python tp03_cycles.py [--save DIR]"""
from _t import *

def linear():
    return tsplot(base, title="36 months, linear: seasonality or noise?")

def fold(period, overlay=False):
    n = (36 // period) * period
    M = base[:n].reshape(-1, period)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    if overlay:
        shades = [str(0.8 - 0.3 * i) for i in range(M.shape[0])]
        for i, row in enumerate(M):
            ax.plot(range(period), row, lw=1.5, color=shades[i % len(shades)])
        ax.set_title(f"cycles overlaid (period {period})", fontsize=10)
    else:
        ax.imshow(M, cmap="Greys", aspect="auto")
        ax.set_title(f"folded at period {period}: rows = cycles", fontsize=10)
        ax.set_yticks([])
    ax.set_xticks([0, period - 1], ["1", str(period)])
    fig.tight_layout(); return fig

b = Builder("Folding time at its period \u2014 the one sanctioned reordering", "tp03")
b.add("plot linear", linear(), "", "tp03_linear.png")
b.add("fold at period=12  # the true period", fold(12),
      "The summer stripe appears: same values, rearranged by a criterion time itself supplies.", "tp03_fold12.png")
b.branch("\u2192 overlay the cycles", fold(12, overlay=True),
      "Three years on one January\u2013December ruler: the seasonal shape AND its drift.", "tp03_overlay.png")
b.branch("fold at period=10  # the WRONG period", fold(10),
      "A diagonal 'drift' pattern \u2014 manufactured entirely by the fold. Wrong-period folding is how "
      "cycle plots lie; the period is a parameter with a truth value.", "tp03_fold10.png")
b.end("The prohibition stands \u2014 shuffled months are garbage \u2014 and the fold is its one exception, "
      "because a period is part of time's structure. State the period; defend the period.")
