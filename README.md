# Card & Krueger (1994): Replication and Ownership Extension

ECON6067 individual project - Zhao Ziming (3036537035).

The project reproduces **Tables 2-4 and Figure 1** of Card & Krueger (1994), then tests whether company ownership moderates the NJ-PA employment contrast conditional on chain.

## Start here

- **Final report:** [report.pdf](report.pdf); browser version: [report/report.html](report/report.html).
- **Review and remaining limitations:** [REVIEW_NOTES.md](REVIEW_NOTES.md).
- **AI use:** [AI_USE_DISCLOSURE.md](AI_USE_DISCLOSURE.md).
- **Reusable workflow:** [skills/SKILL.md](skills/SKILL.md).

The all-available employment DID is +2.76 FTE; the 384-store paired DID is +2.75. The assigned Table 4 sample has **357** stores and yields a NJ coefficient of +2.33 without controls, not +2.75. All five Table 4 coefficients and conventional SEs match the paper after rounding. HC3 sensitivity and two-state inference limitations are reported. The independent ownership interaction is imprecise (about -0.94 FTE, HC3 p=0.721); it does not establish an ownership difference.

## Reproduce from a fresh clone

Use Python 3.14 for the pinned, reviewed environment. Other Python versions have not been verified. A virtual environment is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python code/verify_public_source.py --create-input
python code/run_all.py
```

On Windows activate with `.venv\Scripts\activate`. The source-verification step needs internet access and creates `data/raw/public.csv` **only if missing** from the author-hosted public archive. It also checks every numeric value and missing value against `public.dat`. An existing input is verified, never silently replaced. The main `run_all.py` workflow runs offline after inputs are present, from any working directory, and regenerates processed data, CSV tables, figures, PDF, and HTML without manually editing data or code. Certificate verification remains enabled using certifi.

Alternatively obtain the 410-row public survey from the sources below, convert `public.dat` using the 46-column codebook order, and put the resulting CSV in `data/raw/public.csv`. Raw inputs are excluded from Git. Do not publish course download links or restricted data.

## Data provenance

- [Author data landing page](https://davidcard.berkeley.edu/data_sets.html)
- [Author archive njmin.zip](https://davidcard.berkeley.edu/data_sets/njmin.zip): `public.dat`, `codebook`, `check.sas`, survey forms.
- [Princeton catalogue](https://irs.princeton.edu/publications/data-sets/minimum-wages-and-employment-chapter-4)
- [Original paper](https://davidcard.berkeley.edu/papers/njmin-aer.pdf)

During review, all 410 x 46 submitted input values, including missingness, were independently verified against the author archive. `data/source_verification.json` records hashes. This establishes data identity, not how the original project acquired the input. No claim is made that the student personally performed that download or qualifies for a data-acquisition bonus.

## Definitions and sample rules

- NJ: `STATE=1`; PA: `STATE=0`.
- FTE: `EMPFT + 0.5*EMPPT + NMGRS`, repeated for wave 2.
- Six permanently closed stores (`STATUS2=3`) have zero wave-2 FTE and are included when baseline FTE is observed. Four temporary closures (`2,4,5`) are missing in baseline and zero only in Table 3 row 5. Refusal (`0`) is missing.
- Table 2: variable-specific samples; exact-wage indicators use all stores (missing wage coded false) as in the author SAS program. The wage-distribution figure instead uses observed-wage denominators.
- Table 3: all available means, paired changes, NJ initial-wage subgroups, and temporary-closure sensitivity. `STATE` + `SHEET` is the unique key, not `SHEET` alone.
- Table 4: 357 stores with valid employment changes and wages in both waves, except permanently closed stores remain eligible. Five NJ/GAP models follow author `check.sas`.
- Model v follows author code, which omits ownership despite the printed table label; the ownership-inclusive sensitivity is exported separately.
- Extension: `dfte ~ STATE * CO_OWNED + C(CHAIN)`, HC3 intervals, plus the 384-store sample sensitivity. Wage-bite splits are part of the original analysis and are not claimed as an independent extension.

## Outputs and checks

| Path | Contents |
|---|---|
| `code/analysis.py` | Data definitions, Tables 2-4, Figure 1, ownership extension and benchmark assertions |
| `code/build_report.py` | PDF/HTML built from computed tables |
| `code/verify_public_source.py` | Obtain/verify public source, no overwrite of existing inputs |
| `code/run_all.py` | Offline entry point |
| `data/raw/` | Ignored local input and author codebook |
| `data/processed/` | Derived analysis variables and eligibility indicators |
| `outputs/tables/` | Full estimates, counts, SEs, published comparisons and sensitivities |
| `outputs/figures/` | Correct wage-distribution Figure 1 and ownership-extension intervals |
| `outputs/validation.json` | Sample counts, missingness, closures and input checksum |

Checks cover raw state counts, composite keys, 384/357 sample sizes, design-matrix rank, Table 4 coefficient/SE benchmarks, Table 3 DID values, and histogram totals. `requirements.txt` pins the reviewed dependency versions.

## Honest limits

Table 3 row-3 SEs are not reconstructed (point estimates are); no paired SE is substituted. The public release yields 85.50% NJ stores at exactly $5.05 after the change versus 85.2% printed. Figure 1 documents modern bin boundaries. Model-v residual/F diagnostics and some Table 2 printed summaries differ slightly. These are disclosed in the report and comparison files. HC3 does not solve the two-state policy-inference problem. Findings should not be represented as conclusive positive causal effects.
