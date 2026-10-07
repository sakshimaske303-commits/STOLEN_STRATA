"""v2 extended box: how much of the kiln estimate rests on each labelling pass, and where the sample points fall.

First pass  : the point is labelled kiln ground at close zoom (kiln, clay pit, drying rows, worked bare earth in a kiln field).
Second pass : points first labelled bare or road that lie inside a brick-kiln field when seen one zoom level out.
The paper's figure uses both. This script reports the two separately so a reader can see the dependence.

Run from the repo root:  python v2_redesign/west_extension/09_accuracy_by_labelling_pass.py
Output: v2_redesign/west_extension/accuracy_by_labelling_pass.csv, accuracy_points_by_terrace.csv
"""
import numpy as np, pandas as pd

OUT = "v2_redesign/west_extension/"
HA = 0.09
d = pd.read_csv(OUT + "accuracy_sample_labelled.csv")
d["in_kiln_field"] = d.in_kiln_field.fillna("")


def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(c - h, 0), min(c + h, 1)


rows = []
for s, g in d.groupby("stratum"):
    n = len(g); ha = int(g.stratum_px.iloc[0]) * HA
    first = int((g.my_label == "kiln_ground").sum())
    second = int(((g.my_label != "kiln_ground") & (g.in_kiln_field == "yes")).sum())
    for name, k in [("first pass only: point centre is kiln ground", first),
                    ("added by second pass: bare or road point inside a kiln field", second),
                    ("both passes (figure used in the paper)", first + second)]:
        lo, hi = wilson(k, n)
        rows.append(dict(stratum=s, n=n, stratum_ha=round(ha, 2), definition=name, hits=k, share=round(k / n, 3),
                         est_ha=round(ha * k / n, 1), est_ha_low=round(ha * lo, 1), est_ha_high=round(ha * hi, 1)))
r = pd.DataFrame(rows); r.to_csv(OUT + "accuracy_by_labelling_pass.csv", index=False)
pd.set_option("display.width", 250); print(r.to_string(index=False))
f = r[r.stratum != "C_not_flagged"]
for name in f.definition.unique():
    print("flagged terrace land, %s: %.0f ha" % (name, f[f.definition == name].est_ha.sum()))

t = (d[d.stratum != "C_not_flagged"].groupby(["stratum", "terrace_id"]).agg(points=("point_id", "size"), kiln=("final", lambda x: int((x == "kiln").sum())))
     .reset_index().sort_values(["stratum", "points"], ascending=[True, False]))
t.to_csv(OUT + "accuracy_points_by_terrace.csv", index=False); print(t.to_string(index=False))
