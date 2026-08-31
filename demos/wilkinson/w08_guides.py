"""WILKINSON — guides are the scales\' inverses. Run: python w08_guides.py [--save DIR]"""
from _w import *

m = monthly(prs())
base = lambda: (ggplot(m, aes("month", "prs", colour="repo")) + geom_line(size=1)
                + scale_colour_manual(values=PAL) + theme_course)
b = Builder("Strip the guides — what can the reader still recover?", "w08")
b.add('guides removed', base() + theme(legend_position="none", axis_title=element_blank(),
      axis_text=element_blank()), "Marks without inverses: no value is recoverable.", "w08_bare.png")
b.add('default guides', base(), "Axes and legend: every scale exposes its inverse.", "w08_default.png")
last = m[m.month == m.month.max()]
b.add('  + reference line + direct labels', base() + theme(legend_position="none")
      + geom_hline(yintercept=40, linetype="dashed", colour=MUTED)
      + annotate("text", x=0.5, y=42, label="capacity: 40 PRs/mo", size=9, colour=MUTED, ha="left")
      + geom_text(last, aes(label="repo"), nudge_x=1.2, size=9, show_legend=False),
      "Guides as argument: the claim becomes checkable at a glance (Cleveland, Unit 1).", "w08_argument.png")
b.end("An axis is a function, drawn. What would an argumentative guide look like on your project's main view?")
