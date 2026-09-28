"""CHANGE — levels vs growth vs rates; the window; the connected scatter.
Run: python tp04_change.py [--save DIR]"""
from _t import *

four = {r: SERIES[r] for r in ["augur", "frontend", "docs", "cli"]}

def lines(transform, title):
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    for r, v in four.items():
        ax.plot(t, transform(v), lw=1.5, color=PAL4[r])
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=10)
    fig.tight_layout(); return fig

def logplot():
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    for r, v in four.items():
        ax.semilogy(t, v, lw=1.5, color=PAL4[r])
    ax.set_xticks([]); ax.set_title("log scale: equal slopes = equal RATES", fontsize=10)
    fig.tight_layout(); return fig

def smooth(w):
    noisy = base + np.random.default_rng(3).normal(0, 3, 36)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.plot(t, noisy, lw=0.8, color="#C9D2D8")
    ax.plot(t, pd.Series(noisy).rolling(w, center=True).mean(), lw=2, color=ACCENT)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"rolling window = {w} months", fontsize=10)
    fig.tight_layout(); return fig

def connected():
    va = pd.Series(four["frontend"]).rolling(3, center=True).mean().bfill().ffill()
    vb = pd.Series(four["docs"]).rolling(3, center=True).mean().bfill().ffill()
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    ax.plot(va, vb, lw=1.6, color=INK)
    for k in range(0, 36, 6):
        ax.annotate("", xy=(va[min(k+1, 35)], vb[min(k+1, 35)]), xytext=(va[k], vb[k]),
                    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.4))
        ax.text(va[k], vb[k], f"m{k}", fontsize=7, color=MUTED)
    ax.set_xlabel("frontend"); ax.set_ylabel("docs"); ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); return fig

b = Builder("Level, growth, rate \u2014 and two derived-change idioms", "tp04")
b.add("plot raw levels", lines(lambda v: v, "raw: big series bury small ones' growth"),
      "", "tp04_raw.png")
b.add("index each to 100 at t\u2080", lines(lambda v: 100 * v / v[0], "indexed at month 0: pure growth"),
      "Levels erased ON PURPOSE. The baseline is a claim:", "tp04_idx0.png")
b.branch("\u2192 index at month 12 instead", lines(lambda v: 100 * v / v[12], "same data, baseline month 12"),
      "Different winners. An index without its stated baseline is an argument in costume.", "tp04_idx12.png")
b.branch("\u2192 or keep levels: log scale", logplot(),
      "Equal slopes = equal rates; levels retained, compressed.", "tp04_log.png")
b.add("rolling(3).mean()", smooth(3), "Seasonality survives.", "tp04_w3.png")
b.branch("rolling(9).mean()", smooth(9),
      "Only trend \u2014 the spike you cared about is gone. The window is the bins lesson with a clock.", "tp04_w9.png")
b.add("connected scatter: docs vs frontend, time IN the path", connected(),
      "Elegant \u2014 and measured (Haroz, Kosara & Franconeri 2016) to be misread without heavy guides: "
      "readers see the line's SHAPE, not the temporal story. Presentation tool; handle with arrows.", "tp04_conn.png")
b.end("Four disclosures every temporal chart owes its caption: gap treatment, granularity, window, "
      "index baseline. Generated or handmade \u2014 same debt.")
