"""HIERARCHY — containment vs connection, the treemap trade, and the
matrix that grows a dendrogram. Run: python m04_hierarchy.py [--save DIR]"""
from _md import *
import squarify
from scipy.cluster import hierarchy as sch

counts = df.groupby(["repo", "kind"]).size().rename("n").reset_index()
tot = counts.groupby("repo").n.sum().sort_values(ascending=False)

def nodelink():
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    ax.scatter([0.5], [0.92], s=170, color=INK, zorder=3)
    xs = np.linspace(0.1, 0.9, len(tot))
    for xi, (r, _) in zip(xs, tot.items()):
        ax.plot([0.5, xi], [0.9, 0.62], color="#C9D2D8", lw=1)
        ax.scatter([xi], [0.6], s=95, color=PAL4[r], zorder=3)
        ks = counts[counts.repo == r]
        for kx in np.linspace(xi - 0.08, xi + 0.08, len(ks)):
            ax.plot([xi, kx], [0.58, 0.32], color="#C9D2D8", lw=.7)
            ax.scatter([kx], [0.3], s=26, color=MUTED, zorder=3)
    ax.axis("off"); fig.tight_layout(); return fig

def icicle():
    fig, ax = plt.subplots(figsize=(5.8, 3.6)); y0 = 0.66
    ax.add_patch(mpatches.Rectangle((0, y0), 1, 0.3, color=INK)); x = 0
    for r, v in tot.items():
        w = v / tot.sum()
        ax.add_patch(mpatches.Rectangle((x, y0 - 0.32), w - 0.004, 0.3, color=PAL4[r]))
        kx = x
        for _, row in counts[counts.repo == r].sort_values("n", ascending=False).iterrows():
            kw = w * row.n / v
            ax.add_patch(mpatches.Rectangle((kx, y0 - 0.64), kw - 0.003, 0.3, color=MUTED, alpha=.6))
            kx += kw
        x += w
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); fig.tight_layout(); return fig

def tmap(squar):
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    leaves = counts.sort_values(["repo", "n"], ascending=[True, False])
    if squar:
        rects = squarify.squarify(squarify.normalize_sizes(leaves.n.values, 100, 70), 0, 0, 100, 70)
        for rect, (_, row) in zip(rects, leaves.iterrows()):
            ax.add_patch(mpatches.Rectangle((rect["x"], rect["y"]), rect["dx"] - .3, rect["dy"] - .3,
                color=PAL4[row.repo], alpha=.75, ec="white", lw=1))
    else:
        x = 0
        for r, v in tot.items():
            w = 100 * v / tot.sum(); y = 0
            for _, row in leaves[leaves.repo == r].iterrows():
                h = 70 * row.n / v
                ax.add_patch(mpatches.Rectangle((x, y), w - .4, h - .4, color=PAL4[r], alpha=.75, ec="white", lw=1))
                y += h
            x += w
    ax.set_xlim(0, 100); ax.set_ylim(0, 70); ax.axis("off"); fig.tight_layout(); return fig

def cluster(step):
    M0 = np.zeros((12, 15)); r2 = np.random.default_rng(7)
    gr = [0]*4 + [1]*4 + [2]*4; gc = [0]*5 + [1]*5 + [2]*5
    for i in range(12):
        for j in range(15):
            M0[i, j] = r2.random() < (0.85 if gr[i] == gc[j] else 0.08)
    Ms = M0[r2.permutation(12)][:, r2.permutation(15)]
    if step == 0:
        fig, ax = plt.subplots(figsize=(5.2, 3.6))
        ax.imshow(Ms, cmap="Greys", aspect="auto", vmin=0, vmax=1)
        ax.set_xticks([]); ax.set_yticks([]); fig.tight_layout(); return fig
    Zr = sch.linkage(Ms, "average"); Zc = sch.linkage(Ms.T, "average")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4), gridspec_kw={"width_ratios": [1, 2.1]})
    sch.dendrogram(Zr, ax=axes[0], orientation="left", link_color_func=lambda *_: INK)
    axes[0].set_xticks([]); axes[0].set_yticks([]); axes[0].set_title("the receipt", fontsize=9)
    axes[1].imshow(Ms[sch.leaves_list(Zr)][:, sch.leaves_list(Zc)], cmap="Greys", aspect="auto", vmin=0, vmax=1)
    axes[1].set_xticks([]); axes[1].set_yticks([]); axes[1].set_title("machine-chosen permutation", fontsize=9)
    fig.tight_layout(); return fig

b = Builder("Nesting is data \u2014 what should the picture spend on it?", "m04")
b.add("repo \u2283 kind as CONNECTION (node-link)", nodelink(),
      "Topology explicit; nearly all area spent on whitespace; every leaf an identical dot \u2014 sizes invisible.", "m04_node.png")
b.add("the same tree as CONTAINMENT (icicle)", icicle(),
      "Depth = rows, siblings keep order, width = quantity. Your profiler's flame graph.", "m04_icicle.png")
b.add("containment, space-filling: treemap (slice-and-dice)", tmap(False),
      "Every pixel now quantity \u2014 and the slivers' areas are incomparable.", "m04_slice.png")
b.branch("  \u2192 squarified", tmap(True),
      "Aspect ratios \u2192 1: better area judgments, sibling order sacrificed. Same tree, opposite trade.", "m04_squar.png")
b.add("last week's shuffled matrix", cluster(0), "", "m04_shuf.png")
b.add("  \u2192 hierarchical clustering: permutation + RECEIPT", cluster(1),
      "The linkage chooses the ordering (stated, data-derived, global) and hands back its merge "
      "history as a dendrogram. Bertin's paper strips, formalized \u2014 and auditable: change the "
      "linkage or metric, the tree changes.", "m04_dendro.png")
b.end("Real containment: draw it. Clustered containment: a hypothesis wearing a diagram's confidence \u2014 "
      "keep the receipt, and ask what the flat view said first.")
