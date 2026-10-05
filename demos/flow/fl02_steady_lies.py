"""FLOW — streamlines are instants; pathlines are histories.
Run: python fl02_steady_lies.py [--save DIR]"""
from _fl import *

def panel(unsteady):
    fig, ax = frame((7.0, 4.2))
    ax.streamplot(GX, GY, GU, GV, color="#9AA7B0", density=1.2, linewidth=0.9, arrowsize=0)
    for sy in np.linspace(1.2, 5.2, 7):
        px, py = np.array([1.0]), np.array([sy]); xs, ys = [1.0], [sy]
        for k in range(120):
            u1, v1 = field(px, py, 0.05 * k if unsteady else 0.0)
            px = px + 0.05 * u1; py = py + 0.05 * v1
            xs.append(px[0]); ys.append(py[0])
        ax.plot(xs, ys, lw=1.8, color=ACCENT)
    return fig

b = Builder("The snapshot's promise vs the particle's history", "fl02")
b.add("steady field: release particles on the streamlines", panel(False),
      "Pathlines lie exactly ON the grey skeleton: one picture, whole truth.", "fl02_steady.png",
      key="In a STEADY field the snapshot is a forecast: streamline = pathline. Every static flow map implicitly claims this.")
b.branch("let the field EVOLVE while they travel", panel(True),
      "The vermilion histories peel off the snapshot. Every static wind map is the left claim "
      "made about this right-hand world.", "fl02_unsteady.png",
      key="CONTRAST: grey curves identical in both panels — only TIME was turned on. The gap between grey and vermilion IS the unsteadiness; a static map hides exactly this gap.")
b.end("Flow's disclosure: is this image an INSTANT or a WINDOW? A trail is a short pathline; "
      "extrapolating it is the steady-field lie.",
      key="DISCLOSURE #5 (flow edition): every flow image owes a declaration — instant or window, steady or evolving.")
