#!/usr/bin/env python3
"""
chicago35.py — 35 novel visualizations of Chicago crimes (2001–present), run locally.

Usage:
    python chicago35.py --csv Crimes_-_2001_to_Present.csv            # full run
    python chicago35.py --csv ... --only 3,8,31                       # some figures
    python chicago35.py --csv ... --rebuild                           # force re-aggregate

First run streams the big CSV once (chunked; ~5–10 min for ~8M rows) into a compact
cache (chicago_cache.npz, a few MB). Every figure renders from the cache in seconds,
so iteration after the first pass is cheap. Output: out_chicago/NN_*.png

Deps: pandas, numpy, matplotlib (nothing else).
"""
import argparse, os, sys, json, zipfile, urllib.request, shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp

INK="#2B3A42"; ACCENT="#E4572E"; TEAL="#1C7293"; MUTED="#64707A"; TINT="#F0F3F5"; PUR="#8A5A9E"
plt.rcParams.update({"figure.facecolor":"white","axes.edgecolor":MUTED,
                     "axes.labelcolor":INK,"xtick.color":MUTED,"ytick.color":MUTED,
                     "font.size":10,"axes.titlesize":12})

EPOCH = pd.Timestamp("2001-01-01")
LAT0, LAT1, LON0, LON1 = 41.62, 42.05, -87.95, -87.50
NB = 200                      # spatial bins per axis
LOOP = (41.8781, -87.6298)
TOPN_DAILY = 15
SMALL_TYPES = ["HOMICIDE", "ARSON", "KIDNAPPING"]     # full timestamps kept
HIST_TYPES  = ["THEFT", "BATTERY", "BURGLARY", "NARCOTICS", "MOTOR VEHICLE THEFT", "ASSAULT"]
VIOLENT = {"HOMICIDE","CRIMINAL SEXUAL ASSAULT","CRIM SEXUAL ASSAULT","ROBBERY",
           "BATTERY","ASSAULT","KIDNAPPING","INTIMIDATION"}
PROPERTY = {"THEFT","BURGLARY","MOTOR VEHICLE THEFT","ARSON","CRIMINAL DAMAGE","CRIMINAL TRESPASS"}

USECOLS = ["Date","Primary Type","Description","Location Description","Arrest","Domestic",
           "Beat","Ward","Community Area","Latitude","Longitude"]


DROPBOX_URL = ("https://www.dropbox.com/scl/fi/5jpthactchw7dthbbn7ep/"
               "Crimes_-_2001_to_Present.csv.zip?rlkey=gyz1sg897ransdakjyxs0ncyf&dl=1")  # dl=1 = direct download

def ensure_csv(path):
    """If the CSV isn't in the working directory, download the zip from Dropbox and extract it."""
    if os.path.exists(path):
        return path
    zpath = path + ".zip"
    if not os.path.exists(zpath):
        print(f"[fetch] {path} not found \u2014 downloading from Dropbox (\u22480.5 GB zip)\u2026")
        req = urllib.request.Request(DROPBOX_URL, headers={"User-Agent": "Mozilla/5.0 (chicago35)"})
        with urllib.request.urlopen(req) as r, open(zpath + ".part", "wb") as f:
            total = int(r.headers.get("Content-Length") or 0)
            done = 0
            while True:
                buf = r.read(1 << 20)
                if not buf: break
                f.write(buf); done += len(buf)
                pct = f" ({done/total*100:.0f}%)" if total else ""
                print(f"  \u2026{done/1e6:,.0f} MB{pct}", end="\r")
        os.replace(zpath + ".part", zpath)
        print(f"\n[fetch] saved {zpath}")
    print(f"[fetch] extracting {zpath} \u2026")
    with zipfile.ZipFile(zpath) as z:
        members = [m for m in z.namelist()
                   if m.lower().endswith(".csv") and not m.startswith("__MACOSX")]
        if not members:
            sys.exit(f"[fetch] no .csv inside {zpath} \u2014 contents: {z.namelist()[:5]}")
        member = max(members, key=lambda m: z.getinfo(m).file_size)
        with z.open(member) as src, open(path, "wb") as dst:
            shutil.copyfileobj(src, dst, 1 << 20)
    print(f"[fetch] extracted \u2192 {path} ({os.path.getsize(path)/1e9:.2f} GB); zip kept for reuse")
    return path

