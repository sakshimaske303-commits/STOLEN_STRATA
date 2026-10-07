"""v2 extended box: were the flagged sample points vegetated before the change?

The change tests flag a pixel when its yearly peak NDVI was high in 2013-2015 and low in 2023-2025. The labels in
05_accuracy_result.py check the second half of that against present-day imagery. This script checks the first half:
each of the 85 flagged sample points (strata A_strict and B_drop_only) was looked up in Google Earth Pro historical
imagery of 2013-2014 and labelled vegetated / not_vegetated / unclear.

  accuracy_before_pass.csv   point_id, before_label, image_date, basis (what is seen at the point)

Rule used: vegetated = crop field, orchard, grass, scattered trees or scrub at the point; not_vegetated = kiln ground,
dug ground, building, road, track or bare soil at the point; unclear = cannot be told. Image: 10 September 2014 where it
is usable, otherwise another clear image of 2013-2014 (date recorded per point).

This pass was not blind: only flagged points were looked at, and one image date shows the ground on one day, whereas the
test uses the yearly peak. A point that is bare in a single image can still have had a green season in that year.

Run from the repo root:  python v2_redesign/west_extension/10_before_check_result.py
Output: v2_redesign/west_extension/accuracy_before_result.csv, accuracy_before_by_present_class.csv
"""
import numpy as np
import pandas as pd

OUT = "v2_redesign/west_extension/"
HA = 0.09
d = pd.read_csv(OUT + "accuracy_sample_labelled.csv").merge(pd.read_csv(OUT + "accuracy_before_pass.csv"), on="point_id")
assert len(d) == 85 and set(d.stratum) == {"A_strict", "B_drop_only"}
assert d.before_label.isin(["vegetated", "not_vegetated", "unclear"]).all()


def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(c - h, 0), min(c + h, 1)


rows = []
for s, g in d.groupby("stratum"):
    n = len(g); ha = int(g.stratum_px.iloc[0]) * HA
    for name, hit in [("vegetated before", g.before_label == "vegetated"),
                      ("not vegetated before", g.before_label == "not_vegetated"),
                      ("unclear before", g.before_label == "unclear"),
                      ("vegetated before and not vegetated today", (g.before_label == "vegetated") & ~g.final.isin(["vegetated", "unclear"])),
                      ("vegetated before and inside a kiln field today", (g.before_label == "vegetated") & (g.final == "kiln")),
                      ("inside a kiln field today (05_accuracy_result.py)", g.final == "kiln")]:
        k = int(hit.sum()); lo, hi = wilson(k, n)
        rows.append(dict(stratum=s, n=n, stratum_ha=round(ha, 2), measure=name, hits=k, share=round(k / n, 3),
                         ci95_low=round(lo, 3), ci95_high=round(hi, 3), est_ha=round(ha * k / n, 1),
                         est_ha_low=round(ha * lo, 1), est_ha_high=round(ha * hi, 1)))
r = pd.DataFrame(rows)
tot = []
for name, g in r.groupby("measure", sort=False):
    k, n = int(g.hits.sum()), int(g.n.sum()); lo, hi = wilson(k, n)
    est = g.est_ha.sum()
    var = sum((x.stratum_ha ** 2) * x.share * (1 - x.share) / (x.n - 1) for x in g.itertuples())
    tot.append(dict(stratum="A_and_B", n=n, stratum_ha=round(g.stratum_ha.sum(), 2), measure=name, hits=k, share=round(k / n, 3),
                    ci95_low=round(lo, 3), ci95_high=round(hi, 3), est_ha=round(est, 1),
                    est_ha_low=round(max(est - 1.96 * var ** .5, 0), 1), est_ha_high=round(min(est + 1.96 * var ** .5, g.stratum_ha.sum()), 1)))
r = pd.concat([r, pd.DataFrame(tot)], ignore_index=True)
r.to_csv(OUT + "accuracy_before_result.csv", index=False)
pd.set_option("display.width", 250); print(r.to_string(index=False))

x = pd.crosstab([d.stratum, d.before_label], d.final); x["n"] = x.sum(axis=1)
x.to_csv(OUT + "accuracy_before_by_present_class.csv"); print(x.to_string())
print(d[d.before_label != "vegetated"][["point_id", "stratum", "terrace_id", "p90_2013_15", "before_label", "final", "image_date"]].to_string(index=False))
