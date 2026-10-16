---
name: minwage-did
description: Reproduce the assigned Card-Krueger Tables 2-4 and Figure 1 from the public fast-food survey and test an ownership heterogeneity extension.
---

# Minimum-wage replication workflow

## Input and environment

Install `requirements.txt`. Put the 410-store, 46-column survey CSV at `data/raw/public.csv`, or run `python code/verify_public_source.py --create-input` to obtain it from the public author archive. Do not publish course inputs or credentials.

## Execution

Run `python code/run_all.py` from any working directory after the input exists. This regenerates derived data, full tables, figures, report.pdf, and report/report.html. The main workflow runs offline. Do not manually edit result cells or report estimates.

## Required definitions

- FTE includes managers: EMPFT + 0.5*EMPPT + NMGRS.
- Permanent closure STATUS2=3: wave-2 FTE zero. Temporary closures 2/4/5: missing except Table 3 row 5. Refusal: missing.
- Table 2 uses variable-specific samples; wage indicator denominators and figure denominators are different and documented.
- Table 3 reproduces all five rows and eight groups/contrasts; separate all-available and paired changes. Do not fill row-3 SEs with paired-change SEs.
- Table 4 uses 357 stores: valid employment change and both wages, except retained permanent closures. Reproduce NJ models i/ii and GAP models iii-v. Column v follows author code and omits ownership; report the printed-label discrepancy and ownership-inclusive alternative.
- Figure 1 shows starting-wage distributions, not mean employment.
- The independent extension is the STATE x CO_OWNED interaction conditional on chain, with HC3 intervals and a 384-store sensitivity. Initial-wage comparisons are included in the core replication.

## Validation

Check state counts (331 NJ/79 PA), composite STATE+SHEET key, 384 paired records, 357 regression records, full-rank design matrices, Table 4 published coefficient/OLS-SE benchmarks, Table 3 DIDs (2.75 paired; 2.51 temporary-closure sensitivity), and each wage distribution totaling 100%. Inspect the rendered PDF. Report source discrepancies and two-state inference limitations alongside the results.
