# Where the work stands: 7 October 2026

**Done:** analysis (Phases 1, 2, 4 gate test, wide box, sensitivity, long series), accuracy sample passes 1 and 2, the check of
the flagged points against imagery of 2013-2014, `SS_Research_Paper.md`, `SS_Executive_Summary.md`, Development Log to Entry 27.

**Done on 7 October**
- Section 4.1 compares like with like (mean of the 201 polygons on both sides) (`phase2_timeseries/05_v1_rule_matched_statistic.py`).
- Section 4.5 shows how much of the 141 ha rests on the second labelling pass (Table 3, `west_extension/09_accuracy_by_labelling_pass.py`).
- Before check of the 85 flagged sample points: 72 vegetated in 2013-2014 imagery, 12 not, 1 unclear; kiln estimate restricted to
  points vegetated before is about 134 ha (Table 4, `west_extension/accuracy_before_pass.csv`, `10_before_check_result.py`).
- The flat tops removed by review hold 0.09 ha of strict conversion and none by the drop test, so no figure depends on them
  (`west_extension/11_removed_flat_tops_check.py`). Their labels are still first-pass labels.
- Sources: the tribunal filing (OA 364/2024) and the district list of kilns (OA 594/2022, 4 October 2023) read in full; the press
  reports checked against extracts; six statements corrected to what the sources say. The district list names kilns in the
  Bandagam-Batapora villages.
- The three-decade figure (about 335 ha) is marked as indicative. Figures 1, 2 and 4 redrawn.
- README, CITATION.cff, DATA_ACCESS.md, requirements.txt and the dashboard rebuilt on the revised analysis.

**Still open**
1. PDFs of the paper and summary, a `v2.0` tag, and replacement of the September preprint.
2. Optional, none of it needed for the results as stated: a second labeller for the 120 points; labels for the 460-point terrace
   reference sample; a like-for-like Sentinel-2 composite to explain the 8.43%; geology west of 74.66 E; reading the press
   reports through in the original; a run with the cirrus and saturation flags masked.
