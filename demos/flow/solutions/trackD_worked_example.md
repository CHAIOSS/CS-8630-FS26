# Track D worked example (instructor calibration — do not post): turbli's world turbulence map

**The license (claims the artifact supports, tied to encodings):** (1) *Relative* turbulence
intensity along drawn flight levels — the colour scale encodes EDR, the ICAO-standard cascade
dissipation metric, at the stated flight level and forecast hour; comparisons along one level at
one hour are the designed read. (2) Regime geography — jet-adjacent bands and mountain-wave zones
read as structure, the same pattern-level license as every field picture. (3) Forecast vintage —
the page states model (NOAA GFS-driven indices) and cycle, so "as of the 06Z run" claims are
available to a reader who scrolls.

**The temptation (claims invited but unsupported):** (1) Trajectory talk — "my flight path crosses
orange, so we'll hit turbulence at hour three": the map is a field snapshot per forecast hour, not
an integrated path through an evolving field (the steady-field lie, aviation edition). (2)
Cross-level or cross-day magnitude comparison without noting the colour scale's percentile
behavior. (3) Forecast-as-measurement — EDR here is model output; the colour's confidence is not
pixel-uniform and no uncertainty channel exists.

**The receipt hunt:** turbli/about documents the EDR pipeline and model cadence — a genuine
disclosure page (rare; credit it). Steadiness is implicitly disclosed via per-hour frames; nothing
flags inter-frame evolution rate, which is the one disclosure the checklist finds missing.

**Redesign memo (200 words, abbreviated):** the smallest change converting temptation (1) into a
licensed claim is a route-sampling overlay: let the user drop a great-circle route + departure
time, and have the site sample EDR along the route *through successive forecast hours* — i.e.,
compute the pathline through the forecast cube rather than letting the eye extrapolate across one
frame. Everything needed already exists server-side (per-hour fields); the change moves the
integration from the reader's imagination, where it is wrong, into the system, where it is
checkable. Second-smallest: an inter-frame "evolution speed" badge per region, warning when the
one-frame read decays fastest.
