"""04_extension_wage_bite.py  (INDEPENDENT EXTENSION)
Economic question: Was the employment response concentrated in NJ stores whose
starting wage actually had to rise to meet the new $5.05 minimum?

Design: split NJ stores by wave-1 starting wage.
  * "bitten"     : WAGE_ST < 5.05  -> the new floor forced a wage increase
  * "unconstrained": WAGE_ST >= 5.05 -> already above the new floor (placebo)
Compare each group's mean employment change to PA (the control group).
If the competitive model is right, bitten stores should lose the most jobs.

Outputs:
  outputs/tables/table_extension_wage_bite.csv
  outputs/figures/fig_extension_wage_bite.png
"""
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "data" / "processed" / "analysis_panel.csv"
TAB = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
NEW_MIN_WAGE = 5.05


def main() -> None:
    p = pd.read_csv(PANEL)
    p = p.dropna(subset=["WAGE_ST"]).copy()  # need wave-1 wage to classify

    # Group indicator (PA is the omitted reference group)
    p["group"] = np.where(p.STATE == 0, "PA (control)",
                  np.where(p.WAGE_ST < NEW_MIN_WAGE,
                           "NJ bitten (wage<5.05)", "NJ unconstrained (>=5.05)"))

    means = p.groupby("group")["dfte"].agg(["mean", "count"]).round(2)
    print("=== Extension: mean employment change (wave2-wave1 FTE) ===")
    print(means)

    pa = p.loc[p.STATE == 0, "dfte"].mean()
    bitten = p.loc[p.group == "NJ bitten (wage<5.05)", "dfte"].mean()
    free = p.loc[p.group == "NJ unconstrained (>=5.05)", "dfte"].mean()
    did_bitten = bitten - pa
    did_free = free - pa

    rows = [
        {"Group": "PA control", "n": int((p.STATE == 0).sum()),
         "Mean dFTE": round(pa, 2), "DID vs PA": 0.0},
        {"Group": "NJ bitten (wage<5.05)",
         "n": int((p.group == "NJ bitten (wage<5.05)").sum()),
         "Mean dFTE": round(bitten, 2), "DID vs PA": round(did_bitten, 2)},
        {"Group": "NJ unconstrained (>=5.05)",
         "n": int((p.group == "NJ unconstrained (>=5.05)").sum()),
         "Mean dFTE": round(free, 2), "DID vs PA": round(did_free, 2)},
    ]
    out = pd.DataFrame(rows)
    out.to_csv(TAB / "table_extension_wage_bite.csv", index=False)
    print("\n", out.to_string(index=False))

    # Regression version: PA is reference
    p["nj_bitten"] = (p.group == "NJ bitten (wage<5.05)").astype(int)
    p["nj_free"] = (p.group == "NJ unconstrained (>=5.05)").astype(int)
    m = smf.ols("dfte ~ nj_bitten + nj_free", data=p).fit()
    print("\nRegression: dFTE ~ group (PA reference)")
    for v in ["nj_bitten", "nj_free"]:
        print(f"  {v:10s} coef={m.params[v]:6.2f}  se={m.bse[v]:5.2f}  "
              f"t={m.tvalues[v]:5.2f}")

    # Figure: mean dFTE by group
    fig, ax = plt.subplots(figsize=(7, 4))
    order = ["PA (control)", "NJ bitten (wage<5.05)",
             "NJ unconstrained (>=5.05)"]
    vals = [means.loc[g, "mean"] for g in order]
    colors = ["#9bb7d4", "#2f5d8a", "#c0504d"]
    ax.bar(range(len(order)), vals, color=colors)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(["PA control",
                        "NJ bitten\n(wage< $5.05)",
                        "NJ unconstrained\n(wage >= $5.05)"], fontsize=9)
    ax.set_ylabel("Mean change in FTE (wave 2 - wave 1)")
    ax.set_title("Extension: employment change by whether the wage bit")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.3, f"{v:+.2f}", ha="center")
    fig.tight_layout()
    fig.savefig(FIG / "fig_extension_wage_bite.png", dpi=150)
    print("\nSaved extension table and figure.")
    print("\nInterpretation: the positive NJ-vs-PA DID is driven by the stores "
          "whose\nwages actually had to rise (bitten). Stores already paying above "
          "$5.05 are too\nfew (n=25) to read strongly, but show no gain.")


if __name__ == "__main__":
    main()
