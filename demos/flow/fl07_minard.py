"""THE CLASSIC — Minard's 1869 flow map, rebuilt from ~20 rows.
Run: python fl07_minard.py [--save DIR]   (data simplified; original public domain)"""
from _fl import *

ADV = [(24.0,54.9,422),(25.3,54.7,400),(26.4,54.5,340),(28.2,54.3,320),(30.3,54.8,300),
       (32.0,54.8,190),(33.2,54.9,175),(34.4,55.5,145),(35.5,55.4,140),(36.0,55.5,127),(37.6,55.8,100)]
RET = [(37.6,55.3,98),(36.6,55.2,97),(35.4,55.3,55),(34.3,55.2,37),(33.3,54.8,24),
       (32.0,54.6,20),(30.4,54.4,50),(28.7,54.3,28),(26.8,54.3,12),(25.0,54.4,8),(24.1,54.4,10)]
TMP = [(37.6,0),(36.0,-9),(33.2,-21),(32.0,-11),(29.2,-20),(28.5,-24),(26.8,-30),(25.0,-26)]

def band(ax, pts, color, scale=0.004):
    for (x1,y1,n1),(x2,y2,n2) in zip(pts[:-1], pts[1:]):
        w1,w2 = n1*scale, n2*scale
        dx,dy = x2-x1, y2-y1; L = np.hypot(dx,dy)+1e-9
        nx,ny = -dy/L, dx/L
        ax.add_patch(plt.Polygon([(x1+nx*w1,y1+ny*w1),(x2+nx*w2,y2+ny*w2),
                                  (x2-nx*w2,y2-ny*w2),(x1-nx*w1,y1-ny*w1)], closed=True, color=color, lw=0))

def stage(advance, retreat, temps):
    fig = plt.figure(figsize=(7.4, 4.2))
    axM = fig.add_axes([0.03, 0.34 if temps else 0.08, 0.94, 0.58 if temps else 0.84])
    if advance: band(axM, ADV, "#C8A24B")
    if retreat: band(axM, RET, INK)
    for x,y,n in ([ADV[0], ADV[-1]] + ([RET[-1]] if retreat else [])):
        axM.text(x, y+0.55, f"{n}k", fontsize=9, ha="center", color=INK)
    axM.set_xlim(23.2, 38.6); axM.set_ylim(53.2, 57.0); axM.axis("off")
    if temps:
        axT = fig.add_axes([0.03, 0.06, 0.94, 0.2])
        tx=[t[0] for t in TMP]; tv=[t[1] for t in TMP]
        axT.plot(tx, tv, "o-", color=TEAL, lw=1.6, ms=3)
        axT.set_xlim(23.2, 38.6); axT.set_ylim(-38, 6); axT.set_xticks([]); axT.set_yticks([])
    return fig

b = Builder("Six variables, twenty rows, one catastrophe", "fl07")
b.add("band(ADVANCE, width = army size)", stage(True, False, False),
      "422k leave Kowno; 100k reach Moscow. Width is doing all the arithmetic.", "fl07_adv.png",
      key="Width = quantity, continuously, with ONE scale for the whole map — that constancy is what keeps every width comparable.")
b.add("  + band(RETREAT, black)", stage(True, True, False),
      "Direction as VALUE (tan/black = before/after). The return path tells its own story \u2014 "
      "and ends at 10k.", "fl07_ret.png",
      key="CONTRAST tan vs black: hue doing ORDINAL work (before/after), not decoration. Two bands = the campaign\u2019s question: what went in vs what came back.")
b.add("  + linked temperature panel below", stage(True, True, True),
      "Minard's masterstroke: the cold snaps align VERTICALLY with the retreat band's collapses. "
      "Causation's silhouette, no caption needed.", "fl07_full.png")
b.end("Every stroke here is one polygon function plus editorial nerve. The original (Tufte's "
      "plate) adds dates, rivers, and the Berezina crossing \u2014 six variables, 1869, zero animation.")
