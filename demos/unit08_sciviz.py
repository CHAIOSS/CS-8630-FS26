"""CS 8630 Unit 8 demo — the isovalue is an authored statistic.
One scalar field, three thresholds, three 'anatomies.'
Run: python unit08_sciviz.py [--save DIR]"""
from _style import *

x, y = np.meshgrid(np.linspace(-3, 3, 400), np.linspace(-3, 3, 400))
field = (np.exp(-((x - .8)**2 + (y - .6)**2)) +
         0.85 * np.exp(-((x + 1.1)**2 + (y + .8)**2) / .55) +
         0.35 * np.exp(-((x - 1.6)**2 + (y + 1.4)**2) / .25))

fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
for ax, iso in zip(axes, (0.25, 0.45, 0.7)):
    ax.imshow(field, extent=[-3, 3, -3, 3], origin="lower", cmap="Greys", alpha=.55)
    ax.contour(x, y, field, levels=[iso], colors=[ACCENT], linewidths=2.5)
    n = len(plt.contour(x, y, field, levels=[iso]).allsegs[0]); plt.close()
    ax.set_title(f"isovalue = {iso}\n→ {n} structure(s) 'exist'", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("Same field. The threshold decides how many things there are.", fontsize=12)
fig.tight_layout()
finish(fig, "unit08_isovalues.png")
