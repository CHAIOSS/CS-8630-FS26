# Wilkinson Key-Point Examples — CS 8630, Week 2 (Unit 2, Part II)

Python examples for every key point of *The Grammar of Graphics* (Wilkinson,
2nd ed., 2005 — required Ch. 1, 2, 5; optional Ch. 4, 9), one script per
pipeline stage plus the algebra and the Ch. 2 pie walk. Built on plotnine so
the code is the grammar. Each script is **one evolving canvas**: pipeline stages accumulate on the left, the current rendering on the right, the history in a trail below — the script performs the grammar rather than describing it. **press any key in the figure window to advance.** `--save DIR` runs headless and also writes a `*_explained.png` composite.

| Script | Key point | Reading |
|---|---|---|
| `w01_data.py` | DATA is a slot — specs decouple from datasets | Ch. 1–2 |
| `w02_trans.py` | TRANS: variable transformations run before everything | Ch. 2 |
| `w03_scales.py` | SCALES: the ruler's type is a measurement-level claim | Ch. 2 (Ch. 6) |
| `w04_statistics.py` | STATISTICS are graphing functions inside the spec | Ch. 2 (Ch. 7) |
| `w05_geometry.py` | GEOMETRY: six marks, six assertions about the data | Ch. 2 (Ch. 8) |
| `w06_coordinates.py` | COORDINATES warp finished geometry (polar → pie) | Ch. 9 |
| `w07_aesthetics.py` | AESTHETICS: mapping vs setting (+ the classic bug) | Ch. 2 (Ch. 10) |
| `w08_guides.py` | GUIDES are scales' inverses; annotation is a component | Ch. 2 (Ch. 12) |
| `w09_varsets_algebra.py` | Varsets; cross / nest / blend, printed and rendered | Ch. 4–5 |
| `w10_pie_pipeline.py` | The Ch. 2 walk: the pie born in the final stage | Ch. 2 |

Companions: `../grammar/` covers Wickham 2010 section by section (g08/g09
overlap deliberately with w09/w10 — same ideas, the two books' framings).
