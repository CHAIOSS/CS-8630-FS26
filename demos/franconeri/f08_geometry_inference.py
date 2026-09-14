"""FRANCONERI CLAIM 8 — Geometry steers inference: bars imply discrete
groups, lines imply trends over a continuum. Interactive: two rounds of
'say what this chart shows in one sentence' — same two numbers.
Run: python f08_geometry_inference.py [--save DIR]"""
from _franconeri import *

def bars_fig():
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.bar(["group F", "group M"], [62, 71], color=[INK, ACCENT], width=.55)
    ax.set_ylim(0, 80); ax.set_title("One sentence: what does this show?")
    return fig

def line_fig():
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.plot(["group F", "group M"], [62, 71], "o-", color=INK, lw=2.5, ms=9)
    ax.set_ylim(0, 80); ax.set_title("Same numbers. One sentence: what does this show?")
    return fig

if "--save" in sys.argv:
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.7))
    axes[0].bar(["group F", "group M"], [62, 71], color=[INK, ACCENT], width=.55)
    axes[0].set_title("Bars → 'two discrete groups differ'", fontsize=10)
    axes[1].plot(["group F", "group M"], [62, 71], "o-", color=INK, lw=2.5, ms=9)
    axes[1].set_title("Line → 'a trend across a continuum'(!)", fontsize=10)
    for ax in axes: ax.set_ylim(0, 80)
    fig.suptitle("Two numbers, two geometries, two inferences (claim 8)", fontsize=12)
    fig.tight_layout(); finish(fig, "f08_barline.png")
else:
    for f in (bars_fig, line_fig):
        fig = f(); plt.show(block=False); plt.pause(0.1)
        input("  collect sentences, Enter for next: "); plt.close(fig)
    print("\n  Bars-round sentences compare groups; line-round sentences describe trends.")
    print("  The geometry made claims the data never did.")

claim("Claim 8 — geometry steers inference", [
  "Bars are read as categories; lines as continua — before reasoning starts.",
  "Choose the geometry for the claim you can defend (Unit 2 makes this a grammar component).",
])
