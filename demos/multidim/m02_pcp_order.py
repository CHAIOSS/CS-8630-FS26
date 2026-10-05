"""FUSE — parallel coordinates, one axis at a time; then the order swap.
Run: python m02_pcp_order.py [--save DIR]"""
from _md import *

def pcp(order, colour=True, note=None):
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    Z = (sub[order] - df[order].mean()) / df[order].std()
    for _, row in Z.iterrows():
        c = PAL4[sub.loc[row.name, "repo"]] if colour else INK
        ax.plot(range(len(order)), row.values, lw=.5, alpha=.25, color=c)
    ax.set_xticks(range(len(order)), [LAB[d] for d in order], fontsize=9)
    ax.set_yticks([])
    for xi in range(len(order)): ax.axvline(xi, color="#C9D2D8", lw=1, zorder=0)
    if note: ax.set_title(note, fontsize=9.5, color=MUTED)
    fig.tight_layout()
    return fig

b = Builder("Forty axes on one plane — what did the fusion cost?", "m02")
b.add("two axes: size | files", pcp(["loglines", "logfiles"], colour=False),
      "Between adjacent rulers the weave IS the relation: near-parallel segments = positive correlation.", "m02_two.png")
b.add("  + reviews", pcp(["loglines", "logfiles", "reviews"], colour=False), "", "m02_three.png")
b.add("  + latency   (all four, hue = repo)", pcp(DIMS),
      "Every dimension present at once — the fuse escape's promise, paid for in clutter. "
      "You read per-repo BANDS, not 700 lines: ensembles carry it.", "m02_four.png")
b.branch("SWAP: size | reviews | files | latency", pcp(["loglines", "reviews", "logfiles", "loghours"]),
      "One swap. size\u2013files no longer adjacent \u2014 their correlation just vanished from the picture. "
      "A PCP shows only the k\u22121 adjacencies you chose of k(k\u22121)/2 pairs.", "m02_swapped.png")
b.end("Axis order is the reorderable matrix in a new costume. What criterion orders YOURS \u2014 and is it stated?")
