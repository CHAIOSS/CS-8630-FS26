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
    def __init__(self, question, prefix):
        self.question, self.prefix = question, prefix
        self.lines, self.trail, self.n = [], [], 0
        self.saving = "--save" in sys.argv
        if self.saving:
            i = sys.argv.index("--save")
            self.outdir = sys.argv[i + 1] if len(sys.argv) > i + 1 else "."
            os.makedirs(self.outdir, exist_ok=True)
        self.headless = False
        if not self.saving:
            import matplotlib as _mpl
            self.headless = _mpl.get_backend().lower().startswith("agg")
            if self.headless:
                print("  [no display detected: fast-forwarding; use --save DIR to render]")
        self.fig = None

    def _advance(self, last=False):
        """Wait for the presenter. GUI backends: any key/click IN the figure window
        (keeps the event loop alive so the canvas actually repaints). Non-GUI
        fallbacks: Enter in the terminal."""
        if self.headless:
            return
        import matplotlib as _mpl
        backend = _mpl.get_backend().lower()
        gui_ok = self.fig is not None and hasattr(self.fig.canvas, "start_event_loop") \
                 and not backend.startswith(("template", "agg", "pdf", "svg", "ps"))
        if not gui_ok:
            input("  [Enter to finish] " if last else "  [Enter] ")
            return
        while plt.fignum_exists(self.fig.number):
            try:
                r = self.fig.waitforbuttonpress(timeout=-1)
            except Exception:
                break
            if r is not None:      # True = key, False = mouse; either advances
                break

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

    def _layout(self):
        self.fig = plt.figure(figsize=(13.4, 7.2))
        self.fig.canvas.manager.set_window_title(self.prefix) if hasattr(self.fig.canvas, "manager") else None
        gs = self.fig.add_gridspec(2, 2, width_ratios=[0.36, 0.64], height_ratios=[0.78, 0.22],
                                   left=0.02, right=0.99, top=0.90, bottom=0.02, hspace=0.06, wspace=0.03)
        self.ax_code = self.fig.add_subplot(gs[0, 0]); self.ax_code.axis("off")
        self.ax_plot = self.fig.add_subplot(gs[0, 1]); self.ax_plot.axis("off")
        self.ax_trail = self.fig.add_subplot(gs[1, :]); self.ax_trail.axis("off")
        self._hint = self.fig.text(0.99, 0.965, "", ha="right", fontsize=10,
                                   color=MUTED, style="italic")
        self.fig.suptitle(self.question, x=0.02, ha="left", fontsize=15,
                          fontweight="bold", color=INK)

    def _redraw(self, img, note):
        if self.fig is None:
            self._layout()
        self.ax_code.clear(); self.ax_code.axis("off")
        for j, ln in enumerate(self.lines):
            last = j == len(self.lines) - 1
            self.ax_code.text(0.02, 0.96 - j * 0.075, ("▶ " if last else "  ") + ln,
                              transform=self.ax_code.transAxes, family="monospace",
                              fontsize=11.5, va="top",
                              color=ACCENT if last else INK,
                              fontweight="bold" if last else "normal")
        self.ax_plot.clear(); self.ax_plot.axis("off")
        self.ax_plot.imshow(img)
        if note:
            import textwrap
            self.ax_plot.set_title("\n".join(textwrap.wrap(note, 88)), fontsize=11,
                                   style="italic", color=MUTED, loc="left")
        self.ax_trail.clear(); self.ax_trail.axis("off")
        shown = self.trail[-6:]
        for k, (im, lab) in enumerate(shown):
            x0 = 0.005 + k * (1 / 6)
            axi = self.ax_trail.inset_axes([x0, 0.05, (1 / 6) - 0.012, 0.78])
            axi.imshow(im); axi.axis("off")
            axi.set_title(lab, fontsize=8, color=MUTED, pad=2)
        self.fig.canvas.draw_idle()

    def add(self, code_line, plot, note="", name=None):
        """One step: append a spec line, show its rendering. `name` also writes
        the bare plot PNG under out/<name> so the deck figures keep regenerating."""
        self.n += 1
        img = self._rasterize(plot)
        if self.saving and name:
            fig2, ax2 = plt.subplots(figsize=(img.shape[1] / 115, img.shape[0] / 115))
            ax2.imshow(img); ax2.axis("off")
            fig2.savefig(os.path.join(self.outdir, name), dpi=115, bbox_inches="tight", pad_inches=0)
            plt.close(fig2)
            print("saved", os.path.join(self.outdir, name))
        self.lines.append(code_line)
        if not self.saving and not self.headless:
            self._redraw(img, note)
            if getattr(self, "_hint", None): self._hint.set_text("any key \u2192 next")
            plt.pause(0.15)
            self._advance()
        self.trail.append((img, f"{self.n}"))
        if self.saving:
            # keep the composite canvas current for the final export
            self._redraw(img, note) if self.fig or True else None
        return self

    def branch(self, code_line, plot, note="", name=None):
        """A step that REPLACES the last line (an alternative, not an addition)."""
        if self.lines: self.lines.pop()
        return self.add(code_line, plot, note, name)

    def end(self, closing):
        img_note = closing
        if self.saving:
            self._redraw(self.trail[-1][0], img_note)
            path = os.path.join(self.outdir, f"{self.prefix}_explained.png")
            self.fig.savefig(path, dpi=120)
            print("saved", path)
            plt.close(self.fig)
        elif not self.headless:
            self._redraw(self.trail[-1][0], img_note)
            if getattr(self, "_hint", None): self._hint.set_text("any key \u2192 close")
            plt.pause(0.15)
            self._advance(last=True)
            plt.close(self.fig)


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
