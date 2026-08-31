"""WICKHAM §3.1 — layers stack; positions resolve overlap.
Two canvases: one sentence each. Run: python g02_layers.py [--save DIR]"""
from _grammar import *

df = prs()
sp = lambda: ggplot(df, aes("lines", "hours")) + scale_x_log10() + scale_y_log10() + theme_course
b = Builder("What is a layer?", "g02")
b.add('ggplot(df, aes(lines, hours)) + log scales + geom_point()',
      sp() + geom_point(alpha=.15, colour=INK), "", "g02_layer1.png")
b.add('  + geom_smooth(method="lowess")',
      sp() + geom_point(alpha=.15, colour=INK) + geom_smooth(method="lowess", colour=ACCENT, se=False),
      "A layer that carries its own statistic.", "g02_layer2.png")
b.add('  + geom_rug()',
      sp() + geom_point(alpha=.15, colour=INK) + geom_smooth(method="lowess", colour=ACCENT, se=False) + geom_rug(alpha=.05, colour=TEAL),
      "Three layers, one mapping — nothing was switched, only stacked.", "g02_layer3.png")
b.end("Each layer = data + mapping + stat + geom + position. What fourth layer would earn its ink here?")

counts = df.groupby(["repo", "kind"], as_index=False).size().rename(columns={"size": "n"})
bars = lambda pos: (ggplot(counts, aes("repo", "n", fill="kind")) + geom_col(position=pos)
                    + scale_fill_manual(values=[INK, ACCENT, TEAL]) + theme_course)
b2 = Builder("Where do overlapping marks go?", "g02_pos")
b2.add('geom_col(position="stack")', bars("stack"), "Totals plus composition.", "g02_pos_stack.png")
b2.branch('geom_col(position="dodge")', bars("dodge"), "Direct comparison within groups — position on a common scale.", "g02_pos_dodge.png")
b2.branch('geom_col(position="fill")', bars("fill"), "Proportions; totals traded away.", "g02_pos_fill.png")
b2.end("One word changed three times. Which answers \'who does the most fixes\'? Which \'who does the most work\'?")
