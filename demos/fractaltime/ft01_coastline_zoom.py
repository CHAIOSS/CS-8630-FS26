"""FRACTAL TIME — the ruler argument, then the zoom that looks like itself.
Run: python ft01_coastline_zoom.py [--save DIR]"""
from _ft import *

s = fbm(2048, 0.8, 3)
def ruler(step):
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    idx = np.arange(0, 2048, step)
    ax.plot(np.arange(2048), s, lw=0.5, color="#C9D2D8")
    ax.plot(idx, s[idx], lw=1.6, color=ACCENT, marker="o", ms=2.5)
    L = np.sum(np.hypot(np.diff(idx) / 2048 * 10, np.diff(s[idx])))
    ax.set_title(f"ruler = {step} samples   measured length \u2248 {L:.1f}", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([]); fig.tight_layout(); return fig

b = Builder("How long is this time series?", "ft01")
b.add("measure with a COARSE ruler (every 256th point)", ruler(256), "", "ft01_r256.png",
      key="The 'ruler' is the sampling interval. You have already chosen one every time you said 'daily data'.")
b.branch("shrink the ruler \u00d74", ruler(64), "The length grew.", "ft01_r64.png",
      key="CONTRAST with the trail: same series, same endpoints — only the ruler changed, and the measured quantity moved.")
b.branch("shrink it \u00d78 again", ruler(8),
      "And again \u2014 lawfully. Mandelbrot's coastline, running on time.", "ft01_r8.png",
      key="Lawful growth is the tell: noise would wobble; self-similarity grows on a straight log-log line (next step).")
def loglog():
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    steps = np.array([512, 256, 128, 64, 32, 16, 8, 4]); Ls = []
    for st in steps:
        idx = np.arange(0, 2048, st)
        Ls.append(np.sum(np.hypot(np.diff(idx) / 2048 * 10, np.diff(s[idx]))))
    ax.loglog(10 / steps, Ls, "o-", color=INK, ms=4)
    ax.set_xlabel("1 / ruler"); ax.set_ylabel("measured length")
    fig.tight_layout(); return fig
b.add("plot length vs ruler, log-log", loglog(),
      "A straight line: no true length exists \u2014 only a DIMENSION (the slope).", "ft01_loglog.png",
      key="When a measurement depends on the ruler, report the EXPONENT, not the measurement. That swap is the fractal move.")
def zoom():
    s8 = fbm(4096, 0.8, 9)
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.plot(np.linspace(0, 1, 4096), s8, lw=0.7, color=INK)
    z = (s8[1024:1536] - s8[1024:1536].mean()) / s8[1024:1536].std()
    ax.plot(np.linspace(0, 1, 512), z + 2.6, lw=0.7, color=ACCENT)
    import matplotlib.patches as mp
    ax.add_patch(mp.Rectangle((0.25, s8.min()), 0.125, s8.max() - s8.min(), fill=False, ec=ACCENT, lw=1.2))
    ax.set_xticks([]); ax.set_yticks([]); fig.tight_layout(); return fig
b.add("zoom \u00d78 into the box; rescale; overlay", zoom(),
      "Parent and child are statistically the same animal: self-affinity. Any single-window chart "
      "of this object is one arbitrary face of it.", "ft01_zoom.png",
      key="If zoom ×8 is indistinguishable from the whole, a single-window chart is one arbitrary face of the object — the multiscale ladder is the honest display.")
b.end("When length depends on the ruler, 'daily data' is a ruler choice \u2014 and the multiscale "
      "ladder (deck 2.5) is the honest display.")
