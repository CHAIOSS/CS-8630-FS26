"""WILKINSON — TRANS runs first. Run: python w02_trans.py [--save DIR]"""
from _w import *
import pandas as pd

df = prs().groupby("repo", as_index=False).agg(total=("lines", "sum"), med_hours=("hours", "median"))
b = Builder("What can a variable transformation show that a scale cannot?", "w02")
b.add('aes(total, med_hours) + geom_point()',
      ggplot(df, aes("total", "med_hours")) + geom_point(size=3, colour=INK) + theme_course,
      "Raw variables: skew smears the small repos together.", "w02_raw.png")
df["rank_total"], df["rank_hours"] = df.total.rank(), df.med_hours.rank()
b.add('TRANS: rank(total), rank(med_hours)   # new variables, computed first',
      ggplot(df, aes("rank_total", "rank_hours")) + geom_point(size=3, colour=ACCENT)
      + geom_text(aes(label="repo"), nudge_y=.15, size=9) + theme_course,
      "The monotone relationship is now the whole picture — a new variable, not a new ruler.", "w02_rank.png")
b.end("TRANS makes variables; SCALE makes rulers. Everything downstream sees only what TRANS produced.")
