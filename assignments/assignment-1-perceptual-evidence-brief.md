# Assignment 1: The Perceptual Evidence Brief

**Unit:** Principles Governing Perception | **Due:** Friday, Week 2 | **AI Tier 2** | Individual

## Read & Write

Read Franconeri et al. (2021), *The Science of Visual Data Communication: What Works*, and the assigned Cleveland chapters (*The Elements of Graphing Data*).

**You will be responsible for being prepared to discuss these readings in depth during class week 2. This is a graduate seminar, and we will all participate.**

Write a **1,200-word evidence brief** on two perceptual claims that working analysts rely on daily — choose from: position-along-common-scale beats angle/area judgments; alignment enables comparison; color hue fails for ordered data; animation impairs comparison; 3D depth cues distort magnitude judgments. For each claim: (a) state it precisely, (b) trace the empirical support through Franconeri et al. and Cleveland — what was actually measured, on whom, with what stimuli, (c) state its boundary conditions — where the claim weakens or reverses, and (d) give one real-world chart type the claim indicts, and one it endorses.

This is an evidence brief, not an opinion piece: every claim cites a specific finding, and "everyone knows pie charts are bad" earns nothing without the measurement behind it.

## Build

Implement a miniature Cleveland–McGill-style judgment experiment in Python or R:
1. A stimulus generator producing paired charts encoding the same quantity two ways (e.g., aligned bars vs. pie segments; position vs. area), with randomized true ratios.
2. A response loop (terminal or notebook widget is fine) recording estimated ratios.
3. Run yourself and at least two volunteers through ≥20 trials per encoding; plot the error distributions by encoding (log2 error, per the original study) and write a 150-word caption stating what your n=3 replication does and does not show.

## AI Instructions

Tier 2. AI may scaffold the experiment code, debug the response loop, and suggest the error metric implementation — logged. AI may **not** summarize the readings for you or draft any of the brief; you may ask it to attack a finished draft ("what's the weakest citation here?") and log what you changed. Your stimulus-generation logic and your interpretation of the error plots are examinable in class discussion.

## Grading (100 pts)

Evidence brief: precision of claims and fidelity to sources (40) · boundary conditions and indicted/endorsed charts (15) · experiment runs and generates valid stimuli (25) · error analysis and honest caption (15) · AI-LOG judgment quality (5)
