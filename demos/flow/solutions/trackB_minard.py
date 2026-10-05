"""WORKED SOLUTION — Track B: Minard, Modernized.  (INSTRUCTOR CALIBRATION — do not post)
Process: a cohort of 240 first-time contributors moving through a project, one year.
Second variable along the path (Minard's temperature): median review latency (hours).
STATIC BY RULE. Run: python trackB_minard.py
"""
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _fl import INK, ACCENT, TEAL

# (x, y, cohort_remaining, median_review_hours) along each branch
TRUNK = [(0.5, 3.0, 240, 6), (2.3, 3.0, 240, 8), (4.0, 3.0, 205, 14)]       # arrive -> first PR
CORE  = [(4.0, 3.0, 150, 14), (6.1, 3.9, 112, 20), (8.3, 4.3, 96, 26), (10.2, 4.4, 88, 24)]
DOCS  = [(4.0, 3.0, 55, 14), (6.1, 2.0, 41, 7), (8.3, 1.5, 33, 5), (10.2, 1.4, 31, 5)]
CROSS = [(8.3, 1.5, 9, 5), (9.3, 2.9, 9, 18), (10.2, 4.1, 7, 24)]           # docs -> core late

def lat_color(h):  # second variable: latency -> value ramp (dark = slow)
    t = np.clip((h - 4) / 24, 0, 1)
    return (0.16 + 0.0 * t, 0.23 - 0.1 * t, 0.26 - 0.15 * t, 0.45 + 0.5 * t)

def band(ax, pts, scale=0.0048):
    for (x1, y1, n1, h1), (x2, y2, n2, h2) in zip(pts[:-1], pts[1:]):
        w1, w2 = n1 * scale, n2 * scale
        dx, dy = x2 - x1, y2 - y1; L = np.hypot(dx, dy) + 1e-9
        nx, ny = -dy / L, dx / L
        ax.add_patch(plt.Polygon([(x1 + nx * w1, y1 + ny * w1), (x2 + nx * w2, y2 + ny * w2),
                                  (x2 - nx * w2, y2 - ny * w2), (x1 - nx * w1, y1 - ny * w1)],
                                 closed=True, color=lat_color((h1 + h2) / 2), lw=0))

fig, ax = plt.subplots(figsize=(10.5, 5.2))
for pts in (TRUNK, CORE, DOCS, CROSS): band(ax, pts)
for x, y, n, _ in [TRUNK[0], CORE[-1], DOCS[-1], CROSS[-1], TRUNK[2]]:
    ax.text(x, y + n * 0.0048 + 0.22, f"{n}", fontsize=9, ha="center", color=INK)
for xy, s in [((0.5, 2.2), "cohort arrives\n(Jan, n=240)"), ((10.2, 5.1), "still active in core"),
              ((10.2, 0.7), "still active in docs"), ((4.0, 4.1), "35 never land a PR \u2192 exit")]:
    ax.text(*xy, s, fontsize=8.5, color="#64707A", ha="center")
# the second variable's legend, Minard-style: a latency ramp strip
for i, h in enumerate([4, 10, 16, 22, 28]):
    ax.add_patch(plt.Rectangle((0.5 + i * 0.6, 0.2), 0.55, 0.3, color=lat_color(h)))
ax.text(0.5, 0.62, "band darkness = median review latency (4h \u2192 28h)", fontsize=8, color=INK)
ax.set_xlim(0, 11.2); ax.set_ylim(0, 5.8); ax.axis("off")
ax.set_title("240 first-time contributors, one year: where they went, and how long review made them wait", fontsize=12)
ax.text(0, -0.03, "data: cohort tracking, FY2026 \u00b7 width = contributors remaining \u00b7 darkness = median review hours \u00b7 "
        "counts at branch points; exits not drawn as flows", transform=ax.transAxes, fontsize=7.5, color="#64707A")
fig.savefig("trackB_minard_modern.png", dpi=140, bbox_inches="tight")
print("Track B written. Design-note core: width carries survival; VALUE carries the second "
      "variable (latency) \u2014 the chart's argument is that the slow branch is also the one that bleeds.")
