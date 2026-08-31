"""COMPONENT 1 — data + aesthetic mapping.
A mapping says which variables go to which visual channels. It draws nothing
by itself: with no geom there is no mark to draw. Run: python 01_data_and_mapping.py [--save DIR]"""
from plotnine import ggplot, aes
from _data import m
from _show import show

p = ggplot(m, aes(x="month", y="prs", colour="repo"))   # data + mapping, no geom

print(p)   # plotnine prints the spec's structure
show(p, "01_mapping_only.png")   # an empty panel with axes: the ruler exists, the marks don't
