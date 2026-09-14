"""VISUALIZING DATA — Ch. 4, Trivariate Data
Key tool: the COPLOT (conditioning plot) — Cleveland's signature device.
y vs x in panels conditioned on overlapping intervals (shingles) of z.
Run: python visualizing_ch4_trivariate.py [--save DIR]"""
from _cleveland import *

rng = np.random.default_rng(44)
n = 500
xv = rng.uniform(0, 10, n)
z = rng.uniform(0, 10, n)
# interaction: the x-y slope DEPENDS on z — invisible in a pooled scatter
y = 1 + (z - 5)/3 * xv + rng.normal(0, 1.2, n)

def shingles(z, k=6, overlap=0.5):
    """Cleveland's overlapping intervals."""
    qs = np.linspace(0, 1, k+1)
    edges = np.quantile(z, qs)
    ivals = []
    for i in range(k):
        lo, hi = edges[i], edges[i+1]
        pad = (hi - lo) * overlap / 2
        ivals.append((lo - pad, hi + pad))
    return ivals

ivals = shingles(z)
fig = plt.figure(figsize=(12.5, 5.4))
# shingle diagram on top
axs = fig.add_axes([0.07, 0.86, 0.86, 0.10])
for i, (lo, hi) in enumerate(ivals):
    axs.plot([lo, hi], [i % 2, i % 2], lw=6, color=ACCENT if i % 2 else INK, solid_capstyle="butt")
axs.set_yticks([])
axs.set_title("Coplot: y vs x | z  —  panels condition on these overlapping shingles of z (given)", fontsize=11, loc="left")
for i, (lo, hi) in enumerate(ivals):
    ax = fig.add_axes([0.07 + (i % 3)*0.31, 0.46 - (i // 3)*0.36, 0.26, 0.30])
    m = (z >= lo) & (z <= hi)
    ax.scatter(xv[m], y[m], s=8, color=MUTED, alpha=.6)
    xs, ys = loess(xv[m], y[m], frac=.6)
    ax.plot(xs, ys, color=INK, lw=2)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(y.min(), y.max())
    ax.set_title(f"z ∈ [{lo:.1f}, {hi:.1f}]", fontsize=8.5)
finish(fig, "v4_coplot.png")

keypoints("Visualizing Data Ch.4 — Trivariate Data", [
  "The coplot answers 'how does y-vs-x CHANGE with z' — interactions a pooled scatter averages away.",
  "Shingles overlap deliberately: smooth transitions between panels, points shared across neighbors.",
  "Here the slope flips sign across z: the pooled scatter of this data shows almost nothing.",
  "Slicing/conditioning is the trivariate move; Unit 4's faceting is its grammar-of-graphics descendant.",
])
