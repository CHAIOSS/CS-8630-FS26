# Plain plotnine examples — one grammar component per file

Pure plotnine, no presentation machinery. Read them top to bottom; each file
adds or swaps exactly one component and shows the result. Run any file to see
its windows, or `--save DIR` to write PNGs. Start with `01` and go in order.

| File | Component | The one idea |
|---|---|---|
| `01_data_and_mapping.py` | data + mapping | A mapping alone draws nothing |
| `02_geom.py` | geometry | The mark makes the mapping visible; swap it freely |
| `03_stat.py` | statistic | Every geom carries a stat; name its parameter |
| `04_scale.py` | scales | Change the ruler, not the marks (and a colour mismatch to avoid) |
| `05_position.py` | position | stack / dodge / fill: where overlap goes |
| `06_coord.py` | coordinates | Flip; and log-as-coord ≠ log-as-scale (the fit bends) |
| `07_facet.py` | faceting | Aligned panels; the cost of free scales |
| `08_theme_and_defaults.py` | theme + defaults | The explicit spec behind a two-argument chart |

The presenting versions of the same ideas live one directory up
(`g01`–`g10`, one evolving canvas each) and in `../../wilkinson/`.
These plain files are the Assignment 2 starting point.
