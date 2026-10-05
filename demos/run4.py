#!/usr/bin/env python3
"""CS 8630 demo launcher — run from the demos/ folder:  python run.py
Numbered menu; each pick runs the demo LIVE (interactive canvas / animation)."""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
MENU = [
  ("UNIT 4c \u00b7 FLOW & MOTION", None),
  ("Field three ways: sample \u2192 integrate \u2192 inhabit", "flow/fl01_field_three_ways.py", "same data every panel — construction choice IS message choice"),
  ("Steady lies: pathlines peel off the snapshot", "flow/fl02_steady_lies.py", "instant vs history: the disclosure every static flow map owes"),
  ("LIVE wind map + the one-mover pop-out", "flow/fl03_windmap_motion.py", "motion's budget: one field or one mover — then it's spent"),
  ("Message study: descriptive vs consequential wind", "flow/fl04_message_wind.py", "one threshold = description→warning; p50/p80/p95 move the story"),
  ("Message study: the microburst's two planes", "flow/fl05_microburst.py", "plan view hides the killer; the SECTION is the claim"),
  ("Message study: river, flood, and d\u00d7v", "flow/fl06_river_flood.py", "velocity vs depth×velocity: the variable switch flips the safety story"),
  ("Minard 1869, rebuilt from twenty rows", "flow/fl07_minard.py", "width does the arithmetic; alignment makes the argument; zero animation"),
  ("UNIT 4c \u00b7 FRACTAL TIME", None),
  ("Coastline & the zoom that looks like itself", "fractaltime/ft01_coastline_zoom.py", "the ruler is a choice: 'daily data' already made it"),
  ("Hurst + burstiness: texture as a statistic", "fractaltime/ft02_hurst_bursts.py", "same event count, two textures — H and the CCDF make it measurable"),
  ("The cascade: eddies \u2192 \u22125/3", "fractaltime/ft03_cascade.py", "run during the couplet slide: one keypress per line"),
  ("Parameter outcomes: windows & promises", "fractaltime/ft04_parameter_outcomes.py", "window picks the headline; statistic picks the promise — all true"),
  ("Spectrum lab: memory across scales + shuffle null", "fractaltime/ft05_spectrum_lab.py", "memory across scales + the two robustness checks (rebin, shuffle)"),
  ("H playground: persistence, zoom, window-stories", "fractaltime/ft06_h_playground.py", "persistence manufactures trend-shaped accidents — the honest null"),
  ("Story switch: one log, two dashboards", "fractaltime/ft07_story_switch.py", "two dashboards, six lines apart — the loop the assignment grades"),
  ("UNIT 4b \u00b7 TEMPORAL", None),
  ("Gaps & banking", "temporal/tp01_time_and_gaps.py", "gaps are claims: interpolate / break / zero"),
  ("Many series \u2192 the horizon chart", "temporal/tp02_many_series.py", "attention vs area vs ink: three spendings of one space"),
  ("Cycles & the wrong-period fold", "temporal/tp03_cycles.py", "the fold is sanctioned; the WRONG period manufactures pattern"),
  ("Level/growth/rate, windows, connected scatter", "temporal/tp04_change.py", "level/growth/rate + the baseline that changes winners"),
  ("UNIT 4 \u00b7 MULTIDIM & HIERARCHY", None),
  ("SPLOM + panel ranking", "multidim/m01_splom_rank.py", "panels are variable PAIRS — and some panels earn their rent"),
  ("PCP axis order", "multidim/m02_pcp_order.py", "axis order is authored adjacency"),
  ("Projection knobs (PCA \u2192 t-SNE)", "multidim/m03_projection_knobs.py", "the perplexity knob: three publishable stories, zero new facts"),
  ("Hierarchy trades + the dendrogram receipt", "multidim/m04_hierarchy.py", "containment vs connection, task by task"),
  ("UNIT 3 \u00b7 BERTIN", None),
  ("Bertin on the A3 sample (needs --data, see prompt)", "unit03_bertin_data.py", "the matrix, permuted by stated criteria — on your own A3 sample"),
]
def main():
    while True:
        print("\n\u2500" * 2 + " CS 8630 \u00b7 classroom demos " + "\u2500" * 30)
        n = 0; idx = {}
        for item in MENU:
            label, path, note = (item + (None,))[:3] if len(item) < 3 else item
            if path is None:
                print(f"\n  {label}")
            else:
                n += 1; idx[n] = (label, path)
                print(f"   {n:2d}. {label}")
                if note: print(f"        \u21b3 {note}")
        choice = input("\n  number to run (q quits, s<N> saves composites): ").strip().lower()
        if choice in ("q", "quit", ""): return
        save = choice.startswith("s")
        try: k = int(choice.lstrip("s"))
        except ValueError: continue
        if k not in idx: continue
        label, path = idx[k]
        args = [sys.executable, os.path.join(HERE, path)]
        if "bertin_data" in path:
            d = input("  path to a3_prs_sample.csv: ").strip()
            if d: args += ["--data", d]
        if save: args += ["--save", os.path.join(HERE, "out")]
        while True:
            print(f"\n  \u25b6 {label}")
            print("     in the window: \u2192/space next \u00b7 \u2190 back \u00b7 home/end \u00b7 q close\n")
            subprocess.run(args, cwd=os.path.dirname(os.path.join(HERE, path)))
            nxt = input("  [Enter]=menu \u00b7 n=next demo \u00b7 r=repeat: ").strip().lower()
            if nxt == "r":
                continue
            if nxt == "n" and (k + 1) in idx:
                k += 1
                label, path = idx[k]
                args = [sys.executable, os.path.join(HERE, path)]
                if save: args += ["--save", os.path.join(HERE, "out")]
                continue
            break
if __name__ == "__main__":
    main()
