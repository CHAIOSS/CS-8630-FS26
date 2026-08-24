"""ELEMENTS OF GRAPHING DATA — Ch. 2, Principles of Graph Construction
Key points demonstrated: make the data stand out; scale breaks done
honestly; log scales for percent change; banking to 45 degrees.
Run: python elements_ch2_principles.py [--save DIR]"""
from _cleveland import *

rng = np.random.default_rng(2)
t = np.arange(1980, 2005)
y = 60 + 0.9*(t-1980) + 3*np.sin((t-1980)/3) + rng.normal(0, 1.2, len(t))

# Fig A: make the data stand out
fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
ax = axes[0]
ax.plot(t, y, "s-", color="green", lw=1, ms=7, mec="red", mfc="yellow")
ax.grid(True, which="both", color="red", lw=0.8, alpha=.7)
ax.set_facecolor("#FFFFCC")
for s in ax.spines.values(): s.set_visible(True); s.set_linewidth(2)
ax.set_title("Superfluity: the apparatus outshouts the data", fontsize=10)
ax = axes[1]
ax.plot(t, y, "o-", color=INK, lw=1.6, ms=4)
ax.set_title("Data stand out: quiet scales, prominent marks", fontsize=10)
fig.suptitle("Principle 1 — make the data stand out; avoid superfluity (Elements Ch.2)", fontsize=12)
fig.tight_layout()
finish(fig, "e2_standout.png")

# Fig B: scale breaks — full scale vs FULL break vs sneaky truncation
fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.4))
vals = np.array([742, 748, 745, 751, 756, 761])
yrs = np.arange(2019, 2025)
axes[0].bar(yrs, vals, color=INK); axes[0].set_ylim(0, 800)
axes[0].set_title("Full scale: honest, low resolution", fontsize=10)
axes[1].plot(yrs, vals, "o-", color=INK)
axes[1].set_ylim(735, 765)
axes[1].set_title("Cleveland's rule: a break must be FULL —\nline chart, break marked, no bars", fontsize=10)
axes[1].annotate("scale does not start at zero", xy=(2019, 736.2), fontsize=8, color=ACCENT)
axes[2].bar(yrs, vals, color=ACCENT); axes[2].set_ylim(735, 765)
axes[2].set_title("The crime: truncated BARS —\nlength now lies (see Ch.4 & Unit 10)", fontsize=10)
fig.suptitle("Principle 2 — scale breaks: use them fully and honestly, never with length encodings", fontsize=12)
fig.tight_layout()
finish(fig, "e2_breaks.png")

# Fig C: log scale for percent change
t2 = np.arange(0, 25)
small = 10 * 1.12**t2; big = 1000 * 1.12**t2
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.4))
for s_, b_, ax, ttl in [(small, big, axes[0], "Linear scale: 'the big one is exploding'"),
                         (small, big, axes[1], "Log scale: equal % growth = parallel lines")]:
    ax.plot(t2, s_, "-", color=TEAL, lw=2, label="series A")
    ax.plot(t2, b_, "-", color=INK, lw=2, label="series B")
    ax.set_title(ttl, fontsize=10); ax.legend(fontsize=8)
axes[1].set_yscale("log")
fig.suptitle("Principle 3 — when percent change is the question, the log scale answers it", fontsize=12)
fig.tight_layout()
finish(fig, "e2_log.png")

# Fig D: banking to 45
t3 = np.linspace(0, 30, 400)
series = np.sin(t3) * (1 + t3/18) + t3/9
fig = plt.figure(figsize=(11, 4.2))
ax1 = fig.add_axes([0.07, 0.62, 0.88, 0.33])
ax2 = fig.add_axes([0.07, 0.12, 0.35, 0.38])
ax1.plot(t3, series, color=INK, lw=1.4)
ax1.set_title("Banked toward 45°: rate-of-change differences are legible", fontsize=10)
ax2.plot(t3, series, color=INK, lw=1.4)
ax2.set_title("Square aspect: slopes crowd\nthe vertical — judgment degrades", fontsize=10)
for ax in (ax1, ax2): ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("Principle 4 — aspect ratio is a parameter: bank average |slope| toward 45° (Elements Ch.2)", fontsize=12)
finish(fig, "e2_banking.png")

keypoints("Elements Ch.2 — Principles of Graph Construction", [
  "Make the data stand out; every non-data mark competes with the data.",
  "Scale breaks: full breaks, clearly marked, never with bars or any length encoding.",
  "Choose the log scale when percent change is the quantity of interest.",
  "Aspect ratio is not neutral: bank to 45° so slope comparisons live where perception is best.",
])
