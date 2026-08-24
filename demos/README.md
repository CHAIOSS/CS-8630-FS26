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

## Unit 1
`make_stimulus` returns the positions of the controlled pair, and render marks exactly that pair — dots above the two bars (as Cleveland & McGill did) and exploded slices in the pie — so the ratio you constructed is the ratio the room judges. The true percentages come from a fixed five-step ladder (25, 35, 50, 67, 80), shuffled per round, instead of random uncontrolled ratios. And the error metric is now their actual published measure, log2(|judged% − true%| + ⅛), labeled as such on the plot.

In class it runs exactly as the docstring says: bar round of five trials, one shouted consensus percentage typed in per trial, then the pie round on the same five true ratios, then the error plot appears with the room's own judgments — bars clustered low, pies scattered high. Ten minutes, and the hierarchy stops being a claim from 1984 and becomes something the class did to itself. The same-ratios-both-rounds design also gives you a clean talking point: any bar-vs-pie gap can't be blamed on harder trials.
