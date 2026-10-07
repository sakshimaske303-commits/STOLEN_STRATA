# Where the work stands: 7 October 2026

**Done:** analysis (Phases 1, 2, 4 gate test, wide box, sensitivity, long series), accuracy sample passes 1 and 2,
`SS_Research_Paper.md`, `SS_Executive_Summary.md`, Development Log to Entry 26.

**Done on 7 October, after a full re-check of the folder:**
- Section 4.1 now compares like with like (mean of the 201 polygons on both sides) and says what is and is not known about the cause
  (`phase2_timeseries/05_v1_rule_matched_statistic.py`). Figure 2 redrawn.
- Section 4.5 shows how much of the 141 ha rests on the second labelling pass (Table 3, `west_extension/09_accuracy_by_labelling_pass.py`).
- The three-decade figure (about 335 ha) is marked as indicative, with reasons. Figure 4 now shows 1999–2002 as well.
- Wording corrected: the five flat tops removed in the original box, the 2001 anomaly at Rangeen Kultreh, the terrace count (187 pass the rule, 180 kept).
- Figure 1 redrawn with scale bar, north arrow and coordinates (`paper_figures/make_maps.py`).
- GEDI cells without shots are now left out (`phase4_elevation/01_elevation_gate_test.py`); the terrace rows did not change.
- README, CITATION.cff, DATA_ACCESS.md, requirements.txt and the dashboard rebuilt on the revised analysis.

**Still open, in order**
1. "Before" check in Google Earth Pro (`west_extension/accuracy_sample_points.kml`, historical imagery 2013–2014), for the 85 flagged points.
   22 were viewed earlier with the AI assistant on screenshots (all vegetated before) but not recorded: they have to be redone alone and entered in
   `west_extension/accuracy_before_pass.html`, then `accuracy_before_pass.csv` saved into `west_extension/`.
   Rule: field with bunds = vegetated even if harvested; kiln, brick rows, dug ground, building, road = not_vegetated. Check closely: 91, 101, 31.
2. Join to the key; add the result to paper Section 4.5 and update the limitation that says this check is not done.
3. Read every cited source in the original (NGT OA 364/2024 report first). Then resolve or keep the Kashmir Despatch paragraph in Section 4.6.
4. Label the five removed flat tops myself (`phase1_delineation/review_checklist.csv`, column `my_label`).
5. Move the first-version files into `archive_v1/` and push.
6. Optional: label the 460-point terrace reference sample; a like-for-like Sentinel-2 June–September composite to explain the 8.43%;
   a second labeller; geology west of 74.66° E; a before/after image pair for Rangeen Kultreh.
7. PDFs of the paper and summary, and replacement of the September preprint.
