# Unit 4b Readings — Temporal Data Visualization

Annotated and tiered: ★ required · ◆ recommended · ○ extensions. The module inherits Bach from
Unit 4's optional list and promotes it; everything else is new to the syllabus.

## ★ Required

**Bach, B., Dragicevic, P., Archambault, D., Hurter, C., & Carpendale, S. (2014).** A review of
temporal data visualizations based on space-time cube operations. *EuroVis State of the Art
Reports*, 23–41. (Archival extended version: Bach et al. (2017), A descriptive framework for
temporal data visualization based on generalized space-time cubes, *Computer Graphics Forum,
36*(6), 36–61 — the easier library get.) The module's generative model: most temporal idioms are
operations — cutting, flattening, folding, unrolling — on one conceptual space-time cube. Read for
the operation vocabulary; the deck's Part II closes on it, and seminar Q2 stress-tests it.

**Heer, J., Kong, N., & Agrawala, M. (2009).** Sizing the horizon: The effects of chart size and
layering on the graphical perception of time series visualizations. *Proc. CHI*, 1303–1312. The
horizon chart, perceptually priced: how mirroring and banding trade against chart height, and how
far a series can shrink before estimation degrades. The rare paper that hands you a *number* to
design with — and the evidence behind the deck's claim that the horizon isn't exotic, it's the
space budget obeyed.

**Cleveland, W. S.** *The Elements of Graphing Data* — the banking/aspect-ratio sections
(revisit). Already owned from Unit 1; reread now that aspect ratio has a module to live in.
Companion for the tooling-minded: Heer, J., & Agrawala, M. (2006), Multi-scale banking to 45°,
*IEEE TVCG, 12*(5), 701–708 — banking automated, including for series with structure at several
scales.

## ◆ Recommended

**Robertson, G., Fernandez, R., Fisher, D., Lee, B., & Stasko, J. (2008).** Effectiveness of
animation in trend visualization. *IEEE TVCG, 14*(6), 1325–1332 (InfoVis 2008). The GapMinder
experiment: animated trends versus small multiples versus static traces, measured on analysis and
presentation tasks. The deck's animation verdict — analysis loses, narration survives — is this
paper's finding, and seminar Q3 asks students to argue against it as strongly as they can.

**Haroz, S., Kosara, R., & Franconeri, S. L. (2016).** The connected scatterplot for presenting
paired time series. *IEEE TVCG, 22*(1), 2406–2415. Franconeri again: the elegant
two-series-as-a-path idiom, evaluated. Readers parse the line's *shape* rather than its temporal
meaning unless guides carry them — which turns the deck's "heavy guides or not at all" rule from
taste into citation.

**Byron, L., & Wattenberg, M. (2008).** Stacked graphs — geometry & aesthetics. *IEEE TVCG,
14*(6), 1245–1252. Streamgraphs done rigorously: layer ordering, baseline choice, and wiggle as
explicit optimization targets. Assign to anyone whose project reaches for a stacked area chart —
every parameter they'd otherwise inherit silently is named and priced here.

## ○ Extensions

**Aigner, W., Miksch, S., Schumann, H., & Tominski, C.** *Visualization of Time-Oriented Data*
(2nd ed., Springer, 2023). The field's reference monograph, freshly revised: a systematic model of
time (points vs intervals, linear vs cyclic, ordered vs branching) plus a 100+-technique survey.
The consult-when-choosing book for time, as Nonato & Aupetit is for projections; the 2nd edition
makes it current.

**Wattenberg, M., & Viégas, F.** — for students who enjoyed the Distill pieces: their body of work
on temporal text and history flows shows the module's ideas applied to unconventional temporal
data (edit histories — not far from PR streams).

