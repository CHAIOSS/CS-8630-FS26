"""FRACTAL TIME — estimate H from one log-log line; Poisson vs bursty gaps.
Run: python ft02_hurst_bursts.py [--save DIR]"""
from _ft import *

sH = fbm(4096, 0.8, 2)
def three():
    fig, axes = plt.subplots(1, 3, figsize=(9.8, 2.8))
    for ax, H in zip(axes, [0.3, 0.5, 0.8]):
        ax.plot(fbm(1200, H, 5), lw=0.7, color=INK)
        ax.set_title(f"H = {H}", fontsize=10); ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); return fig

def varplot():
    inc = np.diff(sH)
    ws = 2 ** np.arange(1, 9); vs = []
    for w in ws:
        m = len(inc) // w
        vs.append(np.var(inc[:m * w].reshape(m, w).mean(axis=1)))
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.loglog(ws, vs, "o-", color=INK, ms=4)
    slope = np.polyfit(np.log(ws), np.log(vs), 1)[0]
    ax.set_title(f"aggregated variance vs window \u2014 slope {slope:.2f} \u2192 H \u2248 {1 + slope / 2:.2f}", fontsize=10)
    ax.set_xlabel("window w"); ax.set_ylabel("var of w-means")
    fig.tight_layout(); return fig

def rasters():
    r = np.random.default_rng(1)
    gP = r.exponential(1.0, 400); gB = (r.pareto(1.3, 400) + 1) * 0.12
    tP = np.cumsum(gP); tP = tP / tP[-1] * 100
    tB = np.cumsum(gB); tB = tB / tB[-1] * 100
    fig, axes = plt.subplots(2, 1, figsize=(7.4, 3.0))
    axes[0].eventplot(tP, colors=INK, linewidths=0.7); axes[0].set_title("Poisson: pure chance", fontsize=9)
    axes[1].eventplot(tB, colors=ACCENT, linewidths=0.7); axes[1].set_title("heavy-tailed gaps: storms and silences", fontsize=9)
    for ax in axes: ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); return fig, gP, gB

def ccdf(gP, gB):
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    for g, c, lab in [(gP, INK, "Poisson"), (gB, ACCENT, "bursty")]:
        sg = np.sort(g); ax.loglog(sg, 1 - np.arange(len(sg)) / len(sg), lw=1.6, color=c, label=lab)
    ax.legend(fontsize=8); ax.set_title("gap CCDF, log-log", fontsize=10)
    fig.tight_layout(); return fig

b = Builder("Texture as a statistic: H, and the shape of waiting", "ft02")
b.add("three series, one knob (H)", three(),
      "Your eyes already read H \u2014 as roughness. Now measure it:", "ft02_three.png",
      key="CONTRAST the three panels: ONE parameter apart. Texture is a statistic your visual system computes for free — Bertin's grain, made rigorous.")
b.add("bin at widths w; var(means) vs w, log-log", varplot(),
      "One line, one slope, one number for a whole history's texture. Two repos with equal means "
      "and H 0.55 vs 0.85 are different animals.", "ft02_var.png",
      key="One log-log slope = one number for a whole history's texture. Put H next to the mean on any dashboard that compares series.")
fr, gP, gB = rasters()
b.add("same COUNT of events, two gap laws", fr, "", "ft02_rasters.png",
      key="CONTRAST top vs bottom: SAME event count. Storms-and-silences vs even-rough is a gap-distribution fact, invisible to any monthly total.")
b.add("CCDF of the gaps, log-log", ccdf(gP, gB),
      "The straight tail is the signature: once gaps go heavy-tailed, 'average rate' describes "
      "nothing anyone experiences. (Barab\u00e1si 2005: human activity \u2014 and your PR data \u2014 lives here.)", "ft02_ccdf.png",
      key="The straight log-log tail is the burstiness signature. Once you see it, retire 'average rate' and report median + p95.")
b.end("Report medians and tails for bursty things; put H next to the mean; let log-log axes be "
      "an instrument, not a style.")
