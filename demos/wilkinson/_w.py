"""Shared helpers for the Wilkinson key-point examples (reuses the grammar library)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "grammar"))
from _grammar import *   # plotnine, dataset prs()/monthly(), show(), step(), say(), polar_fallback, PAL, theme_course
