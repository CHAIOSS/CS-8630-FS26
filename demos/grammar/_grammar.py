"""Shared helpers + dataset for the Grammar of Graphics demos (Unit 2)."""
import sys, os, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _style import *          # INK, ACCENT, TEAL, MUTED, TINT, finish, plt, np
import pandas as pd
try:
    from plotnine import *    # the layered grammar, in Python
    import plotnine
except ImportError:
    raise SystemExit("These demos need plotnine (and statsmodels for smoothers):\n"
                     "    pip install plotnine statsmodels altair vl-convert-python")

PAL = {"augur": INK, "frontend": ACCENT, "docs": TEAL, "cli": "#8A5A9E"}
theme_course = theme_minimal(base_size=11) + theme(
    panel_grid_minor=element_blank(), plot_title=element_text(size=12, weight="bold"),
    strip_text=element_text(weight="bold"))
plotnine.options.figure_size = (8, 4.5)

def prs():
    """Per-PR records for four repos over 24 months: the course dataset."""
    rng = np.random.default_rng(2)
    rows = []
    for repo, base, growth in [("augur", 30, 0.9), ("frontend", 18, 1.4), ("docs", 8, 0.1), ("cli", 12, 0.6)]:
        for m in range(24):
            n = max(2, int(base + growth * m + 6 * np.sin(m / 2.5) + rng.normal(0, 3)))
            for _ in range(n):
                size = rng.lognormal(4, 1)                       # lines changed
                lat = np.exp(0.9 + 0.35 * np.log(size) + rng.normal(0, .5))  # review hours
                rows.append(dict(repo=repo, month=m, lines=size, hours=lat,
                                 kind=rng.choice(["feature", "fix", "docs"], p=[.4, .45, .15])))
    return pd.DataFrame(rows)

def monthly(df):
    return df.groupby(["repo", "month"], as_index=False).size().rename(columns={"size": "prs"})

def _display(fig, name):
    """--save: write PNG. Interactive: close only PREVIOUS windows, then show
    this one non-blocking — Enter (see step) is the only control."""
    if "--save" in sys.argv:
        finish(fig, name)
        return
    import matplotlib
    if matplotlib.get_backend().lower().startswith("agg"):
        print(f"  [no display detected — running headless; use `--save DIR` to write {name}]")
        plt.close(fig)
        return
    for num in plt.get_fignums():           # close earlier figures, keep this one
        if num != fig.number:
            plt.close(num)
    fig.show()
    plt.pause(0.25)

def show(p, name):
    """Render a plotnine plot: interactive window, or --save."""
    fig = p.draw()
    _display(fig, name)

def step(msg):
    """Interactive pacing: pause between grammar steps."""
    if "--save" not in sys.argv:
        input(f"  ▶ {msg}  [Enter] ")

def say(title, points):
    print(f"\n=== {title} ===")
    for pt in points: print("  •", pt)
    if "--save" not in sys.argv:
        input("\n  [Enter to close the last figure and finish] ")
        plt.close("all")

def annot(ax, xy, text, dxy=(0.9, 0.7), color=None, fs=9.5):
    """Arrowed callout for in-figure annotation."""
    c = color or ACCENT
    ax.annotate(text, xy=xy, xytext=(xy[0] + dxy[0], xy[1] + dxy[1]),
                fontsize=fs, color=c, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=c, lw=1.6),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=c, lw=1.0, alpha=0.92))


def polar_fallback(values, labels, theta, title, name, colors=None):
    """plotnine has no coord_polar (an embedding gap — Wickham §5). Render the
    polar step with matplotlib and print the ggplot2 spec that would do it."""
    print(f"    (plotnine lacks coord_polar; in ggplot2 this is `+ coord_polar(theta='{theta}')`)")
    colors = colors or [INK, ACCENT, TEAL, "#8FA6B2", "#C9D2D8", "#8A5A9E"] * 5
    fig, ax = plt.subplots(figsize=(5.5, 5))
    if theta == "y":                      # stacked bar wrapped around: the pie
        ax.pie(values, labels=labels, colors=colors[:len(values)], startangle=90, counterclock=False)
    else:                                 # x wrapped: the bullseye (concentric rings)
        tot = sum(values); r = 1.0
        for v, lab, c in zip(values[::-1], labels[::-1], colors[:len(values)][::-1]):
            ax.add_patch(plt.Circle((0, 0), r, color=c))
            ax.text(0, r - 0.02, lab, ha="center", va="top", fontsize=8, color="white")
            r -= v / tot
        ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05); ax.set_aspect(1); ax.axis("off")
    ax.set_title(title, fontsize=11)
    _display(fig, name)


