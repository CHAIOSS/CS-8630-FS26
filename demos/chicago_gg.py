#!/usr/bin/env python3
"""
chicago35_gg.py — the same 35 ideas as chicago35.py, rebuilt in plotnine (grammar of graphics).

Usage (same CLI as the matplotlib version):
    python chicago35_gg.py                       # auto-downloads/unzips CSV if absent
    python chicago35_gg.py --only 3,8,31
    python chicago35_gg.py --rebuild

REQUIRES chicago35.py IN THE SAME DIRECTORY: pass 1 (download, streaming aggregation,
cache) is imported from it rather than duplicated — one provenance chain, two renderers.
Output: out_chicago_gg/NN_*.png

Where the grammar RESISTS the original idiom (polar clocks, the spiral, multi-panel
composites, dual encodings), this file substitutes the grammar-native idiom and says so
in the figure caption — the resistance is part of the lesson.

Deps: pandas, numpy, plotnine (and chicago35.py's deps).
"""
import argparse, os, textwrap
import numpy as np
import pandas as pd
from plotnine import (ggplot, aes, geom_tile, geom_line, geom_area, geom_step, geom_point,
                      geom_col, geom_segment, geom_path, geom_text, geom_ribbon, geom_hline,
                      geom_vline, facet_wrap, labs, theme_minimal, theme, element_text,
                      element_blank, scale_fill_cmap, scale_color_cmap, scale_x_log10,
                      scale_y_log10, scale_fill_gradient2, scale_color_manual,
                      scale_fill_manual, coord_flip, position_fill, annotate, ggsave)

from chicago35 import (ensure_csv, build_cache, load_cache, mser, hwm, dser, months_axis,
                       hurst_av, trim_trailing, EPOCH, VIOLENT, PROPERTY, LOOP,
                       LAT0, LAT1, LON0, LON1, NB)

INK="#2B3A42"; ACCENT="#E4572E"; TEAL="#1C7293"; MUTED="#64707A"; PUR="#8A5A9E"
WD = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
PALETTE = [INK, ACCENT, TEAL, PUR, MUTED, "#B0431F", "#4B6A52", "#9A7B4F"]

def TH(fs=(11,5.2)):
    return (theme_minimal() +
            theme(figure_size=fs, plot_title=element_text(size=12, weight="bold", color=INK),
                  plot_caption=element_text(size=7.5, color=MUTED, ha="left"),
                  strip_text=element_text(size=8.5, color=INK),
                  axis_title=element_text(size=9, color=INK),
                  panel_grid_minor=element_blank()))

def ttl(t): return "\n".join(textwrap.wrap(t, 110))
def capn(n, extra=""):
    base = (f"Grammar-of-graphics rendering of idea #{n}; identical provenance chain to the matplotlib "
            f"version (see chicago35.py image captions: CSV fields \u2192 cache \u2192 transform). ")
    return "\n".join(textwrap.wrap(base + extra, 150))

FIGS = []
def fig(n, name):
    def deco(fn): FIGS.append((n, name, fn)); return fn
    return deco

def save(p, n, name):
    os.makedirs(OUT, exist_ok=True)
    f = os.path.join(OUT, f"{n:02d}_{name}.png")
    p.save(f, dpi=140, verbose=False)
    print("  wrote", f)

def long_monthly(C, types):
    yrs = months_axis(C); rows=[]
    for t in types:
        v = trim_trailing(mser(C,t))
        rows.append(pd.DataFrame({"year": yrs, "type": t.title(), "n": v}))
    return pd.concat(rows, ignore_index=True)

# --------------------------------------------------------------------------- figures
@fig(1, "heartbeat")
def g01(C):
    M = sum(hwm(C,t) for t in C["hw_types"]); M = M/M.sum(1, keepdims=True)
    df = pd.DataFrame([(WD[w], h, M[w,h]) for w in range(7) for h in range(24)],
                      columns=["weekday","hour","share"])
    df["weekday"] = pd.Categorical(df["weekday"], WD[::-1])
    p = (ggplot(df, aes("hour","weekday",fill="share")) + geom_tile() + scale_fill_cmap("magma")
         + labs(title=ttl("The city's heartbeat: one aes(fill=) declaration replaces the colorbar plumbing"),
                caption=capn(1,"MAPPING: x=hour, y=weekday, fill=within-day share. The normalization is a data step; the chart is three lines."))
         + TH((11,4.4)))
    save(p,1,"heartbeat")

@fig(2, "crime_clocks")
def g02(C):
    tot = {t: hwm(C,t).sum() for t in C["hw_types"]}
    pick = sorted(tot, key=tot.get, reverse=True)[:6]
    df = pd.concat([pd.DataFrame({"hour": range(24),
                                  "v": hwm(C,t).sum(0)/max(hwm(C,t).sum(0).max(),1),
                                  "type": t.title()}) for t in pick])
    p = (ggplot(df, aes("hour","v")) + geom_area(fill=ACCENT, alpha=0.85)
         + facet_wrap("~type", ncol=3)
         + labs(title=ttl("Crime clocks, grammar edition: facet_wrap replaces six hand-placed polar axes"),
                x="hour", y="relative rate",
                caption=capn(2,"RESISTANCE: plotnine has no polar coordinate, so the grammar substitutes faceted cartesian profiles \u2014 arguably more comparable (Cleveland: common aligned scale beats angle)."))
         + TH((11,4.8)))
    save(p,2,"crime_clocks")

