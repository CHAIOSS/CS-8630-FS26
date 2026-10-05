"""Shared frame for the Unit 4 demos: Builder + the multidimensional PR table."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "grammar"))
from _grammar import Builder, prs, INK, ACCENT, TEAL, MUTED, TINT
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

rng = np.random.default_rng(4)
df = prs(); _n = len(df)
df["loglines"] = np.log10(df.lines)
df["files"] = np.maximum(1, (df.lines / np.exp(rng.normal(3.6, .5, _n))).round())
df["logfiles"] = np.log10(df.files)
df["reviews"] = rng.poisson(0.6 + 1.1 * (df.loglines - df.loglines.min()), _n)
df["loghours"] = np.log10(df.hours)
DIMS = ["loglines", "logfiles", "reviews", "loghours"]
LAB = {"loglines": "size", "logfiles": "files", "reviews": "reviews", "loghours": "latency"}
PAL4 = {"augur": INK, "frontend": ACCENT, "docs": TEAL, "cli": "#8A5A9E"}
sub = df.sample(700, random_state=1)
