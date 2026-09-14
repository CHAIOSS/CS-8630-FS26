"""FRANCONERI CLAIM 4 — Gestalt grouping is pre-attentive and free;
connectedness beats proximity. Interactive: the class votes on 'which
dots pair up' before and after lines are drawn. Votes flip.
Run: python f04_grouping_gestalt.py [--save DIR]"""
from _franconeri import *

xs = np.arange(8)

def dots(ax, lines=False):
    ax.scatter(xs, [1]*8, s=140, color=INK, zorder=3)
    for i, x in enumerate(xs):
        ax.annotate(str(i+1), (x, 1), ha="center", va="center", color="white", fontsize=9, zorder=4)
    if lines:
        for a, b in [(0, 5), (1, 4), (2, 7), (3, 6)]:
            ax.plot([a, b], [1, 1], color=ACCENT, lw=2.5, zorder=1)
    ax.set_xlim(-1, 8); ax.set_ylim(0.4, 1.6); ax.axis("off")

if "--save" in sys.argv:
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 2.6))
    dots(axes[0]); axes[0].set_title("Which dots go together? (proximity answers)", fontsize=10)
    dots(axes[1], True); axes[1].set_title("Now? Connectedness overrides proximity", fontsize=10)
    fig.suptitle("Grouping happens before attention — you cannot opt readers out (claim 4)", fontsize=12)
    fig.tight_layout(); finish(fig, "f04_gestalt.png")
else:
    fig, ax = plt.subplots(figsize=(8, 2.6)); dots(ax)
    ax.set_title("VOTE: does dot 1 pair with dot 2, or with dot 6?")
    plt.show(block=False); plt.pause(0.1)
    input("  collect the vote (nearly all say 2), then Enter: ")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 2.6)); dots(ax, True)
    ax.set_title("Same dots. VOTE again.")
    plt.show(block=False); plt.pause(0.1)
    input("  the vote flips to 6 — Enter to close: ")
    plt.close(fig)

claim("Claim 4 — grouping for free", [
  "Proximity, similarity, connectedness organize the display before attention arrives.",
  "Connectedness > proximity: one line re-partitions the whole display.",
  "Accidental grouping (palettes, gridlines) misinforms just as automatically.",
])
