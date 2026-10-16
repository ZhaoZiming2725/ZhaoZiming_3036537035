"""01_make_dataset.py
Clean the Card & Krueger (1994) fast-food survey and build the analysis panel.

Input : data/raw/public.csv  (410 stores, two survey waves; suffix 2 = wave 2)
Output: data/processed/analysis_panel.csv

Conventions (documented, matched to C&K 1994):
  * Treatment: STATE == 1 (New Jersey). Control: STATE == 0 (Pennsylvania).
  * Full-time-equivalent employment: FTE = EMPFT + 0.5*EMPPT + NMGRS.
    This reproduces the paper's headline means (see 02_replicate_main_table.py).
  * Wave-2 outcome status (STATUS2): 1 = answered; 0 = refused;
    2 = renovation closure; 3 = permanent closure; 4 = highway closure;
    5 = mall-fire closure. Closed stores have no wave-2 employment.
  * Estimation panel = stores with valid FTE in BOTH waves (balanced panel).
    Closed / refused stores are dropped here; a robustness check in
    02_replicate_main_table.py re-includes permanent closures as zero FTE.
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "public.csv"
OUT = ROOT / "data" / "processed" / "analysis_panel.csv"

STATUS2_LABELS = {
    0: "refused", 1: "answered", 2: "renovation closure",
    3: "permanent closure", 4: "highway closure", 5: "mall-fire closure",
}


def main() -> None:
    df = pd.read_csv(RAW)
    n_raw = len(df)

    # --- 1. Build FTE employment for each wave --------------------------------
    df["fte1"] = df["EMPFT"] + 0.5 * df["EMPPT"] + df["NMGRS"]
    df["fte2"] = df["EMPFT2"] + 0.5 * df["EMPPT2"] + df["NMGRS2"]

    # --- 2. Wave-2 status flag -------------------------------------------------
    df["closed_wave2"] = df["STATUS2"].isin([2, 3, 4, 5]).astype(int)
    df["status2_label"] = df["STATUS2"].map(STATUS2_LABELS)

    # --- 3. Balanced panel: valid FTE in both waves ----------------------------
    has_both = df["fte1"].notna() & df["fte2"].notna()
    panel = df.loc[has_both].copy()
    panel["dfte"] = panel["fte2"] - panel["fte1"]

    # --- 4. Keep analysis columns ---------------------------------------------
    keep = ["SHEET", "CHAIN", "CO_OWNED", "STATE",
            "SOUTHJ", "CENTRALJ", "NORTHJ", "PA1", "PA2", "SHORE",
            "WAGE_ST", "WAGE_ST2", "fte1", "fte2", "dfte",
            "STATUS2", "status2_label", "closed_wave2"]
    panel = panel[keep].sort_values(["STATE", "SHEET"]).reset_index(drop=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUT, index=False)

    # --- 5. Audit trail: raw -> dropped -> kept --------------------------------
    print(f"Raw stores                 : {n_raw}")
    print(f"Missing wave-1 FTE         : {int(df['fte1'].isna().sum())}")
    print(f"Missing wave-2 FTE         : {int(df['fte2'].isna().sum())}")
    print(f"Wave-2 closed (any)        : {int(df['closed_wave2'].sum())}")
    print(f"Balanced panel (kept)      : {len(panel)}  "
          f"(NJ={int((panel.STATE==1).sum())}, PA={int((panel.STATE==0).sum())})")
    print(f"Saved -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
