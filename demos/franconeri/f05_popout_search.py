"""FRANCONERI CLAIM 5 — Pop-out is parallel; conjunction search is serial.
Interactive replication: find the target at three crowd sizes, timed.
Pop-out stays flat with n; conjunction grows. Plot the room's curve.
Run: python f05_popout_search.py [--save DIR]"""
from _franconeri import *

rng = np.random.default_rng()

def array_fig(n, conj, title):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    xs, ys = rng.uniform(0, 10, n), rng.uniform(0, 7, n)
    tx, ty = rng.uniform(1, 9), rng.uniform(1, 6)
    if conj:
        half = n // 2
        ax.scatter(xs[:half], ys[:half], s=70, c=[INK]*half, marker="o")
        ax.scatter(xs[half:], ys[half:], s=70, c=[ACCENT]*(n-half), marker="s")
    else:
        ax.scatter(xs, ys, s=70, c=[INK]*n, marker="o")
    ax.scatter([tx], [ty], s=90, c=[ACCENT], marker="o", zorder=5)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(title, fontsize=11)
    return fig

if "--save" in sys.argv:
    np.random.seed(5); 
    fig = array_fig(80, False, "Pop-out: the vermilion circle, n=80"); finish(fig, "f05_popout.png")
    fig = array_fig(80, True, "Conjunction: the vermilion CIRCLE among vermilion squares and dark circles, n=80")
    finish(fig, "f05_conjunction.png")
else:
    results = {"pop-out": [], "conjunction": []}
    for conj, name in [(False, "pop-out"), (True, "conjunction")]:
        print(f"\n{name.upper()} round — Enter the instant anyone sees the vermilion circle")
        for n in [20, 60, 120]:
            fig = array_fig(n, conj, f"{name}: find the vermilion circle (n={n})")
            plt.show(block=False); plt.pause(0.1)
            results[name].append(timed_enter(f"  n={n}: "))
            plt.close(fig)
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for name, col in [("pop-out", INK), ("conjunction", ACCENT)]:
        ax.plot([20, 60, 120], results[name], "o-", color=col, lw=2, ms=8, label=name)
    ax.set_xlabel("distractors on screen"); ax.set_ylabel("seconds to find")
    ax.legend(); ax.set_title("This room: flat = parallel search, rising = serial")
    plt.show()

claim("Claim 5 — pop-out vs conjunction", [
  "One-channel targets: found in <200 ms regardless of crowd size.",
  "Two-channel targets: item-by-item search; time grows with n.",
  "Every 'find the X that is also Y' dashboard read is the rising line.",
])
