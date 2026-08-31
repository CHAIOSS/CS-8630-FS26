"""WILKINSON — the ruler's type is a claim. Run: python w03_scales.py [--save DIR]"""
from _w import *
import pandas as pd

m = monthly(prs()); a = m[m.repo == "augur"].copy()
b = Builder("Same numbers — what does each ruler claim about them?", "w03")
b.add('x = month (CONTINUOUS)', ggplot(a, aes("month", "prs")) + geom_col(fill=INK) + theme_course,
      "A number line: gaps would show as gaps.", "w03_cont.png")
a["month_cat"] = pd.Categorical(a.month)
b.branch('x = factor(month) (CATEGORICAL)',
      ggplot(a, aes("month_cat", "prs")) + geom_col(fill=ACCENT) + theme_course + theme(axis_text_x=element_text(size=6)),
      "24 unordered boxes: equal spacing asserted, order is convention.", "w03_cat.png")
a["date"] = pd.to_datetime("2025-01-01") + pd.to_timedelta(a.month * 30.44, unit="D")
b.branch('x = as.Date(month) (TIME)', ggplot(a, aes("date", "prs")) + geom_col(fill=TEAL) + theme_course,
      "A calendar-aware ruler: it knows about years.", "w03_time.png")
b.end("Declaring the scale type declares the level of measurement. Which claim is true of YOUR variable?")
