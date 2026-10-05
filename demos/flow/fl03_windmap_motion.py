"""FLOW — a live wind map in a window, plus the one-mover pop-out.
Interactive: real animation (close window to continue). --save DIR: frame strips.
Run: python fl03_windmap_motion.py [--save DIR]"""
from _fl import *
import matplotlib
import matplotlib.animation as anim

saving = "--save" in sys.argv
outdir = sys.argv[sys.argv.index("--save") + 1] if saving and len(sys.argv) > sys.argv.index("--save") + 1 else "."
headless = saving or matplotlib.get_backend().lower().startswith("agg")
os.makedirs(outdir, exist_ok=True)

# --- Act 1: the wind map ---
trails = advect(n=800, steps=140, unsteady=True)
def draw_frame(ax, k):
    ax.set_facecolor("#101820")
    for i in range(0, 800, 2):
        xs = [trails[j][0][i] for j in range(max(0, k - 9), k)]
        ys = [trails[j][1][i] for j in range(max(0, k - 9), k)]
        if xs and max(xs) - min(xs) < 3:
            ax.plot(xs, ys, lw=0.55, color="#CFE8F3", alpha=0.75)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 10); ax.set_ylim(0, 6.4)

if headless:
    fig, axes = plt.subplots(1, 5, figsize=(13, 2.6))
    for fi, ax in enumerate(axes): draw_frame(ax, 20 + fi * 28); ax.set_title(f"t={fi}", fontsize=8)
    fig.suptitle("the wind map, five frames (run without --save for the live version)")
    fig.savefig(os.path.join(outdir, "fl03_windframes.png"), dpi=130, bbox_inches="tight")
    print("saved", os.path.join(outdir, "fl03_windframes.png"))
else:
    fig, ax = plt.subplots(figsize=(9, 5.6))
    fig.suptitle("the wind-map aesthetic: trails are short pathlines  (close to continue)")
    def up(k):
        ax.clear(); draw_frame(ax, 10 + (k % 128))
    a = anim.FuncAnimation(fig, up, interval=60, cache_frame_data=False)
    plt.show()

# --- Act 2: motion pops ---
r = np.random.default_rng(1)
xs0, ys0 = r.uniform(0, 10, 120), r.uniform(0, 6, 120)
if headless:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(xs0, ys0, s=28, color=INK)
    for g in range(8):
        ax.scatter([xs0[17] - 0.55 + g * 0.08], [ys0[17] + 0.3 - g * 0.045], s=28, color=ACCENT, alpha=0.12 + g * 0.11)
    ax.set_xticks([]); ax.set_yticks([]); fig.suptitle("motion pops (multi-exposure stand-in)")
    fig.savefig(os.path.join(outdir, "fl03_popout.png"), dpi=130, bbox_inches="tight")
    print("saved", os.path.join(outdir, "fl03_popout.png"))
else:
    fig, ax = plt.subplots(figsize=(9, 5.4))
    fig.suptitle("120 dots; ONE is moving. You did not have to search.  (close to finish)")
    def up2(k):
        ax.clear()
        ax.scatter(np.delete(xs0, 17), np.delete(ys0, 17), s=28, color=INK)
        ax.scatter([xs0[17] + 0.5 * np.sin(k / 6)], [ys0[17] + 0.3 * np.cos(k / 6)], s=34, color=INK)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(-0.3, 10.3); ax.set_ylim(-0.3, 6.3)
    a2 = anim.FuncAnimation(fig, up2, interval=50, cache_frame_data=False)
    plt.show()
print("fl03 done — the mover is the same colour as everything else; motion alone carried it.")
