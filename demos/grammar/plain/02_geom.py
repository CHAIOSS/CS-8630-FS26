"""COMPONENT 2 — geometry (the mark).
Adding a geom is what makes the mapping visible. Swap the geom, keep everything else.
Run: python 02_geom.py [--save DIR]"""
from plotnine import ggplot, aes, geom_point, geom_line, geom_col
from _data import m
from _show import show

base = ggplot(m, aes(x="month", y="prs", colour="repo"))

show(base + geom_point(), "02_point.png")   # each row becomes a dot
show(base + geom_line(),  "02_line.png")    # rows connected within each colour group
show(base + geom_col(),   "02_col.png")     # bars from zero (colour maps to outline; fill would map to fill)
