"""v2 extended box — join the hand labels to the sample key and estimate what the flagged terrace area is today.

Reference labels, both mine, from present-day Google imagery, blind to stratum:
  accuracy_sample_my_labels.csv   first pass, 7 classes, 120 points
  accuracy_second_pass.csv        second pass on the 68 points first labelled bare_other or road: is the point inside a
                                  brick-kiln field (yes / no / unclear)? Needed because bare worked ground inside a kiln field
                                  could not be told from other bare ground at the first-pass zoom.
Final class: kiln = first-pass kiln_ground or second-pass yes; otherwise the first-pass class (second-pass unclear kept apart).

I run it from the repo root:  python v2_redesign/west_extension/05_accuracy_result.py
"""
import numpy as np
import pandas as pd

OUT = "v2_redesign/west_extension/"
HA = 0.09
d = (pd.read_csv(OUT + "accuracy_sample_key.csv")
     .merge(pd.read_csv(OUT + "accuracy_sample_my_labels.csv")[["point_id", "my_label"]], on="point_id")
     .merge(pd.read_csv(OUT + "accuracy_second_pass.csv"), on="point_id", how="left"))
d["in_kiln_field"] = d.in_kiln_field.fillna("")
assert (d.my_label.fillna("") != "").all()
assert (d.loc[d.my_label.isin(["bare_other", "road"]), "in_kiln_field"] != "").all()
d["final"] = d.my_label
d.loc[(d.my_label == "kiln_ground") | (d.in_kiln_field == "yes"), "final"] = "kiln"
d.loc[d.in_kiln_field == "unclear", "final"] = "unclear"
d.to_csv(OUT + "accuracy_sample_labelled.csv", index=False)

tab = pd.crosstab(d.stratum, d.final)
tab["n"] = tab.sum(axis=1)
tab.to_csv(OUT + "accuracy_confusion.csv")


def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(c - h, 0), min(c + h, 1)


rows = []
for s, g in d.groupby("stratum"):
    n = len(g); ha = int(g.stratum_px.iloc[0]) * HA
    for name, hit in [("kiln", g.final == "kiln"), ("not vegetated", ~g.final.isin(["vegetated", "unclear"])),
                      ("built_up or road, not kiln", g.final.isin(["built_up", "road"])),
                      ("other bare ground, not kiln", g.final == "bare_other"), ("still vegetated", g.final == "vegetated"),
                      ("unclear", g.final == "unclear")]:
        k = int(hit.sum()); lo, hi = wilson(k, n)
        rows.append(dict(stratum=s, n=n, stratum_ha=ha, reference_class=name, hits=k, share=k / n, ci95_low=lo, ci95_high=hi,
                         est_ha=ha * k / n, est_ha_low=ha * lo, est_ha_high=ha * hi))
res = pd.DataFrame(rows)
res.round(3).to_csv(OUT + "accuracy_result.csv", index=False)
pd.set_option("display.width", 250)
print(tab.to_string()); print(res.round(3).to_string(index=False))
k = res[res.reference_class == "kiln"].set_index("stratum")
a, b = k.loc["A_strict"], k.loc["B_drop_only"]
var = sum((r.stratum_ha ** 2) * r.share * (1 - r.share) / (r.n - 1) for r in (a, b))
tot = a.est_ha + b.est_ha
print("kiln ground among flagged terrace pixels: %.0f ha (strict %.0f + drop-only %.0f), 95%% CI about %.0f-%.0f ha" % (
    tot, a.est_ha, b.est_ha, tot - 1.96 * var ** .5, tot + 1.96 * var ** .5))
