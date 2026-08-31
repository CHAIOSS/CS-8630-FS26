"""COMPONENT 5 — position adjustment.
Where do overlapping marks go? stack / dodge / fill are three answers, one geom.
Run: python 05_position.py [--save DIR]"""
from plotnine import ggplot, aes, geom_col
from _data import df
from _show import show

counts = df.groupby(["repo", "kind"], as_index=False).size().rename(columns={"size": "n"})
base = ggplot(counts, aes(x="repo", y="n", fill="kind"))

show(base + geom_col(position="stack"), "05_stack.png")   # totals + composition
show(base + geom_col(position="dodge"), "05_dodge.png")   # side by side: direct comparison
show(base + geom_col(position="fill"),  "05_fill.png")    # proportions: totals discarded
