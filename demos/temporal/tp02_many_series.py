"""MANY SERIES — superpose, multiply, then build a horizon chart band by band.
Run: python tp02_many_series.py [--save DIR]"""
from _t import *

def superposed():
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    for i, (r, v) in enumerate(SERIES.items()):
        ax.plot(t, v, lw=1.1, color=list(PAL4.values())[i % 4])
    ax.set_xticks([]); ax.set_yticks([]); fig.tight_layout(); return fig

def multiples():
    fig, axes = plt.subplots(2, 4, figsize=(7.2, 3.6), sharey=True)
    for ax, (r, v) in zip(axes.flat, SERIES.items()):
        ax.plot(t, v, lw=0.9, color=INK); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(r, fontsize=8)
    fig.tight_layout(); return fig

H = 14
def horizon_build(step, series_n=1):
    """step: 0=area, 1=bands drawn, 2=collapsed; series_n: how many series stacked"""
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    items = list(SERIES.items())[:series_n]
    for i, (r, v) in enumerate(items):
        y0 = i
        if step == 0:
            ax.fill_between(t, y0, y0 + v / v.max() * 2.6, color=ACCENT, alpha=.5, lw=0)
        elif step == 1:
            ax.fill_between(t, y0, y0 + v / v.max() * 2.6, color=ACCENT, alpha=.35, lw=0)
            for bnd in range(1, 3):
                ax.axhline(y0 + bnd * 2.6 / 3, color=INK, lw=0.8, linestyle="--")
        else:
            for bnd in range(3):
                band = np.clip(v - bnd * H, 0, H) / H * 0.92
                ax.fill_between(t, y0, y0 + band, color=ACCENT, alpha=0.28 + 0.3 * bnd, lw=0)
        ax.text(-0.6, y0 + 0.45, r, fontsize=7, ha="right", va="center")
    ax.set_xlim(-4, 36); ax.set_ylim(0, max(1.05, series_n * 1.02) if step == 2 else 3.0)
    ax.set_xticks([]); ax.set_yticks([]); fig.tight_layout(); return fig

b = Builder("Eight series in the space of one: the horizon chart, assembled", "tp02")
b.add("plot all eight, superposed", superposed(),
      "Spaghetti: past the comparison budget by month three.", "tp02_super.png")
b.add("facet \u2192 small multiples", multiples(),
      "Aligned and comparable \u2014 and each series is now a whisper.", "tp02_facets.png")
b.add("take ONE series as an area chart", horizon_build(0),
      "Height is what we're about to spend.", "tp02_area.png")
b.add("slice its y-range into three bands", horizon_build(1),
      "Each band one 'story' of the building.", "tp02_bands.png")
b.branch("collapse the stories: darker = higher band", horizon_build(2),
      "Peak that needed 3\u00d7 height now needs 1\u00d7. Position ran out; VALUE (Bertin's ordered channel) takes over.", "tp02_collapse.png")
b.add("apply to all eight", horizon_build(2, 8),
      "Full per-series detail, one-eighth the space. Heer, Kong & Agrawala measured how far this "
      "shrinking goes before estimation degrades \u2014 farther than you'd guess.", "tp02_horizon.png")
b.end("Three spendings of vertical space: attention (superpose), area (multiples), or ink darkness (horizon). "
      "The task decides; 'when was each repo busy?' loves the horizon.")
