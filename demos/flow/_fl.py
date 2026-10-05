"""Shared flow sandbox: analytic field (jet + two vortices) + Builder."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "grammar"))
from _grammar import Builder, annot, INK, ACCENT, TEAL, MUTED
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)
def field(x, y, t=0.0):
    u = 0.9 + 0.25 * np.sin(0.6 * y + 2.1 * t)
    v = 0.12 * np.sin(1.1 * x - 1.7 * t)
    for (cx, cy, G) in [(3.2, 4.2, 2.4), (7.0, 2.2, -2.0)]:
        dx, dy = x - cx, y - cy
        r2 = dx * dx + dy * dy + 0.35
        u += -G * dy / r2; v += G * dx / r2
    return u, v

GX, GY = np.meshgrid(np.linspace(0, 10, 34), np.linspace(0, 6.4, 22))
GU, GV = field(GX, GY)

def advect(n=350, steps=70, dt=0.05, unsteady=False, seed=7):
    r = np.random.default_rng(seed)
    px, py = r.uniform(0, 10, n), r.uniform(0, 6.4, n)
    trails = [(px.copy(), py.copy())]
    for k in range(steps):
        tt = k * dt if unsteady else 0.0
        u1, v1 = field(px, py, tt)
        u2, v2 = field(px + 0.5*dt*u1, py + 0.5*dt*v1, tt)
        px = (px + dt*u2) % 10; py = np.clip(py + dt*v2, 0, 6.4)
        trails.append((px.copy(), py.copy()))
    return trails

def frame(figsize=(6.8, 4.2)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 10); ax.set_ylim(0, 6.4)
    return fig, ax
