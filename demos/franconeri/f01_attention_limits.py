"""FRANCONERI CLAIM 1 — Vision is a limited-attention channel.
Interactive: the class counts 7s in a digit grid (timed), then counts
again with the 7s given their own channel. The timing gap is the claim.
Run: python f01_attention_limits.py [--save DIR]"""
from _franconeri import *
import random

rng = np.random.default_rng()  # fresh grid every class
def make_grid():
    g = rng.integers(0, 10, (8, 16)); g[g == 7] = 1
    for _ in range(6):
        g[rng.integers(0, 8), rng.integers(0, 16)] = 7
    return g

def show(g, bold, title):
    fig, ax = plt.subplots(figsize=(9, 4))
    for i in range(8):
        for j in range(16):
            hot = bold and g[i, j] == 7
            ax.text(j, 7 - i, str(g[i, j]), ha="center", va="center", fontsize=13,
                    color=ACCENT if hot else INK, fontweight="bold" if hot else "normal")
    ax.set_xlim(-.6, 15.6); ax.set_ylim(-.6, 7.6); ax.axis("off"); ax.set_title(title)
    return fig

if "--save" in sys.argv:
    g = np.array([[3,1,4,7,5,9,2,6,5,3,5,7,9,3,2,3],[8,4,6,7,2,6,4,3,3,8,3,7,9,5,0,2]]*4)
    for bold, name in [(False, "f01_serial.png"), (True, "f01_popout.png")]:
        fig = show(g, bold, "Count the 7s" + (" — now with their own channel" if bold else ""))
        finish(fig, name)
else:
    g = make_grid()
    fig = show(g, False, "COUNT THE 7s — press Enter in terminal when the room agrees")
    plt.show(block=False); plt.pause(0.1)
    t1 = timed_enter("  counting... Enter when done: ")
    plt.close(fig)
    fig = show(g, True, "Same grid — count again")
    plt.show(block=False); plt.pause(0.1)
    t2 = timed_enter("  counting... Enter when done: ")
    plt.close(fig)
    print(f"\n  Serial search: {t1:.1f}s   With a channel: {t2:.1f}s   → the attention gate, timed.")

claim("Claim 1 — limited attention", [
  "You sample a display; you don't 'see' it. Salience decides what gets sampled.",
  "Design's first job: give the message its own channel.",
])
