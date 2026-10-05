"""H PLAYGROUND — persistence, the zoom, and the window-story, live.
Run: python ft06_h_playground.py [--save DIR]"""
from _ft import *
import matplotlib.patches as mp

def series(H):
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.plot(fbm(1400, H, 5), lw=0.7, color=INK)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(f"H = {H}", fontsize=10)
    return fig

b = Builder("One knob, every texture: the H playground", "ft06")
b.add("fbm(H=0.3)   # anti-persistent", series(0.3),
      "Up begets down: the series gnaws at itself. Mean-reversion's texture.", "ft06_h3.png",
      key="Anti-persistence: the under-appreciated regime — thermostats, inventories, anything regulated.")
b.branch("fbm(H=0.5)   # the random walk", series(0.5),
      "Independent steps \u2014 the null everyone assumes.", "ft06_h5.png",
      key="H = 0.5 is what 'random' means in most people's heads — and in most dashboards' implicit null.")
b.branch("fbm(H=0.8)   # persistent", series(0.8),
      "Up begets up: excursions stretch into trend-shaped accidents. Where rivers, traffic, "
      "and repos live (H \u2248 0.7\u20130.9).", "ft06_h8.png",
      key="CONTRAST all three in the trail: one knob. Persistent series produce trend-SHAPED accidents — the crueler, truer null for activity data.")
def zoom():
    s8 = fbm(4096, 0.8, 9)
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ax.plot(np.linspace(0, 1, 4096), s8, lw=0.7, color=INK)
    z = (s8[1024:1536] - s8[1024:1536].mean()) / s8[1024:1536].std()
    ax.plot(np.linspace(0, 1, 512), z + 2.6, lw=0.7, color=ACCENT)
    ax.add_patch(mp.Rectangle((0.25, s8.min()), 0.125, s8.max() - s8.min(), fill=False, ec=ACCENT, lw=1.2))
    ax.set_xticks([]); ax.set_yticks([])
    return fig
b.add("zoom \u00d78 into the box; rescale; overlay", zoom(),
      "Parent and child: statistically the same animal. So a single-window chart is one "
      "arbitrary face of the object.", "ft06_zoom.png",
      key="Self-affinity in one picture: parent and rescaled child indistinguishable. Scale choice = face choice.")
def windows():
    s = fbm(1440, 0.85, 21) * 14 + 60
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.plot(s, lw=0.8, color=INK)
    for a, bnd, c in [(300, 420, "#1C7248"), (700, 820, "#B0431F"), (1050, 1170, "#8A6D1C")]:
        ax.axvspan(a, bnd, color=c, alpha=0.2)
    ax.set_xticks([]); ax.set_yticks([])
    return fig
b.add("three 'quarters' on a changeless H=0.85 process", windows(),
      "+31% / \u221224% / flat \u2014 all true, all window-authored. Invite a volunteer to pick the "
      "window that proves any headline they want.", "ft06_windows.png",
      key="LIVE EXERCISE: a volunteer names a headline; the room finds its window. Uncomfortable on purpose — then write the disclosure that fixes it.")
b.end("Persistence manufactures stories. The honest null for activity dashboards is H \u2248 0.8 "
      "noise \u2014 and most 'trends' don't beat it.")
