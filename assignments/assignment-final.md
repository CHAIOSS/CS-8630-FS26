# CS 8630 Semester Project: A Visualization Design Study

**AI-Use Tier 2 throughout (AI as logged collaborator), except where a milestone marks otherwise.**

## What you are building

Not a notebook of charts. A **design study**: you take a real dataset and a real analytical need, abstract that need into visualization tasks, design encodings that serve those tasks, build an interactive or multi-view solution, and defend every major choice. The final artifact matters; the documented reasoning that produced it matters more, and is graded accordingly.

## Datasets

**Default track — Open Source Software Health (CHAOSS/Augur).** The course provides Augur data exports and SQL access: commits, issues, pull requests, review latency, contributor activity, and dependency freshness (libyear) across real open source repositories. Candidate stakeholder questions include contributor sustainability (is this project a bus-factor-of-one?), review bottlenecks, dependency risk, and community responsiveness. The instructor acts as your stakeholder and will answer questions in that role — these are questions he actually works on.

**Petition track — your own domain.** If you have a dataset from your research or professional life, submit a one-page data memo (see Milestone 1) one week early for approval. Requirements: genuinely multidimensional, at least ~10k records or equivalent complexity, documented provenance, and a stakeholder you can name (a person or role, not "the public").

## Milestones

All milestones are committed to your project repo by 11:59 p.m. on the stated Sunday (Except the data Memo, due on Friday, October 23). The commit history is part of the assessment — work that materializes in one giant final commit will be treated as process undocumented.

### Milestone 1 — Proposal + Data Memo (Week 11) — 10% (DUE THIS FRIDAY)
One page each.
- **Proposal:** dataset, named stakeholder, three candidate analytical questions, and which visualization idioms you suspect are relevant (you may be wrong; say so).
- **Data memo:** provenance, collection method, known caveats, comparability breaks, missingness, and what those problems imply for honest visualization. (Model: the FBI UCR data notes — reporting discontinuities that make naive cross-year charts lies.)

### Milestone 2 — Task Abstraction + Paper Sketches (Week 12) — 10%
- Munzner-style what/why/how breakdown: data abstraction (types, semantics), task abstraction (actions and targets), and initial encoding rationale.
- **Minimum five hand-drawn sketches** of candidate designs, photographed or scanned into the repo. **This part is Tier 0 — no AI.** The sketches are deliberately pre-computational; they are where your own design instincts are visible and assessable. Ugly is fine. Derivative is fine. Generated is a zero.

### Milestone 3 — Working Prototype + AI-LOG Checkpoint (Week 13) — 10%
- A running prototype implementing your primary view(s) against real data.
- Your `AI-LOG.md` to date. This checkpoint is graded on **judgment quality**: the log should show what you asked AI tools to do, what you accepted, what you rejected, and *why* — in perceptual/design terms. "Rejected the suggested treemap: my task is trend comparison across entities, and area encoding on a space-filling layout destroys position-based comparison" is exemplary. Ten pages of pasted transcripts is not.

### Milestone 4 — Peer Critique Exchange (Week 14) — 10%
You will be assigned another project to review using the course assessment rubric (from the Week 11 unit). Deliverables: your written critique of their prototype (framework-grounded, as in Assignment 3), and your one-page response to the critique you received — what you'll change, what you'll defend, and why.

### Presentations + Oral Defense (Week 15) — 25%
- Team/individual presentation of the design study: question → abstraction → design rationale → demo → evaluation.
- **Individual 10-minute oral defense:** the instructor selects one view of your system and asks you to justify it — "why this encoding and not that one," "what does Cleveland say about this comparison," "what breaks if the data doubles." You defend alone, without notes or devices. This is the course's primary integrity mechanism, and it is also simply how graduate work is examined.

### Final Submission (Finals Week, Monday 5:00 p.m.) — 35%
The complete repo:
- Final artifact (source, build instructions, and a rendered/deployed version)
- Full commit history (do not squash)
- Complete `AI-LOG.md`
- **One-page reflection:** where AI genuinely helped, where it misled you, what you overrode and on what grounds, and what you now believe a visualization expert knows that current AI systems don't.

## Grading philosophy

Roughly 40% of the project grade sits in process artifacts (Milestones 1–4), 35% in the final artifact, 25% in the defense. This is deliberate. A polished dashboard with no visible reasoning will score worse than a modest system with an excellent documented design process. Generation is cheap now; judgment is what this degree certifies.
