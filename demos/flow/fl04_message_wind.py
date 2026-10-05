"""MESSAGE STUDY — one wind field, descriptive vs consequential.
Run: python fl04_message_wind.py [--save DIR]"""
from _fl import *
S = np.hypot(GU, GV)

def descriptive():
    fig, ax = frame((7.0, 4.2))
    ax.streamplot(GX, GY, GU, GV, color=S, cmap="viridis", density=1.3, linewidth=1.1, arrowsize=0.8)
    annot(ax, (5.0, 3.4), "everything shown,\nnothing privileged", dxy=(1.6, 1.8), color=INK)
    return fig

def consequential(q, note=True):
    thr = np.quantile(S, q)
    fig, ax = frame((7.0, 4.2))
    ax.streamplot(GX, GY, GU, GV, color="#C9D2D8", density=1.2, linewidth=0.8, arrowsize=0)
    m = S >= thr
    ax.streamplot(GX, GY, np.where(m, GU, np.nan), np.where(m, GV, np.nan),
                  color=ACCENT, density=1.3, linewidth=2.2, arrowsize=0)
    ax.contour(GX, GY, S, levels=[thr], colors=[ACCENT], linewidths=1.2, linestyles="--")
    if note:
        annot(ax, (3.6, 4.6), "above threshold:\nthe MESSAGE", dxy=(1.6, 1.2))
        annot(ax, (8.6, 1.0), "below: demoted\nto context", dxy=(-2.6, -0.5), color="#64707A")
    ax.set_title(f"damage threshold = {int(q*100)}th pct of speed  \u2190 AUTHORED", fontsize=9, color=MUTED)
    return fig

b = Builder("Same wind. What are you trying to SAY about it?", "fl04")
b.add("streamplot(color=speed)        # describe it", descriptive(),
      "DESCRIPTION: continuous, structure-first. The reader explores; the chart doesn't argue.",
      "fl04_desc.png",
      key="Descriptive charts rank NOTHING. That neutrality is itself a design choice \u2014 right for exploration, wrong for a warning.")
b.add("grey everything; alarm only speed >= p80   # consequence", consequential(0.80),
      "CONSEQUENCE: one threshold splits the world into message and context.",
      "fl04_p80.png",
      key="CONTRAST with step 1: identical field. The ONLY new ingredient is a threshold \u2014 one authored number converted a description into a warning.")
b.branch("threshold = p50                 # cautious agency", consequential(0.50),
      "Lower it: half the map is 'dangerous'. Same field \u2014 a more risk-averse institution talking.",
      "fl04_p50.png",
      key="STORY SWITCH: p80\u2192p50 changed no data and changed the story. Whoever sets the threshold authors the message.")
b.branch("threshold = p95                 # only the worst", consequential(0.95),
      "Raise it: danger shrinks to two ribbons. The threshold's PROVENANCE is the caption debt.",
      "fl04_p95.png",
      key="DISCLOSURE: a consequential chart owes its threshold AND where it came from (building code? wind-engineering table? a quantile of convenience?).")
b.end("Descriptive ranks nothing; consequential ranks everything \u2014 and the ranking parameter is authored. "
      "Choose the message, then disclose its dial.",
      key="THE PATTERN FOR THE WHOLE MODULE: think the sentence first \u2192 implement it as a parameter \u2192 disclose the parameter.")
