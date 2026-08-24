"""ELEMENTS OF GRAPHING DATA — Ch. 4, Graphical Perception
Key points: the elementary tasks and their accuracy ordering; the
curve-difference illusion; superposition and detection.
Run: python elements_ch4_perception.py [--save DIR]"""
from _cleveland import *

rng = np.random.default_rng(4)

# Fig A: the curve-difference illusion (the famous import/export lesson)
t = np.linspace(0, 10, 250)
lower = 2 + 0.5*t + 0.4*np.sin(t)
upper = lower + 1.6 + 0.9*np.sin(t/1.4 + 1)
fig, axes = plt.subplots(2, 1, figsize=(9, 5.2), sharex=True, height_ratios=[2, 1])
axes[0].plot(t, upper, color=INK, lw=2, label="curve B")
axes[0].plot(t, lower, color=TEAL, lw=2, label="curve A")
axes[0].fill_between(t, lower, upper, color=TINT)
axes[0].legend(fontsize=9)
axes[0].set_title("Read the gap between the curves: where is it largest?", fontsize=10)
axes[1].plot(t, upper-lower, color=ACCENT, lw=2)
axes[1].set_title("The actual vertical difference — the eye read minimum distance, not vertical distance", fontsize=10)
fig.suptitle("Perception of superposed curves: plot the difference you care about (Elements Ch.4)", fontsize=12)
fig.tight_layout()
finish(fig, "e4_curvediff.png")

# Fig B: elementary tasks side by side — judge B/D in each
vals = np.array([23, 21, 20, 19, 17]); labs = list("ABCDE")
fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.6))
axes[0].bar(labs, vals, color=[ACCENT if l in "BD" else INK for l in labs])
axes[0].set_title("Position/length on common scale", fontsize=10)
bottom = 0
axes[1].bar(["stack"], [vals[0]], color=INK)
b = vals[0]
for v, l in zip(vals[1:], labs[1:]):
    axes[1].bar(["stack"], [v], bottom=b, color=ACCENT if l in "BD" else "#8FA6B2",
                edgecolor="white", linewidth=1)
    b += v
axes[1].set_title("Stacked: same values, now LENGTH\nwithout aligned baselines — harder", fontsize=10)
axes[2].pie(vals, labels=labs, colors=[ACCENT if l in "BD" else c for l, c in zip(labs, [INK,"#4E6470","#6E8492","#8FA6B2","#C9D2D8"])])
axes[2].set_title("Pie: ANGLE — hardest of the three", fontsize=10)
fig.suptitle("One comparison (B vs D), three elementary tasks — the ordering is the chapter (Elements Ch.4)", fontsize=12)
fig.tight_layout()
finish(fig, "e4_tasks.png")

keypoints("Elements Ch.4 — Graphical Perception", [
  "Elementary tasks are ordered by measured accuracy: position > length > angle/slope > area > volume > color.",
  "Superposed curves: the eye judges minimum distance, not vertical difference — plot the difference explicitly.",
  "Design = choosing encodings so the required judgments are the accurate ones.",
  "This chapter is the empirical spine of the whole course; Assignment 1 replicates its method.",
])
