"""CS 8630 Unit 7 demo — preprocessing is editorial.
One synthetic commit-message corpus, two pipelines, two 'findings.'
Run: python unit07_text.py [--save DIR]"""
from _style import *
import re
from collections import Counter

rng = np.random.default_rng(7)
verbs = (["fix"] * 30 + ["fixes"] * 25 + ["fixed"] * 20 + ["build"] * 55 +
         ["test"] * 28 + ["tests"] * 14 + ["refactor"] * 30 + ["docs"] * 20 + ["ci"] * 26)
rng.shuffle(verbs)
corpus = [f"{v} the {o} module" for v, o in zip(verbs, rng.choice(["auth", "db", "api"], len(verbs)))]

def pipeline(msgs, stem, stop):
    toks = []
    for m in msgs:
        for t in re.findall(r"[a-z]+", m.lower()):
            if t in stop: continue
            if stem: t = re.sub(r"(es|ed|s)$", "", t)
            toks.append(t)
    return Counter(toks).most_common(5)

A = pipeline(corpus, stem=True,  stop={"the", "module", "auth", "db", "api"})
B = pipeline(corpus, stem=False, stop={"the", "module", "auth", "db", "api", "ci"})

fig, axes = plt.subplots(1, 2, figsize=(10.5, 4))
for ax, res, name, col in [(axes[0], A, "Pipeline A: stemming ON, stop-list S1", TEAL),
                           (axes[1], B, "Pipeline B: stemming OFF, stop-list S2", ACCENT)]:
    words, counts = zip(*res)
    ax.barh(range(len(words))[::-1], counts, color=col)
    ax.set_yticks(range(len(words))[::-1], words)
    ax.set_title(f"{name}\nheadline: '{words[0]}' dominates", fontsize=10)
fig.suptitle("Same corpus. The 'finding' belongs to the pipeline, not the data.", fontsize=12)
fig.tight_layout()
finish(fig, "unit07_pipelines.png")
print("Pipeline A top terms:", A, "\nPipeline B top terms:", B)
