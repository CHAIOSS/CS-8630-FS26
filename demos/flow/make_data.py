"""Regenerate the assignment sample data in demos/flow/data/."""
from _fl import *
import pandas as pd
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"), exist_ok=True)
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
# wind grid
pd.DataFrame({"x": GX.ravel(), "y": GY.ravel(), "u": GU.ravel(), "v": GV.ravel()}).to_csv(f"{D}/wind_grid.csv", index=False)
# trajectories: 14 walkers riding the unsteady field
tr = advect(n=14, steps=160, unsteady=True, seed=3)
rows = []
for i in range(14):
    for t, (px, py) in enumerate(tr):
        rows.append((f"w{i:02d}", t, round(px[i], 3), round(py[i], 3)))
pd.DataFrame(rows, columns=["id", "t", "x", "y"]).to_csv(f"{D}/trajectories.csv", index=False)
# bursty event log: 6 authors, heavy-tailed gaps
r = np.random.default_rng(5); rows = []
for a in range(6):
    gaps = (r.pareto(1.25 + 0.1 * a, 500) + 1) * 0.08
    ts = np.cumsum(gaps); ts = ts[ts < 720]  # ~30 days of hours
    rows += [(f"a{a}", round(t_, 3)) for t_ in ts]
pd.DataFrame(rows, columns=["author", "hours"]).to_csv(f"{D}/events.csv", index=False)
print("data written:", os.listdir(D))
