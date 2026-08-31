"""COMPONENT 4 — scales.
A scale maps data values to a channel's values (position, colour, size).
Changing a scale changes the ruler, not the marks. Run: python 04_scale.py [--save DIR]"""
from plotnine import ggplot, aes, geom_line, scale_y_log10, scale_colour_manual, scale_colour_brewer
from _data import m
from _show import show

base = ggplot(m, aes(x="month", y="prs", colour="repo")) + geom_line()

show(base, "04_default_scales.png")                                   # scales filled in by defaults
show(base + scale_y_log10(), "04_log_y.png")                          # position scale: equal % growth → parallel lines
show(base + scale_colour_manual(values={"augur": "#2B3A42", "frontend": "#E4572E",
                                         "docs": "#1C7293", "cli": "#8A5A9E"}),
     "04_colour_manual.png")                                          # colour scale: a chosen qualitative palette
show(base + scale_colour_brewer(type="seq"), "04_colour_seq_WRONG.png")  # ordered palette on unordered data (a mismatch)
