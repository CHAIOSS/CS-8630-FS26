"""CS 8630 Unit 5 demo — layout is rhetoric; the matrix never occludes.
Same graph: two force layouts (different seeds), one seriated matrix.
Run: python unit05_networks.py [--save DIR]"""
from _style import *
import networkx as nx

rng = np.random.default_rng(5)
G = nx.connected_caveman_graph(3, 6)          # 3 communities of 6
# sprinkle bridges
G.add_edges_from([(2, 7), (8, 13), (14, 3)])

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4))
for ax, seed in zip(axes[:2], (1, 7)):
    pos = nx.spring_layout(G, seed=seed)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#9FB2BD", width=1)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=90, node_color=INK)
    nx.draw_networkx_nodes(G, pos, nodelist=[2, 8, 14], ax=ax, node_size=110, node_color=ACCENT)
    ax.set_title(f"Force layout, seed={seed}\nsame graph, different story", fontsize=10)
    ax.axis("off")
order = list(nx.utils.cuthill_mckee_ordering(G))   # seriation
A = nx.to_numpy_array(G)[np.ix_(order, order)]
axes[2].imshow(A, cmap="Greys", interpolation="nearest")
axes[2].set_title("Adjacency matrix, seriated\nno occlusion at any density", fontsize=10)
axes[2].set_xticks([]); axes[2].set_yticks([])
fig.suptitle("Bridge contributors (vermilion) — which rendering earns your trust?", fontsize=12)
fig.tight_layout()
finish(fig, "unit05_layouts.png")
