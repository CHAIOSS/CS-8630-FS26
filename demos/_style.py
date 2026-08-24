"""Shared style for CS 8630 demos. Import: from _style import *"""
import sys, os
import matplotlib
if "--save" in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

INK, ACCENT, TEAL, MUTED, TINT = "#2B3A42", "#E4572E", "#1C7293", "#64707A", "#F0F3F5"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": "white"})

def finish(fig, name):
    """Show interactively, or save when called with --save [dir]."""
    if "--save" in sys.argv:
        i = sys.argv.index("--save")
        outdir = sys.argv[i + 1] if len(sys.argv) > i + 1 else "."
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, name)
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print("saved", path)
    else:
        plt.show()
