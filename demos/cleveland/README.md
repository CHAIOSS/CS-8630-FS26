# Cleveland Chapter Demos — CS 8630

One runnable script per chapter of Cleveland's two course texts. Each renders
its chapter's key methods as figures and prints the key points to the terminal.
Run interactively in class, or `--save DIR` to render PNGs.

## The Elements of Graphing Data (1994 revised ed.) — Week 2
| Script | Chapter | Key demonstrations |
|---|---|---|
| `elements_ch1_introduction.py` | 1 Introduction | Same statistics, four datasets (quartet) — why we plot |
| `elements_ch2_principles.py` | 2 Principles of Graph Construction | Data stand out; honest scale breaks; log scales; banking to 45° |
| `elements_ch3_methods.py` | 3 Graphical Methods | Dot plots vs bars; loess spans; Tukey mean–difference plot |
| `elements_ch4_perception.py` | 4 Graphical Perception | Elementary-task ordering; the curve-difference illusion |

## Visualizing Data (1993) — Weeks 3–4
| Script | Chapter | Key demonstrations |
|---|---|---|
| `visualizing_ch1_introduction.py` | 1 Introduction | The fit + residual paradigm, iterated to structureless residuals |
| `visualizing_ch2_univariate.py` | 2 Univariate Data | Quantile plots; two-sample & normal q-q; spread–location |
| `visualizing_ch3_bivariate.py` | 3 Bivariate Data | Robust (bisquare) loess; residual-dependence; spread vs x |
| `visualizing_ch4_trivariate.py` | 4 Trivariate Data | The coplot with overlapping shingles; interactions pooled scatters hide |
| `visualizing_ch5_hypervariate.py` | 5 Hypervariate Data | SPLOM + brushing; conditional structure via linked highlighting |
| `visualizing_ch6_multiway.py` | 6 Multiway Data | Median-ordered multiway dot plots; the barley-style anomaly |

Chapter titles follow the 1994 revised *Elements* and 1993 *Visualizing Data*;
if your edition's numbering differs, the scripts are named by topic and easy to remap.

Requirements: numpy, scipy, matplotlib, statsmodels (`pip install statsmodels`).
Shared style: `../_style.py` via `_cleveland.py` (also provides `loess()`).
