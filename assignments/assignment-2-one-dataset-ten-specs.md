# Assignment 2: One Dataset, Ten Specifications

**Unit:** Grammar of Graphics | **Due:** Sunday, Week 4 | **AI Tier 2 + one Tier-1 exercise** | Individual

## Watch

Depending on how our discussion of week one goes on August 31, there may be a video slide presentation to watch. It's also possible we will get to the slides. So, this is TBD as of the start of class. 

## Read & Write

Read Wickham, *A Layered Grammar of Graphics* (JCGS 2010), alongside three chapters of Wilkinson, *The Grammar of Graphics*, 2nd edition (Springer, 2005; DOI 10.1007/0-387-28695-0 — chapters are available individually through the library's SpringerLink access): **Chapter 1, Introduction**; **Chapter 2, How to Make a Pie**; and **Chapter 5, Algebra**. Chapters 4 (Variables) and 9 (Coordinates) are optional but useful for the essay. Cite the second edition; the 1999 first edition numbers chapters differently.

Write a **1,000-word analytical essay** answering: *where does Wickham's layered grammar depart from Wilkinson's original, and what do those departures buy?* Cover at minimum: the treatment of statistics as layer components, the handling of coordinates and faceting, and defaults as a design philosophy. Close with a 200-word argument for or against this claim: "a grammar of graphics is the right abstraction level for AI chart generation — better than natural language above it or drawing commands below it." Take a side; hedging is graded as absence of a thesis.

## Build

Choose one dataset (course-provided options include an Augur pull-request extract). In ggplot2, plotnine, or Altair, produce **ten distinct specifications** where each successive spec changes exactly one grammar component from a stated parent spec — a geometry swap, a statistic change, a coordinate transform, a scale change, a faceting introduction. For each: the spec, the rendered chart, and a two-sentence annotation naming the component changed and the analytical question the new view answers that the parent didn't. Ten scatterplot recolorings will be returned ungraded.

**Tier-1 exercise (required, submitted as `translation-audit.md`):** Take your most complex specification and ask an LLM to translate it to a different grammar implementation (ggplot2 → Vega-Lite, or Altair → ggplot2). Run the translation. Document every semantic divergence — defaults that silently differ, statistics computed differently, scales inferred differently — in a table: *component → source behavior → translated behavior → visible consequence.* A translation that happens to be perfect must be demonstrated to be perfect.

## AI Instructions

Tier 2 for the ten specs: AI may help with syntax and debugging, logged; the *choice* of which component to vary each step is yours and is the graded skill. The essay follows the standing prose rule. The translation audit is Tier 1: raw model output goes in the repo unmodified.

## Grading (100 pts)

Essay: accurate Wilkinson/Wickham comparison (30) · thesis on grammars as AI abstraction (10) · ten specs with valid single-component deltas and honest annotations (35) · translation audit rigor (20) · AI-LOG (5)
