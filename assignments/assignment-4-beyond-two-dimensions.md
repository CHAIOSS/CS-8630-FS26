# Assignment 4: Beyond Two Dimensions

**Unit:** Multidimensional & Hierarchical Data | **Due:** Friday, Week 6 | **AI Tier 2 + one Tier-1 exercise** | Individual

## Read & Write

Read the assigned Card excerpt (*Information Visualization*) and Bach et al. (2014), *A Review of Temporal Data Visualizations*, plus the Munzner what/why/how chapter used in lecture.

Write a **1,200-word comparative analysis** of three multidimensional idioms — parallel coordinates, scatterplot-matrix (SPLOM), and a dimensionality-reduction projection (PCA/UMAP/t-SNE) — structured by task: for each idiom, which of Munzner's task abstractions it serves well (identify outliers? characterize correlation? find clusters?), what it perceptually costs (crossing clutter, pairwise-only vision, distance distortion), and one published or in-the-wild example where it was the wrong choice. Then a closing section on hierarchies: when does containment (treemap/icicle) beat node-link for a tree, in task terms — not taste terms.

## Build

On one shared dataset (course-provided Augur dependency-freshness extract, or a petitioned alternative with ≥8 quantitative dimensions):

1. A parallel-coordinates plot, a SPLOM, and one projection — same data, consistent color mapping.
2. A treemap **and** an icicle of one genuine hierarchy in the data (e.g., language → repo → package).
3. For all five views: a caption stating the specific task the view serves, and one finding visible in that view that is invisible in at least one of the others. The findings are the point; five views with no cross-view insight is a rendering exercise, not analysis.

**Tier-1 exercise (required, `idiom-advisor-audit.md`):** Describe your dataset and one analytical task to an LLM in plain language and ask it to recommend an idiom, with reasoning. Then judge its recommendation against Munzner: was the task abstraction correct? Was the perceptual reasoning sound, missing, or confabulated? 300–400 words, raw transcript attached.

## AI Instructions

Tier 2 for the builds: scaffolding and debugging logged; every encoding decision you accept from AI needs its perceptual justification in the log. Essay follows the standing prose rule. The advisor audit is Tier 1 — unmodified output, and a *correct* AI recommendation analyzed well scores the same as a flawed one dissected well.

## Grading (100 pts)

Comparative analysis: task-grounded, framework-accurate (35) · hierarchy section (10) · five views correctly built with consistent mappings (25) · cross-view findings in captions (15) · idiom-advisor audit (10) · AI-LOG (5)
