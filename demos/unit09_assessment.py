"""CS 8630 Unit 9 demo — the chart-crime gallery, generated live.
Renders four classic deceptions from the SAME honest series; each panel
names its technique. Doubles as construction reference for the Week 11 lab.
Run: python unit09_assessment.py [--save DIR]"""
from _style import *

q = np.array([102, 104, 103, 107, 105, 109, 108, 112])
labels = [f"Q{i+1}" for i in range(8)]

fig, axes = plt.subplots(2, 2, figsize=(11, 6.4))
# honest reference
axes[0, 0].bar(labels, q, color=INK)
axes[0, 0].set_ylim(0, 120); axes[0, 0].set_title("HONEST: zero baseline — the reference", fontsize=10)
# crime 1: truncation
axes[0, 1].bar(labels, q, color=ACCENT)
axes[0, 1].set_ylim(100, 113)
axes[0, 1].set_title("TRUNCATED AXIS: 'a surge' — bar length now lies", fontsize=10)
# crime 2: cherry-picked window
axes[1, 0].plot(labels[3:6], q[3:6], "o-", color=ACCENT, lw=2.5)
axes[1, 0].set_ylim(104, 110)
axes[1, 0].set_title("WINDOW + ZOOM: Q4–Q6, tight axis — 'wild swings!'", fontsize=10)
# crime 3: rebase to 'growth since Q1', then radius <- growth (area ~ growth^2)
growth = q - q[0] + 1                          # 1,3,2,6,4,8,7,11
for i, g in enumerate(growth):
    axes[1, 1].add_patch(plt.Circle((i * 2.6, 0), g * 0.11, color=ACCENT, alpha=.85))
    axes[1, 1].text(i * 2.6, -1.75, labels[i], ha="center", fontsize=8, color=MUTED)
axes[1, 1].set_xlim(-1.5, 20); axes[1, 1].set_ylim(-2.2, 2.2)
axes[1, 1].set_aspect(1); axes[1, 1].axis("off")
axes[1, 1].set_title("REBASE + AREA: 'growth since Q1' as radius \u2014 a 10% rise becomes 120x the ink", fontsize=10)
fig.suptitle("Four postures, one series (102→112). Friday you build one of these — well.", fontsize=12)
fig.tight_layout()
finish(fig, "unit09_gallery.png")
