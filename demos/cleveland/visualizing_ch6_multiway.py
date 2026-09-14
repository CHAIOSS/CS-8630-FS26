"""VISUALIZING DATA — Ch. 6, Multiway Data
Key tool: the multiway dot plot, panels and levels ORDERED BY MEDIAN —
and the payoff: anomalies pop (an homage to Cleveland's barley finding).
Run: python visualizing_ch6_multiway.py [--save DIR]Run with --reveal to highlight the anomalous site after the class hunts.
"""
import sys
from _cleveland import *

rng = np.random.default_rng(66)
sites = ["Crookston", "Duluth", "Grand Rapids", "Morris", "University Farm", "Waseca"]
varieties = [f"var-{c}" for c in "ABCDEFGH"]
site_eff = dict(zip(sites, [4, 1, 2, 3, 5, 7]))
var_eff = dict(zip(varieties, np.linspace(0, 3.5, len(varieties))))
data = {}
for s in sites:
    y1 = {v: 22 + site_eff[s] + var_eff[v] + rng.normal(0, .7) for v in varieties}
    y2 = {v: y1[v] - 2.2 + rng.normal(0, .7) for v in varieties}      # year 2 lower everywhere...
    if s == "Morris":
        y1, y2 = y2, y1                                                # ...except Morris: swapped (the anomaly)
    data[s] = (y1, y2)

order_sites = sorted(sites, key=lambda s: np.median(list(data[s][0].values())))
order_vars = sorted(varieties, key=lambda v: np.median([data[s][0][v] for s in sites]))

fig, axes = plt.subplots(1, len(order_sites), figsize=(13, 4.6), sharey=True, sharex=True)
for ax, s in zip(axes, order_sites):
    y1, y2 = data[s]
    ax.plot([y1[v] for v in order_vars], order_vars, "o", color=INK, ms=5, label="year 1")
    ax.plot([y2[v] for v in order_vars], order_vars, "o", color=ACCENT, ms=5, label="year 2")
    ax.grid(axis="y", color="#E9EDEF", lw=1)
    reveal = "--reveal" in sys.argv
    ax.set_title(s, fontsize=9, color=ACCENT if (reveal and s == "Morris") else INK,
                 fontweight="bold" if (reveal and s == "Morris") else "normal")
axes[0].legend(fontsize=8, loc="lower right")
fig.suptitle("Multiway dot plot, median-ordered: one site's years are swapped — see it? (Cleveland's barley move, Ch.6)",
             fontsize=12)
fig.tight_layout()
finish(fig, "v6_multiway_reveal.png" if "--reveal" in sys.argv else "v6_multiway.png")

keypoints("Visualizing Data Ch.6 — Multiway Data", [
  "Multiway dot plots: a panel per level, position encoding throughout, common scales everywhere.",
  "ORDER BY MEDIAN, never alphabetically — ordering is what makes the structure and the anomaly visible.",
  "Cleveland's barley analysis found a probable year-swap that 60 years of modeling missed: graphs audit data.",
  "This chapter is the course's origin story for 'visualization as quality control' — and your project's data memo.",
])