# ---------------------------------------------------------------------------
# Builder: one persistent canvas. Spec grows on the left (new line vermilion),
# rendering updates on the right, trail of prior steps below. The script IS
# the visual explanation; Enter advances.
# ---------------------------------------------------------------------------
import io
from matplotlib.image import imread as _imread

class Builder:
    """Collect-then-present canvas. Demo scripts call add/branch/end exactly as
    before; nothing renders until end(), which opens ONE navigable window:
      \u2192 / space / click / n ... forward        \u2190 / backspace / p ... back
      home / end ....................... jump      q / escape ........ close
    --save DIR still writes per-step PNGs + the final composite, headless."""

    def __init__(self, question, prefix):
        self.question, self.prefix = question, prefix
        self.lines, self.steps, self.n = [], [], 0
        self.closing, self.closing_key = "", None
        self.saving = "--save" in sys.argv
        if self.saving:
            i = sys.argv.index("--save")
            self.outdir = sys.argv[i + 1] if len(sys.argv) > i + 1 else "."
            os.makedirs(self.outdir, exist_ok=True)
        self.headless = False
        if not self.saving:
            import matplotlib as _mpl
            self.headless = _mpl.get_backend().lower().startswith(("agg", "template", "pdf", "svg", "ps"))
            if self.headless:
                print("  [no display detected: printing the walkthrough; use --save DIR to render]")
        self.fig = None

    # ---------- collection ----------
    def _rasterize(self, p):
        """plotnine ggplot | mpl Figure | png path -> image array."""
        if isinstance(p, str):
            return _imread(p)
        fig = p.draw() if hasattr(p, "draw") and not hasattr(p, "savefig") else p
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=115, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        return _imread(buf)

    def add(self, code_line, plot, note="", name=None, key=None):
        """One step: append a spec line, store its rendering. `name` also writes
        the bare plot PNG under out/<n> so the deck figures keep regenerating."""
        self.n += 1
        img = self._rasterize(plot)
        if self.saving and name:
            fig2, ax2 = plt.subplots(figsize=(img.shape[1] / 115, img.shape[0] / 115))
            ax2.imshow(img); ax2.axis("off")
            fig2.savefig(os.path.join(self.outdir, name), dpi=115, bbox_inches="tight", pad_inches=0)
            plt.close(fig2)
            print("saved", os.path.join(self.outdir, name))
        self.lines.append(code_line)
        self.steps.append(dict(img=img, lines=list(self.lines), note=note, key=key, n=self.n))
        if self.headless and not self.saving:
            print(f"  step {self.n}: {code_line}")
            if note: print(f"          {note}")
            if key:  print(f"        \u2691 {key}")
        return self

    def branch(self, code_line, plot, note="", name=None, key=None):
        """A step that REPLACES the last line (an alternative, not an addition)."""
        if self.lines: self.lines.pop()
        return self.add(code_line, plot, note, name, key)

    # ---------- presentation ----------
    def _layout(self):
        self.fig = plt.figure(figsize=(13.4, 7.2))
        if hasattr(self.fig.canvas, "manager"):
            try: self.fig.canvas.manager.set_window_title(self.prefix)
            except Exception: pass
        gs = self.fig.add_gridspec(2, 2, width_ratios=[0.36, 0.64], height_ratios=[0.78, 0.22],
                                   left=0.02, right=0.99, top=0.90, bottom=0.02, hspace=0.06, wspace=0.03)
        self.ax_code = self.fig.add_subplot(gs[0, 0]); self.ax_code.axis("off")
        self.ax_plot = self.fig.add_subplot(gs[0, 1]); self.ax_plot.axis("off")
        self.ax_trail = self.fig.add_subplot(gs[1, :]); self.ax_trail.axis("off")
        self._hint = self.fig.text(0.99, 0.965, "", ha="right", fontsize=10,
                                   color=MUTED, style="italic")
        self.fig.suptitle(self.question, x=0.02, ha="left", fontsize=15,
                          fontweight="bold", color=INK)

    def _render(self, i):
        """Draw state i. i == len(steps) is the closing view (last figure + closing text)."""
        if self.fig is None:
            self._layout()
        last_i = len(self.steps)
        closing_view = (i == last_i)
        st = self.steps[min(i, last_i - 1)]
        note = self.closing if closing_view else st["note"]
        key = (self.closing_key or st["key"]) if closing_view else st["key"]
        self.ax_code.clear(); self.ax_code.axis("off")
        for j, ln in enumerate(st["lines"]):
            cur = (j == len(st["lines"]) - 1) and not closing_view
            self.ax_code.text(0.02, 0.96 - j * 0.075, ("\u25b6 " if cur else "  ") + ln,
                              transform=self.ax_code.transAxes, family="monospace",
                              fontsize=11.5, va="top",
                              color=ACCENT if cur else INK,
                              fontweight="bold" if cur else "normal")
        self.ax_plot.clear(); self.ax_plot.axis("off")
        self.ax_plot.imshow(st["img"])
        if note:
            import textwrap
            self.ax_plot.set_title("\n".join(textwrap.wrap(note, 88)), fontsize=11,
                                   style="italic", color=MUTED, loc="left")
        if key:
            import textwrap as _tw
            self.ax_plot.text(0.0, -0.03, "\u2691 KEY POINT  " + "\n".join(_tw.wrap(key, 92)),
                              transform=self.ax_plot.transAxes, fontsize=9.8, va="top",
                              fontweight="bold", color="white",
                              bbox=dict(boxstyle="round,pad=0.45", fc=ACCENT, ec="none"))
        self.ax_trail.clear(); self.ax_trail.axis("off")
        upto = self.steps[:min(i, last_i - 1) + 1]
        shown = upto[-6:]
        for k, stp in enumerate(shown):
            x0 = 0.005 + k * (1 / 6)
            axi = self.ax_trail.inset_axes([x0, 0.05, (1 / 6) - 0.012, 0.78])
            axi.imshow(stp["img"]); axi.axis("off")
            cur = stp is upto[-1]
            axi.set_title(str(stp["n"]), fontsize=8,
                          color=ACCENT if cur else MUTED, pad=2,
                          fontweight="bold" if cur else "normal")
            if cur:
                for sp in axi.spines.values(): pass
                axi.axis("on"); axi.set_xticks([]); axi.set_yticks([])
                for sp in axi.spines.values():
                    sp.set_edgecolor(ACCENT); sp.set_linewidth(2)
        pos = "closing" if closing_view else f"step {st['n']}/{last_i}"
        self._hint.set_text(f"{pos}   \u2190 back \u00b7 \u2192/space next \u00b7 home/end jump \u00b7 q close")
        self.fig.canvas.draw_idle()

    def _navigate(self):
        i = 0
        last = len(self.steps)           # index `last` = closing view
        pending = {"k": None}
        def on_key(ev):  pending["k"] = ev.key or ""
        def on_click(ev): pending["k"] = "right"
        self._render(i)
        cid1 = self.fig.canvas.mpl_connect("key_press_event", on_key)
        cid2 = self.fig.canvas.mpl_connect("button_press_event", on_click)
        try: plt.show(block=False)
        except Exception: pass
        while True:
            pending["k"] = None
            while pending["k"] is None:
                if not plt.fignum_exists(self.fig.number): return
                plt.pause(0.06)
            k = pending["k"]
            if k in ("q", "escape"): break
            elif k in ("right", " ", "space", "enter", "return", "n", "down"):
                if i >= last: break
                i += 1; self._render(i)
            elif k in ("left", "backspace", "up", "p"):
                i = max(0, i - 1); self._render(i)
            elif k == "home":
                i = 0; self._render(i)
            elif k == "end":
                i = last; self._render(i)
        plt.close(self.fig)

    def end(self, closing, key=None):
        self.closing, self.closing_key = closing, key
        if not self.steps:
            return
        if self.saving:
            self._render(len(self.steps))
            path = os.path.join(self.outdir, f"{self.prefix}_explained.png")
            self.fig.savefig(path, dpi=120)
            print("saved", path)
            plt.close(self.fig)
        elif self.headless:
            print(f"  close: {closing}")
        else:
            self._navigate()


def polar_figure(values, labels, theta, colors=None):
    """Polar-coordinate render (plotnine lacks coord_polar) returned as a Figure."""
    colors = colors or [INK, ACCENT, TEAL, "#8FA6B2", "#C9D2D8", "#8A5A9E"] * 5
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    if theta == "y":
        ax.pie(values, labels=labels, colors=colors[:len(values)], startangle=90, counterclock=False)
    else:
        tot = sum(values); r = 1.0
        for v, lab, c in zip(values[::-1], labels[::-1], colors[:len(values)][::-1]):
            ax.add_patch(plt.Circle((0, 0), r, color=c))
            ax.text(0, r - 0.02, lab, ha="center", va="top", fontsize=8, color="white")
            r -= v / tot
        ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05); ax.set_aspect(1); ax.axis("off")
    return fig
