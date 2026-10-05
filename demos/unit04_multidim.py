"""CS 8630 Unit 4 demo — three idioms, one dataset; then the projection lie.
Run: python unit04_multidim.py [--save DIR]"""
from _style import *
import pandas as pd
from pandas.plotting import parallel_coordinates
from sklearn.decomposition import PCA

rng = np.random.default_rng(8630)
n = 60
# two genuine clusters in 6-D + one bridge point
c1 = rng.normal(0, 1, (n, 6)) + np.array([2, 2, 0, 0, 1, 0])
c2 = rng.normal(0, 1, (n, 6)) + np.array([-2, -2, 1, 1, -1, 0])
X = np.vstack([c1, c2, [[0, 0, .5, .5, 0, 0]]])
lab = ["A"] * n + ["B"] * n + ["bridge"]
cols = [f"d{i}" for i in range(6)]
df = pd.DataFrame(X, columns=cols); df["cluster"] = lab

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
parallel_coordinates(df, "cluster", ax=axes[0],
    color=[TEAL, ACCENT, INK], alpha=.45, linewidth=1)
axes[0].legend(fontsize=8); axes[0].set_title("Parallel coordinates:\noutliers & axis-pair structure", fontsize=10)
axes[1].scatter(df.d0, df.d1, c=[{"A": TEAL, "B": ACCENT, "bridge": INK}[l] for l in lab], s=18)
axes[1].set_xlabel("d0"); axes[1].set_ylabel("d1")
axes[1].set_title("One SPLOM panel:\npairwise, position-encoded, honest", fontsize=10)
P = PCA(2).fit_transform(X)
axes[2].scatter(P[:, 0], P[:, 1], c=[{"A": TEAL, "B": ACCENT, "bridge": INK}[l] for l in lab], s=18)
axes[2].annotate("this gap is\nNOT a distance you\nmay quote", xy=(0, 0), xytext=(1.5, 2.6),
    fontsize=9, color=ACCENT, arrowprops=dict(arrowstyle="->", color=ACCENT))
axes[2].set_title("Projection (PCA):\ncluster gestalt real, distances distorted", fontsize=10)
fig.suptitle("Same 6-D data, three idioms — task picks the winner", fontsize=12)
fig.tight_layout()
finish(fig, "unit04_idioms.png")
