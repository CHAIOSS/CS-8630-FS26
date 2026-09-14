"""VISUALIZING DATA — Ch. 3, Bivariate Data
Key tools: loess with span choice, residual-dependence plots, robust
(bisquare) fitting against outliers.
Run: python visualizing_ch3_bivariate.py [--save DIR]"""
from _cleveland import *

rng = np.random.default_rng(33)
x = np.sort(rng.uniform(0, 10, 140))
y = 2 + 1.5*np.log1p(x) + rng.normal(0, .25, 140)
y[::17] += rng.uniform(2, 4, len(y[::17]))     # contaminate with outliers

fig, axes = plt.subplots(1, 3, figsize=(12.8, 3.7))
axes[0].scatter(x, y, s=14, color=MUTED, alpha=.8)
xs0, ys0 = loess(x, y, frac=.4, it=0)
xs1, ys1 = loess(x, y, frac=.4, it=4)
axes[0].plot(xs0, ys0, color=ACCENT, lw=2.2, label="loess, no robustness:\noutliers drag the fit")
axes[0].plot(xs1, ys1, color=INK, lw=2.2, label="bisquare-robust loess:\nthe bulk's structure")
axes[0].legend(fontsize=8)
axes[0].set_title("Robustness is a fitting decision", fontsize=10)

resid = y - np.interp(x, xs1, ys1)
axes[1].scatter(x, resid, s=14, color=TEAL)
axes[1].axhline(0, ls="--", color=MUTED)
xs2, ys2 = loess(x, resid, frac=.4)
axes[1].plot(xs2, ys2, color=INK, lw=2)
axes[1].set_title("Residual-dependence plot:\nflat loess of residuals = fit captured x", fontsize=10)

aresid = np.sqrt(np.abs(resid))
axes[2].scatter(x, aresid, s=14, color=MUTED)
xs3, ys3 = loess(x, aresid, frac=.5)
axes[2].plot(xs3, ys3, color=ACCENT, lw=2)
axes[2].set_title("Spread vs x (s-l applied bivariately):\nis the noise level constant?", fontsize=10)
fig.suptitle("The bivariate discipline: fit robustly, then interrogate the residuals twice (Visualizing Data Ch.3)", fontsize=12)
fig.tight_layout()
finish(fig, "v3_bivariate.png")

keypoints("Visualizing Data Ch.3 — Bivariate Data", [
  "Loess span and robustness iterations are the two authored parameters of every smooth.",
  "Bisquare robustness lets the bulk speak when outliers shout.",
  "A fit is checked by TWO residual plots: dependence (any x-structure left?) and spread (is variance constant?).",
  "'The curve through the points' is a model — Cleveland just makes you look at its failures.",
])
