# Status, October 2026

## Done
- Both accuracy samples labelled and pooled (`west_extension/15_pooled_accuracy.py`, Development Log Entry 30).
- One written rule for where a kiln field ends (`west_extension/KILN_FIELD_RULE.md`); the 86 edge points of both samples
  relabelled under it (`kiln_edge_recheck.csv`) and the kiln estimate recomputed (`16_kiln_rule_result.py`, Entry 31).
- Result: 299 ha of the 331 ha flagged not vegetated today; 262 ha vegetated before and not now; 210 ha (189-231) inside kiln
  fields, 204 ha by the first sample and 217 ha by the second; 197 ha restricted to points vegetated in the older image.
- Long series recomputed with the corrected Landsat 8/9 adjustment (`west_extension/gee_05_long_series_fixed.js`, Entry 32):
  the two belts about 407 ha since the mid-1990s (first run 335 ha).
- Ground check at Lethpora: four field photos inside a mapped terrace, on unflagged land (`phase1_delineation/05_field_photo_check.py`).

## Open
- The Landsat values in the check of the earlier estimate (Section 4.1 of the paper) come from the original-box series, which
  still carries the reversed Landsat 8/9 adjustment.
- Image dates for the first sample; a second labeller; kiln-field outlines on dated imagery; the 460-point terrace sample;
  a geology check west of 74.66 E; a Landsat 8-only run.
