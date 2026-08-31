"""WICKHAM §3.4 — faceting. Run: python g05_facets.py [--save DIR]"""
from _grammar import *

df = prs()
m = df.groupby(["repo", "kind", "month"], as_index=False).size().rename(columns={"size": "prs"})
sp = lambda: (ggplot(m, aes("month", "prs", colour="kind")) + geom_line()
              + scale_colour_manual(values=[INK, ACCENT, TEAL]) + theme_course)
b = Builder("What does splitting into panels buy — and what do free scales cost?", "g05")
b.add('12 series, superposed', sp(), "Try comparing docs-fixes across repos. (You can't; Unit 1 says why.)", "g05_super.png")
b.add('  + facet_wrap("~repo")', sp() + facet_wrap("~repo"),
      "Aligned panels: comparison by position returns.", "g05_wrap.png")
b.branch('  + facet_grid("kind ~ repo")',
      ggplot(m, aes("month", "prs")) + geom_line(colour=INK) + facet_grid("kind ~ repo") + theme_course,
      "Two variables become rows × columns.", "g05_grid.png")
b.branch('  + facet_wrap("~repo", scales="free_y")', sp() + facet_wrap("~repo", scales="free_y"),
      "Each panel legible — now find the repo with the most PRs. (You can't anymore.)", "g05_free.png")
b.end("Shared scales buy cross-panel comparison; free scales buy resolution. Your task picks.")
