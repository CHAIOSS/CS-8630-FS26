"""COMPONENT 8 — theme, and the defaults you never wrote.
The minimal spec below renders because six components were filled in for you.
The explicit spec is the same chart with every choice written down. Run: python 08_theme_and_defaults.py [--save DIR]"""
from plotnine import (ggplot, aes, geom_point, scale_x_continuous, scale_y_continuous,
                      coord_cartesian, facet_null, theme_grey, theme_minimal, labs)
from _data import m
from _show import show

minimal = ggplot(m, aes(x="month", y="prs")) + geom_point()

explicit = (ggplot(m, aes(x="month", y="prs"))
            + geom_point(stat="identity", position="identity", colour="black", size=1.5, alpha=1)
            + scale_x_continuous() + scale_y_continuous()
            + coord_cartesian()
            + facet_null()
            + theme_grey()
            + labs(x="month", y="prs"))

show(minimal,  "08_minimal.png")    # what you wrote
show(explicit, "08_explicit.png")   # what the grammar wrote — identical picture
show(minimal + theme_minimal(), "08_theme_minimal.png")   # theme: presentation, not meaning
