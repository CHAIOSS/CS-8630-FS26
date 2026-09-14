# The Assignment 3 Dataset: A Complete Guide

**CS 8630 · Data Visualization · FS2026.** Read this before you chart anything. It assumes you have
never contributed to open source software and explains everything from zero. The companion datasheet
records the extraction details; this guide explains what the data *means*.

---

## 1. What you are looking at, from zero

Open source software is built in public. The projects in this dataset live on **GitHub**, a website
where each project keeps its code in a **repository** ("repo") — think of a repo as a shared folder
containing the project's entire code plus the full history of every change ever made to it.

Nobody edits that shared folder directly. Instead, changes arrive through a formal proposal process
called a **pull request** (PR). If you've used tracked changes in Word: a PR is a bundle of tracked
changes plus a cover note, submitted for approval. The lifecycle of a PR is the heartbeat of this
dataset:

1. **Opened.** An author — an employee of a sponsoring company, a volunteer, a student, anyone —
   proposes a specific change: a bug fix, a new feature, a documentation edit. The proposal says
   exactly which files change and how many lines are added or removed.
2. **Reviewed.** Other participants examine the proposal and leave **reviews** — approvals, requested
   changes, comments. Serious projects rarely accept unreviewed changes.
3. **Resolved**, one of three ways:
   - **Merged:** accepted; the change becomes part of the project. This is success.
   - **Closed (not merged):** rejected or abandoned — the author gave up, the idea was declined, or it
     was superseded. This is a real outcome, not missing data.
   - **Open:** still undecided when we collected the data.

Every row of the main file is one such proposal: who made it (pseudonymized), how big it was, when it
happened, how it was received, and how it ended. In aggregate, PRs are a remarkably rich trace of how
a software community actually functions — its pace, its openness to outsiders, its review discipline,
its health. An entire research field (empirical software engineering; the CHAOSS project) studies
exactly this kind of data, and this extract was produced by that field's tooling
(**Aveloxis**, the instructor's fleet-scale collection system, which continuously gathers this data
from GitHub for thousands of projects).

One vocabulary note: a software **organization** ("org") on GitHub is an umbrella account owning many
related repos. This dataset covers three orgs, chosen because all three run their real development
through PRs (some famous projects don't — their GitHub presence is just a mirror — which is why your
instructor rejected an earlier candidate set).

## 2. The three organizations and eight repositories

**pytorch** — the organization behind PyTorch, one of the world's dominant deep-learning frameworks,
heavily sponsored by Meta with thousands of contributors. In this dataset:
- `pytorch` — the flagship framework repo. Enormous: it alone is most of this dataset.
- `executorch` — PyTorch's newer system for running models on phones and embedded devices. Young,
  growing fast across our window — and the site of the dataset's documented event (§5).
- `FBGEMM` — a specialized high-performance math library used inside PyTorch. Niche, expert-driven.

**moby** — the organization behind the technology that became Docker, the software-container system
that reshaped how applications are deployed. Mature infrastructure with a long history:
- `moby` — the container engine itself. Older, steadier, more conservative than pytorch.
- `buildkit` — the modern engine for *building* container images. Active, mid-sized.
- `sys` — a small supporting library of low-level operating-system helpers. Genuinely quiet: it has
  **16 months with zero PRs**, and that silence is real (see §5).

**pantsbuild** — the community behind Pants, a build system (a tool that orchestrates compiling and
testing large codebases). Much smaller than the other two orgs; largely volunteer-run:
- `pants` — the main tool.
- `scie-pants` — a small companion launcher. Also genuinely quiet in places (4 empty months).

The deliberate design feature: these communities differ in scale by orders of magnitude — pytorch
contributes **83,405** PRs (89% of the dataset), moby **7,208**, pantsbuild **3,369** — roughly a 25×
spread across projects and far wider between individual repos. Nearly every interesting question you
can ask of this data forces you to decide how to handle that imbalance. That is not an accident.

## 3. The files, and the rule about AI tools

| File | Rows | What it is |
|---|---|---|
| `a3_repo_month.csv` | 268 | One row per repo per month: pre-aggregated summary. Start here. |
| `a3_prs.csv` | 93,982 | One row per PR. The canonical raw layer. **Never upload to AI tools.** |
| `a3_prs_sample.csv` | 11,920 | A fixed random ~⅛ sample of the raw layer. **The only file you may give a hosted AI tool.** |
| `a3_repo_selection.csv` | 169 | Audit trail: every candidate repo and why it was or wasn't included. |
| *(optional full tier)* `a3_full_*.csv` | ~all 169 repos | Everything the fleet has for the three orgs, ungated. See §6. |

The data-handling rule is stated in the assignment and it is policy: full files stay on your machine;
hosted AI tools see only the sample (or no data at all — you can prompt from the schema in this
guide). Your code should switch between sample and full with one flag, because everything an AI
produces for you gets re-run locally against the full data — and whether its story *survives* that
switch is part of what you're graded on.

