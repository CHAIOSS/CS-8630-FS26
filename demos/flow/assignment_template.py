"""ASSIGNMENT TEMPLATE — Make the Invisible Move (all four tracks).
Delete the tracks you aren't doing. Data: ./data/ (regenerate: python make_data.py).
Every TODO is a MESSAGE decision wearing a technical costume."""
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

# ---------- TRACK A · Weather Map of Work ----------
# wind = pd.read_csv("data/wind_grid.csv")            # or YOUR field: any (x,y,u,v)
# X = wind.pivot_table(index="y", columns="x", values="u").columns.values  # etc.
# TODO: streamplot background (structure) + particle layer (now) — see fl01/fl03 for both.
# TODO: the disclosure line, IN the figure: source · instant/window · steady? · particle params.
# TODO: 20-second screen capture narrating ONE claim. The claim comes first; tune the render to it.

# ---------- TRACK B · Minard, Modernized ----------
# TODO: your process as (path points, widths) per branch; width = the quantity (see deck 1.6 band()).
# TODO: the SECOND variable along the path (colour/value/ticks). Minard carried temperature.
# TODO: no animation. If you feel the urge, that's the design failing — fix the statics.

# ---------- TRACK C · The Burst Portrait ----------
ev = pd.read_csv("data/events.csv")                   # or your own event stream
g = ev[ev.author == "a2"].hours.values                # pick an entity
gaps = np.diff(np.sort(g))
# raster:   plt.eventplot(g)
# CCDF:     sg = np.sort(gaps); plt.loglog(sg, 1 - np.arange(len(sg))/len(sg))
# zoom ladder: four windows, each the next one's highlighted strip (deck 2.5)
# Hurst (aggregated-variance): for w in [2,4,8,...]: var of w-binned counts; slope on log-log → H
# TODO: compose as ONE poster arguing ONE sentence about this entity's rhythm.

# ---------- TRACK D · The Honest Forecast Trail ----------
# No code required; the artifact is an annotated pair of screenshots + the receipt.
# TODO: licensed-claims list, tempted-claims list, and WHERE the source discloses steadiness.

# ---------- Tier-1 exercise (all tracks): The Machine's Weather Report ----------
# Give an AI tool data/wind_grid.csv (or your events) and ask it to "describe the flow/trend."
# Save the unmodified transcript. Audit: which disclosures did it volunteer? Which claims
# exceeded the license (deck 1.5 / 2.6)? 200-300 words.
