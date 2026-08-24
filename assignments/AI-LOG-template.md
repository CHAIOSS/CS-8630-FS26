# AI-LOG

**Course:** CS 8630 | **Student:** _name_ | **Project/Assignment:** _which_

> Commit an entry in the same commit as the work it describes. Entries are graded on
> judgment quality, not volume. Summaries, not transcripts. One entry per meaningful
> AI interaction or work session — not per prompt.

---

## Entry template

### [YYYY-MM-DD] — _short description of the work session_
- **Tool/model:** (e.g., Claude Sonnet 4.6, GPT-5, Copilot in VS Code)
- **What I asked for:** one or two sentences summarizing intent, not the verbatim prompt
- **What it produced:** one or two sentences
- **Accepted:** what you kept, and why it was right
- **Rejected/modified:** what you threw out or changed, and the *principle* that justified it
  (perceptual, grammatical, statistical, or engineering grounds — name it)
- **Verification:** how you checked correctness (ran it, compared to docs, tested edge case,
  cross-checked the statistic)

---

## Example entry (delete before first commit)

### [2026-10-14] — First pass at contributor-activity view
- **Tool/model:** Claude Sonnet 4.6
- **What I asked for:** a multi-series time chart of monthly commit counts for the top 8 contributors, from my cleaned dataframe
- **What it produced:** working Plotly code using a stacked area chart with a qualitative palette
- **Accepted:** the data-wrangling (groupby/resample) after checking totals against a manual count for two months
- **Rejected/modified:** the stacked area encoding. My task is comparing individual contributors' trends; stacking puts all but the bottom series on a shifting baseline, which destroys position-along-common-scale judgment (Cleveland). Switched to small multiples with shared y-axis.
- **Verification:** re-ran against raw data; spot-checked contributor #3's spike against the actual commit log for that month.
