"""WICKHAM §3.3 & §6.2 — coordinates warp finished geometry.
Two canvases: the polar walk, then the flip. Run: python g04_coordinates.py [--save DIR]"""
from _grammar import *

df = prs()
counts = df.groupby("kind", as_index=False).size().rename(columns={"size": "n"}); counts["one"] = "all"
spec = lambda: (ggplot(counts, aes("one", "n", fill="kind")) + geom_col(width=1)
                + scale_fill_manual(values=[INK, ACCENT, TEAL]) + theme_course + labs(x="", y=""))
b = Builder("When does the pie start being a pie?", "g04")
b.add('stacked geom_col()', spec(), "One stacked bar. Cartesian. Ordinary.", "g04_cart.png")
b.add("  + coord_polar(theta=\'y\')   # ggplot2; plotnine lacks it",
      polar_figure(list(counts.n), list(counts.kind), "y"),
      "The y-axis wrapped into angle. Nothing else changed.", "g04_pie.png")
b.branch("  + coord_polar(theta=\'x\')",
      polar_figure(list(counts.n), list(counts.kind), "x"),
      "Wrap x instead: the bullseye. Same spec, other axis.", "g04_bullseye.png")
b.end("The grammar reads pie and bar as one sentence. Does your eye? (Unit 1 measured it.)")

byrepo = df.groupby("repo", as_index=False).size().rename(columns={"size": "n"})
cols = lambda: ggplot(byrepo, aes("reorder(repo, n)", "n")) + geom_col(fill=INK, width=.6) + theme_course + labs(x="repo")
b2 = Builder("What is the cheapest large improvement in the grammar?", "g04_flip")
b2.add('geom_col() on repos', cols(), "Vertical columns: labels fight for room.", "g04_cols.png")
b2.add('  + coord_flip()', cols() + coord_flip(),
      "One component: labels breathe, the sort reads top-down, comparison is position on a common scale.", "g04_flip.png")
b2.end("This is Cleveland\'s dot-plot logic (Unit 1) arriving through a coordinate word.")
