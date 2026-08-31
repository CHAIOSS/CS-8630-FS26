"""WILKINSON'S THESIS — chart types are neighborhoods in spec space.
One rung per Enter, one component per rung. Run: python g09_chart_types_dissolve.py [--save DIR]"""
from _grammar import *

m = monthly(prs()); a = m[m.repo == "augur"]
b = Builder("Where do 'chart types' live?", "g09")
b.add('geom_col()', ggplot(a, aes("month", "prs")) + geom_col(fill=INK) + theme_course, "", "g09_step1.png")
b.branch('geom_point()', ggplot(a, aes("month", "prs")) + geom_point(colour=INK, size=2) + theme_course,
      "One word: 'bar chart' became 'scatterplot'.", "g09_step2.png")
b.branch('geom_line()', ggplot(a, aes("month", "prs")) + geom_line(colour=INK, size=1) + theme_course,
      "One word: now a 'line chart'.", "g09_step3.png")
b.branch('geom_area()', ggplot(a, aes("month", "prs")) + geom_area(fill=TEAL, alpha=.6) + theme_course,
      "", "g09_step4.png")
b.branch('aes(prs) + geom_histogram()', ggplot(a, aes("prs")) + geom_histogram(bins=10, fill=ACCENT, colour="white") + theme_course,
      "Change the STAT and the mapping: a 'histogram' appears.", "g09_step5.png")
b.add("  + coord_polar(theta='y')   # ggplot2", polar_figure(list(a.prs[:8]), [f"m{i}" for i in a.month[:8]], "y"),
      "Change the COORD: a 'pie'. Six names, one sentence, six edits.", "g09_step6.png")
b.end("The names are neighborhoods. Assignment 2's ladder is this walk, with your reasons attached.")
