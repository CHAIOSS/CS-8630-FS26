"""WILKINSON — mapping vs setting. Run: python w07_aesthetics.py [--save DIR]"""
from _w import *

m = monthly(prs())
b = Builder("When is colour a claim, and when is it paint?", "w07")
b.add('aes(colour = repo)          # MAPPED',
      ggplot(m, aes("month", "prs", colour="repo")) + geom_line(size=1)
      + scale_colour_manual(values=PAL) + theme_course,
      "Colour carries data: a scale and a legend exist.", "w07_mapped.png")
b.branch('geom_line(colour = "vermilion")   # SET',
      ggplot(m, aes("month", "prs", group="repo")) + geom_line(size=1, colour=ACCENT) + theme_course,
      "An attribute: no scale, no legend, no claim.", "w07_set.png")
b.branch('aes(colour = "vermilion")   # the BUG',
      ggplot(m, aes("month", "prs", group="repo", colour="\'vermilion\'")) + geom_line(size=1) + theme_course,
      "Look at the colour: it is NOT vermilion — the string was mapped through the default "
      "hue scale as a one-level variable, and a legend was invented for it.", "w07_bug.png")
b.end("Every legend entry is a claim. If an attribute carries no data, it must not have one.")
