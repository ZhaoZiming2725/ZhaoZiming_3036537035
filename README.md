# Minimum Wages and Employment: Card & Krueger (1994) Replication

Replication of:

> Card, D., & Krueger, A. B. (1994). "Minimum Wages and Employment: A Case Study
> of the Fast-Food Industry in New Jersey and Pennsylvania." *American Economic
> Review*, 84(4), 772–793.

## Research question

Did New Jersey's April 1, 1992 minimum-wage increase ($4.25 → $5.05) reduce
fast-food employment? We compare employment changes in NJ (treatment) to eastern
PA (control, where the minimum stayed $4.25), surveyed in Feb–Mar 1992 and
Nov–Dec 1992. **Result: no employment decline — NJ employment rose relative to
PA (DID ≈ +2.75 FTE; paper reports +2.76).**

## What is replicated

- **Table 2** — means of wages, hours, prices, and FTE by state × wave.
- **Table 3** — mean FTE employment by state × wave and the DID.
- **Table 4** — regression-adjusted DID (`ΔFTE ~ NJ`, with controls).
- **Figure 1** — mean FTE by state and wave (the DID visually).
- **Independent extension** — split NJ stores by whether the new minimum wage
  actually bit (wave-1 wage below vs above $5.05).

## Data source

Raw data: public replication data for Card & Krueger (1994), downloaded from
the Princeton Industrial Relations Section data archive:

- https://irs.princeton.edu/publications/data-sets/minimum-wages-and-employment-chapter-4
- Archived record: http://arks.princeton.edu/ark:/88435/dsp0170795766s

The data are public and can be analyzed in Python, Stata, or R. Per the course
data policy, the raw CSV is **not** included in this public repository; it is
downloaded locally and placed in the documented input folder.

**To reproduce from a fresh clone:** if `data/raw/public.csv` is missing,
download it from the Princeton link above and place it at `data/raw/public.csv`
(the documented input folder); then run `python3 code/run_all.py`. No other
input is required.

## Reproduce everything (one command)

```bash
pip install pandas numpy matplotlib statsmodels
python3 code/run_all.py
```

This regenerates every table in `outputs/tables/` and figure in
`outputs/figures/` directly from `data/raw/public.csv`. No manual editing of
data or code is needed.

## Repository layout

| Path | Contents |
| --- | --- |
| `README.md` | This file. |
| `report/research_proposal.md` | One-page proposal (final report: `report.pdf`). |
| `AI_USE_DISCLOSURE.md` | How AI was used, checked, corrected/rejected. |
| `data/raw/` | Input folder (not in repo): place downloaded `public.csv` here (410-store survey). |
| `data/processed/analysis_panel.csv` | Balanced analysis panel. |
| `code/run_all.py` | One-click reproduction of all outputs. |
| `code/01_make_dataset.py` … `04_extension_wage_bite.py` | Cleaning, tables, extension. |
| `outputs/tables/` | `table2_*`, `table3_means`, `table4_did_regression`, `table_extension_*`. |
| `outputs/figures/` | `fig_mean_fte_by_state`, `fig_extension_wage_bite`. |
| `skills/SKILL.md` | Reusable workflow that regenerates the main tables/figures. |

## Key definitions

- **Treatment** `STATE == 1` = New Jersey; control = Pennsylvania.
- **FTE employment** = `EMPFT + 0.5·EMPPT + NMGRS`.
- **DID** = (NJ mean ΔFTE) − (PA mean ΔFTE), Δ = wave 2 − wave 1.
