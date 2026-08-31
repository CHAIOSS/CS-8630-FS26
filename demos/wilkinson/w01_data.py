"""WILKINSON — DATA is a slot. Run: python w01_data.py [--save DIR]"""
from _w import *

spec = lambda df: (ggplot(df, aes("month", "prs", colour="repo")) + geom_line(size=1)
                   + scale_colour_manual(values=PAL) + theme_course)
m = monthly(prs())
b = Builder("If the data changes, what happens to the sentence?", "w01")
b.add('spec(dataset_A)', spec(m), "All repos, 24 months.", "w01_a.png")
b.branch('spec(dataset_B)   # a filter upstream — the spec verbatim',
      spec(m[(m.repo.isin(["augur", "docs"])) & (m.month >= 12)]),
      "Nothing in the sentence changed. Data is one slot of eight.", "w01_b.png")
b.end("Templates couple data to picture; grammars decouple them. Where else would this spec work?")
