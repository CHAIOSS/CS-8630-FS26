"""VISUALIZING DATA — Ch. 1, Introduction
Key point: visualization is iterative FITTING — fit the pattern, then
visualize the residuals; repeat until the residuals are structureless.
Run: python visualizing_ch1_introduction.py [--save DIR]"""
from _cleveland import *

rng = np.random.default_rng(11)
x = np.sort(rng.uniform(0, 10, 130))
y = 3 + 0.8*x + 1.1*np.sin(x*1.2) + rng.normal(0, .3, 130)

fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.6))
axes[0].scatter(x, y, s=16, color=MUTED)
b, a = np.polyfit(x, y, 1)
axes[0].plot(x, a+b*x, color=INK, lw=2)
axes[0].set_title("Step 1 — fit: a line looks plausible", fontsize=10)
r1 = y - (a+b*x)
axes[1].scatter(x, r1, s=16, color=ACCENT)
axes[1].axhline(0, color=MUTED, ls="--")
xs, ys = loess(x, r1, frac=.3)
axes[1].plot(xs, ys, color=INK, lw=2)
axes[1].set_title("Step 2 — residuals: structure remains!\nThe fit is incomplete", fontsize=10)
xs2, ys2 = loess(x, y, frac=.25)
r2 = y - np.interp(x, xs2, ys2)
axes[2].scatter(x, r2, s=16, color=TEAL)
axes[2].axhline(0, color=MUTED, ls="--")
axes[2].set_title("Step 3 — refit (loess) and re-check:\nresiduals now structureless — stop", fontsize=10)
fig.suptitle("Cleveland's paradigm: visualization = fit + residual, iterated (Visualizing Data Ch.1)", fontsize=12)
fig.tight_layout()
finish(fig, "v1_fitresid.png")

keypoints("Visualizing Data Ch.1 — Introduction", [
  "The book's engine: every dataset is pattern + residual; visualize both, iterate.",
  "A residual plot with structure is an unfinished analysis, not a finished chart.",
  "This paradigm is why Cleveland's graphics are analysis tools first, presentation second.",
])
