"""TIME AS POSITION — gaps are claims; aspect ratio is analysis.
Run: python tp01_time_and_gaps.py [--save DIR]"""
from _t import *

gaps = [9, 10, 22, 23, 24]
b = Builder("One series, five missing months: what does the line claim?", "tp01")
b.add("plot(months, prs)                       # complete data", tsplot(base),
      "Connection means continuity: the line asserts a process. On a time axis, that assertion is usually earned.", "tp01_full.png")
b.add("five months missing \u2192 interpolate()      # most tools' default", tsplot(base, gaps=gaps, mode="interp"),
      "Five months that never happened, drawn as if they did \u2014 g10's dialect crime, generalized.", "tp01_interp.png")
b.branch("\u2192 break the line at the gaps", tsplot(base, gaps=gaps, mode="break"),
      "The line refuses to claim what it doesn't know. Default in almost nothing; correct surprisingly often.", "tp01_break.png")
b.branch("\u2192 fill with ZERO  # honest iff absence means zero", tsplot(base, gaps=gaps, mode="zero"),
      "For A3's quiet months the datasheet certifies exactly this. No tool can know it \u2014 the analyst tells it.", "tp01_zero.png")

def aspect(figsize, title):
    return tsplot(base, title=title, figsize=figsize)
b.add("same series, figsize=(2.4, 5)            # tall", aspect((2.4, 5), "every wiggle a cliff"),
      "", "tp01_tall.png")
b.branch("figsize \u2192 banked (~45\u00b0 segments)", aspect((6.8, 3.0), "orientations resolve \u2014 rates readable"),
      "Cleveland's banking: choose the aspect so slopes live near \u00b145\u00b0, where the eye discriminates them best.", "tp01_banked.png")
b.branch("figsize \u2192 (9, 1.4)                    # flat", aspect((9, 1.4), "the trend irons out"),
      "The default figure size is not a stated criterion.", "tp01_flat.png")
b.end("Two parameters most people never chose \u2014 gap treatment and aspect ratio \u2014 and the chart made "
      "four different claims. Caption the one you mean.")
