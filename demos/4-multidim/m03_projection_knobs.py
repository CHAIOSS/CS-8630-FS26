"""PROJECT — PCA's confession, then t-SNE's knob, turned live.
Run: python m03_projection_knobs.py [--save DIR]"""
from _md import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

small = sub.sample(350, random_state=2)
Xs = StandardScaler().fit_transform(small[DIMS])

def pca_fig():
    p = PCA(4).fit(Xs); P = p.transform(Xs)
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.5), gridspec_kw={"width_ratios": [2.2, 1]})
    for r, c in PAL4.items():
        m = (small.repo == r).values
        axes[0].scatter(P[m, 0], P[m, 1], s=9, alpha=.6, color=c)
    axes[0].set_xticks([]); axes[0].set_yticks([]); axes[0].set_xlabel("PC1"); axes[0].set_ylabel("PC2")
    axes[1].bar(range(1, 5), p.explained_variance_ratio_, color=[ACCENT, INK, INK, INK])
    axes[1].set_title("variance kept", fontsize=9); axes[1].set_xticks(range(1, 5))
    fig.tight_layout(); return fig

def tsne_fig(perp):
    T = TSNE(perplexity=perp, random_state=0, init="pca").fit_transform(Xs)
    fig, ax = plt.subplots(figsize=(5.4, 4.2))
    for r, c in PAL4.items():
        m = (small.repo == r).values
        ax.scatter(T[m, 0], T[m, 1], s=10, alpha=.65, color=c)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"t-SNE \u00b7 perplexity {perp} \u00b7 seed 0 \u00b7 n {len(small)}", fontsize=9.5, color=MUTED, loc="left")
    fig.tight_layout(); return fig

b = Builder("Two synthetic dimensions: what survives the flattening?", "m03")
b.add("PCA(4 dims) \u2192 PC1 \u00d7 PC2  + variance bar", pca_fig(),
      "Linear, deterministic, axes printable, and the bar CONFESSES how much spread survived. "
      "The least seductive projection \u2014 which is its virtue.", "m03_pca.png")
b.add("TSNE(perplexity=5)", tsne_fig(5),
      "The same 350 PRs. An archipelago of tiny 'clusters'.", "m03_p5.png")
b.branch("TSNE(perplexity=30)", tsne_fig(30),
      "Same rows, same seed \u2014 different story: a few moderate groups.", "m03_p30.png")
b.branch("TSNE(perplexity=100)", tsne_fig(100),
      "One continent. Three publishable pictures, one dataset, zero new information: the "
      "hyperparameter co-authored every 'finding'.", "m03_p100.png")
b.end("The license: grouping structure \u2014 maybe. Distances, densities, axes \u2014 no. "
      "And the caption owes method + parameters + seed, always.")
