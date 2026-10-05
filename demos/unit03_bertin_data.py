"""BERTIN ON YOUR OWN DATA — and deliberately NOT on your assignment.

Runs the Unit 3 concepts against a3_prs_sample.csv (the classroom sample — the
same file your AI tools are allowed to see). By design it answers none of the
Data Guide's Set A/B/C questions: the plane is deliberately WASTED (positions
are random), so nothing here shows a trend, a distribution, a share, or a
latency. What it shows is the retinal variables exercising their powers on
real rows — selectivity, dissociation, order, and the reorderable matrix.

Run:  python unit03_bertin_data.py [--data /path/to/a3_prs_sample.csv] [--save DIR]
      (default data path: ./a3_prs_sample.csv)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "grammar"))
from _grammar import Builder, INK, ACCENT, TEAL, MUTED
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# ---- locate the data ------------------------------------------------------
path = "a3_prs_sample.csv"
if "--data" in sys.argv:
    path = sys.argv[sys.argv.index("--data") + 1]
if not os.path.exists(path):
    raise SystemExit(
        f"Cannot find {path}.\n"
        "Download a3_prs_sample.csv from Canvas (the AI-permitted sample) and either\n"
        "run this script from the same folder or pass --data /path/to/a3_prs_sample.csv")
df = pd.read_csv(path)
rng = np.random.default_rng(8630)
S = df.sample(min(260, len(df)), random_state=8630).reset_index(drop=True)
S["x"], S["y"] = rng.uniform(0, 10, len(S)), rng.uniform(0, 7, len(S))  # the wasted plane
PROJ_HUE = {"pytorch": INK, "moby": ACCENT, "pantsbuild": TEAL}
PROJ_MARK = {"pytorch": "o", "moby": "s", "pantsbuild": "^"}

def cloud_fig(mode):
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    if mode == "hue":
        for pr, c in PROJ_HUE.items():
            m = S.project == pr
            ax.scatter(S.x[m], S.y[m], s=42, color=c)
    elif mode == "shape":
        for pr, mk in PROJ_MARK.items():
            m = S.project == pr
            ax.scatter(S.x[m], S.y[m], s=42, color=INK, marker=mk)
    elif mode == "size":
        sz = 8 + 240 * (S.size_lines / max(S.size_lines.max(), 1))
        ax.scatter(S.x, S.y, s=sz, color=INK, alpha=0.7)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("positions are RANDOM — the plane carries nothing", fontsize=9, color=MUTED)
    return fig

b = Builder("Bertin's powers, on your own PRs — answering none of your questions", "u3data")

b.add("260 real PRs · position = random() · hue = project", cloud_fig("hue"),
      "Find every pantsbuild PR. Done already? That is SELECTIVITY — hue's power, on your data.",
      "u3d_hue.png")

b.branch("same marks · shape = project", cloud_fig("shape"),
      "Now find every pantsbuild PR. Feel the mark-by-mark tour? Shape is Bertin's one "
      "non-selective variable.", "u3d_shape.png")

b.branch("same marks · size = size_lines (real values)", cloud_fig("size"),
      "The whales seize the read: size is DISSOCIATIVE. NOTE: this is not your A2 answer — "
      "no axis carries size here, so no distribution can be read; only size's power to dominate.",
      "u3d_size.png")

# ---- order: association swatches, no counts -------------------------------
def order_fig():
    levels = ["NONE", "CONTRIBUTOR", "COLLABORATOR", "MEMBER"]
    picks = (S[S.author_association.isin(levels)]
             .groupby("author_association").head(3).sample(12, random_state=7, replace=True)
             .author_association.tolist())[:12]
    hues = {"NONE": TEAL, "CONTRIBUTOR": "#C8A24B", "COLLABORATOR": ACCENT, "MEMBER": "#8A5A9E"}
    vals = {"NONE": "0.85", "CONTRIBUTOR": "0.6", "COLLABORATOR": "0.35", "MEMBER": "0.1"}
    fig, axes = plt.subplots(2, 1, figsize=(7.6, 3.2))
    for ax, pal, t in [(axes[0], hues, "hue: rank these 12 PRs by insider-ness — you can't without the legend"),
                       (axes[1], vals, "value: same 12 PRs — the ranking is in the ink")]:
        for i, lv in enumerate(picks):
            ax.add_patch(mpatches.Rectangle((i, 0), 0.92, 1, color=pal[lv]))
        ax.set_xlim(-0.1, 12.1); ax.set_ylim(-0.1, 1.1); ax.axis("off")
        ax.set_title(t, fontsize=9.5, loc="left")
    fig.tight_layout()
    return fig

b.add("12 real PRs · author_association → hue, then value", order_fig(),
      "ORDER: association is ordinal; hue refuses to say so, value cannot help saying so. "
      "(No counts shown — the distribution question is yours, in Set A.)", "u3d_order.png")

# ---- the reorderable matrix: author × repo incidence ----------------------
def matrix_figs():
    # stratify per project: "top authors overall" would all come from pytorch
    # (89% of rows) and collapse the matrix to one org's repos, all cells = 1
    top = pd.Index([a for p in df.project.unique()
                    for a in (df[df.project == p].groupby("author_pseud").size()
                              .sort_values(ascending=False).head(6).index)])
    sub = df[df.author_pseud.isin(top)]
    inc = (sub.groupby(["author_pseud", "repo_name"]).size().unstack(fill_value=0) > 0).astype(int)
    M = inc.to_numpy().astype(float)
    pr_, pc_ = rng.permutation(M.shape[0]), rng.permutation(M.shape[1])
    Ms = M[pr_][:, pc_]
    def spec_order(A):
        Ssim = A @ A.T
        w, v = np.linalg.eigh(Ssim)
        return np.argsort(v[:, -1])
    Mo = Ms[spec_order(Ms)][:, spec_order(Ms.T)]
    figs = []
    for mat, t in [(Ms, "18 prolific authors (6 per project) × 8 repos, arbitrary order:\nwho works where? unreadable"),
                   (Mo, "the SAME cells, rows and columns permuted:\nstructure assembles itself")]:
        fig, ax = plt.subplots(figsize=(5.6, 3.6))
        ax.imshow(mat, cmap="Greys", aspect="auto", vmin=0, vmax=1)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(t, fontsize=9.5)
        figs.append(fig)
    return figs

m1, m2 = matrix_figs()
b.add("matrix: author A touches repo R? (shuffled)", m1,
      "A pure structure question — not in your question sets.", "u3d_matrix_shuffled.png")
b.add("  → permute rows and columns", m2,
      "The blocks that emerge are for YOU to interpret aloud. Permutation is not formatting; "
      "it is the analysis.", "u3d_matrix_sorted.png")

b.end("Selectivity, dissociation, order, permutation — the whole audit toolkit just ran on your "
      "dataset without touching one assignment question. Now aim it at the three you chose.")
