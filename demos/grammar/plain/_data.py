"""The course dataset, nothing else. Every plain example starts: from _data import m, df"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _grammar import prs, monthly
df = prs()              # one row per pull request: repo, month, lines, hours, kind
m = monthly(df)         # one row per repo-month: repo, month, prs
