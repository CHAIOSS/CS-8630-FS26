"""FRANCONERI CLAIM 7 — Uncertainty displays are systematically misread;
distributional displays (and animated draws) calibrate better.
Interactive: the class votes significant/not on three error-bar pairs
(they'll get the overlap case wrong), then watches a hypothetical
outcome plot (HOP) animate. Run: python f07_uncertainty_misreads.py [--save DIR]"""
from _franconeri import *
from scipy import stats

CASES = [  # (mean1, mean2, se, label)
    (64, 71, 2.65, "A"),   # 95% CIs overlap, p ~= .01  <- the trap
    (64, 71, 4.6,  "B"),   # CIs overlap, p ~= .13
    (64, 74, 2.65, "C"),   # clear gap
]

def bars_fig(m1, m2, se, label):
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    ax.errorbar(["control", "treatment"], [m1, m2], yerr=1.96*se, fmt="o", ms=9,
                color=INK, capsize=5, elinewidth=2)
    ax.set_ylim(50, 85); ax.set_title(f"Case {label}: significantly different? VOTE", fontsize=11)
    return fig

def pval(m1, m2, se):
    z = abs(m2 - m1) / (se * np.sqrt(2)); return 2 * (1 - stats.norm.cdf(z))

if "--save" in sys.argv:
    m1, m2, se, _ = CASES[0]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8))
    axes[0].errorbar(["control", "treatment"], [m1, m2], yerr=1.96*se, fmt="o", ms=9,
                     color=INK, capsize=5, elinewidth=2)
    axes[0].set_ylim(50, 85)
    axes[0].set_title(f"95% CIs overlap — yet p = {pval(m1,m2,se):.3f}\nOverlap ≠ not significant", fontsize=10)
    x = np.linspace(50, 85, 300)
    for mu, col in [(m1, INK), (m2, ACCENT)]:
        axes[1].fill_between(x, 0, np.exp(-(x-mu)**2/(2*se**2)), color=col, alpha=.4)
    axes[1].set_yticks([]); axes[1].set_title("The distributions themselves:\nseparation is visible as shape", fontsize=10)
    fig.suptitle("Error bars are misread; distributions calibrate (claim 7)", fontsize=12)
    fig.tight_layout(); finish(fig, "f07_uncertainty.png")
else:
    for m1, m2, se, lab in CASES:
        fig = bars_fig(m1, m2, se, lab)
        plt.show(block=False); plt.pause(0.1)
        input(f"  Case {lab}: collect the vote, Enter to reveal: ")
        print(f"    p = {pval(m1, m2, se):.3f}")
        plt.close(fig)
    print("\n  Case A is the trap: overlapping 95% CIs, p≈.01. Now the HOP —")
    rng = np.random.default_rng()
    m1, m2, se, _ = CASES[0]
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    plt.show(block=False)
    for _ in range(25):                     # hypothetical outcome plot
        ax.clear()
        ax.plot(["control", "treatment"], [rng.normal(m1, se), rng.normal(m2, se)],
                "o-", color=ACCENT, ms=10, lw=2)
        ax.set_ylim(50, 85); ax.set_title("HOP: draws from the distributions —\ncount how often treatment wins")
        plt.pause(0.35)
    plt.close(fig)
    print("  Treatment won nearly every draw — uncertainty experienced, not decoded.")

claim("Claim 7 — uncertainty misreads", [
  "The overlap fallacy: touching 95% CIs read as 'no difference' — wrong.",
  "Bars binarize continuous uncertainty; distributions and HOPs calibrate readers better.",
])
