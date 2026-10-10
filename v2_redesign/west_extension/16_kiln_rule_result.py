"""v2 extended box: the kiln estimate with both samples labelled under one written rule.

The two samples placed the edges of kiln fields differently (15_pooled_accuracy.py: 141 ha against 232 ha). The rule in
KILN_FIELD_RULE.md was written down, and every flagged point whose kiln label depended on its setting was relabelled under it
(kiln_edge_recheck.csv, 86 points: 57 from the first sample, 29 from the second). All other points keep their pooled label.

Run from the repo root:  python v2_redesign/west_extension/16_kiln_rule_result.py
Output: v2_redesign/west_extension/kiln_rule_result.csv, kiln_rule_points.csv,
        kiln_rule_accuracy.csv and kiln_rule_before.csv (same layout as pooled_accuracy_result.csv and pooled_before_result.csv)
"""
import numpy as np
import pandas as pd

OUT = "v2_redesign/west_extension/"
HA = 0.09
d = pd.read_csv(OUT + "pooled_points.csv")
r = pd.read_csv(OUT + "kiln_edge_recheck.csv", dtype=str, keep_default_na=False)
assert len(r) == 86 and (r.confirmed_by_author == "yes").all()
r["point_id"] = r.point_id.astype(int)
d = d.merge(r[["point_id", "rule_label"]], on="point_id", how="left")
d["final_rule"] = d.rule_label.fillna("").where(d.rule_label.fillna("") != "", d.final)
d.to_csv(OUT + "kiln_rule_points.csv", index=False)


def estimate(data, hit, sample):
    rows, ests, var, cap = [], 0.0, 0.0, 0.0
    for s, g in data[data.stratum.isin(["A_strict", "B_drop_only"])].groupby("stratum"):
        n, k = len(g), int(hit(g).sum()); ha = int(g.stratum_px.iloc[0]) * HA; p = k / n
        ests += ha * p; var += ha * ha * p * (1 - p) / (n - 1); cap += ha
        rows.append(dict(sample=sample, stratum=s, n=n, hits=k, share=round(p, 3), est_ha=round(ha * p, 1)))
    rows.append(dict(sample=sample, stratum="A_and_B", n=int(sum(x["n"] for x in rows)), hits=int(sum(x["hits"] for x in rows)),
                     share=round(ests / cap, 3), est_ha=round(ests, 1), est_ha_low=round(max(ests - 1.96 * var ** .5, 0), 1),
                     est_ha_high=round(min(ests + 1.96 * var ** .5, cap), 1)))
    return rows


rows = []
for name, data in (("pooled", d), ("draw 1", d[d.draw == 1]), ("draw 2", d[d.draw == 2])):
    for measure, hit in (("kiln", lambda g: g.final_rule == "kiln"),
                         ("vegetated before and kiln", lambda g: (g.before_label == "vegetated") & (g.final_rule == "kiln")),
                         ("not vegetated", lambda g: ~g.final_rule.isin(["vegetated", "unclear"]))):
        for x in estimate(data, hit, name):
            x["measure"] = measure; rows.append(x)
res = pd.DataFrame(rows)[["sample", "measure", "stratum", "n", "hits", "share", "est_ha", "est_ha_low", "est_ha_high"]]
res.to_csv(OUT + "kiln_rule_result.csv", index=False)
pd.set_option("display.width", 200)
print(res.to_string(index=False))
f = d[d.stratum != "C_not_flagged"]
print(pd.crosstab([f.draw, f.stratum], f.final_rule))
print("labels changed by the rule:", int((d.final_rule != d.final).sum()))


# Full tables in the layout of 15_pooled_accuracy.py, with the rule-based class (used by the dashboard).
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



d["final"] = d.final_rule
present = [("kiln", lambda g: g.final == "kiln"),
           ("not vegetated", lambda g: ~g.final.isin(["vegetated", "unclear"])),
           ("built_up or road, not kiln", lambda g: g.final.isin(["built_up", "road"])),
           ("other bare ground, not kiln", lambda g: g.final == "bare_other"),
           ("still vegetated", lambda g: g.final == "vegetated"),
           ("unclear", lambda g: g.final == "unclear")]
table(d, present).to_csv(OUT + "kiln_rule_accuracy.csv", index=False)
f = d[d.stratum.isin(["A_strict", "B_drop_only"])].copy()
before = [("vegetated before", lambda g: g.before_label == "vegetated"),
          ("not vegetated before", lambda g: g.before_label == "not_vegetated"),
          ("unclear before", lambda g: g.before_label == "unclear"),
          ("vegetated before and not vegetated today", lambda g: (g.before_label == "vegetated") & ~g.final.isin(["vegetated", "unclear"])),
          ("vegetated before and inside a kiln field today", lambda g: (g.before_label == "vegetated") & (g.final == "kiln")),
          ("inside a kiln field today", lambda g: g.final == "kiln")]
table(f, before).to_csv(OUT + "kiln_rule_before.csv", index=False)
