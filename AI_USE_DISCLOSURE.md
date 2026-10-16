# AI-Use Disclosure

## Where and how AI was used

AI assisted with understanding the paper and data documentation, drafting Python code, designing the ownership extension, interpreting results, and preparing the report and repository documentation. This included FTE and wage-gap construction, sample restrictions, table and figure generation, and the reproducible workflow.

## How AI-generated work was checked

- Compared all 410 x 46 input values, including missingness, with the author-hosted public archive using `code/verify_public_source.py`.
- Recomputed tables and figures from the raw input. Checked sample counts, composite store identifiers, closure status, regression-matrix rank and numerical benchmarks.
- Compared all 40 Table 3 point estimates and five Table 4 coefficient/conventional-SE pairs with the paper. The Table 3 point estimates agree within rounding; the Table 4 coefficients and SEs round to the published values.
- Examined HC3 standard errors and confidence intervals, and repeated the ownership extension on the wider employment-only sample.
- Generated the PDF and HTML from computed CSV outputs, visually inspected the PDF, and ran the workflow with newly obtained inputs in a separate directory.

These checks were computer-assisted. The remaining replication differences and statistical limitations are stated in the report.

## Important AI errors and suggestions corrected or rejected

- **Figure definition:** replaced a suggested mean-employment chart with the starting-wage distributions required for Figure 1.
- **Sample and model specification:** corrected Table 4 to the 357-store sample and all five NJ/GAP models. The ownership-label discrepancy between the printed model v and the author program is documented.
- **Closure handling:** distinguished permanent closures from temporary highway, fire and renovation closures. Permanent closures remain zero in the baseline; temporary closures are zero only in the specified sensitivity.
- **Variable construction:** included managers in FTE according to the paper and author codebook.
- **Independent extension:** replaced a wage-bite comparison that overlapped the original paper with an ownership interaction and sample sensitivity.
- **Interpretation:** revised statements that treated positive coefficients as conclusive causal evidence. The report distinguishes conventional and HC3 inference and explains the two-state limitation.
- **Verification wording:** removed unsupported descriptions of computer-assisted calculations as calculations performed by hand.
