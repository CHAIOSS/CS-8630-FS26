"""WORKED SOLUTION — Track A: The Weather Map of Work.  (INSTRUCTOR CALIBRATION — do not post)
System rendered: 'contribution weather' over a 2D map of a project's areas.
Claim carried: "Review attention is a jet: it runs the core\u2192release corridor and starves docs."
Run: python trackA_weather_map.py           (writes static + 36 frames + disclosure baked in)
"""
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _fl import INK, ACCENT

# 1) THE FIELD: attention flow over a semantic map (x = subsystem axis, y = stack depth).
#    Built from data: per-area review counts -> potential; flow = gradient descent toward attention.
areas = {"docs": (1.5, 5.2, 14), "cli": (2.2, 1.4, 22), "api": (5.0, 3.1, 160),
         "core": (7.4, 3.4, 240), "release": (9.0, 3.2, 90)}   # (x, y, reviews/week)
def field(x, y, t=0.0):
    u = np.zeros_like(x, float); v = np.zeros_like(y, float)
    for (ax_, ay, w) in areas.values():
        dx, dy = ax_ - x, ay - y; r2 = dx * dx + dy * dy + 0.6
        u += 0.016 * w * dx / r2; v += 0.016 * w * dy / r2
    u += 0.35 * np.sin(0.5 * y + 1.3 * t)        # ambient churn (unsteady!)
    return u, v

X, Y = np.meshgrid(np.linspace(0, 10.5, 40), np.linspace(0, 6.4, 26))
U, V = field(X, Y); S = np.hypot(U, V)

# 2) STATIC STRUCTURAL VIEW
fig, ax = plt.subplots(figsize=(9, 5.4))
ax.streamplot(X, Y, U, V, color=S, cmap="viridis", density=1.4, linewidth=1.1)
for name, (ax_, ay, w) in areas.items():
    ax.scatter([ax_], [ay], s=40 + w, color=INK, zorder=3)
    ax.text(ax_, ay + 0.42, name, ha="center", fontsize=10, color=INK)
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("review attention as a flow field \u00b7 week of 2026-09-21", fontsize=11)
# 3) THE DISCLOSURE LINE, IN THE FIGURE (non-negotiable)
ax.text(0.01, -0.06, "field: gradient of review-count potential, 5 areas, week agg \u00b7 "
        "snapshot t=0 of an UNSTEADY ambient term \u00b7 streamplot density 1.4 \u00b7 seed n/a (deterministic)",
        transform=ax.transAxes, fontsize=7.5, color="#64707A")
fig.savefig("trackA_static.png", dpi=140, bbox_inches="tight"); plt.close(fig)

# 4) PARTICLE LAYER \u2192 FRAMES (screen-record these playing, or ffmpeg them)
rng = np.random.default_rng(2)
px, py = rng.uniform(0, 10.5, 700), rng.uniform(0, 6.4, 700)
hist = [(px.copy(), py.copy())]
for k in range(120):
    u1, v1 = field(px, py, 0.05 * k)
    px = (px + 0.06 * u1) % 10.5; py = np.clip(py + 0.06 * v1, 0, 6.4)
    hist.append((px.copy(), py.copy()))
os.makedirs("trackA_frames", exist_ok=True)
for f_i, k in enumerate(range(12, 120, 3)):
    fig, ax = plt.subplots(figsize=(9, 5.4)); ax.set_facecolor("#101820")
    for i in range(0, 700, 2):
        xs = [hist[j][0][i] for j in range(k - 9, k)]
        ys = [hist[j][1][i] for j in range(k - 9, k)]
        if max(xs) - min(xs) < 3:
            ax.plot(xs, ys, lw=0.6, color="#CFE8F3", alpha=0.75)
    for name, (ax_, ay, w) in areas.items():
        ax.text(ax_, ay, name, ha="center", fontsize=9, color="#E4572E")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 10.5); ax.set_ylim(0, 6.4)
    fig.savefig(f"trackA_frames/f{f_i:03d}.png", dpi=100, bbox_inches="tight"); plt.close(fig)
print("Track A: static + frames written.")
# 5) BROADCAST SCRIPT (20s): "Here's this week's weather over the codebase. The jet you see
#    runs the api\u2013core\u2013release corridor \u2014 that's where review attention flows and pools.
#    Notice the calm over docs: nothing is carrying attention there. One claim: our attention
#    is a jet, and docs sits outside it. [point] That's the message; the methodology line is
#    at the bottom of the chart."
# 6) WHAT THE MOTION BOUGHT (design-note answer): the static shows the corridor's STRUCTURE;
#    the particles show it's a CURRENT \u2014 persistent transport, not a momentary gradient.
#    If the write-up can't say that sentence, ship the static alone.
