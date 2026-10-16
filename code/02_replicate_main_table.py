"""02_replicate_main_table.py
Replicate Card & Krueger (1994), Table 3 (means) and Table 4 (DID regression).

Outputs:
  outputs/tables/table3_means.csv
  outputs/tables/table4_did_regression.csv
  outputs/figures/fig_mean_fte_by_state.png
"""
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "data" / "processed" / "analysis_panel.csv"
RAW = ROOT / "data" / "raw" / "public.csv"
TAB = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
TAB.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)


def table3_means(p: pd.DataFrame) -> pd.DataFrame:
    """Mean FTE by state x wave, plus within-state change and the DID."""
    rows = []
    for state, label in [(0, "Pennsylvania (control)"), (1, "New Jersey (treatment)")]:
        s = p[p.STATE == state]
        rows.append({
            "State": label,
            "Wave 1 mean FTE": round(s.fte1.mean(), 2),
            "Wave 2 mean FTE": round(s.fte2.mean(), 2),
            "Change (W2-W1)": round(s.fte2.mean() - s.fte1.mean(), 2),
            "n stores": len(s),
        })
    out = pd.DataFrame(rows)
    nj_d = p.loc[p.STATE == 1, "dfte"].mean()
    pa_d = p.loc[p.STATE == 0, "dfte"].mean()
    did = nj_d - pa_d
    print("\n=== Table 3: Mean FTE by state and wave ===")
    print(out.to_string(index=False))
    print(f"\nDID = (NJ change) - (PA change) = {nj_d:.2f} - {pa_d:.2f} = {did:.2f} FTE")
    print("Paper (C&K 1994, Table 3): DID = +2.76 FTE")
    out.to_csv(TAB / "table3_means.csv", index=False)
    return out, did


def table4_regression(p: pd.DataFrame) -> pd.DataFrame:
    """dFTE = a + b*NJ + controls. b is the DID estimate."""
    specs = {
        "(1) no controls": "dfte ~ STATE",
        "(2) chain FE": "dfte ~ STATE + C(CHAIN)",
        "(3) chain + region + co-owned":
            # All PA stores are in PA1 or PA2, so PA1+PA2 == 1-STATE exactly.
            # Drop PA2 (reference = PA2 Easton area + northern NJ) to keep the
            # design matrix full rank while still controlling for region.
            "dfte ~ STATE + C(CHAIN) + SOUTHJ + CENTRALJ + PA1 + CO_OWNED",
    }
    rows = []
    for name, formula in specs.items():
        m = smf.ols(formula, data=p).fit()
        rows.append({
            "Specification": name,
            "DID coef (NJ)": round(m.params["STATE"], 3),
            "Std. Error": round(m.bse["STATE"], 3),
            "t": round(m.tvalues["STATE"], 2),
            "n": int(m.nobs),
            "R2": round(m.rsquared, 3),
        })
    out = pd.DataFrame(rows)
    print("\n=== Table 4: DID regressions (dFTE ~ NJ) ===")
    print(out.to_string(index=False))
    out.to_csv(TAB / "table4_did_regression.csv", index=False)
    return out


def robustness_include_closures() -> None:
    """Re-include permanently closed stores as zero wave-2 FTE (C&K sensitivity)."""
    raw = pd.read_csv(RAW)
    raw["fte1"] = raw.EMPFT + 0.5 * raw.EMPPT + raw.NMGRS
    raw["fte2"] = raw.EMPFT2 + 0.5 * raw.EMPPT2 + raw.NMGRS2
    # permanent closure = STATUS2 3,4,5 -> set wave-2 FTE to 0
    closed = raw.STATUS2.isin([3, 4, 5])
    fte2_closed = raw.loc[closed, "fte2"].fillna(0)
    raw.loc[closed, "fte2"] = fte2_closed
    s = raw.dropna(subset=["fte1", "fte2"]).copy()
    s["dfte"] = s.fte2 - s.fte1
    did = s.loc[s.STATE == 1, "dfte"].mean() - s.loc[s.STATE == 0, "dfte"].mean()
    print(f"\nRobustness: permanent closures counted as 0 FTE -> DID = {did:.2f} FTE "
          f"(n={len(s)})")


def make_figure(p: pd.DataFrame) -> None:
    means = p.groupby("STATE")[["fte1", "fte2"]].mean()
    means.index = ["PA", "NJ"]
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(2)
    ax.bar(x - 0.18, means["fte1"], width=0.36, label="Wave 1 (Feb 1992)",
           color="#9bb7d4")
    ax.bar(x + 0.18, means["fte2"], width=0.36, label="Wave 2 (Nov 1992)",
           color="#2f5d8a")
    ax.set_xticks(x); ax.set_xticklabels(["Pennsylvania (control)",
                                          "New Jersey (treatment)"])
    ax.set_ylabel("Mean FTE employment")
    ax.set_title("Fast-food employment before/after the NJ minimum-wage hike")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "fig_mean_fte_by_state.png", dpi=150)
    print(f"\nSaved figure -> outputs/figures/fig_mean_fte_by_state.png")


def main() -> None:
    p = pd.read_csv(PANEL)
    table3_means(p)
    table4_regression(p)
    robustness_include_closures()
    make_figure(p)


if __name__ == "__main__":
    main()
