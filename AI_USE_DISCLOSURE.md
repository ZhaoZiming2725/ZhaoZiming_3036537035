# AI-Use Disclosure

## Scope

AI assisted initial project drafting and the subsequent review: data definitions, empirical specifications, Python code, source comparisons, extension design, documentation and report writing. The final review uses the author paper, codebook and check.sas rather than trusting a headline estimate.

## Checks actually performed in the review

- Downloaded the author public archive and compared all 410 x 46 CSV values, including missingness. They matched. The verification script and hashes document the check; the original acquisition route is not established.
- Recomputed all tables and figures programmatically; used sample-count, composite-key, matrix-rank and numeric benchmark assertions.
- Compared 40 Table 3 point estimates and five Table 4 coefficients/conventional SEs to the paper. All point estimates are within rounding and all Table 4 coefficient/SE pairs round to the published values.
- Added HC3 inference sensitivity and ownership-extension intervals; ran the alternative employment-only extension sample.
- Regenerated report PDF/HTML from computed CSV outputs, rendered and visually checked the PDF, and checked fresh-input reproduction.

These are computer-assisted checks. An earlier statement that every number had been recomputed "by hand" was unsupported and has been removed. The student should personally inspect and understand the final analysis before submission; this disclosure does not assert student-only verification that was not observed.

## Errors corrected or rejected

1. **Wrong Figure 1:** a mean-employment bar chart was labeled as the original Figure 1. The actual figure shows starting-wage distributions in both states before and after the change. It has been replaced.
2. **Incomplete assigned tables:** replaced a few selected means with the full Table 2 variable list and Table 3 groups/rows; reconstructed all five Table 4 models.
3. **Wrong Table 4 sample:** 384-store employment-paired regressions do not reproduce the 357-store wage-and-employment sample. Both sample definitions are now explicit.
4. **Closure confusion:** the six permanent closures already have zero employment in the public data. Highway/fire/renovation closures are temporary; they are zero only in the corresponding sensitivity. They are not reclassified as permanent closures.
5. **Specification and collinearity confusion:** NJ plus all location dummies is collinear, but the assigned model v uses GAP, not NJ. Both PA dummies are valid with GAP and the omitted NJ reference region. The author model-v ownership omission and printed-label discrepancy are disclosed.
6. **Extension overlap:** the original paper already analyzes initial wages/wage gaps. A wage-bite split alone is no longer called an independent extension; a conditional ownership interaction and sample sensitivity are used instead.
7. **Overconfident interpretation:** a positive coefficient does not prove a positive policy effect. Conventional and HC3 results are distinguished, and the two-state inference limitation is explicit.
8. **FTE definition:** managers are included because the paper and author code say so, not merely because a formula happens to match a target.

## Remaining limits

The Table 3 row-3 standard errors are not reconstructed. Figure 1 uses disclosed bins. A one-store exact-wage-share discrepancy and some printed summary diagnostics remain. No values were changed to force a match. Findings and text were AI-assisted; the student remains responsible for the final submission.
