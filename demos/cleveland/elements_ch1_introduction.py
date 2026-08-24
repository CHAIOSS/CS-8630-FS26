"""ELEMENTS OF GRAPHING DATA — Ch. 1, Introduction
Key point: summaries hide what graphs reveal. Four datasets, identical
statistics, four different truths — the argument for plotting, period.
Run: python elements_ch1_introduction.py [--save DIR]"""
from _cleveland import *

# Anscombe-quartet-style construction (classic values)
x1 = np.array([10,8,13,9,11,14,6,4,12,7,5]); y1 = np.array([8.04,6.95,7.58,8.81,8.33,9.96,7.24,4.26,10.84,4.82,5.68])
y2 = np.array([9.14,8.14,8.74,8.77,9.26,8.10,6.13,3.10,9.13,7.26,4.74])
y3 = np.array([7.46,6.77,12.74,7.11,7.81,8.84,6.08,5.39,8.15,6.42,5.73])
x4 = np.array([8,8,8,8,8,8,8,19,8,8,8]); y4 = np.array([6.58,5.76,7.71,8.84,8.47,7.04,5.25,12.50,5.56,7.91,6.89])

sets = [(x1,y1,"I: the linear story your stats imply"),(x1,y2,"II: a curve — the model is wrong"),
        (x1,y3,"III: one outlier owns the slope"),(x4,y4,"IV: the 'relationship' is one point")]
fig, axes = plt.subplots(1, 4, figsize=(13, 3.4), sharey=True)
for ax,(x,y,t) in zip(axes, sets):
    ax.scatter(x, y, s=40, color=INK, zorder=3)
    b, a = np.polyfit(x, y, 1)
    xs = np.array([3, 20]); ax.plot(xs, a + b*xs, color=ACCENT, lw=2)
    ax.set_title(t, fontsize=9.5); ax.set_xlim(2, 20)
fig.suptitle("Same means, same variances, same r=0.816, same regression line — plot the data (Elements Ch.1)", fontsize=12)
fig.tight_layout()
finish(fig, "e1_quartet.png")

keypoints("Elements Ch.1 — Introduction", [
  "Graphs are instruments of discovery, not decoration: structure invisible to summaries is visible to the eye.",
  "Cleveland's iterative stance: plot, notice, re-plot. A graph is a step in analysis, not its output.",
  "Every later chapter is machinery for making that noticing reliable.",
])
