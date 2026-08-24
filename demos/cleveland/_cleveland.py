"""Shared helpers for the Cleveland chapter demos."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _style import *          # INK, ACCENT, TEAL, MUTED, TINT, finish, plt, np
from statsmodels.nonparametric.smoothers_lowess import lowess

def loess(x, y, frac=0.5, it=3):
    """Cleveland's own smoother (he invented it). Returns xs, ys sorted."""
    out = lowess(y, x, frac=frac, it=it, return_sorted=True)
    return out[:, 0], out[:, 1]

def keypoints(title, points):
    print(f"\n=== {title} ===")
    for p in points:
        print("  •", p)
