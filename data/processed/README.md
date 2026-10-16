# Processed analysis data

Generated from `data/raw/public.csv` by `code/analysis.py` through `python code/run_all.py`.

- `analysis_all.csv`: all 410 original stores with derived analysis variables and regression eligibility.
- `analysis_panel.csv`: 384 stores with observed pre/post FTE employment, the paired-change sample.

Columns: `store_id` (STATE plus SHEET), `STATE` (1 NJ, 0 PA), `CHAIN`, `CO_OWNED`, `STATUS2`, `fte1`, `fte2`, `dfte`, `gap`, and `regression_sample` (357 eligible stores).

FTE includes managers and half of part-time employees. Permanent closures are zero after treatment; temporary closures are missing except for the explicit Table 3 sensitivity. The full-available Table 2/3 samples and restricted Table 4 sample differ deliberately. See root README and report for details. These derived variables are the analysis frames used for tables and regressions; the workflow reconstructs them from raw inputs rather than trusting edited output CSVs. Do not edit these generated files manually.
