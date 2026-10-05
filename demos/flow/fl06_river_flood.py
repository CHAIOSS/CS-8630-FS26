"""MESSAGE STUDY — the river: ordinary vs flood, velocity vs depth\u00d7velocity.
Run: python fl06_river_flood.py [--save DIR]"""
from _fl import *

def river(flood, hazard_fill, notes=True):
    Xr, Yr = np.meshgrid(np.linspace(0, 10, 44), np.linspace(0, 6.4, 30))
    lo, hi = (2.4, 4.0) if not flood else (0.9, 5.5)
    c, h = (lo + hi) / 2, (hi - lo) / 2
    depth = np.clip(1 - ((Yr - c) / h) ** 2, 0, None) * (1.0 if not flood else 1.6)
    u = (3.2 if not flood else 4.4) * depth
    v = 0.25 * np.sin(1.3 * Xr) * depth * (1 if not flood else 1.6)
    fill = depth * np.hypot(u, v) if hazard_fill else np.hypot(u, v)
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.contourf(Xr, Yr, np.where(depth > 0.02, fill, np.nan), levels=12,
                cmap="YlOrRd" if hazard_fill else "Blues")
    m = depth > 0.04
    ax.streamplot(Xr, Yr, np.where(m, u, np.nan), np.where(m, v, np.nan),
                  color=INK, density=0.9, linewidth=0.8, arrowsize=0.7)
    for bk in [2.4, 4.0]:
        ax.axhline(bk, color=INK, lw=1.4, linestyle=":" if flood else "-")
    if notes and flood and not hazard_fill:
        annot(ax, (5.0, 5.0), "spill zone: SLOWER\n\u2192 looks safer", dxy=(1.8, 0.8))
        annot(ax, (5.0, 3.2), "channel: still the\n'danger' by this fill", dxy=(2.2, -1.6), color=TEAL)
    if notes and flood and hazard_fill:
        annot(ax, (5.0, 5.0), "same spill zone: now\nburning \u2014 d\u00d7v says\nyou can't stand here", dxy=(1.6, 0.6))
    ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(0, 6.4)
    ax.set_title(("FLOOD" if flood else "ordinary") + " \u00b7 fill = " +
                 ("depth \u00d7 velocity (hazard rating)" if hazard_fill else "velocity"), fontsize=9, color=MUTED)
    return fig

b = Builder("One river, two regimes \u2014 and the variable that changes sides", "fl06")
b.add("ordinary flow \u00b7 fill = velocity", river(False, False),
      "The descriptive variable works: fast thread, confined banks. Nothing to argue with yet.",
      "fl06_ord_v.png",
      key="Baseline first: in the ordinary regime, description and consequence AGREE \u2014 the fast water is also the dangerous water.")
b.add("FLOOD \u00b7 fill = velocity (same variable)", river(True, False),
      "Over the banks \u2014 and velocity now UNDERSELLS the spill zone: slower water you still can't stand in.",
      "fl06_fld_v.png",
      key="THE TRAP: the regime changed and the variable didn't. 'Slower = safer' is exactly backwards on a floodplain \u2014 the descriptive fill now MISLEADS.")
b.branch("FLOOD \u00b7 fill = depth \u00d7 velocity", river(True, True),
      "The variable switch IS the message: d\u00b7v is the flood-hazard rating (footing \u2248 0.5\u20131 m\u00b2/s; cars float beyond).",
      "fl06_fld_dv.png",
      key="CONTRAST with the last frame (see trail): same flood, opposite reading of the spill zone. One variable swap flipped the safety story \u2014 and THIS one matches the physics of drowning.")
b.add("ordinary \u00b7 fill = depth \u00d7 velocity   # for symmetry", river(False, True, notes=False),
      "The hazard lens on the calm day: danger confined to the thread. Now all four cells of the 2\u00d72 exist.",
      "fl06_ord_dv.png",
      key="DISCIPLINE: a variable switch is defensible when you show the 2\u00d72 (regime \u00d7 variable) \u2014 or at least state which cell your chart lives in.")
b.end("Descriptive asks 'how fast?'; consequential asks 'can you stand in it?'. Flood maps switched "
      "variables decades ago \u2014 your dashboards mostly haven't.",
      key="TRANSFER: what's your domain's d\u00d7v? Mean latency vs p95\u00d7error-rate; velocity vs depth\u00d7velocity \u2014 every field has a consequence variable hiding behind its descriptive one.")
