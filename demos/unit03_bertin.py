"""CS 8630 Unit 3 demo — the level mismatch, felt.
Same ordered data, encoded with hue (selective) vs value (ordered).
Ask the class: 'point at the 3rd-highest region' — time both.
Run: python unit03_bertin.py [--save DIR]"""
from _style import *

rng = np.random.default_rng(3)
grid = rng.uniform(10, 100, (5, 8))
qual = ["#E4572E", "#1C7293", "#8A5A9E", "#5FA052", "#D9A404", "#2B3A42", "#B85042", "#69A297"]

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
# WRONG: ordered data in qualitative hues (rank-binned into 8 hues)
bins = np.digitize(grid, np.quantile(grid, np.linspace(0, 1, 9)[1:-1]))
axes[0].imshow(np.array(qual)[bins] == None)  # placeholder sizing
axes[0].clear()
for (i, j), b in np.ndenumerate(bins):
    axes[0].add_patch(plt.Rectangle((j, 4 - i), 1, 1, color=qual[int(b)]))
axes[0].set_xlim(0, 8); axes[0].set_ylim(0, 5); axes[0].set_aspect(1)
axes[0].axis("off"); axes[0].set_title("Hue: selective, NOT ordered\n'Find the 3rd-highest region' — go", fontsize=11)
# RIGHT: value/luminance
im = axes[1].imshow(grid, cmap="Blues", origin="lower", extent=[0, 8, 0, 5])
axes[1].set_aspect(1); axes[1].axis("off")
axes[1].set_title("Value: ordered — the ranking is legible", fontsize=11)
fig.colorbar(im, ax=axes[1], shrink=0.8)
fig.suptitle("Bertin's match principle: the variable's level must meet the data's level", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.88])
finish(fig, "unit03_mismatch.png")
