# Assignment 3 — Associated Readings (Contemporary)

Annotated and keyed to the assignment's parts and question sets. Suggested tiering: ★ =
required companion reading; ◆ = recommended for the critique; ○ = for extending into the
essay or Set C. 

### Readings to Support Your Work on this Assignment
- Use ★ items as required companions (three papers, all short-course readable).
- Part 2's critique may cite any of cluster A/B in addition to Bertin; Perhaps do a visualization evaluation or
  classification of each output with these in mind.
- Set C1/C3 : Xiao et al. or Song et al. (the AI-era confound) should are exemplary: the strongest possible reading of "did the community change?" is "or did its tooling?"

## A. What AI chart generators actually do (frames Parts 1–2)

★ **Chen, N., Zhang, Y., Xu, J., Ren, K., & Yang, Y. (2024).** VisEval: A benchmark for data
visualization in the era of large language models. *IEEE TVCG, 31*(1), 1301–1311. (VIS 2024 Best
Paper.) The field's systematic answer to "how good are LLMs at making charts": 2,524 natural-language
queries with ground truth, scored on validity, legality, and readability. Its taxonomy of failure
(runs-but-wrong-mapping, missing legends, illegible output) is nearly a rubric for Part 2 — students
can classify each of their three AI outputs into VisEval's categories before applying the course
frameworks. Their documented example failures (a model mapping the wrong aggregate to y; a missing
color legend) will look eerily familiar after Part 1.

★ **Bendeck, A., & Stasko, J. (2025).** An empirical evaluation of the GPT-4 multimodal language
model on visualization literacy tasks. *IEEE TVCG, 31*(1), 1105–1115. The complementary direction:
not can AI *make* charts, but can it *read* them — evaluated on the visualization community's own
literacy instruments. Directly relevant to the assignment's premise that the model's critique
capacity, not just its generation capacity, is under study. Pairs with the oral-defense question
"could the AI have written your critique?"

◆ **Hong, J., Seto, C., Fan, A., & Maciejewski, R. (2025).** Do LLMs have visualization literacy? An
evaluation on modified visualizations to test generalization in data interpretation. *IEEE TVCG.*
Tests whether LLM chart-reading survives perturbed, non-canonical charts — i.e., exactly the
defective charts students will be critiquing. Useful for Set C4 (sample-vs-full divergence): models
that pattern-match canonical charts fail when the picture shifts.

◆ **Chen, Z., Zhang, C., Wang, Q., Troidl, J., Warchol, S., Beyer, J., Gehlenborg, N., & Pfister, H.
(2023).** Beyond generating code: Evaluating GPT on a data visualization course. *EduVis Workshop @
IEEE VIS*, 16–21. GPT run against an actual viz course's assignments — the closest published
analogue to what your students are doing, and a candid inventory of where it earns credit and where
it fakes it.

○ **Dibia, V. (2023).** LIDA: A tool for automatic generation of grammar-agnostic visualizations and
infographics using large language models. *Proc. ACL (System Demos)*, 113–126. The reference
architecture for LLM chart pipelines (summarize → goal → generate → repair). Reading it demystifies
what the tools in Part 1 are doing internally — including the automated "repair" stage students will
outperform in Part 3.

## B. Machine and formal critique of charts (sharpens Part 2)

◆ **Alexander, J., Nanda, P., Yang, K.-C., & Sarvghad, A. (2024).** Can GPT-4 models detect
misleading visualizations? *IEEE VIS (Short Papers)*, 106–110. Asks whether the model can find chart
deception — the exact skill Part 2 grades in the student. Assigning it sets up the uncomfortable,
productive question: on which defect classes is the machine already your peer?

◆ **Chen, Q., Sun, F., Xu, X., Chen, Z., Wang, J., & Cao, N. (2022).** VizLinter: A linter and fixer
framework for data visualization. *IEEE TVCG, 28*(1), 206–216. Critique formalized as machine-checkable
rules over a spec — the grammar-of-graphics payoff from Unit 2 made operational. The change table in
Part 3 is essentially a hand-executed lint-and-fix log; this paper shows what parts of it automate.

