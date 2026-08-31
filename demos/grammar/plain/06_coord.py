"""COMPONENT 6 — coordinate system.
Coordinates transform finished geometry. coord_flip exchanges axes; coord_trans warps
them AFTER statistics run (contrast with 04_scale's log, which runs BEFORE).
Run: python 06_coord.py [--save DIR]"""
from plotnine import ggplot, aes, geom_col, geom_point, geom_smooth, coord_flip, coord_trans, scale_x_log10, scale_y_log10
from _data import df
from _show import show

byrepo = df.groupby("repo", as_index=False).size().rename(columns={"size": "n"})
show(ggplot(byrepo, aes(x="reorder(repo, n)", y="n")) + geom_col(), "06_col.png")
show(ggplot(byrepo, aes(x="reorder(repo, n)", y="n")) + geom_col() + coord_flip(), "06_flip.png")

sample = df.sample(1500, random_state=1)
pts = ggplot(sample, aes(x="lines", y="hours")) + geom_point(alpha=0.2)
show(pts + scale_x_log10() + scale_y_log10() + geom_smooth(method="lm"),   # log BEFORE the fit → straight line
     "06_scale_then_fit.png")
show(pts + geom_smooth(method="lm") + coord_trans(x="log10", y="log10"),   # fit on raw data, THEN warp → bent line
     "06_fit_then_coord.png")
# ggplot2 also has coord_polar (stacked bar → pie); plotnine does not implement it.
