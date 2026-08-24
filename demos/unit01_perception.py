"""CS 8630 Unit 1 demo — Cleveland-McGill, replicated on the room.

RUN OF SHOW (interactive mode: `python unit01_perception.py`):
  1. BAR round: 5 trials. Each shows 5 bars; the two DOTTED bars are the pair.
     The class shouts a consensus answer to one question:
        "the smaller dotted value is what percent of the larger?"
     You type the number (e.g. 60). Next trial appears.
  2. PIE round: same 5 true ratios, same question, highlighted slices.
  3. The error plot renders: the class's own judgments, bars vs pies,
     scored with Cleveland & McGill's published error measure. Bars should
     sit visibly lower. That gap is the hierarchy, measured on this room.

`--save DIR` renders the slide figures headlessly (simulated results,
clearly marked as such in the code below).

Faithful to Cleveland & McGill (1984):
  - the judged pair is explicitly MARKED (dots), and its true ratio is
    controlled per trial from a fixed ladder, as in the original;
  - error = log2(|judged% - true%| + 1/8), their published measure.
"""
import sys, random
from _style import *

# True percentages (smaller/larger * 100), a ladder like the original study's.
RATIO_LADDER = [25, 35, 50, 67, 80]

def make_stimulus(true_pct):
    """Five values; positions 'a' and 'b' are the judged pair with the
    controlled ratio. Returns (values, a, b)."""
    larger = random.uniform(30, 55)
    smaller = larger * true_pct / 100
    distractors = [random.uniform(10, 60) for _ in range(3)]
    vals = [larger, smaller] + distractors
    order = list(range(5)); random.shuffle(order)
    shuffled = [vals[i] for i in order]
    a, b = order.index(0), order.index(1)     # where the pair landed
    return shuffled, a, b

def render(vals, a, b, kind, ax, label):
    colors = [ACCENT if i in (a, b) else INK for i in range(5)]
    if kind == "bar":
        ax.bar(range(5), vals, color=colors)
        for i in (a, b):                       # C&M marked the pair with dots
            ax.plot(i, vals[i] + 2.5, "o", color=ACCENT, ms=8)
        ax.set_ylim(0, 70); ax.set_xticks([]); ax.set_yticks([])
    else:
        _, texts = ax.pie(vals, colors=colors, startangle=90,
                          explode=[0.06 if i in (a, b) else 0 for i in range(5)])
    ax.set_title(f"{label}: smaller dotted ÷ larger dotted = ?%", fontsize=11)

def cm_error(judged_pct, true_pct):
    """Cleveland & McGill's log-absolute-error measure."""
    return np.log2(abs(judged_pct - true_pct) + 1/8)

def experiment():
    results = []          # (encoding, true_pct, judged_pct)
    for kind in ("bar", "pie"):
        ladder = RATIO_LADDER[:]; random.shuffle(ladder)
        print(f"\n=== {kind.upper()} round: {len(ladder)} trials ===")
        print('Ask the room: "the smaller marked value is what percent of the larger?"')
        for t, true_pct in enumerate(ladder, 1):
            vals, a, b = make_stimulus(true_pct)
            fig, ax = plt.subplots(figsize=(5.5, 4.2))
            render(vals, a, b, kind, ax, f"Trial {t}")
            plt.show(block=False); plt.pause(0.1)
            judged = float(input(f"  trial {t} — class consensus %: "))
            plt.close(fig)
            results.append((kind, true_pct, judged))
    return results

def error_plot(results):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for i, kind in enumerate(("bar", "pie")):
        errs = [cm_error(j, t) for k, t, j in results if k == kind]
        x = np.random.normal(i, 0.04, len(errs))
        ax.scatter(x, errs, s=70, color=INK if kind == "bar" else ACCENT, zorder=3)
        ax.hlines(np.mean(errs), i - .2, i + .2, color=MUTED, lw=2)
    ax.set_xticks([0, 1], ["Bars (position)", "Pie (angle)"])
    ax.set_ylabel("log2(|judged% − true%| + 1/8)\nCleveland–McGill 1984 error measure")
    ax.set_title("This room's judgment error, by encoding")
    fig.tight_layout()
    finish(fig, "unit01_error.png")

if __name__ == "__main__":
    if "--save" in sys.argv:
        random.seed(8630); np.random.seed(8630)
        vals, a, b = make_stimulus(50)
        fig, axes = plt.subplots(1, 2, figsize=(9, 4))
        render(vals, a, b, "bar", axes[0], "Bars")
        render(vals, a, b, "pie", axes[1], "Pie")
        fig.suptitle("The question, both encodings: smaller marked ÷ larger marked = ?%", fontsize=12)
        finish(fig, "unit01_stimulus.png")
        # SIMULATED results for the slide figure only (shaped like the
        # literature: bar errors ~2-4 pct points, pie errors ~5-12).
        sim = [("bar", t, t + np.random.normal(0, 3)) for t in np.random.choice(RATIO_LADDER, 14)]
        sim += [("pie", t, t + np.random.normal(0, 8)) for t in np.random.choice(RATIO_LADDER, 14)]
        error_plot(sim)
    else:
        error_plot(experiment())
