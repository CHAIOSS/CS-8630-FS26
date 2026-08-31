"""WILKINSON Ch. 5 — cross, nest, blend, rendered as they are written.
Run: python g08_wilkinson_algebra.py [--save DIR]"""
from _grammar import *

df = prs()
c = df.groupby(["repo", "kind", "month"], as_index=False).size().rename(columns={"size": "prs"})
c["half"] = np.where(c.month < 12, "year 1", "year 2")
agg = c.groupby(["repo", "kind", "half"], as_index=False)["prs"].sum()
y1 = agg[agg.half == "year 1"]
b = Builder("Three operators, three layouts — no chart types named.", "g08")
b.add('repo * kind          (CROSS)',
      ggplot(y1, aes("repo", "prs", fill="kind")) + geom_col(position="dodge")
      + scale_fill_manual(values=[INK, ACCENT, TEAL]) + theme_course,
      "Every combination gets a position: the product of two domains.", "g08_cross.png")
b.branch('kind / repo          (NEST)',
      ggplot(y1, aes("kind", "prs", fill="kind")) + geom_col() + facet_wrap("~repo", nrow=1)
      + scale_fill_manual(values=[INK, ACCENT, TEAL]) + theme_course + theme(legend_position="none"),
      "A scope, not a product: each panel carries its own kinds.", "g08_nest.png")
b.branch('year1 + year2        (BLEND)',
      ggplot(agg, aes("half", "prs", fill="kind")) + geom_col()
      + scale_fill_manual(values=[INK, ACCENT, TEAL]) + theme_course,
      "Two variable sets unioned onto one axis.", "g08_blend.png")
b.end("Write the expression for a chart from your own research — then check what it renders as.")
