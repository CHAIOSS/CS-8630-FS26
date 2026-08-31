"""WICKHAM §4 — the defaults, made visible one line at a time.
Run: python g07_defaults.py [--save DIR]"""
from _grammar import *

m = monthly(prs())
minimal = lambda: ggplot(m, aes("month", "prs")) + geom_point()
b = Builder("You wrote one line. Who wrote the rest of this chart?", "g07")
b.add('ggplot(m, aes(month, prs)) + geom_point()', minimal() + theme_course,
      "A complete chart from two arguments. Watch the invisible co-author appear:", "g07_minimal.png")
same = minimal() + theme_course
for ln in ['   stat="identity", position="identity"   # filled in',
           '   scale_x_continuous() + scale_y_continuous()   # filled in',
           '   coord_cartesian()   # filled in',
           '   facet_null()   # filled in',
           '   theme, colour="black", size, alpha   # filled in']:
    b.add(ln, minimal() + theme_course, "The picture never changes — these lines were always there.")
b.add('OVERRIDE: aes(colour=repo) + scale_y_log10()',
      ggplot(m, aes("month", "prs", colour="repo")) + geom_point() + scale_y_log10()
      + scale_colour_manual(values=PAL) + theme_course,
      "Two defaults overridden deliberately — now the choices are yours to defend.", "g07_explicit.png")
b.end("Every chart is co-authored by its defaults. Which of these six would your task overrule?")
