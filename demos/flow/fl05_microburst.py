"""MESSAGE STUDY — the microburst: plan view vs the vertical section.
Run: python fl05_microburst.py [--save DIR]"""
from _fl import *

def mb(x, z, k=1.0):
    u = k * 2.2 * (x - 5) / (1 + ((x - 5) / 1.4) ** 2) * np.exp(-z / 1.2) * (1 / (1 + z))
    w = -k * 2.6 * np.exp(-((x - 5) / 1.1) ** 2) * (z / (0.4 + z)) \
        + k * 0.55 * np.exp(-z / 0.8) * np.exp(-((np.abs(x - 5) - 2.4) / 0.9) ** 2)
    return u, w

def plan():
    fig, ax = frame((6.8, 4.0))
    th = np.linspace(0, 2 * np.pi, 24)
    for r_ in np.linspace(0.3, 3.0, 7):
        ax.quiver(5 + r_ * np.cos(th), 3.2 + r_ * np.sin(th) * 0.64,
                  np.cos(th) * (2.0 / (0.5 + r_)), np.sin(th) * 0.64 * (2.0 / (0.5 + r_)),
                  color=INK, scale=16, width=0.004)
    ax.add_patch(plt.Circle((5, 3.2), 0.25, color=ACCENT))
    return fig

def section(k=1.0):
    Xs, Zs = np.meshgrid(np.linspace(0.5, 9.5, 46), np.linspace(0.05, 3.2, 26))
    Us, Ws = mb(Xs, Zs, k)
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.streamplot(Xs, Zs, Us, Ws, color=np.hypot(Us, Ws), cmap="inferno", density=1.4, linewidth=1.1, arrowsize=0.8)
    ax.axhline(0.07, color=INK, lw=3)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_ylabel("altitude")
    if k > 1: ax.set_title(f"intensity \u00d7{k:.0f}: the gust-front curl tightens", fontsize=9, color=MUTED)
    return fig

b = Builder("A 3D event: which cutting plane tells the truth?", "fl05")
b.add("PLAN VIEW (from above): quiver(outflow)", plan(),
      "A starburst \u2014 reads as a benign source. The vertical story is invisible from here.", "fl05_plan.png",
      key="The default view (top-down, because maps are top-down) can make a killer look like a fountain. Defaults are choices nobody defended.")
b.add("VERTICAL SECTION: streamplot(x, z)", section(),
      "Descent core, ground splash, rolled-up gust front \u2014 the actual hazard, visible only "
      "in this plane. The SECTION is a choice, and the choice is the message.", "fl05_section.png",
      key="CONTRAST: same event, orthogonal cut — the hazard appears. When a phenomenon has a vertical dimension, the cutting plane carries the claim.")
b.branch("intensity \u00d72", section(2.0),
      "Pilot-training framing: wind-shear escape charts are exactly this section, scaled by threat.", "fl05_intense.png",
      key="Aviation standardized on the section BECAUSE lives depended on reading descent+outflow together — task decided the plane, not convention.")
b.end("When a phenomenon has a vertical dimension, 'top-down because maps are top-down' is a "
      "default masquerading as a decision. Bach: both panels are cuts; choosing the cut is the operation.",
      key="AUDIT QUESTION for any spatial chart: which plane am I NOT seeing, and what lives there?")
