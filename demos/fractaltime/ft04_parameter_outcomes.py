"""CONCRETE OUTCOMES — the window picks the headline; the statistic picks the promise.
Run: python ft04_parameter_outcomes.py [--save DIR]"""
from _ft import *

s = fbm(1440, 0.85, 21) * 14 + 60
WINS = [(300, 420, "#1C7248", '"up 31% \u2014 momentum!"'),
        (700, 820, "#B0431F", '"down 24% \u2014 crisis"'),
        (1050, 1170, "#8A6D1C", '"flat \u2014 stability"')]

def full(highlight=None):
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.plot(s, lw=0.8, color=INK)
    for i, (a, bnd, c, _) in enumerate(WINS):
        if highlight is None or i == highlight:
            ax.axvspan(a, bnd, color=c, alpha=0.2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("H = 0.85 \u00b7 NO underlying change", fontsize=9, color=MUTED)
    return fig

def window(i):
    a, bnd, c, msg = WINS[i]
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.plot(s[a:bnd], lw=1.5, color=c)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(msg, fontsize=11, color=c)
    return fig

b = Builder("Act 1: the window IS the outcome", "ft04")
b.add("one persistent series, three candidate 'quarters'", full(), "", "ft04_full.png",
      key="H = 0.85, driftless: everything you are about to see is manufactured by persistence + a window.")
b.add("report(window_1)", window(0), "True.", "ft04_w1.png",
      key="Arithmetically correct. Remember that.")
b.branch("report(window_2)", window(1), "Also true.", "ft04_w2.png",
      key="CONTRAST with the trail: same process, opposite headline. Nothing changed but the window.")
b.branch("report(window_3)", window(2),
      "All three headlines are arithmetically correct; the parameter that chose the outcome "
      "is the WINDOW \u2014 unstated.", "ft04_w3.png",
      key="STORY SWITCH: the window is an authored parameter wearing a calendar's clothes. State it, or show the ladder.")

g = (np.random.default_rng(6).pareto(1.35, 2600) + 1) * 0.3
def promises(gaps, title):
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    sg = np.sort(gaps)
    ax.loglog(sg, 1 - np.arange(len(sg)) / len(sg), lw=1.8, color=INK)
    for v, c, lab in [(np.median(gaps), "#1C7248", "median"), (gaps.mean(), ACCENT, "mean"),
                      (np.quantile(gaps, 0.95), "#8A5A9E", "p95")]:
        ax.axvline(v, color=c, lw=1.6, linestyle="--")
        ax.text(v * 1.1, 0.4, f"{lab} {v:.1f}h", fontsize=9, color=c)
    ax.set_title(title, fontsize=10)
    return fig

b.add("Act 2: promises(bursty_gaps)", promises(g, "heavy tail: the three summaries disagree by 40\u00d7"),
      "Median promises speed; mean describes nobody; p95 is the honest SLA. Picking the "
      "statistic is picking the message.", "ft04_promB.png",
      key="Median promises speed; mean describes nobody; p95 is the promise a storm survivor would recognize. Pick — and say which you picked.")
gE = np.random.default_rng(6).exponential(g.mean(), 2600)
b.branch("promises(exponential_gaps)   # the null", promises(gE, "exponential: the summaries collapse together"),
      "On memoryless data the three summaries agree \u2014 their DIVERGENCE is itself a "
      "burstiness detector you can run in one line.", "ft04_promE.png",
      key="CONTRAST: on memoryless data the three summaries agree. Their DIVERGENCE is a diagnostic — free, one line, never volunteered by a tool.")
b.end("Two authored parameters, two communicated outcomes. The defense is the same both times: "
      "state the parameter, show the ladder/CCDF, or don't publish the number.")
