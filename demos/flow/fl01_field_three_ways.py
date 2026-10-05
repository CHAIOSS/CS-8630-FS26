"""FLOW — one field: sample it, integrate it, inhabit it.
Run: python fl01_field_three_ways.py [--save DIR]"""
from _fl import *

b = Builder("Velocity is everywhere; your ink is not", "fl01")

fig, ax = frame(); ax.quiver(GX[::2, ::2], GY[::2, ::2], GU[::2, ::2], GV[::2, ::2], color=INK, scale=36, width=0.003)
annot(ax, (3.2, 4.2), "a vortex lives here —\ncan you see it in arrows?", dxy=(1.3, 1.2))
annot(ax, (1.0, 2.6), "the jet: arrows agree,\nstructure only implied", dxy=(0.4, -1.8), color=TEAL)
b.add("quiver(X, Y, U, V)         # sample the field", fig,
      "Honest and local \u2014 every arrow true \u2014 and the CONNECTIVITY is left for your brain to integrate.",
      "fl01_quiver.png",
      key="Glyphs answer 'what is the velocity HERE?' They never answer 'what is the field DOING?' \u2014 that question needs integration.")

fig, ax = frame(); ax.streamplot(GX, GY, GU, GV, color=INK, density=1.2, linewidth=1.0, arrowsize=0.9)
annot(ax, (3.2, 4.2), "SAME vortex: now it\nannounces itself", dxy=(1.3, 1.2))
annot(ax, (7.0, 2.2), "second vortex, opposite\nspin (G < 0)", dxy=(-2.6, -1.4), color=TEAL)
b.add("streamplot(...)            # integrate it", fig,
      "Integral curves: the field's skeleton. Nothing was added to the DATA \u2014 only to the construction.",
      "fl01_stream.png",
      key="CONTRAST with step 1: identical field, identical information \u2014 the vortices were invisible, now they're the headline. Construction choice IS message choice.")

fig, ax = frame()
sp = ax.streamplot(GX, GY, GU, GV, color=np.hypot(GU, GV), cmap="viridis", density=1.3, linewidth=1.1, arrowsize=0.8)
annot(ax, (5.2, 3.6), "bright = fast: colour now\ncarries magnitude", dxy=(1.5, 1.6))
b.branch("streamplot(color=speed)    # free colour for magnitude", fig,
      "Position spent on structure, colour on speed \u2014 the division of labor every weather map uses.",
      "fl01_speed.png",
      key="Unit 1's ladder at work: structure rides position (top channel); magnitude rides colour value (good enough for overview). Two variables, two channels, no fight.")

fig, ax = frame()
tr = advect()
for i in range(0, 350, 2):
    ax.plot([t[0][i] for t in tr[-14:]], [t[1][i] for t in tr[-14:]], lw=0.7, color=ACCENT, alpha=0.5)
annot(ax, (3.4, 4.3), "long trail = fast\n(trail length \u2248 recent speed)", dxy=(1.6, 1.3), color=INK)
annot(ax, (8.6, 5.6), "short trails: the calm zone", dxy=(-3.0, 0.4), color=INK)
b.add("advect particles, draw trails   # inhabit it", fig,
      "One frame of the living version: each trail is a short HISTORY, not a decoration. fl03 animates this.",
      "fl01_particles.png",
      key="A trail is a tiny pathline. That makes this panel TEMPORAL \u2014 and sets the trap slide 1.3 springs: trails tempt you to extrapolate.")

b.end("Three constructions, one triage: glyphs for spot reads, curves for structure, particles for NOW. "
      "The arrow was never wrong \u2014 it just doesn't scale.",
      key="SAME DATA EVERY PANEL. What changed was the question each construction answers \u2014 pick the question first, then the construction.")
