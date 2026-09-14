# Assignment 3: Generate–Critique–Repair

**CS 8630 — Data Visualization | AI-Use Tier 1 (AI use required and under study)**
**Due:** September 20, Week 4, 11:59 p.m. | **Weight:** see syllabus | **Individual work**

## Why this assignment exists

Current AI systems produce syntactically valid, superficially reasonable charts on demand. What they cannot reliably do is justify their encoding choices against the perceptual evidence — and neither can you, until you've done it under pressure. In this assignment the AI's output *is* the exam material. You will grade the machine, then beat it.

## The task

You are given the course dataset (posted on Canvas with its datasheet): PR activity for eight repos in
three PR-native orgs (pytorch, moby, pantsbuild), Aug 2023–Aug 2026. You receive it **complete** —
`a3_prs.csv` (93,982 PRs), `a3_repo_month.csv` (268 repo-months) — plus `a3_prs_sample.csv`, a
deterministic ~12k-row sample. Read the datasheet before charting anything.

**Data-handling rule (this is policy, not advice):** the full files never leave your machine. If you
upload data to a hosted AI tool, you upload `a3_prs_sample.csv` only — or upload nothing and prompt
from the schema in the datasheet. Everything the AI produces is then run and continued *locally*
against the complete data. Structure your code so the switch is one line:

```python
FULL = True   # False only while a hosted AI tool is iterating on the sample
df = pd.read_csv("a3_prs.csv" if FULL else "a3_prs_sample.csv")
```

This is not just hygiene. Whether the AI's chart *survives contact with the full dataset* — the months
it never saw, the tail beyond the sample — is part of what you are grading in Part 2, and your Part 3
repair is graded against the full data. A pattern that appears in the sample and dissolves at full
scale is exactly the kind of finding this assignment exists to catch.

Read the **Data Guide** (`a3_data_guide.md`) before anything else — it explains the domain from zero
(what a pull request is, who the three communities are, what every column means and where it bites)
and defines three question sets of increasing rigor: **Set A (orientation)**, **Set B (comparison)**,
**Set C (investigation)**. The assignment is built on those sets.

Using any LLM or AI charting tool of your choice:

**Part 1 — Generate.** Choose **one question from each set** — one A, one B, one C — and state your
choices at the top of `prompts.md`. For each chosen question, prompt the AI to produce a chart that
answers it. That yields three outputs along a rigor gradient, which is the point: you will watch the
same tool succeed on an orientation question and (probably) fail differently, and more interestingly,
as the questions demand normalization decisions and confound handling. Rules of engagement:
- The AI sees only `a3_prs_sample.csv` / `a3_repo_month.csv` or the schema from the Data Guide —
  never the full raw file (course data policy).
- Give the AI the question essentially as written; you may add format/tooling instructions, but if
  you find yourself pre-answering the analytical decisions (scale, normalization, filtering) in the
  prompt, you've started doing its exam for it — note anything of the kind in `prompts.md`.
- Save exact prompts, tool and model names, dates, and the raw, unmodified outputs (code + image).
- Run each AI output locally against the full data (`FULL = True`) and save both renders where they
  differ. Divergence between sample and full is critique material, not a nuisance.

**Part 2 — Critique.** For each of the three outputs, write a structured critique (350–500 words each) grounded explicitly in course frameworks:

- **Encoding analysis (grammar of graphics):** What aesthetic mappings did the AI choose? Are scale, coordinate system, and geometry appropriate to the data types?
- **Perceptual analysis (Cleveland):** Where do the chosen encodings sit in the hierarchy of graphical perception (position > length > angle > area > color saturation...)? What comparisons does the chart make easy, and which does it make hard?
- **Retinal variables (Bertin):** Are the variables' levels of organization (selective, associative, ordered, quantitative) respected by the visual variables assigned to them?
- **Defects and deceptions:** Truncated axes, dual axes, rainbow colormaps on sequential data, overplotting, misleading aspect ratios, aggregation choices that hide structure. Name each defect precisely.
- **Fitness for the question (new, and weighted):** Does the chart actually answer the chosen
  question at that question's level of rigor? For your Set-B question: did the AI *make* the
  normalization/denominator decision the question forces, dodge it, or make it silently? For Set C:
  did it handle — or even notice — the confound the Data Guide flags (censored open PRs,
  collection-time association labels, small-strata instability, sample-vs-full divergence)? A
  beautiful chart that answers an easier question than the one asked is a specific, nameable failure.
