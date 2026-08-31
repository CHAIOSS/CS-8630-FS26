"""WICKHAM §6.1 — the statistic inside the spec. Run: python g06_statistics_binwidth.py [--save DIR]"""
from _grammar import *

df = prs(); df["loglines"] = np.log10(df["lines"])
base = lambda: ggplot(df, aes("loglines")) + theme_course + labs(x="log10(lines changed)")
b = Builder("Who authored this histogram's finding?", "g06")
b.add('geom_histogram(bins=5)', base() + geom_histogram(bins=5, fill=ACCENT, colour="white"),
      "'One broad population.'", "g06_bins5.png")
b.branch('geom_histogram(bins=20)', base() + geom_histogram(bins=20, fill=INK, colour="white"),
      "'Two groups.' Same data.", "g06_bins20.png")
b.branch('geom_histogram(bins=80)', base() + geom_histogram(bins=80, fill=ACCENT, colour="white"),
      "'Noise everywhere.' Still the same data.", "g06_bins80.png")
b.add('geom_density()', base() + geom_density(fill=TEAL, alpha=.4, colour=TEAL),
      "Swap the statistic: the authored parameter is now bandwidth.", "g06_density.png")
q = df.sort_values("loglines").reset_index(drop=True); q["f"] = (np.arange(len(q)) + .5) / len(q)
b.add('stat = identity (the quantile plot)',
      ggplot(q, aes("f", "loglines")) + geom_point(size=.5, colour=INK) + theme_course,
      "Every observation, nothing authored — Cleveland's answer.", "g06_quantile.png")
b.end("There is no 'the histogram' — only a histogram at a stated bin width. Which would you publish, and why?")
