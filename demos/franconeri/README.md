# Franconeri et al. 2021 — Claim Demos (CS 8630, Week 1)

One runnable demo per major claim of *The Science of Visual Data
Communication: What Works*. Most are interactive class experiments —
the room generates the data that proves the claim. `--save DIR` renders
static slide figures instead.

| Script | Claim | In-class moment |
|---|---|---|
| `f01_attention_limits.py` | Vision is a limited-attention channel | Count the 7s, timed, twice |
| `f02_ensemble_coding.py` | Ensemble stats extracted in a glance | Six half-second flashes, class calls the trend |
| `f03_comparison_capacity.py` | Humans compare 2–4 things | Same question at 2/4/8 series, consensus timed |
| `f04_grouping_gestalt.py` | Grouping is pre-attentive; connectedness wins | Pairing vote flips when lines appear |
| `f05_popout_search.py` | Pop-out parallel, conjunction serial | Search times vs crowd size, plotted live |
| `f06_titles_framing.py` | Titles steer takeaway and memory | One-sentence recall under two titles |
| `f07_uncertainty_misreads.py` | Error bars misread; HOPs calibrate | The overlap-fallacy vote + animated draws |
| `f08_geometry_inference.py` | Bars imply groups, lines imply trends | One-sentence readings, two geometries |

Pairs with `../cleveland/` (Part I of the Unit 1 deck); these are Part II.
Requirements: numpy, scipy, matplotlib. Shared style via `_franconeri.py`.
