"""FRACTAL TIME — build the -5/3 spectrum from stacked eddies.
Run: python ft03_cascade.py [--save DIR]"""
from _ft import *

def eddies(levels):
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    t = np.linspace(0, 1, 4096); s = np.zeros_like(t)
    r = np.random.default_rng(4)
    for L in range(levels):
        k = 2 ** (L + 1)
        s = s + (0.9 ** L) * np.sin(2 * np.pi * k * t + r.uniform(0, 6.28)) * (2 ** (-L * 5 / 6))
    ax.plot(t, s, lw=0.8, color=INK)
    ax.set_title(f"{levels} octave(s) of eddies", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); return fig

b = Builder("Big whorls, little whorls: a spectrum assembles", "ft03")
b.add("one big eddy", eddies(1), "A single scale: a wave.", "ft03_e1.png",
      key="Read-aloud cue (couplet line 1): 'Big whorls' — one eddy, one scale, nothing fractal yet.")
b.branch("add a smaller generation (\u00d7\u00bd size, less energy)", eddies(3), "", "ft03_e3.png",
      key="Couplet line 2: 'feed on their velocity' — each new generation inherits energy: half the size, 2^(-5/6) the amplitude.")
b.branch("\u2026and smaller, and smaller (Richardson's couplet)", eddies(8),
      "It stops looking like waves and starts looking like WEATHER \u2014 or a market, or a repo's commit log.", "ft03_e8.png",
      key="Couplet line 3: 'lesser whorls' — CONTRAST with step 1 in the trail: waves became weather purely by stacking scales.")
def spectrum():
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    k = np.logspace(0, 3, 60)
    ax.loglog(k, 8 * k ** (-5 / 3), lw=2, color=INK)
    ax.text(12, 1.0, "slope \u22125/3", fontsize=10, color=ACCENT)
    ax.set_xlabel("scale (frequency)"); ax.set_ylabel("energy")
    fig.tight_layout(); return fig
b.add("energy per scale, log-log: Kolmogorov's \u22125/3", spectrum(),
      "Power law = self-similarity = the cascade's receipt. The wind map (fl03) is this object, live.", "ft03_spec.png",
      key="Couplet line 4: 'to viscosity' — the spectrum's floor. The straight −5/3 stretch is lines 1–3; fits STOP where the rhyme stops.")
b.end("Turbulence is a fractal in motion \u2014 Part I's beauty and Part II's mathematics are one phenomenon.")