@fig(3, "horizon_24yr")
def g03(C):
    df = long_monthly(C, C["top_daily"][:12])
    df["v"] = df.groupby("type")["n"].transform(lambda s: s/s.max())
    p = (ggplot(df, aes("year","v")) + geom_area(fill=ACCENT, alpha=0.8)
         + facet_wrap("~type", ncol=3)
         + labs(title=ttl("Twenty-four years, twelve types: facet_wrap(~type) is the entire layout algorithm"),
                y="share of own peak",
                caption=capn(3,"The horizon fold is an imperative trick; the grammar's native answer is small multiples on a shared x. Trade disclosed: less vertical compression, more honest baselines."))
         + TH((11.5,6.5)) + theme(axis_text_y=element_blank()))
    save(p,3,"horizon_24yr")

@fig(4, "the_fold")
def g04(C):
    tot = trim_trailing(sum(mser(C,t) for t in C["monthly_types"]))
    n = len(tot); Y = tot.reshape(n//12,12)
    df = pd.DataFrame([(2001+y, m+1, Y[y,m]) for y in range(n//12) for m in range(12)],
                      columns=["year","month","n"]).dropna()
    p = (ggplot(df, aes("month","year",fill="n")) + geom_tile() + scale_fill_cmap("viridis")
         + annotate("rect", xmin=2.5, xmax=6.5, ymin=2019.5, ymax=2020.5, fill=None, color=ACCENT, size=1)
         + labs(title=ttl("The fold as geom_tile: year \u00d7 month is just two position mappings"),
                caption=capn(4,"MAPPING: x=month, y=year, fill=count. The reshape lives in the data frame; the annotation layer marks spring 2020."))
         + TH((10.5,5.6)))
    save(p,4,"the_fold")

@fig(5, "season_fingerprints")
def g05(C):
    rows=[]
    for t in C["top_daily"][:10]:
        v = trim_trailing(mser(C,t)); Y=v.reshape(-1,12)
        with np.errstate(invalid="ignore"):
            prof = np.nanmean(Y/np.nanmean(Y,1,keepdims=True),0)
        rows.append(pd.DataFrame({"month": range(1,13), "rel": prof, "type": t.title()}))
    df = pd.concat(rows)
    p = (ggplot(df, aes("month","rel")) + geom_line(color=ACCENT, size=1)
         + geom_hline(yintercept=1, color=MUTED, linetype="dotted")
         + facet_wrap("~type", ncol=5)
         + labs(title=ttl("Seasonality fingerprints: the y-axis keeps its meaning (1.0 = that type's average month)"),
                y="month / own annual mean",
                caption=capn(5,"GAIN over the ridgeline: no min\u2013max rescaling needed for layout, so amplitude survives \u2014 battery's swing and narcotics' flatness are now honestly different sizes."))
         + TH((11.5,4.6)))
    save(p,5,"season_fingerprints")

@fig(6, "scissors")
def g06(C):
    vio = trim_trailing(sum(mser(C,t) for t in C["monthly_types"] if t in VIOLENT))
    pro = trim_trailing(sum(mser(C,t) for t in C["monthly_types"] if t in PROPERTY))
    def yr_s(v): return np.nanmean(v.reshape(-1,12),1)
    v1, v2 = yr_s(vio), yr_s(pro)
    df = pd.concat([pd.DataFrame({"year": range(2001,2001+len(v1)), "idx": v1/v1[0]*100, "class":"violent"}),
                    pd.DataFrame({"year": range(2001,2001+len(v2)), "idx": v2/v2[0]*100, "class":"property"})])
    p = (ggplot(df, aes("year","idx",color="class")) + geom_line(size=1.3) + geom_point(size=1.5)
         + geom_hline(yintercept=100, color=MUTED, linetype="dotted")
         + scale_color_manual([INK,ACCENT])
         + labs(title=ttl("The scissors: color=class is a declared mapping, so the legend writes itself"),
                y="index (2001 = 100)",
                caption=capn(6,"The violent/property classification is a column in the tidy frame \u2014 reclassify one type and every layer updates; that is the grammar's version of the authored-parameter discipline."))
         + TH((11,4.8)))
    save(p,6,"scissors")

@fig(7, "spectrum")
def g07(C):
    x = dser(C,"ALL"); x = x - x.mean()
    ps = np.abs(np.fft.rfft(x))**2; f = np.fft.rfftfreq(len(x),1.0)
    df = pd.DataFrame({"f": f[1:], "p": ps[1:]})
    p = (ggplot(df, aes("f","p")) + geom_line(size=0.3, color=INK)
         + scale_x_log10() + scale_y_log10()
         + geom_vline(xintercept=[1/7,1/365.25], color=ACCENT, linetype="dashed")
         + labs(title=ttl("The spectrum: scale_x_log10 + scale_y_log10 are declarations, not axes surgery"),
                x="frequency (1/day)", y="power",
                caption=capn(7,"Dashed guides: weekly and annual clocks. The sloping floor is the fractal-time claim; a slope needs a stated fit range before it earns a name."))
         + TH((10.5,4.8)))
    save(p,7,"spectrum")

@fig(8, "homicide_burst")
def g08(C):
    g = np.diff(C["ts_HOMICIDE"]); g = g[g>0]
    r = np.random.default_rng(1); null = r.exponential(g.mean(), len(g))
    def ccdf(v, lab):
        s = np.sort(v); return pd.DataFrame({"x": s, "p": 1-np.arange(len(s))/len(s), "series": lab})
    df = pd.concat([ccdf(g,"observed gaps"), ccdf(null,"memoryless null")])
    p = (ggplot(df, aes("x","p",color="series")) + geom_step(size=0.9)
         + scale_x_log10() + scale_y_log10() + scale_color_manual([MUTED,ACCENT])
         + labs(title=ttl("Homicide gaps vs the memoryless null: the null is just another row group"),
                x="gap between homicides (days)", y="P(gap > x)",
                caption=capn(8,"RESISTANCE: the matplotlib burst PORTRAIT is a composed triptych (raster + CCDF + promises); the grammar builds one plot per claim. This is the core claim; the raster and promises become their own plots when needed."))
         + TH((9.5,5.2)))
    save(p,8,"homicide_burst")

@fig(9, "hurst_ladder")
def g09(C):
    rows=[]
    for t in C["top_daily"][:12]:
        h = hurst_av(np.cumsum(dser(C,t)-dser(C,t).mean()))
        if np.isfinite(h): rows.append((t.title(), h))
    df = pd.DataFrame(rows, columns=["type","H"]).sort_values("H")
    df["type"] = pd.Categorical(df["type"], df["type"])
    p = (ggplot(df, aes("H","type")) + geom_segment(aes(x=0.5, xend="H", yend="type"), color="#C9D2D8")
         + geom_point(size=3, color=ACCENT) + geom_vline(xintercept=0.5, color=MUTED, linetype="dotted")
         + labs(title=ttl("The memory ladder: reorder-by-value is a data-frame sort, not axis bookkeeping"),
                x="Hurst H (aggregated-variance estimate)", y="",
                caption=capn(9,"Everything sits right of the memoryless line: persistence is the default null for 'trend' claims. Point estimates; no intervals \u2014 question that."))
         + TH((10,5)))
    save(p,9,"hurst_ladder")

@fig(10, "zoom_quiz")
def g10(C):
    x = dser(C,"THEFT"); n = len(x)
    spans = {"A": (n//3, n//3+n//8), "B": (n//2, n//2+180), "C": (0, n)}
    rows=[]
    for lab,(a,b) in spans.items():
        seg = x[a:b]; seg=(seg-seg.mean())/(seg.std()+1e-9)
        rows.append(pd.DataFrame({"i": np.linspace(0,1,len(seg)), "v": seg, "panel": f"panel {lab}"}))
    df = pd.concat(rows)
    p = (ggplot(df, aes("i","v")) + geom_line(size=0.3, color=INK) + facet_wrap("~panel")
         + labs(title=ttl("The zoom quiz: three windows are three facet groups of one tidy frame"),
                x="", y="",
                caption=capn(10,"Answers: A = 3 years, B = 6 months, C = 24 years. The z-scoring that makes the quiz hard is a disclosed data transform \u2014 the facets merely refuse to leak it."))
         + TH((11,3.2)) + theme(axis_text=element_blank()))
    save(p,10,"zoom_quiz")

@fig(11, "arrest_collapse")
def g11(C):
    A = C["arrest"]; rows=[]
    for t in C["top_daily"][:12]:
        d = A.get(t,{})
        def rate(ys):
            a=sum(d.get(y,[0,0])[0] for y in ys); m=sum(d.get(y,[0,0])[1] for y in ys)
            return a/m*100 if m else np.nan
        rows += [(t.title(),"2001\u201305",rate(range(2001,2006))),(t.title(),"2019\u201323",rate(range(2019,2024)))]
    df = pd.DataFrame(rows, columns=["type","era","rate"]).dropna()
    p = (ggplot(df, aes("era","rate",group="type")) + geom_line(color=INK, alpha=0.7)
         + geom_point(color=ACCENT, size=2)
         + geom_text(df[df.era=="2001\u201305"], aes(label="type"), ha="right", nudge_x=-0.06, size=6.5, color=INK)
         + labs(title=ttl("The arrest-rate slopegraph: group=type declares the lines; no loop draws them"),
                y="arrest rate %", x="",
                caption=capn(11,"'Arrest' is a report-level flag, not clearance or conviction \u2014 and two decades of recording practice sit inside these slopes."))
         + TH((10.5,5.6)))
    save(p,11,"arrest_collapse")

@fig(12, "system_path")
def g12(C):
    A = C["arrest"]; rows=[]
    for y in range(2001,2025):
        a=sum(A[t].get(y,[0,0])[0] for t in A); m=sum(A[t].get(y,[0,0])[1] for t in A)
        if m: rows.append((y, m/1e3, a/m*100))
    df = pd.DataFrame(rows, columns=["year","vol","rate"])
    lab = df[df.year.isin([2001,2008,2016,2020,df.year.max()])]
    p = (ggplot(df, aes("vol","rate")) + geom_path(color=INK, size=0.7) + geom_point(size=1.2, color=INK)
         + geom_text(lab, aes(label="year"), color=ACCENT, size=8, nudge_y=0.6, fontweight="bold")
         + labs(title=ttl("The system's path: geom_path keeps row order \u2014 time IS the data order, declared"),
                x="recorded crimes (thousands/yr)", y="arrest rate %",
                caption=capn(12,"Both axes derive from the same records; recording changes move points diagonally. The connected scatter shows co-drift, never causation."))
         + TH((10,5.4)))
    save(p,12,"system_path")

def _xy_df(M):
    yy,xx = np.nonzero(M)
    return pd.DataFrame({"x": xx, "y": yy, "n": np.log1p(M[yy,xx])})

@fig(13, "theft_vs_burglary_maps")
def g13(C):
    rows=[]
    for t in ["THEFT","BURGLARY"]:
        d = _xy_df(C["xy"][C["xy_types"].index(t)]); d["type"]=t.title(); rows.append(d)
    df = pd.concat(rows)
    p = (ggplot(df, aes("x","y",fill="n")) + geom_tile() + scale_fill_cmap("magma")
         + facet_wrap("~type")
         + labs(title=ttl("Two geographies: the map is geom_tile on binned counts \u2014 same grammar as the heartbeat"),
                x="", y="", caption=capn(13,"fill = log(1+count); rows without coordinates excluded; coordinates block-shifted by the portal. A density map of records is also a map of where coordinates exist."))
         + TH((11,5.2)) + theme(axis_text=element_blank()))
    save(p,13,"theft_vs_burglary_maps")

@fig(14, "loop_gravity")
def g14(C):
    iy0=(LOOP[0]-LAT0)/(LAT1-LAT0)*NB; ix0=(LOOP[1]-LON0)/(LON1-LON0)*NB
    yy,xx = np.mgrid[0:NB,0:NB]
    km = np.hypot((yy-iy0)*(LAT1-LAT0)/NB*111,(xx-ix0)*(LON1-LON0)/NB*83)
    rows=[]
    for t in C["xy_types"]:
        M = C["xy"][C["xy_types"].index(t)].astype(float)
        for b in range(24):
            m=(km>=b)&(km<b+1)
            rows.append((b+0.5, M[m].sum()/max(m.sum(),1), t.title()))
    df = pd.DataFrame(rows, columns=["km","dens","type"])
    df["rel"] = df.groupby("type")["dens"].transform(lambda s: s/s.max())
    p = (ggplot(df, aes("km","rel",color="type")) + geom_line(size=1)
         + scale_color_manual(PALETTE[:len(C["xy_types"])])
         + labs(title=ttl("The Loop's gravity: six radial profiles, one aes(color=type)"),
                x="km from the Loop", y="density (own peak = 1)",
                caption=capn(14,"Ring denominators are bins, not people \u2014 lake bins dilute; population would reshape. The grammar makes that re-normalization a one-column edit."))
         + TH((10.5,5)))
    save(p,14,"loop_gravity")

@fig(15, "ca_bump")
def g15(C):
    tot = sum(C["ca"][i] for i in range(len(C["ca_types"])))
    th = C["ca"][C["ca_types"].index("THEFT")] if "THEFT" in C["ca_types"] else tot
    hi = C["ca"][C["ca_types"].index("HOMICIDE")] if "HOMICIDE" in C["ca_types"] else tot
    top10 = np.argsort(-tot)[:10]; rows=[]
    for cai in top10:
        for lab, v in [("all crime",tot),("theft",th),("homicide",hi)]:
            rows.append((f"CA {cai}", lab, int(np.sum(v>v[cai]))+1))
    df = pd.DataFrame(rows, columns=["ca","measure","rank"])
    df["measure"] = pd.Categorical(df["measure"], ["all crime","theft","homicide"])
    p = (ggplot(df, aes("measure","rank",group="ca")) + geom_line(color=INK, alpha=0.6)
         + geom_point(color=ACCENT, size=2)
         + geom_text(df[df.measure=="all crime"], aes(label="ca"), nudge_x=-0.15, size=7, color=INK)
         + labs(title=ttl("Same areas, different leaderboards: rank is a computed column, the bump is group=ca"),
                y="rank (1 = most)", x="",
                caption=capn(15,"Counts, not per-capita rates \u2014 population denominators would cross these lines harder, not less."))
         + TH((10,5.4)) + theme(axis_text_y=element_blank()))
    save(p,15,"ca_bump")

@fig(16, "domestic_hours")
def g16(C):
    dom, tot = C["hour_dom"][0], C["hour_dom"][1]
    df = pd.DataFrame({"hour": range(24), "share": dom/np.maximum(tot,1)*100})
    p = (ggplot(df, aes("hour","share")) + geom_area(fill=ACCENT, alpha=0.3) + geom_line(color=ACCENT, size=1.2)
         + labs(title=ttl("When home is the dangerous place: the domestic SHARE by hour"),
                y="% of incidents flagged domestic",
                caption=capn(16,"A share can rise because its denominator falls \u2014 overnight it mostly does. Plot absolute domestic counts beside this before concluding anything about homes at night."))
         + TH((10.5,4.4)))
    save(p,16,"domestic_hours")

@fig(17, "where_bar")
def g17(C):
    items = C["locdesc"][:16]
    df = pd.DataFrame(items, columns=["place","n"]); df["place"]=df["place"].str.title()
    df["place"] = pd.Categorical(df["place"], df.sort_values("n")["place"])
    p = (ggplot(df, aes("place","n")) + geom_col(fill=INK) + coord_flip()
         + labs(title=ttl("Where crime happens: the grammar prefers ranked lengths to a partitioned bar"),
                x="", y="incidents",
                caption=capn(17,"GAIN: geom_col + coord_flip puts the comparison on aligned position (ladder top) instead of the treemap's segment lengths mid-bar. Free-text field; the taxonomy is the officers'."))
         + TH((10.5,5.4)))
    save(p,17,"where_bar")

@fig(18, "street_vs_home")
def g18(C):
    dom, tot = C["hour_dom"][0], C["hour_dom"][1]; street = tot-dom
    df = pd.concat([pd.DataFrame({"hour":range(24),"v":street/street.max(),"city":"non-domestic"}),
                    pd.DataFrame({"hour":range(24),"v":-(dom/dom.max()),"city":"domestic"})])
    p = (ggplot(df, aes("hour","v",fill="city")) + geom_area(alpha=0.85)
         + scale_fill_manual([ACCENT,INK]) + geom_hline(yintercept=0, color="white")
         + labs(title=ttl("Mirror city: the mirror is a sign flip in the data frame, disclosed as such"),
                y="(each city's own peak = 1)",
                caption=capn(18,"Own-peak normalization: shapes comparable, absolute scale deliberately NOT. The domestic city is far smaller in absolute terms."))
         + TH((10.5,4.8)) + theme(axis_text_y=element_blank()))
    save(p,18,"street_vs_home")

@fig(19, "bertin_reorder")
def g19(C):
    pick = C["hw_types"][:12]
    rows=[]
    for t in pick:
        v = hwm(C,t).sum(0); v=v/max(v.sum(),1)
        rows.append(pd.DataFrame({"type": t.title(), "hour": range(24), "share": v, "peak": int(np.argmax(v))}))
    df = pd.concat(rows)
    order = df.drop_duplicates("type").sort_values("peak")["type"]
    df["type"] = pd.Categorical(df["type"], order[::-1])
    p = (ggplot(df, aes("hour","type",fill="share")) + geom_tile() + scale_fill_cmap("Greys")
         + labs(title=ttl("Bertin as a data operation: the permutation is sort_values('peak') \u2014 before any drawing"),
                x="hour", y="",
                caption=capn(19,"THE grammar point of the whole set: reordering rows is a disclosed data-frame transform, not a drawing trick. Criterion stated: peak hour. A different lawful criterion is one sort away."))
         + TH((10.5,4.8)))
    save(p,19,"bertin_reorder")

@fig(20, "calendar_2020")
def g20(C):
    x = dser(C,"ALL"); start=(pd.Timestamp("2020-01-01")-EPOCH).days
    days = x[start:start+366]; fw = pd.Timestamp("2020-01-01").dayofweek
    df = pd.DataFrame({"i": range(366)})
    df["wd"]=(fw+df.i)%7; df["wk"]=(fw+df.i)//7; df["n"]=days[:366]
    df["weekday"]=pd.Categorical([WD[w] for w in df.wd], WD[::-1])
    p = (ggplot(df, aes("wk","weekday",fill="n")) + geom_tile() + scale_fill_cmap("viridis")
         + geom_vline(xintercept=[11,22], color=ACCENT, linetype="dashed")
         + labs(title=ttl("2020 as a calendar tile: week and weekday are computed columns, nothing more"),
                x="week of 2020", caption=capn(20,"Dashed guides (authored): stay-home order week and June 1 \u2014 verify both against the rendered values."))
         + TH((11,3.4)))
    save(p,20,"calendar_2020")

@fig(21, "minard_band")
def g21(C):
    tot = trim_trailing(sum(mser(C,t) for t in C["monthly_types"]))
    v = pd.Series(tot).rolling(6,center=True,min_periods=1).mean().to_numpy()
    yrs = months_axis(C); A=C["arrest"]
    rate = {y: (lambda a,m: a/m*100 if m else np.nan)(sum(A[t].get(y,[0,0])[0] for t in A),
                                                     sum(A[t].get(y,[0,0])[1] for t in A)) for y in range(2001,2026)}
    df = pd.DataFrame({"year": yrs, "w": v/np.nanmax(v)/2}).dropna()
    df["rate"] = [rate.get(int(y),np.nan) for y in df.year]
    p = (ggplot(df, aes("year")) + geom_ribbon(aes(ymin="-w", ymax="w"), fill=MUTED, alpha=0.3)
         + geom_point(aes(y=0, color="rate"), size=1.6) + scale_color_cmap("plasma")
         + labs(title=ttl("A Minard reading: ribbon carries volume; a colored spine carries the arrest rate"),
                y="", caption=capn(21,"RESISTANCE disclosed: a continuously color-varying ribbon fights the grammar (fill maps per-geometry, not per-vertex), so the second variable rides a point layer. Two smoothings (6-mo width, annual color) remain deliberately mismatched."))
         + TH((11,4.2)) + theme(axis_text_y=element_blank()))
    save(p,21,"minard_band")

@fig(22, "era_maps")
def g22(C):
    labs_=["2001\u201308","2009\u201316","2017\u2013present"]; rows=[]
    for e in range(3):
        d=_xy_df(C["xy_era"][e]); d["era"]=labs_[e]; rows.append(d)
    df=pd.concat(rows); df["era"]=pd.Categorical(df["era"],labs_)
    p = (ggplot(df, aes("x","y",fill="n")) + geom_tile() + scale_fill_cmap("magma")
         + facet_wrap("~era")
         + labs(title=ttl("Three eras: the era split is one computed column; facet_wrap does the rest"),
                x="",y="",caption=capn(22,"Coordinate coverage is thinner in early years \u2014 some 'thinning' runs the wrong way. Check share-with-coordinates per era before narrating decline."))
         + TH((11.5,4.4)) + theme(axis_text=element_blank()))
    save(p,22,"era_maps")

@fig(23, "theft_threshold")
def g23(C):
    byy={}
    for dsc,y,n in C["theft_desc"]:
        key = "under $500" if "UNDER" in dsc else ("over $500" if "OVER" in dsc else "other")
        byy.setdefault(key,{}); byy[key][y]=byy[key].get(y,0)+n
    yrs = sorted({y for d in byy.values() for y in d}); rows=[]
    for k,d in byy.items():
        for y in yrs:
            tot = sum(byy[kk].get(y,0) for kk in byy)
            rows.append((y,k,d.get(y,0)/max(tot,1)*100))
    df = pd.DataFrame(rows, columns=["year","band","share"])
    p = (ggplot(df, aes("year","share",color="band")) + geom_line(size=1.1) + geom_point(size=1.2)
         + scale_color_manual([INK,MUTED,ACCENT]) + geom_vline(xintercept=2016, color=PUR, linetype="dashed")
         + labs(title=ttl("The $500 line: category drift inside one crime type, as three share curves"),
                y="share of thefts %",
                caption=capn(23,"The $500 boundary is statutory and nominal while prices rose ~70% \u2014 how much drift is inflation? The dashed marker is authored; verify it."))
         + TH((10.5,4.8)))
    save(p,23,"theft_threshold")

@fig(24, "universal_trough")
def g24(C):
    rows=[]
    for t in C["hw_types"][:14]:
        v=hwm(C,t).sum(0); rows.append(pd.DataFrame({"hour":range(24),"v":v/max(v.max(),1),"type":t.title(),"all":False}))
    va=sum(hwm(C,t) for t in C["hw_types"]).sum(0)
    rows.append(pd.DataFrame({"hour":range(24),"v":va/va.max(),"type":"ALL","all":True}))
    df=pd.concat(rows)
    p = (ggplot(df, aes("hour","v",group="type",alpha="all",size="all")) + geom_line(color=INK)
         + geom_vline(xintercept=5, color=ACCENT, linetype="dotted")
         + labs(title=ttl("The universal trough: fourteen spaghetti strands, one emphasized by a mapped aesthetic"),
                y="(own peak = 1)",
                caption=capn(24,"Occurrence or REPORTING? Fewer victims are awake to call at 5 a.m. \u2014 distinguish before claiming the city sleeps."))
         + TH((10.5,4.8)) + theme(legend_position="none", axis_text_y=element_blank()))
    save(p,24,"universal_trough")

@fig(25, "policing_shapes")
def g25(C):
    rows=[]
    for t in ["NARCOTICS","WEAPONS VIOLATION","PROSTITUTION","BATTERY"]:
        v=hwm(C,t).sum(0)
        if v.sum(): rows.append(pd.DataFrame({"hour":range(24),"v":v/v.max(),"type":t.title()}))
    df=pd.concat(rows)
    p = (ggplot(df, aes("hour","v",color="type")) + geom_line(size=1.1)
         + scale_color_manual([MUTED,ACCENT,TEAL,INK])
         + labs(title=ttl("Enforcement-shaped clocks: four profiles, one declared color mapping"),
                y="(own peak = 1)",
                caption=capn(25,"'Patrol-shaped' is an inference \u2014 no patrol data lives in this dataset. Name the auxiliary data that would confirm it."))
         + TH((10.5,4.6)) + theme(axis_text_y=element_blank()))
    save(p,25,"policing_shapes")

@fig(26, "narcotics_cliff")
def g26(C):
    df = pd.DataFrame({"year": months_axis(C), "n": trim_trailing(mser(C,"NARCOTICS"))}).dropna()
    p = (ggplot(df, aes("year","n")) + geom_area(fill=ACCENT, alpha=0.8)
         + labs(title=ttl("The narcotics cliff: recorded enforcement collapsing \u2014 the data measures attention"),
                y="narcotics incidents / month",
                caption=capn(26,"Nothing in the CSV says WHY. Find the policy record (consent-decree era, directives, decriminalization) that supports or defeats the enforcement reading."))
         + TH((11,4.4)))
    save(p,26,"narcotics_cliff")

@fig(27, "gap_trio")
def g27(C):
    rows=[]
    for key in ["ts_HOMICIDE","ts_ARSON","ts_KIDNAPPING"]:
        ts=C[key]
        if len(ts)<100: continue
        g=np.diff(ts); g=g[g>0]; s=np.sort(g)
        rows.append(pd.DataFrame({"x":s,"p":1-np.arange(len(s))/len(s),"type":key[3:].title()}))
    df=pd.concat(rows)
    p = (ggplot(df, aes("x","p",color="type")) + geom_step(size=0.9)
         + scale_x_log10() + scale_y_log10() + scale_color_manual([INK,ACCENT,TEAL])
         + labs(title=ttl("Three rare crimes' waits: the trio is one tidy frame with a type column"),
                x="gap between incidents (days)", y="P(gap > x)",
                caption=capn(27,"Rare types are where entry errors bite \u2014 audit the five longest gaps per type before trusting any tail."))
         + TH((10,5)))
    save(p,27,"gap_trio")

@fig(28, "era_slopegraph")
def g28(C):
    A=C["arrest"]
    def tot(t,ys): return sum(A.get(t,{}).get(y,[0,0])[1] for y in ys)
    e0={t:tot(t,range(2001,2006)) for t in C["top_daily"]}
    e1={t:tot(t,range(2019,2024)) for t in C["top_daily"]}
    r0={t:i+1 for i,t in enumerate(sorted(e0,key=e0.get,reverse=True))}
    r1={t:i+1 for i,t in enumerate(sorted(e1,key=e1.get,reverse=True))}
    rows=[(t.title(),"2001\u201305",r0[t]) for t in C["top_daily"]]+[(t.title(),"2019\u201323",r1[t]) for t in C["top_daily"]]
    df=pd.DataFrame(rows,columns=["type","era","rank"])
    p = (ggplot(df, aes("era","rank",group="type")) + geom_line(color=INK, alpha=0.6) + geom_point(color=ACCENT,size=2)
         + geom_text(df[df.era=="2001\u201305"], aes(label="type"), nudge_x=-0.08, ha="right", size=6.5, color=INK)
         + labs(title=ttl("The leaderboard, two decades apart \u2014 ranks hide magnitudes; say so"),
                y="rank (1 = most recorded)", x="",
                caption=capn(28,"A one-rank move can be 10\u00d7 larger than a three-rank move. Should emphasis mark rank change or volume change? Defend the choice."))
         + TH((10,5.8)) + theme(axis_text_y=element_blank()))
    save(p,28,"era_slopegraph")

@fig(29, "lorenz_beats")
def g29(C):
    rows=[]
    for key in ["ALL","THEFT","HOMICIDE"]:
        d=C["beat"].get(key,{}); v=np.sort(np.array(list(d.values()),float))[::-1]
        if len(v)<10: continue
        rows.append(pd.DataFrame({"beats": np.arange(1,len(v)+1)/len(v)*100,
                                  "share": np.cumsum(v)/v.sum()*100, "type": key.title()}))
    df=pd.concat(rows)
    p = (ggplot(df, aes("beats","share",color="type")) + geom_line(size=1.2)
         + geom_segment(x=0,y=0,xend=100,yend=100,color=MUTED,linetype="dotted")
         + scale_color_manual([INK,ACCENT,TEAL])
         + labs(title=ttl("Concentration curves: spatial inequality of records, one color mapping"),
                x="% of police beats (busiest first)", y="% of incidents",
                caption=capn(29,"Beats differ in area and population, and boundaries changed \u2014 concentration of RECORDS, never per-capita risk."))
         + TH((9.5,5.2)))
    save(p,29,"lorenz_beats")

@fig(30, "two_chicagos")
def g30(C):
    tot=sum(C["ca"][i] for i in range(len(C["ca_types"])))
    vio=sum(C["ca"][C["ca_types"].index(t)] for t in C["ca_types"] if t in VIOLENT)
    m=tot>0
    df=pd.DataFrame({"total":tot[m],"vshare":vio[m]/tot[m]*100,"ca":np.where(m)[0]})
    p = (ggplot(df, aes("total","vshare")) + geom_point(color=INK, size=2, alpha=0.8)
         + scale_x_log10() + geom_hline(yintercept=float(df.vshare.median()), color=MUTED, linetype="dotted")
         + labs(title=ttl("Two Chicagos: volume vs violent share \u2014 volume \u2260 danger"),
                x="total incidents (log)", y="violent share %",
                caption=capn(30,"Both axes inherit the authored violent list and unequal populations; tiny denominators make noisy shares. Flag quadrant-flippers under reclassification."))
         + TH((10,5.2)))
    save(p,30,"two_chicagos")

@fig(31, "year_week_tile")
def g31(C):
    x = dser(C,"ALL"); nw=len(x)//7
    wk = x[:nw*7].reshape(nw,7).sum(1)
    df = pd.DataFrame({"week": np.arange(nw)%52, "year": 2001+np.arange(nw)//52, "n": wk})
    df = df[df.year<=2025]
    p = (ggplot(df, aes("week","year",fill="n")) + geom_tile() + scale_fill_cmap("viridis")
         + labs(title=ttl("The spiral, un-coiled: the grammar's answer is the year \u00d7 week tile"),
                x="week of year",
                caption=capn(31,"RESISTANCE as argument: plotnine has no polar coordinates, and the tile beats the spiral at every comparison task (equal-area cells; laps align as rows). The spiral's only win is charm \u2014 which is a rhetorical, not analytic, channel."))
         + TH((11,5)))
    save(p,31,"year_week_tile")

@fig(32, "composition_drift")
def g32(C):
    df = long_monthly(C, C["top_daily"][:8])
    df["n"] = df.groupby("type")["n"].transform(lambda s: s.rolling(12,min_periods=6).mean())
    df = df.dropna()
    p = (ggplot(df, aes("year","n",fill="type")) + geom_area(position=position_fill())
         + scale_fill_manual(PALETTE)
         + labs(title=ttl("What 'crime' is made of: position='fill' IS the 100%-stack \u2014 one keyword, disclosed"),
                y="share (within top 8)",
                caption=capn(32,"Middle stacked layers are hard to read (Byron & Wattenberg) \u2014 the grammar makes the line-per-share alternative a one-word change: remove position_fill, add facets."))
         + TH((11.5,5)))
    save(p,32,"composition_drift")

@fig(33, "story_switch")
def g33(C):
    v = pd.Series(trim_trailing(mser(C,"HOMICIDE"))).rolling(3,min_periods=1).mean().to_numpy()
    yrs = months_axis(C); rows=[]
    for lab, y0 in [("WINDOW A: 2016\u2192  'falling from the 2021 peak'", 2016),
                    ("WINDOW B: 2013\u2192  'still above the mid-2010s floor'", 2013)]:
        m=(yrs>=y0)&(yrs<=2025)
        rows.append(pd.DataFrame({"year":yrs[m],"n":v[m],"window":lab}))
    df=pd.concat(rows)
    p = (ggplot(df, aes("year","n")) + geom_line(color=ACCENT, size=1) + facet_wrap("~window", scales="free_x")
         + labs(title=ttl("The story switch: the window is literally a filter on the tidy frame \u2014 the authored parameter made visible"),
                y="homicides/mo (3-mo avg)",
                caption=capn(33,"Both captions are true; only the filter differs. The grammar's gift: the edit that changes the story is one legible line of data code, not an invisible axis limit."))
         + TH((11.4,4.2)))
    save(p,33,"story_switch")

@fig(34, "anomaly_barcode")
def g34(C):
    x = pd.Series(dser(C,"ALL"))
    base = x.rolling(29,center=True,min_periods=10).median()
    mad = (x-base).abs().rolling(91,center=True,min_periods=30).median()+1e-9
    z = ((x-base)/(1.4826*mad)).clip(-6,6)
    df = pd.DataFrame({"day": np.arange(len(x)), "z": z}).dropna()
    df["year"]=2001+df.day/365.25
    p = (ggplot(df, aes("year",0,fill="z")) + geom_tile(aes(height=1))
         + scale_fill_gradient2(low=TEAL, mid="white", high=ACCENT, limits=(-6,6))
         + labs(title=ttl("The anomaly barcode: a 1-row tile strip; every detector constant is in the caption"),
                y="", caption=capn(34,"Authored numbers: 29-day median, 91-day MAD, 1.4826, clip \u00b16. Re-run at 15/45 \u2014 anomalies that exist at one setting are properties of the detector."))
         + TH((11.5,2.8)) + theme(axis_text_y=element_blank()))
    save(p,34,"anomaly_barcode")

@fig(35, "the_ladder")
def g35(C):
    x = pd.Series(dser(C,"THEFT"), index=pd.date_range(EPOCH, periods=int(C["ndays"]), freq="D"))
    rows=[]
    for rule,lab in [("D","1 daily"),("W","2 weekly"),("ME","3 monthly"),("QE","4 quarterly")]:
        try: v=x.resample(rule).sum()
        except ValueError: v=x.resample(rule.rstrip("E")).sum()
        rows.append(pd.DataFrame({"date":v.index,"n":v.to_numpy(),"rung":lab}))
    df=pd.concat(rows)
    p = (ggplot(df, aes("date","n")) + geom_line(color=INK, size=0.4)
         + facet_wrap("~rung", ncol=1, scales="free_y")
         + labs(title=ttl("The ladder: four resamplings are four facet groups \u2014 the scale choice made explicit and plural"),
                x="", y="",
                caption=capn(35,"scales='free_y' is itself an authored disclosure: each rung on its own axis. For a real claim you still pick a rung \u2014 by the question, not the answer."))
         + TH((11,7)))
    save(p,35,"the_ladder")

# --------------------------------------------------------------------------- main
def main():
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="Crimes_-_2001_to_Present.csv")
    ap.add_argument("--cache", default="chicago_cache.npz")
    ap.add_argument("--out", default="out_chicago_gg")
    ap.add_argument("--only", default="")
    ap.add_argument("--rebuild", action="store_true")
    a = ap.parse_args()
    OUT = a.out
    if a.rebuild or not os.path.exists(a.cache):
        ensure_csv(a.csv)
        build_cache(a.csv, a.cache)
    C = load_cache(a.cache)
    print(f"[gg] {C['rows']:,} rows in cache; rendering with plotnine\u2026")
    want = {int(s) for s in a.only.split(",") if s.strip()} if a.only else None
    ok=fail=0
    for n,name,fn in sorted(FIGS):
        if want and n not in want: continue
        try: fn(C); ok+=1
        except Exception as e:
            fail+=1; print(f"  !! fig {n:02d} {name}: {type(e).__name__}: {e}")
    print(f"[done] {ok} grammar figures in {OUT}/" + (f"  ({fail} failed)" if fail else ""))

if __name__ == "__main__":
    OUT="out_chicago_gg"
    main()
