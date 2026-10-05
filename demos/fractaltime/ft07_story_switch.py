"""STORY SWITCH — one event log, two dashboards, six lines apart.
Run: python ft07_story_switch.py [--save DIR]"""
from _ft import *

r = np.random.default_rng(5)
g = (r.pareto(1.3, 4000) + 1) * 0.18
t = np.cumsum(g); t = t[t < 720]
daily, _ = np.histogram(t, bins=30)

def storyX():
    weekly = daily.reshape(6, 5).sum(axis=1)
    sm = np.convolve(weekly, np.ones(3) / 3, mode="same")
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    ax.bar(range(6), sm, color=TEAL, width=0.7)
    ax.plot(range(6), sm, "o-", color=INK, lw=1.5, ms=4)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('"steady, healthy cadence"  (weekly bins, 3-wk smoothing)', fontsize=10)
    return fig

def storyY():
    fig = plt.figure(figsize=(7.0, 3.6))
    axB = fig.add_axes([0.06, 0.45, 0.9, 0.48])
    axB.bar(range(30), daily, color=INK, width=0.8)
    pk = daily.argsort()[-3:]
    axB.bar(pk, daily[pk], color=ACCENT, width=0.8)
    axB.set_xticks([]); axB.set_yticks([])
    share = daily[pk].sum() / daily.sum()
    axB.set_title(f'"it storms" \u2014 daily bins + raw raster \u00b7 {share:.0%} of output in 3 days', fontsize=10)
    axR = fig.add_axes([0.06, 0.1, 0.9, 0.25])
    axR.eventplot(t, colors=ACCENT, linewidths=0.5)
    axR.set_xticks([]); axR.set_yticks([])
    return fig

b = Builder("Think the story first; implement it as parameters", "ft07")
b.add("STORY X: bins=weekly; smooth=3; no raster", storyX(),
      "Nothing in it is false.", "ft07_x.png",
      key="Story X's parameters: weekly bins, 3-week smoothing, no raw layer. Write them down — they ARE the story.")
b.branch("STORY Y: bins=daily; smooth=OFF; + eventplot(raw)", storyY(),
      "Nothing in this one is false either. The delta is six lines: bin width, smoothing "
      "window, one raster. Shipping ONE while knowing the other is the editorial act.", "ft07_y.png",
      key="CONTRAST with the trail: six lines of code apart, both true. The delta is pure authorship — bin width, smoothing, one raster.")
b.add("the SAME data, honestly disclosed either way", storyX(),
      "The professional's loop: write the sentence \u2192 choose the parameters \u2192 disclose them \u2192 "
      "build the strongest OTHER story \u2192 defend your choice. Room exercise: write story Z.", "ft07_loop.png",
      key="THE LOOP: sentence → parameters → disclosure → strongest OTHER story → defend your choice. The assignment grades exactly this.")
b.end("Small changes, different true stories \u2014 all module long: threshold, section, variable, "
      "window, statistic, period, fit range. Authorship hides in parameters; disclosure is the ethic.")
