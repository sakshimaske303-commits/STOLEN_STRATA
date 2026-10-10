# What counts as "inside a kiln field"

Written on 9 October 2026, after pooling the two accuracy samples showed that they placed the edges of kiln fields differently
(141 ha against 232 ha; `15_pooled_accuracy.py`). The edge points of both samples are relabelled under this one rule
(`kiln_edge_recheck.csv`, `kiln_edge_recheck.kml`).

**A point is labelled *kiln field* if**
1. it lies on a kiln, chimney, clay pit, rows or stacks of drying bricks, or a kiln shed; **or**
2. it lies on bare worked ground, a track or a yard inside the worked area of a kiln: within the outer bunds or cut edges of that
   area, with brick rows, pits or a kiln within about 100 m (three Landsat pixels), and with no house, public road or crop field
   between the point and them.

**It is not kiln field if**
- it is on a public or paved road, even one that borders a kiln field: *road*;
- it is on a house, roof or village yard: *built-up*;
- it is bare ground with no brick rows, pits or kiln within about 100 m, or outside the bunds of the worked area: *other bare ground*;
- it is a green field or orchard next to a kiln field: *vegetated*.

**How it is applied.** Newest Google Earth Pro image, viewed from directly above, at a scale that shows about 200 m around the
point; the image date is recorded. Labels are drafted from screen captures and confirmed by the author. The recheck covers every
flagged point whose kiln label depended on its setting: in the first sample the 57 points first labelled bare or road (32 not
counted as kiln, 25 counted as kiln on the second look), in the second sample the 29 kiln points on edges, tracks, yards or cleared
ground. Points that are kiln ground at the point itself, and points that are plainly something else, are not rechecked.

This pass is not blind: the stratum key is open, though the strata are not shown in the recheck list.

**Result** (10 October 2026, `16_kiln_rule_result.py`): kiln land on flagged terraces 210 ha (95% interval 189-231 ha); 204 ha from the
first sample and 217 ha from the second.
