"""Shared frame for the temporal demos."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "grammar"))
from _grammar import Builder, prs, monthly, INK, ACCENT, TEAL, MUTED, TINT
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)
t = np.arange(36)
base = np.maximum(2, 22 + t*0.5 + 7*np.sin(2*np.pi*(t % 12)/12 + 1.2) + rng.normal(0, 1.6, 36))
PAL4 = {"augur": INK, "frontend": ACCENT, "docs": TEAL, "cli": "#8A5A9E"}
SERIES = {}
for i, r in enumerate(["augur", "frontend", "docs", "cli", "api", "infra", "ml", "web"]):
    SERIES[r] = np.maximum(1, 12 + 2.4*i + 6*np.sin(2*np.pi*(t % 12)/12 + i) + t*0.3*rng.uniform(0.4, 1.4) + rng.normal(0, 1.5, 36))

def tsplot(v, title="", color=INK, figsize=(6.6, 3.6), gaps=None, mode="line"):
    fig, ax = plt.subplots(figsize=figsize)
    vv = v.astype(float).copy()
    if gaps is not None:
        if mode == "interp":
            s = pd.Series(np.where(np.isin(t, gaps), np.nan, vv)).interpolate()
            ax.plot(t, s, lw=1.8, color=color)
        elif mode == "break":
            s = pd.Series(np.where(np.isin(t, gaps), np.nan, vv))
            ax.plot(t, s, lw=1.8, color=color)
        else:  # zero
            s = np.where(np.isin(t, gaps), 0, vv)
            ax.plot(t, s, lw=1.8, color=color)
            ax.scatter(gaps, [0]*len(gaps), s=20, color=ACCENT, zorder=3)
    else:
        ax.plot(t, vv, lw=1.8, color=color)
    ax.set_xticks([]); ax.set_yticks([])
    if title: ax.set_title(title, fontsize=10)
    fig.tight_layout()
    return fig
