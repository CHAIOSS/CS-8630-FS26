**Classroom launcher:** `python run.py` (terminal menu; in-canvas →/← navigation, repeat/next from the prompt) or `jupyter lab ClassRunner.ipynb` (inline built explanations).

# CS 8630 FS2026 — Lecture Demos

One runnable demo per unit, designed to be executed live alongside the unit deck
(each deck's LIVE DEMO slide shows the command and this script's actual output).

    python unit01_perception.py     # interactive class experiment; --save renders slide figures
    python unit02_grammar.py        # grammar ladder, one component per panel
    python unit03_bertin.py         # the level mismatch, felt
    python unit04_multidim.py       # three idioms, one dataset; the projection lie
    python unit05_networks.py       # layout is rhetoric; the seriated matrix
    python unit06_geo.py            # four maps, one dataset (no GIS stack needed)
    python unit07_text.py           # preprocessing is editorial: two pipelines
    python unit08_sciviz.py         # the isovalue is an authored statistic
    python unit09_assessment.py     # the chart-crime gallery (lab reference)
    python unit10_persuasion.py     # the title does the work

Requirements: numpy, pandas, matplotlib, networkx, scikit-learn (all standard).
`--save DIR` renders PNGs headlessly (used to embed real output in the decks).
Style is shared via `_style.py`. Colors match the deck design system.

## Reading-keyed libraries (Week 1 and beyond)

- `cleveland/` — one script per chapter of both Cleveland texts (see its README)
- `franconeri/` — one script per claim of Franconeri et al. 2021, most of them
  interactive class experiments where the room generates the evidence (see its README)
- `grammar/` — one script per section of Wickham 2010 + Wilkinson's core, built on
  plotnine so the code IS the grammar; Altair for the Vega-Lite dialect (see its README)
- `flow/` — Unit 4c Part I: field three ways, the unsteady trap, a LIVE animated wind map
  + sample data (data/) and the assignment starter template
- `fractaltime/` — Unit 4c Part II: coastline/zoom, Hurst & burstiness, the cascade
- `multidim/` — Unit 4: SPLOM+ranking, PCP order, projection knobs, hierarchy trades
  as build-an-explanation canvases (needs scikit-learn, scipy, squarify — see its README)
- `temporal/` — Unit 4b: gaps & banking, many-series & horizon build, period folds, change encodings
- `wilkinson/` — Python examples for every key point of Wilkinson 2005: one script per
  pipeline stage, the varset algebra, and the Ch. 2 pie walk (see its README)

## How to run the demos — what each library expects from you

Three input models, stated per library:

**1. Keypress pacing — `grammar/` and `wilkinson/`.**
You type nothing. One window opens and builds the explanation in place:
the spec grows on the left, the rendering updates on the right, the trail
accumulates below. **Press any key in the figure window** when the room is
ready for the next step (an "any key →" hint sits in the corner). The
window is the clicker; the terminal is not involved. On displays without
a GUI backend the scripts fall back to Enter in the terminal.

**2. Typed responses — the class generates data.**
- `unit01_perception.py`: at each trial, type the class's consensus answer
  as a number (e.g. `60` for "60%") and press Enter.
- `franconeri/f02_ensemble_coding.py`: after each flash, type `u` or `d`
  (the class's call: trend up or down).
- `franconeri/f07_uncertainty_misreads.py`: press Enter after collecting each
  vote; the p-value prints, then the animation runs on its own.
- `franconeri/f06_titles_framing.py`: press Enter after the class finishes
  writing each one-sentence recall.

**3. Timed Enter — the time IS the measurement.**
`franconeri/f01`, `f03`, `f05` and the two-grid moment in `f04`: the clock
starts when the figure appears and stops when you press Enter (the instant
the room finds the target / reaches consensus). Press Enter and nothing
else; the script prints or plots the elapsed seconds.

Everything also runs non-interactively with `--save DIR`, which writes the
figures and asks for no input at all.