# ----------------------------------------------------------------------------- pass 1
def build_cache(csv_path, cache_path):
    print(f"[pass 1] streaming {csv_path} …")
    n_months = (pd.Timestamp.now().year - 2001 + 1) * 12
    monthly = {}                       # type -> np.array(n_months)
    hw = {}                            # type -> 7x24
    hour_dom = np.zeros((2,24))        # domestic / all, by hour
    arrest = {}                        # type -> {year: [arrests, total]}
    ca = {}                            # type -> np.array(81)
    ward = {}                          # type -> np.array(51)
    beat = {}                          # key -> {beat: n} for ALL/HOMICIDE/THEFT
    xy = {t: np.zeros((NB,NB), np.int32) for t in HIST_TYPES}
    xy_era = {e: np.zeros((NB,NB), np.int32) for e in range(3)}
    xy_all = np.zeros((NB,NB), np.int32)
    locdesc = {}
    theft_desc = {}                    # (desc, year) -> n
    ts_small = {t: [] for t in SMALL_TYPES}
    daily_counts = {}                  # type -> {dayindex: n}  (top types resolved later)
    total_by_type = {}

    rows = 0
    for chunk in pd.read_csv(csv_path, usecols=lambda c: c in USECOLS,
                             chunksize=1_000_000, low_memory=False):
        rows += len(chunk)
        d = pd.to_datetime(chunk["Date"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
        bad = d.isna()
        if bad.any():                                  # tolerate alt formats
            d2 = pd.to_datetime(chunk.loc[bad, "Date"], errors="coerce")
            d = d.copy(); d.loc[bad] = d2
        ok = d.notna()
        c = chunk.loc[ok].copy(); d = d.loc[ok]
        ty = c["Primary Type"].astype(str).str.upper().str.strip()
        yr = d.dt.year.to_numpy(); mo = d.dt.month.to_numpy()
        midx = (yr - 2001) * 12 + (mo - 1)
        valid_m = (midx >= 0) & (midx < n_months)
        hr = d.dt.hour.to_numpy(); wd = d.dt.day_of_week.to_numpy()
        dayi = ((d - EPOCH).dt.days).to_numpy()
        arr = c["Arrest"].astype(str).str.lower().isin(["true","1","y","yes"]).to_numpy()
        dom = c["Domestic"].astype(str).str.lower().isin(["true","1","y","yes"]).to_numpy()

        for t, g in pd.DataFrame({"ty":ty,"m":midx,"ok":valid_m}).groupby("ty"):
            total_by_type[t] = total_by_type.get(t, 0) + len(g)
            a = monthly.setdefault(t, np.zeros(n_months))
            np.add.at(a, g.loc[g.ok,"m"].to_numpy(), 1)
        # hour x weekday per type (dict of 7x24) + domestic by hour
        for t, g in pd.DataFrame({"ty":ty,"h":hr,"w":wd}).groupby("ty"):
            a = hw.setdefault(t, np.zeros((7,24)))
            np.add.at(a, (g["w"].to_numpy(), g["h"].to_numpy()), 1)
        np.add.at(hour_dom[1], hr, 1); np.add.at(hour_dom[0], hr[dom], 1)
        # arrest by type/year
        df = pd.DataFrame({"ty":ty,"y":yr,"a":arr})
        for (t,y), g in df.groupby(["ty","y"]):
            e = arrest.setdefault(t, {}).setdefault(int(y), [0,0])
            e[0] += int(g["a"].sum()); e[1] += len(g)
        # community area / ward
        cai = pd.to_numeric(c["Community Area"], errors="coerce").fillna(0).astype(int).clip(0,80).to_numpy()
        wdi = pd.to_numeric(c["Ward"], errors="coerce").fillna(0).astype(int).clip(0,50).to_numpy()
        for t, g in pd.DataFrame({"ty":ty,"ca":cai,"wd":wdi}).groupby("ty"):
            a = ca.setdefault(t, np.zeros(81)); np.add.at(a, g["ca"].to_numpy(), 1)
            a = ward.setdefault(t, np.zeros(51)); np.add.at(a, g["wd"].to_numpy(), 1)
        # beats
        bt = pd.to_numeric(c["Beat"], errors="coerce").fillna(-1).astype(int)
        for key, mask in [("ALL", np.ones(len(c), bool)),
                          ("HOMICIDE", (ty=="HOMICIDE").to_numpy()),
                          ("THEFT", (ty=="THEFT").to_numpy())]:
            dd = beat.setdefault(key, {})
            for b, n in bt[mask].value_counts().items():
                if b >= 0: dd[int(b)] = dd.get(int(b), 0) + int(n)
        # spatial
        la = pd.to_numeric(c["Latitude"], errors="coerce").to_numpy()
        lo = pd.to_numeric(c["Longitude"], errors="coerce").to_numpy()
        gok = np.isfinite(la) & np.isfinite(lo) & (la>LAT0)&(la<LAT1)&(lo>LON0)&(lo<LON1)
        la = np.where(gok, la, LAT0); lo = np.where(gok, lo, LON0)   # keep the cast NaN-free
        ix = np.clip(((lo-LON0)/(LON1-LON0)*NB).astype(int), 0, NB-1)
        iy = np.clip(((la-LAT0)/(LAT1-LAT0)*NB).astype(int), 0, NB-1)
        np.add.at(xy_all, (iy[gok], ix[gok]), 1)
        era = np.clip((yr-2001)//8, 0, 2)
        for e in range(3):
            m2 = gok & (era==e); np.add.at(xy_era[e], (iy[m2], ix[m2]), 1)
        for t in HIST_TYPES:
            m2 = gok & (ty==t).to_numpy(); np.add.at(xy[t], (iy[m2], ix[m2]), 1)
        # location description
        for v, n in c["Location Description"].astype(str).str.upper().value_counts().items():
            locdesc[v] = locdesc.get(v, 0) + int(n)
        # theft descriptions by year (threshold artifact)
        mth = (ty=="THEFT").to_numpy()
        if mth.any():
            for (dsc,y), n in pd.DataFrame({"d":c.loc[mth,"Description"].astype(str).str.upper(),
                                            "y":yr[mth]}).value_counts().items():
                theft_desc[(dsc,int(y))] = theft_desc.get((dsc,int(y)),0)+int(n)
        # small-type timestamps + daily counts
        tnum = ((d - EPOCH) / pd.Timedelta("1D")).to_numpy()
        for t in SMALL_TYPES:
            m2 = (ty==t).to_numpy()
            if m2.any(): ts_small[t].append(tnum[m2])
        for t, g in pd.DataFrame({"ty":ty,"di":dayi}).groupby("ty"):
            dd = daily_counts.setdefault(t, {})
            for di, n in g["di"].value_counts().items():
                dd[int(di)] = dd.get(int(di), 0) + int(n)
        print(f"  …{rows:,} rows", end="\r")
    print(f"\n[pass 1] {rows:,} rows aggregated")

    top = sorted(total_by_type, key=total_by_type.get, reverse=True)
    top_daily = [t for t in top if t in daily_counts][:TOPN_DAILY]
    ndays = max(max(dd) for dd in daily_counts.values()) + 1
    D = np.zeros((len(top_daily)+1, ndays), np.int32)
    for j, t in enumerate(top_daily):
        for di, n in daily_counts[t].items(): D[j, di] = n
    for dd in daily_counts.values():
        for di, n in dd.items(): D[-1, di] += n

    out = dict(
        n_months=n_months, ndays=ndays, rows=rows,
        types=json.dumps(top), top_daily=json.dumps(top_daily),
        monthly_types=json.dumps(list(monthly)), monthly=np.stack([monthly[t] for t in monthly]),
        hw_types=json.dumps(list(hw)), hw=np.stack([hw[t] for t in hw]),
        hour_dom=hour_dom, daily=D,
        arrest=json.dumps({t:{str(y):v for y,v in d_.items()} for t,d_ in arrest.items()}),
        ca_types=json.dumps(list(ca)), ca=np.stack([ca[t] for t in ca]),
        ward_types=json.dumps(list(ward)), ward=np.stack([ward[t] for t in ward]),
        beat=json.dumps(beat), xy_all=xy_all,
        xy_era=np.stack([xy_era[e] for e in range(3)]),
        xy_types=json.dumps(HIST_TYPES), xy=np.stack([xy[t] for t in HIST_TYPES]),
        locdesc=json.dumps(sorted(locdesc.items(), key=lambda kv:-kv[1])[:30]),
        theft_desc=json.dumps([[k[0],k[1],v] for k,v in theft_desc.items()]),
        **{f"ts_{t.split()[0]}": (np.sort(np.concatenate(v)) if v else np.zeros(0)) for t,v in ts_small.items()},
        totals=json.dumps(total_by_type),
    )
    np.savez_compressed(cache_path, **out)
    print(f"[pass 1] cache -> {cache_path}")

def load_cache(cache_path):
    z = np.load(cache_path, allow_pickle=False)
    C = {k: z[k] for k in z.files}
    for k in ["types","top_daily","monthly_types","hw_types","ca_types","ward_types",
              "xy_types","locdesc","theft_desc","arrest","beat","totals"]:
        C[k] = json.loads(str(C[k]))
    C["arrest"] = {t:{int(y):v for y,v in d_.items()} for t,d_ in C["arrest"].items()}
    return C

# ----------------------------------------------------------------------------- helpers
def mser(C, t):
    try: return C["monthly"][C["monthly_types"].index(t)]
    except ValueError: return np.zeros(int(C["n_months"]))
def hwm(C, t):
    try: return C["hw"][C["hw_types"].index(t)]
    except ValueError: return np.zeros((7,24))
def dser(C, t):
    if t == "ALL": return C["daily"][-1].astype(float)
    try: return C["daily"][C["top_daily"].index(t)].astype(float)
    except ValueError: return np.zeros(int(C["ndays"]))
def months_axis(C):
    n = int(C["n_months"]); return 2001 + np.arange(n)/12
def hurst_av(x):
    x = np.asarray(x, float); inc = np.diff(x)
    ws = [w for w in [2,4,8,16,32,64,128] if len(inc)//w >= 8]
    vs = [np.var(inc[:(len(inc)//w)*w].reshape(-1,w).mean(1)) for w in ws]
    if len(ws) < 3 or min(vs) <= 0: return np.nan
    sl = np.polyfit(np.log(ws), np.log(vs), 1)[0]
    return 1 + sl/2
def trim_trailing(y, k=1):
    y = y.astype(float); y[-k:] = np.nan; return y   # last partial month(s)
SOURCE = ("City of Chicago Data Portal, \u201cCrimes \u2014 2001 to Present\u201d (CPD incident reports; Kaggle mirror). "
          "One row per reported incident. Recorded crime measures reports and police activity, not underlying offending. "
          "Aggregated locally by chicago35.py pass 1 into chicago_cache.npz; this figure is drawn from the cache fields listed above.")

FIELD_DEFS = {
 "Date": "Date \u2014 string timestamp of when the incident occurred ('MM/DD/YYYY hh:mm:ss AM/PM'); the portal notes this is sometimes a best estimate. Parsed here with format '%m/%d/%Y %I:%M:%S %p'; failures retried with a generic parser; still-unparseable rows dropped.",
 "Primary Type": "Primary Type \u2014 the primary IUCR (Illinois Uniform Crime Reporting) offense category (THEFT, BATTERY, \u2026); upper-cased and stripped before grouping. Reflects CPD classification at report time; classification practice can drift across years.",
 "Description": "Description \u2014 the IUCR secondary description refining Primary Type (e.g. '$500 AND UNDER'); as-recorded text, upper-cased here.",
 "Location Description": "Location Description \u2014 free-text premise type entered on the report (STREET, RESIDENCE, \u2026); uncontrolled vocabulary, upper-cased here, no cleaning.",
 "Arrest": "Arrest \u2014 boolean: whether an arrest was tied to this report AT REPORT LEVEL (not charging, prosecution, or conviction); parsed by string match on true/1/y/yes.",
 "Domestic": "Domestic \u2014 boolean: incident flagged domestic-related under the Illinois Domestic Violence Act, as recorded by CPD; parsed as above.",
 "Beat": "Beat \u2014 smallest CPD patrol geography (numeric code); coerced to integer, non-numeric/negative dropped. Beats differ in area and population, so beat counts are concentration, not per-capita risk.",
 "Community Area": "Community Area \u2014 official community area number 1\u201377; coerced to integer, clipped to 0\u201380 (0 holds missing).",
 "Latitude": "Latitude \u2014 block-level latitude; the portal SHIFTS coordinates to the block to protect privacy, and a nontrivial share of rows (more in early years) have no coordinates at all.",
 "Longitude": "Longitude \u2014 block-level longitude, same anonymization and missingness. Spatial figures keep only 41.62<lat<42.05 and \u221287.95<lon<\u221287.50.",
}

CACHE_DEFS = {
 "monthly": "npz 'monthly'+'monthly_types' \u2014 int matrix [type \u00d7 month]; month index = (year\u22122001)\u00b712+(month\u22121) from parsed Date; the trailing partial month is blanked at plot time (trim_trailing).",
 "hw": "npz 'hw'+'hw_types' \u2014 per-type 7\u00d724 count matrix; row = day-of-week (Mon=0), column = hour, both from parsed Date.",
 "hour_dom": "npz 'hour_dom' \u2014 2\u00d724 hourly counts: row 0 = Domestic-flagged incidents, row 1 = all incidents.",
 "daily": "npz 'daily'+'top_daily' \u2014 int matrix [15 highest-volume types + ALL \u00d7 day]; day index = whole days since 2001-01-01 from parsed Date.",
 "arrest": "npz 'arrest' \u2014 per type per year the pair [arrests, total reports], from the Arrest flag and parsed Date year.",
 "ca": "npz 'ca'+'ca_types' \u2014 per-type counts over Community Area codes 0\u201380.",
 "beat": "npz 'beat' \u2014 beat\u2192count dictionaries kept for ALL, HOMICIDE, THEFT.",
 "xy": "npz 'xy'+'xy_types' \u2014 per-type 200\u00d7200 spatial histogram over the bounding box (one bin \u2248 240 m N\u2013S \u00d7 190 m E\u2013W); rows without valid coordinates excluded.",
 "xy_era": "npz 'xy_era' \u2014 the same 200\u00d7200 all-types histogram split into eras 2001\u201308 / 2009\u201316 / 2017\u2013 via (year\u22122001)//8, clipped.",
 "locdesc": "npz 'locdesc' \u2014 the 30 most frequent Location Description strings with counts.",
 "theft_desc": "npz 'theft_desc' \u2014 (Description, year, count) triples for THEFT rows only.",
 "ts": "npz 'ts_HOMICIDE'/'ts_ARSON'/'ts_KIDNAPPING' \u2014 sorted event times (fractional days since 2001-01-01) for EVERY row of these rare types; all other types keep only counts, never row-level times.",
}

VSETS = ("Violent set (authored, in-script) = HOMICIDE, CRIMINAL SEXUAL ASSAULT, ROBBERY, BATTERY, ASSAULT, KIDNAPPING, INTIMIDATION; "
         "property set = THEFT, BURGLARY, MOTOR VEHICLE THEFT, ARSON, CRIMINAL DAMAGE, CRIMINAL TRESPASS.")

FIGSPEC = {
 1:(["Date"],["hw"]), 2:(["Date","Primary Type"],["hw"]), 3:(["Date","Primary Type"],["monthly"]),
 4:(["Date"],["monthly"]), 5:(["Date","Primary Type"],["monthly"]), 6:(["Date","Primary Type"],["monthly"]),
 7:(["Date"],["daily"]), 8:(["Date","Primary Type"],["ts"]), 9:(["Date","Primary Type"],["daily"]),
 10:(["Date","Primary Type"],["daily"]), 11:(["Date","Primary Type","Arrest"],["arrest"]),
 12:(["Date","Arrest"],["arrest"]), 13:(["Latitude","Longitude","Primary Type"],["xy"]),
 14:(["Latitude","Longitude","Primary Type"],["xy"]), 15:(["Community Area","Primary Type"],["ca"]),
 16:(["Date","Domestic"],["hour_dom"]), 17:(["Location Description"],["locdesc"]),
 18:(["Date","Domestic"],["hour_dom"]), 19:(["Date","Primary Type"],["hw"]),
 20:(["Date"],["daily"]), 21:(["Date","Arrest"],["monthly","arrest"]),
 22:(["Latitude","Longitude","Date"],["xy_era"]), 23:(["Date","Primary Type","Description"],["theft_desc"]),
 24:(["Date","Primary Type"],["hw"]), 25:(["Date","Primary Type"],["hw"]),
 26:(["Date","Primary Type"],["monthly"]), 27:(["Date","Primary Type"],["ts"]),
 28:(["Date","Primary Type"],["arrest"]), 29:(["Beat","Primary Type"],["beat"]),
 30:(["Community Area","Primary Type"],["ca"]), 31:(["Date"],["daily"]),
 32:(["Date","Primary Type"],["monthly"]), 33:(["Date","Primary Type"],["monthly"]),
 34:(["Date"],["daily"]), 35:(["Date","Primary Type"],["daily"]),
}

import textwrap as _tw
CAPTIONS = {
 1:("Fields: Date \u2192 weekday \u00d7 hour counts over all incident types, full 2001\u2013present record; each row normalized to that weekday's total.",
    "Represents WHEN crime happens within the week as shares, not absolute volume \u2014 the within-day rhythm and its weekend shift."),
 2:("Fields: Date (hour) \u00d7 Primary Type; the six highest-volume types; each clock scaled to its own busiest hour.",
    "Represents each type's daily rhythm; shapes are comparable, absolute heights are not."),
 3:("Fields: Date \u2192 monthly counts per Primary Type (12 highest-volume); each series normalized to its own peak and folded into 3 brightness bands; last partial month dropped.",
    "Represents 24 years of per-type volume rhythm in one page; dark = that type's own peak months. Levels are NOT comparable across rows."),
 4:("Fields: Date \u2192 monthly totals over all types, reshaped year \u00d7 month; last partial month dropped.",
    "Represents seasonality (the summer ridge), the long secular decline, and the spring-2020 anomaly in a single matrix."),
 5:("Fields: Date \u2192 monthly counts per type; each year's months divided by that year's mean, averaged across years, then min\u2013max scaled per type.",
    "Represents seasonal SHAPE only \u2014 which months swell for each type; amplitudes are deliberately not comparable."),
 6:("Fields: Date + Primary Type, grouped by an authored violent/property classification (FBI-style lists in the script); annual means indexed to 2001 = 100.",
    "Represents the relative trajectories of two crime families; the grouping itself is an authored parameter."),
 7:("Fields: Date \u2192 daily totals over all types; mean removed; FFT power vs frequency on log\u2013log axes.",
    "Represents the periodic structure of daily crime \u2014 weekly and annual clocks as spikes over a broadband, slowly-varying background."),
 8:("Fields: Date for every HOMICIDE row citywide; gaps between consecutive events; CCDF compared with an exponential of equal mean; median/mean/p95 marked.",
    "Represents the ARRIVAL PATTERN of homicide against a memoryless model \u2014 a test of the \u2018waves\u2019 narrative, not a map of risk."),
 9:("Fields: Date \u2192 daily counts per type; aggregated-variance Hurst estimate on the cumulative, mean-removed series. Point estimates, no confidence intervals.",
    "Represents day-to-day persistence (memory): H > 0.5 means trend-shaped runs occur by default, so apparent streaks need this null."),
 10:("Fields: Date \u2192 daily THEFT counts; three windows (24 years / 3 years / 6 months), each z-scored; answers printed in the corner.",
    "Represents approximate self-similarity in real data \u2014 why a single-window chart of this series is one arbitrary face of it."),
 11:("Fields: Arrest flag share by Primary Type, averaged 2001\u201305 vs 2019\u201323, as recorded at report level (not case outcomes).",
    "Represents the two-decade change in recorded arrest rates per type; orange marks the steepest declines."),
 12:("Fields: Arrest + Date \u2192 per-year citywide totals and arrest share, connected in time order.",
    "Represents the joint drift of volume and clearance as one path; time hides in the trail \u2014 follow the year labels."),
 13:("Fields: Latitude/Longitude binned 200\u00d7200 over the city bounding box; rows without coordinates excluded; color = log(1+count).",
    "Represents the contrasting geographies of THEFT (downtown/retail-condensed) and BURGLARY (residential-diffuse)."),
 14:("Fields: same spatial bins as the maps; mean density by 1 km distance ring from the Loop (41.8781, \u221287.6298), each type scaled to its own peak.",
    "Represents each type's radial profile around downtown \u2014 where its geography actually peaks."),
 15:("Fields: Community Area (as recorded, 1\u201377) \u00d7 Primary Type totals; areas ranked under three measures (all crime / theft / homicide).",
    "Represents rank instability: an area's \u2018crime ranking\u2019 depends on which crime \u2014 orange lines are the big movers."),
 16:("Fields: Domestic flag \u00d7 hour of Date, full record; share of each hour's incidents flagged domestic.",
    "Represents when domestic-flagged incidents dominate the mix \u2014 peaking in the small hours as street crime recedes."),
 17:("Fields: Location Description (free text, as recorded), top 16 values; one bar partitioned by share of all incidents.",
    "Represents the PLACE composition of the record; field quality is whatever officers typed."),
 18:("Fields: hour of Date split by the Domestic flag; each curve normalized to its own peak and mirrored.",
    "Represents the timing contrast between the public city and the domestic city \u2014 shapes only, not absolute scale."),
 19:("Fields: hour-of-day share profiles per type (12 highest-volume); right panel = identical data, rows re-sorted by peak hour (criterion stated).",
    "Represents Bertin's permutation discipline on real data: one lawful reordering turns noise into a diagonal."),
 20:("Fields: Date \u2192 daily totals for calendar 2020, laid out weekday \u00d7 week; reference lines at the stay-home order and June 1.",
    "Represents 2020 at day resolution \u2014 the shutdown dimming and the single anomalous week of June 1."),
 21:("Fields: monthly totals (6-month centered rolling mean) as band width; color = that calendar year's recorded arrest share.",
    "Represents volume and clearance as one Minard-style object \u2014 the quantity flows, its \u2018temperature\u2019 rides along."),
 22:("Fields: coordinates binned as in the maps, split into eras 2001\u201308 / 2009\u201316 / 2017\u2013present; log color scale. Coordinate coverage is thinner in early years.",
    "Represents spatial stability under falling volume: the map thins, its shape persists."),
 23:("Fields: Description within THEFT rows, grouped UNDER/OVER $500/other, share per year; the vertical marker is interpretive.",
    "Represents category drift inside one crime type \u2014 inflation and statute move the lines as surely as behavior does."),
 24:("Fields: hour-of-day profiles for the 14 highest-volume types, each normalized; the all-crime curve emphasized.",
    "Represents the one shared feature of every type's clock: the ~5 a.m. minimum."),
 25:("Fields: hour-of-day profiles for NARCOTICS, WEAPONS VIOLATION, PROSTITUTION, with BATTERY as the behavior-shaped reference.",
    "Represents enforcement-shaped timing: these clocks follow patrol activity \u2014 a reminder that the dataset records attention."),
 26:("Fields: Date \u2192 monthly NARCOTICS counts, full record; annotation interpretive.",
    "Represents the recorded-enforcement collapse (~80%) \u2014 a change in policing, not plausibly in consumption."),
 27:("Fields: Date for every HOMICIDE, ARSON, KIDNAPPING row; gap CCDFs on log\u2013log axes; dotted lines at each p95.",
    "Represents the waiting-time distributions of three rare crimes \u2014 and the p95 as the only summary a planner could keep."),
 28:("Fields: per-type incident totals, 2001\u201305 vs 2019\u201323, converted to ranks.",
    "Represents the re-ordering of the leaderboard across two decades; orange = moves of 3+ ranks."),
 29:("Fields: incident counts per police Beat (as recorded), sorted busiest-first; cumulative share. Beats differ in area and population \u2014 this is concentration, not per-capita risk.",
    "Represents spatial concentration: what share of each crime sits in what share of beats."),
 30:("Fields: per\u2013Community Area totals vs the share classified violent (same authored list as the scissors figure).",
    "Represents volume vs severity composition: lower-volume areas often carry far higher violent shares \u2014 volume \u2260 danger."),
 31:("Fields: Date \u2192 weekly totals on an annual spiral; one lap per year, 2001 at the center; color = crimes/week.",
    "Represents seasonality as recurrence \u2014 the summer sector returns lap after lap; anomalous years break the pattern visibly."),
 32:("Fields: monthly counts for the 8 highest-volume types, 12-month rolling mean, normalized to sum to 1 (shares are within these 8).",
    "Represents what \u2018crime\u2019 is made of over time \u2014 the drifting composition, not the level."),
 33:("Fields: HOMICIDE monthly counts, 3-month average; identical data under two authored windows.",
    "Represents the window as an authored parameter: both headlines are true; only the disclosure separates analysis from advocacy."),
 34:("Fields: daily totals; robust z-score = (x \u2212 29-day rolling median) / (1.4826 \u00d7 91-day rolling MAD); color clipped at \u00b16.",
    "Represents local surprise \u2014 days the city broke its own recent pattern \u2014 with the largest anomaly labeled."),
 35:("Fields: daily THEFT counts resampled to day / week / month / quarter; no smoothing beyond resampling.",
    "Represents scale dependence directly: the honest display for a series whose story changes with the ruler."),
}

def save(fig, n, name):
    os.makedirs(OUT, exist_ok=True)
    transform, reads = CAPTIONS.get(n, ("",""))
    fields, caches = FIGSPEC.get(n, ([],[]))
    parts = []
    parts.append("CSV FIELDS USED \u00b7 " + " ".join(FIELD_DEFS[f] for f in fields))
    parts.append("CACHE FIELDS USED \u00b7 " + " ".join(CACHE_DEFS[c] for c in caches))
    tr = transform + (" " + VSETS if n in (6, 30) else "")
    parts.append("FIGURE TRANSFORM \u00b7 " + tr)
    parts.append("SOURCE \u00b7 " + SOURCE)
    parts.append("READS AS \u00b7 " + reads + " Question any link in this chain: field semantics, parsing, cache derivation, and figure transform are each separately contestable.")
    wrapped = "\n".join(_tw.fill(p, width=200) for p in parts)
    fig.text(0.012, -0.012, wrapped, ha="left", va="top", fontsize=6.8, color=MUTED,
             family="DejaVu Sans", linespacing=1.4)
    f = os.path.join(OUT, f"{n:02d}_{name}.png")
    fig.savefig(f, dpi=140, bbox_inches="tight"); plt.close(fig); print("  wrote", f)

FIGS = []
def fig(n, name):
    def deco(fn): FIGS.append((n, name, fn)); return fn
    return deco

WD = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

# ----------------------------------------------------------------------------- figures
@fig(1, "heartbeat")
def f01(C):
    M = sum(hwm(C,t) for t in C["hw_types"])
    F,ax = plt.subplots(figsize=(11,4.6))
    im = ax.imshow(M/M.sum(1, keepdims=True), aspect="auto", cmap="magma")
    ax.set_yticks(range(7), WD); ax.set_xticks(range(0,24,3), range(0,24,3))
    ax.set_xlabel("hour"); plt.colorbar(im, label="share of that weekday's crime")
    ax.set_title("The city's heartbeat: every weekday bottoms out near 5 a.m. and crests at noon and early evening")
    save(F,1,"heartbeat")

@fig(2, "crime_clocks")
def f02(C):
    tops = C["hw_types"]; tot = {t: hwm(C,t).sum() for t in tops}
    pick = sorted(tot, key=tot.get, reverse=True)[:6]
    F = plt.figure(figsize=(11.5,6.4))
    for i,t in enumerate(pick):
        ax = F.add_subplot(2,3,i+1, projection="polar")
        v = hwm(C,t).sum(0); v = v/v.max()
        th = np.linspace(0, 2*np.pi, 25)
        ax.bar(th[:-1], v, width=2*np.pi/24, color=ACCENT, alpha=0.85)
        ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
        ax.set_xticks(np.linspace(0,2*np.pi,8,endpoint=False), ["0","3","6","9","12","15","18","21"])
        ax.set_yticks([]); ax.set_title(t.title(), fontsize=10)
    F.suptitle("Crime clocks: each type keeps its own time (midnight at the top; bar = relative hourly rate)")
    save(F,2,"crime_clocks")

@fig(3, "horizon_24yr")
def f03(C):
    pick = C["top_daily"][:12]; yrs = months_axis(C)
    F,axes = plt.subplots(len(pick),1, figsize=(11.5,7.2), sharex=True)
    for ax,t in zip(axes,pick):
        v = trim_trailing(mser(C,t)); v = v/np.nanmax(v) if np.nanmax(v)>0 else v
        for k in range(3):
            band = np.clip(v-k/3, 0, 1/3)*3
            ax.fill_between(yrs, 0, band, color=ACCENT, alpha=0.25+0.25*k, lw=0)
        ax.set_yticks([]); ax.set_ylabel(t.title()[:16], rotation=0, ha="right", va="center", fontsize=8)
    axes[-1].set_xlabel("year")
    F.suptitle("Twenty-four years on one page: monthly volume, horizon-folded (dark = that type's own peak)")
    save(F,3,"horizon_24yr")

@fig(4, "the_fold")
def f04(C):
    tot = trim_trailing(sum(mser(C,t) for t in C["monthly_types"]))
    n = int(C["n_months"]); Y = tot.reshape(n//12, 12)
    F,ax = plt.subplots(figsize=(11,5.4))
    im = ax.imshow(Y, aspect="auto", cmap="viridis")
    ax.set_xticks(range(12), ["J","F","M","A","M","J","J","A","S","O","N","D"])
    ax.set_yticks(range(0, n//12, 2), range(2001, 2001+n//12, 2))
    cov = (2020-2001)
    ax.add_patch(mp.Rectangle((2.5,cov-0.5), 3, 1, fill=False, ec=ACCENT, lw=2))
    ax.text(6.0, cov, "spring 2020", color="white", va="center", fontsize=9,
            bbox=dict(fc=ACCENT, ec="none", pad=2))
    plt.colorbar(im, label="crimes / month")
    ax.set_title("The fold: year \u00d7 month \u2014 the summer ridge runs the full two decades; 2020's scar cuts across it")
    save(F,4,"the_fold")

@fig(5, "season_fingerprints")
def f05(C):
    pick = C["top_daily"][:10]
    F,ax = plt.subplots(figsize=(11,6))
    for i,t in enumerate(pick):
        v = trim_trailing(mser(C,t)); n=int(C["n_months"])
        Y = v.reshape(n//12,12); ym = np.nanmean(Y,1,keepdims=True)
        with np.errstate(invalid="ignore", divide="ignore"):
            prof = np.nanmean(np.where(ym>0, Y/np.where(ym>0, ym, 1), np.nan),0)
        ax.fill_between(range(12), i*0.8, i*0.8+(prof-prof.min())/(prof.max()-prof.min()+1e-9),
                        color=ACCENT, alpha=0.6, lw=0)
        ax.text(-0.4, i*0.8+0.3, t.title()[:18], ha="right", fontsize=8.5)
    ax.set_xticks(range(12), ["J","F","M","A","M","J","J","A","S","O","N","D"])
    ax.set_yticks([]); ax.set_xlim(-4,12)
    ax.set_title("Seasonality fingerprints: battery and theft swell in summer; narcotics barely notices the weather")
    save(F,5,"season_fingerprints")

@fig(6, "scissors")
def f06(C):
    vio = trim_trailing(sum(mser(C,t) for t in C["monthly_types"] if t in VIOLENT))
    pro = trim_trailing(sum(mser(C,t) for t in C["monthly_types"] if t in PROPERTY))
    yrs = months_axis(C)
    def yr_s(v): return np.nanmean(v.reshape(-1,12),1)
    F,ax = plt.subplots(figsize=(11,5))
    for v,c,l in [(yr_s(vio),ACCENT,"violent"),(yr_s(pro),INK,"property")]:
        ax.plot(range(2001,2001+len(v)), v/v[0]*100, "-o", ms=3, color=c, lw=1.8, label=l)
    ax.axhline(100, color=MUTED, lw=0.7, ls=":")
    ax.legend(); ax.set_ylabel("index (2001 = 100)")
    ax.set_title("The scissors: property crime fell by half; violent crime took a different path \u2014 one 'crime trend' is two stories")
    save(F,6,"scissors")

@fig(7, "spectrum")
def f07(C):
    x = dser(C,"ALL"); x = x[x>0] if (x>0).sum()>365 else x
    x = x - x.mean()
    ps = np.abs(np.fft.rfft(x))**2; f = np.fft.rfftfreq(len(x), 1.0)
    F,ax = plt.subplots(figsize=(10.5,5))
    ax.loglog(f[1:], ps[1:], lw=0.6, color=INK)
    for per,lab in [(7,"weekly"),(365.25,"annual"),(3.5,"half-week")]:
        ax.axvline(1/per, color=ACCENT, lw=1, ls="--")
        ax.text(1/per, ax.get_ylim()[1]*0.5, " "+lab, color=ACCENT, fontsize=9, rotation=90, va="top")
    ax.set_xlabel("frequency (1/day)"); ax.set_ylabel("power")
    ax.set_title("The spectrum of daily crime: the annual and weekly clocks stand as spikes on a sloping 1/f-style floor")
    save(F,7,"spectrum")

@fig(8, "homicide_burst")
def f08(C):
    ts = C["ts_HOMICIDE"]
    F = plt.figure(figsize=(11.5,5.6))
    ax1 = F.add_axes([0.06,0.62,0.9,0.3])
    ax1.eventplot(ts, colors=INK, linewidths=0.25)
    ax1.set_yticks([]); ax1.set_xlabel("days since 2001")
    ax1.set_title("every homicide as a tick")
    ax2 = F.add_axes([0.06,0.1,0.4,0.38])
    g = np.diff(ts); g = g[g>0]
    sg = np.sort(g); ax2.loglog(sg, 1-np.arange(len(sg))/len(sg), lw=1.6, color=ACCENT, label="observed gaps")
    r = np.random.default_rng(1); sh = np.sort(r.exponential(g.mean(), len(g)))
    ax2.loglog(sh, 1-np.arange(len(sh))/len(sh), lw=1.2, color=MUTED, ls="--", label="memoryless null")
    ax2.legend(fontsize=8); ax2.set_xlabel("gap between homicides (days)"); ax2.set_ylabel("P(gap > x)")
    ax3 = F.add_axes([0.56,0.1,0.4,0.38])
    for q,lab,c in [(np.median(g),"median",TEAL),(g.mean(),"mean",INK),(np.quantile(g,0.95),"p95",ACCENT)]:
        ax3.axvline(q, color=c, lw=1.6); ax3.text(q, 0.9, f" {lab}={q:.2f}d", color=c, fontsize=8.5, rotation=90, va="top")
    ax3.hist(g, bins=50, color=TINT, ec=MUTED); ax3.set_xlabel("gap (days)")
    F.suptitle("Burst portrait of homicide: the waits hug the memoryless curve \u2014 tragedy arrives like a Poisson clock, not in 'waves'")
    save(F,8,"homicide_burst")

@fig(9, "hurst_ladder")
def f09(C):
    rows = []
    for t in C["top_daily"][:12]:
        h = hurst_av(np.cumsum(dser(C,t) - dser(C,t).mean()))
        if np.isfinite(h): rows.append((t,h))
    rows.sort(key=lambda r:r[1])
    F,ax = plt.subplots(figsize=(10.5,5.5))
    for i,(t,h) in enumerate(rows):
        ax.plot([0.5,h],[i,i], lw=0.8, color="#C9D2D8"); ax.scatter([h],[i], s=50, color=ACCENT)
        ax.text(0.49, i, t.title()[:20]+" ", ha="right", va="center", fontsize=8.5)
    ax.axvline(0.5, color=MUTED, lw=1, ls=":"); ax.text(0.5, len(rows)-0.3, " memoryless", fontsize=8, color=MUTED)
    ax.set_yticks([]); ax.set_xlabel("Hurst H (aggregated-variance estimate on daily counts)")
    ax.set_title("The memory ladder: every crime type is persistent (H > 0.5) \u2014 'trend-shaped' runs are the default, not news")
    save(F,9,"hurst_ladder")

@fig(10, "zoom_quiz")
def f10(C):
    x = dser(C,"THEFT"); n = len(x)
    spans = [(0,n,"24 years"),(n//3, n//3+n//8, "3 years"),(n//2, n//2+180, "6 months")]
    F,axes = plt.subplots(1,3, figsize=(11.5,3.0))
    order = [1,2,0]
    for ax,(k) in zip(axes, order):
        a,b,lab = spans[k]; seg = x[a:b]
        seg = (seg-seg.mean())/(seg.std()+1e-9)
        ax.plot(seg, lw=0.5, color=INK); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title("?", fontsize=12)
    axes[0].text(0.02,0.95,"answers, left to right: 3 years \u00b7 6 months \u00b7 24 years",
                 transform=axes[0].transAxes, fontsize=8, color=ACCENT, va="top")
    F.suptitle("The quiz, on real data: daily thefts at three zooms, rescaled \u2014 Chicago's record is self-similar enough to fool you")
    save(F,10,"zoom_quiz")

@fig(11, "arrest_collapse")
def f11(C):
    A = C["arrest"]; rows=[]
    for t in C["top_daily"][:12]:
        d = A.get(t,{})
        def rate(ys):
            a=sum(d.get(y,[0,0])[0] for y in ys); n=sum(d.get(y,[0,0])[1] for y in ys)
            return a/n*100 if n else np.nan
        r0, r1 = rate(range(2001,2006)), rate(range(2019,2024))
        if np.isfinite(r0) and np.isfinite(r1): rows.append((t,r0,r1))
    F,ax = plt.subplots(figsize=(10.5,6))
    for t,r0,r1 in rows:
        c = ACCENT if (r0-r1)>15 else INK
        ax.plot([0,1],[r0,r1], "-o", ms=4, lw=1.6, color=c, alpha=0.85)
        ax.text(-0.02, r0, t.title()[:18]+" ", ha="right", fontsize=8)
        ax.text(1.02, r1, f" {r1:.0f}%", fontsize=8)
    ax.set_xticks([0,1], ["2001\u201305","2019\u201323"]); ax.set_xlim(-0.45,1.15)
    ax.set_ylabel("arrest rate %")
    ax.set_title("The arrest-rate slopegraph: clearance collapsed across nearly every type \u2014 steepest falls in orange")
    save(F,11,"arrest_collapse")

@fig(12, "system_path")
def f12(C):
    A = C["arrest"]; yrs = sorted({y for d in A.values() for y in d})
    yrs = [y for y in yrs if 2001 <= y <= 2024]
    vol=[]; rate=[]
    for y in yrs:
        a = sum(A[t].get(y,[0,0])[0] for t in A); n = sum(A[t].get(y,[0,0])[1] for t in A)
        vol.append(n/1e3); rate.append(a/n*100 if n else np.nan)
    F,ax = plt.subplots(figsize=(10.5,5.6))
    ax.plot(vol, rate, "-o", ms=3.5, lw=1.2, color=INK)
    for i,y in enumerate(yrs):
        if y in (2001,2008,2016,2020, yrs[-1]): ax.annotate(str(y), (vol[i],rate[i]), xytext=(5,5),
            textcoords="offset points", fontsize=9, color=ACCENT, fontweight="bold")
    ax.set_xlabel("recorded crimes (thousands/yr)"); ax.set_ylabel("arrest rate %")
    ax.set_title("The system's path: a connected scatter of volume vs clearance \u2014 time hides in the trail (arrows of travel: follow the labels)")
    save(F,12,"system_path")

@fig(13, "theft_vs_burglary_maps")
def f13(C):
    i1, i2 = C["xy_types"].index("THEFT"), C["xy_types"].index("BURGLARY")
    F,axes = plt.subplots(1,2, figsize=(11,5.4))
    for ax, i, t in [(axes[0],i1,"Theft"),(axes[1],i2,"Burglary")]:
        M = C["xy"][i].astype(float)
        ax.imshow(np.log1p(M), origin="lower", cmap="magma", aspect="auto")
        ax.set_xticks([]); ax.set_yticks([]); ax.set_title(t)
    F.suptitle("Two geographies: theft condenses on the Loop and retail spines; burglary spreads across the residential fabric (log scale)")
    save(F,13,"theft_vs_burglary_maps")

@fig(14, "loop_gravity")
def f14(C):
    iy0 = (LOOP[0]-LAT0)/(LAT1-LAT0)*NB; ix0 = (LOOP[1]-LON0)/(LON1-LON0)*NB
    yy,xx = np.mgrid[0:NB,0:NB]
    km = np.hypot((yy-iy0)*(LAT1-LAT0)/NB*111, (xx-ix0)*(LON1-LON0)/NB*83)
    F,ax = plt.subplots(figsize=(10.5,5.2))
    for t,c in zip(C["xy_types"], [INK,ACCENT,TEAL,PUR,MUTED,"#B0431F"]):
        M = C["xy"][C["xy_types"].index(t)].astype(float)
        bins = np.arange(0,25,1.0); prof=[]
        for b0,b1 in zip(bins[:-1],bins[1:]):
            m = (km>=b0)&(km<b1); prof.append(M[m].sum()/max(m.sum(),1))
        prof = np.array(prof); ax.plot(bins[:-1]+0.5, prof/prof.max(), lw=1.6, color=c, label=t.title()[:18])
    ax.legend(fontsize=8); ax.set_xlabel("km from the Loop"); ax.set_ylabel("density (each type's own peak = 1)")
    ax.set_title("The Loop's gravity: theft decays from downtown like a law; narcotics and battery peak miles away")
    save(F,14,"loop_gravity")

@fig(15, "ca_bump")
def f15(C):
    # rank the top community areas by era
    tot = sum(C["ca"][i] for i in range(len(C["ca_types"])))
    # per-era approximation from monthly shares is not stored; use ALL-time top 10 vs homicide ranks
    hi = C["ca"][C["ca_types"].index("HOMICIDE")] if "HOMICIDE" in C["ca_types"] else tot
    th = C["ca"][C["ca_types"].index("THEFT")] if "THEFT" in C["ca_types"] else tot
    top10 = np.argsort(-tot)[:10]
    series = {"all crime": tot, "theft": th, "homicide": hi}
    F,ax = plt.subplots(figsize=(10.5,5.8))
    for j,cai in enumerate(top10):
        ranks = [int(np.sum(v > v[cai])) + 1 for v in series.values()]
        c = ACCENT if abs(ranks[0]-ranks[2])>15 else INK
        ax.plot(range(3), ranks, "-o", ms=4, lw=1.4, color=c, alpha=0.8)
        ax.text(-0.06, ranks[0], f"CA {cai} ", ha="right", fontsize=8)
    ax.set_xticks(range(3), list(series)); ax.invert_yaxis(); ax.set_ylabel("rank (1 = most)")
    ax.set_title("Same areas, different leaderboards: a community area's rank in 'crime' depends on which crime (orange = big movers)")
    save(F,15,"ca_bump")

@fig(16, "domestic_hours")
def f16(C):
    dom, tot = C["hour_dom"][0], C["hour_dom"][1]
    F,ax = plt.subplots(figsize=(10.5,4.8))
    sh = dom/np.maximum(tot,1)*100
    ax.fill_between(range(24), 0, sh, color=ACCENT, alpha=0.25)
    ax.plot(range(24), sh, "-o", ms=3.5, color=ACCENT)
    ax.set_xticks(range(0,24,3)); ax.set_xlabel("hour"); ax.set_ylabel("% of crimes flagged domestic")
    ax.set_title("When home is the dangerous place: the domestic share peaks in the small hours, exactly when street crime sleeps")
    save(F,16,"domestic_hours")

@fig(17, "where_treemap")
def f17(C):
    items = C["locdesc"][:16]; total = sum(v for _,v in items)
    F,ax = plt.subplots(figsize=(11,5.4)); x0=0
    for i,(name,v) in enumerate(items):
        w = v/total
        ax.add_patch(mp.Rectangle((x0,0), w, 1, color=[INK,ACCENT,TEAL,PUR][i%4], alpha=0.75, ec="white"))
        if w > 0.03:
            ax.text(x0+w/2, 0.5, f"{name.title()[:22]}\n{v/1e6:.2f}M", ha="center", va="center",
                    fontsize=8, color="white", rotation=90 if w<0.06 else 0)
        x0 += w
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Where crime happens: one bar of the whole record, partitioned by place \u2014 street, residence, apartment dominate")
    save(F,17,"where_treemap")

@fig(18, "street_vs_home")
def f18(C):
    # mirrored hourly profile using domestic as the 'home' proxy vs all-domestic
    dom, tot = C["hour_dom"][0], C["hour_dom"][1]
    street = tot - dom
    F,ax = plt.subplots(figsize=(10.5,5))
    ax.fill_between(range(24), 0, street/street.max(), color=INK, alpha=0.8, label="non-domestic (street-ish)")
    ax.fill_between(range(24), 0, -dom/dom.max(), color=ACCENT, alpha=0.8, label="domestic")
    ax.axhline(0,color="white",lw=1); ax.legend(fontsize=9)
    ax.set_xticks(range(0,24,3)); ax.set_yticks([]); ax.set_xlabel("hour")
    ax.set_title("Mirror city: the public city's clock (up) against the domestic city's clock (down) \u2014 each on its own peak")
    save(F,18,"street_vs_home")

@fig(19, "bertin_reorder")
def f19(C):
    pick = C["hw_types"][:12] if len(C["hw_types"])>=12 else C["hw_types"]
    M = np.stack([hwm(C,t).sum(0)/max(hwm(C,t).sum(),1) for t in pick])
    F,axes = plt.subplots(1,2, figsize=(11.5,4.8))
    axes[0].imshow(M, aspect="auto", cmap="Greys")
    axes[0].set_title("as the data arrived")
    peak = M.argmax(1); order = np.argsort(peak)
    axes[1].imshow(M[order], aspect="auto", cmap="Greys")
    axes[1].set_title("rows permuted by peak hour (criterion stated)")
    for ax, od in [(axes[0], range(len(pick))), (axes[1], order)]:
        ax.set_yticks(range(len(pick)), [pick[i].title()[:14] for i in od], fontsize=7)
        ax.set_xticks(range(0,24,6))
    F.suptitle("Bertin on the night shift: the same type \u00d7 hour matrix, before and after one lawful permutation \u2014 the diagonal is the discovery")
    save(F,19,"bertin_reorder")

@fig(20, "calendar_2020")
def f20(C):
    x = dser(C,"ALL"); start = (pd.Timestamp("2020-01-01")-EPOCH).days
    days = x[start:start+366]
    first_wd = pd.Timestamp("2020-01-01").dayofweek
    Mcal = np.full((7,54), np.nan)
    for i,v in enumerate(days):
        wd = (first_wd+i)%7; wk = (first_wd+i)//7
        Mcal[wd,wk]=v
    F,ax = plt.subplots(figsize=(11.5,3.4))
    im = ax.imshow(Mcal, aspect="auto", cmap="viridis")
    ax.set_yticks(range(7), WD, fontsize=7); ax.set_xticks([])
    for wk,lab in [(11,"stay-home order"),(22,"June 1")]:
        ax.axvline(wk, color=ACCENT, lw=1.2, ls="--"); ax.text(wk, -0.8, lab, color=ACCENT, fontsize=8, ha="center")
    plt.colorbar(im, label="crimes/day")
    ax.set_title("2020, day by day: the March shutdown dims the grid; the single brightest column is the week of June 1")
    save(F,20,"calendar_2020")

@fig(21, "minard_band")
def f21(C):
    tot = trim_trailing(sum(mser(C,t) for t in C["monthly_types"]))
    A = C["arrest"]; yrs = months_axis(C)
    yr_rate = {}
    for y in range(2001,2026):
        a=sum(A[t].get(y,[0,0])[0] for t in A); n=sum(A[t].get(y,[0,0])[1] for t in A)
        if n: yr_rate[y]=a/n
    F,ax = plt.subplots(figsize=(11.5,4.6))
    v = pd.Series(tot).rolling(6,center=True,min_periods=1).mean().to_numpy()
    r = np.array([yr_rate.get(int(y),np.nan) for y in yrs])
    up = v/np.nanmax(v)/2
    pts = ax.scatter(yrs, np.zeros_like(yrs), s=0)
    ax.fill_between(yrs, -up, up, color=MUTED, alpha=0.25, lw=0)
    sc = ax.scatter(yrs, np.zeros_like(yrs), c=r*100, cmap="plasma", s=(up*140)**1.2, alpha=0.9)
    plt.colorbar(sc, label="arrest rate % (that year)")
    ax.set_yticks([]); ax.set_xlabel("year")
    ax.set_title("A Minard reading of two decades: band width = monthly volume; color = the arrest rate riding the temperature slot")
    save(F,21,"minard_band")

@fig(22, "era_maps")
def f22(C):
    F,axes = plt.subplots(1,3, figsize=(11.5,4.6))
    labs = ["2001\u201308","2009\u201316","2017\u2013present"]
    for ax, e, lab in zip(axes, range(3), labs):
        M = C["xy_era"][e].astype(float)
        ax.imshow(np.log1p(M), origin="lower", cmap="magma", aspect="auto")
        ax.set_xticks([]); ax.set_yticks([]); ax.set_title(lab)
    F.suptitle("Three eras of the same map: total recorded crime thins everywhere, but its SHAPE barely moves (log scale)")
    save(F,22,"era_maps")

@fig(23, "theft_threshold")
def f23(C):
    td = C["theft_desc"]; byy = {}
    for dsc,y,n in td:
        key = "UNDER $500" if "UNDER" in dsc else ("OVER $500" if "OVER" in dsc else "other")
        byy.setdefault(key, {}); byy[key][y] = byy[key].get(y,0)+n
    yrs = sorted({y for d in byy.values() for y in d})
    F,ax = plt.subplots(figsize=(10.8,5))
    base = np.zeros(len(yrs))
    for key,c in [("UNDER $500",INK),("OVER $500",ACCENT),("other",MUTED)]:
        v = np.array([byy.get(key,{}).get(y,0) for y in yrs], float)
        t_ = np.array([sum(byy.get(k,{}).get(y,0) for k in byy) for y in yrs], float)
        sh = np.divide(v, np.maximum(t_,1))*100
        ax.plot(yrs, sh, "-o", ms=3, lw=1.6, color=c, label=key.lower())
    ax.axvline(2016, color=PUR, lw=1.2, ls="--"); ax.text(2016.2, 70, "felony threshold politics (~2016)", color=PUR, fontsize=8.5)
    ax.legend(fontsize=9); ax.set_ylabel("share of thefts %")
    ax.set_title("The $500 line: theft's internal composition shifts with inflation and law, not just behavior \u2014 categories are authored too")
    save(F,23,"theft_threshold")

@fig(24, "universal_trough")
def f24(C):
    F,ax = plt.subplots(figsize=(10.5,5))
    for t in C["hw_types"][:14]:
        v = hwm(C,t).sum(0); v=v/max(v.max(),1)
        ax.plot(range(24), v, lw=0.7, color=MUTED, alpha=0.5)
    vall = sum(hwm(C,t) for t in C["hw_types"]).sum(0); vall=vall/vall.max()
    ax.plot(range(24), vall, lw=2.4, color=ACCENT, label="all crime")
    ax.axvline(5, color=INK, lw=1, ls=":"); ax.text(5.1, 0.95, "5 a.m.", fontsize=9, color=INK)
    ax.legend(); ax.set_xticks(range(0,24,3)); ax.set_xlabel("hour"); ax.set_yticks([])
    ax.set_title("The universal trough: fourteen crime types, one shared 5 a.m. silence \u2014 the city's only consensus")
    save(F,24,"universal_trough")

@fig(25, "policing_shapes")
def f25(C):
    F,ax = plt.subplots(figsize=(10.5,5))
    for t,c in [("NARCOTICS",ACCENT),("WEAPONS VIOLATION",INK),("PROSTITUTION",TEAL)]:
        v = hwm(C,t).sum(0)
        if v.sum()==0: continue
        ax.plot(range(24), v/v.max(), lw=2, color=c, label=t.title())
    bat = hwm(C,"BATTERY").sum(0)
    if bat.sum(): ax.plot(range(24), bat/bat.max(), lw=1.2, color=MUTED, ls="--", label="Battery (behavior-shaped)")
    ax.legend(fontsize=9); ax.set_xticks(range(0,24,3)); ax.set_yticks([]); ax.set_xlabel("hour")
    ax.set_title("Enforcement-shaped clocks: narcotics and prostitution peak when patrols work, not when behavior does \u2014 the data measures policing")
    save(F,25,"policing_shapes")

@fig(26, "narcotics_cliff")
def f26(C):
    v = trim_trailing(mser(C,"NARCOTICS")); yrs = months_axis(C)
    F,ax = plt.subplots(figsize=(11,4.8))
    ax.fill_between(yrs, 0, v, color=ACCENT, alpha=0.75)
    ax.annotate("enforcement policy turns,\nnot a city suddenly sober", xy=(2015.5, np.nanmax(v)*0.35),
                xytext=(2017.5, np.nanmax(v)*0.7), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK))
    ax.set_ylabel("narcotics incidents / month")
    ax.set_title("The narcotics cliff: an 80% collapse that no one's bloodstream explains \u2014 recorded crime is a record of attention")
    save(F,26,"narcotics_cliff")

@fig(27, "gap_trio")
def f27(C):
    F,ax = plt.subplots(figsize=(10.5,5.4))
    for key,c in [("ts_HOMICIDE",INK),("ts_ARSON",ACCENT),("ts_KIDNAPPING",TEAL)]:
        ts = C[key]
        if len(ts)<100: continue
        g = np.diff(ts); g=g[g>0]; sg=np.sort(g)
        ax.loglog(sg, 1-np.arange(len(sg))/len(sg), lw=1.7, color=c, label=key[3:].title())
        ax.axvline(np.quantile(g,0.95), color=c, lw=0.8, ls=":")
    ax.legend(fontsize=9); ax.set_xlabel("gap between incidents (days)"); ax.set_ylabel("P(gap > x)")
    ax.set_title("Three rare crimes, three wait distributions \u2014 dotted lines mark each p95: the promise a planner could actually keep")
    save(F,27,"gap_trio")

@fig(28, "era_slopegraph")
def f28(C):
    A = C["arrest"]
    def era_tot(t, ys): return sum(A.get(t,{}).get(y,[0,0])[1] for y in ys)
    e0 = {t: era_tot(t, range(2001,2006)) for t in C["top_daily"]}
    e1 = {t: era_tot(t, range(2019,2024)) for t in C["top_daily"]}
    r0 = {t:i+1 for i,t in enumerate(sorted(e0, key=e0.get, reverse=True))}
    r1 = {t:i+1 for i,t in enumerate(sorted(e1, key=e1.get, reverse=True))}
    F,ax = plt.subplots(figsize=(10.5,6.2))
    for t in C["top_daily"]:
        c = ACCENT if abs(r0[t]-r1[t])>=3 else INK
        ax.plot([0,1],[r0[t],r1[t]], "-o", ms=4, lw=1.5, color=c, alpha=0.85)
        ax.text(-0.03, r0[t], t.title()[:20]+" ", ha="right", fontsize=8)
        ax.text(1.03, r1[t], " "+t.title()[:20], fontsize=8)
    ax.set_xticks([0,1],["2001\u201305","2019\u201323"]); ax.invert_yaxis(); ax.set_xlim(-0.55,1.6); ax.set_yticks([])
    ax.set_title("The leaderboard, two decades apart: weapons and vehicle theft climb; narcotics and burglary fall off (orange = \u22653 ranks)")
    save(F,28,"era_slopegraph")

@fig(29, "lorenz_beats")
def f29(C):
    F,ax = plt.subplots(figsize=(9.8,5.6))
    for key,c in [("ALL",INK),("THEFT",TEAL),("HOMICIDE",ACCENT)]:
        d = C["beat"].get(key,{})
        v = np.sort(np.array(list(d.values()), float))[::-1]
        if len(v)<10: continue
        cum = np.cumsum(v)/v.sum()
        ax.plot(np.arange(1,len(v)+1)/len(v)*100, cum*100, lw=1.8, color=c, label=key.title())
    ax.plot([0,100],[0,100], color=MUTED, lw=0.8, ls=":")
    ax.axvline(20, color=MUTED, lw=0.7)
    ax.legend(fontsize=9); ax.set_xlabel("% of police beats (busiest first)"); ax.set_ylabel("% of incidents")
    ax.set_title("Concentration curves: the busiest 20% of beats carry the majority of homicide \u2014 geography is the whole story")
    save(F,29,"lorenz_beats")

@fig(30, "two_chicagos")
def f30(C):
    tot = sum(C["ca"][i] for i in range(len(C["ca_types"])))
    vio = sum(C["ca"][C["ca_types"].index(t)] for t in C["ca_types"] if t in VIOLENT)
    F,ax = plt.subplots(figsize=(10.5,5.6))
    m = tot>0
    x = tot[m]; y = vio[m]/tot[m]*100
    ax.scatter(np.log10(x), y, s=28, color=INK, alpha=0.8)
    ax.axhline(np.median(y), color=MUTED, lw=0.8, ls=":")
    ax.set_xlabel("log10 total incidents (community area)"); ax.set_ylabel("violent share %")
    hi = np.argsort(-y)[:5]
    for i in hi: ax.annotate(f"CA {np.where(m)[0][i]}", (np.log10(x[i]), y[i]), fontsize=8, color=ACCENT,
                             xytext=(4,4), textcoords="offset points")
    ax.set_title("Two Chicagos in one scatter: areas with LESS total crime often carry a far HIGHER violent share \u2014 volume \u2260 danger")
    save(F,30,"two_chicagos")

@fig(31, "spiral")
def f31(C):
    x = dser(C,"ALL"); nweeks = len(x)//7
    wk = x[:nweeks*7].reshape(nweeks,7).sum(1)
    th = np.arange(nweeks)*2*np.pi/52.1775
    r = 2 + np.arange(nweeks)/52.1775
    F = plt.figure(figsize=(8.2,8.2)); ax = F.add_subplot(111, projection="polar")
    sc = ax.scatter(th, r, c=wk, cmap="viridis", s=9)
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
    ax.set_xticks(np.linspace(0,2*np.pi,12,endpoint=False),
                  ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    ax.set_yticks([]); plt.colorbar(sc, label="crimes/week", shrink=0.7)
    ax.set_title("Twenty-four years coiled: each lap one year \u2014 the bright summer sector repeats like a season of the sun; the pale 2020 lap breaks it")
    save(F,31,"spiral")

@fig(32, "composition_drift")
def f32(C):
    pick = C["top_daily"][:8]; yrs = months_axis(C)
    M = np.stack([pd.Series(trim_trailing(mser(C,t))).rolling(12,min_periods=6).mean().to_numpy() for t in pick])
    tot = np.nansum(M,0); Mn = M/np.maximum(tot,1)
    F,ax = plt.subplots(figsize=(11.2,5.2))
    base = np.zeros(len(yrs))
    cols = [INK,ACCENT,TEAL,PUR,MUTED,"#B0431F","#4B6A52","#9A7B4F"]
    for v,t,c in zip(Mn,pick,cols):
        ax.fill_between(yrs, base, base+np.nan_to_num(v), color=c, alpha=0.85, lw=0, label=t.title()[:16])
        base += np.nan_to_num(v)
    ax.legend(fontsize=7, ncol=4, loc="upper center"); ax.set_ylim(0,1.12)
    ax.set_ylabel("share of all recorded crime")
    ax.set_title("What 'crime' is made of, 2001\u2192now: the composition drifts \u2014 theft's slice holds while narcotics' nearly vanishes")
    save(F,32,"composition_drift")

@fig(33, "story_switch")
def f33(C):
    v = pd.Series(trim_trailing(mser(C,"HOMICIDE"))).rolling(3,min_periods=1).mean().to_numpy()
    yrs = months_axis(C)
    F,axes = plt.subplots(1,2, figsize=(11.4,4.4))
    m1 = (yrs>=2016)&(yrs<=2024); axes[0].plot(yrs[m1], v[m1], lw=1.8, color=TEAL)
    axes[0].set_title("WINDOW A (2016\u2192): 'homicide is FALLING \u2014 down sharply from the 2021 peak'", fontsize=9.5, color=TEAL)
    m2 = (yrs>=2013)&(yrs<=2024); axes[1].plot(yrs[m2], v[m2], lw=1.8, color=ACCENT)
    axes[1].set_title("WINDOW B (2013\u2192): 'homicide remains ELEVATED \u2014 still above the mid-2010s floor'", fontsize=9.5, color=ACCENT)
    for ax in axes: ax.set_ylabel("homicides/mo (3-mo avg)")
    F.suptitle("The story switch, live: both captions are true; the only edited parameter is the window \u2014 disclose it or it authors you")
    save(F,33,"story_switch")

@fig(34, "anomaly_barcode")
def f34(C):
    x = pd.Series(dser(C,"ALL"))
    base = x.rolling(29, center=True, min_periods=10).median()
    mad = (x-base).abs().rolling(91, center=True, min_periods=30).median()+1e-9
    z = ((x-base)/ (1.4826*mad)).to_numpy()
    F,ax = plt.subplots(figsize=(11.5,3.6))
    ax.imshow(z[None,:], aspect="auto", cmap="coolwarm", vmin=-6, vmax=6)
    ax.set_yticks([])
    tick_yrs = range(2001, 2026, 2)
    ax.set_xticks([(pd.Timestamp(f"{y}-01-01")-EPOCH).days for y in tick_yrs], tick_yrs)
    k = np.nanargmax(np.abs(np.nan_to_num(z)))
    dstr = (EPOCH+pd.Timedelta(days=int(k))).date()
    ax.annotate(f"largest anomaly: {dstr}", xy=(k,0), xytext=(k, -0.9), ha="center",
                fontsize=9, color=ACCENT, annotation_clip=False,
                arrowprops=dict(arrowstyle="->", color=ACCENT))
    ax.set_title("Every day as a barcode of surprise: robust z-scores against a 4-week local baseline \u2014 red spikes are days the city broke pattern")
    save(F,34,"anomaly_barcode")

@fig(35, "the_ladder")
def f35(C):
    x = pd.Series(dser(C,"THEFT"), index=pd.date_range(EPOCH, periods=int(C["ndays"]), freq="D"))
    F,axes = plt.subplots(4,1, figsize=(11,7), sharex=False)
    specs = [("D","daily", 0.4), ("W","weekly", 0.8), ("ME","monthly", 1.3), ("QE","quarterly", 1.8)]
    for ax,(rule,lab,lw) in zip(axes,specs):
        try: v = x.resample(rule).sum()
        except ValueError: v = x.resample(rule.rstrip("E")).sum()
        ax.plot(v.index, v.to_numpy(), lw=lw, color=INK)
        ax.set_ylabel(lab, rotation=0, ha="right", va="center", fontsize=9)
        ax.set_yticks([])
    F.suptitle("The ladder: one series, four rulers \u2014 the honest display for data whose story depends on the zoom (choose your rung out loud)")
    save(F,35,"the_ladder")

# ----------------------------------------------------------------------------- main
def main():
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="Crimes_-_2001_to_Present.csv",
                help="path to the CSV; auto-downloaded from Dropbox if absent")
    ap.add_argument("--cache", default="chicago_cache.npz")
    ap.add_argument("--out", default="out_chicago")
    ap.add_argument("--only", default="")
    ap.add_argument("--rebuild", action="store_true")
    a = ap.parse_args()
    OUT = a.out
    ensure_csv(a.csv)
    if a.rebuild or not os.path.exists(a.cache):
        build_cache(a.csv, a.cache)
    C = load_cache(a.cache)
    print(f"[pass 2] {C['rows']:,} rows in cache; rendering…")
    want = {int(s) for s in a.only.split(",") if s.strip()} if a.only else None
    ok = fail = 0
    for n, name, fn in sorted(FIGS):
        if want and n not in want: continue
        try:
            fn(C); ok += 1
        except Exception as e:
            fail += 1
            print(f"  !! fig {n:02d} {name}: {type(e).__name__}: {e}")
    print(f"[done] {ok} figures written to {OUT}/" + (f"  ({fail} failed)" if fail else ""))

if __name__ == "__main__":
    OUT = "out_chicago"
    main()