"""Shared fractal-time helpers + Builder."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "grammar"))
from _grammar import Builder, annot, INK, ACCENT, TEAL, MUTED
import numpy as np
import matplotlib.pyplot as plt

def fbm(n, H, seed=0):
    r = np.random.default_rng(seed)
    f = np.fft.rfftfreq(n, 1.0); f[0] = f[1]
    amp = f ** (-(2 * H + 1) / 2)
    x = np.fft.irfft(amp * (r.normal(size=f.shape) + 1j * r.normal(size=f.shape)), n)
    return (x - x.mean()) / x.std()
