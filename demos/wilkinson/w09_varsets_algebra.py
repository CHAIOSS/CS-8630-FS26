"""WILKINSON Ch. 4–5 — varsets and the algebra, printed and rendered.
Run: python w09_varsets_algebra.py [--save DIR]"""
from _w import *
import pandas as pd

toy = pd.DataFrame({"repo": ["augur","augur","docs","docs","cli"],
                    "kind": ["fix","feature","fix","docs","fix"],
                    "n":    [12, 9, 4, 7, 5]})
print("\nThe table:"); print(toy.to_string(index=False))
print("\nAs VARSETS (value -> cases):")
for col in ["repo", "kind"]:
    vs = {v: sorted(toy.index[toy[col] == v].tolist()) for v in toy[col].unique()}
    print(f"  {col}: {vs}")
b = Builder("What do the three operators DO to variable sets?", "w09")
b.add('repo * kind    (CROSS: every pair, empty cells kept)',
      ggplot(toy, aes("repo", "n", fill="kind")) + geom_col(position="dodge") + theme_course
      + scale_fill_manual(values=[INK, ACCENT, TEAL]),
      "The product of two domains — the missing bars are real, empty cells.", "w09_cross.png")
b.branch('kind / repo    (NEST: kind scoped inside repo)',
      ggplot(toy, aes("kind", "n", fill="kind")) + geom_col() + facet_wrap("~repo", scales="free_x")
      + theme_course + scale_fill_manual(values=[INK, ACCENT, TEAL]) + theme(legend_position="none"),
      "Each panel carries only ITS kinds — free_x is the scoping made visible.", "w09_nest.png")
bl = pd.concat([toy.assign(period="year 1"), toy.assign(period="year 2", n=toy.n * 1.4)])
b.branch('year1 + year2  (BLEND: union onto one axis)',
      ggplot(bl, aes("period", "n", fill="kind")) + geom_col() + theme_course
      + scale_fill_manual(values=[INK, ACCENT, TEAL]),
      "", "w09_blend.png")
b.end("Dodges, scoped panels, stacked periods: expressions, not chart choices. Write yours before you plot.")
