# Original input data

`public.csv` is the 410-store, 46-column public Card-Krueger survey, retained from the author-equivalent public release. It is the sole required input. Keep column names and missing values unchanged.

- Author landing page: https://davidcard.berkeley.edu/data_sets.html
- Public archive: https://davidcard.berkeley.edu/data_sets/njmin.zip
- Princeton catalogue: https://irs.princeton.edu/publications/data-sets/minimum-wages-and-employment-chapter-4

From the repository root, `python code/verify_public_source.py --create-input` downloads and converts `public.dat` only if `public.csv` is missing; otherwise it checks the existing CSV against the author data. It preserves certificate verification, checks all values and missingness, and records hashes in `data/source_verification.json`. Internet access is needed only for this optional acquisition/check step.

Run `python code/run_all.py` to reproduce results after this input is present. Do not place credentials in this directory or publish restricted course inputs or download links. Other local raw files are ignored by Git.
