"""COMPONENT 7 — faceting.
Split one spec into aligned panels by a variable. Shared scales keep panels comparable;
scales="free_y" trades that for per-panel resolution. Run: python 07_facet.py [--save DIR]"""
from plotnine import ggplot, aes, geom_line, facet_wrap, facet_grid
from _data import df
from _show import show

series = df.groupby(["repo", "kind", "month"], as_index=False).size().rename(columns={"size": "prs"})
base = ggplot(series, aes(x="month", y="prs", colour="kind")) + geom_line()

show(base, "07_superposed.png")                                     # 12 lines in one panel
show(base + facet_wrap("~repo"), "07_wrap.png")                     # one panel per repo, shared axes
show(base + facet_wrap("~repo", scales="free_y"), "07_wrap_free.png")  # each panel its own y: cross-panel comparison lost
show(ggplot(series, aes(x="month", y="prs")) + geom_line() + facet_grid("kind ~ repo"),
     "07_grid.png")                                                 # rows × columns: two variables
