---
name: minwage-did
description: Replicate the Card & Krueger (1994) New Jersey minimum-wage DID — build the store-level panel, compute mean FTE employment by state and wave, estimate the difference-in-differences, and regenerate the main table and figure. Use when given the fast-food survey CSV (public.csv) and the goal is the employment effect of a minimum-wage hike.
---

# minwage-did — NJ minimum-wage DID workflow

Given a raw store-level survey CSV like `data/raw/public.csv`, reproduce the
Card & Krueger (1994) Table 3 means, the Table 4 DID regressions, and the mean
employment bar figure.

## Input
- A survey CSV with one row per store and columns: `STATE` (1=NJ, 0=PA),
  `EMPFT`, `EMPPT`, `NMGRS` (wave 1) and `EMPFT2`, `EMPPT2`, `NMGRS2` (wave 2),
  plus `CHAIN`, `CO_OWNED`, region dummies, and `STATUS2`.

## Steps
1. **Load & build FTE.** `FTE = EMPFT + 0.5*EMPPT + NMGRS` for each wave.
2. **Define the panel.** Keep stores with non-missing FTE in both waves.
   Record counts of dropped stores (missing wave-1, missing wave-2, closures).
3. **First-stage check.** Compare mean starting wage (`WAGE_ST` vs `WAGE_ST2`)
   by state — the treated state should show a jump to the new minimum.
4. **Table 3 means.** Report mean FTE by state × wave, the within-state change,
   and the DID = (NJ Δ) − (PA Δ).
5. **Table 4 regressions.** Regress `ΔFTE` on `STATE`, then add chain fixed
   effects, then region + co-ownership controls (drop one PA region dummy to
   avoid collinearity with STATE). Report coefficient, SE, t, n, R².
6. **Robustness.** Re-run the DID counting permanently closed stores
   (`STATUS2` in 3,4,5) as zero wave-2 FTE.
7. **Figure.** Bar chart of mean FTE by state, wave 1 vs wave 2.

## Checks (report these)
- Balanced-panel n and the NJ/PA split.
- Did the treated state's starting wage actually rise?
- Does the DID reproduce the paper (≈ +2.7 FTE, positive)?
- Is the coefficient stable when adding chain controls? Note if fine region
  controls shrink it (small PA sample).

## Reproduce
```bash
python3 code/run_all.py
```
Outputs land in `outputs/tables/` and `outputs/figures/`. No manual editing of
data or code is needed after the input CSV is placed in `data/raw/`. This also
builds Table 2 (means of all variables) and the wage-bite extension.
