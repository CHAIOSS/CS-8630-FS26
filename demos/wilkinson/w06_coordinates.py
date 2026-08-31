"""WILKINSON Ch. 9 — coordinates warp finished marks. Run: python w06_coordinates.py [--save DIR]"""
from _w import *

df = prs().groupby("kind", as_index=False).size().rename(columns={"size": "n"})
base = lambda: ggplot(df, aes("kind", "n")) + geom_col(fill=INK) + theme_course
b = Builder("The marks are finished. What can the space still do to them?", "w06")
b.add('geom_col()', base(), "Intervals from a base, Cartesian.", "w06_cart.png")
b.add('  + coord_flip()', base() + coord_flip(), "Axes exchanged; the intervals never re-drawn.", "w06_flip.png")
b.branch("  + coord_polar(theta='y')   # ggplot2", polar_figure(list(df.n), list(df.kind), "y"),
      "The stacked intervals wrapped: the pie exists only in this space.", "w06_polar.png")
b.end("A map projection lives in this same slot. The eye prices the warp; the grammar just performs it.")
