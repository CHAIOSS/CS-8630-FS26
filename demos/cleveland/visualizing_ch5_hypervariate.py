"""VISUALIZING DATA — Ch. 5, Hypervariate Data
Key tools: the scatterplot matrix and BRUSHING — select in one panel,
see the selection everywhere (rendered statically here).
Run: python visualizing_ch5_hypervariate.py [--save DIR]"""
from _cleveland import *

rng = np.random.default_rng(55)
n = 220
d0 = rng.normal(0, 1, n)
d1 = d0*0.8 + rng.normal(0, .5, n)
d2 = rng.normal(0, 1, n)
d3 = np.where(d2 > 0.4, d0*0.9, -d0*0.2) + rng.normal(0, .4, n)   # conditional structure
X = np.c_[d0, d1, d2, d3]; names = ["v1", "v2", "v3", "v4"]
brush = d2 > 0.4                                                   # the brushed subset

fig, axes = plt.subplots(4, 4, figsize=(10.5, 9))
for i in range(4):
    for j in range(4):
        ax = axes[i, j]
        if i == j:
            ax.hist(X[:, i], bins=20, color="#C9D2D8")
            ax.hist(X[brush, i], bins=20, color=ACCENT, alpha=.85)
        else:
            ax.scatter(X[~brush, j], X[~brush, i], s=6, color="#B9C4CB", alpha=.7)
            ax.scatter(X[brush, j], X[brush, i], s=8, color=ACCENT, alpha=.85)
        ax.set_xticks([]); ax.set_yticks([])
        if i == 3: ax.set_xlabel(names[j], fontsize=9)
        if j == 0: ax.set_ylabel(names[i], fontsize=9)
axes[0, 2].add_patch(plt.Rectangle((0.4, X[:,0].min()), X[:,2].max()-0.4,
    X[:,0].max()-X[:,0].min(), fill=False, edgecolor=INK, lw=2, ls="--"))
fig.suptitle("SPLOM + brushing: select v3 > 0.4 (dashed box) — the v1–v4 relationship appears ONLY in the brushed subset",
             fontsize=11.5)
fig.tight_layout(rect=[0, 0, 1, 0.95])
finish(fig, "v5_splom_brush.png")

keypoints("Visualizing Data Ch.5 — Hypervariate Data", [
  "The SPLOM shows every pairwise projection; nothing is hidden, nothing is more than pairwise.",
  "Brushing is conditioning made interactive: a coplot you steer with your hand.",
  "Here brushing v3 reveals a v1-v4 dependence that exists only conditionally — pooled panels average it away.",
  "Static charts inherit this as linked highlighting; your project's linked views are this chapter, shipped.",
])
