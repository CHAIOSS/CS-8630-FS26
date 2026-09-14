"""BERTIN ON YOUR OWN DATA — standalone classroom demo (CS 8630, Unit 3).

Runs the Unit 3 concepts against a3_prs_sample.csv (the classroom sample — the
same file your AI tools are allowed to see). By design it answers none of the
Data Guide's Set A/B/C questions: the plane is deliberately WASTED (positions
are random), so nothing here shows a trend, a distribution, a share, or a
latency. What it shows is the retinal variables exercising their powers on
real rows — selectivity, dissociation, order, and the reorderable matrix.

Requires only: python 3.10+, matplotlib, numpy, pandas.
Run:  python bertin_demo.py [--data /path/to/a3_prs_sample.csv] [--save DIR]
"""
import sys, os, io
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.image import imread as _imread
import matplotlib.patches as mpatches

INK, ACCENT, TEAL, MUTED = "#2B3A42", "#E4572E", "#1C7293", "#64707A"
plt.rcParams.update({"font.family": "sans-serif", "axes.edgecolor": "#C9D2D8",
                     "axes.linewidth": 0.8, "figure.facecolor": "white"})

class Builder:
    """One persistent canvas: steps accumulate on the left, the current figure
    renders on the right, a trail of previous steps builds along the bottom.
    Press any key IN the figure window to advance. --save DIR runs headless."""
    def __init__(self, question, prefix):
        self.question, self.prefix = question, prefix
        self.lines, self.trail, self.n = [], [], 0
        self.saving = "--save" in sys.argv
        if self.saving:
            i = sys.argv.index("--save")
            self.outdir = sys.argv[i + 1] if len(sys.argv) > i + 1 else "."
            os.makedirs(self.outdir, exist_ok=True)
        self.headless = (not self.saving) and matplotlib.get_backend().lower().startswith("agg")
        if self.headless:
            print("  [no display detected: fast-forwarding; use --save DIR to render]")
        self.fig = None

    def _rasterize(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=115, bbox_inches="tight")
        plt.close(fig); buf.seek(0)
        return _imread(buf)

    def _layout(self):
        self.fig = plt.figure(figsize=(13.4, 7.2))
        gs = self.fig.add_gridspec(2, 2, width_ratios=[0.36, 0.64], height_ratios=[0.78, 0.22],
                                   left=0.02, right=0.99, top=0.90, bottom=0.02, hspace=0.06, wspace=0.03)
        self.ax_code = self.fig.add_subplot(gs[0, 0]); self.ax_code.axis("off")
        self.ax_plot = self.fig.add_subplot(gs[0, 1]); self.ax_plot.axis("off")
        self.ax_trail = self.fig.add_subplot(gs[1, :]); self.ax_trail.axis("off")
        self._hint = self.fig.text(0.99, 0.965, "", ha="right", fontsize=10, color=MUTED, style="italic")
        self.fig.suptitle(self.question, x=0.02, ha="left", fontsize=15, fontweight="bold", color=INK)

    def _redraw(self, img, note):
        if self.fig is None: self._layout()
        self.ax_code.clear(); self.ax_code.axis("off")
        for j, ln in enumerate(self.lines):
            last = j == len(self.lines) - 1
            self.ax_code.text(0.02, 0.96 - j * 0.075, ("▶ " if last else "  ") + ln,
                              transform=self.ax_code.transAxes, family="monospace", fontsize=11.5,
                              va="top", color=ACCENT if last else INK,
                              fontweight="bold" if last else "normal")
        self.ax_plot.clear(); self.ax_plot.axis("off")
        self.ax_plot.imshow(img)
        if note:
            import textwrap
            self.ax_plot.set_title("\n".join(textwrap.wrap(note, 88)), fontsize=11,
                                   style="italic", color=MUTED, loc="left")
        self.ax_trail.clear(); self.ax_trail.axis("off")
        for k, (im, lab) in enumerate(self.trail[-6:]):
            x0 = 0.005 + k * (1 / 6)
            axi = self.ax_trail.inset_axes([x0, 0.05, (1 / 6) - 0.012, 0.78])
            axi.imshow(im); axi.axis("off")
            axi.set_title(lab, fontsize=8, color=MUTED, pad=2)
        self.fig.canvas.draw_idle()

    def _advance(self):
        if self.headless: return
        while plt.fignum_exists(self.fig.number):
            try:
                if self.fig.waitforbuttonpress(timeout=-1) is not None: break
            except Exception: break

    def add(self, code_line, fig, note="", name=None):
        self.n += 1
        img = self._rasterize(fig)
        if self.saving and name:
            f2, a2 = plt.subplots(figsize=(img.shape[1] / 115, img.shape[0] / 115))
            a2.imshow(img); a2.axis("off")
            f2.savefig(os.path.join(self.outdir, name), dpi=115, bbox_inches="tight", pad_inches=0)
            plt.close(f2); print("saved", os.path.join(self.outdir, name))
        self.lines.append(code_line)
        if not self.saving and not self.headless:
            self._redraw(img, note); self._hint.set_text("any key → next")
            plt.pause(0.15); self._advance()
        self.trail.append((img, f"{self.n}"))
        if self.saving: self._redraw(img, note)
        return self

    def branch(self, code_line, fig, note="", name=None):
        if self.lines: self.lines.pop()
        return self.add(code_line, fig, note, name)

    def end(self, closing):
        if self.saving:
            self._redraw(self.trail[-1][0], closing)
            path = os.path.join(self.outdir, f"{self.prefix}_explained.png")
            self.fig.savefig(path, dpi=120); print("saved", path); plt.close(self.fig)
        elif not self.headless:
            self._redraw(self.trail[-1][0], closing)
            self._hint.set_text("any key → close")
            plt.pause(0.15); self._advance(); plt.close(self.fig)


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
