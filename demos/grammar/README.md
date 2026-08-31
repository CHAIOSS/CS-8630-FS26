# Grammar of Graphics Demos — CS 8630, Week 2 (Unit 2)

One runnable script per section of Wickham (2010), *A Layered Grammar of
Graphics*, plus the core of Wilkinson's *The Grammar of Graphics*. Built on
**plotnine** (ggplot2's grammar in Python) so the code on screen IS the
grammar, and **Altair** (Vega-Lite) for the machine-interface demo.
Each script opens **one window that builds a visual explanation**: the spec grows line by line on the left (the new word in vermilion), the rendering answers on the right, and a trail of previous steps accumulates along the bottom. **press any key in the figure window to advance** — the window stays live and repaints; the terminal is not involved. `--save DIR` runs headless, writing every step's figure plus a `*_explained.png` composite of the finished canvas.

| Script | Reading | What it shows |
|---|---|---|
| `g01_build_a_plot.py` | Wickham §2 | One chart assembled component by component |
| `g02_layers.py` | Wickham §3.1 | Layers = data+mapping+stat+geom+position; stack/dodge/fill |
| `g03_scales_vs_coords.py` | Wickham §3.2, §6.3 | Scales; scale transform ≠ coord transform (the smoother bends) |
| `g04_coordinates.py` | Wickham §3.3, §6.2 | Stacked bar + polar = pie; bullseye; coord_flip |
| `g05_facets.py` | Wickham §3.4 | Superpose vs facet_wrap vs facet_grid; free vs fixed scales |
| `g06_statistics_binwidth.py` | Wickham §6.1 | Histogram = bar + bin stat; bin sweep; density; quantile plot |
| `g07_defaults.py` | Wickham §4 | The hierarchy of defaults, revealed as explicit code |
| `g08_wilkinson_algebra.py` | Wilkinson | cross / nest / blend, rendered and printed as expressions |
| `g09_chart_types_dissolve.py` | Wilkinson's thesis | Bar→dot→line→area→histogram→pie, one component per step |
| `g10_grammar_as_interface.py` | Synthesis / AI thread | ggplot vs Vega-Lite for one chart + the translation-audit table |

Shared dataset: a constructed per-PR table for four repos over 24 months
(`_grammar.prs()`), shaped like Augur data. Requirements: plotnine, altair,
vl-convert-python, pandas, numpy, matplotlib.
