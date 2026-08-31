"""WILKINSON Ch. 2 — \'How to Make a Pie\': the pipeline, walked.
Run: python w10_pie_pipeline.py [--save DIR]"""
from _w import *
import pandas as pd

df = prs()
counts = df.groupby("kind", as_index=False).size().rename(columns={"size": "n"})
counts["prop"] = counts.n / counts.n.sum(); counts["one"] = "all"
b = Builder("At which stage does the pie start existing?", "w10")
b.add('DATA: per-PR records  ->  VARSET: kind',
      ggplot(df.sample(600, random_state=3), aes("kind")) + geom_bar(fill=MUTED) + theme_course,
      "Raw cases, counted — nothing pie-like anywhere.", None)
b.add('STAT: summary.proportion',
      ggplot(counts, aes("kind", "prop")) + geom_col(fill=INK) + theme_course + labs(y="proportion"),
      "Proportions as intervals: an ordinary bar.", "w10_stat.png")
b.add('GEOM+POSITION: one stacked interval',
      ggplot(counts, aes("one", "prop", fill="kind")) + geom_col(width=1) + theme_course
      + scale_fill_manual(values=[INK, ACCENT, TEAL]) + labs(x="", y="proportion"),
      "Stacked on one base. Still Cartesian. Still ordinary.", "w10_stack.png")
b.add("COORD: polar(theta='y')", polar_figure(list(counts.n), list(counts.kind), "y"),
      "NOW it is a pie — born in the final stage. Every earlier stage was a bar chart's.", "w10_pie.png")
b.end("The pie and the bar differ by one coordinate word. \'Pie\' was never a noun; it was a route.")
