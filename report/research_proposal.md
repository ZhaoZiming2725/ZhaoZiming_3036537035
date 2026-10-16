# Research Proposal — Minimum Wages and Employment (Card & Krueger 1994)

## 1. Question
Does an increase in the minimum wage reduce employment? We test this using the
1992 New Jersey (NJ) minimum-wage hike (to $5.05/h), with eastern Pennsylvania
(PA) as a neighboring control that did not raise its minimum wage.

## 2. Economic reasoning
Competitive labor-market theory predicts a higher binding minimum wage reduces
labor demand (employment falls). The monopsony/efficiency-wage view predicts
employment need not fall — and can rise — when employers have wage-setting
power. **Hypothesis:** if the competitive model holds, NJ fast-food employment
should fall *relative to* PA after April 1992. The empirical DID tells us which
view the data support.

## 3. Measurement
- **Outcome:** store-level full-time-equivalent employment,
  `FTE = EMPFT + 0.5·EMPPT + NMGRS`. Wave 1 = Feb 1992 (pre), wave 2 = Nov 1992
  (post). Source: `data/raw/public.csv`.
- **Treatment indicator:** `STATE` (1 = NJ treated, 0 = PA control).
- **First stage (check):** starting wages. Wave-1 starting wages are ~$4.61/h in
  both states; wave-2 mean rises in NJ to ~$5.08/h (at the new $5.05 floor) while
  PA stays ~$4.62/h — the hike bit in NJ but not in PA.

## 4. Empirical design
Two-period DID on a balanced panel of stores observed in both waves:

```
ΔFTE_i = α + β · NJ_i + ε_i
```

β = (NJ mean ΔFTE) − (PA mean ΔFTE). We also add chain fixed effects and
region/co-ownership controls, and re-include permanently closed stores as zero
employment as a robustness check.

**Sample:** 384 balanced stores (309 NJ, 75 PA); 410 raw stores minus missing
wave-1/wave-2 FTE and closures.

## 5. Interpretation and limitations
- β ≈ +2.75 FTE (t ≈ 2.4): NJ employment rose *relative* to PA — the opposite of
  the competitive prediction, and statistically distinguishable from 0.
- This is association from a border comparison, not a fully identified causal
  effect: NJ and PA could differ on other trends; PA has only 75 stores;
  adding fine region controls shrinks the estimate (≈1.3) and makes it
  insignificant — a sensitivity we discuss.

## 6. Optional extension
Heterogeneity by chain / region, or the effect of the hike on starting-wage
*distribution* (compression near the new $5.05 floor), plus robustness to how
closed stores are counted.

## 7. Pending data checks
1. Confirm FTE convention matches paper means (done: PA 23.4→21.1, NJ 20.4→20.9).
2. Reconcile the small gap to paper means (sample of closed/refused stores).
3. Cluster or at least heteroskedasticity-robust SEs for the report table.
