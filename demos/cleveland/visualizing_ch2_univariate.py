"""VISUALIZING DATA — Ch. 2, Univariate Data
Key tools: the quantile plot, two-sample q-q plot, normal q-q plot,
and the spread-location (s-l) plot.
Run: python visualizing_ch2_univariate.py [--save DIR]"""
from _cleveland import *

rng = np.random.default_rng(22)
a = rng.gamma(3, 2.2, 180)              # skewed group A
b = rng.gamma(3, 2.2, 150) * 1.35 + 1   # shifted + scaled group B

# Fig A: quantile plot + two-sample q-q
fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.7))
f = (np.arange(1, len(a)+1) - 0.5) / len(a)
axes[0].plot(f, np.sort(a), "o", ms=3, color=INK)
axes[0].set_xlabel("f-value"); axes[0].set_ylabel("value")
axes[0].set_title("Quantile plot: the whole distribution,\nevery point visible — no bins to author", fontsize=10)
q = np.linspace(.02, .98, 60)
axes[1].plot(np.quantile(a, q), np.quantile(b, q), "o", ms=4, color=ACCENT)
lims=[0, max(a.max(), b.max())]
axes[1].plot(lims, lims, ls="--", color=MUTED)
axes[1].set_xlabel("A quantiles"); axes[1].set_ylabel("B quantiles")
axes[1].set_title("Two-sample q-q: off the line = groups differ;\nline-parallel offset = additive shift;\nslope ≠ 1 = multiplicative", fontsize=9.5)
from scipy import stats
osm, osr = stats.probplot(a, dist="norm")[0]
axes[2].plot(osm, osr, "o", ms=3, color=TEAL)
axes[2].plot(osm, osm*np.std(a)+np.mean(a), ls="--", color=MUTED)
axes[2].set_title("Normal q-q: the upward bow IS the skew —\nread the shape, not a p-value", fontsize=10)
axes[2].set_xlabel("normal quantiles")
fig.suptitle("Quantiles are the univariate workhorse (Visualizing Data Ch.2)", fontsize=12)
fig.tight_layout()
finish(fig, "v2_quantiles.png")

# Fig B: spread-location plot
groups = {g: rng.gamma(3, s, 140) for g, s in zip("ABCD", [1.5, 2.2, 3.1, 4.0])}
fig, ax = plt.subplots(figsize=(8.5, 3.8))
meds, spreads = [], []
for i, (g, v) in enumerate(groups.items()):
    med = np.median(v); res = np.sqrt(np.abs(v - med))
    ax.scatter(np.full_like(v, med), res, s=8, alpha=.35, color=INK)
    meds.append(med); spreads.append(res.mean())
ax.plot(meds, spreads, "o-", color=ACCENT, lw=2, ms=8)
ax.set_xlabel("group median (location)"); ax.set_ylabel("√|residual| (spread)")
ax.set_title("Spread-location plot: spread grows with level → a log/power transform is indicated (Ch.2)")
fig.tight_layout()
finish(fig, "v2_sl.png")

keypoints("Visualizing Data Ch.2 — Univariate Data", [
  "Quantile plots show every observation; histograms author bins (Unit 2's lesson, pre-taught by Cleveland).",
  "Two-sample q-q reads the KIND of difference: additive shift vs multiplicative scale, at a glance.",
  "Normal q-q: distribution shape as geometry — bows are skew, S-curves are tails.",
  "Spread-location: when spread tracks level, transform before you compare.",
])
