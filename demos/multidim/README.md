# Unit 4 demos — multidimensional & hierarchical data

Four build-an-explanation canvases (any key in the figure window advances;
`--save DIR` runs headless). Extra deps beyond the course base:

    pip install scikit-learn scipy squarify

| Script | Key concepts |
|---|---|
| `m01_splom_rank.py` | Juxtapose: one honest pair → the full SPLOM → panels ranked by a stated measure (mini-scagnostics) |
| `m02_pcp_order.py` | Fuse: PCP built axis by axis; ensemble bands; the order swap that deletes a correlation |
| `m03_projection_knobs.py` | Project: PCA + its variance confession; t-SNE at perplexity 5 → 30 → 100 on identical rows |
| `m04_hierarchy.py` | Node-link vs icicle vs treemaps (both variants); the shuffled matrix growing a dendrogram receipt |

Each ends on the unit's discipline: orderings and projections are authored —
state the criterion, the parameters, and the seed.
