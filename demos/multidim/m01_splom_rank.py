"""JUXTAPOSE — the SPLOM, then Wilkinson's answer to too many panels.
Run: python m01_splom_rank.py [--save DIR]"""
from _md import *

def panel(d1, d2, ax=None):
    fig = None
    if ax is None: fig, ax = plt.subplots(figsize=(4.6, 3.6))
    ax.scatter(sub[d1], sub[d2], s=5, alpha=.3, color=INK)
    ax.set_xlabel(LAB[d1], fontsize=9); ax.set_ylabel(LAB[d2], fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    return fig

def splom(hl=None, ranked=False):
    order = DIMS
    corr = sub[DIMS].corr().abs()
    fig, axes = plt.subplots(4, 4, figsize=(6.6, 5.8))
    pairs = sorted(((corr.loc[a, b], a, b) for i, a in enumerate(DIMS) for b in DIMS[i+1:]), reverse=True)
    top3 = {(a, b) for _, a, b in pairs[:3]} | {(b, a) for _, a, b in pairs[:3]}
    for i, di in enumerate(order):
        for j, dj in enumerate(order):
            ax = axes[i, j]
            if i == j: ax.hist(sub[di], bins=16, color=INK)
            else:
                dim = ranked and (di, dj) not in top3
                ax.scatter(sub[dj], sub[di], s=3, alpha=.06 if dim else .3,
                           color=MUTED if dim else (ACCENT if ranked else INK))
                if ranked and (di, dj) in top3:
                    ax.text(.05, .82, f"|r|={corr.loc[di,dj]:.2f}", transform=ax.transAxes, fontsize=8, color=ACCENT)
            ax.set_xticks([]); ax.set_yticks([])
            if j == 0: ax.set_ylabel(LAB[di], fontsize=8)
            if i == 3: ax.set_xlabel(LAB[dj], fontsize=8)
    fig.tight_layout()
    return fig

b = Builder("Too many honest panels: what does juxtaposition cost?", "m01")
b.add("one pair: scatter(size, files)", panel("loglines", "logfiles"),
      "One fully honest plane — position on common scales. The best judgment vision offers.", "m01_pair.png")
b.add("ALL pairs: the scatterplot matrix", splom(),
      "Every pair honest; nothing hidden. Now imagine 40 dims: 780 of these. Who reads them?", "m01_splom.png")
b.add("rank the panels by a stated measure (|r|)  # mini-scagnostics", splom(ranked=True),
      "Wilkinson's scagnostics idea at toy scale: compute a per-panel measure, read only where it "
      "points. The ordering is stated, data-derived, global — last week's rule, at work.", "m01_ranked.png")
b.end("Juxtapose scales in panels, not in attention. The escape from the escape is a defensible ranking.")
