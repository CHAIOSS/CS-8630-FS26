"""COMPONENT 3 — statistic.
Most geoms carry a hidden stat (geom_point: identity; geom_histogram: bin;
geom_bar: count; geom_smooth: a model). Naming the stat makes its parameter visible.
Run: python 03_stat.py [--save DIR]"""
from plotnine import ggplot, aes, geom_histogram, geom_bar, geom_point, geom_smooth, scale_x_log10, scale_y_log10
from _data import df
from _show import show

show(ggplot(df, aes(x="lines")) + scale_x_log10() + geom_histogram(bins=30),   # stat = bin, parameter = 30
     "03_bin30.png")
show(ggplot(df, aes(x="lines")) + scale_x_log10() + geom_histogram(bins=8),    # same data, parameter = 8
     "03_bin8.png")
show(ggplot(df, aes(x="repo")) + geom_bar(),                                    # stat = count (no y needed)
     "03_count.png")
show(ggplot(df, aes(x="lines", y="hours")) + scale_x_log10() + scale_y_log10()
     + geom_point(alpha=0.15) + geom_smooth(method="lowess"),                  # stat = loess smoother
     "03_smooth.png")
