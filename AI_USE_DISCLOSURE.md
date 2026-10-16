# AI-Use Disclosure

## Where and how AI was used
- Used an AI coding agent to draft the data-cleaning and regression scripts
  (`01_make_dataset.py`, `02_replicate_main_table.py`) from the course data
  dictionary and the Card & Krueger paper description.
- Used AI to propose the FTE employment definition, the DID specification, and
  the directory/README skeleton.
- Used AI to help interpret the statsmodels output and the collinearity warning.

## How AI-generated work was checked
- **Manual recomputation:** independently computed the mean FTE by state and
  wave and the DID by hand (groupby means) and confirmed the script matches:
  DID ≈ +2.75 FTE vs. the paper's +2.76.
- **Against the paper:** compared wave-1/wave-2 means and the DID to Card &
  Krueger (1994) Table 3; small gaps traced to which closed/refused stores are
  in the balanced panel.
- **Assertion / sanity checks:** verified the first stage (NJ starting wage jumps
  to ~$5.08/h, PA unchanged), the balanced-panel count (384 stores), and that
  the coefficient is identical across the no-control and chain-FE regressions.
- **Reran end-to-end:** restarted and ran both scripts from scratch after edits.

## AI errors corrected or rejected
- **Collinearity bug (corrected):** the first region-adjusted specification put
  both PA1 and PA2 dummies plus STATE in the regression. Because every PA store
  is either PA1 or PA2, `PA1 + PA2 = 1 − STATE` exactly — a rank-deficient design
  that produced a spurious coefficient. Detected via the SingularMatrixWarning
  and fixed by dropping PA2.
- **FTE convention (checked, not trusted blindly):** AI first proposed
  `EMPFT + 0.5*EMPPT` without managers. Testing showed including managers
  (`+ NMGRS`) reproduces the paper's means and DID (2.75 vs 2.76); we kept the
  manager-inclusive convention and documented it.
- **Rejected:** an early suggestion to "just use statsmodels default SEs without
  checking"; instead we inspected the design matrix and reported the
  region-control sensitivity honestly.
