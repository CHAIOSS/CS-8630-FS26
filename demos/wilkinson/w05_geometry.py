"""WILKINSON — geometry asserts. Run: python w05_geometry.py [--save DIR]"""
from _w import *

m = monthly(prs()); a = m[m.repo == "augur"]
df = prs(); df["loglines"] = np.log10(df.lines)
b = Builder("What does each mark CLAIM about the data?", "w05")
b.add('geom_point()  # independent observations', ggplot(a, aes("month", "prs")) + geom_point(colour=INK, size=2) + theme_course, "", "w05_1.png")
b.branch('geom_line()  # a connected process', ggplot(a, aes("month", "prs")) + geom_line(colour=INK, size=1) + theme_course, "", "w05_2.png")
b.branch('geom_area()  # an accumulating quantity', ggplot(a, aes("month", "prs")) + geom_area(fill=TEAL, alpha=.6) + theme_course, "", "w05_3.png")
b.branch('geom_col()   # magnitudes from a base', ggplot(a, aes("month", "prs")) + geom_col(fill=ACCENT) + theme_course, "", "w05_4.png")
b.branch('geom_boxplot()  # a distribution, summarized', ggplot(df, aes("repo", "loglines")) + geom_boxplot(fill=TINT, colour=INK) + theme_course, "", "w05_5.png")
b.branch('geom_text()  # the values as marks', ggplot(a[a.month % 4 == 0], aes("month", "prs", label="prs")) + geom_text(size=11, colour=INK) + theme_course, "", "w05_6.png")
b.end("Readers believe the geometry's assertion (Unit 1: bars→groups, lines→trends). Which claim can your data cash?")
