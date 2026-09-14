"""Shared helpers for the Franconeri et al. 2021 claim demos."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _style import *   # INK, ACCENT, TEAL, MUTED, TINT, finish, plt, np

def claim(title, points):
    print(f"\n=== {title} ===")
    for p in points: print("  •", p)

def timed_enter(prompt):
    """Show prompt, return seconds until Enter."""
    t0 = time.time(); input(prompt); return time.time() - t0
