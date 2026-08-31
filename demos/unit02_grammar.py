"""CS 8630 Unit 2 demo — one dataset climbing the grammar, one component per panel.
Run: python unit02_grammar.py [--save DIR]"""
from _style import *
import pandas as pd

rng = np.random.default_rng(8630)
months = pd.date_range("2025-01-01", periods=12, freq="MS")
df = pd.DataFrame({
    "month": np.tile(months, 3),
    "repo": np.repeat(["augur", "frontend", "docs"], 12),
    "prs": np.concatenate([
        30 + 8 * np.sin(np.arange(12) / 2) + rng.normal(0, 3, 12),
        18 + np.arange(12) * 1.6 + rng.normal(0, 3, 12),
        8 + rng.normal(0, 2, 12)]).clip(1),
})
palette = {"augur": INK, "frontend": ACCENT, "docs": TEAL}

fig, axes = plt.subplots(2, 3, figsize=(13, 6.5))
steps = ["1 DATA + AESTHETICS\n(x=month, y=prs)", "2 GEOMETRY: point",
         "3 GEOMETRY: + line", "4 STATISTIC: rolling mean",
         "5 SCALE: log y", "6 FACET result (see window 2)"]
for ax, title in zip(axes.flat, steps):
    ax.set_title(title, fontsize=10, loc="left")
a = axes.flat
for repo, g in df.groupby("repo"):
    a[0].plot(g.month, g.prs, ".", color="none")           # aesthetics mapped, no geometry
    a[1].plot(g.month, g.prs, "o", ms=4, color=palette[repo])
    a[2].plot(g.month, g.prs, "o-", ms=4, lw=1.5, color=palette[repo])
    a[3].plot(g.month, g.prs.rolling(3, min_periods=1).mean(), "-", lw=2.5, color=palette[repo])
    a[4].plot(g.month, g.prs, "o-", ms=4, lw=1.5, color=palette[repo])
a[4].set_yscale("log")
a[5].axis("off")
a[5].text(.5, .5, "Each panel differs from its parent\nby exactly ONE grammar component.\n\nThat is Assignment 2's ladder.",
          ha="center", va="center", fontsize=12, color=INK)
for ax in list(a)[:5]:
    ax.tick_params(axis="x", labelrotation=45, labelsize=7)
fig.suptitle("The layered grammar, one decision at a time", fontsize=13)
fig.tight_layout()
finish(fig, "unit02_ladder.png")

# window 2: the facet step
fig2, axes2 = plt.subplots(1, 3, figsize=(12, 3.4), sharey=True)
for ax, (repo, g) in zip(axes2, df.groupby("repo")):
    ax.plot(g.month, g.prs, "o-", ms=4, lw=1.5, color=palette[repo])
    ax.set_title(f"repo = {repo}", fontsize=10)
    ax.tick_params(axis="x", labelrotation=45, labelsize=7)
fig2.suptitle("7 FACETS: same spec, small multiples — comparison by position (Unit 1)", fontsize=12)
fig2.tight_layout()
finish(fig2, "unit02_facets.png")
