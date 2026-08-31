"""WILKINSON — statistics are graphing functions. Run: python w04_statistics.py [--save DIR]"""
from _w import *

df = prs(); df["loglines"] = np.log10(df.lines)
b = Builder("One variable — how many true charts?", "w04")
b.add('stat = identity', ggplot(df.sample(800, random_state=1), aes("repo", "loglines"))
      + geom_jitter(width=.2, alpha=.2, colour=MUTED) + theme_course,
      "The observations themselves.", "w04_identity.png")
b.branch('stat = count', ggplot(df, aes("repo")) + geom_bar(fill=INK) + theme_course,
      "geom_bar counts cases — implicit, but a statistic all the same.", "w04_count.png")
b.branch('stat = bin(25)', ggplot(df, aes("loglines")) + geom_histogram(bins=25, fill=ACCENT, colour="white") + theme_course,
      "", "w04_bin.png")
b.branch('stat = summary(mean, sd)', ggplot(df, aes("repo", "loglines"))
      + stat_summary(fun_data="mean_sdl", geom="pointrange", colour=INK) + theme_course,
      "A model, drawn.", "w04_summary.png")
b.branch('stat = smooth(loess)', ggplot(df.sample(1200, random_state=2), aes("loglines", "hours"))
      + geom_point(alpha=.15, colour=MUTED) + scale_y_log10()
      + geom_smooth(method="lowess", colour=ACCENT, se=False) + theme_course,
      "Cleveland's smoother as a component.", "w04_smooth.png")
b.end("Five statistics, five true charts. Choosing one is choosing the claim — the trail is your menu.")
