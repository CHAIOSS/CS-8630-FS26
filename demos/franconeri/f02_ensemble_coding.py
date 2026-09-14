"""FRANCONERI CLAIM 2 — Ensemble statistics are extracted in a glance.
Interactive: a scatter flashes for half a second; the class calls the
trend anyway. Item questions at the same exposure fail. Score both.
Run: python f02_ensemble_coding.py [--save DIR]"""
from _franconeri import *

rng = np.random.default_rng()

def cloud(trend):
    x = rng.uniform(0, 10, 60)
    y = trend * x * 0.5 + rng.normal(0, 1.6, 60) + 5
    return x, y

if "--save" in sys.argv:
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for ax, tr, t in [(axes[0], 1, "flashed 0.5 s: trend read anyway"),
                      (axes[1], -1, "same exposure: 'is point 17 above point 41?' — impossible")]:
        x, y = cloud(tr); ax.scatter(x, y, s=18, color=INK); ax.set_title(t, fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Ensembles are free; items are rationed (Franconeri claim 2)", fontsize=12)
    fig.tight_layout(); finish(fig, "f02_ensemble.png")
else:
    score = 0
    print("\nSix flashes, 0.6 s each. Class calls UP or DOWN after each.\n")
    for i in range(6):
        tr = rng.choice([-1, 1])
        x, y = cloud(tr)
        fig, ax = plt.subplots(figsize=(6, 4.5))
        ax.scatter(x, y, s=18, color=INK); ax.set_xticks([]); ax.set_yticks([])
        plt.show(block=False); plt.pause(0.6); plt.close(fig)
        g = input(f"  flash {i+1} — class says (u/d): ").strip().lower()
        ok = (g == "u") == (tr > 0); score += ok
        print(f"    {'✓' if ok else '✗'}  (trend was {'UP' if tr>0 else 'DOWN'})")
    print(f"\n  {score}/6 from half-second glances — that's ensemble coding.")
    print("  Now ask any ITEM question about the last flash. Silence — that's the ration.")

claim("Claim 2 — ensemble coding", [
  "Means, trends, spreads: parallel extraction, milliseconds.",
  "Design the ensemble read first; items are the reader's second visit.",
])
