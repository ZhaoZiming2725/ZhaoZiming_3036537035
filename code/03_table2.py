"""03_table2.py
Replicate Card & Krueger (1994) Table 2: means of key variables by state and wave.

Besides employment, the paper shows that other store characteristics (starting
wage, hours open, and prices) did not move systematically between NJ and PA.

Output: outputs/tables/table2_means_all_variables.csv
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "public.csv"
TAB = ROOT / "outputs" / "tables"
TAB.mkdir(parents=True, exist_ok=True)

# (wave-1 column, wave-2 column, label, unit)
VARS = [
    ("WAGE_ST",   "WAGE_ST2",  "Starting wage ($/hr)", "$/hr"),
    ("HRSOPEN",   "HRSOPEN2",  "Hours open / day",     "hours"),
    ("PSODA",     "PSODA2",    "Price: medium soda",   "$"),
    ("PFRY",      "PFRY2",     "Price: small fries",   "$"),
    ("PENTREE",   "PENTREE2",  "Price: entree",        "$"),
]


def main() -> None:
    df = pd.read_csv(RAW)
    df["fte1"] = df.EMPFT + 0.5 * df.EMPPT + df.NMGRS
    df["fte2"] = df.EMPFT2 + 0.5 * df.EMPPT2 + df.NMGRS2

    rows = []
    # Employment row first (FTE), then the listed variables
    var_list = [("fte1", "fte2", "FTE employment", "FTE")] + VARS
    for c1, c2, label, unit in var_list:
        for state, slabel in [(0, "PA"), (1, "NJ")]:
            s = df[df.STATE == state]
            rows.append({
                "Variable": label, "State": slabel,
                "Wave 1": round(s[c1].mean(), 3),
                "Wave 2": round(s[c2].mean(), 3),
                "Change": round(s[c2].mean() - s[c1].mean(), 3),
            })
    out = pd.DataFrame(rows)
    out.to_csv(TAB / "table2_means_all_variables.csv", index=False)
    print("=== Table 2: Means by state and wave ===")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
