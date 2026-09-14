# Bertin, On Your Own Data — a standalone classroom demo

**CS 8630 · Data Visualization · Unit 3 (Semiology of Graphics).**

One script that runs Bertin's core concepts — selectivity, dissociation,
order, and the reorderable matrix — against the course dataset itself
(`a3_prs_sample.csv`), while deliberately answering **none** of the Assignment 3
question sets. Study it freely: the plane is wasted on purpose (every PR gets
a random position, stated on the canvas), so no trend, distribution, share, or
latency can be read from anything it draws.

## Requirements

Python 3.10+ with `matplotlib`, `numpy`, `pandas` (no other course tooling):

    pip install matplotlib numpy pandas

## Getting the data

Download `a3_prs_sample.csv` from Canvas — the ~12k-row classroom sample (the
same file the AI-use policy permits into hosted tools; even this demo touches
nothing larger). Put it next to the script, or point at it with `--data`.

## Running

    python bertin_demo.py                          # expects ./a3_prs_sample.csv
    python bertin_demo.py --data /path/to/a3_prs_sample.csv
    python bertin_demo.py --save figures/          # headless; writes all PNGs + composite

Interactive mode opens **one window that builds the explanation**: steps
accumulate on the left (current step in vermilion), the rendering on the
right, the history in a trail below. **Press any key in the figure window to
advance** — there is nothing to type.

## What each step shows

1. **Selectivity** — 260 real PRs at random positions, project in **hue**:
   isolating pantsbuild is instantaneous.
2. **(branch)** the same marks with project in **shape**: the same task becomes
   a mark-by-mark tour. Shape is Bertin's one non-selective variable.
3. **Dissociation** — the same marks sized by real `size_lines`: the giant PRs
   seize the read. (Not an A2 answer: no axis carries size, so no
   distribution is displayed — only size's power to dominate.)
4. **Order** — twelve real PRs' `author_association` as swatches, in hue
   (unrankable without the legend) then in value (the ranking is in the ink).
   No counts are shown.
5–6. **The reorderable matrix** — 18 prolific authors (six per project) ×
   8 repos: does author A touch repo R? Shuffled, it's noise; permuted
   (spectral seriation standing in for Bertin's paper strips), the three
   organizations assemble themselves. Permutation is not formatting — it is
   the analysis.

## Why it can't do your homework

Assignment 3's questions live on axes this demo never draws: time, magnitude
scales, shares, latencies. Everything here demonstrates *how variables carry
meaning*, which is the audit vocabulary you need — the questions remain yours.
