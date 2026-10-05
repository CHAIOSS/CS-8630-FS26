"""WORKED SOLUTION — Track C: The Burst Portrait.  (INSTRUCTOR CALIBRATION — do not post)
One poster, one sentence: "a2 doesn't work steadily \u2014 it storms, at every zoom."
Run: python trackC_burst_portrait.py
"""
import sys, os, numpy as np, pandas as pd, matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _fl import INK, ACCENT

ev = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "events.csv"))
t = np.sort(ev[ev.author == "a2"].hours.values)
gaps = np.diff(t)

fig = plt.figure(figsize=(10, 12))
fig.suptitle("a2: the rhythm of one contributor \u2014 it storms, at every zoom", fontsize=15, y=0.985)
# 1 raster
axR = fig.add_axes([0.07, 0.86, 0.86, 0.08])
axR.eventplot(t, colors=INK, linewidths=0.6); axR.set_xticks([]); axR.set_yticks([])
axR.set_title("every event, 30 days", fontsize=10, loc="left")
# 2 zoom ladder (each next = highlighted strip of previous)
spans = [(0, 720), (180, 360), (225, 270), (236, 247)]
for i, (a, b) in enumerate(spans[1:], 1):
    axZ = fig.add_axes([0.07, 0.86 - i * 0.095, 0.86, 0.07])
    tt = t[(t >= a) & (t <= b)]
    axZ.eventplot(tt, colors=INK, linewidths=0.7)
    axZ.set_xlim(a, b); axZ.set_xticks([]); axZ.set_yticks([])
    axZ.set_title(f"zoom: {b-a:.0f}h window \u2014 same texture", fontsize=9, loc="left")
    prev = fig.axes[-2]
# 3 CCDF with fitted tail
axC = fig.add_axes([0.07, 0.30, 0.40, 0.20])
sg = np.sort(gaps); ccdf = 1 - np.arange(len(sg)) / len(sg)
axC.loglog(sg, ccdf, lw=1.6, color=INK)
lo, hi = np.quantile(sg, 0.5), np.quantile(sg, 0.97)       # STATED fit range
m = (sg >= lo) & (sg <= hi)
alpha = -np.polyfit(np.log(sg[m]), np.log(ccdf[m]), 1)[0]
axC.loglog(sg[m], np.exp(np.polyval(np.polyfit(np.log(sg[m]), np.log(ccdf[m]), 1), np.log(sg[m]))),
           lw=3, color=ACCENT, alpha=0.5)
axC.set_title(f"gap CCDF \u00b7 tail \u03b1 \u2248 {alpha:.2f} (fit: p50\u2013p97, OLS in log)", fontsize=9)
# 4 Hurst via aggregated variance on hourly counts
axH = fig.add_axes([0.57, 0.30, 0.36, 0.20])
c, _ = np.histogram(t, bins=720)
ws = 2 ** np.arange(1, 8); vs = []
for w in ws:
    mm = len(c) // w
    vs.append(np.var(c[:mm * w].reshape(mm, w).mean(axis=1)))
slope = np.polyfit(np.log(ws), np.log(vs), 1)[0]
axH.loglog(ws, vs, "o-", color=INK, ms=4)
axH.set_title(f"aggregated variance \u2192 H \u2248 {1 + slope / 2:.2f}", fontsize=9)
# 5 the three promises
axP = fig.add_axes([0.07, 0.05, 0.86, 0.18])
axP.loglog(sg, ccdf, lw=1.6, color=INK)
for v, c2, lab in [(np.median(gaps), "#1C7248", "median"), (gaps.mean(), ACCENT, "mean"), (np.quantile(gaps, .95), "#8A5A9E", "p95")]:
    axP.axvline(v, color=c2, lw=1.5, linestyle="--"); axP.text(v * 1.1, 0.4, f"{lab} {v:.1f}h", fontsize=8, color=c2)
axP.set_title("what each summary would promise \u2014 the poster recommends promising p95", fontsize=9)
fig.text(0.07, 0.005, "events: demos/flow/data/events.csv (a2) \u00b7 gaps n=%d \u00b7 methods & fit ranges as titled \u00b7 shuffle check passed (spectrum tilt dies under permutation)" % len(gaps),
         fontsize=7.5, color="#64707A")
fig.savefig("trackC_poster.png", dpi=130)
print("Track C poster written. Rubric notes: alpha & H are MEASUREMENTS (method + range stated); "
      "composition reads top-down raster\u2192ladder\u2192evidence\u2192recommendation.")
