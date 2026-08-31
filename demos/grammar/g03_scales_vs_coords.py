"""WICKHAM §3.2 & §6.3 — the same word \'log\', two pipeline positions.
Two canvases: the transform lesson, then the colour-scale lesson.
Run: python g03_scales_vs_coords.py [--save DIR]"""
from _grammar import *

df = prs().sample(1500, random_state=1)
base = lambda: ggplot(df, aes("lines", "hours")) + geom_point(alpha=.2, colour=INK) + theme_course
b = Builder("Where in the pipeline does \'log\' happen?", "g03")
b.add('ggplot(df, aes(lines, hours)) + geom_point()', base(), "Skew crushes the bulk into a corner.", "g03_raw.png")
b.add('  + scale_x_log10() + scale_y_log10() + geom_smooth(lm)',
      base() + scale_x_log10() + scale_y_log10() + geom_smooth(method="lm", colour=ACCENT, se=False),
      "SCALE: data logged BEFORE the fit — the line is straight.", "g03_scale.png")
b.branch('  + geom_smooth(lm) + coord_trans(x="log10", y="log10")',
      base() + geom_smooth(method="lm", colour=ACCENT, se=False) + coord_trans(x="log10", y="log10"),
      "COORD: fit first on raw data, axes warped after — the same fit bends.", "g03_coord.png")
b.end("Same word, two positions, two claims. Which chart\'s slope would you report — and why?")

m = monthly(prs())
lines = lambda: ggplot(m, aes("month", "prs", colour="repo")) + geom_line(size=1) + theme_course
b2 = Builder("Colour is a scale too — what does the palette claim?", "g03_col")
b2.add('  + scale_colour_manual(values=PAL)', lines() + scale_colour_manual(values=PAL),
      "A chosen qualitative palette: four categories, no order implied.", "g03_col1.png")
b2.branch('  + scale_colour_brewer(type="seq")', lines() + scale_colour_brewer(type="seq"),
      "Same data, ORDERED palette — the reader now infers a ranking that does not exist.", "g03_col2.png")
b2.end("Which repo does this palette say is \'highest\'? (None is. That\'s the defect — Unit 3 names it.)")
