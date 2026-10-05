"""SPECTRUM LAB — the cascade test on event-count data + fit discipline.
Run: python ft05_spectrum_lab.py [--save DIR]"""
from _ft import *

r = np.random.default_rng(5)
gB = (r.pareto(1.3, 60000) + 1) * 0.05
tsB = np.cumsum(gB); tsB = tsB[tsB < 2048]
gP = r.exponential(2048 / len(tsB), 60000)
tsP = np.cumsum(gP); tsP = tsP[tsP < 2048]

def counts(ts, width):
    bins = int(2048 / width)
    c, _ = np.histogram(ts, bins=bins)
    return c

def spec_fig(width, shuffled=False):
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    for ts, col, lab in [(tsP, MUTED, "Poisson"), (tsB, ACCENT, "bursty")]:
        c = counts(ts, width).astype(float)
        if shuffled and col == ACCENT:
            r.shuffle(c); lab = "bursty, SHUFFLED"
        F = np.abs(np.fft.rfft(c - c.mean())) ** 2
        f = np.fft.rfftfreq(len(c), 1.0)
        fb = np.logspace(np.log10(f[1]), np.log10(f[-1]), 24)
        idx = np.digitize(f[1:], fb)
        fm = [f[1:][idx == i].mean() for i in range(1, 24) if (idx == i).any()]
        Fm = [F[1:][idx == i].mean() for i in range(1, 24) if (idx == i).any()]
        ax.loglog(fm, Fm, "o-", ms=3, lw=1.4, color=col, label=lab)
    ax.legend(fontsize=8)
    ax.set_title(f"bin width = {width} (the ruler, again)", fontsize=10)
    return fig

b = Builder("Is there memory across scales? Ask the spectrum.", "ft05")
b.add("spectrum(counts, bin=1)", spec_fig(1),
      "Poisson: flat (white). Bursty: rising low-frequency power \u2014 long waves carry the "
      "energy. The 1/f family, on plain event data.", "ft05_w1.png",
      key="CONTRAST the two curves: Poisson flat (no memory), bursty tilted (long waves carry the power). The tilt IS memory across scales.")
b.branch("bin width = 8   # coarser ruler", spec_fig(8),
      "The tilt survives rebinning \u2014 scale-crossing structure should. (A 'pattern' that "
      "dies when the ruler changes was the ruler.)", "ft05_w8.png",
      key="Robustness check #1: real cross-scale structure survives rebinning. A pattern that needs one particular bin width was an artifact.")
b.add("SHUFFLE the bursty counts, respectrum", spec_fig(8, shuffled=True),
      "Shuffling kills the tilt: the structure was temporal, not distributional. The cheapest "
      "null check in this module \u2014 one line, and no AI tool volunteers it.", "ft05_shuf.png",
      key="Robustness check #2 (the shuffle null): destroy order, keep values. Structure that survives was distributional; structure that dies was TEMPORAL — exactly what you were claiming.")
b.end("Report: slope, FIT RANGE, binning, and the shuffle check. 'Looks 1/f-ish' is a mood; "
      "this canvas is the measurement.")