- **Sample-vs-full check:** Report whether the AI's story survived `FULL = True`. If anything moved
  (a trend flattened, a category vanished, an outlier appeared), diagnose why in one paragraph.

Every claim must cite the framework it comes from. "It looks cluttered" earns nothing; "the AI encoded an ordered variable with hue, which Bertin classifies as selective but not ordered, so the reader cannot recover the ordering" earns full credit.

**Part 3 — Repair.** Choose the most defective of the three outputs and rebuild it yourself (Python
or R, per course tooling), running against the **full** dataset (`FULL = True`). The repair must
answer the *original chosen question* at its intended level of rigor — including the decisions the AI
dodged: state your scale choice against the ~150× size skew, your normalization against the 89%
pytorch imbalance, your handling of NULLs/censoring, and (for Set C) your treatment of the named
confound. If your Set-C question involves ExecuTorch, your repair can be checked against the
documented release dates — design as if the reader will do exactly that. Every change from the AI's version must appear in a change table: *what changed → which principle motivated it → what the reader can now do that they couldn't before.* Cosmetic changes without perceptual justification count against you.

## Deliverables (single repo or notebook, per course template)

1. `prompts.md` — your three chosen questions (one per set) and why; exact prompts, tool and model used, dates; any pre-answering you caught yourself doing
2. `raw-outputs/` — the three unmodified AI outputs (code + images), plus the local full-data render of each where it differs from the sample render
3. `critique.md` — the three structured critiques
4. `repair/` — your rebuilt visualization (source + rendered output)
5. `change-table.md` — the justified diff
6. `AI-LOG.md` — standard course log (Tier 1: the required AI use above, plus any *additional* AI assistance you used for Part 3, logged as usual)

## Rubric (100 pts)

| Component | Pts | What earns full credit |
|---|---|---|
| Generation quality | 10 | Three genuinely distinct encoding strategies; prompts show intent, not luck |
| Critique: framework grounding | 25 | Every claim tied to Cleveland, Bertin, or grammar-of-graphics concepts, accurately |
| Critique: defect detection & fitness-for-question | 25 | Real defects named precisely; the dodge-or-decide analysis done for B and C; sample-vs-full divergence diagnosed; no invented defects |
| Repair: perceptual improvement | 25 | The rebuild measurably improves the comparisons the data supports |
| Change table justification | 10 | Each change traced to a principle; no unjustified cosmetics |
| Reproducibility | 5 | Code runs clean from the repo; outputs regenerate |

## Choosing your questions

Any A/B/C combination is legitimate, but combinations that share a thread critique better — e.g.,
A4 → B1 → C1 (the association/newcomer thread), or A1 → B4 → C3 (the volume/release thread), or
A2 → B2 → C4 (the size/skew thread). A shared thread means your three critiques compound instead of
starting over, and your Part 3 repair inherits everything you learned. Threads are suggestions, not
requirements; a deliberate contrast (easy A, hostile C) is also defensible if you say why.

## Notes

- You will not be penalized because the AI produced a good chart. If an output is genuinely strong, a critique that demonstrates *why* it is strong — in framework terms — is exactly as valuable as finding flaws. Inventing defects that aren't there is the failure mode.
- Using a second AI to write your critique defeats the purpose and is easy to detect in the oral follow-ups conducted during Week 5 studio. Be ready to defend any sentence in your critique, live.
