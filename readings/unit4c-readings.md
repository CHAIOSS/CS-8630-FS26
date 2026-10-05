# Unit 4c Readings — Flow, Motion & the Fractal Structure of Time

Annotated and tiered: ★ required · ◆ recommended (assignment support) · ○ extensions.
Two short required readings on purpose — this module also carries the heaviest assignment build.

## ★ Required

**Laidlaw, D. H., Kirby, R. M., Jackson, C. D., Davidson, J. S., Miller, T. S., da Silva, M.,
Warren, W. H., & Tarr, M. J. (2005).** Comparing 2D vector field visualization methods: A user
study. *IEEE TVCG, 11*(1), 59–70. Flow visualization's Cleveland moment: six methods (arrow grids,
jittered glyphs, LIC-family textures, integrated curves) measured on real tasks — locating critical
points, predicting advection, judging direction. Read for the result pattern: the methods that
*integrate* beat the methods that *sample*, and aesthetic preference tracked effectiveness only
sometimes. The deck's slides 1.1–1.2 are this paper's argument performed on our sandbox field.

**Mandelbrot, B. B. (1967).** How long is the coast of Britain? Statistical self-similarity and
fractional dimension. *Science, 156*(3775), 636–638. Three pages that opened a geometry. Assign it
as a *measurement* argument: length depends lawfully on the ruler, so some natural objects have no
length — only a dimension. The deck transplants the argument to time series (slide 2.1), where
"daily data" is revealed as a ruler choice. Bring one ruler-dependent quantity from your own field.

**The wind map, primary sources (web).** hint.fm/wind (Viégas & Wattenberg, 2012; acquired by
MoMA); earth.nullschool.net (Beccario); turbli.com's world turbulence maps. Ten minutes flying
each, with the deck's 1.5 license in hand: one claim each artifact supports, one it tempts.
Web-native, not archival — the Laidlaw and Mandelbrot papers are this module's citable spine.

## ◆ Recommended

**Barabási, A.-L. (2005).** The origin of bursts and heavy tails in human dynamics. *Nature, 435*,
207–211. Why waiting times in human activity — correspondence, edits, and (directly relevant to
your A3 extract) development events — go heavy-tailed: priority queues, not Poisson chance. The
burst-portrait track's theoretical backbone, and the paper that converts A3's "quiet months" from
anomaly to expectation.

**Mandelbrot, B. B., & Van Ness, J. W. (1968).** Fractional Brownian motions, fractional noises
and applications. *SIAM Review, 10*(4), 422–437. The formal definition of fBm and the Hurst
parameter the deck's concept slide C3 quotes — self-affinity stated as a theorem rather than a
vibe, plus the β = 2H+1 spectral bridge the course's own fbm() code implements. For students who
want the mathematics under ft06's playground.

**Phan, D., Xiao, L., Yeh, R., Hanrahan, P., & Winograd, T. (2005).** Flow map layout. *Proc. IEEE
InfoVis*, 219–224. The algorithmic rescue of Minard's instrument from OD-spaghetti: merging,
routing, and branching flows so hundreds of origin–destination pairs stay legible. Track B's
natural citation, and a clean example of layout-as-editing.

**Cabral, B., & Leedom, L. C. (1993).** Imaging vector fields using line integral convolution.
*Proc. SIGGRAPH*, 263–270. LIC: smear a noise texture along the field and the whole plane becomes
flow-aligned grain — dense flow visualization without glyphs or seeds. The texture-family entry in
Laidlaw's lineup, and the conceptual ancestor of every "the pixels themselves flow" rendering.

**van Wijk, J. J. (2002).** Image based flow visualization. *Proc. SIGGRAPH*, 745–754. IBFV:
advect the *image* instead of particles — real-time animated flow on 2002 hardware, and the bridge
between LIC's statics and the wind map's living surface. Read §1–3 for the idea; skim the rest.

## ○ Extensions

**Tufte, E. R. (1983).** *The Visual Display of Quantitative Information* — the Minard plate and
commentary (pp. 40–41 in most printings). The original 1869 flow map carries six variables through
one catastrophe; ninety seconds on the document itself recalibrates what "complex" means. (Course
library copy on reserve from Unit 1.)

**Frisch, U. (1995).** *Turbulence: The Legacy of A. N. Kolmogorov.* Cambridge UP. The honest route
to K41 and the −5/3 law for anyone the cascade slide hooks. Chapter-level reading; the deck's
claims need only its first two chapters.

**Peng, C.-K., Havlin, S., Stanley, H. E., & Goldberger, A. L. (1995).** Quantification of scaling
exponents and crossover phenomena in nonstationary heartbeat time series. *Chaos, 5*(1), 82–87.
DFA — the workhorse estimator when trends contaminate the aggregated-variance method ft02 teaches.
For Track C students whose series have obvious drift.

**Richardson, L. F. (1922).** *Weather Prediction by Numerical Process.* Cambridge UP — for the
couplet alone ("Big whorls have little whorls…", p. 66), quoted on the cascade slide, parodying
Swift, and compressing this module into nineteen words in 1922.