○ **McNutt, A., Kindlmann, G., & Correll, M. (2020).** Surfacing visualization mirages. *Proc. CHI.*
The vocabulary for defects that live in the *data-to-chart pipeline* rather than the marks —
aggregation choices, filtering, dirty data producing plausible-looking lies. Set B5 and C-level
critiques benefit most; "mirage" is the precise word for a sample-only pattern that dies at full scale.

○ **Moritz, D., Wang, C., Nelson, G. L., Lin, H., Smith, A. M., Howe, B., & Heer, J. (2019).**
Formalizing visualization design knowledge as constraints: Actionable and extensible models in
Draco. *IEEE TVCG, 25*(1), 438–448. Design knowledge (much of it Cleveland-derived) encoded as
weighted constraints a solver can apply. For the essay-minded: if critique can be constraints, what
exactly is left for the human in Part 2? (Course answer: the question-fitness dimension.)

○ **Lo, L. Y.-H., Gupta, A., Shigyo, K., Wu, A., & Qu, H. (2022).** Misinformed by visualization:
What do we learn from misinformative visualizations? *Computer Graphics Forum, 41*(3) (EuroVis
STAR). The survey and taxonomy of misleading-chart research — the map on which every Part 2 defect
sits.

## C. Human chart-reading and its failure modes (calibrates the critique's standard)

◆ **Ge, L. W., Cui, Y., & Kay, M. (2023).** CALVI: Critical thinking assessment for literacy in
visualizations. *Proc. CHI.* An instrument measuring precisely the skill Part 2 exercises —
detecting misleaders — with the sobering base rates of educated readers who don't. Useful for
grounding what "the reader" in a critique can actually be assumed to catch.

○ **Cui, Y., Ge, L. W., Ding, Y., Yang, F., Harrison, L., & Kay, M. (2023).** Adaptive assessment of
visualization literacy. *IEEE TVCG.* The modern measurement companion: literacy varies enormously
and can be measured efficiently. Background for the "audiences" thread from Unit 1.

## D. The data's world: PR-based open source research, into the AI era (grounds the question sets)

★ **Gousios, G., Pinzger, M., & van Deursen, A. (2014).** An exploratory study of the pull-based
software development model. *Proc. ICSE*, 345–355. The foundational empirical anatomy of exactly
this dataset's row type — what drives PR acceptance and latency. Every Set B question has an
ancestor in this paper; students can check whether its findings visualize out of *their* extract.

◆ **Goggins, S., Germonprez, M., & Lumbard, K. (2021).** Making open source project health
transparent. *IEEE Computer, 54*(8), 104–111. The health-metrics framing (CHAOSS) behind why data
like this is collected at all — and, transparently, the instructor's own research program, of which
the course dataset's pipeline is the current instrument. Turns "why these columns?" into a research
question with a literature.

◆ **Xiao, T., Hata, H., Treude, C., & Matsumoto, K. (2024).** Generative AI for pull request
descriptions: Adoption, impact, and developer interventions. *Proc. ACM on Software Engineering,
1*(FSE), 1043–1065. Early empirical evidence that AI-assisted PRs move review outcomes — measured on
the same variables as Set B (review time, merge likelihood). The dataset's window overlaps the
period this paper describes: your students' data contains this phenomenon.

○ **Song, F., Agarwal, A., & Wen, W. (2024).** The impact of generative AI on collaborative
open-source software development: Evidence from GitHub Copilot. arXiv:2410.02091. Larger-scale
causal-flavored evidence on AI assistance reshaping OSS contribution patterns — relevant context for
any Set C claim about activity or author-mix changes across 2023–2026: part of what moved may be the
tools, not the communities.

○ **Golzadeh, M., Decan, A., Legay, A., & Mens, T. (2021).** A ground-truth dataset and
classification model for detecting bots in GitHub pull request and issue comments. *Journal of
Systems and Software, 175*, 110911. Why the datasheet's bot audit exists: in most PR corpora,
automation is a leading "author." Your extract was audited clean at the top — this paper is the
reason that sentence had to be earned.

○ *(Set C5 extension)* The **AIDev** dataset — hundreds of thousands of AI-agent-authored PRs mined
from GitHub (2025) — and the first MSR 2026 studies built on it document AI agents as PR authors at
scale. For students pushing the full tier: the era boundary where "author" stops implying "human"
falls *inside* this dataset's window. (Cite the specific MSR'26 papers if used; the dataset landed
Nov 2025.)

---


