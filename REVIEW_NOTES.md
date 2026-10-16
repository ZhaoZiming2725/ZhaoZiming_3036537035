# Review record - 16 October 2026

Reviewed against the full course brief and the author paper, codebook and executable check.sas. This revision is based on remote main ec67432, preserving the documented author mirror. The subsequent remote update 7faae89, which includes the public author-equivalent CSV, was also retained during synchronization.

## Corrections

| Finding | Resolution |
|---|---|
| Mean-employment bar chart incorrectly labeled Figure 1 | Replaced with two-wave starting-wage distributions and exported bin counts |
| Table 2 omitted chain/ownership, full-time share, exact-wage shares, full-meal price, recruitment, SEs and tests | Full variable list and counts/SEs/tests added; published-mean comparison exported |
| Table 3 omitted wage groups, contrasts and closure sensitivity | All 40 point estimates reproduced within 0.009 FTE of the printed numbers |
| Table 4 used 384 rather than 357 records and omitted GAP models | All five assigned coefficient/OLS-SE pairs reproduce after rounding |
| Highway/fire closures called permanent; permanent closures said to be newly included in robustness | Separate six permanent and four temporary closures; baseline permanent zeros retained |
| Wage-bite split overlaps original analysis | Ownership interaction conditional on chain used as independent extension; sample sensitivity and HC3 intervals reported |
| Overstated significance and unsupported hand-check claims | Distinguish OLS/HC3 and two-state inference limits; describe only checks actually performed |
| PDF was manually disconnected from code outputs | Generate PDF and HTML from the same computed CSV outputs |
| Raw-source path not verifiable from fresh clone | Optional verified author-data acquisition/conversion script and pinned requirements added |

## Important results

- Table 3 all-available DID: +2.76 FTE; paired (384) DID: +2.75; temporary closures set to zero: +2.51.
- Table 4 coefficients: NJ 2.33, 2.30; GAP 15.65, 14.92, 11.91, with the published conventional SEs after rounding.
- Independent extension, 357 stores: ownership difference in DID -0.94 FTE; HC3 SE 2.64; 95% CI [-6.14, 4.25]; p=0.721. No precise ownership difference is established.
- Wider 384-store extension: interaction -1.14 FTE; p=0.637.

## Source and replication qualifications

- Independently verified all 410 x 46 existing input values against the public author archive; this does not establish the initial acquisition route or entitlement to a data-acquisition bonus.
- The source codebook labels SHEET as unique, but 407 appears once per state; STATE+SHEET is unique. Do not delete either observation.
- Table 3 row-3 SEs are not reconstructed. Point estimates are reproduced; those SEs are left blank rather than copied from a different estimator.
- NJ post-period exact-$5.05 share is 85.50% versus printed 85.2%, a one-store discrepancy in this public release, left visible. Some printed summary tests differ slightly.
- Model v author code excludes ownership, despite the printed table's label; including it changes GAP from 11.91 to 11.98. Both variants are exported. Some residual/F diagnostics differ from the printed table.
- Figure 1 uses explicit modern bins and is not a pixel-identical reproduction.
- HC3 does not address arbitrary within-state dependence; two treated/control states cannot support reliable conventional state-cluster inference.

## What the student should check

Read the revised methods and AI disclosure, verify that the name/student ID are correct, and make sure the teaching team can access the final repository URL. No course submission has been made by this review. No claim is made that the student personally performed AI-assisted checks.

## Validation completed

A fresh directory with no input data successfully downloaded/converted the author archive, ran the complete workflow from a different working directory, reproduced every table CSV byte-for-byte, and generated a seven-page PDF. The final PDF was rendered and inspected; the clipped extension-chart title was shortened and rechecked. The initial review verified raw CSV exclusion; synchronization subsequently preserved remote commit 7faae89, which includes only the verified public author-equivalent CSV. Other raw inputs remain ignored.
