"""CS 8630 Unit 6 demo — four maps, one dataset. No GIS stack needed:
a tile-grid 'state' map shows normalization and classification doing
all the work. Run: python unit06_geo.py [--save DIR]"""
from _style import *
from matplotlib.colors import BoundaryNorm
from matplotlib import cm

rng = np.random.default_rng(6)
R, C = 5, 8                                  # 40 fake states
pop = rng.lognormal(1.2, 0.8, (R, C)) * 1e5  # skewed populations
rate = rng.uniform(150, 850, (R, C))         # true per-capita rate
counts = rate * pop / 1e5                    # observed counts

def tile(ax, data, cmap, norm, title):
    ax.imshow(data, cmap=cmap, norm=norm, origin="lower")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=10)

fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.2))
tile(axes[0, 0], counts, "Blues", None, "Raw counts\n(this is mostly a population map)")
tile(axes[0, 1], rate, "Blues", None, "Per 100k\nthe actual phenomenon")
q = np.quantile(rate, [0, .2, .4, .6, .8, 1])
tile(axes[1, 0], rate, cm.Blues, BoundaryNorm(q, 256), "Per 100k, QUANTILE breaks\nevery class equally full — dramatic")
e = np.linspace(rate.min(), rate.max(), 6)
tile(axes[1, 1], rate, cm.Blues, BoundaryNorm(e, 256), "Per 100k, EQUAL-INTERVAL breaks\nsame data — calmer country")
fig.suptitle("One dataset, four defensible-looking maps — three of them mislead", fontsize=12)
fig.tight_layout()
finish(fig, "unit06_fourmaps.png")
