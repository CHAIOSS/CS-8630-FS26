"""SYNTHESIS — one sentence, two dialects, and where the defaults diverge.
Run: python g10_grammar_as_interface.py [--save DIR]"""
from _grammar import *
import altair as alt, json, tempfile

m = monthly(prs())
b = Builder("The same sentence in two grammars — what survives translation?", "g10")
gg = (ggplot(m, aes("month", "prs", colour="repo")) + geom_line() + geom_point()
      + scale_y_log10() + scale_colour_manual(values=PAL) + theme_course)
b.add('ggplot(m, aes(month, prs, colour=repo)) + line + point + log y', gg,
      "The layered-grammar dialect.", "g10_ggplot.png")
chart = (alt.Chart(m).mark_line(point=True).encode(
    x="month:Q", y=alt.Y("prs:Q", scale=alt.Scale(type="log")), color="repo:N")
    .properties(width=520, height=300))
vl_png = os.path.join(tempfile.gettempdir(), "g10_vl.png")
chart.save(vl_png, scale_factor=2)
if "--save" in sys.argv:
    i = sys.argv.index("--save"); outdir = sys.argv[i+1] if len(sys.argv) > i+1 else "."
    chart.save(os.path.join(outdir, "g10_vegalite.png"), scale_factor=2)
    print("saved", os.path.join(outdir, "g10_vegalite.png"))
b.add('the SAME sentence as Vega-Lite JSON (Altair)', vl_png,
      "Translated — but look: different hues, different tick breaks, different point size.", None)
spec = json.loads(chart.to_json())
print("\nThe Vega-Lite sentence:")
print(json.dumps({k: spec[k] for k in ("mark", "encoding")}, indent=2))
print("\nWhat did NOT survive translation (the audit):")
for row in [("palette", "ggplot HCL wheel vs Vega category10"),
            ("log breaks", "10/100 vs 10/20/50/100 — tick density changed"),
            ("gap handling", "ggplot breaks the line at a missing month; Vega-Lite interpolates ACROSS it")]:
    print(f"  · {row[0]:12s} {row[1]}")
b.end("The sentence translated; the defaults didn't. That gap is Assignment 2's Tier-1 audit.")
