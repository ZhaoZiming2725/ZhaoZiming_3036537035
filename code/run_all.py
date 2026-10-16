"""run_all.py
Single entry point: regenerate EVERY table and figure in outputs/ from the raw
data. Run from the project root:

    python3 code/run_all.py

Requires: pandas, numpy, matplotlib, statsmodels.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

STEPS = [
    "01_make_dataset.py",            # clean -> data/processed/analysis_panel.csv
    "02_replicate_main_table.py",    # Table 3 means + Table 4 DID regression + Fig
    "03_table2.py",                  # Table 2 means of all variables
    "04_extension_wage_bite.py",     # independent extension (wage-bite groups)
]


def main() -> None:
    for step in STEPS:
        print(f"\n{'='*60}\n>>> running {step}\n{'='*60}")
        subprocess.run([sys.executable, str(HERE / step)], check=True)
    print("\nAll tables and figures regenerated in outputs/.")


if __name__ == "__main__":
    main()