## 4. Column dictionary (raw layer, `a3_prs.csv`)

For each column: what it is, its **level of measurement** (this course's obsession — it determines
which visual channels can carry it), and what to watch for.

- **`project`** — which organization (pytorch / moby / pantsbuild). *Nominal, 3 levels.* An unordered
  category: any encoding that implies an order among projects is claiming something false.
- **`repo_name`** — which repository (8 values). *Nominal, 8 levels.* Note it's nested inside
  `project` — Wilkinson's nest operator from Unit 2, in the wild.
- **`month`** — the calendar month the PR was opened, e.g. `2024-10-01` = October 2024. *Temporal.*
  36 months, Aug 2023 through Jul 2026. A month absent for a repo means **zero PRs that month**, not
  missing data (assignment tier only — see §6). Watch: tools that interpolate lines across absent
  months are inventing activity that didn't happen.
- **`outcome`** — merged / closed / open. *Nominal, 3 levels* — though you may defensibly treat it as
  a success gradient; if you do, say so. Watch: "open" is censored, not failed — recent months have
  more opens simply because their PRs haven't had time to resolve. Any merge-rate trend that "drops"
  in the last few months is probably this artifact.
- **`author_association`** — GitHub's label for the author's relationship to the project **at
  collection time**. *Ordinal.* The levels, in increasing insider-ness:
  1. `NONE` — an outsider: no prior accepted work here.
  2. `FIRST_TIME_CONTRIBUTOR` — first accepted contribution in flight. *(not present in-window)*
  3. `CONTRIBUTOR` — has prior merged work but no special standing.
  4. `COLLABORATOR` — granted direct write access; a trusted regular.
  5. `MEMBER` — formal member of the organization (often employees/maintainers).
  6. `OWNER` — the org's owner account. *(not present in-window)*
  Four levels appear in this window. **This column is genuinely ordered** — and it is the dataset's
  best trap, because AI tools almost always encode it with unordered rainbow hues, which throws the
  order away. Bertin has a name for that mistake; you'll learn it in Unit 3. Watch: the label reflects
  status *when we collected*, not when the PR was opened — a 2023 PR by someone who became a MEMBER in
  2025 carries `MEMBER`. Any "newcomers vs insiders over time" story must reckon with this.
- **`author_pseud`** — the author, as a stable pseudonym (`a`+8 hex chars). *Nominal, ~thousands of
  levels.* Same person = same pseudonym everywhere, so "how many distinct authors" and "does this
  author appear in multiple repos" work; identity does not. Never chart raw pseudonym labels — count
  or rank them.
- **`size_lines`** — total lines added + deleted across the PR's files. *Quantitative (ratio).* The
  distribution is violently skewed: the 99th percentile is ~**150×** the median. Typical PRs touch
  dozens of lines; a few touch hundreds of thousands (vendored files, generated code, mass renames).
  On a linear scale, one such PR flattens everything else into invisibility. Watch: 0 is possible
  (metadata-only changes), which breaks naive log scales — decide and disclose.
- **`files_touched`** — how many files the PR modified. *Quantitative.* Skewed like `size_lines`,
  correlated with it but not redundant (one huge generated file vs. fifty small edits).
- **`review_count`** — number of formal review submissions the PR received. *Quantitative (count).*
  0 is common and meaningful (merged unreviewed, or closed before anyone looked).
- **`hours_to_first_review`** — hours from opening to the first review. *Quantitative.* **NULL when
  no review ever happened** — and that's a huge, non-random slice. Averaging over only-reviewed PRs
  answers a different question than "how responsive is this project"; know which one you're asking.
- **`hours_to_merge`** — hours from opening to merge. *Quantitative.* **NULL unless merged.** Skewed:
  minutes to years. The same censoring warning as `outcome` applies to recent months.

**Aggregate layer (`a3_repo_month.csv`)** adds, per repo-month: `prs_opened`, `prs_merged`,
`share_merged` (merged ÷ opened that month), `median_hours_to_merge` (over that month's *merged* PRs
only), `median_size_lines`, `active_authors` (distinct pseudonyms). Watch: in low-volume repo-months
(tomcat-sized counts), these summaries are computed over a handful of PRs and jump around; a "trend"
in a 5-PR month is noise wearing a costume.

## 5. Facts you must reckon with (they will appear in your charts whether you know them or not)

1. **The imbalance is real.** 89% of rows are pytorch. Raw-count comparisons across projects are
   dominated before you start; shares, rates, and per-author measures are your normalizing tools —
   and each answers a different question.
2. **The skew is real.** p99/p50 ≈ 150 on size. Every chart of size or latency makes a scale decision.
3. **The quiet months are real** (assignment tier). `moby/sys` and `scie-pants` were watched
   continuously; their empty months are true inactivity. Distinguish this from the full tier (§6).
