"""WICKHAM §2 — one chart, built. The spec grows on the left; the picture
answers on the right. Run: python g01_build_a_plot.py [--save DIR]"""
from _grammar import *

df = monthly(prs())
b = Builder("What does each added word do?", "g01")
base = lambda: ggplot(df, aes("month", "prs", colour="repo")) + theme_course
b.add('ggplot(m, aes(month, prs, colour=repo))', base(),
      "A mapping with no geom: a sentence without a verb renders an empty panel.", "g01_step1.png")
b.add('  + geom_point()', base() + geom_point(), "", "g01_step2.png")
b.add('  + scale_colour_manual(...)', base() + geom_point() + scale_colour_manual(values=PAL),
      "Same marks — the data→colour function changed.", "g01_step3.png")
b.add('  + geom_line()', base() + geom_point() + geom_line() + scale_colour_manual(values=PAL),
      "A second layer on the same mapping.", "g01_step4.png")
b.add('  + scale_y_log10()', base() + geom_point() + geom_line() + scale_colour_manual(values=PAL) + scale_y_log10(),
      "Nothing was redrawn by hand; the ruler changed.", "g01_step5.png")
b.end("Five lines, five pictures. Which line would you change to ask about growth rates?")
