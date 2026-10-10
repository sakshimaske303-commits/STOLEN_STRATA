"""v2 extended box: accuracy and before-check on the pooled sample (first draw 1-120 + second draw 121-240).

First draw : 25 strict / 60 drop-only / 35 unflagged points (04_accuracy_sample.py), labels in
             accuracy_sample_labelled.csv (present class) and accuracy_before_pass.csv (before class, flagged points only).
Second draw: 35 / 60 / 25 points from the same strata, leaving out the pixels already sampled (12_accuracy_sample_supplement.py).
             Labels in accuracy_sample2_labels_in_progress.csv: present class and before class for every point, from Google
             Earth Pro historical imagery, labelled blind to stratum (the key was opened only after all 120 were labelled).
             Present class "kiln" already covers both labelling passes of the first draw (kiln ground at the point, or bare
             worked ground / track inside a kiln field). Points with no clear image in 2013-2015 (before_date not in 2013-2015)
             count as unclear in the before-check.
Pooled     : 60 / 120 / 60 points. Each stratum is a simple random sample in both draws, so the pooled points are treated
             as one simple random sample per stratum (the second draw excluded the 120 first-draw pixels, a negligible change).

I run it from the repo root:  python v2_redesign/west_extension/15_pooled_accuracy.py
Output: v2_redesign/west_extension/pooled_accuracy_result.csv, pooled_before_result.csv, pooled_confusion.csv,
        pooled_before_by_present_class.csv, pooled_points.csv
"""
import re
import numpy as np
import pandas as pd

OUT = "v2_redesign/west_extension/"
HA = 0.09

s1 = pd.read_csv(OUT + "accuracy_sample_labelled.csv")
b1 = pd.read_csv(OUT + "accuracy_before_pass.csv")
s1 = s1.merge(b1[["point_id", "before_label", "image_date"]], on="point_id", how="left")
s1 = s1.rename(columns={"image_date": "before_date"}); s1["draw"] = 1

k2 = pd.read_csv(OUT + "accuracy_sample2_key.csv")
l2 = pd.read_csv(OUT + "accuracy_sample2_labels_in_progress.csv", dtype=str, keep_default_na=False)
assert len(l2) == 120 and (l2.confirmed_by_author == "yes").all()
l2["point_id"] = l2.point_id.astype(int)
s2 = k2.merge(l2[["point_id", "before_label", "before_date", "now_class"]], on="point_id")
assert len(s2) == 120
s2 = s2.rename(columns={"now_class": "final"}); s2["draw"] = 2
yr = s2.before_date.str.extract(r"(20\d\d)")[0].astype(int)
s2.loc[~yr.between(2013, 2015), "before_label"] = "unclear"

# both draws must use the same stratum sizes
px = pd.concat([s1.groupby("stratum").stratum_px.first(), s2.groupby("stratum").stratum_px.first()], axis=1)
assert (px.iloc[:, 0] == px.iloc[:, 1]).all(), px

cols = ["point_id", "draw", "stratum", "stratum_px", "terrace_id", "p90_2013_15", "p90_2023_25", "final", "before_label", "before_date"]
d = pd.concat([s1[cols], s2[cols]], ignore_index=True)
assert set(d.final) <= {"kiln", "vegetated", "built_up", "road", "bare_other", "unclear"}, set(d.final)
d.to_csv(OUT + "pooled_points.csv", index=False)


def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(c - h, 0), min(c + h, 1)


def table(data, measures, by_draw=True):
    rows = []
    groups = [("pooled", data)] + ([("draw 1", data[data.draw == 1]), ("draw 2", data[data.draw == 2])] if by_draw else [])
    for sample, dd in groups:
        for s, g in dd.groupby("stratum"):
            n = len(g); ha = int(g.stratum_px.iloc[0]) * HA
            for name, fn in measures:
                k = int(fn(g).sum()); lo, hi = wilson(k, n)
                rows.append(dict(sample=sample, stratum=s, n=n, stratum_ha=round(ha, 2), measure=name, hits=k, share=round(k / n, 3),
                                 ci95_low=round(lo, 3), ci95_high=round(hi, 3), est_ha=round(ha * k / n, 1),
                                 est_ha_low=round(ha * lo, 1), est_ha_high=round(ha * hi, 1)))
    r = pd.DataFrame(rows)
    tot = []
    for (sample, name), g in r[r.stratum.isin(["A_strict", "B_drop_only"])].groupby(["sample", "measure"], sort=False):
        k, n = int(g.hits.sum()), int(g.n.sum())
        est = sum(x.stratum_ha * x.hits / x.n for x in g.itertuples())
        var = sum((x.stratum_ha ** 2) * (x.hits / x.n) * (1 - x.hits / x.n) / (x.n - 1) for x in g.itertuples())
        cap = g.stratum_ha.sum()
        tot.append(dict(sample=sample, stratum="A_and_B", n=n, stratum_ha=round(cap, 2), measure=name, hits=k, share=round(est / cap, 3),
                        ci95_low=round(max(est - 1.96 * var ** .5, 0) / cap, 3), ci95_high=round(min(est + 1.96 * var ** .5, cap) / cap, 3),
                        est_ha=round(est, 1), est_ha_low=round(max(est - 1.96 * var ** .5, 0), 1), est_ha_high=round(min(est + 1.96 * var ** .5, cap), 1)))
    return pd.concat([r, pd.DataFrame(tot)], ignore_index=True)


present = [("kiln", lambda g: g.final == "kiln"),
           ("not vegetated", lambda g: ~g.final.isin(["vegetated", "unclear"])),
           ("built_up or road, not kiln", lambda g: g.final.isin(["built_up", "road"])),
           ("other bare ground, not kiln", lambda g: g.final == "bare_other"),
           ("still vegetated", lambda g: g.final == "vegetated"),
           ("unclear", lambda g: g.final == "unclear")]
acc = table(d, present)
acc.to_csv(OUT + "pooled_accuracy_result.csv", index=False)
conf = pd.crosstab(d.stratum, d.final); conf["n"] = conf.sum(axis=1); conf.to_csv(OUT + "pooled_confusion.csv")

f = d[d.stratum.isin(["A_strict", "B_drop_only"])].copy()
assert f.before_label.isin(["vegetated", "not_vegetated", "unclear"]).all()
before = [("vegetated before", lambda g: g.before_label == "vegetated"),
          ("not vegetated before", lambda g: g.before_label == "not_vegetated"),
          ("unclear before", lambda g: g.before_label == "unclear"),
          ("vegetated before and not vegetated today", lambda g: (g.before_label == "vegetated") & ~g.final.isin(["vegetated", "unclear"])),
          ("vegetated before and inside a kiln field today", lambda g: (g.before_label == "vegetated") & (g.final == "kiln")),
          ("inside a kiln field today", lambda g: g.final == "kiln")]
bef = table(f, before)
bef.to_csv(OUT + "pooled_before_result.csv", index=False)
x = pd.crosstab([f.stratum, f.before_label], f.final); x["n"] = x.sum(axis=1); x.to_csv(OUT + "pooled_before_by_present_class.csv")

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
print(conf.to_string()); print()
print(acc[acc["sample"] == "pooled"].to_string(index=False)); print()
print(bef[bef["sample"] == "pooled"].to_string(index=False)); print()
print(x.to_string()); print()
k = acc[(acc.measure == "kiln") & (acc.stratum == "A_and_B")]
for r in k.itertuples():
    print("%s: kiln ground among flagged terrace pixels %.0f ha (95%% CI %.0f-%.0f)" % (r.sample, r.est_ha, r.est_ha_low, r.est_ha_high))