4. **The documented event.** ExecuTorch — one of your eight repos — shipped its Beta in **October
   2024** and its 1.0 release on **October 22, 2025** (announced at PyTorch Conference). Release
   pushes leave signatures: expect elevated activity in the run-up months. This is the dataset's
   ground truth: when a chart (yours or an AI's) claims something happened in executorch's history,
   these dates are checkable reality.
5. **No bots in the leading roles.** The top authors were audited; all are human accounts. (In most
   PR datasets, automation is a major author — treasure this.)
6. **Pseudonyms, no text.** Names, emails, and all free text were removed at extraction. Analyze
   behavior, not people; de-anonymization attempts are prohibited and pointless for the assignment.

## 6. The optional full tier — and why its silence lies

`a3_full_*.csv` contains *every* fleet repo matching the three orgs — 169 candidates, no quality
gates, archived and defunct repos included (flagged in columns). It exists for extending an analysis
beyond the curated eight. The crucial difference: in the assignment tier, quiet months are guaranteed
real; in the full tier, a repo's silence might be real *or might be shallow collection* — the
guarantee is exactly what the selection gates bought. `a3_full_repo_index.csv` maps what each repo
contributes; read it first, trust it more than any individual repo's zero.

---

## 7. Question sets: three levels of rigor

You'll use these in the assignment (one question from each set drives one of your three AI
generations). They're ordered by how much they demand — not more *work*, more *judgment*.

### Set A — Orientation: direct questions with honest answers
*One or two variables; the challenge is encoding them defensibly, not finding them.*

- **A1.** How has monthly PR volume evolved in each of the eight repos across the 36 months? (The
  scale-imbalance problem in its purest form: one chart, repos spanning 3+ orders of magnitude.)
- **A2.** What does the distribution of PR sizes look like — overall, and per project? (The skew
  problem: your first chart will show one bar. What's your second?)
- **A3.** What share of PRs reaches each outcome (merged / closed / open), by repo? (Part-to-whole:
  the pie temptation, plus the open-PR censoring trap in recent months.)
- **A4.** How is authorship distributed among the association levels, per project? (The ordered
  variable meets the hue trap.)

### Set B — Comparison: questions that force a normalization or design decision
*The data answers only after you decide what "fair comparison" means — and your decision is the chart.*

- **B1.** Do outsiders wait longer? Compare time-to-first-review across `author_association` levels.
  (Confront the NULLs: unreviewed PRs aren't slow reviews, they're a different fate. And the levels
  are ordered — your encoding must say so.)
- **B2.** Are bigger PRs slower to merge — and is that relationship the same in pytorch and moby?
  (Two skewed variables and a comparison across communities of wildly different scale.)
- **B3.** Which repo has the healthiest review culture, and what did you decide "healthy" means?
  (Review counts, unreviewed shares, latency — a composite claim requiring an explicit definition.)
- **B4.** Find ExecuTorch's two Octobers. Does the release cadence (Beta Oct 2024, 1.0 Oct 2025) show
  in opened PRs, merged PRs, latency, authors — and which lens shows it most honestly? (The
  documented event as a design problem: same truth, five encodings, different visibility.)
- **B5.** Small repos vs. large: is `share_merged` comparable between a repo merging 30 of 40 PRs and
  one merging 1,500 of 2,300? What must the chart show for the comparison to be honest? (Denominator
  visibility; small-n instability from §4's warning.)

### Set C — Investigation: questions with confounds, where a defensible answer needs several charts
*Real analytical work: every question here has a tempting wrong answer that a naive chart will happily assert.*

- **C1.** Newcomer experience over time: are `NONE`-authors' PRs treated differently (latency,
  outcome) in 2026 than in 2023 — per project? (Confounds everywhere: association measured at
  collection time; changing PR mix; censoring. State what you can and cannot conclude.)
- **C2.** Author concentration: how dependent is each repo on its few most prolific authors, and how
  has that concentration moved across the window? (Define a concentration measure and defend it;
  visualize thousands of authors without charting pseudonym labels.)
- **C3.** The release-regime question: did ExecuTorch's 1.0 *change* the project — size of typical
  PRs, review latency, author mix before vs. after October 2025 — or did the push merely add volume
  temporarily? (Regime comparison with only ~9 months of "after"; resist overclaiming.)
- **C4.** Sample vs. reality: take one finding an AI tool produced from `a3_prs_sample.csv` and test
  whether it survives `a3_prs.csv` — then explain *why* it did or didn't (sampling noise? tail
  effects? small strata?). (The assignment's data-handling protocol, turned into a question.)
- **C5.** *(full tier)* Choose one org and bring in its full-tier repos. Which conclusions from the
  curated eight generalize to the wider org, and where does the full tier's provenance ambiguity (§6)
  make an apparent finding untrustworthy? (The survivorship question: what did the selection gates do
  to the story?)

A useful discipline for every question in every set: before you chart, write one sentence predicting
what you expect and one sentence naming the decision (scale, normalization, encoding, filter) you
suspect will matter most. Your prediction can be wrong; noticing the decision cannot be skipped.
